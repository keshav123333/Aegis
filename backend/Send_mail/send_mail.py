import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from db.db import get_db
import os 

load_dotenv()

def get_friends(user_id):
    conn=get_db()
    cursor=conn.cursor()
    cursor.execute("SELECT u.email from friends f JOIN users u ON f.friend_id=u.id where f.user_id=?", (user_id,))
    friends = cursor.fetchall()
    conn.close()
    return [friend[0] for friend in friends]


def send_email(receiver_email, subject,User,location):
    body=f"""
<h1>SOS Alert</h1>

<p>User {User} needs help.</p>

<a href="{location}">
    Open Location
</a>
"""

    sender_email = os.getenv("sender_email")
    app_password = os.getenv("app_password")

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = ",".join(receiver_email) if isinstance(receiver_email, list) else receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()

        server.login(sender_email, app_password)

        server.sendmail(
            sender_email,
            receiver_email,
            msg.as_string()
        )

        server.quit()
        return {
            "status": "success",
            "message": "Email sent successfully"
        }

    except Exception as e:
        print(e)
        return False


