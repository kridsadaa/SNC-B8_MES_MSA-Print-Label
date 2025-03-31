from datetime import datetime

from app.utils import convert_to_date, convert_to_str


def validate(data, keys):
    missing_keys = []

    for key_info in keys:
        key = key_info.get("key")
        expected_type = key_info.get("type")
        value = data.get(key)

        if value is None or convert_to_str(value) == "":
            missing_keys.append({"key": key, "message": "Value is missing or empty"})
        else:
            if expected_type == "int":
                if isinstance(value, str):
                    missing_keys.append({"key": key, "message": "Must be an integer, not a string"})
                else:
                    try:
                        int_value = int(value)
                        if int_value <= 0:
                            missing_keys.append({"key": key, "message": "Must be a number greater than zero"})
                    except ValueError:
                        missing_keys.append({"key": key, "message": "Cannot convert value to an integer"})
            elif expected_type == "str":
                if not isinstance(value, str):
                    missing_keys.append({"key": key, "message": "Must be a string"})
            elif expected_type == "date":
                try:
                    date_value = datetime.strptime(value, "%d/%m/%Y")
                except ValueError:
                    missing_keys.append({"key": key, "message": "Must be a date in the format dd/mm/yyyy"})

    return missing_keys
