#!/bin/bash
url=https://hbpmonitor.bsc.es:5665/v1/actions/process-check-result
service=UMAN-NMC-spinn-20!NMC-JupyterSpiNNaker-Push
ttl=120
username=uman
password=bb91d0039f24e5e62dc0
n_jupyterhub=$(pgrep -c "^jupyterhub$")
if [ $n_jupyterhub -gt 0 ]; then
    n_dockers=$(docker ps | grep jupyter | wc -l)
    curl -s -X POST -H "Accept: application/json" -k -u "$username":"$password" -d "{\"exit_status\": 0, \"plugin_output\": \"JupyterHub Running\", \"performance_data\": \"'Users Online'=$n_dockers\", \"ttl\": $ttl, \"service\": \"$service\"}" $url
else
    curl -s -X POST -H "Accept: application/json" -k -u "$username":"$password" -d "{\"exit_status\": 2, \"plugin_output\": \"JupyterHub Down!\", \"ttl\": $ttl, \"service\": \"$service\"}"
fi
