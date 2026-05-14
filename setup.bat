@echo off
echo.
echo [bold cyan]AutoOSINT: One-Click Installer[/bold cyan]
echo ------------------------------------------
echo.

echo [+] Installing dependencies...
pip install -r requirements.txt

echo [+] Installing AutoOSINT globally...
pip install .

echo.
echo [+] Testing installation...
autoosint --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] WARNING: 'autoosint' command not found in PATH.
    echo [!] You can still run it using: python cli.py
    echo [!] To fix this, add your Python Scripts folder to your Windows PATH.
) else (
    echo [bold green]SUCCESS![/bold green] You can now use 'autoosint' from any terminal.
)

pause
