FROM ubuntu:16.04

ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

USER root

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y software-properties-common wget sudo
RUN apt-add-repository ppa:deadsnakes/ppa
RUN apt-add-repository "deb http://packages.ros.org/ros/ubuntu xenial main"
RUN wget -O - http://packages.osrfoundation.org/gazebo.key | sudo apt-key add -
RUN apt-add-repository "deb http://packages.osrfoundation.org/gazebo/ubuntu xenial main"
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    curl git python python-dev python3.6 python3.6-dev build-essential unzip libxext-dev libsm6 libxrender1 \
    gcc-arm-none-eabi libnewlib-arm-none-eabi \
    bzip2 ca-certificates locales fonts-liberation run-one nano less iputils-ping \
    && apt-get -y autoremove \
    && apt-get -y clean  \
    && rm -rf /var/lib/apt/lists/*

# Override older python version with 3.6
RUN rm /usr/bin/python3
RUN ln -s /usr/bin/python3.6 /usr/bin/python3
RUN ln -s /usr/bin/pip3.6 /usr/bin/pip3

RUN echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen
    
# Add a script that we will use to correct permissions after running certain commands
ADD fix-permissions /usr/local/bin/fix-permissions
    
# Configure environment
ENV SHELL=/bin/bash \
    NB_USER=$NB_USER \
    NB_UID=$NB_UID \
    NB_GID=$NB_GID \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
ENV HOME=/home/$NB_USER

# Create NB_USER wtih name jovyan user with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers && \
    sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers && \
    useradd -m -s /bin/bash -N -u $NB_UID $NB_USER && \
    chmod g+w /etc/passwd && \
    fix-permissions $HOME

RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN python2 get-pip.py
RUN python3 get-pip.py
RUN rm get-pip.py
RUN pip2 --no-cache-dir install requests[security]
    
# Install Tini
ADD https://github.com/krallin/tini/releases/download/v0.18.0/tini /bin/tini
RUN chmod ugo+x /bin/tini

# Install Jupyter Notebook, Lab, and Hub
# Generate a notebook server config
# Cleanup temporary files
# Correct permissions
# Do all this in a single RUN command to avoid duplicating all of the
# files across image layers when the permissions change
RUN pip3 --no-cache-dir install \
    'notebook==6.0.0' \
    'jupyterhub==1.0.0' \
    'jupyterlab==1.0.4' && \
    jupyter notebook --generate-config && \
    rm -rf /home/$NB_USER/.cache/yarn && \
    fix-permissions /home/$NB_USER

EXPOSE 8888

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start-notebook.sh"]

# Add local files as late as possible to avoid cache busting
COPY start.sh /usr/local/bin/
COPY start-notebook.sh /usr/local/bin/
COPY start-singleuser.sh /usr/local/bin/
COPY jupyter_notebook_config.py /etc/jupyter/

# Fix permissions on /etc/jupyter as root
USER root
RUN fix-permissions /etc/jupyter/

RUN pip2 --no-cache-dir install --upgrade ipykernel
RUN pip2 --no-cache-dir install virtualenv
RUN pip3 --no-cache-dir install --upgrade ipykernel
RUN pip3 --no-cache-dir install virtualenv

RUN rm -rf $HOME/.cache

# Switch back to jovyan to avoid accidental container runs as root
USER $NB_UID
WORKDIR $HOME

RUN echo "c.IPCompleter.greedy = True" >> .jupyter/jupyter_notebook_config.py

RUN ipython profile create spynnaker
RUN echo "c.InteractiveShellApp.matplotlib = 'notebook'" >> .ipython/profile_spynnaker/ipython_kernel_config.py

RUN python3 -m virtualenv sPyNNaker
ADD --chown=jovyan:users activate $HOME/sPyNNaker/bin/
RUN /bin/bash -c "source sPyNNaker/bin/activate && pip install numpy scipy matplotlib"
RUN /bin/bash -c "source sPyNNaker/bin/activate && pip install ipykernel spynnaker8"
RUN /bin/bash -c "source sPyNNaker/bin/activate && python -m spynnaker8.setup_pynn"
RUN /bin/bash -c "source sPyNNaker/bin/activate && python -m ipykernel install --user --name sPyNNaker --profile spynnaker"

RUN python3 -m virtualenv sPyNNakerGit
ADD --chown=jovyan:users activate $HOME/sPyNNakerGit/bin/
WORKDIR $HOME/sPyNNakerGit
RUN git clone https://github.com/SpiNNakerManchester/SupportScripts.git support
RUN support/install.sh 8 -y
RUN /bin/bash -c "cd sPyNNaker && git checkout fix_ethernet_control_connection"
RUN /bin/bash -c "cd sPyNNaker8 && git checkout fix_ethernet_control_connection"
RUN /bin/bash -c "source bin/activate && cd SpiNNUtils && python setup.py develop"
RUN /bin/bash -c "source bin/activate && pip install ipykernel matplotlib"
RUN /bin/bash -c "source bin/activate && support/automatic_make.sh"
RUN /bin/bash -c "source bin/activate && support/setup.sh"
RUN /bin/bash -c "source bin/activate && python -m spynnaker8.setup_pynn"
RUN /bin/bash -c "source bin/activate && python -m ipykernel install --user --name sPyNNakerGit --profile spynnaker"

WORKDIR $HOME
ADD --chown=jovyan:users .spynnaker.cfg /home/$NB_USER
ADD --chown=jovyan:users SynfireExample.ipynb /home/$NB_USER
ADD --chown=jovyan:users 01.RunningPyNNSimulations /home/$NB_USER/01.RunningPyNNSimulations

# Install things for robotics
USER root
RUN apt-get update && apt-get install -y cmake g++ gcc make curl libz-dev xvfb python-opengl libgl1-mesa-dev libharfbuzz-dev

# Install a proxy server to allow servers to run within Jupyter
RUN python3 -m pip install jupyter-server-proxy

# Install the HBP NRP
RUN apt-get update && apt-get install -y cmake python-h5py python-lxml build-essential doxygen autogen automake libtool autoconf libltdl7-dev libreadline6-dev libncurses5-dev libgsl0-dev libxslt1-dev zlib1g-dev python-opencv ruby libtar-dev libprotoc-dev protobuf-compiler imagemagick libtinyxml2-dev libffi-dev uwsgi-plugin-python cimg-dev libgnuplot-iostream-dev openssh-client
USER $NB_USER
ENV HBP=$HOME/Documents/NRP
ENV NRP_INSTALL_MODE=user
RUN mkdir -p $HBP
WORKDIR $HBP
RUN git clone https://bitbucket.org/hbpneurorobotics/user-scripts.git --branch=master
WORKDIR $HBP/user-scripts
RUN ./clone-all-repos
RUN echo "export PYTHONPATH=" >> $HOME/.bashrc
RUN echo ". $HBP/user-scripts/nrp_variables" >> $HOME/.bashrc
RUN echo ". $HBP/user-scripts/nrp_aliases" >> $HOME/.bashrc
USER root
RUN apt-get update && apt-get install --allow-unauthenticated -y ros-kinetic-desktop-full ros-kinetic-web-video-server ros-kinetic-control-toolbox ros-kinetic-controller-manager ros-kinetic-transmission-interface ros-kinetic-joint-limits-interface ros-kinetic-rosauth ros-kinetic-smach-ros python-rospkg
RUN apt-get remove -y --purge gazebo7* libgazebo7* ros-kinetic-gazebo*
RUN apt-get update && apt-get install -y libignition-math2-dev libignition-transport-dev libignition-transport0-dev
RUN apt-get update && apt-get install -y libsimbody-dev libgts-dev libgdal-dev ruby-ronn xsltproc graphviz-dev
RUN apt-get update && apt-get install -y libgsl0-dev bison byacc
RUN apt-get update && apt-get install -y libgts-dev libjansson-dev
RUN apt-get update && apt-get install -y libblas-dev liblapack-dev libhdf5-dev gfortran
RUN apt-get update && apt-get install -y nginx-extras lua-cjson
RUN apt-get update && apt-get install -y ruby-compass
WORKDIR $HBP/ExDFrontend
RUN gem install compass
RUN pip2 install --force-reinstall virtualenv
USER $NB_USER
ENV USER=$NB_USER
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.33.0/install.sh | /bin/bash
ENV NVM_DIR=$HOME/.nvm
RUN /bin/bash -i -c "nvm install 0.10"
RUN /bin/bash -i -c "nvm install 8"
RUN /bin/bash -i -c "nvm alias default 8"
RUN /bin/bash -i -c "npm install -g bower"
WORKDIR $HBP/user-scripts
RUN /bin/bash -i -c "./configure_nrp 2>/dev/null"
WORKDIR $HBP/ExDFrontend
RUN /bin/bash -i -c "npm install -g grunt-cli"
RUN /bin/bash -i -c "npm install -g grunt"
WORKDIR $HBP/user-scripts
RUN /bin/bash -i -c "./configure_nrp"

# Magic to make the camera work in Xvfb
ENV DISPLAY=:0
RUN sed -Ez 's|(\s*)(#if OGRE_VERSION_MAJOR == 1 && OGRE_VERSION_MINOR < 8\n)(\s*fsaa = 0;\n\s*)(#endif)|\1//\2\3//\4|' -i $HBP/gazebo/gazebo/rendering/Camera.cc
RUN /bin/bash -i -c "./update_nrp build all"
RUN /bin/bash -i -c "./rendering_mode cpu"

# Here be magic to fix for JupyterHub
ADD --chown=jovyan:users nginx.conf $HBP/user-scripts/config_files/nginx/nginx.conf
RUN sed -e 's\http://localhost:9000/proxy\../9000/proxy\' -i $HBP/user-scripts/config_files/ExDFrontend/config.json.local
RUN /bin/bash -i -c "./configure_nrp"
RUN /bin/bash -i -c "cd $HBP/ExDFrontend && npm install --no-save && grunt build"
RUN /bin/bash -i -c "source $HOME/.opt/platform_venv/bin/activate && pyxbgen -u $HBP/user-scripts/migrate_xmltf/xsd/xml-tf-bibi.xsd -m $HBP/user-scripts/migrate_xmltf/lib/bibi_api_gen && deactivate"

# Add SpiNNaker to NRP
WORKDIR $HOME/.opt/platform_venv
ADD --chown=jovyan:users activate $HOME/.opt/platform_venv/bin/
RUN git clone https://github.com/SpiNNakerManchester/SupportScripts.git support
RUN support/install.sh 8 -y
RUN /bin/bash -c "cd sPyNNaker && git checkout fix_ethernet_control_connection"
RUN /bin/bash -c "cd sPyNNaker8 && git checkout fix_ethernet_control_connection"
RUN /bin/bash -c "source bin/activate && cd SpiNNUtils && python setup.py develop"
RUN /bin/bash -c "source bin/activate && pip install --upgrade pip"
RUN /bin/bash -c "source bin/activate && pip install ipykernel matplotlib"
RUN /bin/bash -c "source bin/activate && pip uninstall -y lazyarray"
RUN /bin/bash -c "source bin/activate && support/automatic_make.sh"
RUN /bin/bash -c "source bin/activate && support/setup.sh"
RUN /bin/bash -c "source bin/activate && python -m spynnaker8.setup_pynn"
RUN /bin/bash -c "source bin/activate && pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade numpy"

# Change to working version of NRP
WORKDIR $HBP
RUN cd CLE && git remote add agdr https://bitbucket.org/agdr/cle.git && git fetch agdr spinnaker_changes_merge && git checkout spinnaker_changes_merge
RUN cd ExDBackend && git remote add agdr https://bitbucket.org/agdr/exdbackend.git && git fetch agdr spinnaker_changes_merge && git checkout spinnaker_changes_merge

ADD --chown=jovyan:users fix_nrp.sh $HBP/user-scripts/fix_nrp.sh
ADD --chown=jovyan:users run_xvfb.sh $HBP/user-scripts/run_xvfb.sh

RUN echo ". $HBP/user-scripts/fix_nrp.sh " >> $HOME/.bashrc

USER root
RUN sed '/wrapper=""/ i /usr/bin/Xvfb -shmem -screen 0 1280x1024x24 &' -i /usr/local/bin/start-notebook.sh

USER $NB_UID
WORKDIR $HOME

# Make NRP storage visible from within Jupyter
RUN ln -s $HOME/.opt/nrpStorage nrpStorage
