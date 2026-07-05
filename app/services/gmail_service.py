import base64
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def send_otp_email(email: str, otp: str):
    creds = Credentials.from_authorized_user_file(
        "token.json",
        SCOPES,
    )

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(f"Your AMIGO OTP is: {otp}")

    message["to"] = email
    message["from"] = "amigoamrita@gmail.com"
    message["subject"] = "AMIGO Password Reset OTP"

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={"raw": raw},
    ).execute()

    print("Email sent successfully")