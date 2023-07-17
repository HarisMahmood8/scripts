import unittest
import os
import json
from unittest.mock import patch, mock_open
import coverage
import pandas as pd
from test_case import TestCase
from Reading_files import testCaseGenerator, getNewPath, getEnvironment, getAllTestCases, getPaths, getName
from Processing_data import cleaningName, countDuplicates, findDuplicates, writeToFiles
class FileReaderTests(unittest.TestCase):

    cov = coverage.Coverage()
    cov.start() # Start code coverage measurement

    def test_testCaseGenerator(self):

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
        
            
        cov.stop()
        cov.report() # prints report
    
    def test_getNewPath(self):
        cov = coverage.Coverage() # starting code coverage
        cov.start()

        json_file = r"C:/Users/HM05256/pl_ui_automation/test-data/december/auto/capability/capping.json" # setting up mock file path

        new_path = getNewPath(json_file) # calling find new path

        expected_path = "auto/capability/capping"
        self.assertEqual(new_path, expected_path)
        # auto/capability/capping == auto/capability/capping

        cov.stop()
        cov.report() # prints report

        
    def test_getEnvironment(self):
        cov = coverage.Coverage() # starting code coverage
        cov.start()
        
        file_path = "test-data/system/auto-insprint/capping.json" # setting mock file path
        environment = getEnvironment(file_path) # should set environment = insprint
        expected_environment = "system"
        
        self.assertEqual(environment, expected_environment) # Checking insprint = insprint
        
        cov.stop()
        cov.report() # printing report
       
 
    def test_getPaths(self):
        cov = coverage.Coverage() # starting coverage
        cov.start()
        
        path = getPaths()[0] # returns the path to the first (only) file in december
        expected_path = "test-data/system/auto/capability/advance_clearance.json"
        
        self.assertEqual(path, expected_path) # checks that path found is equivalent to expected
    
        cov.stop()
        cov.report() # printing report
    
    def test_getName(self):
        cov = coverage.Coverage()
        cov.start()
        
        mock_data = """[
            {"red": "color1"},
            {"green": "color2"},
            {"blue": "color3"}
        ]"""
        
        data = json.loads(mock_data)
        keys = getName(data)
        expected_keys = ["red", "green", "blue"]
        
        self.assertEqual(keys, expected_keys)
        
        cov.stop()
        cov.report()       
        
    def test_cleaningName(self):
        
        cov = coverage.Coverage()
        cov.start()
        
        test_case = TestCase(name = "TC01!_AZ_Verify-_Thank_you_page_for_Customer_when_providing_the_same_details_for_another_Auto_policy_checking_if_length_is_too_long_for_creation_to_happen_or_exceeds_limit",
                             environment=None, 
                             old_path=None,
                             new_path = "./new-data/auto/capability/advance_clearance",
                             case_data = None
                             )
        cleaningName(test_case)
        
        expected_name = "TC01_AZ_Verify_Thank_you_page_for_Customer_when_providing_the_same_details_for_another_Auto_policy_checking_if_length_is_too_long_for_creation_to_happen_"
        expected_error = "Special characters found / Maximum characters exceeded"

        cov.stop()
        cov.report()




    def test_countDuplicates(self):
        
        cov = coverage.Coverage()
        cov.start()
        
        test_case_one = TestCase(name = "red",environment=None, old_path=None,new_path = None,case_data = {"red": "color1"},duplicate = "no")
        test_case_two = TestCase(name = "red",environment=None, old_path=None,new_path = None,case_data = {"red": "color2"},duplicate = "yes*")
        
        test_cases = [test_case_one, test_case_two]
        
        countDuplicates(test_cases)
        
        self.assertEqual(test_case_one.duplicateCount, 1)
        
        cov.stop()
        cov.report()

    # work in progress

    def test_findDuplicates(self):
        cov = coverage.Coverage()
        cov.start()
        test_cases = [
            TestCase("test1", "env1", '', "./new-data/test1", "data1", None, None),
            TestCase("test2", "env2", '', "./new-data/test2", "data2", None, None),
            TestCase("test1", "env3", '', "./new-data/test1", "data1", None, None),
        ]

        unique_cases, report_df = findDuplicates(test_cases)

        self.assertIsInstance(unique_cases, list)
        self.assertIsInstance(report_df, pd.DataFrame)
        self.assertEqual(len(unique_cases), 2)
        self.assertEqual(test_cases[0].duplicate, "no")
        self.assertEqual(test_cases[2].duplicate, "yes")


        cov.stop()
        cov.report()

    # work in progress


    def test_writeToFiles(self):
        cov = coverage.Coverage()
        cov.start()

        test_cases = [
                TestCase("test1", "env1", "", "./new-data/test1", {"data": 1}, None, None),
                TestCase("test2", "env2", "", "./new-data/test2", {"data": 2}, None, None),
                TestCase("test3", "env3", "", "./new-data/test3", {"data": 3}, None, None),
            ]

        # Mock the os.path.exists function to return True
        with patch("os.path.exists", return_value=True):
            with patch("builtins.open", mock_open()):
                writeToFiles(test_cases)


        self.assertEqual(os.path.exists("./new-data/test1/test1.json"), True)
        self.assertEqual(os.path.exists("./new-data/test2/test2.json"), True)            

        cov.stop()
        cov.report()

if __name__ == "__main__":
    unittest.main()
