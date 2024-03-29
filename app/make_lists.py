from tabulate import tabulate
from colorama import Back
from colorama import Fore
from app import helper
from app.api_call import handle
from app import jprint

"""
    Contest list
"""
def contest_list(response, page, gym):
    def cf_contest(response, start, end):
        past_contest = False
        Table = [["Contest Id", "Name", "Start", "Length"]]
        for i in range(start, end + 1):
            if (response[i]['startTimeSeconds'] < helper.get_real_time() and past_contest == False):
                Table.append(["Past Contests", "-----", "--", "--"])
                past_contest = True
            row = []
            row.append(response[i]['id'])
            row.append(response[i]['name'])
            row.append(helper.get_date_time(response[i]['startTimeSeconds']))
            row.append(helper.get_contest_time(response[i]['durationSeconds']))
            Table.append(row)
        return tabulate(Table, headers="firstrow", tablefmt="grid")
    
    def gym_contest(response, start, end):
        Table = [["Contest Id", "Name", "Start", "Length", "Type"]]
        for i in range(start, end + 1):
            row = []
            row.append(response[i]['id'])
            row.append(response[i]['name'])
            if 'startTimeSeconds' in response[i]:
                row.append(helper.get_date_time(response[i]['startTimeSeconds']))
            else:
                row.append('--')
            row.append(helper.get_contest_time(response[i]['durationSeconds']))
            Table.append(row)
        return tabulate(Table, headers="firstrow", tablefmt="grid")

    response = response['result']

    start = max(0, 15 * (page - 1))
    end = min(len(response) - 1, 15 * page - 1)
    if start > end:
        return "Invalid page"
    
    if gym:
        return gym_contest(response, start, end)
    else:
        return cf_contest(response, start, end)


"""
    Submission list
"""
def sub_list(response, num):
    if response['status'] == 'FAILED':
        return Fore.RED + "!!! " + Fore.RESET + "Can\'t find such user"
    response = response['result']

    Table = [["Time", "Problem", "Lang", "Verdict", "Time", "Memory"]]
    for i in range(0, min(len(response), num)):
        row = []
        row.append(helper.get_date_time(response[i]['creationTimeSeconds']))
        row.append(str(response[i]['problem']['contestId']) + response[i]['problem']['index'])
        row.append(response[i]['programmingLanguage'])

        verdict = response[i]['verdict']
        if verdict == 'OK':
            row.append(Fore.GREEN + "Accepted" + Fore.RESET)
        elif verdict == 'TESTING':
            row.append("Testing on test " + response[i]['passedTestCount'])
        else:
            s = ""
            pre = ""
            for ch in verdict:
                if pre == "" or pre == "_":
                    s += ch
                pre = ch
            row.append(Fore.RED + s + Fore.RESET + " on test " + Fore.BLUE + str(response[i]['passedTestCount'] + 1) + Fore.RESET)

        row.append(str(response[i]['timeConsumedMillis']) + " ms")
        row.append(str(response[i]['memoryConsumedBytes'] / 1000) + " KB")

        Table.append(row)

    return tabulate(Table, headers="firstrow", missingval="-", tablefmt="grid")


"""
    Get dashboard
"""
def db(response):
    if response['status'] == 'FAILED':
        return Fore.RED + "!!! " + Fore.RESET + "Can\'t find such contest"
    response = response['result']

    contest = response['contest']
    problems = response['problems']
    rows = response['rows']

    Table = [['Problem', 'Name', 'Solved']]
    for i in range(0, len(problems)):
        problem = []
        index = str(problems[i]['index'])
        name = problems[i]['name']
        
        cnt, solved, attemps = 0, 0, 0
        for row in rows:
            if row['problemResults'][i]['points'] > 0:
                cnt += 1
                if row['party']['members'][0]['handle'] == handle:
                    solved = 1
            if row['party']['members'][0]['handle'] == handle:
                attemps = row['problemResults'][i]['rejectedAttemptCount'] + row['problemResults'][i]['points']

        if attemps == 0:
            problem = [index, name, cnt]
        else:
            if solved == 1:
                problem = [Back.GREEN + index + Back.RESET, name, cnt]
            else:
                problem = [Back.RED + index + Back.RESET, name, cnt]

        Table.append(problem)

    return tabulate(Table, headers="firstrow", missingval="-", tablefmt="grid")