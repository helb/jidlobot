# -*- coding: utf-8 -*-

from datetime import datetime
from bs4 import BeautifulSoup
import urllib2
import locale
import re

locale.setlocale(locale.LC_ALL, "cs_CZ.UTF-8")

config = open("plugins/jidlobot/jidlobot.conf").read().split("\n")

config_channel = re.sub(r".*: ", r"", config[0]).strip()

outputs = []


def fetch_menu():
    """
    Gets today's menu.
    """

    def brana():
        """
        U Malické brány
        """

        menu = ""
        amounts = []
        names = []
        prices = []
        url = "http://www.plzen-info.cz/umalickebrany/index.php?akce=tydenni_nabidka"

        html = BeautifulSoup(urllib2.urlopen(url).read())
        for i in html.findAll("table", {"width": "99%"}):
            x = 0
            for j in i.findAll("td", {"width": "10%"}):
                if x % 2 != 0:
                    prices.append(u"" + j.text.replace(u",-  Kč", u" Kč").strip())
                else:
                    amounts.append(j.text.strip())
                x += 1

            for j in i.findAll("td", {"width": "53%"}):
                names.append(j.text.strip())

        x = 0
        while x < len(names):
            line = u"• " + re.sub(r"^g$", r"", amounts[x]) + " " + names[x] + " " + prices[x]
            line = re.sub(r"\s{2,}", r" ", line) + "\n"
            menu += line
            x += 1

        return u"*U Malické brány:*\n\n" + menu

    def excelent():
        """
        Excelent Comix Pub
        """

        menu = ""
        url = "https://www.zomato.com/plzen/comix-excelent-urban-pub-plze%C5%88"

        html = BeautifulSoup(urllib2.urlopen(url).read())
        for i in html.findAll("div", {"class": "tmi-daily"}):
            line = u"• " + re.sub(r"\s{2,}", r" ", i.text.strip()) + "\n"
            line = re.sub(r"\s{2,}", r" ", line)
            menu += line

        return u"*Excelent Comix Pub:*\n\n" + menu

    def vegetka():
        """
        Vegetka
        """

        menu = ""
        names = []
        prices = []
        url = "http://www.menicka.cz/1615-vegetka-zdrava-vyziva.html"

        html = BeautifulSoup(urllib2.urlopen(url).read())
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

        return u"*Vegetka:*\n\n" + menu

    return brana() + "\n\n" + excelent() + "\n\n" + vegetka()


date = datetime.strftime(datetime.now(), u"%A %-d.%-m.".encode("utf-8")).decode("utf-8").lower()
header = u"*Obědy – " + date + ":*\n\n"
menu = header + fetch_menu()
outputs.append([config_channel, menu])
