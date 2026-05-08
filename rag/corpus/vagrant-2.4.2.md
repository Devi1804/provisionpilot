# Vagrant 2.4.3 Release Notes

Released June 2024.

## FEATURES:

- provider/virtualbox: Add support for VirtualBox 7.1 [GH-13513]

## IMPROVEMENTS:

- core: Always downcase type value when getting digest for checksum calculation [GH-13471]
- core: Activate all runtime dependencies at startup [GH-13526]
- guest/debian: Fix NFS install capability to prevent hang on install [GH-13411]
- kernel_v2/config: Add warning for IPv6 address ending with :1 [GH-13362]
- provider/docker: Properly match container ID when trailing output is present [GH-13475]
- provider/docker: Support build with containerd storage [GH-13343]
- provider/virtualbox: Allow paused state when booting vm [GH-13496]
- provider/virtualbox: Handling warnings in output when detecting version [GH-13394]
- synced_folder/nfs: Output mounting entry [GH-13383]
- synced_folder/smb: Adjust ordering in mount entry output [GH-13383]

## BUG FIXES:

- command/cloud: Fix provider upload [GH-13467]
- host/bsd: Use nfsd update command instead of restart [GH-13490]
- kernel_v2/config: Fix IP address check [GH-13494] 
- provider/docker: Prevent error if network configuration data is missing [GH-13337, GH-13373]
- provider/docker: Fix docker-exec commands to pass kwargs correctly [GH-13488]
- provider/docker: Fix docker to not rebuild image if it already exists [GH-13489]
- provider/virtualbox: Prevent encoding errors within error translation [GH-13525]
- provider/hyperv: Fix configure disks capability [GH-13346]
- provisioner/ansible: Fix version detection [GH-13375]
- provisioner/ansible: Support double digit versions [GH-13493]
- provisioner/salt: Fix bootstrap script URLs [GH-13517]
- synced_folder/nfs: Fix upstart detection [GH-13409]

## VAGRANT-GO: