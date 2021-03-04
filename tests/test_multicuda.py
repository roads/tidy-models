# -*- coding: utf-8 -*-
# Copyright 2020 Brett D. Roads. All Rights Reserved.
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
# ==============================================================================
"""Test Multi-proessing CUDA example."""

import multiprocessing
import os
import re
import time

from tidy_models import multicuda

# os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
# os.environ["CUDA_VISIBLE_DEVICES"] = ""


def dummy_target(id=None, path=None):
    """Target function."""
    # Determine which CUDA devices are visible in the current process
    # context. If things are working correctly, there should only be
    # one device visible.
    cuda_visible_ids = os.getenv('CUDA_VISIBLE_DEVICES')

    # Save some info to a process-specific file for later verification.
    fn = path.join('test-{0}.txt'.format(id))
    f = open(fn, 'w')
    f.write("id={0}\n".format(id))
    f.write("pid={0}\n".format(os.getpid()))
    f.write("cuda_visible_ids={}\n".format(cuda_visible_ids))
    f.close()


def test_0(tmpdir):
    """Test multi-process CUDA.

    NOTE: Assumes 4 CUDA devices are available.

    """
    desired_counter = 9

    # Define available CUDA IDs.
    cuda_id_list = [0, 1, 3]

    # Define task information.
    args_list = [
        {'id': '0', 'path': tmpdir},
        {'id': '1', 'path': tmpdir},
        {'id': '2', 'path': tmpdir},
        {'id': '3', 'path': tmpdir},
        {'id': '4', 'path': tmpdir},
        {'id': '5', 'path': tmpdir},
        {'id': '6', 'path': tmpdir},
        {'id': '7', 'path': tmpdir},
        {'id': '8', 'path': tmpdir},
    ]

    # Execute multiprocess code.
    multicuda.cuda_manager(
        dummy_target, args_list, cuda_id_list, n_concurrent=2
    )

    # Check results.
    fn_regex = 'test-[0-9]*'
    matching_file_list = os.listdir(tmpdir)
    counter = 0
    for fn in matching_file_list:
        result = re.match(fn_regex, fn)
        if result is not None:
            fp = tmpdir.join(fn)
            f = open(fp, "r")
            ln0 = f.readline().rstrip().split('=')
            ln1 = f.readline().rstrip().split('=')
            ln2 = f.readline().rstrip().split('=')
            f.close()

            # Assert id matches.
            assert (fn.split('-')[1]).split('.')[0] == ln0[1]

            # Assert only one CUDA device was visible to the worker.
            assert len(ln2[1].split(',')) == 1

            counter += 1

    # Assert that 8 processes completed.
    assert desired_counter == counter
