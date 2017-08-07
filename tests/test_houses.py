from unittest.case import TestCase
from unittest.mock import patch

import pytest
import requests_mock
from roometr import Roometr, exceptions


@requests_mock.Mocker()
@patch('roometr.Roometr.check_complex', return_value=True)
class TestHouseChecking(TestCase):
    TEST_URL = 'http://api.host.com/developers/dvlpr/complexes/cmplx/houses/{house}/'

    def setUp(self):
        self.r = Roometr('test', developer='dvlpr', api_host='http://api.host.com')

    def test_house_ok(self, m, house_checker):
        m.get(self.TEST_URL.format(house='100500'), json={})
        assert self.r.check_house('cmplx', 100500)
        assert 'cmplx__100500' in self.r._checked_houses  # complex is saved in cached
        assert house_checker.call_count == 1  # delopver has been checked either

    def test_house_is_not_checked_for_the_second_time(self, *args):
        self.r._checked_houses = {'cmplx__100500'}
        assert self.r.check_house('cmplx', 100500)  # should return True without a mock

    def test_house_fail(self, m, *args):
        m.get(self.TEST_URL.format(house='100500'), status_code=404)
        with pytest.raises(exceptions.RoometrHouseNotFound):
            assert self.r.check_house('cmplx', 100500)
