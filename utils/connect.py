from pymongo import MongoClient
from datetime import datetime


def connect():
    """Connect to MongoDB"""
    uri = "mongodb://root:password@mongo:27017/ZMS?authSource=admin"
    return MongoClient(uri)


def is_id(x):
    return not x[0] == "_id"


def read_mongo(db: str = "ZMS", collection: str = "profile", no_id: bool = False):
    """Read from Mongo and Store into DataFrame"""
    db = connect()
    collection = db[collection]
    df = list(collection.find())
    if no_id:
        df = [dict(filter(is_id, list(x.items()))) for x in df]
    return df


def save_mongo(df: list, db: str = "ZMS", collection: str = "profile"):
    """Read from dict and saves to MongoDB"""
    assert isinstance(df, list), "Please pass list of dicts"
    for i in df:
        i["CreatedDate"] = datetime.now()
    db = connect()
    collection = db[collection]
    collection.insert_many(df)
    return True


def acces_mongo_base(db: str = "ZMS", collection: str = "profile"):

    """Returning pointer for mongoDB"""
    conn = connect()
    db = conn[db]
    return db[collection].find({})
