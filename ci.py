"""
Postprocess binaries on CI (ad-hoc signing)
"""

import subprocess
import sys
from pathlib import Path

# Configurable options
IDENTITY = "-"  # ad-hoc signing for CI/test
TARGET_DIR = Path("Universal-Binaries")
UNUSED = [
    "10.13.6-18",
    "10.13.6-19",
    "10.14.4-18",
    "10.14.4-19",
    "10.14.6-19",
    "WebDriver-387.10.10.10.40.140/WebDriver-387.10.10.10.40.140.pkg",
    "WebDriver-387.10.10.10.40.140/WebDriver-387.10.10.15.15.108.pkg",
]

MACHO_MAGIC = {
    "MH_MAGIC": b"\xfe\xed\xfa\xce",
    "MH_CIGAM": b"\xce\xfa\xed\xfe",
    "MH_MAGIC_64": b"\xfe\xed\xfa\xcf",
    "MH_CIGAM_64": b"\xcf\xfa\xed\xfe",
    "FAT_MAGIC": b"\xbe\xba\xfe\xca",
    "FAT_CIGAM": b"\xca\xfe\xba\xbe",
}


def clean_unused():
    for path in UNUSED:
        path = TARGET_DIR / path
        if path.exists():
            print(f"Removing: {path}")
            subprocess.check_output(["rm", "-rf", path])

    for path in TARGET_DIR.rglob(".DS_Store"):
        print(f"Removing: {path}")
        path.unlink()


def get_machos(directory=TARGET_DIR):
    machos: dict[Path, bytes] = {}
    for file in directory.rglob("*"):
        if not file.is_file() or file.is_symlink():
            continue
        with file.open("rb") as f:
            magic = f.read(4)
            if magic in MACHO_MAGIC.values():
                machos[file] = magic
    return dict(sorted(machos.items(), key=lambda item: item[0]))


def thin_macho(file: Path, magic: bytes):
    if magic in (MACHO_MAGIC["FAT_MAGIC"], MACHO_MAGIC["FAT_CIGAM"]):
        subprocess.check_output(["lipo", "-thin", "x86_64", "-output", file, file])


def signing_sanity_checks(file: Path) -> tuple[bool, bool]:
    with file.open("rb") as f:
        magic = f.read(4)
        if magic not in (MACHO_MAGIC["MH_CIGAM_64"], MACHO_MAGIC["FAT_CIGAM"]):
            print(f"ERROR: {file} is not a 64-bit Mach-O")
            return False, False

    result = subprocess.run(["codesign", "-dvvv", file], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if result.returncode != 0 and "not signed at all" not in result.stderr.decode():
        raise RuntimeError(f"codesign failed ({result.returncode}): {result.stderr.decode()}")

    # Если подпись отсутствует или adhoc — подписываем
    return True, True


def sign_macho(file: Path):
    print(f"Signing (ad-hoc): {file}")
    subprocess.check_output([
        "codesign", "-f", "-s", IDENTITY,
        "--preserve-metadata=entitlements",
        "--generate-entitlement-der",
        file
    ])


if __name__ == "__main__":
    clean_unused()

    machos = get_machos()
    if not machos:
        print("No machos found!")
        sys.exit(1)

    machos_to_sign = []
    all_valid = True
    for macho, _ in machos.items():
        valid, needs_signing = signing_sanity_checks(macho)
        all_valid &= valid
        if needs_signing:
            machos_to_sign.append(macho)

    if not all_valid:
        sys.exit(1)

    for macho, magic in machos.items():
        thin_macho(macho, magic)

    for macho in machos_to_sign:
        sign_macho(macho)

    print("Done! Binaries signed ad-hoc for CI/test.")
