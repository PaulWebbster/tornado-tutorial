from urllib.parse import urlencode
from http.cookiejar import CookieJar
from urllib.request import build_opener
from urllib.request import HTTPRedirectHandler, HTTPHandler, HTTPSHandler, HTTPCookieProcessor

from multiprocessing import Process

import time

from authentication import main


class TestLogin:

    main_url = "http://localhost:8888"
    login_url = "http://localhost:8888/auth/login"
    correct_values = dict(
        name="pawel",
        password="pkbcilwl"
    )
    incorrect_values = dict(
        name="adam",
        password="mysecret"
    )

    def setup_method(self, method):
        self.cookies = CookieJar()
        self.opener = build_opener(
            HTTPRedirectHandler(),
            HTTPHandler(debuglevel=0),
            HTTPSHandler(debuglevel=0),
            HTTPCookieProcessor(self.cookies)
        )
        self.application_process = Process(target=main)
        self.application_process.start()

    def teardown_method(self, method):
        self.application_process.terminate()

    def test_correct_user_can_log_in(self):
        data = urlencode(self.correct_values).encode('utf-8')
        response = self.opener.open(self.login_url, data)
        assert "Hello, pawel".encode('utf-8') in response.read()
        assert len(self.cookies) == 1

    def test_incorrect_user_cannot_log_in(self):
        data = urlencode(self.incorrect_values).encode('utf-8')
        response = self.opener.open(self.login_url, data)
        assert "incorrect password or username".encode('utf-8') in response.read()
        assert len(self.cookies) == 0
