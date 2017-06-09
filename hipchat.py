import requests
import json
import mistune


def send_hipchat(body, subject, config):
    body = mistune.markdown(body).replace("<h4>", "<br><b>").replace("</h4>", "</b><br>")
    message = "<b>" + subject + "</b><br>" + body
    payload = json.dumps({
        "color": config["HIPCHAT_COLOR"],
        "from": "jidlobot",
        "message_format": "html",
        "message": message,
        "notify": True
    })

    requests.post(config["HIPCHAT_URL"] + "v2/room/" + str(config["HIPCHAT_ROOM"]) + "/notification",
                  data=payload,
                  timeout=config["HTTP_TIMEOUT"],
                  headers={
                    "Content-type": "application/json",
                    "Authorization": "Bearer " + config["HIPCHAT_TOKEN"]
                  })
