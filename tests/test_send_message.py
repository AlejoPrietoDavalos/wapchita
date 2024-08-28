import os
from wapchita import Wapchita


def test_send_message_text(wapchita: Wapchita, phone_tester: str, text_test: str) -> None:
    if not os.getenv("MOCKED_TEST_SEND_MESSAGE"):
        r = wapchita.send_message(phone=phone_tester, message=text_test)
        assert r.status_code == 201
