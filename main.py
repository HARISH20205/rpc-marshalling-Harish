

from student_profile import StudentProfile
from client import RPCClient
import subprocess
import time
import sys


def demonstrate_rpc_framework():

    print("=" * 60)
    print("RPC Framework with Type Validation Demonstration")
    print("=" * 60)

    # create rpc client
    client = RPCClient()

    print("\n--- example 1: valid student profile ---")
    try:
        # create a valid student profile
        profile1 = StudentProfile(
            name="alice johnson",
            id=12345,
            grades=[85, 90, 92, 88, 95]
        )

        print(f"student: {profile1.name}")
        print(f"id: {profile1.id}")
        print(f"grades: {profile1.grades}")

        # make remote call
        average = client.calculate_grade_average(profile1)
        print(f"calculated average: {average:.2f}")
        print("success: remote procedure executed correctly\n")

    except Exception as e:
        print(f"error: {e}\n")

    print("\n--- example 2: another valid student ---")
    try:
        profile2 = StudentProfile(
            name="bob smith",
            id=67890,
            grades=[78, 82, 85, 80, 88]
        )

        print(f"student: {profile2.name}")
        print(f"id: {profile2.id}")
        print(f"grades: {profile2.grades}")

        average = client.calculate_grade_average(profile2)
        print(f"calculated average: {average:.2f}")
        print("success: remote procedure executed correctly\n")

    except Exception as e:
        print(f"error: {e}\n")

    print("\n--- example 3: demonstrating type validation ---")
    print("attempting to send invalid data (string id instead of int)...")
    try:
        # create invalid profile dict with string id
        invalid_profile = {
            'name': 'charlie davis',
            'id': '11111',  # string instead of int - should fail
            'grades': [88, 92, 85]
        }

        result = client.call('calculate_grade_average', profile=invalid_profile)
        print(f"unexpected: should have failed validation but got: {result}\n")

    except Exception as e:
        print(f"expected error caught by validate_types(): {e}")
        print("type validation is working correctly!\n")

    print("=" * 60)
    print("demonstration complete")
    print("=" * 60)
    print("\nfor more comprehensive tests, run: python client.py")
    print("(make sure server.py is running in a separate terminal)")


def main():

    print("rpc marshalling framework - lab da-1")
    print("\nthis framework implements:")
    print("- remote procedure call (rpc) system")
    print("- type validation in marshalling layer")
    print("- calculate_grade_average() remote procedure")
    print("- StudentProfile with name, id, and grades")

    print("\n" + "=" * 60)
    print("to use this framework:")
    print("=" * 60)
    print("1. start the server: python server.py")
    print("2. run the client:   python client.py")
    print("3. or run this demo: python main.py --demo")
    print("\nfor implementation details, see results.md")

    # check if demo flag is provided
    if len(sys.argv) > 1 and sys.argv[1] == '--demo':
        print("\nstarting demonstration...")
        print("note: make sure server.py is running in another terminal\n")
        time.sleep(2)
        demonstrate_rpc_framework()


if __name__ == "__main__":
    main()
