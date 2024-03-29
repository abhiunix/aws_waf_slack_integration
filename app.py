from flask import Flask, request, render_template
import autoRemoveBlacklistedIPs
import threading
import os
from dotenv import load_dotenv
import sendSlackMessage
import listBlackListedIPs, listBlackListedIPsv6

load_dotenv()   
webhook_url = os.getenv("webhook_url")
app = Flask(__name__)

@app.route("/")
def home():
    return "Java Server"
# def home():
#     return render_template_string(HTML_CODE)

@app.route("/blockip", methods=['POST'])
def blockip():
    data = request.form
    text = data.get('text')
    user_name = data.get('user_name')
    team_domain = data.get('team_domain')
    channel_name = data.get('channel_name')

    try:
        if user_name in ("YourUserName") and team_domain == "YourTeamDomain" and channel_name in ("YourChannelName", "abhi-internal"):
            parts = text.split(" ")
            ip = parts[0]
            if '/' not in ip:
                sendSlackMessage.sendToSlack(webhook_url, f"Wrong input format, {user_name}. Please use CIDR format to block the IPs.\n eg: For IPv4: 162.247.74.206/32 \n For IPv6: 2606:54c0:7680:d28::1d3:53/128")
                return "Wrong input format, please use CIDR format to block the IPs"
            days = int(parts[1])
            hours = int(parts[2])
            minutes = int(parts[3])
            seconds = int(parts[4])
            thread = threading.Thread(target=execute_auto_remove, args=(ip, days, hours, minutes, seconds))
            sendSlackMessage.sendToSlack(webhook_url, f"{user_name} has Blacklisted the IP {ip} for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds.")
            #print(f"{user_name} has Blacklisted the IP {ip} for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds.")
            thread.start()
            return ""
        else:
            sendSlackMessage.sendToSlack(webhook_url, f"({user_name}) is trying to attack this bot.")
            return "You are not authorized to perform this actions."
    except IndexError:
        sendSlackMessage.sendToSlack(webhook_url, f"Input is not in the proper format, please enter in this format: [IPv4inCIDR or IPv6inCIDR] [Days] [Hours] [Minutes] [Seconds]. eg: \nFormate for blocking IPv4 use /blockip 162.247.74.206/32 0 0 0 60\nFormate for blocking IPv6: /blockip 2606:54c0:7680:d28::1d3:53/128 0 0 0 60\nThis will block the given IP for 60 Seconds")
        return ""

@app.route("/listBlockedIPv4", methods=['GET', 'POST'])
def listBlockedIPv4():
    data = request.form
    #text = data.get('text')
    user_name = data.get('user_name')
    team_domain = data.get('team_domain')
    channel_name = data.get('channel_name')
    if user_name in ("YourUserName") and team_domain == "YourTeamDomain" and channel_name in ("YourChannelName", "abhi-internal"):
        listBlackListedIPs.main()
    else:
            sendSlackMessage.sendToSlack(webhook_url, f"({user_name}) is trying to attack this bot.")
            return "You are not authorized to perform this action."
    return ""    

@app.route("/listBlockedIPv6", methods=['GET', 'POST'])
def listBlockedIPv6():
    data = request.form
    #text = data.get('text')
    user_name = data.get('user_name')
    team_domain = data.get('team_domain')
    channel_name = data.get('channel_name')
    if user_name in ("YourUserName") and team_domain == "YourTeamDomain" and channel_name in ("YourChannelName", "abhi-internal"):
        listBlackListedIPsv6.main()
    else:
            sendSlackMessage.sendToSlack(webhook_url, f"({user_name}) is trying to attack this bot.")
            return "You are not authorized to perform this action."
    return ""  


def execute_auto_remove(ip, days, hours, minutes, seconds):
    autoRemoveBlacklistedIPs.autoAddRemoveIP(ip, days, hours, minutes, seconds)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8002)
