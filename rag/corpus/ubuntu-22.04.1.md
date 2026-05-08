# Ubuntu 22.04.1 LTS Release Notes

First point release of Jammy Jellyfish, released August 2022.

## Highlights
- Updated to Linux kernel 5.15.0-46
- Mesa graphics stack updated to 22.0.5
- Improved support for ARM64 server installations
- OpenSSL 3.0.2 with backported security fixes

## Known Issues
- cloud-init may fail to apply network configuration on systems with
  multiple NICs if no priority is specified.
- Some VMware guests experience slow boot times. Workaround: disable
  VMware's "Accelerate 3D Graphics" option.

## Bug Fixes
- Fixed apt sources list corruption during do-release-upgrade
- netplan now correctly handles bond interfaces with VLAN tags
- Update the Ubuntu logo to the new branding for the Install Ubuntu screen.