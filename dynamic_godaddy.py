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
ipify_url = 'https://api.ipify.org' # ipify - to get current external IP address
ipify6_url = 'https://api6.ipify.org' # ipify - to get current external IPv6 address
gd_url = f'https://api.godaddy.com/v1/domains/{my_domain}/records/A/{gd_hostname}'# GoDaddy API URL
gd6_url = f'https://api.godaddy.com/v1/domains/{my_domain}/records/AAAA/{gd_hostname}'# GoDaddy AAAA 
headers = {'Authorization': f'sso-key {gd_api_key}:{gd_secret}'}

external_ip = requests.get(ipify_url).text
external_ipv6 = requests.get(ipify6_url).text
logger.debug(f'External IP: {external_ip}')

# get the IP address from the GoDaddy DNS
gd_dns_request = requests.get(gd_url, headers=headers)
gd_dns6_request = requests.get(gd6_url, headers=headers)
if gd_dns_request.status_code == 200:
  gd_dns = gd_dns_request.json()[0]['data']
  logger.debug(f'GoDaddy IP: {gd_dns}')
  logger.debug(f'GoDaddy response: {gd_dns_request.text}')
else:
  logger.error(f'Received {gd_dns_request.status_code} from GoDaddy with info:\n\t\t'
               f'{gd_dns_request.text} -- CANNOT CONTINUE')
  sys.exit(1)


if gd_dns6_request.status_code == 200:
  gd_dns6 = gd_dns6_request.json()[0]['data']
  logger.debug(f'GoDaddy IP: {gd_dns6}')
  logger.debug(f'GoDaddy response: {gd_dns6_request.text}')
else:
  logger.error(f'Received {gd_dns6_request.status_code} from GoDaddy with info:\n\t\t'
               f'{gd_dns6_request.text} -- CANNOT CONTINUE')
                
# check if the addresses match, change GoDaddy if they don't
while True:
  if external_ip == gd_dns:
    logger.info(f'current External IPv4 is {external_ip}, GoDaddy DNS IP is {gd_dns}. All is good')
  elif external_ip != gd_dns:
    logger.info(f'IP has changed from {gd_dns} to {external_ip}!! Updating GoDaddy')
    headers['Content-Type'] = 'application/json'
    data = f'[{{"data": "{external_ip}"}}]'
    new_gd_dns = requests.put(gd_url, data=data, headers=headers)
    if new_gd_dns.status_code == 200:
      logger.info('Successfully changed GoDaddy IPv4')
      logger.debug(f'GoDaddy response: {gd_dns_request.text}')
    else:
      logger.error(f'Received {gd_dns_request.status_code} from GoDaddy with info:\n\t\t'
                   f'GoDaddy IPv4 address probably NOT CHANGED.')
  else:
    logger.warning('something terrible happened IPv4')
  
  if external_ipv6 == gd_dns6:
    logger.info(f'current External IPv6 is {external_ipv6}, GoDaddy DNS IP is {gd_dns6}. All is good')
  elif external_ipv6 != gd_dns6:
    logger.info(f'IPv6 has changed from {gd_dns6} to {external_ipv6}!! Updating GoDaddy')
    headers['Content-Type'] = 'application/json'
    data = f'[{{"data": "{external_ipv6}"}}]'
    new_gd_dns6 = requests.put(gd6_url, data=data, headers=headers)
    if new_gd_dns6.status_code == 200:
      logger.info('Successfully changed GoDaddy IPv6')
      logger.debug(f'GoDaddy response: {gd_dns6_request.text}')
    else:
      logger.error(f'Received {gd_dns6_request.status_code} from GoDaddy with info:\n\t\t'
                   f'GoDaddy IPv6 address probably NOT CHANGED.')
  else:
    logger.warning('something terrible happened IPv6')
  time.sleep(300)
