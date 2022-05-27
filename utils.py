def search_by_key(dictionary, key_target, path="", _level=0):
    """Looks for a key in a nested dictionary.

    Returns:
        A tuple with
            -The value corresponding to the key_target
            -A boolean when the key_target was found
            -A path of the keys when the value is in the interior of nested dictionaries

    Note: _level is a variable used for internal functionality, don't modify it
    """
    # If key is found, return what was requested
    if key_target in dictionary:
        if path == "":
            path = key_target
        else:
            path += ".{}".format(key_target)
        result = (dictionary[key_target], True, path)
        return result

    # Search recursively in the interior dictionaries
    for key, value in dictionary.items():
        if not isinstance(value, dict):
            continue
        if path == "":
            path = key
        else:
            path += ".{}".format(key)
        result = search_by_key(value, key_target, path, _level + 1)
        if isinstance(result, tuple):
            return result

    # Return "key was not found" when all dictionaries were analyzed
    if _level == 0:
        result = (None, False, "")
        return result

dictionary_test = {
    "int_dict":{
        "int_dict_1": {
            "A": 1,
            "B": 2
        },
    },
    "int_dict_2":{
        "int_dict_2_1": {
            "int_dict_2_2": {
                "C": 3,
                "D": 4
            }
        },
    },
    "int_dict_3":{
        "int_dict_3_1": {
            "E": 5,
            "F": 6
        },
    },
}
print(search_by_key(dictionary_test, "A"))



def get_element_by_path(dictionary, path):
    keys = path.split(".")
    aux_element = dictionary
    for key in keys:
        try:
            aux_element = aux_element[key]
        except Exception as error:
            print(error)
            return None
    return aux_element
