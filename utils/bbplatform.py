# A base class for platforms to inherit from

import os

class Platform:
    ALL_DOMAINS_FILE="data/all_domains.txt"
    ALL_WILDCARDS_FILE="data/all_wildcards.txt"

    def __init__(self):

        # Create data folder if it doesn't exist
        if os.path.isdir("data"):
            pass
        else:
            print("[+] Creating data directory")
            os.mkdir("data")

        # Create all_domains.txt if it doesn't exist
        if os.path.isfile(self.ALL_DOMAINS_FILE):
            pass
        else:
            print("[+] Creating all_domains.txt")
            with open(self.ALL_DOMAINS_FILE, 'w'):
                pass

        # Create all_wildcards.txt if it doesn't exist
        if os.path.isfile(self.ALL_WILDCARDS_FILE):
            pass
        else:
            print("[+] Creating all_wildcards.txt")
            with open(self.ALL_WILDCARDS_FILE, 'w'):
                pass
