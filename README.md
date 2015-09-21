Plugin for [python-rtmbot](https://github.com/slackhq/python-rtmbot) – get lunch menus sent into channel.

## Installation

Create environment:

```
$ virtualenv -p `which python2` jidlobot
$ cd jidlobot
$ source bin/activate
```

Install rtmbot:

```
$ git clone https://github.com/helb/python-rtmbot.git
$ cd python-rtmbot
$ pip install -r requirements.txt
```

Install plugin:

```
$ cd plugins
$ git clone https://github.com/helb/jidlobot.git
$ cd jidlobot
$ pip install -r requirements.txt
```

Edit `jidlobot.conf` and set:

 - `CHANNEL` to your channel ID – these can be found at `https://slack.com/api/channels.list?token=…`.
 - `HTTP_TIMEOUT` to the number of seconds you would want to wait for each URL
 - `URLS` – list of urls at menicka.cz
 
Configure rtmbot:

```
$ cd ../..
$ cp doc/example-config/rtmbot.conf .
```

Edit `rtmbot.conf` and set `SLACK_TOKEN`.

Run the bot:

```
$ ./rtmbot.py
```

Create a cron job if everything works.

Example script for running from cron:

```
#!/bin/bash
cd /path/to/virtualenv
source bin/activate
cd python-rtmbot
./rtmbot.py
```

Example crontab entry (runs Monday to Friday at 10:58):

```
58 10 * * 1-5 /path/to/jidlobot.sh
```

(Slack sends out e–mail notifications at :00/:15/:30/:45 mins, so it's handy to have the script run a minute or two before that)

*Note: rtmbot has no utf8 support, but it's easy to enable it: https://github.com/slackhq/python-rtmbot/pull/9/*


## TODO

 - support for multiple channels
