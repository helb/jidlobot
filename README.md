> get lunch menus sent to your e-mail

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


Edit `jidlobot.conf` and set:

 - `HTTP_TIMEOUT` to the number of seconds you would want to wait for each URL
 - `URLS` – list of urls at menicka.cz
 - `MAIL_FROM`, `MAIL_PW`, `MAIL_SERVER`, `MAIL_PORT` – SMTP server credentials for sending e-mails
 - `MAIL_TO` – list of recipients

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
