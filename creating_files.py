def create_test_case_files(test_cases):
    directory_path = 'test-data1'

    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    for test_case in test_cases:
        # Truncate the file name if it exceeds 256 characters
        truncated_name = test_case.name[:252] if len(test_case.name) > 256 else test_case.name

        # Create the file path
        file_name = f"{truncated_name}.json"
        file_path = os.path.join(directory_path, file_name)

        # Write the test case data to the file
        with open(file_path, 'w') as f:
            json.dump(test_case.case_data, f)

        print(f"File created: {file_path}")
