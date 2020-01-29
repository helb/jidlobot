import yaml
from fetch import get_menus, get_title
from mattermost import send_mattermost
from mail import send_mail
from console import send_console
from hipchat import send_hipchat
from rocketchat import send_rocketchat
from slack import send_slack

with open("jidlobot.yml", "r") as conf_file:
    config = yaml.safe_load(conf_file)

menus = get_menus(config)
title = get_title()

if "console" in config["BACKENDS"]:
    send_console(menus, title, config)
if "mattermost" in config["BACKENDS"]:
    send_mattermost(menus, title, config)
if "hipchat" in config["BACKENDS"]:
    send_hipchat(menus, title, config)
if "rocketchat" in config["BACKENDS"]:
    send_rocketchat(menus, title, config)
if "slack" in config["BACKENDS"]:
    send_slack(menus, title, config)
if "mail" in config["BACKENDS"]:
    send_mail(menus, title, config)
