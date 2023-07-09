import boto3
from dotenv import load_dotenv
import os
import sendSlackMessage

load_dotenv()
webhook_url = os.getenv("webhook_url")

wafv2_client = boto3.client('wafv2')

response = wafv2_client.list_ip_sets(Scope='REGIONAL')

ip_set_id = None
for ip_set in response['IPSets']:
    if ip_set['Name'] == 'Blacklist':
        ip_set_id = ip_set['Id']
        break

def block_this_ip(ip_block):
    if ip_set_id:
        ip_address = ip_block

        get_ip_set_response = wafv2_client.get_ip_set(
            Name='Blacklist',
            Id=ip_set_id,
            Scope='REGIONAL'
        )

        addresses = get_ip_set_response['IPSet']['Addresses']
        lock_token = get_ip_set_response['LockToken']

        addresses.append(ip_address)

        response = wafv2_client.update_ip_set(
            Name='Blacklist',
            Id=ip_set_id,
            Scope='REGIONAL',
            Addresses=addresses,
            LockToken=lock_token
        )

        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            sendSlackMessage.sendToSlack(webhook_url, f"IP address '{ip_address}' added to the Blacklist IP set.")
            print(f"IP address '{ip_address}' added to the Blacklist IP set.")
        else:
            sendSlackMessage.sendToSlack(webhook_url, "Failed to update the Blacklisted IPs set.")
            print("Failed to update the Blacklist IP set.")
    else:
        sendSlackMessage.sendToSlack(webhook_url, "IP set 'Blacklist' not found.")
        print("IP set 'Blacklist' not found.")

def main():
    return

if __name__ == "__main__":
    main()