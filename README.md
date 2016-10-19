Mattermost "bot" – get lunch menus sent into channel.

## Installation

Clone the repo and install dependencies:

```
$ git clone https://github.com/helb/jidlobot.git
$ cd jidlobot
```

Create virtual environment:

```
$ virtualenv -p `which python3` venv
$ source venv/bin/activate
```

Install dependencies:

```
$ pip install -r requirements.txt
```


Edit `jidlobot.conf` and set:

 - `MATTERMOST_KEY` – [Mattermost docs: Incoming Webhooks](https://docs.mattermost.com/developer/webhooks-incoming.html)
 - `HTTP_TIMEOUT` to the number of seconds you would want to wait for each URL
 - `URLS` – list of urls at menicka.cz

Run the bot:

```
$ ./jidlobot.py
```

Create a cron job if everything works.

Example script for running from cron:

```bash
#!/bin/bash
cd /path/to/jidlobot
source venv/bin/activate
./jidlobot.py
```

Example crontab entry (runs Monday to Friday at 10:58):

```
58 10 * * 1-5 /path/to/jidlobot.sh
```
