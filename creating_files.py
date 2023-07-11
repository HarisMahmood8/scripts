import os
import json

def create_test_case_files(test_cases):
    directory_path = 'test-data1'

    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    for test_case in test_cases:
        # Truncate the directory path and file name if necessary
        truncated_path, truncated_name = truncate_path_and_file_name(directory_path, test_case.name, 256)

        # Create the subdirectory if it doesn't exist
        if not os.path.exists(truncated_path):
            os.makedirs(truncated_path)

        # Create the file path within the subdirectory
        file_path = os.path.join(truncated_path, f"{truncated_name}.json")

        # Write the test case data to the file
        with open(file_path, 'w') as f:
            json.dump(test_case.case_data, f)

        print(f"File created: {file_path}")


def truncate_path_and_file_name(directory_path, file_name, max_length):
    # Calculate the maximum allowed length for the directory path and the file name
    max_dir_length = max_length - len(file_name) - len(os.sep) - 5  # Subtracting room for separators and extension

    # Truncate the directory path if it exceeds the maximum length
    truncated_path = directory_path[:max_dir_length]

    # Truncate the file name if it exceeds the maximum length
    truncated_name = file_name[:max_length]

    # Return the truncated directory path and file name
    return truncated_path, truncated_name

