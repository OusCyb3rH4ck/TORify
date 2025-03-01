#!/usr/bin/env python3

from colorama import Fore, Style
from pwn import *
import os, sys, time, requests, signal, argparse, subprocess

def def_handler(sig, frame):
    print(f'\n\n{Fore.YELLOW}[!] Closing TOR Connection & Exiting...\n{Style.RESET_ALL}')
    os.system('sudo systemctl stop tor')
    os.system("sudo sed -i '/nameserver 127.0.0.1/d' /etc/resolv.conf")
    os.system('sudo iptables -F && sudo iptables -F -t nat')
    print(f'{Fore.RED}[!] Exited successfully!\n{Style.RESET_ALL}')
    sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

def showcountries():
    print("\n")
    p = log.progress(f'{Fore.LIGHTMAGENTA_EX}Retrieving countries list{Style.RESET_ALL}')
    p.status('3 seconds please...')
    response = requests.get('https://onionoo.torproject.org/details')
    if response.status_code == 200:
        data = response.json()
        countries = set()
        for relay in data['relays']:
            country_name = relay.get('country_name', 'Unknown')
            country_code = relay.get('country', '??').upper()
            countries.add(f"{country_name} [{country_code}]")
        p.success(f'{Fore.GREEN}Listing available countries...{Style.RESET_ALL}')
        time.sleep(3)
        print("\n")
        for country in sorted(countries):
            print(country)
        print("\n")
    else:
        print(f'{Fore.RED}[!] Failed to retrieve country list. Status code: {response.status_code}{Style.RESET_ALL}')

def config_tor():
    check = os.path.exists('/etc/tor/torrc')
    if check == 0:
        os.system('sudo apt update && sudo apt install tor nyx -y')
    
    country = input(f'{Fore.BLUE}[?] Enter country codename (ES, FR, US, etc.) > {Style.RESET_ALL}')
    
    torrc_content = '''DNSPort 9053
TransPort 9040
AutomapHostsOnResolve 1

ExitNodes {country}
StrictNodes 1
'''

    torrc_content = torrc_content.replace('country', country)

    with open('/etc/tor/torrc', 'w') as torrc:
        torrc.write(torrc_content)

    interface = subprocess.check_output("ip route | awk '/default/ {print $5}'", shell=True).decode().strip()
    
    os.system(f'sudo iptables -t nat -A OUTPUT -o {interface} -p udp --dport 53 -j REDIRECT --to-ports 9053')
    os.system(f'sudo iptables -t nat -A OUTPUT -o {interface} -p tcp --dport 80 -j REDIRECT --to-ports 9040')
    os.system(f'sudo iptables -t nat -A OUTPUT -o {interface} -p tcp --dport 443 -j REDIRECT --to-ports 9040')
    os.system("sudo sed -i '1i nameserver 127.0.0.1' /etc/resolv.conf")
    os.system('sudo systemctl start tor')
    
    print(f'\n\n{Fore.GREEN}[+] Tor configured successfully!\n{Style.RESET_ALL}')
    print(f'{Fore.BLUE}[i] Your IP address and info:\n{Style.RESET_ALL}')
    time.sleep(1)
    r = requests.get('https://ipinfo.io/')
    print(r.text)

def change_ip_node():
    os.system('sudo systemctl restart tor')
    print(f'\n\n{Fore.GREEN}[+] IP address changed successfully!\n{Style.RESET_ALL}')
    print(f'{Fore.BLUE}[i] Your new IP address and info:\n{Style.RESET_ALL}')
    time.sleep(1)
    r = requests.get('https://ipinfo.io/')
    print(r.text)
    print(f'{Fore.LIGHTYELLOW_EX+Style.BRIGHT}\n[-] If the IP has not changed, please, {Fore.LIGHTRED_EX}run again{Fore.LIGHTYELLOW_EX} or try thoses instructions:{Style.RESET_ALL} https://github.com/OusCyb3rH4ck/TORify/blob/main/README.md#instructions-if-the-ip-does-not-change-with-the--c-parameter')

def disconnect_tor():
    os.system('sudo systemctl stop tor')
    os.system("sudo sed -i '/nameserver 127.0.0.1/d' /etc/resolv.conf")
    os.system('sudo iptables -F && sudo iptables -F -t nat')
    print(f'\n\n{Fore.YELLOW}[!] TOR connection closed successfully!\n{Style.RESET_ALL}')

if __name__ == '__main__':
    if os.getuid() != 0:
        print(f'{Fore.RED}\n\n[!] Please run as root!\n{Style.RESET_ALL}')
        sys.exit(1)
    
    parser = argparse.ArgumentParser(description='Use TOR like a VPN for your anonymity and privacy.')
    parser.add_argument('-sc','--show-countries', help='Show the list of countries available', action='store_true')
    parser.add_argument('-s', '--start', help='Start the TOR connexion', action='store_true')
    parser.add_argument('-c', '--change', help='Change the TOR Node and IP address', action='store_true')
    parser.add_argument('-d', '--disconnect', help='Close the TOR connexion', action='store_true')
    args = parser.parse_args()

    if args.show_countries:
        showcountries()
    elif args.start:
        config_tor()
    elif args.change:
        change_ip_node()
    elif args.disconnect:
        disconnect_tor()
    else:
        parser.print_help()
        sys.exit(1)
