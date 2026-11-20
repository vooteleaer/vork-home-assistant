#!/bin/sh
# The vØrk node in Home Assistant: its configuration and identity made at
# the first start in /data (kept in backups), then run with the vork0
# interface. Home Assistant's own DNS is left alone (see DOCS.md).
set -e
C=/data/vork.toml
NAME=$(sed -n 's/.*"name": *"\([^"]*\)".*/\1/p' /data/options.json 2>/dev/null)
NAME=${NAME:-homeassistant}

if [ ! -e "$C" ]; then
    vork init --config "$C" --tun vork0
    # A port of its own, so it doesn't collide with other nodes behind the
    # same router (a phone, a NAS); the router is asked to open it (UPnP, PCP).
    PORT=$(awk 'BEGIN { srand(); print 40000 + int(rand() * 20000) }')
    sed -i "s|^listen = .*|listen = \"0.0.0.0:$PORT\"|" "$C"
    # The dashboard, behind the add-on's Open Web UI button.
    sed -i 's|^# web = .*|web = "[::]:30742"|' "$C"
    grep -q '^web *=' "$C" || echo 'web = "[::]:30742"' >> "$C"
fi
# The name from the add-on's options, kept up to date.
if grep -q '^name *=' "$C"; then
    sed -i "s|^name *=.*|name = \"$NAME\"|" "$C"
elif grep -q '^# name *=' "$C"; then
    sed -i "s|^# name *=.*|name = \"$NAME\"|" "$C"
else
    echo "name = \"$NAME\"" >> "$C"
fi

echo "vØrk: $(vork version)"
# The dashboard's private link, once the node has made its key.
(
    sleep 8
    echo "The dashboard's private link (open it once; the browser keeps the key):"
    vork web-link --config "$C" 2>/dev/null | head -1
) &
exec vork run --config "$C"
