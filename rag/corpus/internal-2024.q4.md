# Internal Platform Notes — Q4 2024

Decision log and known-issue tracker for the ProvisionPilot fleet.
Owned by the platform team. Update on every incident or decision.

## Decisions

### 2024-11-08: Pin perk/ubuntu-2204-arm64 to box version 20240619+
Earlier versions (e.g., 20240515) ship a broken cloud-init that hangs
on first boot for 10+ minutes waiting on a metadata service that
doesn't exist in our network. Confirmed fixed in 20240619.

### 2024-12-03: Move from libvirt to QEMU provider on Apple Silicon
Vagrant 2.4.0 with the libvirt provider leaks tap interfaces on every
destroy. Cumulative leakage requires manual `ip link delete tap<N>`
or a host reboot. The QEMU provider doesn't have this issue.

## Known Issues

- Ubuntu 22.04 with kernel 5.15.0-100 has a regression where bond0
  fails to come up if both interfaces use DHCP. Workaround: set static
  IPs on both bond members in netplan. Tracked: PROV-148.

- ansible.posix.netplan silently drops bond `parameters` if specified
  as a string. Always use the dict form. See ansible-2.17 release notes.