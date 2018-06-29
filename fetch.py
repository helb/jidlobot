import locale
from datetime import datetime
from menicka import fetch as fetch_menicka
from zomato import fetch as fetch_zomato


parsers = {
  "menicka.cz": fetch_menicka,
  "zomato.com": fetch_zomato
}


def get_menus(config):
    menus = []
    for url in config["URLS"]:
        for domain in parsers.keys():
            if domain in url:
                menus.append(parsers[domain](url, config))
    return "\n".join(menus)


def get_title():
    locale.setlocale(locale.LC_ALL, "cs_CZ.UTF-8")
    date = datetime.strftime(datetime.now(), "%A %-d.%-m.")
    return "Obědy – " + date
