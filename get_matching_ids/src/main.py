from fastapi import FastAPI, HTTPException

from azure_interactions import AzureBlob

import uuid

app = FastAPI()

storage_container_url = "https://felix0test0storage0acc.blob.core.windows.net/id-graph"

bc_id_graph = AzureBlob(url=storage_container_url)
df_id_graph = bc_id_graph.read_latest_blob_to_df(sep=";")

# data = {
#    "com_1": ["d1_1", np.nan, "d1_4", "d1_3"],
#    "com_2": ["d2_A", np.nan, np.nan, "d2_D"],
#    "com_3": ["d3_6", np.nan, "d3_8", np.nan],
#    "com_4": [np.nan, "d4_X", "d4_Y", np.nan],
# }

# df_id_graph = pd.DataFrame(data=data)


@app.get("/matching-ids/")
async def read_item(company_1: str, company_2: str):
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
