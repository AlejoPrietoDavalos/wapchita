from typing import List, Optional
from datetime import datetime, UTC
import re

from pydantic import BaseModel, Field

from wapchita.models.device import WapDevice
from wapchita.models._extras._webhook import WapMeta, WapLinks, MsgType
from wapchita.models.user import WapUser


class WebhookStatus(BaseModel):
   status: str
   webhookSyncedAt: Optional[str]

class WapchitaAudioMeta(BaseModel):
    duration: Optional[int] = None
    hasPreview: bool

class WapchitaAudioStats(BaseModel):
    downloads: int

class WapchitaAudioPreview(BaseModel):
    image: Optional[str] = None

class WapchitaAudioLinks(BaseModel):
    resource: str
    download: str
    chat: str
    contact: str
    message: str

class WapchitaMedia(BaseModel):
    id: str
    message: str
    chat: str
    flow: str                               # Literal["in"] #TODO: Habrá "out"?
    status: str                             # Literal["available"]
    caption: Optional[str] = None
    type: str                               # audio
    size: int
    mime: str                               # audio/mp3
    extension: str                          # mp3
    format: Optional[str | dict] = None     # ptt
    source: Optional[str] = None            # "upload"
    uploadFileId: Optional[str] = None      # Es el ID del elemento subido.
    filename: str
    createdAt: datetime
    expiresAt: datetime
    meta: WapchitaAudioMeta
    stats: WapchitaAudioStats
    preview: WapchitaAudioPreview
    links: WapchitaAudioLinks


class WapChat(BaseModel):
    id: str
    scope: str
    type: MsgType
    flow: str
    status: str
    ack: str
    from_: str = Field(alias="from")
    fromNumber: str
    to: str
    toNumber: str
    date: datetime
    timestamp: int
    body: Optional[str] = None
    chat: str
    device: WapDevice
    media: Optional[WapchitaMedia] = None
    events: dict
    webhook: WebhookStatus
    meta: WapMeta
    links: WapLinks

    @property
    def is_user(self) -> bool:
        return self.fromNumber != self.device.phone

    @property
    def is_text(self) -> bool:
        return self.type == "text"
    
    @property
    def is_image(self) -> bool:
        return self.type == "image"
    
    @property
    def is_sticker(self) -> bool:
        return self.type == "sticker"
    
    @property
    def is_video(self) -> bool:
        return self.type == "video"
    
    @property
    def is_location(self) -> bool:
        return self.type == "location"
    
    @property
    def is_audio(self) -> bool:
        return self.type == "audio"
    
    @property
    def is_document(self) -> bool:
        return self.type == "document"
    
    @property
    def is_contacts(self) -> bool:
        return self.type == "contacts"

    @property
    def file_id(self) -> str:
        url_download = self.media.links.download
        pattern = r"files/(.*)/download"
        match = re.search(pattern, url_download)
        if match:
            return match.group(1)
        raise Exception("Invalid Format.")


class WapChats(BaseModel):
    chats: List[WapChat]
    user: WapUser

    @property
    def date_last(self) -> datetime:
        return self.chats[-1].date

    @property
    def id_last(self) -> str:
        return self.chats[-1].id
    
    @property
    def id_last_user(self) -> str | None:
        for i in list(range(len(self.chats)-1,-1,-1)):
            if self.chats[i].fromNumber == self.user.phone:
                return self.chats[i].id
        return None

    @property
    def is_empty(self) -> bool:
        return len(self.chats) == 0

    # def iter_chat_specs(self) -> Generator[dict, None, None]:
    #     for chat in self.chats:
    #         yield {
    #             "user_phone": self.user.phone,
    #             "device_phone": chat.device.phone,
    #             "fromNumber": chat.fromNumber,
    #             "toNumber": chat.toNumber,
    #             "chat_id": chat.id
    #         }

    def leak_chats_by_dt(self, dt_max_secs: int) -> None:
        datetime_now = datetime.now(tz=UTC)

        if len(self.chats) > 1:
            # Caso en que el mensaje más reciente está hace más tiempo que `dt_max_secs`.
            if (datetime_now - self.chats[-1].date).seconds > dt_max_secs:
                self.chats = []
            else:
                flag, k = True, 0
                while flag and k < len(self.chats) - 1:
                    f, i = len(self.chats) - (k+1), len(self.chats) - (k+2)
                    chat_f, chat_i = self.chats[f], self.chats[i]
                    dt = (chat_f.date - chat_i.date).seconds
                    if dt > dt_max_secs:
                        self.chats = self.chats[f:]
                        flag = False
                    #print(f"{f} | {i} | {dt}")
                    k += 1
