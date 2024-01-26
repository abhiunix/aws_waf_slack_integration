import boto3
from dotenv import load_dotenv
import os
import sendSlackMessage

load_dotenv()
webhook_url = os.getenv("webhook_url")

# Create a WAFv2 client
wafv2_client = boto3.client('wafv2')

# Retrieve the IP set with the name "Blacklist"
response = wafv2_client.list_ip_sets(Scope='REGIONAL')

ip_set_id = None
for ip_set in response['IPSets']:
    if ip_set['Name'] == 'Blacklist':
        ip_set_id = ip_set['Id']
        break

def remove_this_ip(remove_ip):
    if ip_set_id:
        # Prompt the user to enter the IP address to remove
        ip_address = remove_ip

        # Get the current IP addresses in the IP set
        get_ip_set_response = wafv2_client.get_ip_set(
            Name='Blacklist',
            Id=ip_set_id,
            Scope='REGIONAL'
        )

        addresses = get_ip_set_response['IPSet']['Addresses']
        lock_token = get_ip_set_response['LockToken']

        # Check if the IP address exists in the IP set
        if ip_address in addresses:
            # Remove the IP address from the list
            addresses.remove(ip_address)

            # Update the IP set
            response = wafv2_client.update_ip_set(
                Name='Blacklist',
                Id=ip_set_id,
                Scope='REGIONAL',
                Addresses=addresses,
                LockToken=lock_token
            )

            # Process the response
            if response['ResponseMetadata']['HTTPStatusCode'] == 200:
                sendSlackMessage.sendToSlack(webhook_url, f"IP address '{ip_address}' removed from the Blacklist IP set.")
                print(f"IP address '{ip_address}' has been removed from the Blacklist IP set.")
            else:
                sendSlackMessage.sendToSlack(webhook_url, f"Failed to update the Blacklist IP set.")
                print("Failed to update the Blacklist IP set.")
        else:
            sendSlackMessage.sendToSlack(webhook_url, f"IP address '{ip_address}' is not found in the Blacklist IP set.")
            print(f"IP address '{ip_address}' is not found in the Blacklist IP set.")
    else:
        sendSlackMessage.sendToSlack(webhook_url, f"IP set 'Blacklist' not found.")
        print("IP set 'Blacklist' not found.")
        