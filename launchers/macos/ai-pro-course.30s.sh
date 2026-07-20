#!/usr/bin/env bash
# <bitbar.title>AI Pro-level Course</bitbar.title>
# <bitbar.version>v0.1</bitbar.version>
# <bitbar.desc>Open today's AI Pro-level Course lesson</bitbar.desc>

# EDIT THIS PATH to the repo root on your Mac.
REPO_ROOT="${HOME}/Work/AIProCourse"

# Status line (shown in menu bar)
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; then
  echo "AIC •"
else
  echo "AIC ○"
fi

echo "---"
echo "Open today's lesson | href=http://localhost:3000/"
echo "Open schedule | href=http://localhost:3000/schedule"
echo "Open search | href=http://localhost:3000/search"
echo "Progress | href=http://localhost:3000/progress"
echo "---"
echo "Start dev server | bash='${REPO_ROOT}/launchers/macos/start-server.sh' terminal=false refresh=true"
echo "Open repo in Finder | bash='/usr/bin/open' param1='${REPO_ROOT}' terminal=false"
echo "Refresh | refresh=true"
