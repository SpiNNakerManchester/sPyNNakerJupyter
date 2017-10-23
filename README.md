# Installation
This document details the installation of a JupyterHub system for running the sPyNNaker8 platform.  The instructions below are for an Ubuntu system, but should be similar in other systems (with different commands, but the same outcome).


## Install JupyterHub

1. JupyterHub requires Python 3.4 to be installed, as well as npm and nodejs-legacy.  On an Ubuntu system, these are installed using:

    sudo apt-get install python3 npm nodejs-legacy

1. It is additionally useful to install pip:

    wget https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py
    
1. This might result in pip for python 2 being overridden if installed.  If so, you can correct this:

    rm /usr/local/bin/pip
    ln -s /usr/local/bin/pip2 /usr/local/bin/pip

1. You can now install JupyterHub:

    python3 -m pip install jupyterhub
    npm install -g configurable-http-proxy
    
1. Install Docker Spawner (launches a Docker for each user):

    python3 -m pip install dockerspawner
    
1. Install First Use Authenticator (First time a username is used, any password can be used, but that is then kept for future uses):

    python3 -m pip install jupyterhub-firstuseauthenticator


## Install Docker

The sPyNNaker setup uses a Docker image launched for each client.  To set this up:

1. Install docker:

    sudo apt-get install docker.io

1. Get the JupyterHub image:

	docker pull jupyterhub/single-user:0.8

1. Copy the sPyNNakerDocker folder from this repository.

1. Set up the docker image:

    docker build -t spynnaker sPyNNakerDocker/


## Set up JupyterHub

The file ```jupyterhub_config``` in the root of this repository contains the configuration that will launch the ```spynnaker``` docker instance for each user that logs in, and will authenticate each user using the First Use Authenticator.


## Run JupyterHub

As a user who can control Docker on the machine, with the ```jupyterhub_config.py``` in the current folder, start JupyterHub as follows:

    jupyterhub --config jupyterhub_config.py
    
