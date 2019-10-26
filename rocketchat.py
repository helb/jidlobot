import json
import re
import requests


def send_rocketchat(body, subject, config):
    body_rocket = re.sub(r'^#### (.*)$', r'*\1*', body, flags=re.MULTILINE).replace('\n\n', '\n')
    message = "*" + subject + "*\n@all\n" + body_rocket
    payload = json.dumps({
        "channel": config["ROCKETCHAT_CHANNEL"],
        "text": message
    })

    requests.post(config["ROCKETCHAT_WEBHOOK"], data=payload, timeout=config["HTTP_TIMEOUT"])
