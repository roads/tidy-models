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
"""Test ModelIdentifier."""

from tidy_models.model_identifier import ModelIdentifier


def test_0():
    """Test minimal init arguments."""
    desired_name = 'model-0-0-x'

    mid = ModelIdentifier()
    name = mid.name

    assert desired_name == name


def test_1():
    """Test init with options."""
    desired_name = 'model-0-0-0'

    split = 0
    mid = ModelIdentifier(split=split)
    name = mid.name

    assert desired_name == name


def test_2():
    """Test init with options."""
    desired_name = 'model-1-2-0'

    arch_id = 1
    input_id = 2
    split = 0

    mid = ModelIdentifier(arch_id=arch_id, input_id=input_id, split=split)
    name = mid.name

    assert desired_name == name


def test_3():
    """Test init with options."""
    desired_name = 'emb-1-2-0'

    arch_id = 1
    input_id = 2
    split = 0
    prefix = 'emb'

    mid = ModelIdentifier(
        arch_id=arch_id, input_id=input_id, split=split, prefix=prefix
    )
    name = mid.name

    assert desired_name == name


def test_4():
    """Test init with options.
    
    Integer hypers.

    """
    desired_name = 'emb-1-2-3-0'

    arch_id = 1
    input_id = 2
    split = 0
    prefix = 'emb'
    hypers = {'n_dim': 3}
    mid = ModelIdentifier(
        arch_id=arch_id, input_id=input_id, hypers=hypers, split=split,
        prefix=prefix
    )
    name = mid.name

    assert desired_name == name


def test_5():
    """Test init with options.

    With float hypers and default formatting.

    """
    desired_name = 'emb-1-2-0.001-0'

    arch_id = 1
    input_id = 2
    split = 0
    prefix = 'emb'
    hypers = {'lr': .001}
    mid = ModelIdentifier(
        arch_id=arch_id, input_id=input_id, hypers=hypers, split=split,
        prefix=prefix
    )
    name = mid.name

    assert desired_name == name


def test_6():
    """Test init with options.

    With float hypers and formatting.

    """
    desired_name = 'emb-1-2-1-0'

    arch_id = 1
    input_id = 2
    split = 0
    prefix = 'emb'
    hypers = {'lr': .001}
    formatter = {'lr': lambda x: str(int(x*1000))}
    mid = ModelIdentifier(
        arch_id=arch_id, input_id=input_id, hypers=hypers, split=split,
        formatter=formatter, prefix=prefix
    )
    name = mid.name

    assert desired_name == name
