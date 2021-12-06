def gather_allels_to_one_key(
    data: list[dict], apart_keys: list[str], renamed_apart_keys: list[str]
) -> list[dict]:
    """Function which gather all allels in a dict a returns nested dict with all allels under one key"""
    df = []
    for i in range(len(data)):
        out = {}
        vals = [data[i][x] for x in apart_keys]
        out = dict(zip(apart_keys, vals))
        alllels = {k: v for k, v in data[i].items() if k not in apart_keys}
        out["allels"] = alllels
        for old_key, new_key in zip(apart_keys, renamed_apart_keys):
            out = rename_dict_key(out, old_key, new_key)
        df.append(out)
    return df


def rename_dict_key(d: list[dict], oldkey: str, newkey: str) -> list[dict]:
    """Helper function which renames key in a dict"""
    try:
        if newkey != oldkey:
            d[newkey] = d[oldkey]
            del d[oldkey]
    except KeyError:
        print("No such key, returning untouched dict")
    return d
