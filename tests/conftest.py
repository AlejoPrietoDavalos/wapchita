from datetime import datetime, UTC
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

import pytest

from wapchita.client import Wapchita

@pytest.fixture
def wap_url_base() -> str: return os.getenv("WAP_URL_BASE")
@pytest.fixture
def wap_api_key() -> str: return os.getenv("WAP_API_KEY")
@pytest.fixture
def wap_device_id() -> str: return os.getenv("WAP_DEVICE_ID")
@pytest.fixture
def wap_phone() -> str: return os.getenv("WAP_PHONE")
@pytest.fixture
def phone_tester() -> str: return os.getenv("PHONE_TESTER")

@pytest.fixture
def wapchita(wap_api_key: str, wap_device_id: str) -> Wapchita:
    return Wapchita(tkn=wap_api_key, device=wap_device_id)

@pytest.fixture
def path_data() -> Path:
    path_data_ = Path(__file__).parent / "data"
    path_data_.mkdir(exist_ok=True)
    return path_data_

@pytest.fixture
def text_test() -> str:
    return f"Simple text message {datetime.now(tz=UTC)}"

@pytest.fixture
def PATH_IMG_PNG_TEST(path_data: Path) -> Path:
    return path_data / "michis.png"

@pytest.fixture
def PATH_IMG_JPEG_TEST(path_data: Path) -> Path:
    return path_data / "michis.jpeg"
