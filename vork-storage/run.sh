#!/bin/sh
# vØrk storage in Home Assistant: vorkd with its store in /data (kept in
# backups), on the vØrk add-on's node (its local API socket in /share/vork),
# and its page (vork-web) behind Home Assistant's ingress.
set -e
B=/opt/vork-storage
STORE=/data/store
export VORK_API=/share/vork/api.sock
export VORK_STORE=$STORE
opt() { sed -n "s/.*\"$1\": *\"\([^\"]*\)\".*/\1/p" /data/options.json 2>/dev/null; }
NAME=$(opt name); NAME=${NAME:-homeassistant}
MAX=$(opt max_store); MAX=${MAX:-20G}
mkdir -p "$STORE"

# The vØrk add-on (0.6.1 or newer) makes the socket; until it runs, wait.
n=0
until [ -S "$VORK_API" ]; do
    [ $((n % 30)) -eq 0 ] && echo "waiting for the vØrk add-on's node ($VORK_API): install and start the vØrk add-on (0.6.1 or newer)"
    n=$((n + 1))
    sleep 2
done

# The media token: Home Assistant's media browser (the vork_storage
# integration) reads the libraries' files with it, and nothing else. Made
# once, kept with the add-on's data.
if [ ! -s /data/media-token ]; then
    head -c 32 /dev/urandom | od -An -tx1 | tr -d ' \n' > /data/media-token
    chmod 600 /data/media-token
fi

# Its page: only the Supervisor's ingress proxy may reach it, and it passes
# the browser's Host on; Home Assistant shows the page in a frame of its own
# origin. /media/ answers whoever holds the token.
VORK_WEB_LISTEN=0.0.0.0:8741 VORK_WEB_ALLOW=172.30.32.2/32 VORK_WEB_HOSTS='*' VORK_WEB_FRAMED=1 \
    "$B/vork-web" --store "$STORE" --media-token-file /data/media-token &
W=$!

# Tells Home Assistant where the media browser finds it: the vØrk storage
# integration (installed from this repository with HACS) offers itself.
HOST=$(hostname)
if curl -fsS -X POST -H "Authorization: Bearer ${SUPERVISOR_TOKEN}" -H "Content-Type: application/json" \
    -d "{\"service\":\"vork_storage\",\"config\":{\"host\":\"${HOST}\",\"port\":8741,\"token\":\"$(cat /data/media-token)\"}}" \
    http://supervisor/discovery >/dev/null; then
    echo "media browser: offered to Home Assistant (the vØrk storage integration) at http://${HOST}:8741"
else
    echo "media browser: Home Assistant wasn't told; set up the vØrk storage integration by hand: http://${HOST}:8741 and the token in /data/media-token"
fi

# vorkd, again if it stops; a stop of the add-on reaches it as SIGINT, on
# which it closes its store.
trap 'kill -INT $p 2>/dev/null; wait $p; kill $W 2>/dev/null; exit 0' TERM INT
while :; do
    "$B/vorkd" --store "$STORE" --device "$NAME" --no-mounts --crash-library "" --max-store "$MAX" &
    p=$!
    wait $p || true
    echo "vorkd stopped; again in 5 s"
    sleep 5
done
