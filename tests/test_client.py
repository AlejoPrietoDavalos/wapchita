import pytest

from requests import Response

from wapchita.client import Wapchita

def test_send_message(wapchita: Wapchita, PHONE_TESTER: str) -> Response:
    return wapchita.send_message(phone=PHONE_TESTER, message="asd")
