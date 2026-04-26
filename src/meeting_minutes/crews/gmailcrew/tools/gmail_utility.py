import os
import base64
from email.message import EmailMessage
from email.mime.text import MIMEText
import markdown
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    {body}
</body>
</html>"""


def authenticate_gmail():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    token_path = os.path.join(base_dir, "token.json")
    creds_path = os.path.join(base_dir, "credentials.json")

    creds = None

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                raise FileNotFoundError(
                    f"credentials.json not found at {creds_path}. "
                    "Download your OAuth 2.0 credentials from Google Cloud Console "
                    "and place them in the same directory as this script."
                )
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, "w") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def create_message(sender, to, subject, body_markdown):
    md = markdown.Markdown(extensions=["tables", "fenced_code", "nl2br"])
    html_body = HTML_TEMPLATE.format(body=md.convert(body_markdown))

    msg = EmailMessage()
    msg["To"] = to
    msg["From"] = sender
    msg["Subject"] = subject
    msg.add_header("Content-Type", "text/html")
    msg.set_payload(html_body)

    return {"raw": base64.urlsafe_b64encode(msg.as_bytes()).decode()}


def create_draft(service, user_id, message_body):
    try:
        draft = service.users().drafts().create(
            userId=user_id,
            body={"message": message_body}
        ).execute()

        print(f"Draft created — ID: {draft['id']}")
        return draft

    except Exception as e:
        print(f"Failed to create draft: {e}")
        return None
