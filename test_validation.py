

from marshalling import validate_types
from student_profile import StudentProfile


def test_validate_types():

    print("testing validate_types() function")
    print("=" * 50)

    # define expected schema
    expected_schema = {
        'name': str,
        'id': int,
        'grades': list
    }

    # test 1: valid data
    print("\ntest 1: valid data")
    valid_data = {
        'name': 'john doe',
        'id': 12345,
        'grades': [85, 90, 92]
    }
    try:
        validate_types(valid_data, expected_schema)
        print("passed: valid data accepted")
    except TypeError as e:
        print(f"failed: {e}")

    # test 2: invalid id (string instead of int)
    print("\ntest 2: invalid id type")
    invalid_id_data = {
        'name': 'jane smith',
        'id': '67890',  # string instead of int
        'grades': [88, 92, 85]
    }
    try:
        validate_types(invalid_id_data, expected_schema)
        print("failed: should have raised TypeError")
    except TypeError as e:
        print(f"passed: correctly caught error - {e}")

    # test 3: invalid grade type
    print("\ntest 3: invalid grade type")
    invalid_grade_data = {
        'name': 'bob jones',
        'id': 11111,
        'grades': [88, '92', 85]  # string in list
    }
    try:
        validate_types(invalid_grade_data, expected_schema)
        print("failed: should have raised TypeError")
    except TypeError as e:
        print(f"passed: correctly caught error - {e}")

    # test 4: missing field
    print("\ntest 4: missing required field")
    missing_field_data = {
        'name': 'alice brown',
        'id': 22222
        # missing 'grades'
    }
    try:
        validate_types(missing_field_data, expected_schema)
        print("failed: should have raised TypeError")
    except TypeError as e:
        print(f"passed: correctly caught error - {e}")

    print("\n" + "=" * 50)
    print("all validate_types() tests completed")


def test_student_profile():

    print("\n\ntesting StudentProfile class")
    print("=" * 50)

    # create profile
    profile = StudentProfile(
        name="test student",
        id=99999,
        grades=[75, 80, 85, 90, 95]
    )

    print(f"\ncreated profile:")
    print(f"  name: {profile.name}")
    print(f"  id: {profile.id}")
    print(f"  grades: {profile.grades}")

    # test serialization
    profile_dict = profile.to_dict()
    print(f"\nserialized to dict: {profile_dict}")

    # test deserialization
    restored_profile = StudentProfile.from_dict(profile_dict)
    print(f"\ndeserialized from dict:")
    print(f"  name: {restored_profile.name}")
    print(f"  id: {restored_profile.id}")
    print(f"  grades: {restored_profile.grades}")

    print("\nStudentProfile serialization/deserialization works correctly")
    print("=" * 50)


if __name__ == "__main__":
    test_validate_types()
    test_student_profile()
    print("\nall local tests passed!")
