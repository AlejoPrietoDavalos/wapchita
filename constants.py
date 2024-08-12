import os

from dotenv import load_dotenv

load_dotenv()

WAP_API_KEY = os.getenv("WAP_API_KEY")
WAP_DEVICE_ID = os.getenv("WAP_DEVICE_ID")
WAP_PHONE = os.getenv("WAP_PHONE")
PHONE_TESTER = os.getenv("PHONE_TESTER")
WAP_URL_BASE = os.getenv("WAP_URL_BASE")
