/bin/sed -E "s#^(\s*'Content-Security-Policy'):.*\$#\1 \"frame-ancestors 'self' https://collab.humanbrainproject.eu https://*.ebrains.eu\"#" -i /etc/jupyter/jupyter_notebook_config.py
