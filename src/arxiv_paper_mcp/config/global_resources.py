import os

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv(), override=True)

USING_MODEL_INFO=os.getenv("USING_MODEL_INFO")
MODEL_TEMPERATURE=float(os.getenv("MODEL_TEMPERATURE", "0.0"))
MODEL_SEED=int(os.getenv("MODEL_SEED", "256"))

PDF_DOWNLOAD_PATH=os.getenv("PDF_DOWNLOAD_PATH")