#!/usr/bin/python3.10

import sys
import logging
import logging.handlers
import requests
import time

# create logger
logger = logging.getLogger('dynamic_gd_dns')
logger.setLevel(logging.INFO) # DEBUG, INFO, WARNING, ERROR, CRITICAL
# create console handler and set level to debug

# comment out the StreamHandler() if running as a cron job not a container
ch = logging.StreamHandler()

# comment out the SysLogHandler() if running as a container not a cronjob
#ch = logging.handlers.SysLogHandler(address = '/dev/log')
ch.setLevel(logging.INFO) # DEBUG, INFO, WARNING, ERROR, CRITICAL
# create formatter
formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

my_domain = 'garflak.com' # name of GoDaddy domain
gd_hostname = 'gateway' # name of DNS record in GoDaddy to look for
gd_api_key = 'AQ8opxtekmU_TgxBdVxeRDXwQyQt85KqCh' # GoDaddy API key
gd_secret = '3MTFiBZyKJpyyh2FFVhL3V' # GoDaddy secret
ipify_url = 'https://api6.ipify.org' # ipify - to get current external IP address
gd_url = f'https://api.godaddy.com/v1/domains/{my_domain}/records/A/{gd_hostname}'# GoDaddy API URL
headers = {'Authorization': f'sso-key {gd_api_key}:{gd_secret}'}

external_ip = requests.get(ipify_url).text
logger.debug(f'External IP: {external_ip}')

# get the IP address from the GoDaddy DNS
gd_dns_request = requests.get(gd_url, headers=headers)
if gd_dns_request.status_code == 200:
  gd_dns = gd_dns_request.json()[0]['data']
  logger.debug(f'GoDaddy IP: {gd_dns}')
  logger.debug(f'GoDaddy response: {gd_dns_request.text}')
else:
  logger.error(f'Received {gd_dns_request.status_code} from GoDaddy with info:\n\t\t'
               f'{gd_dns_request.text} -- CANNOT CONTINUE')
  sys.exit(1)
                
# check if the addresses match, change GoDaddy if they don't
while True:
  if external_ip == gd_dns:
    logger.info(f'current External IP is {external_ip}, GoDaddy DNS IP is {gd_dns}. All is good')
  elif external_ip != gd_dns:
    logger.info(f'IP has changed from {gd_dns} to {external_ip}!! Updating GoDaddy')
    headers['Content-Type'] = 'application/json'
    data = f'[{{"data": "{external_ip}"}}]'
    new_gd_dns = requests.put(gd_url, data=data, headers=headers)
    if new_gd_dns.status_code == 200:
      logger.info('Successfully changed GoDaddy IP')
      logger.debug(f'GoDaddy response: {gd_dns_request.text}')
    else:
      logger.error(f'Received {gd_dns_request.status_code} from GoDaddy with info:\n\t\t'
                   f'GoDaddy IP address probably NOT CHANGED.')
  else:
    logger.warning('something terrible happened')
  time.sleep(300)
