import requests
from requests import Response

from wapchita.api.headers import get_headers
from wapchita.api.urls import get_url_delete_message


def delete_message(*, tkn: str, message_wid: str = "") -> Response:
    url = get_url_delete_message(message_wid=message_wid)
    headers = get_headers(tkn)
    return requests.delete(url, headers=headers)
