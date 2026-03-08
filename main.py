#! python3

import os
from dotenv import load_dotenv

# Import classes for platforms
from utils.hackerone import hackerone
from utils.bugcrowd import bugcrowd
from utils.intigriti import intigriti

def init():
	load_dotenv()
	h1 = hackerone(os.getenv("HACKERONE_USERNAME"),os.getenv("HACKERONE_API_TOKEN"))
	intig = intigriti(os.getenv("INTIGRITI_API_TOKEN"))
	return h1, intig

def main():
    h1, intig = init()
    intig.get_programs()
    print(intig.program_handles)
    intig.get_and_write_program_scopes()
    
    
if __name__ == "__main__":
	main()
