import re
import math
import copy

def validate_profile(input, sex_allels=["AMEL"], check_id=False):
    """Validates correctness of the profile record and preprocess input.
    :param profile: profile to validate
        Assumptions:
            - all values are of type string, filled in by user
            - under all keys there is a string input inside lists
            - values are comma separated
            - dot is used for fractions notation
            - only X, Y, number characters accepted
            - removes empty allels
        Example: {"allels": {"AMEL": ["X", "X"], "example": ["1.1", "2"]}, "opinion": "xyz"}
    :param sex_allels: markers names for allels defining sex i.e. AMEL
    :param check_id: to determine if ID validation is needed
    :returns:
        - flag - True if profile is correct, False if must be returned to user to correct
        - message - if profile is incorrect - error message to user
        - profile - preprocessed profile with good data types
    """
    profile = copy.deepcopy(input)
    # Preprocess all allels
    for key, allel in profile["allels"].items():
        for i, value in enumerate(allel):
            if value is None or (value != value):
                value = ""
            value = str(value)
            # Remove spaces
            value = "".join(value.split())
            value = value.strip()
            # Check for disallowed characters
            if allel and key not in sex_allels:
                if not bool(re.search(r"^[0-9]+\.?[0-9]*$", value)) and value != "":
                    return (
                        False,
                        "ERROR: Wprowadzono niedozwolone znaki.",
                        profile,
                    )
            allel[i] = value
        # Remove empty strings
        allel[:] = [x for x in allel if x]
        profile["allels"][key] = allel
    
    # Remove empty allels
    to_remove = []
    for key, value in profile["allels"].items():
        if profile["allels"][key] == []:
            to_remove.append(key)

    for key in to_remove:
        profile["allels"].pop(key, None)

    # Numeric markers
    numeric_markers = set(profile["allels"].keys()) - set(sex_allels)
    for key in numeric_markers:
        value = profile["allels"][key]
        # Cast strings to numeric
        try:
            value[:] = [float(x) for x in value]
        except ValueError as e:
            return (
                False,
                "ERROR: Wprowadzono nieprawid??owe dane w chromosomach autosomalnych.",
                profile,
            )
        profile["allels"][key] = value

    # Sex chromosome
    for key, value in profile["allels"].items():
        if key in sex_allels and value is not None:
            for marker in value:
                marker = marker.upper()
                if marker not in ["X", "Y"]:
                    return (
                        False,
                        "ERROR: Wprowadzono nieprawid??owe dane w chromosomie p??ci.",
                        profile,
                    )

    # Check sample identifier
    if check_id:
        if len(profile["opinion"]) == 0:
            return (False, "ERROR: Uzupe??nij identyfikator pr??bki.", profile)

    # Positive check and preprocess
    return (True, "Pomy??lna walidacja profilu.", profile)
