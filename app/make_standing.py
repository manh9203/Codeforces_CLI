from tabulate import tabulate
from colorama import Fore

def get_standing(response, page):
    if response['status'] == 'FAILED':
        return Fore.RED + "!!! " + Fore.RESET + "Can\'t find such contest"
    response = response['result']

    contest = response['contest']
    problems = response['problems']

    rows = response['rows']
    start = max(0, 20 * (page - 1))
    end = min(len(rows) - 1, 20 * page - 1)
    if start > end:
        return "Invalid page"
    
    Table = []
    if contest['type'] == "CF":
        """
            Standing for CF contests 
        """
        head = ['Rank', 'Handle', 'Total', 'Hacks']
        for problem in problems:
            head.append(problem['index'] + '\n' + str(int(problem['points'])))
        Table.append(head)

        for i in range(start, end + 1):
            row = []
            row.append(rows[i]['rank'])

            participant = rows[i]['party']['members'][0]['handle']
            if rows[i]['party']['participantType'] == 'VIRTUAL':
                participant += "(#)"
            elif rows[i]['party']['participantType'] == 'OUT_OF_COMPETITION':
                participant += "*"
            row.append(participant)

            row.append(rows[i]['points'])

            hacks = ""
            if rows[i]["successfulHackCount"] != 0 or rows[i]["unsuccessfulHackCount"] != 0:
                hacks += str(rows[i]["successfulHackCount"]) +  " : " 
                if rows[i]["unsuccessfulHackCount"] > 0:
                    hacks += "-"
                hacks += str(rows[i]["unsuccessfulHackCount"])
            row.append(hacks)

            for prob in range(0, len(problems)):
                point = rows[i]['problemResults'][prob]['points']
                attemps = rows[i]['problemResults'][prob]['rejectedAttemptCount']
                res = ""
                if point > 0:
                    success_time = rows[i]['problemResults'][prob]['bestSubmissionTimeSeconds']
                    res += Fore.GREEN + str(int(point)) + Fore.RESET
                    if success_time < contest['durationSeconds']:
                        res += "\n" + str(int(success_time/3600)) + ":"
                        if int(((success_time) % 3600) / 60) < 10:
                            res += "0"
                        res += str(int(((success_time) % 3600) / 60))
                elif attemps > 0:
                    res += Fore.RED + "-" + str(attemps) + Fore.RESET
                row.append(res)
            
            Table.append(row)

    else:
        """
            Standing for ICPC contests
        """
        head = ['Rank', 'Handle', 'Solved', 'Penalty', 'Hacks']
        for problem in problems:
            head.append(problem['index'])
        Table.append(head)

        for i in range(start, end + 1):
            row = []
            row.append(rows[i]['rank'])

            participant = rows[i]['party']['members'][0]['handle']
            if rows[i]['party']['participantType'] == 'VIRTUAL':
                participant += "(#)"
            elif rows[i]['party']['participantType'] == 'OUT_OF_COMPETITION':
                participant += "*"
            row.append(participant)

            row.append(rows[i]['points'])
            row.append(rows[i]['penalty'])

            hacks = ""
            if rows[i]["successfulHackCount"] != 0 or rows[i]["unsuccessfulHackCount"] != 0:
                hacks += str(rows[i]["successfulHackCount"]) +  " : " 
                if rows[i]["unsuccessfulHackCount"] > 0:
                    hacks += "-"
                hacks += str(rows[i]["unsuccessfulHackCount"])
            row.append(hacks)

            for prob in range(0, len(problems)):
                point = rows[i]['problemResults'][prob]['points']
                attemps = rows[i]['problemResults'][prob]['rejectedAttemptCount']
                res = ""
                if point > 0:
                    success_time = rows[i]['problemResults'][prob]['bestSubmissionTimeSeconds']
                    res += Fore.GREEN + "+"
                    if attemps > 0:
                        res += str(attemps)
                    res += Fore.RESET
                    if success_time < contest['durationSeconds']:
                        res += "\n" + str(int(success_time/3600)) + ":"
                        if int(((success_time) % 3600) / 60) < 10:
                            res += "0"
                        res += str(int(((success_time) % 3600) / 60))
                elif attemps > 0:
                    res += Fore.RED + "-" + str(attemps) + Fore.RESET
                row.append(res)
            
            Table.append(row)

    return tabulate(Table, headers="firstrow", missingval="-", tablefmt="grid")