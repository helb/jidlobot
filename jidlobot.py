# -*- coding: utf-8 -*-

from datetime import datetime
from bs4 import BeautifulSoup
from urllib.request import urlopen
import yaml
import locale
import re
import socket
import sys
import smtplib

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
            line = "• " + names[i] + " " + prices[i]
            menu += line + "\n"

        return restaurant + ":\n" + "-" * (len(restaurant) + 1) + "\n" + menu
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
            line = "• " + names[i] + " " + prices[i]
            menu += line + "\n"

        return config["LOKAL_NAME"] + ":\n" + "-" * (len(config["LOKAL_NAME"]) + 1) + "\n" + menu
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
        header = "To:" + config["MAIL_TO"] + "\n" + "From: " + config["MAIL_FROM"] + "\n" + "Subject: " + subject + " \n"
        message = header + "\n" + body + "\n\n"
        mail.sendmail(config["MAIL_FROM"], config["MAIL_TO"], message.encode("utf-8"))
    except Exception as e:
        print("Error sending e-mails.")


def get_menus():
    menus = []
    for url in config["URLS"]:
        menus.append(fetch_menu(url))
    menus.append(fetch_lokal_menu(config["LOKAL_URL"]))
    return "\n".join(menus)


def get_title():
    date = datetime.strftime(datetime.now(), "%A %-d.%-m.")
    return "[jidlobot] Obědy – " + date

send_mail(get_menus(), get_title())
