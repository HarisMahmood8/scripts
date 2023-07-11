from Reading_files import generate_full
import pandas as pd
from config import environment_precedence

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
                # if data is not the same
                if test_case.case_data != unique_case.case_data: 
                    new_path = test_case.new_path + "_" + test_case.environment 
                    test_case.new_path = new_path # renaming based on environment
                    unique_test_cases.append(test_case)
                
                # If the duplicate has an existing key in the duplicate envs dictionary 
                if test_case.name in duplicate_environments:
                    if test_case.environment not in duplicate_environments[test_case.name]: # prevents multiple of same environment
                        duplicate_environments[test_case.name].append(test_case.environment) # environment is appended to value list
                else:
                    duplicate_environments[test_case.name] = [test_case.environment] # new key is added to dictionary with environment as value
    
                duplicate_cases.append(test_case) # list of all duplicates
                is_duplicate = True
                break
        # if test case is not a duplicate it is added to unique list
        if not is_duplicate:
            unique_test_cases.append(test_case)
    
    # Loop through each duplicate     
    for test_case in duplicate_cases:
        found_environments = duplicate_environments[test_case.name] # a list of environments for the test case
        report_data.append({
            'Name': test_case.name,
            'Environment From': test_case.environment,
            'Environment Kept': found_environments[0],
            'Found in Environments': "/".join(found_environments)
        })
    report_df = pd.DataFrame(report_data)
            
    #creates data frame merging the three lists into their own columns
    return unique_test_cases, report_df
    
if(__name__== "__main__"):
    
    Test_Cases, df = generate_full(environment_precedence)
        
    unique_cases, df = remove_duplicates(Test_Cases)
    
    print(f"Number of Unique Test Cases:{len(unique_cases)}")
    df.to_csv("./Duplicates_Report.csv", index = False)
