# -*- coding: utf-8 -*-
# Copyright 2021 Brett D. Roads. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============================================================================
"""ModelIdentifier Module.

Classes:
    ModelIdentifier: Object to keep track of a model's identifying information.

"""

import os
from pathlib import Path


class ModelIdentifier(object):
    """Object to keep track of a model's identifying information.

    Attributes:
        arch_id: Integer that identifies the model architecture.
        input_id: Integer that identifies the input data.
        hypers: Dictionary of hyper-parameters.
        split_seed: Integer indicating the split seed.
        split: Integer indicating the split (zero-indexed). A value of
            '-1' indicates that all of the provided data was used for
            training and there was no validation set.
        name: A string representation of ID.
        path: A Path object representing the complete path.

    Methods:
        as_dict: Return dictionary representation of ID.

    """

    def __init__(
        self,
        arch_id=0,
        input_id=0,
        hypers={},
        n_split=10,
        split=-1,
        split_seed=252,
        path='',
        prefix='model',
        formatter={}
    ):
        """Initialize.

        Arguments:
            arch_id: Integer that identifies the model architecture.
            input_id: Integer that identifies the input data used.
            hypers: A dictionary of hyperparameters. Cannot be a nested
                dictionary. Dictionary key names will be used to create
                attributes in the object.
            split_seed: The split seed.
            split: The split (zero-indexed).
            path: TODO
            prefix (optional): File name prefix.
            formatter (optional): Dictionary corresponding to hypers
                that specifies the format rule to use when converting
                float hyperparmeters to strings.

        Raises:
            ValueError if a key in `hypers` already exists as an
            object attribute.

        """
        super(ModelIdentifier, self).__init__()
        self.arch_id = int(arch_id)
        self.input_id = int(input_id)
        self._add_hypers(hypers)
        self.split_seed = int(split_seed)
        self.n_split = int(n_split)
        self.split = int(split)
        self.path = Path(path)
        self.prefix = prefix
        self._add_formatter(formatter)

    @property
    def name(self):
        """Getter method for `name`.

        NOTE: This is called `name` and not filename since it is up to
        the user how the name will be used.

        """
        split = self.split
        if split == -1:
            split = 'x'

        # Create string for hyperparameters.
        hypers_string = ''
        if len(self.hypers) > 0:
            for k, v in self.hypers.items():
                if isinstance(v, float):
                    # Convert float to string.
                    k_formatter = self.formatter[k]
                    v_str = k_formatter(v)
                    hypers_string += '-{0}'.format(v_str)
                else:
                    hypers_string += '-{0}'.format(v)

        name = '{0}-{1}-{2}{3}-{4}'.format(
            self.prefix, self.arch_id, self.input_id, hypers_string, split
        )
        return name

    @property
    def pathname(self):
        """Getter method for `pathname`."""
        pn = self.path / Path(self.name)
        return pn

    def as_dict(self):
        """As dictionary."""
        d = {
            'arch_id': self.arch_id,
            'input_id': self.input_id,
            'split_seed': self.split_seed,
            'n_split': self.n_split,
            'split': self.split,
        }
        # Add hypers with "hyp_" prefix.
        for k, v in self.hypers.items():
            d.update(
                {'hyp_' + k: v}
            )
        return d

    def get_config(self):
        """Return configuration."""
        d = {
            'arch_id': self.arch_id,
            'input_id': self.input_id,
            'hypers': self.hypers,
            'split_seed': self.split_seed,
            'n_split': self.n_split,
            'split': self.split,
            'path': os.fspath(self.path),
            'prefix': self.prefix,
            'precision': self.precision
        }
        return d

    def _add_hypers(self, hypers):
        """Parse hyperparameters.

        Raises:
            ValueError if attribute already exists.

        """
        self.hypers = hypers
        for k, v in hypers.items():
            if not hasattr(self, k):
                setattr(self, k, v)
            else:
                raise ValueError(
                    'Attribute {0} already exists.'.format(k)
                )

    def _add_formatter(self, formatter):
        """Add formatter."""
        for k, v in self.hypers.items():
            if isinstance(v, float):
                # Check that formatter exists.
                if k not in formatter:
                    # Add default
                    formatter[k] = lambda x: str(x)
        self.formatter = formatter

        # If none provided, use default.
        # hypers_string += '-{1:.{0}f}'.format(self.precision, v)  TODO
