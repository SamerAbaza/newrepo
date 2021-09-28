import json
from dataclasses import dataclass
from unittest.mock import MagicMock

import pandas
import pytest
from azure.storage.blob import BlobClient
from fastapi import HTTPException
from freezegun import freeze_time

from main import validate_companies, write_mapping_to_company_data_lake, generate_blob_name
import main
from.conftest import mock_uuid


@pytest.mark.parametrize(
    "company_1,company_2,raises",
    [
        # Two Times same company
        ("RTL", "RTL", True),
        # First company not in Graph
        ("Not in Graph", "RTL", True),
        # Second company not in Graph
        ("RTL", "Not in Graph", True),
        # Successful check
        ("RTL", "DPV", False),
    ],
)
def test_validate_companies(company_1, company_2, raises):
    if raises:
        with pytest.raises(HTTPException):
            validate_companies(
                columns=["RTL", "TV Now", "DPV"],
                company_1=company_1,
                company_2=company_2,
            )
    else:
        validate_companies(
            columns=["RTL", "TV Now", "DPV"], company_1=company_1, company_2=company_2
        )


def test_write_mapping_to_company_data_lake():
    mock_client = MagicMock(autospec=BlobClient)
    mapping = pandas.DataFrame(
        data={
            "crm_id": ["d1_1", "d1_3"],
            "random_id": [
                "bdd640fb-0667-4ad1-9c80-317fa3b1799d",
                "23b8c1e9-3924-46de-beb1-3b9046685257",
            ],
        }
    )
    expected_upload_data = """crm_id;random_id
d1_1;bdd640fb-0667-4ad1-9c80-317fa3b1799d
d1_3;23b8c1e9-3924-46de-beb1-3b9046685257
"""

    write_mapping_to_company_data_lake(blob_client=mock_client, mapping=mapping)

    mock_client.upload_blob.assert_called_once()
    mock_client.upload_blob.assert_called_with(data=expected_upload_data)


@freeze_time("2021-01-01")
def test_generate_blob_name(mock_uuid):
    assert generate_blob_name(company_1="com1", company_2="com2") == \
           "share-ids/2021-01-01/bdd640fb-0667-4ad1-9c80-317fa3b1799d-com1-com2.csv"


def test_get_blob_client():
    blob_client = main.get_blob_client("com1", "some-blob.csv")
    assert blob_client.blob_name == "some-blob.csv"
    assert blob_client.account_name == "storage-account-com1"
    assert blob_client.container_name == "storage-container-1"

    blob_client = main.get_blob_client("com2", "some-blob.csv")
    assert blob_client.blob_name == "some-blob.csv"
    assert blob_client.account_name == "storage-account-com2"
    assert blob_client.container_name == "storage-container-2"

    with pytest.raises(Exception):
        main.get_blob_client("not-in-env", "some-blob.csv")
