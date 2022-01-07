# %%
import pandas as pd
import numpy as np
from utils.upload_helpers import *
import math
from utils.connect import save_mongo


def take_cols(path):
    df = pd.read_excel(path, engine="openpyxl")
    cols = df.columns
    nans = list(cols[cols.str.contains("Unnamed")])
    cols = list(cols)
    lonely_ones = df[["DYS391", "DYS576", "DYS570"]]
    data = df.loc[:, ["opinia", "Próbka"]]

    for i in range(len(nans)):
        index = cols.index(nans[i])
        prev_index = index - 1
        name = cols[prev_index]
        data[name] = list(zip(df.iloc[:, prev_index], df.iloc[:, index]))
    return data, lonely_ones


def replacer(input):
    """Funkcja slużąca do wyciągania przeróżnego badziewia z tego excela i
    zamieniania tego na coś sensownego"""
    if type(input) == tuple:
        inp = list(input)
        inp = [np.NaN if x == u"\xa0*" or x == "*" else x for x in inp]
        if type(inp[0]) == str:
            inp[0] = inp[0].replace(",", ".")
        if type(inp[1]) == str:
            inp[1] = inp[1].replace(",", ".")
        t = tuple(inp)
        return t


def take_data_from_float_tuple(val):

    """Funkcja do zamieniania tupli postaci (float('nan'),float('nan'))
    na np.NaN w celu łatwiejszej filtracji później tych danych
    """
    output = []
    assert isinstance(val, tuple)
    for x in val:
        x = float(x)
        if not math.isnan(x):
            output.append(x)
    cast_to_float = map(float, val)
    all_nulls = all(map(math.isnan, cast_to_float))
    if all_nulls:
        output = np.NaN
    return output


def take_data_from_str_tuple(val):
    output = []
    for x in val:
        if isinstance(x, str):
            output.append(x)
    if not output:
        return np.NaN
    else:
        return output


def save_prepare(data):
    data = data.iloc[1:, :]
    data_dict = data.to_dict(orient="records")
    for i, d in enumerate(data_dict):
        data_dict[i] = {k: v for k, v in d.items() if str(v) != "nan"}
    return data_dict


def read_write_excel(path):
    data, lonely_ones = take_cols(path)
    cols_to_change_tuples_nans = data.columns[3:]
    for col in cols_to_change_tuples_nans:
        data[col] = data[col].apply(replacer).apply(take_data_from_float_tuple)
    data = pd.concat([data, lonely_ones], axis=1)
    data["AMEL"] = data["AMEL"].apply(take_data_from_str_tuple)
    cols = ["opinia", "Próbka"]
    data["opinion"] = data[cols].apply(
        lambda row: "_".join(row.values.astype(str)), axis=1
    )
    data.drop(cols, axis=1, inplace=True)
    data_dict = save_prepare(data)
    apart_keys = ["opinion"]
    renamed_apart_keys = ["opinion"]
    df = gather_allels_to_one_key(data_dict, apart_keys, renamed_apart_keys)
    save_mongo(df)
    return df
