import pandas

from generate_share_mapping import generate_share_mapping_person, generate_share_mapping_cell


def test_generate_share_mapping_person(test_df, mock_uuid):
    output = generate_share_mapping_person(test_df, "com_1", "com_2")
    expected_output = {
        "com_1": pandas.DataFrame(
            {
                "crm_id": ["d1_1", "d1_3"],
                "random_id": ["bdd640fb-0667-4ad1-9c80-317fa3b1799d",
                              "23b8c1e9-3924-46de-beb1-3b9046685257"]
            }
        ),
        "com_2": pandas.DataFrame(
            {
                "crm_id": ["d2_A", "d2_D"],
                "random_id": ["bdd640fb-0667-4ad1-9c80-317fa3b1799d",
                              "23b8c1e9-3924-46de-beb1-3b9046685257"]
            }
        )
    }

    assert output.keys() == {"com_1", "com_2"}
    pandas.testing.assert_frame_equal(output["com_1"], expected_output["com_1"])
    pandas.testing.assert_frame_equal(output["com_2"], expected_output["com_2"])


def test_generate_share_mapping_cell(test_df, mock_uuid):
    output = generate_share_mapping_cell(test_df, "com_1", "com_3")
    expected_output = {
        "com_1": pandas.DataFrame(
            {
                "crm_id": ["d1_1", "d1_4", "d1_3"],
                "cell_id": ["bdd640fb-0667-4ad1-9c80-317fa3b1799d",
                            "23b8c1e9-3924-46de-beb1-3b9046685257",
                            "23b8c1e9-3924-46de-beb1-3b9046685257"]
            }
        ),
        "com_3": pandas.DataFrame(
            {
                "crm_id": ["d3_6", "d3_8", "d3_9"],
                "cell_id": ["bdd640fb-0667-4ad1-9c80-317fa3b1799d",
                            "23b8c1e9-3924-46de-beb1-3b9046685257",
                            "23b8c1e9-3924-46de-beb1-3b9046685257"]
            }
        )
    }

    assert output.keys() == {"com_1", "com_3"}
    pandas.testing.assert_frame_equal(output["com_1"], expected_output["com_1"])
    pandas.testing.assert_frame_equal(output["com_3"], expected_output["com_3"])