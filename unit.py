import unittest
import os
import json
from unittest.mock import patch, mock_open
import coverage
from test_case import TestCase
from Reading_files import testCaseGenerator, getNewPath, getEnvironment, getAllTestCases, getPaths, getName
from Processing_data import cleaningName, countDuplicates

class FileReaderTests(unittest.TestCase):

    def unitTests(self):
        cov = coverage.Coverage()
        cov.start() # Start code coverage measurement
        
        mock_file_content = """[
            {"first": "Test Case 1"},
            {"second": "Test Case 2"},
            {"third": "Test Case 3"},
            {"fourth": "Test Case 4"},
            {"fifth": "Test Case 5"},
            {"sixth": "Test Case 6"},
            {"seventh": "Test Case 7"},
            {"eighth": "Test Case 8"},
            {"ninth": "Test Case 9"},
            {"tenth": "Test Case 10"}
        ]""" # data to put in mock file

        with patch("builtins.open", mock_open(read_data=mock_file_content)): # patch replaces open w/ a mock object; mimics open
            new_folder = "test-data/system/unit_tests"

            test_cases, data_frame = testCaseGenerator(new_folder) # calling test case generator

            self.assertEqual(len(test_cases), 10)  # checks that there are 10 test cases
        
        file_path = "data/system/capping.json"
        testCases, df = testCaseGenerator(file_path)
        self.assertEqual(len(testCases), 0)
        
        json_file = r"C:/Users/HM05256/pl_ui_automation/test-data/december/auto/capability/capping.json" # setting up mock file path

        new_path = getNewPath(json_file) # calling find new path

        expected_path = "auto/capability/capping"
        self.assertEqual(new_path, expected_path)
        # auto/capability/capping == auto/capability/capping
        
        path = getPaths()[0] # returns the path to the first (only) file in december
        expected_path = "test-data/system/auto/capability/advance_clearance.json"
        
        self.assertEqual(path, expected_path) # checks that path found is equivalent to expected
        
        mock_data = """[
            {"red": "color1"},
            {"green": "color2"},
            {"blue": "color3"}
        ]"""
        
        data = json.loads(mock_data)
        keys = getName(data)
        expected_keys = ["red", "green", "blue"]
        
        self.assertEqual(keys, expected_keys)
        
        test_case = TestCase(name = "TC01!_AZ_Verify-_Thank_you_page_for_Customer_when_providing_the_same_details_for_another_Auto_policy_checking_if_length_is_too_long_for_creation_to_happen_or_exceeds_limit",
                             environment=None, 
                             old_path=None,
                             new_path = "./new-data/auto/capability/advance_clearance",
                             case_data = None
                             )
        cleaningName(test_case)
        
        expected_name = "TC01_AZ_Verify_Thank_you_page_for_Customer_when_providing_the_same_details_for_another_Auto_policy_checking_if_length_is_too_long_for_creation_to_happen_"
        expected_error = "Special characters found / Maximum characters exceeded"
        self.assertEqual(test_case.name, expected_name)
        self.assertEqual(test_case.error, expected_error)
        
        cov.stop()
        cov.report()
        

if __name__ == "__main__":
    unittest.main()
