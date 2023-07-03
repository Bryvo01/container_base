## GoDaddy
(copied/modified from https://www.instructables.com/Quick-and-Dirty-Dynamic-DNS-Using-GoDaddy/)<br\>
Add an A record in GoDaddy.

For "Type" make sure to use "A" -- CNAME won't work.

For "Host" enter the hostname you'd like to use. I like to use "gateway" because it's how I reach the resources behind the entry point to my home network.

For "Points to" you can enter anything you want. I use "1.1.1.1" so that it will be obvious my script is working once I run it. This is the value that will change when your ISP changes you IP address.

For "TTL" choose "Custom" then put in an arbitrarily short timeout. This tells systems that read this DNS record how long they should cache it before getting a new one. Typically, this is long (1 hour) for static DNS entries. It helps reduce DNS traffic on the general internet. For dynamic DNS, I like to use something shorter like 600 seconds (10 minutes). You don't want this to be too long because it governs the "switching" time between your old IP address and your new one. If this is an hour, it could take up to an hour to reach your dynamic resource after an IP change. NOTE: you can always flushdns at the endpoint, but sometimes intermediate DNS servers will cache the reply (again, to save on traffic).

The most important thing is to make sure it's an "A" record.

Go to this link [GoDaddy API Keys](https://developer.godaddy.com/keys) and click "Create New API key"

You'll want to give it a new name (I use "Dynamic DNS") and select an environment. GoDaddy recommends you test with the OTE environment first, then move to Production. You're using my code, so you can probably just create a production key.

Next, you'll see your API key and your key secret. Make sure you copy these down. The API key will still be visible when you come back to this screen, but the secret will never be displayed again and cannot be recovered!! If you lose the secret, you'll have to create a new key. HINT: Don't lose the secret.

## Docker

### change the variables in dynamic_godaddy.py accordingly
my_domain = ' ' # name of GoDaddy domain <br/>
gd_hostname = ' ' # name of DNS record in GoDaddy to look for <br/>
gd_api_key = ' ' # GoDaddy API key <br/>
gd_secret = ' ' # GoDaddy secret <br/>

build the image:
docker image build -t gd_dyndns:0.0.1 .

and add this line as your cronjob:
*/10 * * * * docker run --log-driver syslog --log-opt syslog-facility=daemon --rm gd_dyndns:0.0.1 > /dev/null 2>&1
