from pydantic import ConfigDict
from crewai.tools import BaseTool
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import mimetypes
from typing import List, Tuple, IO
from typing import Annotated, Any

# ...

load_dotenv()

class EmailSenderTool(BaseTool):
    name: str = "email_sender"
    description: str = "Sends an email to a specified recipient with a subject, body, and optional attachments."

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _run(
        self,
        subject: str,
        body: str,
        to: str,
        attachment_paths: List[str] = None,
        attachment_streams: Annotated[Any, "In-memory files"] = None,
    ) -> str:

        msg = EmailMessage()
        msg.set_content(body)
        msg['Subject'] = subject
        msg['To'] = to

        user = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_PASSWORD")
        if not user:
            return "EMAIL_USER is not set in the environment variables."
        if not password:
            return "EMAIL_PASSWORD is not set in the environment variables."

        msg['From'] = user

        # Handle file path attachments
        if attachment_paths:
            for path in attachment_paths:
                if not os.path.isfile(path):
                    return f"Attachment file not found: {path}"
                try:
                    mime_type, _ = mimetypes.guess_type(path)
                    mime_type = mime_type or "application/octet-stream"
                    maintype, subtype = mime_type.split("/", 1)

                    with open(path, "rb") as f:
                        file_data = f.read()
                        file_name = os.path.basename(path)
                        msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)
                except Exception as file_error:
                    return f"Failed to attach file '{path}': {str(file_error)}"

        # Handle in-memory stream attachments
        if attachment_streams:
            for file_stream, filename in attachment_streams:
                try:
                    mime_type, _ = mimetypes.guess_type(filename)
                    mime_type = mime_type or "application/octet-stream"
                    maintype, subtype = mime_type.split("/", 1)

                    file_stream.seek(0)
                    file_data = file_stream.read()
                    msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=filename)
                except Exception as stream_error:
                    return f"Failed to process in-memory attachment '{filename}': {str(stream_error)}"

        # Send the email
        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(user, password)
                server.send_message(msg)
            return "Email sent successfully"
        except smtplib.SMTPException as smtp_error:
            return f"SMTP error occurred: {str(smtp_error)}"
        except Exception as e:
            return f"Failed to send email: {str(e)}"
