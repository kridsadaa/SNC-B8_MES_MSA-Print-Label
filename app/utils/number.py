import re

def extract_number(string: str):
    if not string:
        return None

    match = re.search(r'(\d{4})$', string)
    if match:
        return int(match.group(1))
    return None
