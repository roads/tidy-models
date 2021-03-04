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
    collapse_splits: TODO
    select_hypers: TODO

"""

import numpy as np
import pandas as pd

import tidy_models.databases.pandas.core as db
from tidy_models.utils.identify_hypers import identify_hypers


def collapse_splits(df_fit, id_data, mode='balanced'):
    """Collapse data across different splits.

    Arguments:
        df_fit: A pd.DataFrame with model fit data.
        id_data: A dictionary of model identifiers. All models matching
            the identifiers will be assumed to be part of the collapse
            procedure.
        mode (optional): The manner in which to collapse across splits.
            Can be 'None' or 'balanced'. If 'None', uses all splits for
            each hyperparameter setting, even if unbalanced. If
            `balanced`, only splits that are balanced across all hyper-
            parameter settings will be used. For example if
            `hyper_n_dim=2` has splits [0, 1, 2, 3] and `hyper_n_dim=3`
            has splits [1, 2], then only splits [1, 2] are used in the
            derivation of split statistics.

    Returns:
        df_fit_collapse: Data collapsed across splits.

    """
    # Make sure that all models have the same architecture and input by
    # select relevant rows for analysis.
    df_fit = db.find(df_fit, id_data)

    # Remove split '-1` from analysis.
    df_fit = df_fit.query('split != -1')

    if len(df_fit) == 0:
        raise ValueError(
            'There is no data for the requested `id_data`.'
        )

    id_keys = list(id_data.keys())
    if mode == 'balanced':
        # Filter data so that splits are balanced across dimensions.

        # First, determine the hyperparameters.
        hypers = identify_hypers(df_fit)

        # Second, determine the intersection of splits across all hyper-
        # parameter settings.
        for hyper in hypers:
            hyper_arr = pd.unique(df_fit[hyper])
            split_intersect = pd.unique(df_fit['split'])
            for v in hyper_arr:
                select_dict = {hyper: v}
                loc = db.is_match(df_fit, select_dict)
                df_fit_sub = df_fit[loc]
                split_intersect = np.intersect1d(
                    split_intersect, pd.unique(df_fit_sub['split'])
                )

        # Drop rows that are not in the intersection.
        bidx_keep = None
        for split in split_intersect:
            if bidx_keep is None:
                bidx_keep = df_fit['split'] == split
            else:
                bidx_keep = bidx_keep | (df_fit['split'] == split)
        df_fit = df_fit[bidx_keep]

    # Exploit multi-index functionality to collapse across splits.
    stat_column_list = id_keys + hypers
    df_count = df_fit.groupby(stat_column_list).size().to_frame('count')
    df_mean = df_fit.groupby(stat_column_list).mean()
    # Adjust std error computation based on global mean of split. TODO
    # df_global_mean = df_fit.groupby(id_keys).mean()
    df_std = df_fit.groupby(stat_column_list).std().add_suffix('_std')
    df_fit_collapse = pd.concat([df_count, df_mean, df_std], axis=1)

    # Drop unneeded columns.
    df_fit_collapse = df_fit_collapse.drop(
        ['split', 'split_std'],
        axis=1
    )

    # Flatten multi-index.
    df_fit_collapse = df_fit_collapse.reset_index()

    return df_fit_collapse
