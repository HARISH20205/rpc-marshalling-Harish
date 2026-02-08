

import socket
import threading
from typing import Dict, Any

from student_profile import StudentProfile
from marshalling import (
    unmarshal_rpc_request,
    marshal_rpc_response,
    unmarshal_student_profile
)


def calculate_grade_average(profile: StudentProfile) -> float:

    if not profile.grades:
        raise ValueError("cannot calculate average of empty grades list")

    # calculate and return the average
    total = sum(profile.grades)
    average = total / len(profile.grades)
    return average


class RPCServer:
    def __init__(self, host: str = 'localhost', port: int = 9000):
        self.host = host
        self.port = port
        self.socket = None
        self.running = False

        # registry of available remote procedures
        self.procedures: Dict[str, callable] = {
            'calculate_grade_average': self._handle_calculate_grade_average
        }

    def _handle_calculate_grade_average(self, params: Dict[str, Any]) -> float:
        # extract profile data
        profile_data = params.get('profile')
        if not profile_data:
            raise ValueError("missing 'profile' parameter")

        # unmarshal and validate student profile types
        # this will raise TypeError if types are incorrect
        profile_bytes = profile_data.encode('utf-8') if isinstance(profile_data, str) else profile_data

        # convert profile_data dict directly since it's already deserialized
        from marshalling import validate_types
        expected_schema = {
            'name': str,
            'id': int,
            'grades': list
        }

        # validate types - this will raise TypeError if incorrect
        validate_types(profile_data, expected_schema)

        # create StudentProfile instance
        profile = StudentProfile.from_dict(profile_data)

        # calculate and return average
        return calculate_grade_average(profile)

    def start(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        self.running = True

        print(f"rpc server listening on {self.host}:{self.port}")

        while self.running:
            try:
                # accept client connection
                client_socket, address = self.socket.accept()
                print(f"connection from {address}")

                # handle client in a new thread
                client_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket,)
                )
                client_thread.start()
            except Exception as e:
                if self.running:
                    print(f"error accepting connection: {e}")

    def _handle_client(self, client_socket: socket.socket):
        try:
            # receive request data
            data = client_socket.recv(4096)
            if not data:
                return

            # unmarshal request
            method_name, params = unmarshal_rpc_request(data)
            print(f"received rpc call: {method_name}")

            # execute the requested procedure
            try:
                if method_name not in self.procedures:
                    raise ValueError(f"unknown procedure: {method_name}")

                procedure = self.procedures[method_name]
                result = procedure(params)

                # send successful response
                response = marshal_rpc_response(result, error=None)
                client_socket.sendall(response)
                print(f"sent result: {result}")

            except TypeError as e:
                # type validation error - send error response
                error_msg = f"type validation error: {str(e)}"
                response = marshal_rpc_response(None, error=error_msg)
                client_socket.sendall(response)
                print(f"type error: {error_msg}")

            except Exception as e:
                # other execution error - send error response
                error_msg = f"execution error: {str(e)}"
                response = marshal_rpc_response(None, error=error_msg)
                client_socket.sendall(response)
                print(f"error: {error_msg}")

        except Exception as e:
            print(f"error handling client: {e}")
        finally:
            client_socket.close()

    def stop(self):
        self.running = False
        if self.socket:
            self.socket.close()
        print("rpc server stopped")


if __name__ == "__main__":
    # start the server
    server = RPCServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nshutting down server...")
        server.stop()
