# Launchers — Open AI Catalyst on any machine

One click / one shortcut to: **start the dev server (if needed) → open today's lesson in your browser**.

## macOS — Menu-bar icon (SwiftBar)

1. Install [SwiftBar](https://github.com/swiftbar/SwiftBar) (`brew install --cask swiftbar`).
2. Copy `macos/ai-catalyst.30s.sh` to `~/Library/Application Support/SwiftBar/`.
3. `chmod +x` the file.
4. In SwiftBar preferences, set Plugin Folder to that directory.
5. An "AIC" item appears in your menu bar with a "Open today's lesson" action.

The script:
- Checks if `http://localhost:3000` is up; if not, `cd` into the repo's `app/` and runs `npm run dev` in the background.
- Opens the home route (which routes to today's lesson).

## Windows — System tray

Two simple options:

### Option A — desktop shortcut (simplest)

Create a shortcut to `windows/open-aicatalyst.bat`. Pin it to the taskbar.

### Option B — persistent system-tray icon

Install [AutoHotkey v2](https://www.autohotkey.com/), then run `windows/AICatalyst-Tray.ahk`. This creates a persistent tray icon with right-click menu (Open today, Open schedule, Start dev server, Stop dev server, Open repo).

Set it to launch at login via `shell:startup` if you want it always available.

## Both platforms — how the launcher decides "today's lesson"

The launcher just opens `http://localhost:3000/` — the app itself computes today's slot from `curriculum.json` + today's date and renders the correct lesson. No launcher logic needed.
