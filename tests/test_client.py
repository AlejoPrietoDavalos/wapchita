import pytest

from requests import Response

from wapchita.client import Wapchita


def test_send_message_text(wapchita: Wapchita, PHONE_TESTER: str, TEXT_TEST: str) -> Response:
    return wapchita.send_message(phone=PHONE_TESTER, message=TEXT_TEST)
