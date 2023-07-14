import unittest
import os
import json
from your_module import findDuplicates, writeToFiles

class TestFunctions(unittest.TestCase):

    def test_findDuplicates(self):
        # Mock test cases
        test_cases = [
            TestCase("test1", "data1", "env1"),
            TestCase("test2", "data2", "env2"),
            TestCase("test3", "data3", "env3"),
            TestCase("test1", "data1", "env4"),
            TestCase("test4", "data4", "env5"),
            TestCase("test2", "data2", "env6")
        ]

        unique_cases, df = findDuplicates(test_cases)

        # Check the types of the return values
        self.assertIsInstance(unique_cases, list)
        self.assertIsInstance(df, pd.DataFrame)

        # Verify if all test cases are present in the unique_cases list
        self.assertEqual(len(unique_cases), len(test_cases))

        # Verify if duplicates are handled correctly
        self.assertEqual(unique_cases[0].duplicate, "no")
        self.assertEqual(unique_cases[1].duplicate, "no")
        self.assertEqual(unique_cases[2].duplicate, "no")
        self.assertEqual(unique_cases[3].duplicate, "yes*")
        self.assertEqual(unique_cases[4].duplicate, "no")
        self.assertEqual(unique_cases[5].duplicate, "yes*")

    def test_writeToFiles(self):
        # Mock test cases
        test_cases = [
            TestCase("test1", {"data": 1}, "env1"),
            TestCase("test2", {"data": 2}, "env2")
        ]

        # Set up a temporary directory for test files
        temp_dir = "./temp"
        os.makedirs(temp_dir, exist_ok=True)

        # Call the function
        writeToFiles(test_cases)

        # Verify if the files are created in the temporary directory
        self.assertTrue(os.path.isfile(os.path.join(temp_dir, "test1.json")))
        self.assertTrue(os.path.isfile(os.path.join(temp_dir, "test2.json")))

        # Clean up the temporary directory
        for test_case in test_cases:
            file_path = os.path.join(temp_dir, test_case.name)
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(temp_dir)


class TestCase:
    def __init__(self, name, case_data, environment):
        self.name = name
        self.case_data = case_data
        self.environment = environment

if __name__ == '__main__':
    unittest.main()
