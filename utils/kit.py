def insert_kit(db, kit):
    """Inserts kit to the kits' collection.
    :param db: database connection to client.ZMS
    :param kit: dictionary in schema {"name": "abc", "Allels": ["a", "b", "c"]}
    """
    # Check for Name or Allels duplicate
    if db["kits"].count_documents({"name": kit["name"]}, limit=1) != 0:
        raise Exception("Kit with specified name already exists.")
    elif db["kits"].count_documents({"allels": kit["allels"]}, limit=1) != 0:
        raise Exception("Kit with specified allels' marker already exists.")
    # Insert
    db["kits"].insert_one(kit)
