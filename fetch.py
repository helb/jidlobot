from bs4 import BeautifulSoup
import requests
import socket
from datetime import datetime
import locale


def fetch_menu(url, config):
    menu = ""
    names = []
    prices = []

    try:
        result = requests.get(url, timeout=config["HTTP_TIMEOUT"])
        html = BeautifulSoup(result.content, "html5lib")
        day = html.findAll("div", {"class": "menicka"})[0]
        restaurant = html.findAll("span", {"class": "org"})[0].text

        for j in day.findAll("div", {"class": "nabidka_1"}):
            names.append(" ".join(j.text.strip().split()))
            prices.append(j.next_sibling.next_sibling.text.strip())

        for i in range(len(names)):
            line = "- " + names[i] + " " + prices[i]
            menu += line + "\n"

        return "\n#### " + restaurant + ":\n\n" + menu
    except socket.timeout:
        return "" + url + ": timeout :angry:\n"


def get_menus(config):
    menus = []
    for url in config["URLS"]:
        menus.append(fetch_menu(url, config))
    return "\n".join(menus)


def get_title():
    locale.setlocale(locale.LC_ALL, "cs_CZ.UTF-8")
    date = datetime.strftime(datetime.now(), "%A %-d.%-m.")
    return "Obědy – " + date
