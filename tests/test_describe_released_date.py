from unittest import mock

from copernicusmarine import CopernicusMarineCatalogue, describe
from copernicusmarine.core_functions.fields_query_builder import build_query
from tests.resources.mock_stac_catalog_WAW3.mock_marine_data_store_stac_metadata import (  # noqa: E501
    mocked_stac_requests_get,
)

exclude_query = build_query(
    {"description", "keywords"}, CopernicusMarineCatalogue
)


class TestDescribeReleaseDate:
    @mock.patch(
        "requests.Session.get",
        side_effect=mocked_stac_requests_get,
    )
    def when_I_describe_the_marine_data_store(
        self,
        mock_get,
        show_all_versions=False,
    ):
        return describe(
            show_all_versions=show_all_versions,
        )

    def test_only_released_dataset_by_default(self, snapshot):
        describe_result = self.when_I_describe_the_marine_data_store()
        self.then_I_dont_get_the_not_released_products_version_and_datasets(
            describe_result, snapshot
        )

    def then_I_dont_get_the_not_released_products_version_and_datasets(
        self, describe_result: CopernicusMarineCatalogue, snapshot
    ):
        assert 1 == len(describe_result.products)
        assert (
            describe_result.model_dump(
                exclude_none=True,
                exclude_unset=True,
                exclude=exclude_query,
            )
            == snapshot
        )

    def test_describe_all_versions(self, snapshot):
        describe_result = self.when_I_describe_the_marine_data_store(
            show_all_versions=True
        )
        self.then_I_get_all_products_versions_and_datasets(
            describe_result, snapshot
        )

    def then_I_get_all_products_versions_and_datasets(
        self, describe_result: CopernicusMarineCatalogue, snapshot
    ):
        assert 2 == len(describe_result.products)
        assert (
            describe_result.model_dump(
                exclude_none=True,
                exclude_unset=True,
                exclude=exclude_query,
            )
            == snapshot
        )
