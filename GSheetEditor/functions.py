from re import match


def tasa_format_checker(tasa):
    pattern = r'^\d+(,\d+)?$'
    if match(pattern, tasa):
        return True
    return False
