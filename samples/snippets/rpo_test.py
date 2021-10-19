# Copyright 2021 Google LLC
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

import uuid
import pytest
from google.cloud import storage

import storage_get_rpo
import storage_set_rpo_async_turbo
import storage_set_rpo_default
import storage_create_bucket_turbo_replication


@pytest.fixture
def dr_bucket():
    """Yields a dual region bucket that is deleted after the test completes."""
    bucket = None
    while bucket is None or bucket.exists():
        bucket_name = "bucket-lock-{}".format(uuid.uuid4())
        bucket = storage.Client().bucket(bucket_name)
        bucket.location = "NAM4"
    bucket.create()
    yield bucket
    bucket.delete(force=True)


def test_get_rpo(dr_bucket, capsys):
    storage_get_rpo.get_rpo(dr_bucket.name)
    out, _ = capsys.readouterr()
    assert f"RPO for {dr_bucket.name} is DEFAULT." in out


def test_set_rpo_async_turbo(dr_bucket, capsys):
    storage_set_rpo_async_turbo.set_rpo_async_turbo(dr_bucket.name)
    out, _ = capsys.readouterr()
    assert f"RPO is ASYNC_TURBO for {dr_bucket.name}." in out


def test_set_rpo_default(dr_bucket, capsys):
    storage_set_rpo_default.set_rpo_default(dr_bucket.name)
    out, _ = capsys.readouterr()
    assert f"RPO is DEFAULT for {dr_bucket.name}." in out


def test_create_bucket_turbo_replication(capsys):
    bucket_name = "test-rpo-{}".format(uuid.uuid4())
    storage_create_bucket_turbo_replication.create_bucket_turbo_replication(bucket_name)
    out, _ = capsys.readouterr()
    assert f"{bucket_name} created with RPO ASYNC_TURBO in NAM4." in out
