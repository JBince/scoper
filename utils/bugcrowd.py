#! python3

import requests
from bs4 import BeautifulSoup
import json


class Bugcrowd:
    # File path constants
    DOMAINS_FILE = "data/bugcrowd_domains.txt"
    WILDCARDS_FILE = "data/bugcrowd_wildcards.txt"
    OTHERS_FILE = "data/bugcrowd_other.txt"

    def __init__(self, session):
        # Ensure that, regardless of what programs we scope, it double checks the directory setup
        self.cookies = {"_bugcrowd_session": session}
        self.program_handles = []
        self.changelog_endpoints = []

    def get_programs(self):
        # Get BB Programs
        print("[+] Getting BugCrowd Programs")
        n = 1
        while True:
            resp = requests.get(
                f"https://bugcrowd.com/engagements.json?category=bug_bounty&page={n}",
                cookies=self.cookies,
            )
            data = resp.json()
            for i in range(24):
                try:
                    self.program_handles.append(data["engagements"][i]["briefUrl"])
                except:
                    print(
                        f"[+] Retrieved {len(self.program_handles)} programs from BugCrowd"
                    )
                    return
            n += 1
        # Get VDP

    def get_and_write_program_scopes(self):
        # This loop parses all programs for their changelog endpoint
        bugcrowd_domain_file = open(self.DOMAINS_FILE, "w")
        bugcrowd_wildcard_file = open(self.WILDCARDS_FILE, "w")
        bugcrowd_other_file = open(self.OTHERS_FILE, "w")

        for program in self.program_handles:
            # Retrieve the program page
            resp = requests.get(f"https://bugcrowd.com/{program}", cookies=self.cookies)
            soup = BeautifulSoup(resp.text, "html.parser")
            # The API endpoints are stored in the value of the data-api-endpoints attribute on a div with id researcher-engagement-brief-root
            div = soup.find("div", id="researcher-engagement-brief-root")
            api_raw = div.get("data-api-endpoints")
            api_json = json.loads(api_raw)
            changelog_endpoint = api_json["engagementBriefApi"][
                "getBriefVersionDocument"
            ]
            self.changelog_endpoints.append(changelog_endpoint)

        # This loop retrieves all of the scopes
        for changelog in self.changelog_endpoints:
            data = requests.get(
                f"https://bugcrowd.com{changelog}.json", cookies=self.cookies
            ).json()

            try:
                for scope in data["data"]["scope"]:
                    if scope["inScope"]:
                        for target in scope["targets"]:
                            match target["category"]:
                                case "website":
                                    # Wildcards are not explicitly marked, so must be parsed.
                                    if target["name"].startswith("*"):
                                        bugcrowd_wildcard_file.write(
                                            f"{changelog.split("/")[2]}: {target["name"]}\n"
                                        )
                                    else:
                                        if " " in target["name"]:
                                            bugcrowd_other_file.write(
                                                f"{changelog.split("/")[2]}: {target["name"]}\n"
                                            )
                                        else:
                                            bugcrowd_domain_file.write(
                                                f"{changelog.split("/")[2]}: {target["name"]}\n"
                                            )
                                case "api":
                                    bugcrowd_domain_file.write(
                                        f"{changelog.split("/")[2]}: {target["name"]}\n"
                                    )
                                case _:
                                    pass
                    else:
                        pass
            except Exception as e:
                continue
