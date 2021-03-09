# Data Mail

## What
This script checks values on a webpage and sends it to your mail

It is written in Python 3

## Why
I needed to check when Apple TAEG credit drops to 0.  
Now, I also use it to check if a new version of a software is out.  
Thanks to a cron, I can schedule it to be launched every day.

## Requirements
```bash
pip install -r requirements.txt
```

OR

```bash
pip install requests
```

## How
* Rename `data_mail.config.spec` into `data_mail.config`
* Fill `[mail]` stanza with your mail information
* Then you can have multiple stanza in `data sections` for multiple sites

	* `[name_1]`: the name of the stanza. Will be passed as parameter for the script
	* `sent_from`: the mail of the sender
	* `sent_to`: the mail of the receiver
	* `data_url`: the url of the webpage to check
	* `data_regex`: the regex to isolate the value to retrieve
	* `message_prefix`: a message that will be written before the value
	* `last_value`: optional. If set, mail will be sent only if new value is different from last value. Remove variable if you do not want it

## --help
```bash
usage: data_mail.py [-h] data_name

Check data on a web page and send it by mail

positional arguments:
  data_name   name of the section to use

optional arguments:
  -h, --help  show this help message and exit

```

### Exemple
```
[apple_taeg]
sent_from = john.doe@gmail.com
sent_to = john.doe@gmail.com
data_url = https://www.apple.com/fr/shop/browse/finance/loan
data_regex = <li>TAEG.*:\s*(.*?)<\/li>
message_prefix = Apple TAEG:
last_value =
```
Call the script with the following command:
```bash
python3 data_mail.py apple_taeg
```