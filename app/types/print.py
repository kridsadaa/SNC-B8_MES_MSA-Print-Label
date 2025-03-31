from typing import TypedDict


class TREQ_PostPrintLabel(TypedDict):
    tag_no: int
    customer_name: str
    model: str
    supplier: str
    part_code: str
    part_name: str
    mat: str
    color: str
    producer: str
    date: str
    image_url: str
    quantity: int
    number_of_tags: int
    code: str

 