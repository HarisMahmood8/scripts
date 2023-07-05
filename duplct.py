import pandas as pd
from Reading_files import test_case_generator, cleaning_up_special_characters, get_cases, find_new_path

def find_duplicates(test_cases):

    # Finds duplicate test cases based on their name.
    # Returns a list of unique test cases, considering precedence.
    
    unique_cases = []
    duplicates = []

    for case in test_cases:
        if case.name not in [c.name for c in unique_cases]:
            unique_cases.append(case)
        else:
            duplicates.append(case)

    for duplicate in duplicates:
        for index, unique_case in enumerate(unique_cases):
            if duplicate.name == unique_case.name:
                if duplicate.environment in unique_case.environment:
                    # Duplicate has higher precedence, replace the existing case
                    unique_cases[index] = duplicate
                break

    return duplicates

def generate_duplicates_dataframe(duplicates):
    data = {
        "Environment": [],
        "File Name": [],
        "Data Similarity": []
    }

    unique_names = set()  # Track unique names

    for duplicate in duplicates:
        if duplicate.name in unique_names:
            data["Environment"].append(duplicate.environment)
            data["File Name"].append(duplicate.new_path)
            data["Data Similarity"].append("Duplicate")
        else:
            unique_names.add(duplicate.name)

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

    duplicate_cases = find_duplicates(test_cases)

    df_duplicates = generate_duplicates_dataframe(duplicate_cases)

    df_duplicates.to_csv("Duplicates_Report.csv", index=False)
