# vØrk

[vØrk](https://github.com/vooteleaer/vork) connects your own devices into one private network, with no account and no company in the middle. With this add-on, Home Assistant is one of your devices: your phone and laptop reach it by name from anywhere, and nothing else can.

> vØrk is an early prototype: it runs every day on its author's machines, but nothing has been audited and the network format may still change between versions. Keep your devices on the same version.

## Getting started

1. Install the add-on and start it. Turn on **Show in sidebar** if you like: the dashboard is then in Home Assistant's sidebar.
2. **Open Web UI** opens the node's dashboard inside Home Assistant, signed in by Home Assistant. (The same dashboard is also on `https://<home assistant>:30742`, for a browser outside Home Assistant: open it with the private link the **Log** tab prints.)
3. Link your devices: in the dashboard, **Devices → Show a code**, and scan it with the vØrk app on your phone (or open the link on another device's dashboard). Your devices are one group: link Home Assistant to one of them and it is linked to all.

If linking doesn't get through (Home Assistant can't reach the device that made the code), give it a connection first: **Settings → Connections**, add `host:port` of a node of yours that is reachable from the internet (or one of the [public nodes to start from](https://github.com/vooteleaer/vork#public-nodes-to-start-from)), then use the link again.

Then, from any of your devices, wherever they are: **`http://homeassistant.vork:8123`** (or its fixed IPv4 address, shown in the dashboard).

## Options

- **`name`**: Home Assistant's name in your network, so `name.vork` (default `homeassistant`). It's given to the node when the add-on is first started and whenever you change it here; a name changed on the dashboard (**Settings**) stays after a restart.

The node's other settings are in its dashboard (**Settings**), and in `/data/vork.toml` in the add-on's data.

## The router

The node picks a UDP port of its own at the first start and asks the router to open it (UPnP, PCP). If the router doesn't, the dashboard's **Settings → Network** says so and which port to forward by hand; you can choose the port there too. Without an open port everything still works: what can't connect directly goes through relays.

## Names inside Home Assistant

Your devices reach Home Assistant by name with nothing to set up. The other way round, Home Assistant and its add-ons ask the Supervisor's DNS for names, which this add-on doesn't change (another add-on that did that broke name resolution for some people). For an integration that should reach one of your devices:

- use the device's vØrk IPv4 address (`198.18.x.x`, the same everywhere, shown in the dashboard: it doesn't change).

`.vork` names inside Home Assistant itself aren't supported yet.

## Exit node

Home Assistant can be an exit node for your devices (their internet through home when they're on someone else's Wi-Fi): the dashboard's **Exit node** page. The exit answers its clients' names itself, from Home Assistant's own resolver, so they don't depend on outside DNS servers being reachable.

## Security

Only your linked devices reach Home Assistant through vØrk. Other vØrk nodes may carry traffic for you but can't open a connection to it (the walled garden). The add-on needs the host network, `NET_ADMIN` and `/dev/net/tun` for its network interface.
