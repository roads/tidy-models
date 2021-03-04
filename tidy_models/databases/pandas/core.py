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
"""Databases module.

Functions:
    load_db:
    save_db:
    is_match:
    find:
    update_one:

"""

import pandas as pd


def create_empty_db(fp, columns=['arch_id', 'input_id']):
    """Create empty database.

    Arguments:
        fp: Filepath for database.
        columns (optional): List of column names. The default column
            names constitute the minimum unique identifiers of a model.
            This list does not need to be exhaustive since columns can
            be retroactively added to a pd.DataFrame.

    """
    df = pd.DataFrame(
        columns=columns
    )
    save_db(df, fp)


def load_db(fp):
    """Load DataFrame database."""
    return pd.read_csv(fp, header=0, sep=' ')


def save_db(df, fp):
    """Save DataFrame database.

    Arguments:
        df: Database DataFrame.
        fp: Save filepath.

    """
    df.to_csv(fp, sep=' ', index=False)


def is_match(df, id_dict):
    """Find a rows based on exact match to identifiers.

    Arguments:
        df:
        id_dict: An identifier dictionary.

    Returns:
        loc: A Boolean index.

    """
    loc = None
    if len(df) > 0:
        for k, v in id_dict.items():
            if loc is None:
                loc = df[k] == v
            else:
                loc = loc & (df[k] == v)
    else:
        loc = []
    return loc


def find(df, match_dict):
    """Find a rows based on exact match to identifiers.

    Arguments:
        df:
        match_dict: An dictionary of key values to match.

    Returns:
        df: A DataFrame with any matching rows.

    """
    loc = is_match(df, match_dict)
    return df[loc]


def update_one(df, id_data, assoc_data):
    """Update first row that is found.

    Arguments:
        df: DataFrame of fit database.
        id_data: Dictionary of identifying keys.
        assoc_dict: Dictionary of data that should be associated with
            identifiers.

    """
    # Check if correspondig row already exists.
    loc = is_match(df, id_data)

    # if len(df[loc]) > 1:
    #     TODO: Throw warning if more than one match.

    if df[loc].empty:
        # Create new row and add.
        df_new = pd.DataFrame({**id_data, **assoc_data}, index=[len(df)])
        df = df.append(df_new, ignore_index=True)
        # Re-sort by identifier keys to keep things tidy.
        df = df.sort_values(list(id_data.keys()))
    else:
        # Apply updates.
        for k, v in assoc_data.items():
            df.loc[loc, k] = v

    return df
