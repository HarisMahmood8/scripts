import unittest
import os
import json
from unittest.mock import patch, mock_open
import coverage
from Processing_data import findDuplicates, writeToFiles, cleaningName, countDuplicates, TestCase

class ProcessingDataTests(unittest.TestCase):

    def test_findDuplicates(self):
        test_cases = [
            TestCase("test1", "env1", None, "./new-data/test1", "data1", None, None),
            TestCase("test2", "env2", None, "./new-data/test2", "data2", None, None),
            TestCase("test3", "env3", None, "./new-data/test3", "data3", None, None),
            TestCase("test1", "env4", None, "./new-data/test1", "data1", None, None),
            TestCase("test4", "env5", None, "./new-data/test4", "data4", None, None),
            TestCase("test2", "env6", None, "./new-data/test2", "data2", None, None)
        ]

        unique_cases, report_df = findDuplicates(test_cases)

        self.assertIsInstance(unique_cases, list)
        self.assertIsInstance(report_df, pd.DataFrame)
        self.assertEqual(len(unique_cases), 4)
        self.assertEqual(unique_cases[0].duplicate, "no")
        self.assertEqual(unique_cases[1].duplicate, "no")
        self.assertEqual(unique_cases[2].duplicate, "no")
        self.assertEqual(unique_cases[3].duplicate, "yes*")

    def test_writeToFiles(self):
        test_cases = [
            TestCase("test1", "env1", None, "./new-data/test1", {"data": 1}, None, None),
            TestCase("test2", "env2", None, "./new-data/test2", {"data": 2}, None, None)
        ]

        temp_dir = "./temp"
        os.makedirs(temp_dir, exist_ok=True)

        writeToFiles(test_cases)

        self.assertTrue(os.path.isfile(os.path.join(temp_dir, "test1.json")))
        self.assertTrue(os.path.isfile(os.path.join(temp_dir, "test2.json")))

        for test_case in test_cases:
            file_path = os.path.join(temp_dir, test_case.name + ".json")
            if os.path.isfile(file_path):
                os.remove(file_path)
        os.rmdir(temp_dir)

    def test_cleaningName(self):
        test_case = TestCase("test_case!", "env", None, "./new-data/test_case!", {"data": 1}, None, None)

        cleaningName(test_case)

        self.assertEqual(test_case.name, "test_case")
        self.assertEqual(test_case.error, "Special characters found / Maximum characters exceeded")

    def test_countDuplicates(self):
        test_cases = [
            TestCase("test1", "env1", None, "./new-data/test1", {"data": 1}, None, "yes"),
            TestCase("test2", "env2", None, "./new-data/test2", {"data": 2}, None, "yes"),
            TestCase("test1", "env3", None, "./new-data/test1", {"data": 1}, None, "yes"),
            TestCase("test3", "env4", None, "./new-data/test3", {"data": 3}, None, "no")
        ]

        countDuplicates(test_cases)

        self.assertEqual(test_cases[0].duplicateCount, 2)
        self.assertEqual(test_cases[1].duplicateCount, 2)
        self.assertEqual(test_cases[2].duplicateCount, 2)
        self.assertEqual(test_cases[3].duplicateCount, 1)


if __name__ == "__main__":
    # Start code coverage measurement
    cov = coverage.Coverage()
    cov.start()

    unittest.main()

    # Stop code coverage measurement
    cov.stop()
    cov.report()
