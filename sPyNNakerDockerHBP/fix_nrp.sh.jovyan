#!/bin/bash

# Run the python script to fix config files
python3 $HBP/user-scripts/fix_nrp.py

# NGinX Config
sed -e 's\JUPYTER_USER\'$JUPYTERHUB_USER'\' -i $HBP/user-scripts/config_files/nginx/conf.d/frontend.conf
sed -e 's\JUPYTER_USER\'$JUPYTERHUB_USER'\' -i $HBP/user-scripts/config_files/nginx/conf.d/nrp-services.conf
cp $HBP/user-scripts/config_files/nginx/conf.d/*.conf .local/etc/nginx/conf.d/
