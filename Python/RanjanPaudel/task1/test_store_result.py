import unittest
import datetime

from store_result import validate_date, validate_score

class TestDateValidation(unittest.TestCase):
    def test_incorrect_date_format(cls):
        incorrect_sample_date = '09/12/2019'

        cls.assertRaises(SystemExit, validate_date, incorrect_sample_date)
        print("---> validate_date(incorrect_date_format): Prints 'Invalid date format. Should be DD-MM-YYYY.' and exits.")

    def test_correct_date_format(cls):
        expected_date = '2019-12-09'
        result_date = validate_date('09-12-2019')

        cls.assertEqual(expected_date, result_date)
        print('---> validate_date(correct_date_format): Returns standard date format YYYY-MM-DD if the input format is DD-MM-YYYY.')

class TestScoreValidation(unittest.TestCase):
    def test_score_lt_zero(cls):
        score_lt_zero = {
            "total": 100,
            "score": -2
        }

        cls.assertRaises(SystemExit, validate_score, score_lt_zero)
        print("---> validate_score(result_with_score_less_than_zero): Prints 'Score not in valid range. \
        \n\tpython3 store_result.py --help, for detail.' and exits.")

    def test_score_gt_total(cls):
        score_gt_total = {
            "total": 100,
            "score": 103.89
        }

        cls.assertRaises(SystemExit, validate_score, score_gt_total)
        print("---> validate_score(result_with_score_greater_than_total): Prints 'Score not in valid range. \
        \n\tpython3 store_result.py --help, for detail.' and exits.")

if __name__ == "__main__":
    unittest.main()
