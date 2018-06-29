from bs4 import BeautifulSoup
import requests
import socket


def fetch(url, config):
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
