#! python3

import requests
import re
import os


class YesWeHack:
    DOMAINS_FILE = "data/yeswehack_domains.txt"
    WILDCARDS_FILE = "data/yeswehack_wildcards.txt"

    def __init__(self, access_token):
        self.program_handles = []
        self.headers = {"Authorization": f"Bearer {access_token}"}

    def get_programs(self):
        print("[+] Getting YesWeHack Programs")
        n = 1
        while True:
            resp = requests.get(
                "https://api.yeswehack.com/programs",
                headers=self.headers,
                params={
                    "filter[disabled]": 0,
                    "page": n,
                    "resultsPerPage": 42,
                    "filter[type][]": "bug-bounty",
                },
            )
            data = resp.json()
            for i in range(42):
                try:
                    self.program_handles.append(data["items"][i]["slug"])
                except:
                    print(
                        f"[+] Retrieved {len(self.program_handles)} programs from YesWeHack"
                    )
                    return
            n += 1

    def get_and_write_program_scopes(self):
        # Open file handlers for later writing
        yeswehack_domains_file = open(self.DOMAINS_FILE, "w")
        yeswehack_wildcards_file = open(self.WILDCARDS_FILE, "w")

        # Iterate over programs
        for program in self.program_handles:
            resp = requests.get(
                f"https://api.yeswehack.com/programs/{program}", headers=self.headers
            )
            data = resp.json()
            assets = data["scopes"]
            for asset in assets:
                match asset["scope_type"]:
                    case "wildcard":
                        yeswehack_wildcards_file.write(
                            f"{data["slug"]}: {asset["scope"]}\n"
                        )

                    case "web-application":
                        yeswehack_domains_file.write(
                            f"{data["slug"]}: {asset["scope"]}\n"
                        )
                    case _:
                        pass
