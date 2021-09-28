import json
import os
import uuid
from datetime import datetime
from typing import List

from azure.identity import DefaultAzureCredential
from azure.storage.blob import BlobClient
from fastapi import FastAPI, HTTPException
from pandas import DataFrame

import azure_interactions as ai
from generate_share_mapping import generate_share_mapping_person, generate_share_mapping_cell
from test_data import df_id_graph


ACCESSIBLE_RESOURCES: dict = json.loads(os.environ["ACCESSIBLE_RESOURCES"])
_CREDENTIALS = None


_CREDENTIALS = None


app = FastAPI()


def azure_credentials():
    global _CREDENTIALS
    if _CREDENTIALS is None:
        _CREDENTIALS = DefaultAzureCredential()
    return _CREDENTIALS


def validate_companies(columns: List[str], company_1: str, company_2: str):
    if company_1 not in columns:
        raise HTTPException(
            status_code=404, detail=f"Could not find company '{company_1}' in ID-Graph"
        )
    if company_2 not in columns:
        raise HTTPException(
            status_code=404, detail=f"Could not find company '{company_2}' in ID-Graph"
        )
    if company_1 == company_2:
        raise HTTPException(status_code=404, detail=f"Got two times the same company")


def generate_blob_name(company_1: str, company_2: str) -> str:
    return f"share-ids/{datetime.utcnow().strftime('%Y-%m-%d')}/{uuid.uuid4()}-{company_1}-{company_2}.csv"


def get_blob_client(company: str, blob_name: str) -> BlobClient:
    company_datalakes = ACCESSIBLE_RESOURCES["storage_containers"]["company-datalakes"]
    assert company in company_datalakes, f"Did not find DataLake associated to company '{company}'"

    url = os.path.join(company_datalakes[company], blob_name)
    print("Ahmed" + url)
    return BlobClient.from_blob_url(blob_url=url, credential=azure_credentials())


def write_mapping_to_company_data_lake(blob_client: BlobClient, mapping: DataFrame) -> None:
    blob_client.upload_blob(data=mapping.to_csv(sep=";", index=False))


@app.get("/share_person/")
async def read_item(company_1: str, company_2: str):
    bc_id_graph = ai.AzureBlob(
       url=ACCESSIBLE_RESOURCES["storage_containers"]["meta-id-table"]
    )
    df_id_graph = bc_id_graph.read_latest_blob_to_df()
    validate_companies(df_id_graph.columns, company_1, company_2)

    mapping_df = generate_share_mapping_person(
        df_id_graph=df_id_graph, company_1=company_1, company_2=company_2
    )

    blob_name = generate_blob_name(company_1, company_2)
    return_dict = {}
    for company, mapping in mapping_df.items():
        target_blob = get_blob_client(company, blob_name)
        write_mapping_to_company_data_lake(blob_client=target_blob, mapping=mapping)
        return_dict[company] = target_blob.url

    return return_dict

@app.get("/share_cell/")
async def read_item(company_1: str, company_2: str):
    bc_id_graph = ai.AzureBlob(
       url=ACCESSIBLE_RESOURCES["storage_containers"]["meta-id-table"]
    )
    df_id_graph = bc_id_graph.read_latest_blob_to_df()

    validate_companies(df_id_graph.columns, company_1, company_2)
    mapping_df = generate_share_mapping_cell(
        df_id_graph=df_id_graph, company_1=company_1, company_2=company_2
    )
    blob_name = generate_blob_name(company_1, company_2)
    return_dict = {}
    for company, mapping in mapping_df.items():
        target_blob = get_blob_client(company, blob_name)
        write_mapping_to_company_data_lake(blob_client=target_blob, mapping=mapping)
        return_dict[company] = target_blob.url

    return return_dict

