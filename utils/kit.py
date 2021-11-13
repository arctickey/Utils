def insert_kit(db, kit: str):
    """Inserts kit to the kits' collection.
    :param db: database connection to client.ZMS
    :param kit: dictionary in schema {"name": "abc", "allels": ["a", "b", "c"]}
    """
    # Check for Name or Allels duplicate
    if db["kits"].count_documents({"name": kit["name"]}, limit=1) != 0:
        raise Exception("Kit with specified name already exists.")
    elif db["kits"].count_documents({"allels": kit["allels"]}, limit=1) != 0:
        raise Exception("Kit with specified allels' markers already exists.")
    # Insert
    db["kits"].insert_one(kit)
    return


def load_kit(db, kit_name: str):
    """Loads kit from the kits' collection.
    :param db: database connection to client.ZMS
    :param kit_name: name of the kit passed during inserting
    """
    kit = db.kits.find_one({"name": kit_name})
    if kit is None:
        raise Exception("Kit with specified name doesn't exist.")
    return kit


def delete_kit(db, kit_name: str):
    """Deletes kit from the kits' collection.
    :param db: database connection to client.ZMS
    :param kit_name: name of the kit to delete
    """
    # Check if kit with passed name exists
    if db["kits"].count_documents({"name": kit_name}, limit=1) == 0:
        raise Exception("Kit with specified name doesn't exist.")
    # Delete
    db["kits"].delete_one({"name": kit_name})
    return


def update_kit(db, kit_to_modify_name, new_kit):
    """Handles modification of kit definition.
    Enables edition of both kit_name and allels.
    :param db: database connection to client.ZMS
    :param kit_name: name of the kit that user wants to modify
    :param new_kit: full kit in schema {"name": "abc", "allels": ["a", "b", "c"]}
    """
    # Delete old version
    delete_kit(db, kit_to_modify_name)
    # Insert new version
    insert_kit(db, new_kit)
    return
