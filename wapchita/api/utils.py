import asyncio
import time
import logging

import httpx
import requests
from requests import Response

from wapchita.api.headers import get_headers
from wapchita.api.urls import url_get_message

QUEUED = "queued"  # Status de mensaje en cola.
logger = logging.getLogger(__name__)


def wait_msg_sent(*, tkn: str, message_wid: str, max_tries: int = 120) -> Response:
    url = url_get_message(message_wid=message_wid)
    headers = get_headers(tkn=tkn)
    response = requests.get(url, headers=headers)
    k = 0
    while response.json()["status"] == QUEUED and k < max_tries:
        k += 1
        logger.info(f"wait_msg_sent - {message_wid} - {k}/{max_tries}")
        time.sleep(1)
        response = requests.get(url, headers=headers)
    return response


async def async_wait_msg_sent(*, tkn: str, message_wid: str, max_tries: int = 120) -> httpx.Response:
    url = url_get_message(message_wid=message_wid)
    headers = get_headers(tkn=tkn)

    async with httpx.AsyncClient() as httpx_client:
        response = await httpx_client.get(url, headers=headers)
        k = 0
        while response.json()["status"] == QUEUED and k < max_tries:
            k += 1
            logger.info(f"wait_msg_sent - {message_wid} - {k}/{max_tries}")
            await asyncio.sleep(1)
            response = await httpx_client.get(url, headers=headers)
    return response
