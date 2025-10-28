# MetopPy
Load native METOP products in Python. 
It's a Python wrapper around [MetopDatasets.jl](https://github.com/eumetsat/MetopDatasets.jl) making it easy to install and use the package with Python.

[MetopDatasets.jl](https://github.com/eumetsat/MetopDatasets.jl) is a package for reading products from the [METOP satellites](https://www.eumetsat.int/our-satellites/metop-series) using the native binary format specified for each product. The METOP satellites are part of the EUMETSAT-POLAR-SYSTEM (EPS) and have produced near real-time, global weather and climate observation since 2007. Learn more METOP and the data access on [EUMETSATs user-portal](https://user.eumetsat.int/dashboard).

## Status
Metopdatasetpy is under development and is not ready for use yet.

## Copyright and License
This code is licensed under MIT license. See file LICENSE for details on the usage and distribution terms.

## Authors
* Simon Kok Lupemba - *Maintainer* - [EUMETSAT](http://www.eumetsat.int)
* Francesco Murdaca- *Contributor* - [EUMETSAT](http://www.eumetsat.int)

## Installation
(This still have to be implemented)
```bash
pip install metoppy
```


## Dependencies

| Dependency | Version | License | Home URL |
|------|---------|---------|--------------|
| juliacall | >=0.9.14 | MIT License | https://juliapy.github.io/PythonCall.jl/stable/ |
| juliapkg | >=0.1.22 | MIT License | https://pypi.org/project/juliapkg/ |


## Build/Edit/Test Dependencies
The following dependencies are only required for building/editing/testing the software, they are not distributed with it:

| Dependency | Version | License | Home URL |
|------|---------|---------|--------------|
| pytest | 8.4.1  | MIT License (MIT) | https://docs.pytest.org/en/latest |
| pytest-html | 4.1.1 | MIT License (MIT)   | https://github.com/pytest-dev/pytest-html  |
| pytest-mock | 3.14.1  | MIT License (MIT) | https://github.com/pytest-dev/pytest-mock |
| coverage | 7.10.5  | Apache Software License (Apache License Version 2.0) | https://github.com/nedbat/coveragepy |
| pre-commit | 4.3.0  | MIT License (MIT) | https://github.com/pre-commit/pre-commit  |

## Example

1. Get test file

```python
from pathlib import Path
from metoppy.metopreader import MetopReader

metop_reader = MetopReader()
reduced_data_folder = metop_reader.get_test_data_artifact()
# ensure it's a Path object
reduced_data_folder = Path(reduced_data_folder)
reduced_data_files = [f for f in reduced_data_folder.iterdir() if f.is_file()]

test_file_name = next((s for s in reduced_data_files if s.name.startswith("ASCA_SZO")))
test_file_path = reduced_data_folder / test_file_name
ds = metop_reader.load_dataset(file_path=str(test_file_path))
```

2. Check keys

```python
keys = metop_reader.get_keys(ds)
print(list(keys))
```
<details>

<summary>Output of the print </summary>

```
['record_start_time', 'record_stop_time', 'degraded_inst_mdr', 'degraded_proc_mdr', 'utc_line_nodes', 'abs_line_number', 'sat_track_azi', 'as_des_pass', 'swath_indicator', 'latitude', 'longitude', 'sigma0_trip', 'kp', 'inc_angle_trip', 'azi_angle_trip', 'num_val_trip', 'f_kp', 'f_usable', 'f_land', 'lcr', 'flagfield']
```

</details>

3. Display variable information

```python
print(ds['latitude'])
```
<details>

<summary>Output of the print </summary>

```
latitude (42 × 10)
  Datatype:    Union{Missing, Float64} (Int32)
  Dimensions:  xtrack × atrack
  Attributes:
   description          = Latitude (-90 to 90 deg)
   missing_value        = Int32[-2147483648]
   scale_factor         = 1.0e-6
```

</details>

4. Read variable

```python
from juliacall import Main

# Convert CFVariable to a full Julia Array
latitude_julia = Main.Array(ds['latitude'])  # preserves the 2D shape

# Convert to nested Python list
latitude_list = [
  [latitude_julia[i, j] for j in range(latitude_julia.size[1])]
  for i in range(latitude_julia.size[0])
]

# Print first 5x5 elements
for row in latitude_list[:5]:
    print(row[:5])
```
<details>

<summary>Output of the print </summary>

```
[71.101406, 70.99323199999999, 70.88307999999999, 70.770985, 70.65697999999999]
[71.298254, 71.18898999999999, 71.077743, 70.964546, 70.849434]
[71.494503, 71.384132, 71.271771, 71.157454, 71.041217]
[71.690134, 71.578638, 71.465144, 71.349689, 71.23231]
[71.885128, 71.772486, 71.65784099999999, 71.541231, 71.422691]
```

</details>



## Development

Pre-requisite: Install podman or docker in your machine.

1. Fork this repository and move into it
```bash
git clone XXX && cd XXX
```

2. Start container mounting the content
```bash
podman run -v ./:/usr/local/bin/metoppy -it python:3.12 /bin/bash
```

or

```bash
docker run -v ./:/usr/local/bin/metoppy -it python:3.12 /bin/bash
```

3. Move to the repository and install the package for testing
```
cd /usr/local/bin/metoppy && pip install -e .
```

4. Modify the local code and test in the container.

```
python3 metoppy/tests/test_get_test_data_artifact.py
```

5. When you are happy, push code to your fork and open a MR (Gitlab) or PR (Github)
