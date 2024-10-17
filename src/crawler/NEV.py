from dotenv import load_dotenv
import os

load_dotenv()

class EnvConfig:
    HEADLESS = os.getenv("HEADLESS", "true").lower() == "true"
    NEWS_SITE_A_URL = os.getenv("NEWS_SITE_A_URL")
    NEWS_SITE_B_URL = os.getenv("NEWS_SITE_B_URL")
    THREAD_COUNT = int(os.getenv("THREAD_COUNT", 2))