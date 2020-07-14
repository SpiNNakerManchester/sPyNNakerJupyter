#!/bin/bash
HOST_WEB="https://spinn-20.cs.man.ac.uk:444"
HOST_WS="wss://spinn-20.cs.man.ac.uk:444"
COUNT=$(grep -c nrp-services-local $HBP/nrpBackendProxy/proxy/serversProxy.ts)
if [[ $COUNT -eq 0 ]]; then

    # NRP Backend Proxy configuration
    sed -e 's\nrp-services\nrp-services-local\' -i $HBP/nrpBackendProxy/proxy/serversProxy.ts
    sed -e 's\http://localhost:8080\'$HOST_WEB'/proxy/'$JUPYTERHUB_USER'/nrp_services/\' -i $HBP/user-scripts/config_files/nrpBackendProxy/config.json.sample.local
    sed -e 's\ws://localhost:8080\'$HOST_WS'/proxy/'$JUPYTERHUB_USER'/nrp_services/\' -i $HBP/user-scripts/config_files/nrpBackendProxy/config.json.sample.local
    sed '/nrp-services/ a \        "nrp-services-local": "http://localhost:8080",' -i $HBP/user-scripts/config_files/nrpBackendProxy/config.json.sample.local
    rm -f $HBP/nrpBackendProxy/config.json.bak*
    rm -f $HBP/nrpBackendProxy/config.json.sample.local
    ln -s $HBP/user-scripts/config_files/nrpBackendProxy/config.json.sample.local $HBP/nrpBackendProxy/config.json.sample.local
    if [ -f $HBP/nrpBackendProxy/config.json ]; then
        rm $HBP/nrpBackendProxy/config.json
    fi
    cp $HBP/nrpBackendProxy/config.json.sample.local $HBP/nrpBackendProxy/config.json
    sed -e '/storage/ s/Collab/FS/' -i $HBP/nrpBackendProxy/config.json
    sed -e '/authentication/ s/Collab/FS/' -i $HBP/nrpBackendProxy/config.json

    # NRP Front End Config
    sed -e 's\"checkEnabled": true,\"checkEnabled": false,\' -i $HBP/user-scripts/config_files/ExDFrontend/config.json.local

    # NGinX Config
    sed -e 's\JUPYTER_USER\'$JUPYTERHUB_USER'\' -i $HBP/user-scripts/config_files/nginx/conf.d/frontend.conf
    sed -e 's\JUPYTER_USER\'$JUPYTERHUB_USER'\' -i $HBP/user-scripts/config_files/nginx/conf.d/nrp-services.conf
    cp $HBP/user-scripts/config_files/nginx/conf.d/*.conf .local/etc/nginx/conf.d/
fi
