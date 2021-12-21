#/bin/sh
if [ ! -e ~/.local/share/tracker-migrated ]; then
    tracker3 reset -s
    touch ~/.local/share/tracker-migrated
fi
