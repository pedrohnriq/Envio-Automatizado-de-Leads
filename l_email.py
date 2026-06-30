import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from dotenv import load_dotenv

load_dotenv()

class Email:

    def __init__(self):
        self.host = os.getenv("emailHostNoReply")
        self.port = int(os.getenv("emailPortNoReply"))
        self.user = os.getenv("emailUserNoReply")
        self.password = os.getenv("emailPasswordNoReply")

    def send_email(self, to, subject, body,
                   attachments=None, cc=None):

        attachments = attachments or []
        cc = cc or []

        try:
            server = smtplib.SMTP(self.host, self.port)
            server.starttls()
            server.login(self.user, self.password)

            msg = MIMEMultipart()
            msg["From"] = self.user
            msg["To"] = ", ".join(to) if isinstance(to, list) else to
            msg["Cc"] = ", ".join(cc)
            msg["Subject"] = subject

            msg.attach(MIMEText(body, "plain"))

            for file in attachments:
                with open(file, "rb") as f:
                    part = MIMEApplication(
                        f.read(),
                        Name=os.path.basename(file)
                    )
                    part["Content-Disposition"] = (
                        f'attachment; filename="{os.path.basename(file)}"'
                    )
                    msg.attach(part)

            recipients = []

            if isinstance(to, list):
                recipients.extend(to)
            else:
                recipients.append(to)

            recipients.extend(cc)

            server.sendmail(
                self.user,
                recipients,
                msg.as_string()
            )

            server.quit()

            print("E-mail enviado com sucesso!")

        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")