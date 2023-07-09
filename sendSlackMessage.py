from dotenv import load_dotenv
import os
import requests

load_dotenv()
webhook_url = os.getenv("webhook_url")

def sendToSlack(webhook_url, message):
    payload = {
        'text': message
    }
    response = requests.post(webhook_url, json=payload)
    if response.status_code != 200:
        print(f"Failed to send Slack notification. Error: {response.status_code} - {response.text}")

def main():
    with open('blacklistedIPs.txt', 'r') as file:
        ip_list = file.readlines()
        ip_message = "\n".join(ip_list)
    sendToSlack(webhook_url, ip_message)

if __name__ == "__main__":
    main()

#sendSlackMessage.sendToSlack(webhook_url, "Input is not in the proper format, please enter in this format: [IPv4inCIDR] [Days] [Hours] [Minutes] [Seconds]. eg: /blockip 162.247.74.206/32 0 0 0 60")
