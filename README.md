## for Docker
build the image:
docker image build -t gd_dyndns:0.0.1 .

and add this line as your cronjob:
*/10 * * * * docker run --log-driver syslog --log-opt syslog-facility=daemon --rm gd_dyndns:0.0.1 > /dev/null 2>&1
