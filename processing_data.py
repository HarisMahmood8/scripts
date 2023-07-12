from Reading_files import generate_full
import pandas as pd
import os
import json
from config import environment_precedence
import pathlib

'''
Returns a list of unique test cases that were chosen (in the case of duplicates) based on precedence.
Returns a data frame of the name of duplicates, which environment was kept, which environment it is from and all the environments that duplicate was found in.
'''
def remove_duplicates(all_test_cases):
    unique_test_cases = []
    duplicate_cases = []
    report_data = []
    duplicate_environments = {}
    
    # Loop through each test case
    for test_case in all_test_cases:
        is_duplicate = False
        
        # Loop through each unique test case
        for unique_case in unique_test_cases:
            # if test case name matches existing test case name
            if test_case.name == unique_case.name:
                
                # If the duplicate has an existing key in the duplicate envs dictionary 
                if test_case.name in duplicate_environments:
                    if test_case.environment not in duplicate_environments[test_case.name]: # prevents multiple of same environment
                        duplicate_environments[test_case.name].append(test_case.environment) # environment is appended to value list
                else:
                    duplicate_environments[test_case.name] = [unique_case.environment]
                    if test_case.environment not in duplicate_environments[test_case.name]:
                        duplicate_environments[test_case.name].append(test_case.environment) # new key is added to dictionary with environment as value
                
                # if data is not the same
                if test_case.case_data != unique_case.case_data: 
                    mod_name = test_case.name + "_" + test_case.environment
                    existing_name = unique_case.modified_name
                    new_name = new_name_generator(mod_name, existing_name)
                    test_case.modified_name = new_name
                    unique_test_cases.append(test_case)
                    test_case.duplicate = "yes*"
                else:
                    test_case.duplicate = "yes"
                    duplicate_cases.append(test_case) # list of duplicates with same data
    
                is_duplicate = True
                break
        # if test case is not a duplicate it is added to unique list
        if not is_duplicate:
            test_case.duplicate = "no"
            unique_test_cases.append(test_case)
        
    #Looping through all test cases
    for test_case in [unique_test_cases, duplicate_cases]:
        found_environments = duplicate_environments[test_case.name]# a list of environments for the test case
        if found_environments != None: #If it is a duplicate
            environment_kept = found_environments[0] # found environment with highest precedence
            found_in_environments = "/".join(found_environments)
        else:
            environment_kept = test_case.environment
            found_in_environments = test_case.environment
            
        cleaning_up_name(test_case) # sets the test case name or test case modified name shorter if too long
        report_data.append({ #writes info for the report
            'Environment': test_case.environment,
            'Path': test_case.new_path,
            'Original Path': test_case.old_path,
            'Name': test_case.name,
            'Duplicate': test_case.duplicate,
            'Environment Kept': environment_kept,
            'Found in Environments': found_in_environments,
            'Naming Error': test_case.error
        })

            
    report_df = pd.DataFrame(report_data)
    #creates data frame merging the three lists into their own columns
    return unique_test_cases, report_df

# Shortening file paths that are too long and storing error
def cleaning_up_name(test_case):
    # Cases when test case data is different - so modified name has _ "env" added to name
    if test_case.modified_name != None:
        end_to_keep = test_case.modified_name[len(test_case.environment) + 1:] # "_system"
        name = test_case.modified_name[:len(test_case.environment) + 1] # Everything up to "_{env}"
        length_for_name = 250 - len(os.path.abspath(test_case.old_path)) + len(test_case.environment) - len(end_to_keep)
        if len(name) >= length_for_name:
            test_case.modified_name = f"{name[:length_for_name]}.json"
            if (test_case.error != None):
                test_case.error = "Special characters found / Maximum Characters Exceeded"
            else: 
                test_case.error = "Maximum Characters Exceeded"
    
    else:
        length_for_name = 250 - len(os.path.abspath(test_case.old_path)) + len(test_case.environment)
        if (len(test_case.name) >= length_for_name):
            test_case.name = f"{test_case.name[:length_for_name]}.json"
            if (test_case.error != None):
                test_case.error = "Special characters found / Maximum Characters Exceeded"
            else: 
                test_case.error = "Maximum Characters Exceeded"
            
            
# Recursively checks if path exists and adds "_" if it does
def new_name_generator(mod_name, existing_name):
    if mod_name != existing_name: 
        return mod_name # renaming based on environment
    else:
        new_name = mod_name + "_"
        new_name_generator(new_name, existing_name)



def create_test_case_files(test_cases):
    directory_path = "./new_data-" + test_case.folder

    if not os.path.exists(directory_path): # checks if directory path exists, if not creates it
        os.makedirs(directory_path)

    errors = []  # List to store encountered errors
    error_count = 0
    for test_case in test_cases:
        # Create the file name
        if test_case.modified_name != None:
            file_name = test_case.modified_name
        else:
            file_name = test_case.name

        file_path = os.path.join(directory_path, file_name) # create full file path
        
        try:
            # Write the test case data to the file
            with open(file_path, 'w') as f:
                json.dump(test_case.case_data, f)
            # print(f"File created: {file_path}")
        except Exception as e:
            error_count += 1
            errors.append((test_case.name, str(e)))
            print(f"Error creating file for test case '{test_case.name}': {str(e)}")

    if errors:
        print("\nEncountered errors:")
        for name, error in errors:
            print(f"Test case '{name}': \n{error}\n")
    print(error_count)




if(__name__== "__main__"):
    
    Test_Cases, df = generate_full(environment_precedence)
        
    unique_cases, df = remove_duplicates(Test_Cases)
    
    print(f"Number of Unique Test Cases:{len(unique_cases)}")
    df.to_csv("./Duplicates_Report.csv", index = False)

    create_test_case_files(unique_cases)
