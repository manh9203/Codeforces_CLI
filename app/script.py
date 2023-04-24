import click

from app import api_call
from app import user_info
from app import make_standing
from app import make_lists
from app import submit_problem

@click.group()
def cli():
    pass


"""
    Get user info
"""
@click.command(help='Show user\'s info')
@click.argument('handle')
def user(handle):
    response = api_call.API_call("user.info", {"handles": handle})
    click.echo(user_info.get_user(response))
cli.add_command(user)



"""
    Get standing
"""
@click.command(help='Show standing')
@click.argument('contest_id')
@click.argument('page', type=int, default=1)
@click.option('--friends', '-fr', is_flag=True, help="Get friends' standing")
@click.option('--unofficial', '-u', is_flag=True, help="Show unofficial standing")
def standing(contest_id, page, friends, unofficial):
    method = "contest.standings"
    params = {"contestId": contest_id}

    start = 20 * (page - 1) + 1
    count = "20"
    params["from"] = int(start)
    params["count"] = count

    if friends:
        temp = api_call.API_call("user.friends", {})["result"]
        handles = ""
        for friend in temp:
            handles += friend + ";"
        handles += api_call.handle
        params["handles"] = handles

    if unofficial:
        params["showUnofficial"] = "true"
    
    response = api_call.API_call(method, params)    
    click.echo(make_standing.get_standing(response))

cli.add_command(standing)



"""
    Get contest list
"""
@click.command(help="Show list of contest")
@click.argument('page', type=int, default=1)
@click.option('--gym', '-g', is_flag=True, help='Show gym contests')
def contests(page, gym):
    method = "contest.list"
    params = {}
    if gym:
        params["gym"] = "true"
    response = api_call.API_call(method, params)
    click.echo(make_lists.contest_list(response, page, gym))
cli.add_command(contests)


"""
    Get user's submission
"""
@click.command(help='Show user\'s submission')
@click.argument('handle', default=api_call.handle)
@click.argument('number_of_submissions', default=15)
def submission(handle, number_of_submissions):
    response = api_call.API_call("user.status", {"handle": handle})
    click.echo(make_lists.sub_list(response, number_of_submissions))
cli.add_command(submission)


"""
    Get verdict of recent submission
"""
@click.command(help='Show the most recent submission')
def verdict():
    response = api_call.API_call("user.status", {"handle": api_call.handle, "from": "1", "count": "1"})
    click.echo(make_lists.sub_list(response, 1))
cli.add_command(verdict)


"""
    Get contest's dashboard
"""
@click.command(help="Show contest's dashboard")
@click.argument('contest_id')
def dashboard(contest_id):
    response = api_call.API_call("contest.standings", {"contestId": contest_id})
    click.echo(make_lists.db(response))
cli.add_command(dashboard)



"""
    Submit code
"""
@click.command(help='Submit a problem')
@click.argument('problem_name')
@click.argument('file_name')
def submit(problem_name, file_name):
    chars_list = list(problem_name)
    ptr = 0
    contestId, index, lang = "", "", ""
    while ord(chars_list[ptr]) >= 48 and ord(chars_list[ptr]) <= 57:
        contestId += problem_name[ptr]
        ptr += 1
    while ptr < len(chars_list):
        index += problem_name[ptr]
        ptr += 1

    ptr = len(file_name) - 1
    while file_name[ptr] != ".":
        ptr -= 1
    for i in range(ptr + 1, len(file_name)):
        lang += file_name[i]
    
    click.echo(submit_problem.submit_problem(contestId, index, lang, file_name))
cli.add_command(submit)


if __name__ == '__main__':
    cli()