# Ansible-core 2.16 Release Notes

Released November 2023.

## Highlights
- Python 3.10+ required on controller (Python 3.9 deprecated)
- New `ansible.posix.netplan` module for declarative netplan config
- Improved `--diff` output for template module

## Module Changes
- The `setup` module now collects bonded interface details under
  ansible_facts.bonding
- Added `bond_mode` and `bond_members` to the network facts schema

## Bug Fixes
- ansible-pull no longer silently fails on shallow clones
- become_method=sudo correctly preserves environment with -E