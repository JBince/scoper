#! python3

import requests
import os
from utils.bbplatform import Platform

"""
TODO: 
@ Add authorization checks to stop on failure
@ Add checks to ensure only unique lines are added to files
"""
class HackerOne(Platform):
    # File Path Constants
    DOMAINS_FILE = "data/h1_domains.txt"
    WILDCARDS_FILE = "data/h1_wildcards.txt"

    def __init__(self, username, api_token):
        # Ensure that, regardless of what programs we scope, it double checks the directory setup
        Platform.__init__(self)
        self.username = username
        self.api_token = api_token
        self.program_handles = []
        
        # Create Hackerone domain file if it doesn't exist
        if os.path.isfile(self.DOMAINS_FILE):
            pass
        else:
            print("[+] Creating h1_domains.txt")
            with open(self.DOMAINS_FILE, 'w'):
                pass

        # Create wildcards file if it doesn't exist
        if os.path.isfile(self.WILDCARDS_FILE):
            pass
        else:
            print('[+] Creating h1_wildcards.txt')
            with open(self.WILDCARDS_FILE, 'w'):
                pass


    def get_programs(self):
        n = 1
        while True:
            resp = requests.get(
                "https://api.hackerone.com/v1/hackers/programs",
                auth=(self.username, self.api_token),
                params={"page[size]": 100, "page[number]": n},
            )
            data = resp.json()
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
        all_domains_file = open(self.ALL_DOMAINS_FILE, "w")
        all_wildcard_file = open(self.ALL_WILDCARDS_FILE, "w")

        # Iterate over programs
        for program in self.program_handles:
            n = 1
            while True:
                flag = False
                print(f"[+] Getting scopes for {program} from HackerOne")
                # Get all scopes from the program
                resp = requests.get(
                    f"https://api.hackerone.com/v1/hackers/programs/{program}/structured_scopes",
                    auth=(self.username, self.api_token),
                    params={"page[size]": 100, "page[number]": n},
                )
                data = resp.json()
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
