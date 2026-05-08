# QEMU 8.2 Release Notes

Released December 2023.

## ARM
- Improved virt machine emulation for aarch64
- Added support for Cortex-A710, Cortex-A715, Cortex-X3 CPU models
- The `host` CPU model now correctly reports SVE2 features on Apple Silicon

## Networking
- virtio-net-pci performance improvements (~15% throughput on aarch64)
- New socket-based netdev for inter-VM communication

## Known Issues
- HVF accelerator on Apple Silicon does NOT support cortex-a72 CPU model.
  Use `cpu=host` or `cpu=max` for HVF on M-series Macs.
- Live migration between hosts with different page sizes is not supported.