# Ubuntu 22.04.3 LTS Release Notes

Released August 2023.

## Highlights
- HWE kernel updated to Linux 6.2
- ARM64 image now ships with cloud-init 23.1
- Resolved bonding regression from 22.04.2

## Bug Fixes
- Fixed bond0 interface failing to come up when both members use DHCP
- netplan apply no longer silently drops bond parameters specified as strings
- Improved boot performance on virtio-blk storage

## Security
- OpenSSL updated to 3.0.10
- Fixed CVE-2023-2650 in OpenSSL OBJ_obj2txt