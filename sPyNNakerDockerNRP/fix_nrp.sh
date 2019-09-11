#!/bin/bash
HOST_WEB="https://spinn-20.cs.man.ac.uk"
HOST_WS="wss://spinn-20.cs.man.ac.uk"
COUNT=$(grep -c nrp-services-local $HBP/nrpBackendProxy/proxy/serversProxy.ts)
if [[ $COUNT -eq 0 ]]; then
    sed -e 's\nrp-services\nrp-services-local\' -i $HBP/nrpBackendProxy/proxy/serversProxy.ts
    sed -e 's\http://localhost:\'$HOST_WEB'/user/'$JUPYTERHUB_USER'/proxy/\' -i $HBP/user-scripts/config_files/nrpBackendProxy/config.json.sample.local
    sed -e 's\ws://localhost:\'$HOST_WS'/user/'$JUPYTERHUB_USER'/proxy/\' -i $HBP/user-scripts/config_files/nrpBackendProxy/config.json.sample.local
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
fi
