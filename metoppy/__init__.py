#!/usr/bin/env python
#
# Package Name: metoppy
# Author: Simon Kok Lupemba, Francesco Murdaca
# License: MIT License
# Copyright (c) 2025 EUMETSAT

# This package is licensed under the MIT License.
# See the LICENSE file for more details.

"""Metoppy package initialization."""

# Optional: version info
__version__ = "0.1.0"

# Import main classes/functions
from .metopreader import MetopReader

__all__ = [
    MetopReader.__name__,
]
