# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Tests the load_projects_buckets_acls_pipeline."""

from tests.unittest_utils import ForsetiTestCase
import mock
import unittest

# pylint: disable=line-too-long
from google.cloud.security.common.data_access import bucket_dao
from google.cloud.security.common.data_access import errors as data_access_errors
from google.cloud.security.common.gcp_api import errors as api_errors
from google.cloud.security.common.gcp_api import storage
from google.cloud.security.common.util import log_util
from google.cloud.security.inventory import errors as inventory_errors
from google.cloud.security.inventory.pipelines import load_projects_buckets_acls_pipeline
from tests.inventory.pipelines.test_data import fake_buckets
from tests.inventory.pipelines.test_data import fake_configs
# pylint: enable=line-too-long


class LoadProjectsBucketsAclsPipelineTest(ForsetiTestCase):
    """Tests for the load_projects_buckets_acls_pipeline."""

    FAKE_PROJECT_NUMBERS = ['11111']
    FAKE_BUCKETS = ['fakebucket1']

    def setUp(self):
        """Set up."""

        self.cycle_timestamp = '20001225T120000Z'
        self.configs = fake_configs.FAKE_CONFIGS
        self.mock_gcs_acl = mock.create_autospec(storage.StorageClient)
        self.mock_dao = mock.create_autospec(bucket_dao.BucketDao)
        self.maxDiff = None
        self.pipeline = (
            load_projects_buckets_acls_pipeline.LoadProjectsBucketsAclsPipeline(
                self.cycle_timestamp,
                self.configs,
                self.mock_gcs_acl,
                self.mock_dao))

    def test_can_transform_bucket_acls(self):
        """Test that bucket acls can be tranformed."""

        loadable_buckets = list(self.pipeline._transform(
            fake_buckets.FAKE_BUCKET_ACL_MAP))
        self.assertEquals(
            fake_buckets.EXPECTED_LOADABLE_BUCKET_ACLS,
            loadable_buckets)

    def test_retrieve_bucket_acls(self):
        """Test that bucket acls can be retrieved."""
        mock_get_raw_buckets = mock.MagicMock()
        self.mock_dao.get_raw_buckets = mock_get_raw_buckets
        mock_get_raw_buckets.return_value = fake_buckets.FAKE_RAW_BUCKET_ROW
        bucket_acls = self.pipeline._retrieve()
        mock_get_raw_buckets.assert_called_once_with(self.cycle_timestamp)
        self.assertEquals(
            fake_buckets.EXPECTED_RAW_BUCKET_JSON,
            bucket_acls)

    @mock.patch.object(
        load_projects_buckets_acls_pipeline.LoadProjectsBucketsAclsPipeline,
        '_get_loaded_count')
    @mock.patch.object(
        load_projects_buckets_acls_pipeline.LoadProjectsBucketsAclsPipeline,
        '_load')
    @mock.patch.object(
        load_projects_buckets_acls_pipeline.LoadProjectsBucketsAclsPipeline,
        '_transform')
    @mock.patch.object(
        load_projects_buckets_acls_pipeline.LoadProjectsBucketsAclsPipeline,
        '_retrieve')
    def test_subroutines_are_called_by_run(self, mock_retrieve, mock_transform,mock_load, mock_get_loaded_count):
        """Test that the subroutines are called by run."""
        mock_retrieve.return_value = (
            fake_buckets.FAKE_BUCKET_ACL_MAP)
        mock_transform.return_value = (
            fake_buckets.EXPECTED_LOADABLE_BUCKET_ACLS)
        self.pipeline.run()

        mock_retrieve.assert_called_once_with()

        mock_transform.assert_called_once_with(
            fake_buckets.FAKE_BUCKET_ACL_MAP)

        self.assertEquals(1, mock_load.call_count)

        # The regular data is loaded.
        called_args, called_kwargs = mock_load.call_args_list[0]
        expected_args = (
            self.pipeline.RESOURCE_NAME,
            fake_buckets.EXPECTED_LOADABLE_BUCKET_ACLS)
        self.assertEquals(expected_args, called_args)

        mock_get_loaded_count.assert_called_once


if __name__ == '__main__':
      unittest.main()
