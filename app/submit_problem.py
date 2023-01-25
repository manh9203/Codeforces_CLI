import os
import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from robobrowser import RoboBrowser

from dotenv import load_dotenv
load_dotenv()

def submit_problem(contestId, index, lang, filename):
    browser = RoboBrowser(parser = "lxml")
    browser.open('https://codeforces.com/enter')

    login_form = browser.get_form(id="enterForm")
    login_form['handleOrEmail'] = os.getenv('CF_HANDLE')
    login_form['password'] = os.getenv('CF_PASSWORD')
    browser.submit_form(login_form)

    if browser.url == 'https://codeforces.com/enter':
        return "Wrong password"

    browser.open('https://codeforces.com/contest/' + contestId + '/submit')
    submit_form = browser.get_form(class_="submit-form")
    submit_form['submittedProblemIndex'] = index
    submit_form['sourceFile'] = filename

    # get lang code
    value = '61' # default c++
    if lang == "cpp":
        value = '61'
    elif lang == "c":
        value = '43'
    elif lang == "py":
        value = '70'
    elif lang == "java":
        value = '60'
    elif lang == "kt":
        value = '83'
    elif lang == "hs":
        value = '12'
    elif lang == "rs":
        value = '75'
    elif lang == "rb":
        value = '67'
    elif lang == "go":
        value = '32'
    elif lang == "js":
        value = '34'
    submit_form['programTypeId'] = value

    browser.submit_form(submit_form)
    if browser.url == 'https://codeforces.com/contest/' + contestId + '/my':
        return 'Submitted successfully'
    else:
        return 'You have submitted exactly the same code before'