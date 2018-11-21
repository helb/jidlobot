# 🍔🥓 jidlobot 🍕🍄

> get lunch menus sent to your e-mail/groupchat

## Installation

### Using Ansible

[→ ansible-role/README.md](ansible-role/README.md)

### Manually

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

Copy `jidlobot.yml.example` to `jidlobot.yml` and set:

-   `HTTP_TIMEOUT` to the number of seconds you would want to wait for each URL
-   `URLS` – list of urls, supported sites are:
    - `menicka.cz`
    - `zomato.com` (they have some scraping protection in place, make sure to have `ZOMATO_UA` set in your config)
-   `BACKENDS` – where to send the message:
    -   `mail`
    -   `mattermost`
    -   `hipchat`
    -   `rocketchat`
    -   `console` (just prints the output).

If using `mail` backend:

-   `MAIL_FROM` – Sender e-mail address
-   `MAIL_TO` – List of recipients
-   `MAIL_SERVER` (default `localhost`) and `MAIL_PORT` (default `25`) – *MTA* (SMTP server) address
-   `MAIL_USER` (default same as `MAIL_FROM`) and `MAIL_PW` – SMTP server credentials (not used if `MAIL_PW` is not set)
-   `MAIL_STARTTLS` (default `True`) – Use *STARTTLS* connection method
-   If your local *MTA* works well, set `MAIL_FROM` and `MAIL_TO` only

If using `mattermost` backend:

-   `MATTERMOST_WEBHOOK` – URL for webhook, `https://mattermost.…/hooks/…`
-   `MATTERMOST_CHANNEL` – channel name
-   `MATTERMOST_USERNAME` – bot's username

If using `hipchat` backend:

-   `HIPCHAT_URL` – URL of your HipChat server, with trailing slash
-   `HIPCHAT_ROOM` – room ID
-   `HIPCHAT_TOKEN` – room notification token
-   `HIPCHAT_COLOR` – message background, valid values are  `yellow`, `green`, `red`, `purple`, `gray`, and `random`.

If using `rocketchat` backend:

-   `ROCKETCHAT_WEBHOOK` – URL for webhook, `https://rocketchat.…/hooks/…`
-   `ROCKETCHAT_CHANNEL` – channel name

More than one backend can be used at the same time, eg.:

```yaml
BACKENDS:
    - mattermost
    - mail
    - console
```

### Running

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
