import json
import re
import requests


def send_slack(body, subject, config):
    body_slack = re.sub(r'^#### (.*)$', r'*\1*', body, flags=re.MULTILINE).replace('\n\n', '\n')
    message = "*" + subject + "*\n" + body_slack
    payload = json.dumps({
        "text": message
    })

    requests.post(config["SLACK_WEBHOOK"], data=payload, timeout=config["HTTP_TIMEOUT"])
