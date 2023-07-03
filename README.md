## for Docker

### change the variables in dynamic_godaddy.py accordingly
my_domain = ' ' # name of GoDaddy domain <br/>
gd_hostname = ' ' # name of DNS record in GoDaddy to look for <br/>
gd_api_key = ' ' # GoDaddy API key <br/>
gd_secret = ' ' # GoDaddy secret <br/>

build the image:
docker image build -t gd_dyndns:0.0.1 .

and add this line as your cronjob:
*/10 * * * * docker run --log-driver syslog --log-opt syslog-facility=daemon --rm gd_dyndns:0.0.1 > /dev/null 2>&1
