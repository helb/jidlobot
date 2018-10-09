from bs4 import BeautifulSoup
import requests
import socket
import re


def fetch(url, config):
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

    except IndexError:
        # return empty string when there is no menu for today
        return ""

    except Exception:
        return "" + url + ": something went wrong :dizzy_face:\n"
