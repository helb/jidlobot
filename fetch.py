from bs4 import BeautifulSoup
import requests
import socket
from datetime import datetime
import locale
import re


def fetch_menicka(url, config):
    menu = ""
    names = []
    prices = []

    try:
        result = requests.get(url, timeout=config["HTTP_TIMEOUT"])
        html = BeautifulSoup(result.content, "html5lib")
        day = html.findAll("div", {"class": "menicka"})[0]
        restaurant = html.findAll("span", {"class": "org"})[0].text

        for j in day.select("div[class='doplnujici_info']"):
            names.append(" ".join(j.text.strip().split()))
            prices.append(j.next_sibling.next_sibling.text.strip())

        for j in day.select("div[class*='nabidka_']"):
            for allergen in j.find_all("em"):
                allergen.replaceWith("")
            names.append(" ".join(j.text.strip().split()))
            prices.append(j.next_sibling.next_sibling.text.strip())

        for i in range(len(names)):
            line = "- " + names[i] + " " + prices[i]
            menu += line + "\n"

        if len(menu) > 0:
            return "\n#### " + restaurant + ":\n\n" + menu
        else:
            return ""

    except socket.timeout:
        return "" + url + ": timeout :angry:\n"


def fetch_zomato(url, config):
    menu = ""
    names = []
    prices = []

    try:
        url = re.sub(r"\?.*/?(daily-menu)?$", "/daily-menu", url)
        result = requests.get(url, timeout=config["HTTP_TIMEOUT"], headers={
            "User-Agent": config["ZOMATO_UA"],
            "Referer": url
        })
        html = BeautifulSoup(result.content, "html5lib")
        day = html.findAll("div", {"class": "tmi-group"})[0]
        restaurant = html.select("h1.res-name a")[0].text.strip()

        for j in day.findAll("div", {"class": "tmi-daily"}):
            names.append(j.findAll("div", {"class": "tmi-name"})[0].text.strip())
            prices.append(j.findAll("div", {"class": "tmi-price"})[0].text.strip())

        for i in range(len(names)):
            line = "- " + names[i] + " " + prices[i]
            menu += line + "\n"

        if len(menu) > 0:
            return "\n#### " + restaurant + ":\n\n" + menu
        else:
            return ""

    except socket.timeout:
        return "" + url + ": timeout :angry:\n"


def get_menus(config):
    menus = []
    for url in config["URLS"]:
        if "menicka.cz" in url:
            menus.append(fetch_menicka(url, config))
        if "zomato.com" in url:
            menus.append(fetch_zomato(url, config))
    return "\n".join(menus)


def get_title():
    locale.setlocale(locale.LC_ALL, "cs_CZ.UTF-8")
    date = datetime.strftime(datetime.now(), "%A %-d.%-m.")
    return "Obědy – " + date
