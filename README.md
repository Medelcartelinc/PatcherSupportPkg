# PatcherSupportPkg

A repository dedicated to Apple binaries used for patching macOS to run on legacy hardware.

### 📌 Key Features & Changes:
* **Up to date:** Synced with [`laobamac 2.0.0`](https://github.com/laobamac/PatcherSupportPkg/releases/tag/2.0.0), featuring a restored `AppleHDA` specifically for macOS Tahoe.
* **File System:** Transitioned completely to APFS due to the removal of HFS+ support starting in macOS 26.4 Beta 1.
* **Audio:** Added `AppleHDA` sourced from macOS 26.0 Beta 1.

---

## 👥 Credits & Sources

Special thanks to the following developers and projects:

* **[ASentientBot](https://github.com/ASentientBot)**
  * Mojave, Catalina, and Big Sur graphics acceleration patches.
* **[dosdude1](https://github.com/dosdude1)**
  * Brightness control for OS X El Capitan.
  * Mojave and Catalina graphics acceleration patches.
* **[Ausdauersportler](https://github.com/Ausdauersportler)**
  * Linking fixes for `AppleIntelSNBGraphicsFB.kext` and `AMDRadeonX3000.kext`.
* **[Jackluke](https://github.com/jacklukem)**, **EduCovas**, **[DhinakG](https://github.com/DhinakG)**, and **[Khronokernel](https://github.com/khronokernel)**
  * Research and development of the patch set for Intel HD 4000 graphics.
