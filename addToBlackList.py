import boto3
from dotenv import load_dotenv
import os
import ipaddress
import sendSlackMessage

load_dotenv()
webhook_url = os.getenv("webhook_url")

wafv2_client = boto3.client('wafv2')

def get_ip_set_id(ip_version):
    response = wafv2_client.list_ip_sets(Scope='REGIONAL')
    ip_set_name = 'Blacklist' if ip_version == 4 else 'Blacklist_IP_dynamic_ipv6'

    for ip_set in response['IPSets']:
        if ip_set['Name'] == ip_set_name:
            return ip_set['Id']
    return None

def expand_ipv6(ip):
    ip_obj = ipaddress.ip_network(ip, strict=False)
    return ip_obj.exploded

def block_this_ip(ip_block):
    try:
        ip_version = ipaddress.ip_network(ip_block, strict=False).version
    except ValueError as e:
        sendSlackMessage.sendToSlack(webhook_url, f"Invalid IP address: {ip_block}")
        print(f"Invalid IP address: {ip_block}")
        return

    ip_set_id = get_ip_set_id(ip_version)

    if ip_version == 6:
        ip_block = expand_ipv6(ip_block)

    if ip_set_id:
        get_ip_set_response = wafv2_client.get_ip_set(
            Name='Blacklist' if ip_version == 4 else 'Blacklist_IP_dynamic_ipv6',
            Id=ip_set_id,
            Scope='REGIONAL'
        )

        addresses = get_ip_set_response['IPSet']['Addresses']
        lock_token = get_ip_set_response['LockToken']

        addresses.append(ip_block)


        response = wafv2_client.update_ip_set(
            Name='Blacklist' if ip_version == 4 else 'Blacklist_IP_dynamic_ipv6',
            Id=ip_set_id,
            Scope='REGIONAL',
            Addresses=addresses,
            LockToken=lock_token
        )


        if response['ResponseMetadata']['HTTPStatusCode'] == 200:
            sendSlackMessage.sendToSlack(webhook_url, f"IP address '{ip_block}' added to the Blacklist IP set.")
            print(f"IP address '{ip_block}' added to the Blacklist IP set.")
        else:
            sendSlackMessage.sendToSlack(webhook_url, "Failed to update the Blacklisted IPs set.")
            print("Failed to update the Blacklist IP set.")
    else:
        sendSlackMessage.sendToSlack(webhook_url, f"IP set for IPv{ip_version} 'Blacklist' not found.")
        print(f"IP set for IPv{ip_version} 'Blacklist' not found.")

def main():
    #block_this_ip('35.80.0.1/32')  # Example IPv4
    #block_this_ip('2606:54c0:7680:d28::1d3:53/128')  # Example shortened IPv6
    # block_this_ip('2a02:4780::0040/128')  # Another example shortened IPv6
    return

if __name__ == "__main__":
    main()
