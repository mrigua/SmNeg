#!/bin/sh
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Said Mrigua
# macOS only: build src/smneg/assets/icon.icns from icon.png
set -e
cd "$(dirname "$0")/../src/smneg/assets"
rm -rf icon.iconset && mkdir icon.iconset
for size in 16 32 128 256 512; do
  sips -z $size $size icon.png --out icon.iconset/icon_${size}x${size}.png >/dev/null
  sips -z $((size*2)) $((size*2)) icon.png --out icon.iconset/icon_${size}x${size}@2x.png >/dev/null
done
iconutil -c icns icon.iconset -o icon.icns
rm -rf icon.iconset
