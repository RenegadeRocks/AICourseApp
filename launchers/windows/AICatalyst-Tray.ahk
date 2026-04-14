; AI Catalyst C3 — Windows system tray launcher (AutoHotkey v2)
; Save and double-click to get a persistent tray icon with a right-click menu.
; Requires AutoHotkey v2.

#Requires AutoHotkey v2.0

RepoRoot := A_ScriptDir . "\..\.."
AppDir := RepoRoot . "\app"

TraySetIcon "shell32.dll", 44
A_IconTip := "AI Catalyst C3"

tray := A_TrayMenu
tray.Delete()
tray.Add("Open today's lesson", OpenToday)
tray.Add("Open schedule", (*) => Run("http://localhost:3000/schedule"))
tray.Add("Open search", (*) => Run("http://localhost:3000/search"))
tray.Add("Open progress", (*) => Run("http://localhost:3000/progress"))
tray.Add()
tray.Add("Start dev server", StartServer)
tray.Add("Stop dev server", StopServer)
tray.Add("Open repo folder", (*) => Run("explorer.exe " . RepoRoot))
tray.Add()
tray.Add("Exit", (*) => ExitApp())
tray.Default := "Open today's lesson"

OpenToday(*) {
    if !IsServerUp() {
        StartServer()
        Sleep 3000
    }
    Run("http://localhost:3000/")
}

StartServer(*) {
    if IsServerUp() {
        TrayTip "AI Catalyst", "Dev server already running.", 3
        return
    }
    Run('cmd /c "cd /d ' . AppDir . ' && npm run dev"', , "Min")
    TrayTip "AI Catalyst", "Starting dev server…", 3
}

StopServer(*) {
    RunWait('cmd /c "for /f `"tokens=5`" %a in (''netstat -ano ^| findstr :3000 ^| findstr LISTENING'') do taskkill /pid %a /f"', , "Hide")
    TrayTip "AI Catalyst", "Stopped any process listening on :3000.", 3
}

IsServerUp() {
    try {
        req := ComObject("MSXML2.XMLHTTP")
        req.Open("GET", "http://localhost:3000/", false)
        req.Send()
        return req.Status = 200
    } catch {
        return false
    }
}
