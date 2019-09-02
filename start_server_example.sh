#!/bin/bash
client_id=<oidc_client_id>
client_secret=<oidc_client_secret>
token_url=https://services.humanbrainproject.eu/oidc/token
userdata_url=https://services.humanbrainproject.eu/oidc/userinfo
username_key=preferred_username
authorize_url=https://services.humanbrainproject.eu/oidc/authorize
callback_url=https://spinn-20.cs.man.ac.uk/hub/oauth_callback

OAUTH2_AUTHORIZE_URL=$authorize_url OAUTH_CLIENT_ID=$client_id OAUTH_CLIENT_SECRET=$client_secret OAUTH2_TOKEN_URL=$token_url OAUTH2_USERDATA_URL=$userdata_url OAUTH2_USERNAME_KEY=$username_key OAUTH_CALLBACK_URL=$callback_url /usr/local/bin/jupyterhub --config /localhome/jupyter/sPyNNaker8Jupyter/jupyterhub_config.py 2&>1 >& spynnaker.out &
