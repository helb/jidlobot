# Role `jidlobot`

Install and configure [jidlobot](https://github.com/helb/jidlobot) on
debian-like system.

The role currently support only *mattermost* module.


## Variables

| Variable          | Required | Default      | Description |
| ----------------- | -------- | ------------ | ----------- |
| jidlobot_urls     | yes      |              | List of *menicka* URLs of desired restaurants (value of `URLS` config parameter) |
|                   |          |              |  |
| jidlobot_mattermost_webhook | yes |         | URL for Mattermost webhook (`MATTERMOST_WEBHOOK` parameter) |
| jidlobot_mattermost_channel | yes |         | Used Mattermost channel (`MATTERMOST_CHANNEL` parameter) |
| jidlobot_mattermost_username | yes |        | Used bot's username (`MATTERMOST_USERNAME` parameter) |
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
