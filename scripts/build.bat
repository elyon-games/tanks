@echo off
setlocal enabledelayedexpansion
set "current_dir=%~dp0../"
set "src_path=%current_dir%src/main.py"
set "assets_path=%current_dir%assets"
set "config_path=%current_dir%config"
set "pulic_server=%current_dir%src/server/public"

call "%current_dir%venv/Scripts/activate.bat"
pyinstaller --add-data "%config_path%:config" --add-data "%pulic_server%:server_public_files" --add-data "%assets_path%:assets" --onefile "%src_path%" --icon="%assets_path%\logo\round.ico"

pause
