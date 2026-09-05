#!/usr/bin/env bash
set -e

# Homebrew...
/usr/bin/xattr -rc Universal-Binaries || true
find Universal-Binaries -name .DS_Store -delete || true
hdiutil create -srcfolder Universal-Binaries tmp.dmg -volname "OpenCore Patcher Resources (Root Patching)" -fs APFS -ov -format UDRO -megabytes 4096
if security find-identity -v -p codesigning | grep -q "OpenCore Legacy Patcher Software Signing"; then
    codesign -s "OpenCore Legacy Patcher Software Signing" Universal-Binaries.dmg
elif security find-identity -v -p codesigning | grep -q "OCLP Self Signed"; then
    codesign -s "OCLP Self Signed" Universal-Binaries.dmg
else
    codesign -s - Universal-Binaries.dmg
fi
rm tmp.dmg
