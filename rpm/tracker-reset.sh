#/bin/sh
if [ ! -e ~/.local/share/localsearch-migrated ]; then
    tracker3 reset -s
    touch ~/.local/share/localsearch-migrated
fi
