import os
import time
import pyuac
import re
import subprocess


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


DEFAULT_TEXT_HOST_FILE = """# Copyright (c) 1993-2006 Microsoft Corp. # # This is a sample HOSTS file used by Microsoft TCP/IP for Windows. 
# 
# This file contains the mappings of IP addresses to host names. Each 
# entry should be kept on an individual line. The IP address should 
# be placed in the first column followed by the corresponding host name. 
# The IP address and the host name should be separated by at least one
# space. 
# 
# Additionally, comments (such as these) may be inserted on individual 
# lines or following the machine name denoted by a '#' symbol. 
# 
# For example: 
# 
# 102.54.94.97 rhino.acme.com 
# source server 
# 38.25.63.10 x.acme.com 
# x client host 
# localhost name resolution is handle within DNS itself. 
# 127.0.0.1 localhost 
# ::1 localhost
"""

HOST_PATH = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
IP_ADDRESS = '127.0.0.1'


def take_privilegies():
    """Restart the script with privilegies"""
    if not pyuac.isUserAdmin():
        pyuac.runAsAdmin()
        quit()


def gotomain():
    """Bring back the user to main"""
    print('backing to main...')
    time.sleep(0.5)
    main()


def cls():
    """Clean the console"""
    os.system('cls' if os.name == 'nt' else 'clear')


def get_blocked_urls():
    blocked_urls = []
    with open(HOST_PATH, 'r+') as hf:
        file_lines = hf.readlines()
        for line in file_lines:
            if line.strip() != '' and line[0][0] != '#':
                blocked_urls.append(line[10:].strip())
    return blocked_urls


def display_blocked_urls(enum=False):
    blocked_urls = get_blocked_urls()
    if not len(blocked_urls):
        print("There is no blocked URL")
    for i, url in enumerate(blocked_urls):
        if enum:
            print(f'{i+1} -> {url}')
        else:
            print('-> ' + url)
    print('\n')


def block_url(url):

    # for cleaning the dns cache in the OS
    os.system('ipconfig /flushdns')

    with open(HOST_PATH, 'r+') as hf:
        file_content = hf.read()
        if url not in file_content:
            hf.write("\n"+IP_ADDRESS + ' ' + url)


def unlock_url(url_to_remove):
    blocked_urls = get_blocked_urls()
    unlock_all_urls()
    with open(HOST_PATH, 'a') as hf:
        line_to_add = ''
        for url in blocked_urls:
            if url == url_to_remove:
                continue
            else:
                line_to_add = line_to_add + '\n' + IP_ADDRESS + ' ' + url
        hf.write(line_to_add)


def unlock_all_urls():
    with open(HOST_PATH, 'w') as hf:
        hf.write(DEFAULT_TEXT_HOST_FILE)


def add_a_url():
    cls()
    url_pattern = "((http|https)\\:\\/\\/)?[a-zA-Z0-9\\.\\/\\?\\:@\\-_=#]+\\.([a-zA-Z]){2,6}([a-zA-Z0-9\\.\\&\\/\\?\\:@\\-_=#])*"
    print(f"{bcolors.WARNING}///////////////////////////////////////////// BLOCK A URL ////////////////////////////////////////////////{bcolors.ENDC}")
    blocked_urls = get_blocked_urls()
    answer = str(input('Write the url to block (or B to return to main): '))
    if answer.upper() == 'B':
        gotomain()

    url_to_add = answer.lower()
    if not re.match(url_pattern, url_to_add):
        print('Invalid selection')
        time.sleep(0.5)
        add_a_url()
    if 'http://' in url_to_add:
        url_to_add = url_to_add.replace('http://', '')
    elif 'https://' in url_to_add:
        url_to_add = url_to_add.replace('https://', '')

    if url_to_add in blocked_urls:
        print('ALREADY BLOCKED')
    else:
        block_url(url_to_add)
        print(f'{url_to_add} --> BLOCKED')

    gotomain()


def remove_a_url():
    cls()
    print(f"{bcolors.WARNING}///////////////////////////////////////////// UNLOCK A URL ////////////////////////////////////////////////{bcolors.ENDC}")
    blocked_urls = get_blocked_urls()

    display_blocked_urls(enum=True)

    answer = input('Write the number to unlock (or B to return to main): ')
    if answer.upper() == 'B':
        gotomain()

    choiche = -1

    try:
        choiche = int(answer)-1
    except:
        print('Invalid selection')

    if choiche == -1:
        time.sleep(0.5)
        remove_a_url()

    if 0 <= choiche < len(blocked_urls):
        url_to_remove = blocked_urls[choiche]
        unlock_url(url_to_remove)
        print(f'{url_to_remove} --> UNLOCKED')
    else:
        print('Inexisting selection')
        time.sleep(0.5)
        remove_a_url()

    gotomain()


def remove_all_urls():
    cls()
    print(f"{bcolors.WARNING}///////////////////////////////////////////// UNLOCK ALL URLS ////////////////////////////////////////////////{bcolors.ENDC}")
    choiche = input('Are you sure of unblock all the urls? [Y/N]: ')
    match choiche.upper():
        case 'Y':
            unlock_all_urls()
            print('ALL URLS REMOVED')
        case 'N':
            pass
        case _:
            print('Invalid selection')
            time.sleep(0.5)
            remove_all_urls()

    gotomain()


def main():

    cls()
    os.system('color')  # -> used for color the console

    print(f'{bcolors.WARNING}//////////////////////////////////////////////////////////////////////////////////////////////////////////{bcolors.ENDC}')
    print(f"{bcolors.WARNING}///////////////////////////////////////////// URL BLOCKER ////////////////////////////////////////////////{bcolors.ENDC}")
    print(f'{bcolors.WARNING}//////////////////////////////////////////////////////////////////////////////////////////////////////////{bcolors.ENDC}')

    print(f'{bcolors.UNDERLINE}\nBLOCKED URLS LIST:{bcolors.ENDC}')

    display_blocked_urls()

    print(f'{bcolors.HEADER}ACTIONS{bcolors.ENDC}')
    print(f'{bcolors.BOLD}1 - Block a URL{bcolors.ENDC}')
    print(f'{bcolors.BOLD}2 - Unlock a URL{bcolors.ENDC}')
    print(f'{bcolors.BOLD}3 - Unlock all the URLs\n{bcolors.ENDC}')
    print(f'{bcolors.WARNING}//////////////////////////////////////////////////////////////////////////////////////////////////////////{bcolors.ENDC}')

    user_choiche = input('Your choiche: ')

    try:
        user_choiche = int(user_choiche)
    except:
        print('The choiche must be a number!')
        time.sleep(0.5)
        main()

    match user_choiche:
        case 1:
            add_a_url()
        case 2:
            remove_a_url()
        case 3:
            remove_all_urls()
        case _:
            print('Inexisting selection')
            time.sleep(0.5)
            main()


if __name__ == "__main__":
    take_privilegies()
    main()
