import random
from ping3 import ping
import socket

# Define IP address ranges
ipv4_ranges = [
    "162.159.192.",
    "162.159.193.",
    "162.159.195.",
    "188.114.96.",
    "188.114.97.",
    "188.114.98.",
    "188.114.99."
]

# Function to generate random IPv4 addresses
def generate_ipv4_list(count):
    ip_list = []
    while len(ip_list) < count:
        ip_range = random.choice(ipv4_ranges)
        ip = ip_range + str(random.randint(0, 255))
        if ip not in ip_list:  # Ensure IP uniqueness
            ip_list.append(ip)
    return ip_list

def is_valid_ipv4(ip):
    try:
        # Send ping to check if IP is valid and return ping time
        response = ping(ip, timeout=1)
        if response is not None:
            return int(response * 1000)  # Convert seconds to milliseconds and return as int
    except socket.error:
        return None
    return None

def main():
    iplist = 100  # Number of IP addresses to generate
    unique_ips = generate_ipv4_list(iplist)
    
    ip_ping_times = {}
    for ip in unique_ips:
        ping_time = is_valid_ipv4(ip)
        if ping_time is not None:
            ip_ping_times[ip] = ping_time
            print(f"{ip} with ping: {ping_time}ms")
    
    if ip_ping_times:
        # Sort IPs by ping time and get the 5 best
        best_ips = sorted(ip_ping_times, key=ip_ping_times.get)[:5]
        print("\nBest 5 IPv4 addresses with lowest ping times:")
        for ip in best_ips:
            print(f"{ip} - Ping: {ip_ping_times[ip]}ms")
    else:
        print("No valid IPv4 addresses found.")

if __name__ == "__main__":
    main()
