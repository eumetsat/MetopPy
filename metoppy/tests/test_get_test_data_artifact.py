#!/usr/bin/env python
#
# Package Name: metoppy
# Author: Simon Kok Lupemba, Francesco Murdaca
# License: MIT License
# Copyright (c) 2025 EUMETSAT

# This package is licensed under the MIT License.
# See the LICENSE file for more details.

"""Test file."""

# TODO: Convert to pytest
from pathlib import Path
from juliacall import Main
from metoppy.metopreader import MetopReader

metop_reader = MetopReader()
reduced_data_folder = metop_reader.get_test_data_artifact()
# ensure it's a Path object
reduced_data_folder = Path(reduced_data_folder)
reduced_data_files = [f for f in reduced_data_folder.iterdir() if f.is_file()]

test_file_name = next((s for s in reduced_data_files if s.name.startswith("ASCA_SZO")))
test_file_path = reduced_data_folder / test_file_name
ds = metop_reader.load_dataset(file_path=str(test_file_path))

keys = metop_reader.get_keys(ds)
print(list(keys))

print(ds["latitude"])

# Convert CFVariable to a full Julia Array
latitude_julia = Main.Array(ds["latitude"])  # preserves the 2D shape

# Convert to nested Python list
latitude_list = [
    [latitude_julia[i, j] for j in range(latitude_julia.size[1])]
    for i in range(latitude_julia.size[0])
]

# Print first 5x5 elements
for row in latitude_list[:5]:
    print(row[:5])
