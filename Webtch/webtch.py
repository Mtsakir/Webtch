import requests,time
import os
import requests
import argparse
import signal
import json

parser = argparse.ArgumentParser(description="Arguments")
parser.add_argument("-w", "--wordlist", required=None, help="The wordlist")
parser.add_argument("-u", "--url", required=None, help="The website")
parser.add_argument("-d", action="store_true",help="Add this, if you want to use default wordlist (https://github.com/digination/dirbuster-ng/blob/master/wordlists/small.txt)")

args = parser.parse_args()

b = args.wordlist  # wordlist
a = args.url  # web or url or IP
r=0
subdirectory_len =0

message = "The website doesn't exist"
myobj = {'something': ':something'}
default_wordlist = '/usr/share/webtch/wordlist/directory-list-2.3-small.txt'
found_sites = []

def banner():
    print("""\033[91m █████   ███   █████          █████     ███████████          █████     
░░███   ░███  ░░███          ░░███     ░█░░░███░░░█         ░░███      
 ░███   ░███   ░███   ██████  ░███████ ░   ░███  ░   ██████  ░███████  
 ░███   ░███   ░███  ███░░███ ░███░░███    ░███     ███░░███ ░███░░███ 
 ░░███  █████  ███  ░███████  ░███ ░███    ░███    ░███ ░░░  ░███ ░███ 
  ░░░█████░█████░   ░███░░░   ░███ ░███    ░███    ░███  ███ ░███ ░███ 
    ░░███ ░░███     ░░██████  ████████     █████   ░░██████  ████ █████
     ░░░   ░░░       ░░░░░░  ░░░░░░░░     ░░░░░     ░░░░░░  ░░░░ ░░░░░ \033[0m
                     \033[95mWebsite Subdirectory Brute Forcer v1.0\033[0m    
                            \033[95mCreator:MTsakir\033[0m  
                        
                        
        \033[31m [!] DISCLAIMER [!] \033[0m
\033[31mThis tool is developed for educational purposes. 
You have your own responsibilities and you are liable to any damage or violation of laws by this tool.
The author is not responsible for any misuse of WebTch!\033[0m                
                    
                        
                        """)

def usage():
    print("""
\033[36mpython3 webtchh.py -u website -w wordlist 
    Tips:
        -w, --wordlist Enter the wordlist path
        -u, --url Enter the url or ip address of the website

        [!] In this version, some status codes are not supported [!]
        [!] The status code 403 shows website exists but it is not accesible [!]

        Additions:
            If you want to use the default wordlist, just type
                            python3 webtch.py -u website -d    
    
    
        \033[0m
    """)

#----------
def site_checker():
    try:
        print(f"Checking URL: {a}")
        x = requests.post(a, json=myobj, allow_redirects=False)
        if x.status_code in [200, 301, 302, 304, 307, 308, 403]:
            size_in_bytes = len(x.content)
            size_in_kb = size_in_bytes / 1024
            print(f"\033[32m[+] The website exists --- STATUS:{x.status_code} --- SIZE:{size_in_kb:.2f} KB [+] \033[0m")
            time.sleep(0.5)
            return True
        elif x.status_code == 404:
            size_in_bytes = len(x.content)
            size_in_kb = size_in_bytes / 1024
            print(f"\033[31m[x] The website doesn't exist --- STATUS:{x.status_code} [x]\033[0m")
            return False
        else:
            print(f"\033[33m[!] Unexpected status code: {x.status_code} [!]\033[0m")
            return False
    except requests.exceptions.ConnectionError:
        print(f"\033[31m[x] Failed to establish a new connection [x]\033[0m")
    except requests.exceptions.Timeout:
        print(f"\033[31m[x] Connection timed out [x]\033[0m")
    except requests.exceptions.RequestException as e:
        print(f"\033[31m[x] An error occurred: {e} [x]\033[0m")
    time.sleep(0.6)#----------
def brute_force(site, wordlist):
    print("\033[34m[!] The brute force has been started [!]\033[0m")
    time.sleep(0.8)

    with open(wordlist, "r") as f:
        wordlist_a = [line.strip() for line in f if line.strip()]

    global r
    global subdirectory_len 
    for subdirectory in wordlist_a:
        if not subdirectory.startswith('#'):

            subdirectory = subdirectory.strip()
            subdirectory_len = subdirectory_len + 1
            url = f"{site}/{subdirectory}"

            response = requests.get(url,allow_redirects=False)

            if response.status_code in [200,301,304,307,308,403]:
                size_in_bytes = len(response.content)
                size_in_kb = size_in_bytes / 1024
                print(f"\033[2K\r\033[92m[\u2713] WEBSITE FOUND -> {url} -- STATUS: {response.status_code} -- SIZE: {size_in_kb:.2f} KB\033[0m")
                r = r + 1
                found_sites.append(r)
            print(f"\033[2K\r ·[{r}/{subdirectory_len}] --- {(subdirectory_len/len(wordlist_a))*100:.2f}% --- {site}/\033[4m{subdirectory}\033[0m", end="", flush=True)
            #time.sleep(0.5)
    print("\033[2K", end="")
    print("\n")
    print("\033[34m                               +---------------------------------------------+\033[0m")
    print(
            f"                               \033[34m|\033[0m\033[35m[!] Number of scanned Subdirectories -> {subdirectory_len}\033[0m  \033[34m|\033[0m")
    print(
            f"                               \033[34m|\033[0m\033[92m[\u2713] Number of founded Subdirectories -> {r}\033[0m    \033[34m|\033[0m")
    print("                               \033[34m+---------------------------------------------+\033[0m")
    
    if not found_sites:
        print("\033[91mNO WEBSITES FOUND :( \033[0m ")
        exit(0)
    else:
        exit(0)

def brute_force_default_wordlist(site):
    print("\033[34m[!] The brute force has been started [!]\033[0m")
    time.sleep(0.8)

    with open(default_wordlist, "r") as f:
        wordlist_a = [line.strip() for line in f if line.strip()]

    global r
    global subdirectory_len 
    for subdirectory in wordlist_a:
        if not subdirectory.startswith('#'):

            subdirectory = subdirectory.strip()
        #--------------------------------------#
            subdirectory_len = subdirectory_len + 1
        #--------------------------------------#
            url = f"{site}/{subdirectory}"

            response = requests.get(url, allow_redirects=False)

            if response.status_code in [200,301,304,307,308,403]:

                size_in_bytes = len(response.content)
                size_in_kb = size_in_bytes / 1024
                print(f"\033[2K\r\033[92m[\u2713] WEBSITE FOUND -> {url} -- STATUS: {response.status_code} -- SIZE: {size_in_kb:.2f} KB\033[0m")
                r = r + 1
                found_sites.append(r)
            print(f"\033[2K\r ·[{r}/{subdirectory_len}] --- {(subdirectory_len/len(wordlist_a))*100:.2f}% --- {site}/\033[4m{subdirectory}\033[0m", end="", flush=True)
            #time.sleep(0.4)
    print("\033[2K", end="")
    print("\n")
    print("\033[34m                               +-------------------------------------------+\033[0m")
    print(
            f"                               \033[34m|\033[0m\033[35m[!] Number of scanned Subdirectories -> {subdirectory_len}\033[0m \033[34m|\033[0m")
    print(
            f"                               \033[34m|\033[0m\033[92m[\u2713] Number of founded Subdirectories -> {r}\033[0m  \033[34m|\033[0m")
    print("                               \033[34m+-------------------------------------------+\033[0m")
    
    if not found_sites:
        print("\033[91mNO WEBSITES FOUND :( \033[0m ")
    exit(0)
  
def wordlist_validator(wordlist):
    if os.path.isfile(wordlist):
        return True
    else:
        return False
##########################
# args.a = args.d        #
# args.b = args.wordlist #
# args.c = args.url      #     
##########################

banner()
usage()
#time.sleep(1.91)
def main(site,wordlist_other):
    global found_sites

    if args.d and args.wordlist and args.url:
        usage()

    elif not args.d and args.wordlist and args.url:
        print(f"\033[93mEntered Website -> {site}\033[0m")
        print(f"\033[93mWordlist -> {wordlist_other}\033[0m ")
        checker = os.path.abspath(wordlist_other)
        print(f"\033[93mFULL PATH -> {checker}\033[0m")
        if wordlist_validator(wordlist_other) == True:
            print("\033[32mWordlist is found [\u2713] \033[32m")
            if site_checker():
                print("",end="\n")
                print("\033[1m-----------------------------------------------------------------------------------\033[1m")
                print("",end="\n")
                brute_force(a, b)
            else:
                exit(0)
        else:
            print("\033[31m[X] No wordlist found [X] \033[0m")
            exit(0)

    elif args.d and not args.wordlist and args.url:
        print(f"\033[93mEntered Website -> {site}\033[0m")
        print(f"\033[93mWordlist -> {default_wordlist}\033[0m ")
        checker = os.path.abspath(default_wordlist)
        print(f"\033[93mFULL PATH -> {checker}\033[0m")
        if wordlist_validator(default_wordlist) == True:
            print("\033[32mWordlist is found [\u2713] \033[32m")
            time.sleep(0.81)
            if site_checker():
                print("",end="\n")
                print("\033[1m-----------------------------------------------------------------------------------\033[1m")
                print("",end="\n")
                brute_force_default_wordlist(a)
            else:
                exit(0)
        else:
            print("\033[31m[X] No wordlist found [X] \033[0m")
            exit(0)
    
    elif args.d and args.wordlist and args.url:
        print("The wordlist and default wordlist can not be exist at the same time!")
        usage()
    
    # a,b,d true
    elif args.d and args.wordlist and not args.url:
        print("The wordlist and default wordlist can not be exist at the same time and url or ip address is not entered")
        usage()

    # a,b true
    elif args.d and args.wordlist and not args.url:
        print("The wordlist and default wordlist can not be exist at the same time and url or ip address is not entered")
        usage()
  
    # a,c true
    elif args.d and not args.wordlist and args.url:
        print(f"\033[93mEntered Website -> {site}\033[0m")
        print(f"\033[93mWordlist -> {default_wordlist}\033[0m ")
        checker = os.path.abspath(default_wordlist)
        print(f"\033[93mFULL PATH -> {checker}\033[0m")
        if wordlist_validator(default_wordlist) == True:
            print("\033[32mWordlist is found [\u2713] \033[32m")
            time.sleep(0.81)
            if site_checker():
                print("",end="\n")
                brute_force_default_wordlist(a)
            else:
                exit(0)
        else:
            print("\033[31m[X] No wordlist found [X] \033[0m")
            exit(0)

    # a,d true
    elif args.d and not args.wordlist and not args.url:
        print("The url or ip address is not entered")
        usage()

    # b,c true
    elif not args.d and args.wordlist and args.url:
        print(f"\033[93mEntered Website -> {site}\033[0m")
        print(f"\033[93mWordlist -> {wordlist_other}\033[0m ")
        checker = os.path.abspath(wordlist_other)
        print(f"\033[93mFULL PATH -> {checker}\033[0m")
        if wordlist_validator(wordlist_other) == True:
            print("\033[32mWordlist is found [\u2713] \033[32m")
            time.sleep(0.81)
            if site_checker():
                print("",end="\n")
                brute_force(a, b)
            else:
                exit(0)
        else:
            print("\033[31m[X] No wordlist found [X] \033[0m")
            exit(0)
        
    # b,d true
    elif not args.d and args.wordlist and not args.url:
        print("The url or ip address is not entered")
        usage()


    #c,d true
    elif not args.d and not args.wordlist and args.url:
        print("The wordlist is not entered")
        usage()
    
    #a true
    elif args.d and not args.wordlist and not args.url:
        print("The url or ip address is not entered")
        usage()

    #b true
    elif not args.d and args.wordlist and not args.url:
        print("The url or ip address is not entered")
        usage()

    #c true
    elif not args.d and not args.wordlist and args.url:
        print("The url or ip address is not entered")
        usage()

    #d true
    elif not args.d and not args.wordlist and not args.url:
        usage()
    
    


##########################
# args.a = args.d        #
# args.b = args.wordlist #
# args.c = args.url      #     
##########################

def signal_handler(sig, frame):
    while True:
        print("\n")
        choice = input('Do you want to continue or quit? (c/q): ')
        if choice.lower() == 'c' or choice.lower() == 'C':
            print('Continuing...')
            break
        elif choice.lower() == 'q' or choice.lower() == 'Q':
            print("\n")
            print(f"\033[93mThe number of web pages found so far -> {len(found_sites)} \033[0m")
            print("\n")
            print('\033[91mQuitting...\033[0m')
            exit(0)

signal.signal(signal.SIGINT, signal_handler)


main(a,b)







