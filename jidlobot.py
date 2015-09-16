# -*- coding: utf-8 -*-

from datetime import datetime
from bs4 import BeautifulSoup
import yaml
import urllib2
import locale
import re
import socket

locale.setlocale(locale.LC_ALL, "cs_CZ.UTF-8")

with open("plugins/jidlobot/jidlobot.conf", 'r') as conf_file:
    config = yaml.load(conf_file)

outputs = []


def fetch_menu():
    """
    Gets today's menu.
    """

    def brana():
        """
        U Malické Brány
        """

        menu = ""
        names = []
        prices = []
        url = "http://www.menicka.cz/1631-u-malicke-brany.html"

        try:
            html = BeautifulSoup(urllib2.urlopen(url, timeout=config["HTTP_TIMEOUT"]).read(), "html5lib")
            day = html.findAll("div", {"class": "menicka"})[0]

            for j in day.findAll("div", {"class": "nabidka_1"}):
                names.append(" ".join(j.text.strip().split()))

            for j in day.findAll("div", {"class": "cena"}):
                prices.append(j.text.strip())

            x = 0
            while x < len(names):
                line = u"• " + names[x] + " " + prices[x]
                menu += line + "\n"
                x += 1

            return u"*U Malické Brány:*\n" + menu
        except socket.timeout, e:
            return u"*U Malické Brány:*\n timeout :angry:\n"

    def excelent():
        """
        Excelent Comix Pub
        """

        menu = ""
        names = []
        prices = []
        url = "http://www.menicka.cz/1639-comix-excelent-urban-pub.html"

        try:
            html = BeautifulSoup(urllib2.urlopen(url, timeout=config["HTTP_TIMEOUT"]).read(), "html5lib")
            day = html.findAll("div", {"class": "menicka"})[0]

            for j in day.findAll("div", {"class": "nabidka_1"}):
                names.append(j.text.strip())

            for j in day.findAll("div", {"class": "cena"}):
                prices.append(j.text.strip())

            x = 0
            while x < len(names):
                line = u"• " + names[x] + " " + prices[x]
                menu += line + "\n"
                x += 1

            return u"*Excelent Comix Pub:*\n" + menu
        except socket.timeout, e:
            return u"*Excelent Comix Pub:*\n timeout :angry:\n"

    def vegetka():
        """
        Vegetka
        """

        menu = ""
        names = []
        prices = []
        url = "http://www.menicka.cz/1615-vegetka-zdrava-vyziva.html"

        try:
            html = BeautifulSoup(urllib2.urlopen(url, timeout=config["HTTP_TIMEOUT"]).read(), "html5lib")
            day = html.findAll("div", {"class": "menicka"})[0]

            for j in day.findAll("div", {"class": "nabidka_1"}):
                names.append(j.text.strip())

            for j in day.findAll("div", {"class": "cena"}):
                prices.append(j.text.strip())

            x = 0
            while x < len(names):
                line = u"• " + names[x] + " " + prices[x]
                menu += line + "\n"
                x += 1

            return u"*Vegetka:*\n" + menu
        except socket.timeout, e:
            return u"*Vegetka:*\n timeout :angry:\n"

    return brana() + "\n" + excelent() + "\n" + vegetka()

date = datetime.strftime(datetime.now(), u"%A %-d.%-m.".encode("utf-8")).decode("utf-8").lower()
header = u"<!channel> *Obědy – " + date + ":*\n\n"
menu = header + fetch_menu()
outputs.append([config["CHANNEL"], menu])
