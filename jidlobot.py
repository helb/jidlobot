# -*- coding: utf-8 -*-

from datetime import datetime
from bs4 import BeautifulSoup
import yaml
import urllib2
import locale
import re
import socket
import sys

locale.setlocale(locale.LC_ALL, "cs_CZ.UTF-8")
parser = "html5lib"

with open("plugins/jidlobot/jidlobot.conf", 'r') as conf_file:
    config = yaml.load(conf_file)


def fetch_menu(url):
    """
    Gets today's menu from given URL.
    """

    menu = ""
    names = []
    prices = []

    try:
        html = BeautifulSoup(urllib2.urlopen(url, timeout=config["HTTP_TIMEOUT"]).read(), parser)
        day = html.findAll("div", {"class": "menicka"})[0]
        restaurant = html.findAll("span", {"class": "org"})[0].text

        for j in day.findAll("div", {"class": "nabidka_1"}):
            names.append(" ".join(j.text.strip().split()))
            prices.append(j.next_sibling.next_sibling.text.strip())

        for i in range(len(names)):
            line = u"• " + names[i] + " " + prices[i]
            menu += line + "\n"

        return u"*" + restaurant + ":*\n" + menu
    except socket.timeout, e:
        return u"" + url + ": timeout :angry:\n"


def fetch_lokal_menu(url):
    """
    Gets today's menu from Lokal/Ambiente URL.
    """

    menu = ""
    names = []
    prices = []

    try:
        html = BeautifulSoup(urllib2.urlopen(url, timeout=config["HTTP_TIMEOUT"]).read(), parser)
        meals = html.findAll("img", {"alt": config["LOKAL_NAME"]})[0].parent.parent.findAll("div", {"class": "list"})[0].findAll("table")[0].findAll("tr", {"class": None})

        for line in meals:
            names.append(" ".join(line.findAll("td")[0].text.strip().split()))
            prices.append(line.findAll("td")[1].text.strip())

        for i in range(len(names)):
            line = u"• " + names[i] + " " + prices[i]
            menu += line + "\n"

        return u"*" + config["LOKAL_NAME"] + ":*\n" + menu
    except socket.timeout, e:
        return u"" + url + ": timeout :angry:\n"

menus = []

for url in config["URLS"]:
    menus.append(fetch_menu(url))

menus.append(fetch_lokal_menu(config["LOKAL_URL"]))

date = datetime.strftime(datetime.now(), u"%A %-d.%-m.".encode("utf-8")).decode("utf-8").lower()
header = u"<!channel> *Obědy – " + date + ":*\n\n"
message = header + "\n".join(menus)

outputs = []
outputs.append([config["CHANNEL"], message])
sys.exit(0)
