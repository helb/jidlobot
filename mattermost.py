import requests
import json


def send_mattermost(body, subject, config):
    message = "@channel\n\n### " + subject + "\n\n" + body.replace(".", "\.")
    payload = json.dumps({
        "channel": config["MATTERMOST_CHANNEL"],
        "username": config["MATTERMOST_USERNAME"],
        "text": message
    })

    requests.post(config["MATTERMOST_WEBHOOK"], data=payload, timeout=config["HTTP_TIMEOUT"])
