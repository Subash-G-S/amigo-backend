import os

from dotenv import load_dotenv
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=int(os.getenv("MAIL_PORT")),
    MAIL_SERVER=os.getenv("MAIL_SERVER"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_otp_email(
    email: str,
    otp: str,
):
    try:
        message = MessageSchema(
            subject="AMIGO Password Reset OTP",
            recipients=[email],
            body=f"Your AMIGO OTP is: {otp}",
            subtype="plain",
        )

        fm = FastMail(conf)

        print("Sending OTP:", otp)

        await fm.send_message(message)

        print("Email successfully sent")

    except Exception as e:
        import traceback

        print("MAIL ERROR:", str(e))
        traceback.print_exc()