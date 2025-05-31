from schema.json_schema import is_valid_with_schema

class JsonAgent():

    def validate_json_schema(self, data):
        return is_valid_with_schema(data)