> get lunch menus sent to your e-mail/channel

## Installation

Clone the repo:

```
$ git clone https://github.com/helb/jidlobot.git
$ cd jidlobot
```

Create a virtual environment:

```
$ virtualenv -p `which python3` .venv
$ source .venv/bin/activate
```

Install dependencies:

```
$ pip install -r requirements.txt
```


Edit `jidlobot.conf` (YAML format) and set:

-   `HTTP_TIMEOUT` to the number of seconds you would want to wait for each URL
-   `URLS` – list of urls at menicka.cz
-   `BACKENDS` – where to send the message, current choices are `mail`, `mattermost`, and `console` (which just prints the output).

If using `mail` backend:

-   `MAIL_FROM`, `MAIL_PW`, `MAIL_SERVER`, `MAIL_PORT` – SMTP server credentials for sending e-mails
-   `MAIL_TO` – list of recipients

If using `mattermost` backend:

-   `MATTERMOST_WEBHOOK` – URL for webhook, `https://mattermost.…/hooks/…`
-   `MATTERMOST_CHANNEL` – channel name
-   `MATTERMOST_USERNAME` – bot's username

More than one backend can be used at the same time, eg.:

```yaml
BACKENDS:
    - mattermost
    - mail
    - console
```

## Running

```
$ ./jidlobot.py
```

Create a cron job if everything works.

Example script for running from cron:

```bash
#!/bin/bash
set -e
cd /path/to/jidlobot
source .venv/bin/activate
python jidlobot.py
```

Example crontab entry (runs Monday to Friday at 10:58):

```
58  10  *  *  1-5  /path/to/jidlobot.sh
```
