''' Test file for store_result.py '''
import pytest
import datetime

from store_result import dob_parser 

def test_dob_parser():
    ''' Test dob_parser False '''
    expected_result = False
    actual_result = dob_parser("Invalid test data")

    assert actual_result == expected_result


def test_dob_parser_pass():
    ''' Test dob_parser pass '''
    test_date = "10/24/1991"
    expected_result = datetime.datetime.strptime(test_date, '%m/%d/%Y')
    actual_result = dob_parser(test_date)

    assert actual_result == expected_result
