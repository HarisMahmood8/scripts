from test_case import TestCase
import json
import os
import string
import pandas as pd
from config import environment_precedence


class TestCase:
    def __init__(self, name, environment, old_path, new_path, case_data, error, duplicate):
        self.name = name
        self.environment = environment
        self.old_path = old_path
        self.new_path = new_path
        self.case_data = case_data
        self.error = error
        self.duplicate= duplicate

def cleaning_up_special_characters(name, length_of_path):
    error = None
    cleaned_name = name.replace(" ", "_")
    special_char_removed_name = ''.join(c for c in cleaned_name if c.isalnum() or c == '_')
    if special_char_removed_name != cleaned_name:
        error = "Special characters found"
    return special_char_removed_name, error

# creating test case objects and storing them in list 
def test_case_generator(file_path):
    test_cases = []
    environment = None
    df = pd.DataFrame(columns = ["Directory", "File Name", "Number of Test Cases"])
    
    # assigning the environments from a hardcoded list of all environments present 
        
    try:
        # data from JSON file being converted into Python  
        with open(file_path, encoding='utf8') as f:
            data = json.load(f)

        if isinstance(data, list):
            # going through each of the arrays inside JSON file 
            for index, item in enumerate(data):  
                # storing the test case JSON object 
                case_data = item
                environment = get_environment(file_path)
                length_of_path = 41 + len(file_path) - len(environment) + 4
                # getting the name of each test case and replacing the spaces between with "_"
                names = extract_json(data)
                name, error = cleaning_up_special_characters(names[index], length_of_path)
                # naming the new file as the new name
                #file_name = f"{name}.json"
                folder = find_new_path(file_path)
                new_path = (os.path.join(folder, name)).replace("\\","/")
                old_path = file_path[:-5]

                 # process of creating test case object 
                test_case = TestCase(name = name, environment = environment, old_path = old_path, new_path = new_path, case_data = case_data, error = error, duplicate = None, folder = folder, modified_name = None)
                test_cases.append(test_case)
        

        data = pd.DataFrame([[environment, os.path.basename(file_path), len(test_cases)]],  columns = ["Directory", "File Name", "Number of Test Cases"])
        df = pd.concat([df, data], ignore_index=True)
    
    # also display errors in the report 
    except (FileNotFoundError, json.JSONDecodeError) as e:
        data = pd.DataFrame([[environment, os.path.basename(file_path), "Error Reading JSON File"]],  columns = ["Directory", "File Name", "Number of Test Cases"])
        df = pd.concat([df, data], ignore_index=True)
    
    return test_cases, df

# find where test data starts search for word test data 
def find_new_path(path):
    # original file path: something/test-data/abc/hello.json
    env = get_environment(path)
    # looking for "test-data" in path
    if f"{env}" in path.lower():
        # new file path: test-data/abc/hello
        new_path = path[path.lower().index(env)+len(env)+1:len(path)-5]
    return new_path

def get_environment(file_path):
    for env in environment_precedence:
            if "/"+env+"/" in file_path:
                return env
    return None

# Storing filepaths in a list 
def get_cases(precedence):
    paths = []
    for environment in precedence:
        filepath = "test-data/"+ environment
        # "walking" through file path 
        for root, _, files in os.walk(filepath): 
            for file in files:
                paths.append(os.path.join(root, file).replace("\\", "/"))
    return (paths)

# Finding the key for each test case and returning it 
def extract_json(json_list):
    first_level_key = []
    # going through each JSON object in JSon list
    for json_object in json_list:
        # getting each JSON Key  
        keys = list(json_object.keys()) 
        if keys:
            # only getting the first key -- which is the name, and putting it in the list  
            first_level_key.append(keys[0])
    return (first_level_key)

def generate_full(precedence):
    
    file_paths = get_cases(precedence)
    
    Test_Cases = []
    Data_Frames = []
    for path in file_paths:
        test_cases, dataFrame = test_case_generator(path)
        Test_Cases += test_cases
        Data_Frames.append(dataFrame)

    df = pd.concat(Data_Frames)
    
    return Test_Cases, df
            
if(__name__== "__main__"):
    
    Test_Cases, df = generate_full(environment_precedence)
    print(len(Test_Cases))
    df.to_csv("./Report.csv", index = False)
