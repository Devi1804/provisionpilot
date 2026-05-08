# QEMU 9.0 Release Notes

Released April 2024.

## ARM / Apple Silicon
- HVF accelerator stability improvements on macOS
- Removed support for some legacy CPU models that never worked with HVF
- New `highmem-mmio-size` machine option for arm64 virt

## Storage
- qcow2 backing chains now validated more strictly on open
- Snapshot deletion is faster for chains longer than 5 snapshots

## Bug Fixes
- Fixed crash when starting VMs with smp=0,sockets=0
- virtio-net-pci: corrected MAC address handling on hot-plug