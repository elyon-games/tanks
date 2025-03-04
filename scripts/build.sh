#!/bin/bash

current_dir="$(dirname "$0")/../"
src_path="${current_dir}src/main.py"
assets_path="${current_dir}assets"
config_path="${current_dir}config"
public_server="${current_dir}src/server/public"

source ./venv/bin/activate

./venv/bin/pyinstaller --add-data "$config_path:config" --add-data "$public_server:server_public_files" --add-data "$assets_path:assets" --onefile "$src_path" --icon="${assets_path}/logo/round.ico"