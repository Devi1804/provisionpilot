# Vagrant 2.4.0 Release Notes

Released October 2023.

## FEATURES:

- core: Add architecture support [GH-13239]

## IMPROVEMENTS:

- communicator/ssh: Add key type detection on insecure key replacement [GH-13219]
- core: Extract box files as sparse files [GH-13252]
- keys: Add ed25519 insecure private key [GH-13219]
- util/downloader: Perform best effort revocation checks on Windows [GH-13214]
- util/keypair: Add support for generating ed25519 key pairs [GH-13219]

## BUG FIXES:

- core: Fix extension installation path [GH-13215]
- provider/virtualbox: Fix ipv6 static network configuration [GH-13241]

## VAGRANT-GO:

- Add basic support for HCL based config [GH-13257]