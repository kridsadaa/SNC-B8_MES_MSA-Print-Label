from datetime import datetime


def convert_to_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

def convert_to_str(value, default="Unknown"):
    return str(value or default)

def convert_to_date(value, default="01/01/1900"):
    try:
        return datetime.strptime(value, "%d/%m/%Y").strftime("%d/%m/%Y")
    except (ValueError, TypeError):
        return default

def convert_code(value):
    return value.strip() if value.strip() else "test"