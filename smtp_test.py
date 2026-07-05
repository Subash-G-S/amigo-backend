import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg["Subject"] = "SMTP Test"
msg["From"] = "amigoamrita@gmail.com"
msg["To"] = "cb.sc.u4cse24117@cb.students.amrita.edu"

msg.set_content("Hello from Render!")

with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
    smtp.starttls()
    smtp.login(
        "amigoamrita@gmail.com",
        "bfeyhfiddplqanfr",
    )
    smtp.send_message(msg)

print("Sent!")