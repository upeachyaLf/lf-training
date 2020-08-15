import pytest

from task1 import calculate_percentage

@pytest.mark.parametrize("score , total , output",[(90,100,90), (45.5,100,45.5)])
def test_calculate_percentage(score, total, output):
    percentage = calculate_percentage(score,total)
    assert percentage == output
