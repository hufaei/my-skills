param(
  [ValidateSet("all", "codex", "claude")]
  [string]$Target = "codex",
  [ValidateSet("global", "project")]
  [string]$Scope = "project",
  [string]$ProjectRoot = (Get-Location).Path,
  [string]$CodexHome,
  [string]$ClaudeHome
)

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$skillsRoot = Join-Path $scriptDir "skills"
$skills = Get-ChildItem -Path $skillsRoot -Directory | Sort-Object Name | ForEach-Object { $_.Name }

function Get-SkillRootForScope([string]$scope, [string]$kind) {
  if ($kind -eq "codex") {
    if ($scope -eq "project") {
      return Join-Path $ProjectRoot ".codex\skills"
    }
    return "$HOME\.codex\skills"
  }

  if ($scope -eq "project") {
    return Join-Path $ProjectRoot ".claude\skills"
  }
  return "$HOME\.claude\skills"
}

if ([string]::IsNullOrWhiteSpace($CodexHome)) {
  if ($Scope -eq "project") {
    $CodexHome = Join-Path $ProjectRoot ".codex\skills"
  } else {
    $CodexHome = "$HOME\.codex\skills"
  }
}

if ([string]::IsNullOrWhiteSpace($ClaudeHome)) {
  if ($Scope -eq "project") {
    $ClaudeHome = Join-Path $ProjectRoot ".claude\skills"
  } else {
    $ClaudeHome = "$HOME\.claude\skills"
  }
}

$destinations = @()
if ($Target -eq "all" -or $Target -eq "codex") {
  $destinations += @{ Name = "codex"; Root = $CodexHome }
}
if ($Target -eq "all" -or $Target -eq "claude") {
  $destinations += @{ Name = "claude"; Root = $ClaudeHome }
}

$codexRoot = Split-Path -Parent $CodexHome
$previousCodexHome = $env:CODEX_HOME
$env:CODEX_HOME = $codexRoot

try {
  foreach ($destination in $destinations) {
    $destRoot = $destination.Root
    New-Item -ItemType Directory -Force -Path $destRoot | Out-Null
    $isCodexRoot = $destination.Name -eq "codex"
    $alternateScope = if ($Scope -eq "project") { "global" } else { "project" }
    $alternateRoot = Get-SkillRootForScope $alternateScope $destination.Name

    foreach ($skillName in $skills) {
      $sourceDir = Join-Path $skillsRoot $skillName
      $destDir = Join-Path $destRoot $skillName
      $alternateSkillDir = Join-Path $alternateRoot $skillName

      if ($alternateRoot -ne $destRoot -and (Test-Path $alternateSkillDir)) {
        Remove-Item -Path $alternateSkillDir -Recurse -Force
        Write-Host "Removed opposite-scope $skillName from $alternateRoot"
      }

      if (Test-Path $destDir) {
        Get-ChildItem -Path $destDir -Exclude "node_modules" | Remove-Item -Recurse -Force
      }
      New-Item -ItemType Directory -Force -Path $destDir | Out-Null

      Get-ChildItem -Path $sourceDir | Where-Object { $_.Name -ne "node_modules" } | ForEach-Object {
        Copy-Item -Path $_.FullName -Destination $destDir -Recurse -Force
      }

      if (-not $isCodexRoot) {
        $openAiYaml = Join-Path $destDir "agents\openai.yaml"
        if (Test-Path $openAiYaml) {
          Remove-Item -Path $openAiYaml -Force
        }
      }

      Write-Host "Installed $skillName -> $destDir"
      $setupScript = Join-Path $destDir "scripts\setup.js"
      if (Test-Path $setupScript) {
        Push-Location $destDir
        try {
          node scripts/setup.js
          if ($LASTEXITCODE -ne 0) {
            throw "Setup failed for $skillName"
          }
        } finally {
          Pop-Location
        }
      }
    }
  }
} finally {
  $env:CODEX_HOME = $previousCodexHome
}

Write-Host ""
Write-Host "Installed skills for target=$Target scope=$Scope."
Write-Host "Codex root: $CodexHome"
Write-Host "Claude root: $ClaudeHome"
