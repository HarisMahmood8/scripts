def create_test_case_files(test_cases):
    directory_path = 'test-data1'

    # Create the directory if it doesn't exist
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    for test_case in test_cases:
        # Create the file path
        file_name = f"{test_case.name}.json"
        file_path = os.path.join(directory_path, file_name)

        # Write the test case data to the file
        with open(file_path, 'w') as f:
            json.dump(test_case.case_data, f)

        print(f"File created: {file_path}")

if __name__ == "__main__":
    Test_Cases, df = generate_full(environment_precedence)

    unique_cases, df = remove_duplicates(Test_Cases)

    print(f"Number of Unique Test Cases: {len(unique_cases)}")
    df.to_csv("./Duplicates_Report.csv", index=False)

    create_test_case_files(unique_cases)
