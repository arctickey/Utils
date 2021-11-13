import re


def validate_profile(profile, sex_allels=["AMEL"]):
    """Validates correctness of the profile record and preprocess input.
    :param profile: profile to validate
        Assumptions:
            - all values are of type string, filled in by user
            - under all keys there is a single string input inside lists
            - values are comma separated
            - dot is used for fractions notation
        Example: {"allels": {"AMEL": ["X, X"], "example": ["1.1, 2"]}, "sample": "xyz"}
    :param sex_allels: markers names for allels defining sex i.e. AMEL
    :returns:
        - flag - True if profile is correct, False if must be returned to user to correct
        - message - if profile is incorrect - error message to user
        - profile - preprocessed profile with good data types
    """
    # Preprocess all allels
    for key, value in profile["allels"].items():
        if value:
            # Check for disallowed characters
            if bool(re.search(r"[^A-Za-z0-9\.\,]+", value[0])):
                return (
                    False,
                    "ERROR: Wprowadzono niedozwolone znaki.",
                    profile,
                )
            # Remove spaces
            value = "".join(value[0].split())
            # Split on commas
            value = value.split(",")
            # Remove empty strings
            value[:] = [x for x in value if x]
            profile["allels"][key] = value

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
                "ERROR: Wprowadzono nieprawidłowe dane w chromosomach autosomalnych.",
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
                        "ERROR: Wprowadzono nieprawidłowe dane w chromosomie płci.",
                        profile,
                    )

    # Check sample identifier
    if len(profile["sample"]) == 0:
        return (False, "ERROR: Uzupełnij identyfikator próbki.", profile)

    # Positive check and preprocess
    return (True, "Pomyślna walidacja profilu.", profile)
