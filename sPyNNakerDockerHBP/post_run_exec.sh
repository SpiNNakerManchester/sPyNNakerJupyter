#!/bin/bash
chown 1000:100 /home/spinnaker/Documents/NRP/user-scripts/config_files/nginx/conf.d/*.conf /home/spinnaker/Documents/NRP/user-scripts/fix_nrp*
chown 1000:100 /home/jovyan/Documents/NRP/user-scripts/config_files/nginx/conf.d/*.conf /home/jovyan/Documents/NRP/user-scripts/fix_nrp*
if grep -q ebrains.eu /etc/jupyter/jupyter_notebook_config.py
then
    echo "Not updating config"
else
    /bin/sed -E "s#^(\s*'Content-Security-Policy':).*\$#\1 \"frame-ancestors 'self' https://collab.humanbrainproject.eu https://*.ebrains.eu\"#" -i /etc/jupyter/jupyter_notebook_config.py
fi
