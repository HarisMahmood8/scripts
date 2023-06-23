from Reading_files import generate_full
import pandas as pd

def remove_duplicates(all_test_cases, precedence):
    unique_test_cases = []
    
    for test_case in all_test_cases:
        duplicate_case = False
        for unique_case in unique_test_cases:
            if test_case.case_data == unique_case.case_data:
                prior_environment_index = precedence.index(unique_case.environment)
                current_environment_index = precedence.index(test_case.environment)
                
                if current_environment_index < prior_environment_index:
                    unique_test_cases.remove(unique_case)
                    unique_test_cases.append(test_case)
                    
                duplicate_case = True
                break
        if not duplicate_case:
            unique_test_cases.append(test_case)
            
    return unique_test_cases 
    
if(__name__== "__main__"):
    
    TEST_DATA_DIRECTORY = "test-data"
    Test_Cases, df = generate_full(TEST_DATA_DIRECTORY)
        
    precedence = ["insprint", "system", "insprinttt", "systemtt", "uat", "december"]
    unique_cases = remove_duplicates(Test_Cases,precedence)
    
    print(f"Number of Unique Test Cases:{len(unique_cases)}")
