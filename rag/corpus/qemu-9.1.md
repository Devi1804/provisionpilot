# QEMU 9.1 Release Notes

Released September 2024.

## Networking
- New netdev backend: `vhost-vdpa` for high-performance NIC passthrough
- Improved user-mode networking SLIRP performance
- hostfwd rules now support IPv6 link-local addresses

## ARM
- Cortex-A720 CPU model added
- Improved nested virtualization support on Apple Silicon hosts
  running macOS 14.4+

## Migration Notes
- Configurations using `cpu=cortex-a72` with HVF will now error
  immediately at startup rather than silently fail. Update to
  `cpu=host` before upgrading.