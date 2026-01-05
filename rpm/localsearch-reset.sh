#/bin/sh
if [ ! -e ~/.local/share/localsearch-migrated ]; then
    localsearch reset -s
    touch ~/.local/share/localsearch-migrated
fi
