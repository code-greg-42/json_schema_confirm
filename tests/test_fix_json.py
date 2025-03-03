import pytest
from fix_json import fix_json
from tests.test_cases import FIX_TEST_CASES

"""
Test Case Categories:
1. input string is valid json, true
2. input string is slightly off from valid json, true
3. input string is very off from valid json, false
4. input string has no json whatsoever, false
5. edge cases of each of the above
"""

@pytest.mark.parametrize("test_description, input_string, expected_result", FIX_TEST_CASES)
def test_fix_json(test_description, input_string, expected_result):
    corrected_data, success = fix_json(input_string)
    assert success == expected_result, f"Failed: {test_description}"
