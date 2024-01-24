## Description

This repository contains a Python Flask application that enables integration between AWS WAF (Web Application Firewall) and Slack. The application utilizes the slack's `Slash Command` feature to to interact with the application and uses `boto3` moudle to interact with AWS services (here WAF & Shields).

## Features

- Block IPs directly from Slack using a slash command. This eliminates the need to access the AWS WAF console manually.
 
- Easily view the list of blacklisted IPs within Slack.
- IPs can be blocked with an expiration time. For example, by using the slash command `/blockip 162.247.74.206/32 0 0 0 60` in your Slack channel, the IP `162.247.74.206` will be blocked for 60 seconds. Once the time expires, the IP will be automatically removed from AWS WAF.

## Slash Command Format: 
The slash command should be provided in the following format:
```
 `/blockip [IPv4inCIDR] [Days] [Hours] [Minutes] [Seconds]`
  /listblockedips 
```
eg: If you want to block an IP for a day.
- `/blockip 162.247.74.206/32 1 0 0 0 `

If you want to block an IP for 6 hours.
- `/blockip 162.247.74.206/32 0 6 0 0 `

## Prerequisites
Before using the application, ensure you have the following:

- AWS account with read and write access to AWS WAF. 
- AWS cli setup.
- Slack workspace with administrative access. 
- Need `Slack Token` and one `webhook url`.
- Python 3.x installed on your local machine.

## Initial setup
To set up and use the AWS WAF Slack Integration, follow these steps:

1. Clone this repository to your local machine using the following command:
```
git clone https://github.com/abhiunix/aws_waf_slack_integration.git & cd aws_waf_slack_integration & touch .env

```
2.  Install the required Python packages by running the following command:
```
pip3 install -r requirements.txt
```
3. Configure the AWS credentials on your local machine, either by configuring the AWS CLI or by setting the `aws_access_key_id` and `aws_secret_access_key` environment variables.

4. Create a Slack app and obtain the Slack API token(App-Level Tokens).
![](images/SlackToken.png)
5. Create a incoming webhooks url for your channel.
![](images/incomingWebhooks.png)

6. Now create a `.env` file (if not present already) Update it with your slack webhooks.
```
webhook_url=https://hooks.slack.com/services/abc/xyz
```
7. Now create a Slash Command from Slack api
![](images/SlashCommands.png)

8. Replace `your-server-ip` and set the request URL to the URL where your Flask application is running. You can use [ngrok](https://ngrok.com/) to expose your local development server to the Internet with minimal effort.
![](images/edit_command.png)

9. Start the Flask application by executing the following command:
```
python3 app.py
```
10. In your Slack, you have to goto the same channel for which you created the webhook and enter the command `/listblockedips` e.g:
```
 /listblockedips 
```
11. Now you will notice that you're getting some `json data` in your console, where you have run the app and in your slack channel you'll see `You are not authorized to perform this actions.`
Now from the data you obtained from the console, you're supposed to change the `user_name`, `team_domain`, and `channel_name` value in line number `32` and `54` (in app.py file)
```
if user_name == "replace_with_user_name__from_console" and replace_with_team_domain == "replace_with_team_domain_from_console" and channel_name == "replace_with_channel_name_from_console":
```

After all those steps, you're ready to go.

You can now use the defined slash commands in Slack to block and list IPs.

## Upcoming Features
- IPv6 Support: Support for blocking and managing IPv6 addresses in addition to IPv4.

## Contributing
Contributions to this repository are welcome! If you encounter any issues or have suggestions for improvements, please open an issue or submit a pull request.

