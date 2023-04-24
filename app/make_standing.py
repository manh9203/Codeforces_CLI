from tabulate import tabulate
from colorama import Fore
from app import helper

def get_standing(response):
    def get_party(party):
        res = ""
        if 'teamId' in party:
            res = party['teamName']
            for i in range(0, len(party['members'])):
                res += ": " if i == 0 else ', '
                res += party['members'][i]['handle']
        else:
            res = party['members'][0]['handle']

        if party['participantType'] == 'VIRTUAL':
            res += "(#)"
        elif party['participantType'] == 'OUT_OF_COMPETITION':
            res += "*"

        return res
    
    def get_hack(success, failed):
        hacks = ""
        if success != 0 or failed != 0:
            hacks += str(success) +  " : " 
            if failed > 0:
                hacks += "-"
            hacks += str(failed)
        return hacks

    def cf_standing(problems, rows):
        Table = []
        head = ['Rank', 'Handle', 'Total', 'Hacks']
        for problem in problems:
            head.append(problem['index'] + '\n' + str(int(problem['points'])))
        Table.append(head)

        for user in rows:
            row = []
            row.append(user['rank'])
            row.append(get_party(user['party']))
            row.append(user['points'])
            row.append(get_hack(user["successfulHackCount"], user["unsuccessfulHackCount"]))

            for prob in range(0, len(problems)):
                point = user['problemResults'][prob]['points']
                attemps = user['problemResults'][prob]['rejectedAttemptCount']
                res = ""
                if point > 0:
                    success_time = user['problemResults'][prob]['bestSubmissionTimeSeconds']
                    res += Fore.GREEN + str(int(point)) + Fore.RESET
                    if success_time < contest['durationSeconds']:
                        res += "\n" + helper.get_contest_time(success_time)
                elif attemps > 0:
                    res += Fore.RED + "-" + str(attemps) + Fore.RESET
                row.append(res)
            Table.append(row)
        return tabulate(Table, headers="firstrow", missingval="-", tablefmt="grid")
    
    def icpc_standing(problems, rows):
        Table = []
        head = ['Rank', 'Handle', 'Solved', 'Penalty', 'Hacks']
        for problem in problems:
            head.append(problem['index'])
        Table.append(head)

        for user in rows:
            row = []
            row.append(user['rank'])

            row.append(get_party(user['party']))
            row.append(user['points'])
            row.append(user['penalty'])
            row.append(get_hack(user["successfulHackCount"], user["unsuccessfulHackCount"]))

            for prob in range(0, len(problems)):
                point = user['problemResults'][prob]['points']
                attemps = user['problemResults'][prob]['rejectedAttemptCount']
                res = ""
                if point > 0:
                    success_time = user['problemResults'][prob]['bestSubmissionTimeSeconds']
                    res += Fore.GREEN + "+"
                    if attemps > 0:
                        res += str(attemps)
                    res += Fore.RESET
                    if success_time < contest['durationSeconds']:
                        res += "\n" + helper.get_contest_time(success_time)
                elif attemps > 0:
                    res += Fore.RED + "-" + str(attemps) + Fore.RESET
                row.append(res)

            Table.append(row)
        return tabulate(Table, headers="firstrow", missingval="-", tablefmt="grid")

    if response['status'] == 'FAILED':
        return Fore.RED + "!!! " + Fore.RESET + "Can\'t find such contest"
    
    response = response['result']
    contest = response['contest']
    problems = response['problems']

    rows = response['rows']
    
    if contest['type'] == "CF":
        return cf_standing(problems, rows)
    else:
        return icpc_standing(problems, rows)
        