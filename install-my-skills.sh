#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="codex"
SCOPE="project"
PROJECT_ROOT="$(pwd)"
CODEX_HOME_DIR=""
CLAUDE_HOME_DIR=""
SKILLS=()
for skill_dir in "$SCRIPT_DIR"/skills/*; do
  [ -d "$skill_dir" ] || continue
  SKILLS+=("$(basename "$skill_dir")")
done

while [ "$#" -gt 0 ]; do
  case "$1" in
    --target)
      TARGET="${2:?missing value for --target}"
      shift 2
      ;;
    --scope)
      SCOPE="${2:?missing value for --scope}"
      shift 2
      ;;
    --project-root)
      PROJECT_ROOT="${2:?missing value for --project-root}"
      shift 2
      ;;
    --codex-home)
      CODEX_HOME_DIR="${2:?missing value for --codex-home}"
      shift 2
      ;;
    --claude-home)
      CLAUDE_HOME_DIR="${2:?missing value for --claude-home}"
      shift 2
      ;;
    *)
      echo "Unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

case "$TARGET" in
  all|codex|claude) ;;
  *)
    echo "Invalid --target: $TARGET" >&2
    exit 1
    ;;
esac

case "$SCOPE" in
  global|project) ;;
  *)
    echo "Invalid --scope: $SCOPE" >&2
    exit 1
    ;;
esac

get_skill_root_for_scope() {
  local scope="$1"
  local kind="$2"
  if [ "$kind" = "codex" ]; then
    if [ "$scope" = "project" ]; then
      printf '%s/.codex/skills' "$PROJECT_ROOT"
    else
      printf '%s/.codex/skills' "$HOME"
    fi
    return
  fi

  if [ "$scope" = "project" ]; then
    printf '%s/.claude/skills' "$PROJECT_ROOT"
  else
    printf '%s/.claude/skills' "$HOME"
  fi
}

if [ -z "$CODEX_HOME_DIR" ]; then
  if [ "$SCOPE" = "project" ]; then
    CODEX_HOME_DIR="$PROJECT_ROOT/.codex/skills"
  else
    CODEX_HOME_DIR="$HOME/.codex/skills"
  fi
fi

if [ -z "$CLAUDE_HOME_DIR" ]; then
  if [ "$SCOPE" = "project" ]; then
    CLAUDE_HOME_DIR="$PROJECT_ROOT/.claude/skills"
  else
    CLAUDE_HOME_DIR="$HOME/.claude/skills"
  fi
fi

DEST_NAMES=()
DEST_ROOTS=()
if [ "$TARGET" = "all" ] || [ "$TARGET" = "codex" ]; then
  DEST_NAMES+=("codex")
  DEST_ROOTS+=("$CODEX_HOME_DIR")
fi
if [ "$TARGET" = "all" ] || [ "$TARGET" = "claude" ]; then
  DEST_NAMES+=("claude")
  DEST_ROOTS+=("$CLAUDE_HOME_DIR")
fi

CODEX_ROOT_DIR="$(dirname "$CODEX_HOME_DIR")"
export CODEX_HOME="$CODEX_ROOT_DIR"

for index in "${!DEST_ROOTS[@]}"; do
  dest_root="${DEST_ROOTS[$index]}"
  dest_name="${DEST_NAMES[$index]}"
  mkdir -p "$dest_root"
  if [ "$SCOPE" = "project" ]; then
    alternate_scope="global"
  else
    alternate_scope="project"
  fi
  alternate_root="$(get_skill_root_for_scope "$alternate_scope" "$dest_name")"

  for skill_name in "${SKILLS[@]}"; do
    source_dir="$SCRIPT_DIR/skills/$skill_name"
    dest_dir="$dest_root/$skill_name"
    alternate_skill_dir="$alternate_root/$skill_name"

    if [ "$alternate_root" != "$dest_root" ] && [ -d "$alternate_skill_dir" ]; then
      rm -rf "$alternate_skill_dir"
      echo "Removed opposite-scope $skill_name from $alternate_root"
    fi

    mkdir -p "$dest_dir"
    if [ -d "$dest_dir" ]; then
      find "$dest_dir" -mindepth 1 -maxdepth 1 \
        ! -name 'node_modules' \
        -exec rm -rf {} +
    fi
    for item in "$source_dir"/* "$source_dir"/.[!.]* "$source_dir"/..?*; do
      [ -e "$item" ] || continue
      name="$(basename "$item")"
      [ "$name" = "node_modules" ] && continue
      cp -r "$item" "$dest_dir/"
    done

    if [ "$dest_name" != "codex" ] && [ -f "$dest_dir/agents/openai.yaml" ]; then
      rm -f "$dest_dir/agents/openai.yaml"
    fi

    echo "Installed $skill_name -> $dest_dir"
    if [ -f "$dest_dir/scripts/setup.js" ]; then
      (cd "$dest_dir" && node scripts/setup.js)
    fi
  done
done

echo ""
echo "Installed skills for target=$TARGET scope=$SCOPE."
echo "Codex root: $CODEX_HOME_DIR"
echo "Claude root: $CLAUDE_HOME_DIR"
