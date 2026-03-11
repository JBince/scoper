#! python3

import requests
import os

"""
TODO: 
@ Add authorization checks to stop on failure
@ Add checks to ensure only unique lines are added to files
"""


class HackerOne:
    # File Path Constants
    DOMAINS_FILE = "data/h1_domains.txt"
    WILDCARDS_FILE = "data/h1_wildcards.txt"

    def __init__(self, username, api_token):
        # Ensure that, regardless of what programs we scope, it double checks the directory setup
        self.username = username
        self.api_token = api_token
        self.program_handles = []

    def get_programs(self):
        print("[+] Getting HackerOne Programs")
        n = 1
        while True:
            data = requests.get(
                "https://api.hackerone.com/v1/hackers/programs",
                auth=(self.username, self.api_token),
                params={"page[size]": 100, "page[number]": n},
            ).json()
            for i in range(100):
                try:
                    self.program_handles.append(data["data"][i]["attributes"]["handle"])
                except:
                    # Stops when it gets to the end of the list
                    print(
                        f"[+] Retrieved {len(self.program_handles)} programs from HackerOne"
                    )
                    return
            n += 1

    def get_and_write_program_scopes(self):
        # Open file handlers for later writing
        h1_domains_file = open(self.DOMAINS_FILE, "w")
        h1_wildcard_file = open(self.WILDCARDS_FILE, "w")

        # Iterate over programs
        for program in self.program_handles:
            n = 1
            while True:
                flag = False
                # Get all scopes from the program
                data = requests.get(
                    f"https://api.hackerone.com/v1/hackers/programs/{program}/structured_scopes",
                    auth=(self.username, self.api_token),
                    params={"page[size]": 100, "page[number]": n},
                ).json()
                # Parse each scope
                for n in range(100):
                    try:
                        # Handle scope type with case
                        asset = data["data"][n]["attributes"]
                        match asset["asset_type"]:
                            case "WILDCARD":
                                # Write to h1 wildcard file
                                h1_wildcard_file.write(
                                    f'{program}: {asset["asset_identifier"]}\n'
                                )
                            case "URL":
                                # Write to H1 Domains File
                                h1_domains_file.write(
                                    f'{program}: {asset["asset_identifier"]}\n'
                                )
                            case _:
                                pass
                    except:
                        flag = True
                        break
                if flag:
                    break
                else:
                    n += 1
        # Write domains and wildcards to file
