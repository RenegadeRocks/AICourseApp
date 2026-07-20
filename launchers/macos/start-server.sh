#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${HOME}/Work/AIProCourse"

cd "${REPO_ROOT}/app"

# If port already in use, do nothing.
if lsof -iTCP:3000 -sTCP:LISTEN -n -P >/dev/null 2>&1; then
  echo "Dev server already running on :3000"
  exit 0
fi

# Detached, logs to file
nohup npm run dev > "${REPO_ROOT}/launchers/macos/dev.log" 2>&1 &
disown
echo "Started dev server; logs: ${REPO_ROOT}/launchers/macos/dev.log"
