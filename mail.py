import smtplib
import mistune
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(body, subject, config):
    try:
        mail = smtplib.SMTP(config["MAIL_SERVER"], config["MAIL_PORT"])
        mail.ehlo()
        mail.starttls()
        mail.login(config["MAIL_FROM"], config["MAIL_PW"])

        css = """
        body {
            background: #eee;
            color: #333;
            font: 11pt sans-serif;
        }

        body * {
            margin: 0;
            padding: 0;
        }

        h4 {
            color: #b42112;
            font-size: 1.25em;
            font-weight: normal;
            line-height: 1.5em;
            margin: 1em 0 0.5em;
        }

        ul {
            line-height: 1.5em;
            list-style-position: outside;
            margin-left: 1.5em;
        }

        li {
            color: #333;
        }
        """

        body_html = "<html><head><style type='text/css'>" + css + "</style></head>" + "<body>" + mistune.markdown(body) + "</body></html>"

        html_part = MIMEText(body_html, "html")

        msg = MIMEMultipart()
        msg["From"] = config["MAIL_FROM"]
        msg["To"] = ", ".join(config["MAIL_TO"])
        msg["Subject"] = "[jidlobot] " + subject
        msg.attach(html_part)
        mail.sendmail(config["MAIL_FROM"], config["MAIL_TO"], msg.as_string())

        mail.quit()
    except Exception as e:
        print("Error sending e-mails: " + str(e))
