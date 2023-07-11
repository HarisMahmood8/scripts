import os
import json

def create_test_case_files(test_cases):
    directory_path = 'test-data1'

    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    errors = []  # List to store encountered errors

    for test_case in test_cases:
        # Create the file name
        file_name = f"{test_case.name}.json"

        # Create the full file path
        file_path = os.path.join(directory_path, file_name)

        try:
            # Write the test case data to the file
            with open(file_path, 'w') as f:
                json.dump(test_case.case_data, f)
            print(f"File created: {file_path}")
        except Exception as e:
            errors.append((test_case.name, str(e)))
            print(f"Error creating file for test case '{test_case.name}': {str(e)}")

    # Output the encountered errors
    if errors:
        print("\nEncountered errors:")
        for name, error in errors:
            print(f"Test case '{name}': {error}")

