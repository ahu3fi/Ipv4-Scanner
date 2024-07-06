import random
import socket
import json
import os

try:
    from ping3 import ping
except:
    print("Please Install 'ping3' module...")
    input()

def load_settings():
    settings = {
        "number_of_ip_scans": 100,
        "show_best_ipv4_count": 5,
    }
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as file:
            settings = json.load(file)
    return settings

def save_settings(settings):
    with open('settings.json', 'w') as file:
        json.dump(settings, file, indent=4)

def main():
    global settings
    settings = load_settings()
    show_main_menu(settings)

def show_main_menu(settings):
    clear()
    print("[1] Scan IPv4")
    print("[2] Settings")
    print("[3] Github (ahu3fi)")
    print("[4] Exit")

    option = input("Select an option: ")
    if option == '1':
        clear()
        generate_ipv4(settings)
    elif option == '2':
        handle_settings(settings)
    elif option == '3':
        open_github()
    elif option == '4':
        exit()
    else:
        input("Invalid option! Press Enter to try again...")
        show_main_menu(settings)

def handle_settings(settings):
    clear()
    print("[1] Number of Ip Scans =", settings['number_of_ip_scans'])
    print("[2] Show Best IPv4 by ping =", settings['show_best_ipv4_count'])
    print("[3] Back")

    option = input("Select an option: ")
    if option == '1':
        change_number_of_ip_scans()
    elif option == '2':
        change_show_best_ipv4_count()
    elif option == '3':
        show_main_menu(settings)
        
    else:
        input("Invalid option! Press Enter to try again...")
        handle_settings(settings)

def change_number_of_ip_scans():
    clear()
    print("Enter the number of IP scans: ")
    while True:
        try:
            num_scans = int(input("Number of IP scans: ").strip())
            settings['number_of_ip_scans'] = num_scans
            save_settings(settings)
            break
        except ValueError:
            input("Invalid input! Please enter a number. Press Enter to try again...")
            break
    handle_settings(settings)

def change_show_best_ipv4_count():
    clear()
    print("Enter the number of best IPv4 to show:")
    while True:
        try:
            count = int(input("Number of best IPv4 to show: ").strip())
            if 1 <= count <= settings['number_of_ip_scans']:
                settings['show_best_ipv4_count'] = count
                save_settings(settings)
                break
            else:
                input(f"Number out of range! Please enter a number between 1 and {settings['number_of_ip_scans']}. Press Enter to try again...")
                continue
        except ValueError:
            input("Invalid input! Please enter a number. Press Enter to try again...")
            break
    handle_settings(settings)
    
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def open_github():
    import webbrowser
    webbrowser.open_new_tab('https://github.com/ahu3fi')
    show_main_menu(settings)

def generate_ipv4_list(count):
    ipv4_ranges = [
        "162.159.192.",
        "162.159.193.",
        "162.159.195.",
        "188.114.96.",
        "188.114.97.",
        "188.114.98.",
        "188.114.99."
    ]
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

def generate_ipv4(settings):
    iplist = settings['number_of_ip_scans']
    unique_ips = generate_ipv4_list(iplist)
    
    ip_ping_times = {}
    for ip in unique_ips:
        ping_time = is_valid_ipv4(ip)
        if ping_time is not None:
            ip_ping_times[ip] = ping_time
            print(f"{ip} with ping: {ping_time}ms")
    
    if ip_ping_times:
        clear()
        best_ips = sorted(ip_ping_times, key=ip_ping_times.get)[:settings['show_best_ipv4_count']]
        print(f"\nBest {settings['show_best_ipv4_count']} IPv4 addresses with lowest ping times:")
        with open('Ips.txt', 'w') as file:
            for ip in best_ips:
                print(f"{ip} - Ping: {ip_ping_times[ip]}ms")    
                file.write(f"{ip}\n")
            file.close()
        os.system("start Ips.txt")
    else:
        print("No valid IPv4 addresses found.")

    input("Press Enter ... ")
    show_main_menu(settings)

if __name__ == "__main__":
    main()
