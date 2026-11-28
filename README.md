# vØrk for Home Assistant

A Home Assistant add-on repository (and an integration): [vØrk](https://github.com/vooteleaer/vork), your own private network between your devices, with no account and no company in the middle. With it, your phone and laptop reach Home Assistant by name from anywhere (`http://homeassistant.vork:8123`), and nothing else can.

## Install

1. In Home Assistant: **Settings → Add-ons → Add-on store → ⋮ → Repositories**, and add `https://github.com/vooteleaer/vork-home-assistant`.
2. Install **vØrk**, start it, and follow its **Documentation** tab.
3. Optionally, **vØrk storage** too ([vork-storage](https://github.com/vooteleaer/vork-storage)): your files, photos and contacts on your own devices, with Home Assistant holding a copy. It runs on the vØrk add-on's node.
4. Optionally, your vØrk storage libraries in Home Assistant's **Media** page: in HACS, **⋮ → Custom repositories**, add this repository as an **Integration** and download **vØrk storage**; restart, and the add-on offers itself under **Settings → Devices & services**. Files are fetched as they're opened, nothing is copied.

Needs Home Assistant OS or Supervised (add-ons), on amd64 or aarch64 (a Raspberry Pi 4/5, most mini PCs).

> vØrk is an early prototype. Keep your devices on the same version.

## License

MIT, as vØrk.
