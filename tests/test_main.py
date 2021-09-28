import pytest
from azure.storage.blob import BlobClient
from fastapi.testclient import TestClient

import azure_interactions

from main import app
import main
from test_data import df_id_graph

test_client = TestClient(app)


def get_mapping(monkeypatch, endpoint)-> None:
    monkeypatch.setattr(main, "get_blob_client", lambda company, blob_name: BlobClient.from_blob_url(
        f"https://account.blob.core.windows.net/container/{blob_name}"))
    monkeypatch.setattr(main, "write_mapping_to_company_data_lake", lambda *args, **kwargs: None)
    monkeypatch.setattr(azure_interactions.AzureBlob, "read_latest_blob_to_df", lambda _: df_id_graph)
    response = test_client.get(
        f"/{endpoint}", params={"company_1": "com_1", "company_2": "com_2"}
    )

    assert response.status_code == 200

    response_dict = response.json()
    assert response_dict.keys() == {"com_1", "com_2"}
    assert all(isinstance(value, str) for value in response_dict.values())

    response = test_client.get(
        f"/{endpoint}", params={"company_1": "com_1", "company_2": "com_1"}
    )
    assert response.status_code == 404


def test_get_mapping(monkeypatch):
    get_mapping(monkeypatch=monkeypatch, endpoint="share_person")
    get_mapping(monkeypatch=monkeypatch, endpoint="share_cell")