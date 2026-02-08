

import socket
from typing import Any, Dict

from student_profile import StudentProfile
from marshalling import marshal_rpc_request, unmarshal_rpc_response


class RPCClient:
    def __init__(self, host: str = 'localhost', port: int = 9000):
        self.host = host
        self.port = port

    def call(self, method_name: str, **params) -> Any:
        # create socket connection
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            # connect to server
            client_socket.connect((self.host, self.port))

            # marshal request
            request = marshal_rpc_request(method_name, params)

            # send request
            client_socket.sendall(request)

            # receive response
            response_data = client_socket.recv(4096)

            # unmarshal response
            result, error = unmarshal_rpc_response(response_data)

            # check for errors
            if error:
                raise Exception(f"remote call failed: {error}")

            return result

        finally:
            client_socket.close()

    def calculate_grade_average(self, profile: StudentProfile) -> float:
        # convert profile to dictionary
        profile_dict = profile.to_dict()

        # make remote call
        return self.call('calculate_grade_average', profile=profile_dict)


def test_valid_request():
    print("\n test 1: valid student profile ")
    client = RPCClient()

    profile = StudentProfile(
        name="alice johnson",
        id=12345,
        grades=[85, 90, 92, 88, 95]
    )

    try:
        average = client.calculate_grade_average(profile)
        print(f"student: {profile.name}")
        print(f"grades: {profile.grades}")
        print(f"average: {average:.2f}")
        print("test passed")
    except Exception as e:
        print(f"test failed: {e}")


def test_invalid_id_type():
    print("\n test 2: invalid id type (string instead of int) ")
    client = RPCClient()

    invalid_profile_dict = {
        'name': 'bob smith',
        'id': '67890',  # string instead of int - should fail validation
        'grades': [78, 82, 85]
    }

    try:
        result = client.call('calculate_grade_average', profile=invalid_profile_dict)
        print(f"test failed: should have raised TypeError but got result: {result}")
    except Exception as e:
        if "type" in str(e).lower():
            print(f"expected error caught: {e}")
            print("test passed - validate_types() correctly rejected invalid type")
        else:
            print(f"test failed with unexpected error: {e}")


def test_invalid_grade_type():
    print("\n test 3: invalid grade type (string in grades list) ")
    client = RPCClient()

    invalid_profile_dict = {
        'name': 'charlie davis',
        'id': 11111,
        'grades': [88, '92', 85]  # string in grades list - should fail validation
    }

    try:
        result = client.call('calculate_grade_average', profile=invalid_profile_dict)
        print(f"test failed: should have raised TypeError but got result: {result}")
    except Exception as e:
        if "type" in str(e).lower() or "integer" in str(e).lower():
            print(f"expected error caught: {e}")
            print("test passed - validate_types() correctly rejected invalid type")
        else:
            print(f"test failed with unexpected error: {e}")


def test_missing_field():
    print("\n test 4: missing required field ")
    client = RPCClient()

    # create profile with missing 'grades' field
    invalid_profile_dict = {
        'name': 'diana evans',
        'id': 22222
        # missing 'grades' field
    }

    try:
        result = client.call('calculate_grade_average', profile=invalid_profile_dict)
        print(f"test failed: should have raised TypeError but got result: {result}")
    except Exception as e:
        if "missing" in str(e).lower() or "type" in str(e).lower():
            print(f"expected error caught: {e}")
            print("test passed - validate_types() correctly caught missing field")
        else:
            print(f"test failed with unexpected error: {e}")


if __name__ == "__main__":
    print("rpc client test suite")

    import time
    print("\nwaiting 2 seconds for server connection...")
    time.sleep(2)

    # run all tests
    test_valid_request()
    test_invalid_id_type()
    test_invalid_grade_type()
    test_missing_field()

    print("\n" + "=" * 50)
    print("test suite completed")
