# check enum
def CheckEnum(value: str, data: dict | list) -> bool:
    if type(data) == dict:
        data = data.keys()
    
    for key in data:
        if value.lower() == key.lower():
            return True
    raise ValueError(f'{value} is not matching enum')