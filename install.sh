#!/usr/bin/env bash
BASEDIR=$(dirname "$0")
cd "$BASEDIR" || exit

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

LOGO="logo.png"
START_FILE="start.sh"

cat >~/.local/share/applications/music_library.desktop <<EOL
[Desktop Entry]
Type=Application
Encoding=UTF-8
Name=Music Library
Comment=An easy way to find your music
Exec=${BASEDIR}/${START_FILE}
Icon=${BASEDIR}/${LOGO}
Terminal=false
EOL


