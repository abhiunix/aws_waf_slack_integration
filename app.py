from flask import Flask, request, render_template
import autoRemoveBlacklistedIPs
import threading
import os
from dotenv import load_dotenv
import sendSlackMessage
import listBlackListedIPs

load_dotenv()   
webhook_url = os.getenv("webhook_url")
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")
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
        if (user_name == "YourUserName" and team_domain == "YourTeamDomain" and channel_name == "YourChannelName"):
            parts = text.split(" ")
            ip = parts[0]
            days = int(parts[1])
            hours = int(parts[2])
            minutes = int(parts[3])
            seconds = int(parts[4])

            thread = threading.Thread(target=execute_auto_remove, args=(ip, days, hours, minutes, seconds))
            thread.start()

            sendSlackMessage.sendToSlack(webhook_url, f"{user_name} has Blacklisted the IP {ip} for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds.")
            return f"IP {ip} has been blacklisted for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds."
        else:
            sendSlackMessage.sendToSlack(webhook_url, f"({user_name}) is trying to attack this bot.")
            return "You are not authorized to perform this action."
    except IndexError:
        sendSlackMessage.sendToSlack(webhook_url, f"Hey {user_name}, your input is not in the correct format, please enter in this format: [IPv4inCIDR] [Days] [Hours] [Minutes] [Seconds]. eg: /blockip 162.247.74.206/32 0 0 0 60")
        return "Input is not in the correct format."

@app.route("/listBlockedIPs", methods=['GET', 'POST'])
def listBlockedIPs():
    data = request.form
    text = data.get('text')
    user_name = data.get('user_name')
    team_domain = data.get('team_domain')
    channel_name = data.get('channel_name')
    try:
        if (user_name == "YourUserName" and team_domain == "YourTeamDomain" and channel_name == "YourChannelName"):
            result = listBlackListedIPs.main()  # This now returns a dictionary
            if result and result["ip_message"]:  # Check if the IP message is not empty
                response = f"<pre>{result['file_message']}\n{result['count_message']}\n\nBlocked IPs:\n{result['ip_message']}</pre>"
                return response
            else:
                return "No blocked IPs found."
        else:
            sendSlackMessage.sendToSlack(webhook_url, f"({user_name}) is trying to attack this bot.")
            return "You are not authorized to perform this action."    
            
    except IndexError:
        sendSlackMessage.sendToSlack(webhook_url, f"Hey {user_name}, your input is not in the correct format, please enter in this format: [IPv4inCIDR] [Days] [Hours] [Minutes] [Seconds]. eg: /blockip 162.247.74.206/32 0 0 0 60")
        return "Input is not in the correct format."        



def execute_auto_remove(ip, days, hours, minutes, seconds):
    autoRemoveBlacklistedIPs.autoAddRemoveIP(ip, days, hours, minutes, seconds)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8002)
