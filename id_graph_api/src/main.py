from fastapi import FastAPI, HTTPException
from . import azure_interactions as ai
import pandas as pd
import numpy as np
import os
import json
import uuid

app = FastAPI()

accessible_resources = os.environ["ACCESSIBLE_RESOURCES"]
accessible_resources_dict = json.loads(accessible_resources)

data = {
    "com_1": ["d1_1", np.nan, "d1_4", "d1_3"],
    "com_2": ["d2_A", np.nan, np.nan, "d2_D"],
    "com_3": ["d3_6", np.nan, "d3_8", np.nan],
    "com_4": [np.nan, "d4_X", "d4_Y", np.nan],
}

df_id_graph = pd.DataFrame(data=data)


@app.get("/share_person/")
async def read_item(company_1: str, company_2: str):
    # bc_id_graph = ai.AzureBlob(
    #    url=accessible_resources_dict["storage_containers"]["meta-id-table"]
    # )
    # df_id_graph = bc_id_graph.read_latest_blob_to_df(sep=";")

    if company_1 not in df_id_graph.columns:
        raise HTTPException(
            status_code=404, detail=f"Could not finde company '{company_1}' in ID-Graph"
        )
    if company_2 not in df_id_graph.columns:
        raise HTTPException(
            status_code=404, detail=f"Could not finde company '{company_2}' in ID-Graph"
        )
    if company_1 == company_2:
        raise HTTPException(status_code=404, detail=f"Got 2 times the same company")

    df_preprocessed = df_id_graph[[company_1, company_2]].dropna(thresh=2)
    df_preprocessed["random_id"] = df_preprocessed.apply(lambda _: uuid.uuid4(), axis=1)
    df_preprocessed.reset_index(drop=True, inplace=True)

    dict_return_1 = df_preprocessed[[company_1, "random_id"]].to_dict()
    dict_return_2 = df_preprocessed[[company_2, "random_id"]].to_dict()
    return {
        company_1: dict_return_1,
        company_2: dict_return_2,
    }


@app.get("/share_cell/")
async def read_item(company_1: str, company_2: str):
    # bc_id_graph = ai.AzureBlob(
    #    url=accessible_resources_dict["storage_containers"]["meta-id-table"]
    # )
    # df_id_graph = bc_id_graph.read_latest_blob_to_df(sep=";")

    if company_1 not in df_id_graph.columns:
        raise HTTPException(
            status_code=404, detail=f"Could not finde company '{company_1}' in ID-Graph"
        )
    if company_2 not in df_id_graph.columns:
        raise HTTPException(
            status_code=404, detail=f"Could not finde company '{company_2}' in ID-Graph"
        )
    if company_1 == company_2:
        raise HTTPException(status_code=404, detail=f"Got 2 times the same company")

    # use only rows where all information is givenn
    df_preprocessed = df_id_graph[[company_1, company_2, "cell_id"]].dropna(thresh=3)

    # create mapping dict to replace actual cell id by random id
    list_cell_ids = df_preprocessed["cell_id"].unique()
    list_cell_ids = [x for x in list_cell_ids if x]

    list_uuid = []
    for i in range(0, len(list_cell_ids)):
        list_uuid.append(uuid.uuid4())

    dict_cell_ids = dict(zip(list_cell_ids, list_uuid))

    df_return_1 = df_preprocessed[[company_1, "cell_id"]]
    df_return_2 = df_preprocessed[[company_2, "cell_id"]]

    dict_return_1 = df_return_1.replace({"cell_id": dict_cell_ids}).to_dict()
    dict_return_2 = df_return_2.replace({"cell_id": dict_cell_ids}).to_dict()

    return {
        company_1: dict_return_1,
        company_2: dict_return_2,
    }