from unittest.case import TestCase

import pytest
import requests_mock
from roometr import Roometr, exceptions


@requests_mock.Mocker()
class TestHTTPQueries(TestCase):
    TEST_URL = 'http://api.host.com/test/'

    @classmethod
    def setUpClass(cls):
        cls.r = Roometr('test', 'test', api_host='http://api.host.com')

    def test_format_url(self, *args):
        assert self.r._format_url('sms') == 'http://api.host.com/sms/'
        assert self.r._format_url('/sms/') == 'http://api.host.com/sms/'
        assert self.r._format_url('sms/message') == 'http://api.host.com/sms/message/'

    def test_post(self, m):
        m.post(self.TEST_URL, json={'ok': True}, status_code=202)
        assert self.r.post('test', data={}) == {'ok': True}

    def test_get(self, m):
        m.get(self.TEST_URL, json={'ok': True})
        assert self.r.get('test') == {'ok': True}

    def test_bad_status_code(self, m):
        m.post(self.TEST_URL, json={'ok': True}, status_code=418)  # i am a teapot!
        with pytest.raises(exceptions.RoometrBadServerResponseException):
            self.r.post('test', data={})

    def test_403(self, m):
        m.post(self.TEST_URL, json={'ok': True}, status_code=403)
        with pytest.raises(exceptions.Roometr403Exception):
            self.r.post('test', data={})

    def test_404(self, m):
        m.post(self.TEST_URL, json={'ok': True}, status_code=404)
        with pytest.raises(exceptions.Roometr404Exception):
            self.r.post('test', data={})
