#! python3

import requests
import os
from utils.bbplatform import Platform

class Bugcrowd(Platform):
	# File path constants
	DOMAINS_FILE="data/bugcrowd_domains.txt"
	WILDCARDS_FILE="data/bugcrowd_wildcards.txt"

	def __init__(self, api_token):
		# Ensure that, regardless of what programs we scope, it double checks the directory setup
		Platform.__init__(self)
		self.api_token = api_token
        
		# Create BugCrowd domain file if it does not exist
		if os.path.isfile(self.DOMAINS_FILE):
			pass
		else:
			print("[+] Creating bugcrowd_domains.txt")
			with open(self.DOMAINS_FILE, "w"):
				pass
		
		# Create BugCrowd wildcards file if it does not exist
		if os.path.isfile(self.WILDCARDS_FILE):
			pass
		else:
			print("[+] Creating bugcrowd_wildcards.txt")
			with open(self.WILDCARDS_FILE, "w"):
				pass

	def get_programs(self):
		pass

	def get_and_write_program_scopes(self):
		# Bugcrowd is rate limited to 60 req/min per IP
		pass