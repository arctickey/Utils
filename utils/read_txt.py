import pandas as pd
from utils.upload_helpers import *


def read_txt(path):
    df = pd.read_table(path)
    df = df.loc[:, df.columns[:-1]]
    df.columns = ["Sample_Name", "Panel", "Marker", "Allel_1", "Allel_2"]
    df["Allel"] = list(zip(df["Allel_1"], df["Allel_2"]))
    df.drop(["Allel_1", "Allel_2", "Panel"], axis=1, inplace=True)
    df_wide = df.pivot(index="Sample_Name", columns="Marker", values="Allel")
    df_wide.reset_index(inplace=True, drop=False)
    df_wide.rename({"Sample_Name": "Próbka"}, axis=1, inplace=True)
    to_delete = ["K+", "ladder"]
    df_wide = df_wide.loc[~df["Próbka"].isin(to_delete)]
    df_wide = df_wide.to_dict(orient="records")
    return df_wide


def read_write_txt(path, apart_keys=["Próbka"], renamed_apart_keys=["opinion"]):
    df_wide = read_txt(path)
    out = gather_allels_to_one_key(df_wide, apart_keys, renamed_apart_keys)
    return out
