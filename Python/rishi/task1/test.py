import pytest
import argparse
import sys

from datetime import date
from unittest import mock
# from mock import MagicMock
from io import StringIO
from types import SimpleNamespace

from store_result import validate_choice, numeric_type, calc_percent, date_validation, write_to_file, get_args, append_contents, make_list
from show_result import read_records

def test_validate_choice():
    assert validate_choice('English') == 'English'
    assert validate_choice('english') == 'English'

def test_argument_type_error():
    with pytest.raises(argparse.ArgumentTypeError) as validate_choice_info:
        validate_choice(1)
    with pytest.raises(argparse.ArgumentTypeError) as numeric_type_info:
        numeric_type('a')
    with pytest.raises(argparse.ArgumentTypeError) as date_validation_info:
        date_validation('2019/01/01')
    assert "Not a valid Type" in str(validate_choice_info.value)
    assert "Must be a number type" in str(numeric_type_info.value)
    assert "Not a valid date: 2019/01/01" in str(date_validation_info.value)

def test_numeric_type():
    assert numeric_type(1) == 1.0
    assert numeric_type(2.0) == 2.0
    assert numeric_type(3.1) != 3.0

def test_calc_percent():
    assert calc_percent(100, 70) == 70

def test_zero_division_error():
    with pytest.raises(ZeroDivisionError) as zero_division_error_info:
        calc_percent(0, 100)
    assert "division by zero" in str(zero_division_error_info.value)

def test_date_validation():
    assert date_validation('2019-01-01') == date.fromisoformat('2019-01-01')

def test_make_list():
    _dict = {'name': 'rishi', 'dob': date.fromisoformat('2020-08-05'), 'subject': 'English', 'score': 80, 'totalscore': 100}
    args = SimpleNamespace(**_dict)
    list_ = make_list(args)
    assert list_ == ['rishi', date.fromisoformat('2020-08-05'), 'English', 80, 100, '80.0%']

def test_append_content():
    get_content = append_contents([['a', 'b'], ['c', 'd']], ['rishi'])
    assert get_content == [['a', 'b'], ['c', 'd'], ['rishi']]

# def test_parser():
#     sys.argv = ["sys",'--name', 'rishi', '--dob', '2019-01-01', '-sub', 'English', '--score', 70, '-total', 100, '--store', 'za.csv']

#     parser = get_args(sys.argv)
    # assert parser.name == 'rishi'

# def test_write_to_file():
#     handle = MagicMock()
#     m = mock.mock_open()
#     with mock.patch('__main__.open', m, create=True):
#         write_to_file('aa.csv', [['rishi', '2019-01-01', 'Maths', 69, 100], ['Rishi', '2019-01-01', 'English', 89, 100]])
#     m.mock_calls
#     # m.assert_called_once_with('aa.csv', 'w')
#     # assert 

# def test_read_records():
#     read = StringIO()
#     with mock.patch('__main__.open', m, create=True):
#         with open('aa.csv') as f:
#             result = f.read()
#         assert result == 'A B C'
