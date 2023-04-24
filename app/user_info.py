import time
from tabulate import tabulate
from colorama import Fore
from app import helper

"""
    Return user's info
"""
def get_user(response):
    if response['status'] == "FAILED":
        return Fore.RED + "!!! " + Fore.RESET + "Can\'t find such user"
    response = response['result'][0]

    color = ""
    if "rating" not in response:
        color = Fore.RESET
    else:
        color = helper.get_color(response['rating'])

    s1 = color + "##" + Fore.RESET + " User"
    s2 = ""
    name = response['handle']
    if "rating" in response and response['rating'] >= 3000:
        s2 += Fore.BLACK + name[0] + Fore.RESET + color + name[1:len(name)] + Fore.RESET
    else:
        s2 += color + name + Fore.RESET
    Table = [[s1, s2]]

    if "rating" in response:
        Table.append([color + "##" + Fore.RESET + " Rating", color + str(response['rating']) + Fore.RESET])
        Table.append([color + "##" + Fore.RESET + " Rank", color + response['rank'] + Fore.RESET])
        oldColor = helper.get_color(response['maxRating'])
        Table.append([color + "##" + Fore.RESET + " Max rating", oldColor + str(response['maxRating']) + Fore.RESET])
        Table.append([color + "##" + Fore.RESET + " Max rank", oldColor + response['maxRank'] + Fore.RESET])
    else:
        Table.append([color + "##" + Fore.RESET + " Rating", color + "Unrated" + Fore.RESET])

    if "country" in response:
        Table.append([color + "##" + Fore.RESET + " Country", response['country']])

    if "organization" in response:
        Table.append([color + "##" + Fore.RESET + " From", response['organization']])

    if abs(response['lastOnlineTimeSeconds'] - time.time()) > 1000:
        Table.append([color + "##" + Fore.RESET + " Status", Fore.WHITE + "Offline" + Fore.RESET])
    else:
        Table.append([color + "##" + Fore.RESET + " Status", Fore.GREEN + "Online" + Fore.RESET])

    return tabulate(Table)
