import boto3
import sendSlackMessage
from dotenv import load_dotenv
import os

load_dotenv()
webhook_url = os.getenv("webhook_url")

def save_blacklistedIPs():
    # Create a WAFv2 client
    wafv2_client = boto3.client('wafv2')

    # Retrieve the IP set with the name "Blacklist_IP_dynamic_ipv6"
    response = wafv2_client.list_ip_sets(Scope='REGIONAL')
    ip_set_id = None
    for ip_set in response['IPSets']:
        if ip_set['Name'] == 'Blacklist_IP_dynamic_ipv6':
            ip_set_id = ip_set['Id']
            break

    if ip_set_id:
        response = wafv2_client.get_ip_set(
            Name='Blacklist_IP_dynamic_ipv6',
            Id=ip_set_id,
            Scope='REGIONAL'  # Set the scope to 'REGIONAL' for regional IP sets or 'CLOUDFRONT' for CloudFront IP sets
        )
        
        # Process the response
        if 'IPSet' in response:
            ip_set = response['IPSet']
            ip_set_id = ip_set['Id']
            addresses = ip_set['Addresses']
            print(f"IP Set ID: {ip_set_id}")
            print("IP Addresses:")
            with open('blacklistedIPv6.txt', 'w') as file:
                for address in addresses:
                    print(address)
                    file.write(address + '\n')
            print("IP addresses saved to 'blacklistedIPv6.txt' file.")
        else:
            print("Failed to retrieve IP set 'Blacklist_IP_dynamic_ipv6'.")
    else:
        print("IP set 'Blacklist_IP_dynamic_ipv6' not found.")

def count_lines():
    count = 0
    with open('blacklistedIPv6.txt', 'r') as file:
        for line in file:
            count += 1
    return count

def main():
    save_blacklistedIPs()
    count = count_lines()
    print(f"Number of blacklistedIPv6 IPs are: {count}")
    with open('blacklistedIPv6.txt', 'r') as file:
        ip_list = file.readlines()
        ip_message = "\n".join(ip_list)
    sendSlackMessage.sendToSlack(webhook_url, ip_message)
    sendSlackMessage.sendToSlack(webhook_url, f"Number of blacklistedIPv6 are: {count}")
    return
    
if __name__ == "__main__":
    main()  


