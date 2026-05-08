# Internal Platform Runbook — Q2 2025

Operational guidance for engineers running ProvisionPilot.

## RB-031: Multi-NIC bonding on vagrant-qemu

Because vagrant-qemu can't expose multiple host-attached NICs, we use
kernel dummy interfaces to demonstrate bonding configuration. The
bonding logic (mode, members, addresses, MII monitor) is identical
to a physical-NIC setup; only the underlying interface type differs.

Steps performed by the network role:
1. Load `bonding` and `dummy` kernel modules
2. Create dummy0 and dummy1 via `ip link add type dummy`
3. Bring both interfaces up
4. Apply netplan config with bond0 over [dummy0, dummy1]

Verification: `ip addr show bond0` should show the bond IP and slaves.

## RB-032: SSH port allocation

Every VM in our Vagrantfile must declare `qe.ssh_port`. Allocate
sequentially starting at 50022:
- 50022–50031: web tier
- 50032–50041: db tier
- 50042–50051: app tier

The Vagrantfile.j2 template auto-allocates from the rendered spec.

## RB-033: Ansible upgrade caveats

- Pin `ansible-core<2.18` if any role uses `community.libvirt < 1.4`.
- After 2.17, the netplan module's `parameters` argument MUST be a
  dict; the string form now errors.
- After 2.18, the controller requires Python 3.11. Verify the venv
  with `python --version` before running playbooks.