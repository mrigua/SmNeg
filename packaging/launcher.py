# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Said Mrigua
"""Entry point used by PyInstaller."""
import sys

from smneg.app import main

if __name__ == "__main__":
    sys.exit(main())
