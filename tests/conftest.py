import random
import pytest
import uuid
import numpy as np
import pandas
import json
import os


@pytest.fixture()
def mock_uuid(monkeypatch):
    rnd = random.Random()
    rnd.seed(42)
    monkeypatch.setattr(
        uuid, "uuid4", lambda: uuid.UUID(int=rnd.getrandbits(128), version=4)
    )


@pytest.fixture
def test_df():
    return pandas.DataFrame(
        data={
            "com_1": ["d1_1", np.nan, "d1_4", "d1_3"],
            "com_2": ["d2_A", np.nan, np.nan, "d2_D"],
            "com_3": ["d3_6", np.nan, "d3_8", "d3_9"],
            "com_4": [np.nan, "d4_X", "d4_Y", np.nan],
            "cell_id": [1, 2, 2, 2],
        })


os.environ["ACCESSIBLE_RESOURCES"] = json.dumps(
    {
        "storage_containers": {
            "meta-id-table": "https://graph-account-com1.blob.core.windows.net/graph-container/",
            "company-datalakes": {
                "com1": "https://storage-account-com1.blob.core.windows.net/storage-container-1/",
                "com2": "https://storage-account-com2.blob.core.windows.net/storage-container-2/",
            }
        }
    }
)