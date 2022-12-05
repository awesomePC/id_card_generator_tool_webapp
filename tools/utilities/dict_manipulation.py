import logging
from loguru import logger

def get_multi_occurrence_key_value(list_of_dicts, key_name, log=False):
    """
    # Get value of key that occurs multiple times in dictionaries of list
    # ex.
    example_list = [
        {'points': 400, 'gold': 80},
        {'points': 100, 'gold': 10},
        {'points': 100, 'gold': 10},
        {'points': 100, 'gold': 10}
    ]
    then 
        get_multi_occurrence_key_value(example_list, points)
    returns:
        [400, 100, 100, 100]
    """
    result_list = []

    if list_of_dicts:
        if isinstance(list_of_dicts, (list,)):
            for val_dict in list_of_dicts:
                #print(list_of_dicts)
                if key_name in val_dict:
                    result_list.append(val_dict[key_name])
                else:
                    print(f"list of dictionary has no key with name '{key_name}'")
                    break
        else:
            print(f"list of dictionary is not instance of list type its type is {type(list_of_dicts)}")
    else:
        print("list of dictionary cannot be empty")
    if log:
        logger.debug(
            f"Result list after getting multi occurred key value from list of dicts {result_list}"
        )
    return result_list

def sum_values_in_dict(list_of_dicts, key_name):
    """
    # sum values in dictionary
    # ex.
    example_list = [
        {'points': 400, 'gold': 80},
        {'points': 100, 'gold': 10},
        {'points': 100, 'gold': 10},
        {'points': 100, 'gold': 10}
    ]
    then 
        sum(item['gold'] for item in myLIst)
    returns:
        110
    """
    sum = None

    if list_of_dicts:
        if isinstance(list_of_dicts, (list,)):
            sum = 0
            for val_dict in list_of_dicts:
                if key_name in val_dict:
                    sum += val_dict[key_name]
                else:
                    print(f"list of dictionary has no key with name {key_name}")
                    sum = None
                    break
        else:
            print(f"list of dictionary is not instance of list type its type is {type(list_of_dicts)}")
    else:
        print("list of dictionary cannot be empty")
    return sum
