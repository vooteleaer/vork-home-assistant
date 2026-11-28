# vØrk storage

[vØrk storage](https://github.com/vooteleaer/vork-storage) keeps your files, photos and contacts on your own devices, encrypted, kept in sync and backed up by them, with no company in the middle. With this add-on, Home Assistant is one of those devices: it can hold a copy of your libraries (a backup at home), and you manage them from its page in Home Assistant.

> vØrk storage is an early prototype: the storage format may still change between versions and the encryption is waiting for an independent review. Keep another copy of anything important.

## Before you start

vØrk storage runs on vØrk: install the **vØrk** add-on from this repository first (version 0.6.1 or newer), start it and link Home Assistant to your devices (its Documentation tab says how). This add-on talks to the network only through the vØrk add-on's node, whose local API is in `/share/vork`.

## Getting started

1. Install the add-on and start it. Turn on **Show in sidebar** if you like.
2. **Open Web UI** opens its page inside Home Assistant, signed in by Home Assistant: your libraries, the public ones heard on the network, this device's status and settings.
3. To keep a copy of a library of yours here: open the library on another of your devices (its page or window), **Invite** with the role you want, and open the link here (**Join with link**). Libraries your devices hold are kept here too when you tell them to (**Keep all of it here**).

## Options

- **`name`**: this device's name among your devices, as vØrk storage's keep rules see it (default `homeassistant`).
- **`max_store`**: how much of the disk storage may use (`20G`, `500G`, `1T`). Your libraries' data is in the add-on's data folder, so it's in Home Assistant's backups: keep it small if your backups go somewhere small.

## In the media browser

Your libraries can be in Home Assistant's **Media** page, beside its own media and Frigate's: folders, photos, videos and music, each file fetched from vØrk storage as it's opened (from this device, or from your other devices if it isn't kept here). Nothing is copied into Home Assistant's media folder. It takes the **vØrk storage** integration:

1. In HACS: **⋮ → Custom repositories**, add `https://github.com/vooteleaer/vork-home-assistant` as an **Integration**, then download **vØrk storage** and restart Home Assistant.
2. With this add-on running, **Settings → Devices & services** shows vØrk storage as discovered: **Add**. (By hand instead: **Add integration → vØrk storage**, the address from the add-on's log and the token in its `/data/media-token`.)
3. **Media → vØrk storage**.

The integration reads files with a token only it and this add-on know; it can't change anything.

## What's not here yet

- Libraries as folders for other add-ons (Music Assistant, Plex): they need FUSE, which add-ons don't get. On a NAS beside Home Assistant, the Docker setup does it.
