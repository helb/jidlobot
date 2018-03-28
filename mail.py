import smtplib
import mistune
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_mail(body, subject, config):
    # set default values
    mail_server = config.get('MAIL_SERVER','localhost')
    mail_port = config.get('MAIL_PORT',25)
    mail_from = config.get('MAIL_FROM')
    mail_to = config.get('MAIL_TO')
    mail_user = config.get('MAIL_USER', mail_from)
    mail_pw = config.get('MAIL_PW', None)
    mail_starttls = config.get('MAIL_STARTTLS', True)


    try:
        mail = smtplib.SMTP(mail_server, mail_port)
        mail.ehlo()
        if mail_starttls:
            mail.starttls()
        if mail_pw:
            mail.login(mail_user, mail_pw)

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
        msg["From"] = mail_from
        msg["To"] = ", ".join(mail_to)
        msg["Subject"] = "[jidlobot] " + subject
        msg.attach(html_part)
        mail.sendmail(mail_from, mail_to, msg.as_string())

        mail.quit()
    except Exception as e:
        print("Error sending e-mails: " + str(e))
