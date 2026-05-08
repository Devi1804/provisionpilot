# Vagrant 2.4.1 Release Notes

Released January 2024.

## Bug Fixes
- command/plugin: Fix plugin extension installation on Windows [GH-13328]
- communicator/ssh: Fix private key writing on Windows [GH-13329]
- core: Fix Vagrant SSL helper detection on macOS [GH-13277]
- core: Fix box collection sorting [GH-#13320]
- util/platform: Fix architecture mapping for Windows [GH-13278]

## IMPROVEMENTS

- communicator/ssh: Support ECDSA type keys for insecure key replacement [GH-13327]
- communicator/ssh: Inspect guest for supported key types [GH-13334]
- core: Update Ruby constraint to allow Ruby 3.3 [GH-13335]
- core/bundler: Force strict dependencies for default gems [GH-13336]
- provisioner/ansible: Support pip installation for RHEL >= 8 [GH-13326]
- util/keypair: Add support for ECDSA keys [GH-13327]