#!/bin/bash
export CONFIGPROXY_AUTH_TOKEN=$(openssl rand -hex 32)
echo $CONFIGPROXY_AUTH_TOKEN
export JUPYTERHUB_CRYPT_KEY=$(openssl rand -hex 32)
/usr/local/bin/jupyterhub --config /localhome/jupyter/sPyNNakerJupyter/jupyterhub_config_hbp_debug.py --port 7000 --JupyterHub.proxy_api_port=9001 --JupyterHub.hub_port=9081
