from datetime import datetime
from bs4 import BeautifulSoup
import requests
import yaml
import locale
import re
import socket
import sys
import smtplib
import json
import mistune
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


locale.setlocale(locale.LC_ALL, "cs_CZ.UTF-8")
parser = "html5lib"

with open("jidlobot.conf", 'r') as conf_file:
    config = yaml.load(conf_file)


def fetch_menu(url):
    """
    Gets today menu from given URL at menicka.cz and output it in Markdown format.
    """

    menu = ""
    names = []
    prices = []

    try:
        result = requests.get(url)
        html = BeautifulSoup(result.content, parser)
        day = html.findAll("div", {"class": "menicka"})[0]
        restaurant = html.findAll("span", {"class": "org"})[0].text

        for j in day.findAll("div", {"class": "nabidka_1"}):
            names.append(" ".join(j.text.strip().split()))
            prices.append(j.next_sibling.next_sibling.text.strip())

        for i in range(len(names)):
            line = "- " + names[i] + " " + prices[i]
            menu += line + "\n"

        return "\n## " + restaurant + ":\n\n" + menu
    except socket.timeout:
        return "" + url + ": timeout :angry:\n"


def send_to_mattermost(body, subject):
    message = "@channel\n\n# " + subject + "\n\n" + body
    payload = json.dumps({
        "channel": config["MATTERMOST_CHANNEL"],
        "username": config["MATTERMOST_USERNAME"],
        "text": message
    })

    requests.post(config["MATTERMOST_WEBHOOK"], data=payload)


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

        body_html = "<html><head><style type='text/css'>" + css +
        "</style></head>" + "<body>" + mistune.markdown(body) + "</body></html>"

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


def get_menus():
    menus = []
    for url in config["URLS"]:
        menus.append(fetch_menu(url))
    return "\n".join(menus)


def get_title():
    date = datetime.strftime(datetime.now(), "%A %-d.%-m.")
    return "Obědy – " + date


menus = get_menus()
title = get_title()

if "mail" in config["BACKENDS"]:
    send_mail(menus, title)
if "mattermost" in config["BACKENDS"]:
    send_to_mattermost(menus, title)
