# Ubuntu 22.04.2 LTS Release Notes

Released February 2023 as the second point release of Ubuntu 22.04 LTS.

## Highlights
- HWE kernel updated to Linux 5.19
- Improved Apple Silicon support via the new arm64 desktop image
- systemd 249.11 with backported fixes

## Known Issues
- Bonding driver in 5.19 has a regression with active-backup mode when
  combined with VLANs. Affected users should pin to the GA kernel until 22.04.3.
- iSCSI initiator may fail to discover targets after suspend/resume.

## Networking
- netplan 0.106 includes new options for bond xmit_hash_policy
- Open vSwitch updated to 2.17.5