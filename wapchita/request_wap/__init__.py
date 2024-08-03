""" Requests básicas de Wapchita, actualizar al agregar."""
from typing import List
from pathlib import Path

from requests import Response

from wapchita.typings import Priority, PRIORITY_DEFAULT, SortChats, SORTCHATS_DEFAULT
from wapchita.models.device import WapDevice
from wapchita.request_wap._basics._device_by_id import device_by_id
from wapchita.request_wap._basics._download_file import download_file
from wapchita.request_wap._basics._edit_message import edit_message
from wapchita.request_wap._basics._get_chats import get_chats
from wapchita.request_wap._basics._search_chat import search_chat
from wapchita.request_wap._basics._send_message import send_message
from wapchita.request_wap._basics._update_chat_labels import update_chat_labels
from wapchita.request_wap._basics._upload_file import upload_file


class RequestWap:
    """ TODO: Encapsular requests con tenacity, de forma que sea flexible."""
    def __init__(self, *, tkn: str, device: WapDevice):
        self._tkn = tkn
        self._device: WapDevice = device
    
    @property
    def tkn(self) -> str:
        return self._tkn
    
    @property
    def device(self) -> WapDevice:
        if self._device is None:
            # FIXME: Que lo levante de un .json.
            self._device = WapDevice.from_device_id(tkn=self.tkn, device_id=self.device_id)
        return self._device
    
    @property
    def device_id(self) -> str:
        return self.device.id

    def device_by_id(self, *, device_id: str) -> Response:
        return device_by_id(tkn=self.tkn, device_id=device_id)

    def download_file(self, *, file_id: str) -> Response:
        return download_file(tkn=self.tkn, device_id=self.device.id, file_id=file_id)
    
    def edit_message(self, *, message_wid: str, text: str) -> Response:
        return edit_message(tkn=self.tkn, device_id=self.device.id, message_wid=message_wid, text=text)
    
    def get_chats(self, *, user_wid: str, sort_: SortChats = SORTCHATS_DEFAULT) -> Response:
        return get_chats(tkn=self.tkn, device_id=self.device.id, user_wid=user_wid, sort_=sort_)

    def search_chat(self, *, phone: str, device_id: str) -> Response:
        return search_chat(tkn=self.tkn, phone=phone, device_id=device_id)

    def send_message(self, *, phone: str, message: str = "", file_id: str = None, priority: Priority = PRIORITY_DEFAULT) -> Response:
        return send_message(tkn=self.tkn, phone=phone, message=message, file_id=file_id, priority=priority)

    def update_chat_labels(self, *, user_wid: str, labels: List[str] = None) -> Response:
        return update_chat_labels(tkn=self.tkn, device_id=self.device.id, user_wid=user_wid, labels=labels)
    
    def upload_file(self, *, path_file: Path) -> Response:
        return upload_file(tkn=self.tkn, path_file=path_file)