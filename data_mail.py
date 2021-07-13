#!/usr/bin/env python3

import requests
import re
import smtplib
import sys
from email.message import EmailMessage
from configparser import RawConfigParser
import argparse

parser = argparse.ArgumentParser(description="Check data on a web page and send it by mail")
parser.add_argument('data_name', help="name of the section to use")
args = parser.parse_args()

data_name = args.data_name

myConfigFile = 'data_mail.config'

config = RawConfigParser()
config.read(myConfigFile)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_4) AppleWebKit/536.30.1 (KHTML, like Gecko) Version/6.0.5 Safari/536.30.1'
}

##
# Get the data to send
##
try:
	r = requests.get(config[data_name]['data_url'], headers=headers)
except KeyError:
	parser.print_usage()
	print(f"Error: section {data_name} does not exist")
	sys.exit()

message = "No message yet"
sendMail = False

if r.status_code != 200:
	message = "Error reading page"
	sendMail = True
else:
	m = re.search(config[data_name]['data_regex'], r.text)
	if m:
		try:
			message = m.group(1)
		except IndexError:
			print(f"Error: Regex must contain 1 group ()")
			sys.exit()
	else:
		message = 'NO DATA IN PAGE'

if not config.has_option(data_name, "last_value"):
	sendMail = True
else:
	if message != config[data_name]['last_value']:
		sendMail = True
		config[data_name]['last_value'] = message
		with open(myConfigFile, 'w') as configfile:
			config.write(configfile)

if sendMail:
	##
	# Send the mail
	##
	body = f"""
		{config[data_name]['data_url']}
	"""

	msg = EmailMessage()
	msg.set_content(body)
	msg['Subject'] = f"{config[data_name]['message_prefix']} {message}"
	msg['From'] = config[data_name]['sent_from']
	msg['To'] = config[data_name]['sent_to']

	try:
		server = smtplib.SMTP(config['mail']['smtp_url'], config['mail']['smtp_port'])
		server.starttls()
		server.login(config['mail']['smtp_user'], config['mail']['smtp_password'])
		server.send_message(msg)
		server.quit()

		print('Email sent!')
	except:
		sys.exit(f'Something went wrong...{sys.exc_info()[0]}')