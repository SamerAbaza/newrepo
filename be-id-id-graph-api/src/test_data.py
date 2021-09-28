import pandas as pd
import numpy as np

data = {
    "com_1": ["d1_1", np.nan, "d1_4", "d1_3"],
    "com_2": ["d2_A", np.nan, np.nan, "d2_D"],
    "com_3": ["d3_6", np.nan, "d3_8", "d3_9"],
    "com_4": [np.nan, "d4_X", "d4_Y", np.nan],
    "cell_id": [1, 2, 2, 2],
}

df_id_graph = pd.DataFrame(data=data)