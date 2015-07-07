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

Edit `jidlobot.conf` and set `CHANNEL` to your channel ID – these can be found at `https://slack.com/api/channels.list?token=…`.

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

Example crontab entry (runs every day at 10:45):

```]
45 10 * * * /path/to/jidlobot.sh
```

Note: rtmbot has no utf8 support, but it's easy to enable it: https://github.com/slackhq/python-rtmbot/pull/9/


## TODO

 - support for multiple channels
 - more pubs
 - handle timeouts when source websites are not working
 
