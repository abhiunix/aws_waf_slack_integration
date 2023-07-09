import boto3
import sendSlackMessage
from dotenv import load_dotenv
import os

load_dotenv()
webhook_url = os.getenv("webhook_url")

def save_blacklistedIPs():
    wafv2_client = boto3.client('wafv2')

    response = wafv2_client.list_ip_sets(Scope='REGIONAL')
    ip_set_id = None
    for ip_set in response['IPSets']:
        if ip_set['Name'] == 'Blacklist':
            ip_set_id = ip_set['Id']
            break

    if ip_set_id:
        response = wafv2_client.get_ip_set(
            Name='Blacklist',
            Id=ip_set_id,
            Scope='REGIONAL' 
        )
        
        if 'IPSet' in response:
            ip_set = response['IPSet']
            ip_set_id = ip_set['Id']
            addresses = ip_set['Addresses']
            print(f"IP Set ID: {ip_set_id}")
            print("IP Addresses:")
            with open('blacklistedIPs.txt', 'w') as file:
                for address in addresses:
                    print(address)
                    file.write(address + '\n')
            print("IP addresses saved to 'blacklistedIPs.txt' file.")
        else:
            print("Failed to retrieve IP set 'Blacklist'.")
    else:
        print("IP set 'Blacklist' not found.")

def count_lines():
    count = 0
    with open('blacklistedIPs.txt', 'r') as file:
        for line in file:
            count += 1
    return count

def main():
    save_blacklistedIPs()
    count = count_lines()
    print(f"Number of blacklistedIPs IPs are: {count}")
    with open('blacklistedIPs.txt', 'r') as file:
        ip_list = file.readlines()
        ip_message = "\n".join(ip_list)
    sendSlackMessage.sendToSlack(webhook_url, ip_message)
    sendSlackMessage.sendToSlack(webhook_url, f"Number of blacklistedIPs IPs are: {count}")
    return

if __name__ == "__main__":
    main()  
