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

## Install Seafile Drive Client

Follow instructions at https://help.seafile.com/en/drive_client/drive_client_for_linux.html.

## Configure

1. Create folders where the EBRAINS drive should be mounted, and where the local work folder should be mounted.

1. Update any references to ```/localhome/jupyter``` in the following files to point at the correct locations for where you have installed things:

    1. ```jupyterhub_config_hbp.py```

    1. ```run_seafile_mounter.sh```

    1. ```start_server_hbp.sh``` 

## Run Mounter and JupyterHub

1. Start the mounter:

        start_mounter.sh

    Output is stored in ```mounter.out```

1. Start JupyterHub:

        start_server_hbp.sh

    Output is stored in ```server_hbp.out```


Pip Freeze
==========
This code was tested with all (SpiNNakerManchester)[https://github.com/SpiNNakerManchester] on tag 7.0.0

Pip Freeze showed the dependencies as:

appdirs==1.4.4

astroid==2.15.6

attrs==23.1.0

certifi==2023.5.7

charset-normalizer==3.2.0

contourpy==1.1.0

coverage==7.2.7

csa==0.1.12

cycler==0.11.0

dill==0.3.6

ebrains-drive==0.5.1

exceptiongroup==1.1.2

execnet==2.0.2

fonttools==4.41.0

graphviz==0.20.1

httpretty==1.1.4

idna==3.4

importlib-resources==6.0.0

iniconfig==2.0.0

isort==5.12.0

jsonschema==4.18.4

jsonschema-specifications==2023.7.1

kiwisolver==1.4.4

lazy-object-proxy==1.9.0

lazyarray==0.5.2

matplotlib==3.7.2

mccabe==0.7.0

mock==5.1.0

multiprocess==0.70.14

neo==0.12.0

numpy==1.24.4

opencv-python==4.8.0.74

packaging==23.1

pathos==0.3.0

Pillow==10.0.0

pkgutil_resolve_name==1.3.10

platformdirs==3.9.1

pluggy==1.2.0

pox==0.3.2

ppft==1.7.6.6

py==1.11.0

pylint==2.17.4

PyNN==0.11.0

pyparsing==2.4.7

pytest==7.4.0

pytest-cov==4.1.0

pytest-forked==1.6.0

pytest-instafail==0.5.0

pytest-progress==1.2.5

pytest-timeout==2.1.0

pytest-xdist==3.3.1

python-coveralls==2.9.3

python-dateutil==2.8.2

PyYAML==6.0.1

quantities==0.14.1

referencing==0.30.0

requests==2.31.0

rpds-py==0.9.2

scipy==1.10.1

six==1.16.0

tomli==2.0.1

tomlkit==0.11.8

typing_extensions==4.7.1

urllib3==2.0.4

websocket-client==1.6.1

wrapt==1.15.0

zipp==3.16.2

