#!/bin/bash
HOST="spinn-20.cs.man.ac.uk:9000"
COUNT=$(grep -c nrp-services-local $HBP/nrpBackendProxy/proxy/serversProxy.ts)
if [[ $COUNT -eq 0 ]]; then
    sed -e 's\nrp-services\nrp-services-local\' -i $HBP/nrpBackendProxy/proxy/serversProxy.ts
    sed -e 's\://localhost:\://'$HOST'/user/'$JUPYTERHUB_USER'/proxy/\' -i $HBP/user-scripts/config_files/nrpBackendProxy/config.json.sample.local
    sed '/nrp-services/ a \        "nrp-services-local": "http://localhost:8080",' -i $HBP/user-scripts/config_files/nrpBackendProxy/config.json.sample.local
    $HBP/user-scripts/configure_nrp
fi
