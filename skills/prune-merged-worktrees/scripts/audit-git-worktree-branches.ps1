param(
  [string]$Repo = (Get-Location).Path,
  [string]$Base = "origin/dev",
  [string[]]$Keep = @("dev", "main", "master"),
  [switch]$FetchPrune,
  [switch]$Delete,
  [switch]$RemoveWorktrees,
  [switch]$Force
)

$ErrorActionPreference = "Stop"

function Invoke-Git {
  param([string[]]$Arguments)
  $output = & git -C $Repo @Arguments 2>&1
  if ($LASTEXITCODE -ne 0) {
    throw "git $($Arguments -join ' ') failed: $output"
  }
  return @($output)
}

function ConvertTo-LongPath {
  param([string]$Path)
  if ($Path.StartsWith("\\?\")) {
    return $Path
  }
  if ($Path.StartsWith("\\")) {
    return "\\?\UNC\" + $Path.TrimStart("\")
  }
  return "\\?\" + $Path
}

function Test-IsChildPath {
  param(
    [string]$Path,
    [string]$Parent
  )
  $resolvedPath = (Resolve-Path -LiteralPath $Path).Path.TrimEnd("\", "/")
  $resolvedParent = (Resolve-Path -LiteralPath $Parent).Path.TrimEnd("\", "/")
  return $resolvedPath.Equals($resolvedParent, [System.StringComparison]::OrdinalIgnoreCase) -or
    $resolvedPath.StartsWith($resolvedParent + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)
}

function Remove-DirectoryRobust {
  param([string]$Path)
  if (-not (Test-Path -LiteralPath $Path)) {
    return
  }
  $resolved = (Resolve-Path -LiteralPath $Path).Path
  Remove-Item -LiteralPath (ConvertTo-LongPath $resolved) -Recurse -Force
}

function Get-WorktreeStatus {
  param([string]$Path)
  $output = & git -C $Path status --porcelain --untracked-files=all 2>&1
  if ($LASTEXITCODE -ne 0) {
    throw "git status failed for worktree ${Path}: $output"
  }
  return @($output)
}

function Get-Worktrees {
  $lines = Invoke-Git @("worktree", "list", "--porcelain")
  $items = @()
  $current = @{}

  foreach ($line in $lines) {
    if ([string]::IsNullOrWhiteSpace($line)) {
      if ($current.ContainsKey("path")) {
        $items += [pscustomobject]$current
      }
      $current = @{}
      continue
    }

    if ($line -like "worktree *") {
      $current.path = $line.Substring(9)
    } elseif ($line -like "branch refs/heads/*") {
      $current.branch = $line.Substring(18)
    } elseif ($line -eq "bare") {
      $current.bare = $true
    } elseif ($line -eq "detached") {
      $current.detached = $true
    }
  }

  if ($current.ContainsKey("path")) {
    $items += [pscustomobject]$current
  }

  return $items
}

function Get-BranchRows {
  $format = "%(refname:short)|%(upstream:short)|%(upstream:track)|%(committerdate:iso8601)|%(objectname:short)|%(subject)"
  $lines = Invoke-Git @("branch", "--format", $format, "--sort=-committerdate")
  foreach ($line in $lines) {
    $parts = $line -split "\|", 6
    [pscustomobject]@{
      Name = $parts[0]
      Upstream = $parts[1]
      Track = $parts[2]
      Date = $parts[3]
      Commit = $parts[4]
      Subject = $parts[5]
    }
  }
}

function Get-StaleWorktreeDirectories {
  param([object[]]$Worktrees)
  $worktreesRoot = Join-Path $Repo ".worktrees"
  if (-not (Test-Path -LiteralPath $worktreesRoot)) {
    return @()
  }

  $registered = @{}
  foreach ($worktree in $Worktrees) {
    if ($worktree.PSObject.Properties.Name -contains "path" -and (Test-Path -LiteralPath $worktree.path)) {
      $registered[(Resolve-Path -LiteralPath $worktree.path).Path.TrimEnd("\", "/").ToLowerInvariant()] = $true
    }
  }

  $stale = @()
  foreach ($dir in Get-ChildItem -LiteralPath $worktreesRoot -Directory -Force) {
    $resolved = $dir.FullName.TrimEnd("\", "/").ToLowerInvariant()
    $isRegistered = $false
    foreach ($path in $registered.Keys) {
      if ($path -eq $resolved -or $path.StartsWith($resolved + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase)) {
        $isRegistered = $true
        break
      }
    }
    if (-not $isRegistered) {
      $stale += $dir.FullName
    }
  }
  return $stale
}

$repoRoot = (Resolve-Path -LiteralPath $Repo).Path
$Repo = $repoRoot

Invoke-Git @("rev-parse", "--git-dir") | Out-Null
Invoke-Git @("rev-parse", "--verify", $Base) | Out-Null

if ($FetchPrune) {
  Invoke-Git @("fetch", "--all", "--prune") | Out-Null
}

$mainBranch = (Invoke-Git @("rev-parse", "--abbrev-ref", "HEAD") | Select-Object -First 1).Trim()
$merged = @(Invoke-Git @("branch", "--format", "%(refname:short)", "--merged", $Base))
$mergedSet = @{}
foreach ($name in $merged) {
  if (-not [string]::IsNullOrWhiteSpace($name)) {
    $mergedSet[$name.Trim()] = $true
  }
}

$worktrees = @(Get-Worktrees)
$worktreeByBranch = @{}
foreach ($worktree in $worktrees) {
  if ($worktree.PSObject.Properties.Name -contains "branch" -and $worktree.branch) {
    $worktreeByBranch[$worktree.branch] = $worktree.path
  }
}

$branches = @(Get-BranchRows)
$candidates = @()
$kept = @()

foreach ($branch in $branches) {
  $worktreePath = $worktreeByBranch[$branch.Name]
  $isPrimaryWorktreeBranch = $false
  if ($branch.Name -eq $mainBranch -and $worktreePath -and (Test-Path -LiteralPath $worktreePath)) {
    $isPrimaryWorktreeBranch = (Resolve-Path -LiteralPath $worktreePath).Path -eq $repoRoot
  }
  $reason = $null

  if ($isPrimaryWorktreeBranch) {
    $reason = "current primary worktree branch"
  } elseif ($Keep -contains $branch.Name) {
    $reason = "protected branch"
  } elseif (-not $mergedSet.ContainsKey($branch.Name)) {
    $reason = "not merged into $Base"
  }

  $row = [pscustomobject]@{
    Branch = $branch.Name
    Upstream = $branch.Upstream
    Track = $branch.Track
    Commit = $branch.Commit
    Date = $branch.Date
    Subject = $branch.Subject
    Worktree = $worktreePath
    Reason = $reason
  }

  if ($reason) {
    $kept += $row
  } else {
    $candidates += $row
  }
}

Write-Host "Repository: $repoRoot"
Write-Host "Base: $Base"
Write-Host "Mode: $(if ($Delete) { 'delete' } else { 'dry-run' })"
Write-Host ""

Write-Host "Candidates merged into ${Base}:"
if ($candidates.Count -eq 0) {
  Write-Host "  none"
} else {
  foreach ($candidate in $candidates) {
    $worktree = if ($candidate.Worktree) { " worktree=$($candidate.Worktree)" } else { "" }
    Write-Host "  $($candidate.Branch) [$($candidate.Track)] $($candidate.Commit)$worktree"
  }
}

Write-Host ""
Write-Host "Kept branches:"
foreach ($branch in $kept) {
  Write-Host "  $($branch.Branch): $($branch.Reason)"
}

$staleDirectories = @(Get-StaleWorktreeDirectories $worktrees)
if ($staleDirectories.Count -gt 0) {
  Write-Host ""
  Write-Host "Unregistered directories under .worktrees:"
  foreach ($path in $staleDirectories) {
    Write-Host "  $path"
  }
}

if (-not $Delete) {
  Write-Host ""
  Write-Host "Dry-run only. Re-run with -Delete to delete candidates. Add -RemoveWorktrees to remove linked worktrees first."
  exit 0
}

$skipped = @{}
$worktreesRoot = Join-Path $repoRoot ".worktrees"

foreach ($candidate in $candidates) {
  if (-not $candidate.Worktree) {
    continue
  }

  if (-not $RemoveWorktrees) {
    Write-Warning "Skipping $($candidate.Branch): checked out at $($candidate.Worktree). Re-run with -RemoveWorktrees after verifying it is clean."
    $skipped[$candidate.Branch] = $true
    continue
  }

  if (-not (Test-Path -LiteralPath $candidate.Worktree)) {
    Write-Warning "Worktree path is missing for $($candidate.Branch): $($candidate.Worktree). Pruning stale metadata before deleting branch."
    Invoke-Git @("worktree", "prune") | Out-Null
    continue
  }

  $resolvedWorktree = (Resolve-Path -LiteralPath $candidate.Worktree).Path
  $status = @(Get-WorktreeStatus $resolvedWorktree)
  if ($status.Count -gt 0) {
    throw "Refusing to remove dirty worktree for $($candidate.Branch) at ${resolvedWorktree}:`n$($status -join "`n")"
  }

  if ((Test-Path -LiteralPath $worktreesRoot) -and (Test-IsChildPath $resolvedWorktree $worktreesRoot)) {
    Remove-DirectoryRobust $resolvedWorktree
    Invoke-Git @("worktree", "prune") | Out-Null
    Write-Host "Removed worktree directory: $resolvedWorktree"
    continue
  }

  $args = @("worktree", "remove")
  if ($Force) {
    $args += "--force"
  }
  $args += $resolvedWorktree
  Invoke-Git $args | Out-Null
  Write-Host "Removed external worktree with git: $resolvedWorktree"
}

foreach ($candidate in $candidates) {
  if ($skipped.ContainsKey($candidate.Branch)) {
    continue
  }

  Invoke-Git @("branch", "-d", $candidate.Branch) | Out-Null
  Write-Host "Deleted branch: $($candidate.Branch)"
}
