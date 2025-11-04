#!/usr/bin/env python
#
# Package Name: metoppy
# Author: Simon Kok Lupemba, Francesco Murdaca
# License: MIT License
# Copyright (c) 2025 EUMETSAT

# This package is licensed under the MIT License.
# See the LICENSE file for more details.

"""Test file."""

import pytest
from pathlib import Path
from metoppy.metopreader import MetopReader


@pytest.fixture(scope="module")
def metop_reader():
    """
    Initialize the MetopReader once for the entire module
    """
    reader = MetopReader()
    return reader  # Make it available to tests


@pytest.fixture
def test_file(request, metop_reader):
    """
    Fixture to get test file
    """
    product_type = request.param  # get parameter from the test

    reduced_data_folder = Path(metop_reader.get_test_data_artifact())
    reduced_data_files = [f for f in reduced_data_folder.iterdir() if f.is_file()]
    test_file_name = next((f for f in reduced_data_files if f.name.startswith(product_type)), None)
    test_file_path = reduced_data_folder / test_file_name

    return test_file_path


@pytest.mark.parametrize("test_file", ["ASCA_SZO"], indirect=True)
def test_get_keys(metop_reader, test_file):
    """
    Simple test for metop_reader.get_key
    """
    # arrange
    ds = metop_reader.open_dataset(file_path=str(test_file))
    
    # act
    keys = metop_reader.get_keys(ds)
    
    # assert
    assert "latitude" in keys
    assert "record_start_time" in keys
    assert "sigma0_trip" in keys
    assert "utc_line_nodes" in keys
    assert "latitude_full" not in keys

    # clean 
    metop_reader.close_dataset(ds)


@pytest.mark.parametrize("test_file", ["ASCA_SZO"], indirect=True)
def test_close_dataset(metop_reader, test_file):
    """
    Test for metop_reader.test_close_dataset. It should not be 
    possible to read from a closed dataset
    """
    # arrange
    import juliacall
    ds = metop_reader.open_dataset(file_path=str(test_file))
    
    # act
    metop_reader.close_dataset(ds)
    
    # assert
    with pytest.raises(juliacall.JuliaError):
        ds['longitude'][0,0]


@pytest.mark.parametrize("test_file", ["ASCA_SZO"], indirect=True)
def test_shape(metop_reader, test_file):
    """
    Simple test for metop_reader.shape.
    """
    # arrange
    ds = metop_reader.open_dataset(file_path=str(test_file))
    
    # act
    latitude = ds['latitude']
    longitude_slice = ds['longitude'][10:14,0:2]

    shape_latitude = metop_reader.shape(latitude)
    shape_longitude_slice = metop_reader.shape(longitude_slice)
    
    # assert
    assert shape_latitude == (42,10)
    assert shape_longitude_slice == (4,2)

    # clean 
    metop_reader.close_dataset(ds)


@pytest.mark.parametrize("test_file", ["IASI_xxx"], indirect=True)
def test_read_single_value(metop_reader, test_file):
    """
    Test reading scalar value and assert that the value is correct. 
    The test also checks that Julia datetimes are converted to Python datetime.datetime
    """
    # arrange
    import datetime
    ds = metop_reader.open_dataset(file_path=str(test_file))
    
    # act
    CO2_radiance = ds["gs1cspect"][91, 0, 0, 0]
    start_time = ds["record_start_time"][0]

    # assert
    assert CO2_radiance == pytest.approx(0.0006165, abs=2e-5) 
    assert isinstance(CO2_radiance, float)
    
    assert start_time.year == 2024
    assert start_time.month == 9
    assert start_time.day == 25
    assert isinstance(start_time, datetime.datetime)

    # clean 
    metop_reader.close_dataset(ds)

@pytest.mark.parametrize("test_file", ["ASCA_SZR"], indirect=True)
def test_read_array(metop_reader, test_file):
    """
    Test reading varible as an array and conveting it to numpy.
    This test uses default parameter which results in less performant
    dynamic types.
    """
    # arrange
    import numpy as np
    ds = metop_reader.open_dataset(file_path=str(test_file))
    
    # act
    latitude_julia = metop_reader.as_array(ds['latitude'])
    longitude_julia = metop_reader.as_array(ds['longitude'])
    longitude_slice_julia = ds['longitude'][10:14,0:2]
    latitude = np.array(latitude_julia, copy = None)
    longitude = np.array(longitude_julia, copy = None)
    longitude_slice = np.array(longitude_slice_julia, copy = None)

    # assert
    assert np.all((0 < longitude)&(longitude < 360))
    assert np.all((-90 < latitude)&(latitude < 90))
    assert np.all((0 < longitude_slice)&(longitude_slice < 360))
    assert longitude_slice.shape == (4,2)

    # clean 
    metop_reader.close_dataset(ds)

@pytest.mark.parametrize("test_file", ["ASCA_SZR"], indirect=True)
def test_type_stable_array(metop_reader, test_file):
    """
    Test reading varible as an array and conveting it to numpy the performant way.
    This also check that the numpy data type is set correctly. 
    "maskingvalue = float("nan")" is used to generate arrays with concrete data type.
    """
    # arrange
    import numpy as np
    ds = metop_reader.open_dataset(file_path=str(test_file), maskingvalue = float("nan"))
    
    # act
    latitude = np.array(metop_reader.as_array(ds['latitude']), copy = None)
    longitude = np.array(metop_reader.as_array(ds['longitude']), copy = None)

    # assert
    assert latitude.dtype == np.dtype('float64')
    assert longitude.dtype == np.dtype('float64')
    assert np.all((0 < longitude)&(longitude < 360))
    assert np.all((-90 < latitude)&(latitude < 90))

    # clean 
    metop_reader.close_dataset(ds)

@pytest.mark.parametrize("test_file", ["ASCA_SZF", "ASCA_SZO","ASCA_SZR", "MHSx_xxx", "HIRS_xxx", "AMSA_xxx", "IASI_SND", "IASI_xxx"], indirect=True)
def test_different_file_types(metop_reader, test_file):
    """
    Test that different types of test files can be opened.
    """
    # act
    ds = metop_reader.open_dataset(file_path=str(test_file))
    
    # assert
    assert ds is not None
    assert "record_start_time" in metop_reader.get_keys(ds)
    
    # clean 
    metop_reader.close_dataset(ds)