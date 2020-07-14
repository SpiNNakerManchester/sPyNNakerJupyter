#!/bin/bash
export CONFIGPROXY_AUTH_TOKEN=$(openssl rand -hex 32)
export JUPYTERHUB_CRYPT_KEY=$(openssl rand -hex 32)
/usr/local/bin/jupyterhub --config /localhome/jupyter/sPyNNaker8Jupyter/jupyterhub_config_hbp.py >& server_hbp.out &
