from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from email_service import config

def send_email(to_email, subject, html_content):
    message = Mail(
        from_email=config.SENDER_EMAIL,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    try:
        sg = SendGridAPIClient(config.SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Email sent to {to_email}, status code: {response.status_code}")
        return response.status_code
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return None
