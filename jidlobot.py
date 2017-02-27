from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
import yaml
import locale
import re
import socket
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


locale.setlocale(locale.LC_ALL, "cs_CZ.UTF-8")
parser = "html5lib"

with open("jidlobot.conf", 'r') as conf_file:
    config = yaml.load(conf_file)


def fetch_menu(url):
    """
    Gets today's menu from given URL.
    """

    menu = ""
    names = []
    prices = []

    try:
        html = BeautifulSoup(urlopen(url, timeout=config["HTTP_TIMEOUT"]).read(), parser)
        day = html.findAll("div", {"class": "menicka"})[0]
        restaurant = html.findAll("span", {"class": "org"})[0].text

        for j in day.findAll("div", {"class": "nabidka_1"}):
            names.append(" ".join(j.text.strip().split()))
            prices.append(j.next_sibling.next_sibling.text.strip())

        for i in range(len(names)):
            line = "<li>" + names[i] + " " + prices[i] + "</li>"
            menu += line + "\n"

        return "\n<h2>" + restaurant + ":</h2>\n\n<ul>" + menu + "</ul>"
    except socket.timeout:
        return "" + url + ": timeout :angry:\n"


def fetch_lokal_menu(url):
    """
    Gets today's menu from Lokal/Ambiente URL.
    """

    menu = ""
    names = []
    prices = []
    try:
        html = BeautifulSoup(urlopen(url, timeout=config["HTTP_TIMEOUT"]).read(), parser)
        meals = html.findAll("img", {"alt": config["LOKAL_NAME"]})[0].parent.parent.findAll("div", {"class": "list"})[0].findAll("table")[0].findAll("tr", {"class": None})

        for line in meals:
            names.append(" ".join(line.findAll("td")[0].text.strip().split()))
            prices.append(line.findAll("td")[1].text.strip())

        for i in range(len(names)):
            line = "<li>" + names[i] + " " + prices[i] + "</li>"
            menu += line + "\n"

        return "\n<h2>" + config["LOKAL_NAME"] + ":</h2><ul>" + menu + "</ul>"
    except socket.timeout:
        return "" + url + ": timeout :angry:\n"


def send_mail(body, subject):
    """
    Sends an email, addresses and other settings are loaded from jidlobot.conf.
    """

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

        h2 {
            color: #b42112;
            font-weight: normal;
            font-size: 1.25em;
            margin: 1em 0 0.5em;
            line-height: 1.5em;
        }

        ul {
            list-style-position: outside;
            margin-left: 1.5em;
            line-height: 1.5em;
        }

        li {
            color: #333;
        }
        """
        body_html = "<html><head><style type='text/css'>" + css + "</style></head><body>" + body + "</body></html>"
        html_part = MIMEText(body_html, "html")

        for recipient  in config["MAIL_TO"]:
            msg = MIMEMultipart()
            msg["From"] = config["MAIL_FROM"]
            msg["To"] = recipient
            msg["Subject"] = subject
            msg.attach(html_part)
            mail.sendmail(config["MAIL_FROM"], recipient, msg.as_string())

        mail.quit()
    except Exception as e:
        print("Error sending e-mails: " + str(e))


def get_menus():
    menus = []
    for url in config["URLS"]:
        menus.append(fetch_menu(url))
    menus.append(fetch_lokal_menu(config["LOKAL_URL"]))
    return "\n".join(menus)


def get_title():
    date = datetime.strftime(datetime.now(), "%A %-d.%-m.")
    return "[jidlobot] Obědy – " + date

print(get_menus(), get_title())
#send_mail(get_menus(), get_title())
