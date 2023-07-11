import os
import json
from pathlib import Path

def create_test_case_files(test_cases):
    directory_path = 'test-data1'

    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    for test_case in test_cases:
        # Truncate the file name if it exceeds 256 characters
        truncated_name = truncate_string(test_case.name, 256)

        # Create the subdirectory path by joining the directory path and truncated name
        subdir_path = Path(directory_path) / truncated_name

        # Truncate the subdirectory path if it exceeds 256 characters
        truncated_path = truncate_path(subdir_path, 256)

        # Create the subdirectory if it doesn't exist
        truncated_path.mkdir(parents=True, exist_ok=True)

        # Create the file path within the subdirectory
        file_path = truncated_path / f"{truncated_name}.json"

        # Write the test case data to the file
        with open(file_path, 'w') as f:
            json.dump(test_case.case_data, f)

        print(f"File created: {file_path}")

def truncate_string(string, max_length):
    # Truncate the string if it exceeds the maximum length
    if len(string) > max_length:
        return string[:max_length]
    return string

def truncate_path(path, max_length):
    # Truncate the path components if it exceeds the maximum length
    components = path.parts
    truncated_components = [truncate_string(c, max_length) for c in components]
    truncated_path = Path(*truncated_components)
    return truncated_path

