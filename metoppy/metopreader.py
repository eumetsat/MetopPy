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
        self._keys = Main.MetopDatasets.keys
        self._load_dataset = Main.MetopDatasets.MetopDataset
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
        return self._keys(dataset)

    def load_dataset(self, file_path: str):
        """
        Load a dataset from a record path using MetopDatasets.MetopDataset.

        Parameters
        ----------
        file_path : str
            Path to the dataset record.

        Returns
        -------
        Julia object
            A MetopDataset object loaded from the provided path.
        """
        try:
            return self._load_dataset(file_path)
        except Exception as e:
            raise RuntimeError(f"Failed to load dataset: {file_path}") from e

    def get_test_data_artifact(self):
        """
        Retrieve the test dataset artifact from MetopDatasets.

        Returns
        -------
        Julia object
            A MetopDataset object containing test data for validation or demo purposes.
        """
        return self._get_test_data_artifact()
