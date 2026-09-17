import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    ORS_API_KEY = os.environ.get("ORS_API_KEY", "")
