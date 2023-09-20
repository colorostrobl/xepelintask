from re import match


def tasa_format_checker(tasa):
    """
    Esta funcion checkea que la tasa recibida sea un numero entero o decimal con coma

    Parameters:
    - tasa (string): representacion en string de la tasa.

    Returns:
    - boolean: si cumple con el formato deseado o no.
    """
    pattern = r'^\d+(,\d+)?$'
    if match(pattern, tasa):
        return True
    return False
