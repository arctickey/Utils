from utils.connect import connect


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
    :returns: kit in dictionary type
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


# %%


def load_all_kits():
    client = connect()
    db = client.ZMS
    inp = "AMEL		D3S1358		D1S1656		D2S441		D10S1248		D13S317		Penta E		D16S539		D18S51		D2S1338		CSF1PO		Penta D		TH01		vWA		D21S11		D7S820		D5S818		TPOX 		D8S1179		D12S391		D19S433		SE33		D22S1045		DYS391	FGA		DYS576	DYS570"  # NOQA
    inp = inp.replace("\t\t", "\t")
    inp = inp.split("\t")

    kit = {"name": "Fusion 6C", "allels": inp}
    insert_kit(db, kit)

    inp = (
        "D3S13		vWA		D16S539		D2S1338		AM		D8S1179		D21S11		D18S51		D19S433		TH01		FGA"
    )
    inp = inp.replace("\t\t", "\t")
    inp = inp.split("\t")

    kit = {"name": "SGM+", "allels": inp}
    insert_kit(db, kit)

    inp = "Am.	D8S1179	D21S11	D18S51	D3S1358	vWA	D16S539	D2S1338	D19S433	TH01	FGA"
    inp = inp.replace("\t\t", "\t")
    inp = inp.split("\t")

    kit = {"name": "SGM+ 2", "allels": inp}
    insert_kit(db, kit)

    inp = "D3S1358		TH01		D21S11		D18S51		Penta E		D5S818		D13S317		D7S820		D16S539		CSF1PO		Penta D		AM		vWA		D8S1179		TPOX		FGA"  # NOQA
    inp = inp.replace("\t\t", "\t")
    inp = inp.split("\t")

    kit = {"name": "PowerPlex 16", "allels": inp}
    insert_kit(db, kit)

    inp = "D3S13		vWA		D16S539		D2S1338		AM		D8S1179		SE33		D19S433		TH01		FGA		D21S11		D18S51"
    inp = inp.replace("\t\t", "\t")
    inp = inp.split("\t")

    kit = {"name": "SE Filer", "allels": inp}
    insert_kit(db, kit)
    return True
