import pytest
from extract import extract
from tests.test_cases import TEST_CASES

"""
Test Case Categories:
1. Only valid JSON in the input string, true
2. Valid JSON in the response, between JSON blocks ```json ```, true
3. Additional text at beginning or end, no json blocks, but there is valid json somewhere in the input string, true
4. No valid JSON in input string, false
"""

@pytest.mark.parametrize("test_description, input_string, expected_result", TEST_CASES)
def test_extract(test_description, input_string, expected_result):
    json_data, success = extract(input_string)
    assert success == expected_result, f"Failed: {test_description}"
