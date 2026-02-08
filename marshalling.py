

import json
from typing import Any, Dict, List


def validate_types(data: Dict[str, Any], expected_schema: Dict[str, type]) -> None:
    for field_name, expected_type in expected_schema.items():
        if field_name not in data:
            raise TypeError(f"missing required field: {field_name}")

        actual_value = data[field_name]

        # check the basic type
        if not isinstance(actual_value, expected_type):
            raise TypeError(
                f"type mismatch for field '{field_name}': "
                f"expected {expected_type.__name__}, "
                f"got {type(actual_value).__name__}"
            )

        # additional validation for list of integers (grades field)
        if field_name == 'grades' and expected_type == list:
            if not all(isinstance(grade, int) for grade in actual_value):
                raise TypeError(
                    f"all elements in 'grades' must be integers, "
                    f"but found non-integer values"
                )


def marshal_student_profile(profile_dict: Dict[str, Any]) -> bytes:

    # define expected schema for student profile
    expected_schema = {
        'name': str,
        'id': int,
        'grades': list
    }

    # validate types before marshalling
    validate_types(profile_dict, expected_schema)

    # serialize to json bytes
    json_str = json.dumps(profile_dict)
    return json_str.encode('utf-8')


def unmarshal_student_profile(data: bytes) -> Dict[str, Any]:

    # deserialize from json bytes
    json_str = data.decode('utf-8')
    profile_dict = json.loads(json_str)

    # define expected schema for student profile
    expected_schema = {
        'name': str,
        'id': int,
        'grades': list
    }

    # validate types after unmarshalling
    validate_types(profile_dict, expected_schema)

    return profile_dict


def marshal_rpc_request(method_name: str, params: Dict[str, Any]) -> bytes:

    request = {
        'method': method_name,
        'params': params
    }
    json_str = json.dumps(request)
    return json_str.encode('utf-8')


def unmarshal_rpc_request(data: bytes) -> tuple[str, Dict[str, Any]]:

    json_str = data.decode('utf-8')
    request = json.loads(json_str)
    return request['method'], request['params']


def marshal_rpc_response(result: Any, error: str = None) -> bytes:

    response = {
        'result': result,
        'error': error
    }
    json_str = json.dumps(response)
    return json_str.encode('utf-8')


def unmarshal_rpc_response(data: bytes) -> tuple[Any, str]:

    json_str = data.decode('utf-8')
    response = json.loads(json_str)
    return response['result'], response['error']
