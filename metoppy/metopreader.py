#!/usr/bin/env python
#
# Package Name: metoppy
# Author: Simon Kok Lupemba, Francesco Murdaca
# License: MIT License
# Copyright (c) 2025 EUMETSAT

# This package is licensed under the MIT License.
# See the LICENSE file for more details.


"""MetopDatasets.jl Python wrapper class: MetopReader."""

from juliacall import Main


class MetopReader:
    """Python wrapper class for MetopDatasets.jl Julia package."""

    def __init__(self):
        """
        Initialize the MetopReader by loading the MetopDatasets.jl package
        into the Julia Main environment and caching references to its functions.
        """
        # Import Julia package installed via juliapkg.json
        Main.seval("import MetopDatasets")
        # Store module and commonly used functions
        self._open_dataset = Main.MetopDatasets.MetopDataset
        self._get_test_data_artifact = Main.MetopDatasets.get_test_data_artifact

    def get_keys(self, dataset):
        """
        Return the available keys from a given MetopDataset.

        Parameters
        ----------
        dataset : Julia object
            A dataset object created by MetopDatasets.MetopDataset.

        Returns
        -------
        list
            The list of keys available in the dataset.
        """
        return Main.keys(dataset)
    
    def as_array(self, variable):
        """
        Load the variable as a Julia array.

        Parameters
        ----------
        variable : Julia object
            A variable from a MetopDatasets.MetopDataset object.

        Returns
        -------
        Julia array
            The data from the variable loaded as an array.
        """
        return Main.Array(variable)
    
    def shape(self, variable_or_j_array):
        """
        Get the shape a Julia array or variable.

        Parameters
        ----------
        variable_or_j_array : Julia object
            A variable from a MetopDatasets.MetopDataset object or a Julia Array.

        Returns
        -------
        Tuple of ints
            The shape of the variable
        """
        return Main.size(variable_or_j_array)

    def open_dataset(self, file_path: str, maskingvalue = Main.missing):
        """
        Open a dataset from a record path using MetopDatasets.MetopDataset.

        Parameters
        ----------
        file_path : str
            Path to the dataset record.

        maskingvalue
            The masking values are used to replace missing observations. Defaults to Julia Missing type. 
            A recommended alternative is float("nan") which increasse performance for float data.

        Returns
        -------
        Julia object
            A MetopDataset object opened from the provided path.
        """
        try:
            return self._open_dataset(file_path, maskingvalue = maskingvalue)
        except Exception as e:
            raise RuntimeError(f"Failed to open dataset: {file_path}") from e
        
    def close_dataset(self, dataset):
        """
        Close a dataset and free the file lock created by MetopReader.open_dataset

        Parameters
        ----------
        dataset : Julia object
            A dataset object created by MetopDatasets.MetopDataset.

        Returns
        -------
        None
        """
        Main.close(dataset)
        return None
    
    def get_test_data_artifact(self):
        """
        Retrieve the test dataset artifact from MetopDatasets.

        Returns
        -------
        Julia object
            A MetopDataset object containing test data for validation or demo purposes.
        """
        return self._get_test_data_artifact()
