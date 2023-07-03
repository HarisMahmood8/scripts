import pandas as pd
from file_reader import test_case_generator, sanitize_file_name, get_cases, find_new_path

def find_duplicates(test_cases):
    """
    Finds duplicate test cases based on their name.
    Returns a list of unique test cases, considering precedence.
    """
    unique_cases = []
    duplicates = []

    for case in test_cases:
        if case.name not in [c.name for c in unique_cases]:
            unique_cases.append(case)
        else:
            duplicates.append(case)

    for duplicate in duplicates:
        for i, unique_case in enumerate(unique_cases):
            if duplicate.name == unique_case.name:
                if duplicate.environment in unique_case.environment:
                    # Duplicate has higher precedence, replace the existing case
                    unique_cases[i] = duplicate
                break

    return unique_cases, duplicates

def generate_duplicates_dataframe(duplicates):
    """
    Generates a new DataFrame containing the duplicate test cases.
    Includes information about the environment and data similarity.
    """
    data = {
        "Environment": [],
        "File Name": [],
        "Data Similarity": []
    }

    for duplicate in duplicates:
        data["Environment"].append(duplicate.environment)
        data["File Name"].append(duplicate.new_path)
        data["Data Similarity"].append("Same" if duplicate.case_data == duplicate.case_data else "Different")

    df_duplicates = pd.DataFrame(data)
    return df_duplicates

if __name__ == "__main__":
    TEST_DATA_DIRECTORY = "test-data"
    file_paths = get_cases(TEST_DATA_DIRECTORY)

    test_cases = []
    for i in file_paths:
        input_data = i
        new_folder = find_new_path(input_data)
        cases, _ = test_case_generator(input_data, new_folder)
        test_cases += cases

    unique_cases, duplicate_cases = find_duplicates(test_cases)

    df_duplicates = generate_duplicates_dataframe(duplicate_cases)
    df_unique = pd.DataFrame([[case.environment, case.new_path, ""] for case in unique_cases], columns=["Environment", "File Name", "Data Similarity"])

    df_duplicates.to_csv("Duplicates_Report.csv", index=False)
    df_unique.to_csv("Unique_Test_Cases.csv", index=False)
