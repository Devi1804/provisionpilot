# Internal Platform Notes — Q1 2025

## Incident 2025-02-14 — All M-series provisioning broken

### Summary
After upgrading vagrant-qemu plugin to 0.3.x, every VM bring-up on
Apple Silicon engineers' workstations failed with "Invalid CPU model".

### Root cause
Our Vagrantfile template specified `qe.cpu = "cortex-a72"`. This worked
while QEMU silently fell back to TCG, but with HVF acceleration enabled
by default in 0.3.x, the CPU model is validated strictly. HVF on Apple
Silicon only accepts: `cortex-a53`, `cortex-a57`, `host`, `max`.

### Fix
Changed `Vagrantfile.j2` to use `qe.cpu = "host"` unconditionally. As a
side benefit, HVF can now use native CPU features for a measurable speedup.

### Lessons
- Don't rely on silent fallbacks; pin to known-good values.
- Test Vagrantfile changes against both Intel and Apple Silicon hosts
  in CI before merging.

## Other Open Issues

- vagrant-qemu silently ignores `config.vm.network` settings. For
  multi-NIC bonding demos, use kernel `dummy` interfaces inside the VM
  rather than relying on hypervisor-attached NICs. See RB-031.

- SSH port collisions: vagrant-qemu defaults every VM to host port 50022.
  Set `qe.ssh_port` per VM. We allocate sequentially from 50022.