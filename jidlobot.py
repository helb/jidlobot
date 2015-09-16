# -*- coding: utf-8 -*-

from datetime import datetime
from bs4 import BeautifulSoup
import yaml
import urllib2
import locale
import re
import socket

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

        for j in day.findAll("div", {"class": "cena"}):
            prices.append(j.text.strip())

        x = 0
        while x < len(names):
            line = u"• " + names[x] + " " + prices[x]
            menu += line + "\n"
            x += 1

        return u"*" + restaurant + ":*\n" + menu
    except socket.timeout, e:
        return u"" + url + ": timeout :angry:\n"

menus = []
for url in config["URLS"]:
    menus.append(fetch_menu(url))

date = datetime.strftime(datetime.now(), u"%A %-d.%-m.".encode("utf-8")).decode("utf-8").lower()
header = u"<!channel> *Obědy – " + date + ":*\n\n"
message = header + "\n".join(menus)

outputs = []
outputs.append([config["CHANNEL"], message])
