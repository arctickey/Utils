from utils.connect import acces_mongo_base, connect, save_mongo
from bson.objectid import ObjectId

import pandas as pd 

def eval_sample(sample, pattern, keys, nr_of_errors_possible=0):
    """
    Function to evalute two samples
    keys - list with common allels
    """

    nr_of_errors = 0
    allels_with_error = []
    if len(keys) == 0:
        return 99,0
    for i in keys:
        error_flg=0
        s_in_p = len([j for j in sample[i] if j in pattern[i]])
        p_in_s = len([j for j in pattern[i] if j in sample[i]])
        if s_in_p ==2 and p_in_s == 1 : 
            nr_of_errors +=1
            error_flg=1
        if s_in_p == 1: 
            nr_of_errors +=1 
            error_flg=1
        if s_in_p == 0: 
            nr_of_errors +=2
            error_flg=1

        if nr_of_errors > nr_of_errors_possible:
            return 99,0
        if error_flg == 1 : 
            allels_with_error.append(i)
            print(i)
            
        
    return nr_of_errors, allels_with_error


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
    error_allels = []
    for cur_sample in acces_mongo_base():

        sample_keys = list(cur_sample['allels'])

        keys_to_check = list(set(pattern_keys) & set(sample_keys))
        curr_nr_of_errors, allels_errors = eval_sample(cur_sample['allels'], pattern, keys_to_check, nr_of_errors_possible)      
        if  curr_nr_of_errors <= nr_of_errors_possible:
            id_to_return.append(cur_sample)
            nr_of_errors_to_return.append(curr_nr_of_errors)
            error_allels.append(allels_errors)

    return id_to_return , nr_of_errors_to_return ,error_allels



def insert_with_drop_dubs(record_to_insert:dict):
    """Remove dupcilates if exist and add record to the data base.
       Work befoer inserting each record
       Assuming max one duplicate exist in data base 
    """
    db = connect()
    profiles, nr_of_errors,_ = mongoDB_search(record_to_insert)
    if len(nr_of_errors) == 0 :
        dict_to_insert = {}
        dict_to_insert['allels']= record_to_insert

        save_mongo([dict_to_insert])
        return
    else:
        if len(profiles[0]["allels"])> len(record_to_insert):
            comment = record_to_insert
            db['ZMS']['profile'].find_one_and_update({"_id": profiles[0]['_id']}, 
                                 {"$set": {"Duplicate": comment}})
        else :
             comment = profiles[0]['allels']
             
             dict_to_insert = {}
             dict_to_insert['allels']= record_to_insert
             dict_to_insert['Duplicate'] = comment
             print(dict_to_insert)
             save_mongo([dict_to_insert])
             db['ZMS']['profile'].remove({'_id':ObjectId(profiles[0]['_id'])}) 
    return

 
def population_stats(): 
    """Return statistinc in the form 
    {allel_name = {allel_val_1 : [number_of_occurenc, precent_occurenc_in_population ], ...},...}  """
    pointer = acces_mongo_base()

    allels_dict = {}
    for i in pointer: 
        for key,vals in i['allels'].items():
            if key in allels_dict.keys(): 
                for k in vals:
                    allels_dict[key].append(k)
            else:
                allels_dict[key] = []
                for k in vals:
                    allels_dict[key].append(k)
    
    for key,val in allels_dict.items():
        values_table = pd.Series(val).value_counts().reset_index()
        sum_of_all = values_table.iloc[:,1].sum()
        # Creating output dict 
        new_dict = {}
        for i in range(values_table.shape[0]): 
            new_dict[values_table.iloc[i,0]]=[int(values_table.iloc[i,1]),round(values_table.iloc[i,1]/sum_of_all*100,2)]
        allels_dict[key]=new_dict
    return allels_dict


def parrenthod_check(p_father: dict,mother: dict,child: dict): 
    """Cheking if father is bilogical father
    IMPORTAN!!! Profiles must be given witouth X/Y allel
    and as 'allels' from DB
    first return is IS_FATHER_FLG"""
    # matherhod check 
    mother_error_nr = 0 
    mother_error_allels = []
    for i in set(mother.keys()).intersection(set(child.keys())):
        if  len([j for j in mother[i] if j in child[i]]) == 0:
            mother_error_nr +=1 
            mother_error_allels.append(i)

    #fatherhod check 
    father_error_nr = 0 
    father_error_allels = []

    for i in set(p_father.keys()).intersection(set(child.keys())).difference(set(mother_error_allels)):
        # Creating posibitys 
        current_key_possibilites=[
        [p_father[i][0],mother[i][0]],
        [p_father[i][1],mother[i][1]],
        [p_father[i][1],mother[i][0]],
        [p_father[i][0],mother[i][1]]    
        ]
        for j in range(4):
            current_key_possibilites.append(current_key_possibilites[j][::-1])
        if not child[i] in current_key_possibilites:
            father_error_nr +=1 
            father_error_allels.append(i)
    
    if mother_error_nr > 2 : 
        return 0,mother_error_nr,mother_error_allels,father_error_nr,father_error_allels,'PROBLEM Z MATKĄ'
    if father_error_nr > 3: 
        return 0,mother_error_nr,mother_error_allels,father_error_nr,father_error_allels,'PROBLEM Z OJCEM'
    return 1,mother_error_nr,mother_error_allels,father_error_nr,father_error_allels,'OJCIEC'
            





    


    


