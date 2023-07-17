def test_writeToFiles(self):
        test_cases = [
            TestCase("test1", "env1", "", "./new-data/test1", {"data": 1}, None, None),
            TestCase("test2", "env2", "", "./new-data/test2", {"data": 2}, None, None),
            TestCase("test3", "env3", "", "./new-data/test3", {"data": 3}, None, None),
        ]

        # Mock the os.path.exists function to return True
        with patch("os.path.exists", return_value=True):
            # Mock the open function to do nothing (since we're not writing actual files)
            with patch("builtins.open", mock_open()):
                writeToFiles(test_cases)

        # Add assertions to verify the behavior of writeToFiles
        # Here, you can check if the expected file paths are created and if the mock file writing is called appropriately
        # You can also assert any other desired side effects or behavior of the function

        # Example assertions:
        self.assertEqual(os.path.exists("./new-data/test1/test1.json"), True)  # Asserts the existence of the file for test1
        self.assertEqual(os.path.exists("./new-data/test2/test2.json"), True)  # Asserts the existence of the file for test2
        self.assertEqual(os.path.exists("./new-data/test3/test3.json"), True)  # Asserts the existence of the file for test3
