#!/bin/bash
if [ -d /home/jovyan/Documents ]; then
    mv /root/frontend.conf.jovyan /home/jovyan/Documents/NRP/user-scripts/config_files/nginx/conf.d/frontend.conf
    mv /root/nrp-services.conf.jovyan /home/jovyan/Documents/NRP/user-scripts/config_files/nginx/conf.d/nrp-services.conf
    mv /root/fix_nrp.sh /root/fix_nrp.py /home/jovyan/Documents/NRP/user-scripts/
    chown 1000:100 /home/jovyan/Documents/NRP/user-scripts/config_files/nginx/conf.d/*.conf /home/jovyan/Documents/NRP/user-scripts/fix_nrp*
fi
if [ -d /home/spinnaker/Documents ]; then
    mv /root/frontend.conf.spinnaker /home/spinnaker/Documents/NRP/user-scripts/config_files/nginx/conf.d/frontend.conf
    mv /root/nrp-services.conf.spinnaker /home/spinnaker/Documents/NRP/user-scripts/config_files/nginx/conf.d/nrp-services.conf
    mv /root/fix_nrp.sh /root/fix_nrp.py /home/spinnaker/Documents/NRP/user-scripts/
    chown 1000:100 /home/spinnaker/Documents/NRP/user-scripts/config_files/nginx/conf.d/*.conf /home/spinnaker/Documents/NRP/user-scripts/fix_nrp*
fi
if grep -q ebrains.eu /etc/jupyter/jupyter_notebook_config.py
then
    echo "Not updating config"
else
    /bin/sed -E "s#^(\s*'Content-Security-Policy':).*\$#\1 \"frame-ancestors 'self' https://collab.humanbrainproject.eu https://*.ebrains.eu\"#" -i /etc/jupyter/jupyter_notebook_config.py
fi
