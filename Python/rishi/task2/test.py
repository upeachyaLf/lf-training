import pytest

from scrapper import get_filepath_name

def test_get_filepath_name():
    filename = 'searchfile'
    filepath = 'home/lf/rishi'

    result = get_filepath_name(filepath, filename)
    assert result == 'home/lf/rishi/searchfile'
    