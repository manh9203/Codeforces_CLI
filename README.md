# Codeforces CLI

## Introduction

Codeforce CLI provides a command line interface to see information from [Codeforces](https://codeforces.com/) and fast-submit source code through the terminal.


## Install

Run 
```
git clone https://github.com/manh9203/Codeforces_CLI.git
cd Codeforces_CLI
pip install .
```

Then go to the "app" directory in the package's location, or run:
```
cd $(pip3 show Codeforces_CLI | sed -n '8p' | cut -b 11-)/app
```

Next, create a .env file like the following:
```
CF_KEY=<your client key>
CF_SECRET=<your client secret>
CF_HANDLE=<your codeforces handle>
CF_PASSWORD=<your codeforces password>
```
Get your key and secret from (https://codeforces.com/settings/api), handle and password are from your Codeforces account.


## Usage 

```
cf + [command]
```

Supported command:

```
  contests    Show list of contest

  dashboard   Show contest's dashboard

  standing    Show standing

  submission  Show user's submission

  submit      Submit a problem

  user        Show user's info

  verdict     Show the most recent submission
```
​Run ```cf --help``` to see the help menu

## Contribution
Please open an issue if you find any bugs, or have any idea for a feature. Feel free to submit an issue with your feedback!
