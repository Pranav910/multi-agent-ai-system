from jsonschema import validate, ValidationError

json_schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "age": {"type": "number"},
    },
    "required": ["name", "age"]
}

data = {
    "name": "Alice",
    "age": 30
}

def is_valid_with_schema(data, schema=json_schema):
    try:
        validate(instance=data, schema=schema)
        return True
    except ValidationError as e:
        # print(f"Validation error: {e.message}")
        return False
    
# if is_valid_with_schema(data=data, schema=json_schema):
#     print('json data is valid')
# else:
#     print('json data is not valie')