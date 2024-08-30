import pytest
from wapchita.client import Wapchita
from wapchita.api.endpoints.send_message import ResponseSendMessage
from constants import PHONE_TESTER


def test_send_msg_and_wait(wapchita: Wapchita):
    r_send_message = wapchita.send_message(phone=PHONE_TESTER, message="test_send_msg_and_wait")
    message_wid = ResponseSendMessage.from_response(response=r_send_message).data.waId
    wapchita.wait_msg_sent(message_wid=message_wid)

@pytest.mark.asyncio
async def test_async_send_msg_and_wait(wapchita: Wapchita):
    r_send_message = wapchita.send_message(phone=PHONE_TESTER, message="test_async_send_msg_and_wait")
    message_wid = ResponseSendMessage.from_response(response=r_send_message).data.waId
    response = await wapchita.async_wait_msg_sent(message_wid=message_wid)
