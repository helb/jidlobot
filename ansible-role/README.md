# Role `jidlobot`

Install and configure [jidlobot](https://github.com/helb/jidlobot) on
debian-like system.

The role currently support only *mattermost* module.


## Variables

| Variable          | Required | Default      | Description |
| ----------------- | -------- | ------------ | ----------- |
| jidlobot_urls     | yes      |              | List of *menicka* URLs of desired restaurants (value of `URLS` config parameter) |
|                   |          |              |  |
| jidlobot_install_path | no   | /opt/jidlobot | Directory where jidlobot would be installed |
|                   |          |              |  |
| jidlobot_admin_mail | no     |              | `MAILTO` recipients in cron job |
| jidlobot_cron     | no       |              | Dictionary with following parameters |
| .hour             | no       | *            | `hour` parameter for cron job |
| .minute           | no       | *            | `minute` parameter for cron job |
| .day              | no       | *            | `day` parameter for cron job |
| .month            | no       | *            | `month` parameter for cron job |
| .weekday          | no       | *            | `weekday` parameter for cron job |
|                   |          |              |  |
| jidlobot_backend  | yes      |              | Definition of jidlobot backends (see *jidlobot documentation* for details); dictionary with following parameters |
| .console          | no       |              | Definition of console backend |
| .mail             | no       |              | Definition of mail backend (parameters are `from`, `to`, `server`, `port`, `user`, `pw` and `starttls`) |
| .mattermost       | no       |              | Definition of Mattermost backend (parameters are `webhook`, `channel` and `username`) |
| .hipchat          | no       |              | Definition of Hipchat backend (parameters are `url`, `room`, `token` and `color`) |

Default `jidlobot_cron` variable is set to:
```
jidlobot_cron:
  hour: '10'
  minute: '58'
  weekday: '1-5'
```

If any of the parameters is not defined, it is omitted from module parameters.
See
[cron module documentation](https://docs.ansible.com/ansible/latest/cron_module.html#options)
for details.
