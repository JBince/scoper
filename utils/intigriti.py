#! python3

import requests
import os
from utils.bbplatform import Platform

"""
TODO: 
@ Add authorization checks to stop on failure
@ Add checks to ensure only unique lines are added to files
"""

class Intigriti(Platform):
    # File path constants
    DOMAINS_FILE="data/intigriti_domains.txt"
    WILDCARDS_FILE="data/intigriti_wildcards.txt"

    def __init__(self, api_token):
        # Ensure that, regardless of what programs we scope, it double checks the directory setup
        Platform.__init__(self)
        self.program_handles = []
        self.headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {api_token}",
        }

        # Create Hackerone domain file if it doesn't exist
        if os.path.isfile(self.DOMAINS_FILE):
            pass
        else:
            print("[+] Creating intigriti_domains.txt")
            with open(self.DOMAINS_FILE, 'w'):
                pass

        # Create wildcards file if it doesn't exist
        if os.path.isfile(self.WILDCARDS_FILE):
            pass
        else:
            print("[+] Creating intigriti_wildcards.txt")
            with open(self.WILDCARDS_FILE, 'w'):
                pass

    def get_programs(self):
        n = 0
        while True:
            # Gets programs 100 at a time
            headers = self.headers
            resp = requests.get(
                "https://api.intigriti.com/external/researcher/v1/programs",
                headers=headers,
                params={"limit": "100", "offset": n},
            )
            data = resp.json()
            for i in range(100):
                try:
                    # Scopes are found by a GUID, rather than by a name like the H1 scoping
                    self.program_handles.append(data["records"][i]["id"])
                except:
                    print(
                        f"[+] Retrieved {len(self.program_handles)} programs from Intigriti"
                    )
                    return
            n += 100

    def get_and_write_program_scopes(self):
        # Open file handlers for later writing
        intigriti_domains_file = open(self.DOMAINS_FILE, "w")
        intigriti_wildcard_file = open(self.WILDCARDS_FILE, "w")
        all_domains_file = open(self.ALL_DOMAINS_FILE, "w")
        all_wildcard_file = open(self.ALL_WILDCARDS_FILE, "w")

        # Iterate over programs
        for program in self.program_handles:
            flag = True
            print(f"[+] Getting Scopes for {program} from Intigriti")
            # Get all scopes for the programs
            resp = requests.get(
                f"https://api.intigriti.com/external/researcher/v1/programs/{program}",
                headers=self.headers,
            )
            data = resp.json()
            # If it returns a 403, it's likely a program you have not yet applied to. We just skip those
            if resp.status_code == 403:
                continue
            else:
                # Parse the in-scope assets
                assets = data["domains"]["content"]
                for asset in assets:
                    # Remove out of scope assets from parsing
                    if asset["tier"]["id"] == 5:
                        continue
                    else:
                        match asset["type"]["id"]:
                            # Type 1 is a URL
                            case 1:
                                intigriti_domains_file.write(
                                    f'{data["handle"]}: {asset["endpoint"]}\n'
                                )
                                all_domains_file.write(f'{asset["endpoint"]}\n')
                            # Type 7 is a wildcard
                            case 7:
                                intigriti_wildcard_file.write(
                                    f'{data["handle"]}: {asset["endpoint"]}\n'
                                )
                            case _:
                                pass
