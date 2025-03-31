import re

def find_part_code(string: str):
    match = re.search(r'\d+', string)
    if match:
        return match.group()
    return "-"

def find_part_name(string: str):
    # The original function had a bug: re.search(r'\d+', '', string).strip()
    # Corrected version:
    match = re.search(r'\d+', string)
    if match:
        # Extract everything after the part code
        code = match.group()
        name = string[string.find(code) + len(code):].strip()
        return name
    return "-"
