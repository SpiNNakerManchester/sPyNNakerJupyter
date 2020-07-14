# Python Script to update the NRP configuration

import json
import os
import shutil

# Get Evironment Variables
JUPYTERHUB_HOST_PORT = os.environ["JUPYTERHUB_HOST_PORT"]
JUPYTERHUB_USER = os.environ["JUPYTERHUB_USER"]
HBP = os.environ["HBP"]


#################################
#### Fix the nrpBackendProxy ####
#################################

# The configuration files to be updated
NRP_PROXY_CONFIG = "{}/user-scripts/config_files/nrpBackendProxy/config.json.sample.local".format(HBP)
NRP_PROXY_CONFIG_TARGET_LOCAL = "{}/nrpBackendProxy/config.json.sample.local".format(HBP)
NRP_PROXY_CONFIG_TARGET = "{}/nrpBackendProxy/config.json".format(HBP)

# Define the URLs to put in place
NRP_SERVICES = "{}/proxy/{}/nrp_services".format(JUPYTERHUB_HOST_PORT, JUPYTERHUB_USER)
WEB_SERVICES = "https://{}".format(NRP_SERVICES)
WS_SERVICES = "wss://{}".format(NRP_SERVICES)

# Read the config file
with open(NRP_PROXY_CONFIG, "r") as config_fp:
    config = json.load(config_fp)

# Update the config parameters
config["servers"]["localhost"]["gzweb"]["assets"] = "{}/assets".format(WEB_SERVICES)
config["servers"]["localhost"]["gzweb"]["nrp-services"] = "{}/".format(WEB_SERVICES)
config["servers"]["localhost"]["gzweb"]["nrp-services-local"] = "http://localhost:8080"
config["servers"]["localhost"]["gzweb"]["videoStreaming"] = "{}/webstream/".format(WEB_SERVICES)
config["servers"]["localhost"]["gzweb"]["websocket"] = "{}/gzbridge".format(WS_SERVICES)
config["servers"]["localhost"]["rosbridge"]["websocket"] = "{}/rosbridge".format(WS_SERVICES)
config["storage"] = "FS"
config["authentication"] = "FS"

# Write the config file
with open(NRP_PROXY_CONFIG, "w") as config_fp:
    json.dump(config, config_fp, indent=4, sort_keys=True)

# Link and copy the config file, because that's what the NRP does    
os.unlink(NRP_PROXY_CONFIG_TARGET_LOCAL)
os.symlink(NRP_PROXY_CONFIG, NRP_PROXY_CONFIG_TARGET_LOCAL)
os.unlink(NRP_PROXY_CONFIG_TARGET)
shutil.copy(NRP_PROXY_CONFIG_TARGET_LOCAL, NRP_PROXY_CONFIG_TARGET)


##########################
#### Fix the FrontEnd ####
##########################

# Proxy URL
PROXY_URL = "https://{}/proxy/{}/nrp/proxy".format(JUPYTERHUB_HOST_PORT, JUPYTERHUB_USER)

# The configuration files to be updated
NRP_FRONTEND_CONFIG = "{}/user-scripts/config_files/ExDFrontend/config.json.local".format(HBP)
NRP_FRONTEND_CONFIG_TARGET = "{}/ExDFrontend/dist/config.json".format(HBP)

# Read the config file
with open(NRP_FRONTEND_CONFIG, "r") as config_fp:
    config = json.load(config_fp)

config["api"]["proxy"]["url"] = PROXY_URL
config["api"]["versionCheck"]["checkEnabled"] = False

# Write the config file
with open(NRP_FRONTEND_CONFIG, "w") as config_fp:
    json.dump(config, config_fp, indent=4, sort_keys=True)
os.unlink(NRP_FRONTEND_CONFIG_TARGET)
shutil.copy(NRP_FRONTEND_CONFIG, NRP_FRONTEND_CONFIG_TARGET)

