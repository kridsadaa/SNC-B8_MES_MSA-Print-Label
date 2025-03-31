from app.utils import validate


def validatePostPrintLabel(req):
    validation_schema = [
        {"key": "tag_no", "type": "int"},
        {"key": "customer_name", "type": "str"},
        {"key": "model", "type": "str"},
        {"key": "supplier", "type": "str"},
        {"key": "part_code", "type": "str"},
        {"key": "part_name", "type": "str"},
        {"key": "mat", "type": "str"},
        {"key": "color", "type": "str"},
        {"key": "producer", "type": "str"},
        {"key": "date", "type": "date"},
        {"key": "image_url", "type": "str"},
        {"key": "quantity", "type": "int"},
        {"key": "number_of_tags", "type": "int"},
        {"key": "code", "type": "str"}
    ]

    res = validate(req, validation_schema)
    return res