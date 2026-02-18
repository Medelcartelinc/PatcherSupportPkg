#!/usr/bin/env python3
"""
Build PatcherSupportPkg Disk Image for local testing.
DMG is password-encrypted but NOT signed.
"""

import os
import argparse
import subprocess

UB_DIRECTORY: str = "Universal-Binaries"
DMG_NAME: str = "Universal-Binaries.dmg"
DMG_VOLNAME: str = "OpenCore Patcher Resources (Root Patching)"
DMG_SIZE: str = "4096"
DMG_FORMAT: str = "UDRW"
DMG_PASSPHRASE: str = "password"


class GenerateDiskImage:

    def __init__(self) -> None:
        print("Generating DMG (test build, no signing)")
        self._set_working_directory()
        self._strip_extended_attributes()
        self._remove_ds_store()
        self._create_dmg()
        self._convert_dmg()
        self._remove_tmp_dmg()

    def _set_working_directory(self) -> None:
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        print("  - Working directory set")

    def _strip_extended_attributes(self) -> None:
        print("  - Stripping extended attributes")
        result = subprocess.run(
            ["/usr/bin/xattr", "-rc", UB_DIRECTORY],
            capture_output=True
        )
        if result.returncode != 0:
            stderr = result.stderr.decode().strip()
            if stderr:
                print(f"    - xattr warning: {stderr}")

    def _remove_ds_store(self) -> None:
        print("  - Removing .DS_Store files")
        subprocess.run(
            ["/usr/bin/find", UB_DIRECTORY, "-name", ".DS_Store", "-delete"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )

    def _create_dmg(self) -> None:
        print("  - Creating temporary DMG (UDRW)")
        subprocess.run(
            [
                "/usr/bin/hdiutil", "create",
                "-srcfolder", UB_DIRECTORY,
                "tmp.dmg",
                "-volname", DMG_VOLNAME,
                "-fs", "APFS",
                "-format", DMG_FORMAT,
                "-megabytes", DMG_SIZE,
                "-ov"
            ],
            check=True
        )

    def _convert_dmg(self) -> None:
        print("  - Converting to encrypted ULMO DMG")
        subprocess.run(
            [
                "/usr/bin/hdiutil", "convert",
                "tmp.dmg",
                "-format", "ULMO",
                "-o", DMG_NAME,
                "-encryption",
                "-stdinpass",
                "-ov"
            ],
            input=DMG_PASSPHRASE.encode(),
            check=True
        )

    def _remove_tmp_dmg(self) -> None:
        subprocess.run(["/bin/rm", "-f", "tmp.dmg"])
        print(f"  - Temporary DMG removed. Output: {DMG_NAME}")


if __name__ == "__main__":
    GenerateDiskImage()
