from datetime import datetime, UTC

import pytest

from constants import WAP_API_KEY, WAP_DEVICE_ID, PHONE_TESTER
from wapchita import Wapchita


@pytest.mark.skip(reason="Solo pueden eliminarse mensajes en "
                         "estado queued, por lo que a veces falla")
def test_send_message_text():
    wapchita = Wapchita(
        tkn=WAP_API_KEY,
        device=WAP_DEVICE_ID
    )
    response = wapchita.send_message(phone=PHONE_TESTER, message=f"Simple text message {datetime.now(tz=UTC)}")
    assert response.status_code == 201
    message_wid = response.json()['id']
    response = wapchita.delete_message(message_wid=message_wid)
    assert response.status_code == 200
