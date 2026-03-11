# Scoper
A Python tool to retrieve bug bounty program scopes, both public and private, from your favorite platforms

# Description
Scoper is capable of retrieving both public and private programs for a user and parsing the scope on four platforms:
- HackerOne
- BugCrowd
- Intigriti
- YesWeHack

Tested on Python 3.13

# Getting Started

## Usage

`pip install -r requirements.txt`

```
usage: Scoper [-h] [-p {h1,bc,ywh,intig,all} [{h1,bc,ywh,intig,all} ...]]

A Python tool to retrieve bug bounty program scopes, both public and private, from your favorite platforms

options:
  -h, --help            show this help message and exit
  -p, --platforms {h1,bc,ywh,intig,all} [{h1,bc,ywh,intig,all} ...]
                        Select one or more platforms to retrieve program scopes from. Default: all
```
## Output
The script will create an output folder called `data` that contains the output from each platform in the format of `<PLATFORM>_domains.txt` and `<PLATFORM>_wildcards.txt`.
These files each contain the name of the program and the asset in the format of `contoso-bb: example.com`. This is to ensure that, if you run tools against the master lists of domains or wildcards and find something,
you can quickly refer back to the platform specific files and identify the program the website belongs to.

At the end of the run, it will compile the content of all domains and wildcards into two completed files; `domains_complete.txt` and `wildcards_complete.txt`

## The .env File
Before you begin, copy the .env.example file to .env and define the environment variables.

### _For HackerOne_
The HackerOne section uses their provided researcher API. Their API uses HTTP Basic authentication and expects your HackerOne username and API token. You can find more information on creating an API token here: [HackerOne: API Token](https://docs.hackerone.com/en/articles/8410331-api-token)

### _For BugCrowd_
As BugCrowd does not provide researchers with an API, this section uses a bit of HTML and JSON parsing. The `BUGCROWD_SESSION` variable value is the value of the `_bugcrowd_session` cookie when authenticated to the platform.

### _For Intigriti_
Intigriti keeps it simple and provides researchers with an API token to interact with the platform. More information on creating an API token can be found here [Intigriti Researcher API: Authentication](https://intigriti-researcher-api.readme.io/reference/authentication)

### _For YesWeHack_
YesWeHack uses an API, but you do not need to create an API token. the `YESWEHACK_AUTH_TOKEN` is the JWT `Bearer` token sent to the API when you authenticate to the platform.

# Considerations
The rules described above for parsing do not cover every conceivable format a program may use to describe their scope. For example, a program on a platform may list "All assets owned by Contoso" as a website scope. Accomodating these edge cases is a work in progress.
