# %%
from utils.connect import connect, save_mongo
from utils.read_excel import read_write_excel
from utils.read_txt import read_write_txt

# %%


def _wipe_database(colllection):
    """Function to wipe out whole collection"""
    conn = connect()
    db = conn.ZMS[colllection]
    db.delete_many({})


def _fetch_and_save(collection, txt_path, excel_path):
    """Function to read and write to database excel and txt file from ZMS"""
    txt_df = read_write_txt(txt_path)
    excel_df = read_write_excel(excel_path)
    save_mongo(excel_df, collection=collection)
    save_mongo(txt_df, collection=collection)
    return txt_df, excel_df


def reload_base(collection, txt_path, excel_path):
    _wipe_database(collection)
    _fetch_and_save(collection, txt_path, excel_path)
