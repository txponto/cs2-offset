# CS2-ESP Offsets and Web Radar Asset Backup

This repository supports [CS2-ESP](https://cs2-esp.xyz/) by providing the offset data and backup assets used by its desktop overlay and browser-based radar.

It is an infrastructure repository rather than a standalone application. The files stored here may be updated or replaced as Counter-Strike 2 changes, and they are intended to be consumed by the CS2-ESP launcher and related services.

## What this repository supports

- Offset data required by the external CS2 overlay
- Backup assets used by the Web Radar interface
- Recovery of required resources when a primary asset source is unavailable
- Compatibility maintenance following relevant Counter-Strike 2 updates

## CS2 Web Radar

Web Radar is the browser-based companion to the desktop overlay. It displays live player positions, loadouts, bomb location, and bomb timing information in a browser. The radar can run at the same time as the desktop ESP, so using one does not require disabling the other.

Read the [CS2 Web Radar overview](https://cs2-esp.xyz/web-radar) for an explanation of the browser view and how it works with the desktop overlay.

## Setup and usage

This repository does not contain the public setup instructions for the launcher. Installation, menu controls, Web Radar setup, configuration details, and troubleshooting steps are maintained in the official [CS2-ESP documentation](https://cs2-esp.xyz/documentation).

## Availability

Because this repository acts as a live resource source and backup, file names, formats, and contents may change without notice. Avoid building third-party dependencies around individual files unless you control the integration and can accommodate future changes.

## Important notice

CS2-ESP is third-party software and is not affiliated with or endorsed by Valve Corporation. Use of third-party game software can carry account and enforcement risk. No compatibility or account-safety guarantee is implied by the availability of files in this repository.

For product information, current features, and access options, visit the [official CS2-ESP website](https://cs2-esp.xyz/).
