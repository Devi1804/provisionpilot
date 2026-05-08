# Ansible-core 2.18 Release Notes

Released November 2024.

## Breaking Changes
- Python 3.10 removed from controller support. Minimum is now 3.11.
- The deprecated string form of netplan `parameters` is now an error.
- ansible-galaxy collection install no longer accepts SHA-1 only checksums.

## Features
- New `--check-with-diff` flag combines --check and --diff in one pass
- Inventory plugins can now declare schema for validation

## Known Issues
- Some collections (notably community.libvirt < 1.4) are incompatible
  with the new Python 3.11 minimum. Pin ansible-core<2.18 if you need these.