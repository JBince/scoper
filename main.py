#! python3

import os
from dotenv import load_dotenv

# Import classes for platforms
from utils.hackerone import HackerOne
from utils.bugcrowd import Bugcrowd
from utils.intigriti import Intigriti

def init():
	load_dotenv()
	hackerone = HackerOne(os.getenv("HACKERONE_USERNAME"),os.getenv("HACKERONE_API_TOKEN"))
	intigriti = Intigriti(os.getenv("INTIGRITI_API_TOKEN"))
	bugcrowd = Bugcrowd(os.getenv("BUGCROWD_API_TOKEN"))
	return hackerone, intigriti, bugcrowd

def main():
	hackerone, intigriti, bugcrowd = init()

	# Get HackerOne Programs
	print("[+] Getting HackerOne Scopes")
	# hackerone.get_programs()
	# hackerone.get_and_write_program_scopes()

	# Get Intigriti Programs
	print("[+] Getting Intigriti Scopes")
	# intigriti.get_programs()
	# intigriti.get_and_write_program_scopes()

	# Get BugCrowd Programs

	# Need to add a final function to cleanup all domains and place them in a single file.
    
    
if __name__ == "__main__":
	main()
