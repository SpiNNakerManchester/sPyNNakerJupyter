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


## Checkout and install repositories

Checkout the following repositories:

1. This repository:

    git clone https://github.com/SpiNNakerManchester/sPyNNaker8Jupyter

1. DockerSpawner (launches a Docker container from an image for each user):

    git clone https://github.com/SpiNNakerManchester/dockerspawner
    cd dockerspawner
    git checkout ports_and_mounts
    python setup.py develop --user
    cd ..

1. FirstUseAuthenticator (First time a username is used, any password can be used, but that is then kept for future uses):

    cd sPyNNaker8Jupyter
    git clone https://github.com/SpiNNakerManchester/firstuseauthenticator
    cd ..

1. MultiAuth (Setup for using FirstUseAuthenticator, HBP OAuth and EBRAINS OAuth)

    git clone https://github.com/SpiNNakerManchester/multiauth
    cd multiauth
    python setup.py develop --user
    cd ..

1. ClbAuthenticator (EBRAINS authentication with drive mounting):

    git clone https://github.com/SpiNNakerManchester/clb-authenticator
    cd clb-authenticator
    git checkout add_drive_mount
    python setup.py develp --user
    cd ..

## Install Docker

The sPyNNaker setup uses a Docker image launched for each client.  To set this up:

1. Install docker:

        sudo apt-get install docker.io

1. Check the ```.spynnaker.cfg``` file contains the appropriate values for your setup.  You should have a [spalloc server](https://spalloc_server.readthedocs.io/) set up, and you should update the address of this in the config file.

1. Set up the docker image:

        docker build -t spynnakerhbpdebug sPyNNakerDockerHBP/


## Run JupyterHub

A start script has been provided:

    start_server_hbp.sh

Output will be stored in:

    server_hbp.out

