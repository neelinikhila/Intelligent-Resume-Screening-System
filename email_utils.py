import smtplib
from email.mime.text import MIMEText


def send_interview_email(
    receiver_email,
    candidate_name,
    interview_date,
    interview_time,
    interview_mode
):

    sender_email = "resume.screening.ai@gmail.com"
    sender_password = "wzflpuudakpplcqi"

    subject = "Interview Invitation"

    body = f"""
Hello {candidate_name},

Congratulations!

Your interview has been scheduled.

Date : {interview_date}
Time : {interview_time}
Mode : {interview_mode}

Please be available on time.

Best Regards,
HR Team
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = receiver_email

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()

        print("Email Sent Successfully")

    except Exception as e:
        print("Email Error:", e)