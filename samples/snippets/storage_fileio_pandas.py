#!/usr/bin/env python

# Copyright 2019 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License');
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

import sys

"""Sample that creates and consumes a GCS blob using pandas with file-like IO
"""

# [START storage_fileio_pandas]
from google.cloud import storage


def pandas_write_read(bucket_name, blob_name):
    """Use pandas to interact with GCS using file-like IO"""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"

    # The ID of your new GCS object
    # blob_name = "storage-object-name"

    import pandas as pd

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)

    with blob.open("w") as f:
        df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})
        f.write(df.to_csv(index=False))

    with blob.open("r") as f:
        df = pd.read_csv(f)
        print(df.values.flatten())


# [END storage_fileio_pandas]

if __name__ == "__main__":
    pandas_write_read(
        bucket_name=sys.argv[1],
        blob_name=sys.argv[2]
    )
