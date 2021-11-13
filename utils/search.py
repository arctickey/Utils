from utils.connect import acces_mongo_base, connect, save_mongo


def eval_sample(sample, pattern, keys, nr_of_errors_possible=0):
    """
    Function to evalute two samples
    keys - list with common allels
    """

    nr_of_errors = 0
    if len(keys) == 0:
        return 99
    for i in keys:
        s_in_p = len([j for j in sample[i] if j in pattern[i]])
        p_in_s = len([j for j in pattern[i] if j in sample[i]])
        if s_in_p ==2 and p_in_s == 1 : 
            nr_of_errors +=1
        if s_in_p == 1: 
            nr_of_errors +=1 
        if s_in_p == 0: 
            nr_of_errors +=2

        if nr_of_errors > nr_of_errors_possible:
            return 99
    return nr_of_errors


def mongoDB_search(pattern: dict, nr_of_errors_possible=0):
    """
    Function to search database with posible nr_of_errors_possible
    pattern - dicionary {allel : values} only with no NA values
    """

    # search
    id_to_return = []
    nr_of_errors_to_return =[]
    pattern_keys = list(pattern.keys())
    # Do zmany w całym pakiecie 
    for cur_sample in acces_mongo_base():

        sample_keys = list(cur_sample['allels'])

        keys_to_check = list(set(pattern_keys) & set(sample_keys))
        curr_nr_of_errors = eval_sample(cur_sample['allels'], pattern, keys_to_check, nr_of_errors_possible)      
        if  curr_nr_of_errors <= nr_of_errors_possible:
            id_to_return.append(cur_sample)
            nr_of_errors_to_return.append(curr_nr_of_errors)

    return id_to_return , nr_of_errors_to_return


def insert_with_drop_dubs(record_to_insert:dict):
    """Remove dupcilates if exist and add record to the data base.
       Work befoer inserting each record
       Assuming max one duplicate exist in data base 
    """
    db = connect()
    profiles, nr_of_errors = mongoDB_search(record_to_insert)
    if len(nr_of_errors) == 0 :
        save_mongo(record_to_insert)
        return
    else:
        if len(profiles[0]["allels"])> len(record_to_insert[0]["allels"]):
            comment = record_to_insert['allels']
            db['ZMS']['profile'].find_one_and_update({"_id": profiles[0]['_id']}, 
                                 {"$set": {"Comment": comment}})
        else :
             comment = profiles[0]['allels']
             record_to_insert['Comment'] = comment
             save_mongo(record_to_insert)    
    return
