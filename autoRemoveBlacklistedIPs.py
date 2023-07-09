import time
import addToBlackList
import removeIPFromBlackList

def autoAddRemoveIP(ip, days, hours, minutes, seconds):
    def execute_after_duration(ip, duration):
        days, hours, minutes, seconds = map(int, duration)
        total_seconds = ((days * 24 + hours) * 60 + minutes) * 60 + seconds

        print(f"Blacklisted {ip} for the {days} days {hours} hours {minutes} minutes and {seconds} seconds...")

        time.sleep(total_seconds)

        print(f"Removing {ip} from the blocklist.")
        removeIPFromBlackList.remove_this_ip(ip)

    addToBlackList.block_this_ip(ip)
    execute_after_duration(ip, (days, hours, minutes, seconds))

