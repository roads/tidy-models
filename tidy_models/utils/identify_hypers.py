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
    identify_hypers: TODO

"""

import re


def identify_hypers(df_fit):
    """Identify hyperparameters.

    Arguments:
        df_fit: A pd.DataFrame of model fit data.

    Returns:
        hypers: A list of strings.

    """
    hypers = []
    for col_name in list(df_fit.columns):
        if re.match(r'hyp_*.', col_name):
            hypers.append(col_name)
    return hypers
