from pymongo import MongoClient


def connect(host="localhost", port=27017):
    """Connect to MongoDB"""
    return MongoClient(host, port)


def is_id(x):
    return not x[0] == "_id"


def read_mongo(db: str = "ZMS", collection: str = "profile", no_id: bool = False):
    """Read from Mongo and Store into DataFrame"""
    conn = connect()
    db = conn[db]
    collection = db[collection]
    df = list(collection.find())
    if no_id:
        df = [dict(filter(is_id, list(x.items()))) for x in df]
    return df


def save_mongo(df: dict, db: str = "ZMS", collection: str = "profile"):
    """Read from dict and saves to MongoDB"""
    conn = connect()
    db = conn[db]
    collection = db[collection]
    collection.insert_many(df)
    return True


def drop_duplicates(df: list) -> list:
    """Drop duplicates from list of dictionaries"""
    df = [dict(filter(is_id, list(x.items()))) for x in df]
    no_dups = []
    for x in df:
        if x not in no_dups:
            no_dups.append(x)
    return no_dups


def acces_mongo_base(db: str = "ZMS", collection: str = "profile"):
    """Returning pointer for mongoDB"""
    conn = connect()
    db = conn[db]
    return db[collection].find({})
