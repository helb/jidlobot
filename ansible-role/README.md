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
| .rocketchat       | no       |              | Definition of Rocket Chat backend (parameters are `webhook` and `channel`) |
| .slack            | no       |              | Definition of Slack backend (the only parameter is `webhook` url) |

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


## Examples

Simple installation with `console` backend (for testing):

```yaml
jidlobot_admin_mail: 'admin@example.cz'
jidlobot_backend:
  console:

jidlobot_urls:
  - https://www.menicka.cz/...
```

Send daily menus in `Mattermost` message:

```yaml
jidlobot_admin_mail: 'admin@example.cz'
jidlobot_backend:
  mattermost:
    channel: 'lunch'
    username: 'jidlobot'
    webhook: 'https://mattermost.example.cz/hooks/s3cr3tUR1'

jidlobot_urls:
  - https://www.menicka.cz/...
```


Send Wednesday menus on 11:30 to e-mail recipients:

```yaml
jidlobot_admin_mail: 'admin@example.cz'
jidlobot_backend:
  mail:
    from: 'jidlobot@example.cz'
    to:
      - admin@example.cz
      - hungry@hippo.org
      - foo@bar.xyz

jidlobot_cron:
  hour: '11'
  minute: '30'
  weekday: '3'

jidlobot_urls:
  - https://www.menicka.cz/...
```
