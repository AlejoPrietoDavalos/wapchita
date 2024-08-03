import os
from dotenv import load_dotenv
load_dotenv()

import pytest

from wapchita.client import Wapchita

@pytest.fixture
def WAP_URL_BASE() -> str: return os.getenv("WAP_URL_BASE")
@pytest.fixture
def WAP_API_KEY() -> str: return os.getenv("WAP_API_KEY")
@pytest.fixture
def WAP_DEVICE_ID() -> str: return os.getenv("WAP_DEVICE_ID")
@pytest.fixture
def WAP_PHONE() -> str: return os.getenv("WAP_PHONE")
@pytest.fixture
def PHONE_TESTER() -> str: return os.getenv("PHONE_TESTER")

@pytest.fixture
def wapchita(WAP_API_KEY: str, WAP_DEVICE_ID: str) -> Wapchita:
    return Wapchita(tkn=WAP_API_KEY, device=WAP_DEVICE_ID)
