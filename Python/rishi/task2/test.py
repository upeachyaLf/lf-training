import pytest

from scrapper import get_per_car_url_list, AUTO_MOBILE_SEARCH_URL

def test_get_per_car_url_list():
    l1 = ['Hyundai']
    result = get_per_car_url_list(l1)

    assert result == [AUTO_MOBILE_SEARCH_URL.replace('&searchword=', f'&searchword={l1[0].lower()}')]
