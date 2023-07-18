def test_cleaningName(self):
    test_case = TestCase(
        name="TC01!_AZ_Verify-_Thank_you_page_for_Customer_when_providing_the_same_details_for_another_Auto_policy_checking_if_length_is_too_long_for_creation_to_happen_or_exceeds_limit_making_file_name_long_enough",
        environment=None,
        old_path=None,
        new_path="./new-data/auto/capability/advance_clearance",
        case_data=None
    )

    with patch("builtins.open", mock_open()) as mock_file:
        cleaningName(test_case)

        expected_name = "TC01_AZ_Verify_Thank_you_page_for_Customer_when_providing_the_same_details_for_another_Auto_policy_checking_if_length_is_too_long_for_creation_to_happen_or_exceeds_limit_makin"
        expected_error = "Special characters found / Maximum characters exceeded"

        self.assertEqual(test_case.name, expected_name)
        self.assertEqual(test_case.error, expected_error)

        mock_file.assert_called_once_with("./new-data/auto/capability/advance_clearance/cleaned_name.txt", "w")
        mock_file().write.assert_called_once_with(expected_name)






def test_countDuplicates(self):
    test_case_one = TestCase(
        name="red",
        environment=None,
        old_path=None,
        new_path=None,
        case_data={"red": "color1"},
        duplicate="no"
    )
    test_case_two = TestCase(
        name="red",
        environment=None,
        old_path=None,
        new_path=None,
        case_data={"red": "color2"},
        duplicate="yes*"
    )

    test_cases = [test_case_one, test_case_two]

    with patch("builtins.open", mock_open()) as mock_file:
        countDuplicates(test_cases)

        self.assertEqual(test_case_one.duplicateCount, 1)

        mock_file.assert_called_once_with("./duplicate_counts.txt", "w")
        mock_file().write.assert_called_once_with("Duplicate Counts:\nred: 1\n")
