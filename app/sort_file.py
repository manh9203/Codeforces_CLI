import os
import requests
import shutil

#move to the directory
os.chdir(os.path.join('/Users/manh9203', 'Documents', 'Testing'))

#API call to get problemset's data
response = requests.get("https://codeforces.com/api/problemset.problems")
problems = response.json()['result']['problems']

for filename in os.listdir('.'):
    if (len(filename) >= 5 and filename[:2] == "CF" and filename[len(filename) - 3:] == "cpp"):
        filename_chars = list(filename)
        ptr = 2

        contestId = ""
        while (ord(filename_chars[ptr]) >= 48 and ord(filename_chars[ptr]) <= 57):
            contestId += filename[ptr]
            ptr += 1
        contestId = int(contestId)

        index = ""
        while (filename_chars[ptr] != '.'):
            index += filename[ptr]
            ptr += 1

        for problem in problems:
            if (problem['contestId'] == contestId and problem['index'] == index):
                newDir = os.path.join('.', str(problem['rating']))
                if (os.path.exists(newDir) == False):
                    os.makedirs(newDir)
                shutil.move(os.path.join('.', filename), os.path.join(newDir))
                break