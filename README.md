Flet Shift Schedule
====================

Quick start
-----------

1. (If you haven't already) create and activate a virtual environment.

Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Windows (cmd.exe):
```cmd
python -m venv .venv
.venv\Scripts\activate.bat
```

Git Bash on Windows (Mingw/MSYS):
```bash
python -m venv .venv
source .venv/Scripts/activate
```

macOS / Linux / WSL:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

If PowerShell blocks scripts, run once as admin:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app (either):

- Direct with Python:
```bash
python main.py
```

- Using the Flet CLI (recommended for web/desktop targets and dev flags):
```bash
flet run main.py --target web
```

Notes
-----
- `main.py` calls `ft.run(main)`, so running it with `python main.py` starts the Flet app.
- `flet run` provides extra CLI options (target, hot-reload, port, etc.) useful during development.
- To exit the virtual environment: `deactivate`
