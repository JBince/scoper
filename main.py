#! python3

import os
from dotenv import load_dotenv
import glob
import argparse
import shutil

# Import classes for platforms
from utils.hackerone import HackerOne
from utils.bugcrowd import Bugcrowd
from utils.intigriti import Intigriti
from utils.yeswehack import YesWeHack

# File Constants
ALL_DOMAINS_FILE = "data/domains_complete.txt"
ALL_WILDCARDS_FILE = "data/wildcards_complete.txt"

"""
TODO
@ Add authentication checks for platforms, i.e. if it fails, let user know, continue where possible.
@ Should probably add some debugging/logging statements
"""


def init():
    load_dotenv()

    # Removes any old data, just so you have the freshest pull each time

    if os.path.isdir("data"):
        shutil.rmtree("./data")
        os.mkdir("data")
    else:
        os.mkdir("data")

    parser = argparse.ArgumentParser(
        prog="Scoper",
        description="A Python tool to retrieve bug bounty program scopes, both public and private, from your favorite platforms",
    )

    parser.add_argument(
        "-p",
        "--platforms",
        nargs="+",
        choices=["h1", "bc", "ywh", "intig", "all"],
        default=["all"],
        help="Select one or more platforms to retrieve program scopes from. Default: all",
    )
    args = parser.parse_args()
    banner = """
░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓███████▓▒░░▒▓████████▓▒░▒▓███████▓▒░  
░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
 ░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓███████▓▒░░▒▓██████▓▒░ ░▒▓███████▓▒░  
       ░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
       ░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░░▒▓█▓▒░▒▓█▓▒░      ░▒▓█▓▒░      ░▒▓█▓▒░░▒▓█▓▒░ 
░▒▓███████▓▒░ ░▒▓██████▓▒░ ░▒▓██████▓▒░░▒▓█▓▒░      ░▒▓████████▓▒░▒▓█▓▒░░▒▓█▓▒░ 
                                                                                
A Python tool to retrieve bug bounty program scopes, both public and private, from your favorite platforms

By .joward
"""
    print(banner)
    platforms = []
    if "all" in args.platforms:
        platforms.append(
            hackerone := HackerOne(
                os.getenv("HACKERONE_USERNAME"), os.getenv("HACKERONE_API_TOKEN")
            )
        )
        platforms.append(intigriti := Intigriti(os.getenv("INTIGRITI_API_TOKEN")))
        platforms.append(bugcrowd := Bugcrowd(os.getenv("BUGCROWD_SESSION")))
        platforms.append(yeswehack := YesWeHack(os.getenv("YESWEHACK_AUTH_TOKEN")))
    else:
        for i in args.platforms:
            match i:
                case "h1":
                    platforms.append(
                        hackerone := HackerOne(
                            os.getenv("HACKERONE_USERNAME"),
                            os.getenv("HACKERONE_API_TOKEN"),
                        )
                    )
                case "intig":
                    platforms.append(
                        intigriti := Intigriti(os.getenv("INTIGRITI_API_TOKEN"))
                    )
                case "bc":
                    platforms.append(
                        bugcrowd := Bugcrowd(os.getenv("BUGCROWD_SESSION"))
                    )
                case "ywh":
                    platforms.append(
                        yeswehack := YesWeHack(os.getenv("YESWEHACK_AUTH_TOKEN"))
                    )
                case _:
                    pass

    return platforms


def compile_files():
    print("[+] Scope retrieval complete, compiling master files")

    # Open or create master files
    all_domains = open(ALL_DOMAINS_FILE, "w")

    all_wildcards = open(ALL_WILDCARDS_FILE, "w")

    domain_list = glob.glob("data/*_domains.txt")
    wildcard_list = glob.glob("data/*_wildcards.txt")

    for domain_file in domain_list:
        with open(domain_file, "r") as file:
            for line in file:
                domain = line.split()[1]
                all_domains.write(f"{domain}\n")

    for wildcard_file in wildcard_list:
        with open(wildcard_file, "r") as file:
            for line in file:
                wildcard = line.split()[1]
                all_wildcards.write(f"{wildcard}\n")


def main():
    platforms = init()

    for platform in platforms:
        platform.get_programs()
        platform.get_and_write_program_scopes()

    compile_files()


if __name__ == "__main__":
    main()
