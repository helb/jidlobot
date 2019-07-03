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
        restaurant = html.select(".profile .line1 h1")[0].text

        for line in day.select("li"):
            name = line.select(".polozka")
            if len(name) > 0:
                names.append(name[0].text)
                prices.append(name[0].next_sibling.next_sibling.text)

        for i in range(len(names)):
            line = "- " + names[i] + " " + prices[i]
            menu += line + "\n"

        if len(menu) > 0:
            return "\n#### " + restaurant + ":\n\n" + menu
        else:
            return ""

    except socket.timeout:
        return "" + url + ": timeout :angry:\n"

    except Exception:
        return "" + url + ": something went wrong :dizzy_face:\n"
