# %%
from utils.connect import connect, save_mongo
from utils.read_excel import read_write_excel
from utils.read_txt import read_write_txt
from utils.search import insert_with_drop_dubs

# %%


def _wipe_database(colllection):
    """Function to wipe out whole collection"""
    conn = connect()
    db = conn.ZMS[colllection]
    db.remove({})


s


def _fetch_and_save(txt_path, excel_path):
    """Function to read and write to database excel and txt file from ZMS"""
    txt_df = read_write_txt(txt_path)
    excel_df = read_write_excel(excel_path)
    for record in txt_df:
        insert_with_drop_dubs(record)
    for record in excel_df:
        insert_with_drop_dubs(record)
    return txt_df, excel_df


def reload_base(collection, txt_path, excel_path):
    _wipe_database(collection)
    _fetch_and_save(txt_path, excel_path)
