from typing import Dict
from pandas import DataFrame
import uuid


def generate_share_mapping_person(df_id_graph: DataFrame, company_1: str, company_2: str) -> Dict[str, DataFrame]:
    df_preprocessed = df_id_graph[[company_1, company_2]].dropna(thresh=2)
    df_preprocessed["random_id"] = df_preprocessed.apply(lambda _: str(uuid.uuid4()), axis=1)
    df_preprocessed.reset_index(drop=True, inplace=True)

    return {
        company_1: df_preprocessed[[company_1, "random_id"]].rename(columns={company_1: "crm_id"}),
        company_2: df_preprocessed[[company_2, "random_id"]].rename(columns={company_2: "crm_id"}),
    }


def generate_share_mapping_cell(df_id_graph: DataFrame, company_1: str, company_2: str) -> Dict[str, DataFrame]:
    df_preprocessed = df_id_graph[[company_1, company_2, "cell_id"]].dropna(thresh=3)
    list_cell_ids = df_preprocessed["cell_id"].unique()
    list_cell_ids = [x for x in list_cell_ids if x]
    list_uuid = []
    for i in range(0, len(list_cell_ids)):
        list_uuid.append(str(uuid.uuid4()))

    dict_cell_ids = dict(zip(list_cell_ids, list_uuid))
    df_preprocessed = df_preprocessed.replace({"cell_id": dict_cell_ids})
    df_preprocessed.reset_index(drop=True, inplace=True)

    return {
        company_1: df_preprocessed[[company_1, "cell_id"]].rename(columns={company_1: "crm_id"}),
        company_2: df_preprocessed[[company_2, "cell_id"]].rename(columns={company_2: "crm_id"}),
    }

