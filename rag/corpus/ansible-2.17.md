# Ansible-core 2.17 Release Notes

Released May 2024.

## Highlights
- Python 3.7-3.9 dropped from controller (3.10+ required)
- Performance improvements for large inventories (>500 hosts)
- New `dump_inventory` plugin for debugging dynamic inventories

## Module Changes
- ansible.posix.netplan: `parameters` argument now requires dict form.
  String form is deprecated and will warn loudly. Will be removed in 2.19.
- The `command` module's `creates` argument now supports glob patterns.

## Deprecations
- `set_fact` will warn when assigning a fact whose name shadows
  a built-in ansible_facts key.