def insert_kit(db: str, kit: str):
    """Inserts kit to the kits' collection.
    :param db: database connection to client.ZMS
    :param kit: dictionary in schema {"Name": "abc", "Allels": ["a", "b", "c"]}
    """
    # Check for Name or Allels duplicate
    if db["kits"].count_documents({"Name": kit["Name"]}, limit=1) != 0:
        raise Exception("Kit with specified name already exists.")
    elif db["kits"].count_documents({"Allels": kit["Allels"]}, limit=1) != 0:
        raise Exception("Kit with specified allels' markers already exists.")
    # Insert
    db["kits"].insert_one(kit)


def load_kit(db: str, kit_name: str):
    """Loads kit from the kits' collection.
    :param db: database connection to client.ZMS
    :param kit_name: name of the kit passed during inserting
    """
    # try:
    kit = db["kits"].find({"Name": kit_name})
    # except:
    #     raise Exception("Kit with specified name already exists.")

    return kit
