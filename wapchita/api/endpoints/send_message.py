from typing import Literal
from datetime import datetime

import requests
from requests import Response
from requestsdantic import BaseJSON, BaseResponse

from wapchita.typings import Priority, PRIORITY_DEFAULT
from wapchita.api.urls import url_send_message
from wapchita.api.headers import get_headers_app_json


class RetryMaxCount(BaseJSON):
    max: int
    count: int


class ResponseSendMessageData(BaseJSON):
    id: str
    waId: str
    phone: str
    wid: str
    status: Literal["queued"] | str                 # FIXME: Ver todos los estados.
    deliveryStatus: Literal["queued"] | str         # FIXME: Ver todos los estados.
    createdAt: datetime
    deliverAt: datetime
    message: str
    priority: Priority
    retentionPolicy: str
    retry: RetryMaxCount
    webhookStatus: str
    device: str

class ResponseSendMessage(BaseResponse):
    data: ResponseSendMessageData

    @property
    def status_code(self) -> int:
        return 201


def send_message(
        *,
        tkn: str,
        phone: str,
        message: str = "",
        file_id: str = None,
        priority: Priority = PRIORITY_DEFAULT
    ) -> Response:
    url = url_send_message()
    json_ = {"phone": phone, "message": message, "priority": priority}
    if file_id is not None:
        json_["media"] = {"file": file_id}
    return requests.post(url=url, json=json_, headers=get_headers_app_json(tkn=tkn))
