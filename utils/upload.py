import utils
from read_excel import read_write_txt
from read_txt import read_write_excel


def wipe_database(colllection):
    conn = utils.connect()
    db = conn.ZMS[colllection]
    db.remove({})


def fetch_and_save(collection, txt_path, excel_path):
    txt_df = read_write_txt(txt_path)
    excel_df = read_write_excel(excel_path)
    utils.save_mongo(excel_df, collection=collection)
    utils.save_mongo(txt_df, collection=collection)
    return txt_df, excel_df


def do(collection,txt_path,excel_path):
    wipe_database(collection)
    fetch_and_save(txt_path, excel_path, collection)
