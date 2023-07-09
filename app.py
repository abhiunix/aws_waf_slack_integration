from flask import Flask, request
import autoRemoveBlacklistedIPs
import threading
#from flask_ngrok2 import run_with_ngrok
import os
from dotenv import load_dotenv
import sendSlackMessage
import listBlackListedIPs

load_dotenv()   
webhook_url = os.getenv("webhook_url")
app = Flask(__name__)
#run_with_ngrok(app)

@app.route("/")
def home():
    return "Unauthorized Access!!! <script>alert('Nothing here for you!')</script>"

def execute_auto_remove(ip, days, hours, minutes, seconds):
    autoRemoveBlacklistedIPs.autoAddRemoveIP(ip, days, hours, minutes, seconds)

@app.route("/listBlockedIPs", methods=['POST'])
def listBlockedIPs():
    data = request.form
    #text = data.get('text')
    user_name = data.get('user_name')
    team_domain= data.get('team_domain')
    channel_name= data.get('channel_name')
    print(data)
    #Check the user name, team_domain, and channel from the console and replace it with below names
    try:
        if user_name == "user_name__from_console" and team_domain == "team_domain_from_console" and channel_name == "channel_name_from_console":
            sendSlackMessage.sendToSlack(webhook_url, f"{user_name} has requested to see the blacklisted IPs")
            thread = threading.Thread(target=listBlackListedIPs.main())
            thread.start()
            return ""
        else:
            sendSlackMessage.sendToSlack(webhook_url, f"({user_name}) is trying to attack this bot.")
            return "You are not authorized to perform this actions."
    except IndexError:
        sendSlackMessage.sendToSlack(webhook_url, f"Input is not in the proper format, please enter in this format: /listBlockedIPs")
        return ""

@app.route("/blockip", methods=['POST'])
def blockip():
    data = request.form
    text = data.get('text')
    user_name = data.get('user_name')
    team_domain= data.get('team_domain')
    channel_name= data.get('channel_name')
    print(data)
    print(f" username {user_name} team-domain {team_domain} channel_name {channel_name}")
    try:
        if user_name == "user_name__from_console" and team_domain == "team_domain_from_console" and channel_name == "channel_name_from_console":
            parts = text.split(" ")
            ip = parts[0]
            days = parts[1]
            hours = parts[2]
            minutes = parts[3]
            seconds = parts[4]
            thread = threading.Thread(target=execute_auto_remove, args=(ip, days, hours, minutes, seconds))
            sendSlackMessage.sendToSlack(webhook_url, f"{user_name} has Blacklisted the IP {ip} for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds.")
            #print(f"{user_name} has Blacklisted the IP {ip} for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds.")
            thread.start()
            return ""
        else:
            sendSlackMessage.sendToSlack(webhook_url, f"({user_name}) is trying to attack this bot.")
            return "You are not authorized to perform this actions."
    except IndexError:
        sendSlackMessage.sendToSlack(webhook_url, f"Input is not in the proper format, please enter in this format: [IPv4inCIDR] [Days] [Hours] [Minutes] [Seconds]. eg: /blockip 162.247.74.206/32 0 0 0 60")
        return ""
        
if __name__ == "__main__":
    app.run(port=5002)

