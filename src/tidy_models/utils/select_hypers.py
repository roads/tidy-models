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
"""Selection module.

Functions:
    select_hypers: TODO

"""

import numpy as np
import pandas as pd

import tidy_models.databases.pandas.core as db
from tidy_models.utils.identify_hypers import identify_hypers


def select_hypers(
        df_fit_collapse, id_data, monitor_key='val_loss', select_mode='min'):
    """Select hyperparameters for a set of comparable models.

    Requires that all provided models use the same architecture
    (`arch_id`) and input data (`input_id`).

    Arguments:
        df_fit_collapse: A pd.DataFrame containing collapsed fit
            information.
        id_data: A dictionary specifying the model to select hyper-
            parameters. At a minimum this is should include 'arch_id'
            and 'input_id'.
        monitor_key (optional): The key on which to select the best
            hyperparemters. By default, selection will assume that a
            column named `val_loss` exists.
        select_mode (optional): Can be 'min' or 'max'.
        options (optional): A dictionary of options for each
            hyperparameter.

    Returns:
        df_fit_best

    Raises:
        ValueError if there is no split data for the requested
            `arch_id` and `input_id`.

    """
    # Settings:
    monitor_threshold = 0.

    # Make sure that all models have the same architecture and input by
    # select relevant rows for analysis.
    df_fit_collapse = db.find(df_fit_collapse, id_data)

    if len(df_fit_collapse) == 0:
        raise ValueError(
            'There is no data for the requested `id_data`.'
        )

    # Select best row.
    if select_mode == 'min':
        # best_row = np.argmin(df_fit_collapse[monitor_key].values)
        best_idx = df_fit_collapse[monitor_key].idxmin(axis='columns')
    elif select_mode == 'max':
        best_idx = df_fit_collapse[monitor_key].idxmax(axis='columns')
    else:
        raise ValueError('Unrecognized `select_mode`.')
    df_fit_best = df_fit_collapse.iloc[[best_idx], :].copy()

    # Add min/max hyperparameter information.
    hypers = identify_hypers(df_fit_collapse)
    for hyper in hypers:
        hyper_arr = df_fit_collapse[hyper].values
        hyper_min = np.min(hyper_arr)
        hyper_max = np.max(hyper_arr)
        df_fit_best[hyper + '_min'] = hyper_min
        df_fit_best[hyper + '_max'] = hyper_max

    return df_fit_best
