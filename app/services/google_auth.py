import json
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()


def prepare_google_files():
    credentials = os.getenv("GOOGLE_CREDENTIALS_JSON")
    token = os.getenv("GOOGLE_TOKEN_JSON")

    if credentials:
        Path("credentials.json").write_text(
            json.dumps(json.loads(credentials), indent=2)
        )

    if token:
        Path("token.json").write_text(json.dumps(json.loads(token), indent=2))
