import os

import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")


def send_otp_email(
    email: str,
    otp: str,
):
    try:
        resend.Emails.send(
            {
                "from": "Amigo <onboarding@resend.dev>",
                "to": [email],
                "subject": "AMIGO Password Reset OTP",
                "text": f"Your OTP is: {otp}",
            }
        )

        print("Email successfully sent")

    except Exception as e:
        print("Resend Error:", e)
        raise