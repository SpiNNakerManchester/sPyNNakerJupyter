FROM jupyterhub/singleuser:0.9.4

USER root

RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
    curl git python python-dev build-essential unzip libxext-dev libsm6 libxrender1 \
    gcc-arm-none-eabi libnewlib-arm-none-eabi

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN python2 get-pip.py
RUN rm get-pip.py
RUN pip2 --no-cache-dir install requests[security]
RUN rm -rf /root/.cache
RUN echo "Installing Kernel"
RUN python2 -m pip install --upgrade ipykernel
RUN python2 -m ipykernel install
RUN python2 -m pip install virtualenv

USER $NB_USER

WORKDIR /home/$NB_USER

RUN ipython profile create spynnaker
RUN echo "c.InteractiveShellApp.matplotlib = 'notebook'" >> .ipython/profile_spynnaker/ipython_kernel_config.py

RUN python2 -m virtualenv sPyNNaker
RUN /home/$NB_USER/sPyNNaker/bin/pip install ipykernel spynnaker8 matplotlib
RUN /home/$NB_USER/sPyNNaker/bin/python -m spynnaker8.setup-pynn
RUN /home/$NB_USER/sPyNNaker/bin/python -m ipykernel install --user --name sPyNNaker --profile spynnaker

RUN conda create -p /home/$NB_USER/sPyNNakerGit python==3.6
WORKDIR /home/$NB_USER/sPyNNakerGit
RUN git clone https://github.com/SpiNNakerManchester/spinnaker_tools.git
RUN git clone https://github.com/SpiNNakerManchester/spinn_common.git
RUN git clone https://github.com/SpiNNakerManchester/SpiNNUtils.git
RUN git clone https://github.com/SpiNNakerManchester/SpiNNMachine.git
RUN git clone https://github.com/SpiNNakerManchester/SpiNNStorageHandlers.git
RUN git clone https://github.com/SpiNNakerManchester/spalloc.git
RUN git clone https://github.com/SpiNNakerManchester/PACMAN.git
RUN git clone https://github.com/SpiNNakerManchester/SpiNNMan.git
RUN git clone https://github.com/SpiNNakerManchester/DataSpecification.git
RUN git clone https://github.com/SpiNNakerManchester/SpiNNFrontEndCommon.git
RUN git clone https://github.com/SpiNNakerManchester/SpiNNakerGraphFrontEnd.git
RUN git clone https://github.com/SpiNNakerManchester/sPyNNaker.git
RUN git clone https://github.com/SpiNNakerManchester/sPyNNaker8.git
RUN git clone https://github.com/SpiNNakerManchester/PyNN8Examples.git

ENV SPINN_DIRS=/home/$NB_USER/sPyNNakerGit/spinnaker_tools
ENV PATH=${PATH}:/home/$NB_USER/sPyNNakerGit/spinnaker_tools/tools
ENV PERL5LIB=/home/$NB_USER/sPyNNakerGit/spinnaker_tools/tools
ENV NEURAL_MODELLING_DIRS=/home/$NB_USER/sPyNNakerGit/sPyNNaker/neural_modelling

RUN cd SpiNNUtils && python3 setup.py develop --user
RUN /bin/bash -c "source activate /home/$NB_USER/sPyNNakerGit && cd SpiNNUtils && python setup.py develop"
RUN /bin/bash -c "source activate /home/$NB_USER/sPyNNakerGit && pip install ipykernel matplotlib"

RUN make -C /home/$NB_USER/sPyNNakerGit/spinnaker_tools
RUN make -C /home/$NB_USER/sPyNNakerGit/spinn_common
RUN make -C /home/$NB_USER/sPyNNakerGit/spinn_common install
RUN make -C /home/$NB_USER/sPyNNakerGit/SpiNNFrontEndCommon/c_common
RUN make -C /home/$NB_USER/sPyNNakerGit/SpiNNFrontEndCommon/c_common install
RUN make -C /home/$NB_USER/sPyNNakerGit/sPyNNaker/neural_modelling

RUN /bin/bash -c "source activate /home/$NB_USER/sPyNNakerGit && cd SpiNNMachine && python setup.py develop"
RUN /bin/bash -c "source activate /home/$NB_USER/sPyNNakerGit && cd SpiNNStorageHandlers && python setup.py develop"
RUN /bin/bash -c "source activate /home/$NB_USER/sPyNNakerGit && cd spalloc && python setup.py develop"
RUN /bin/bash -c "source activate /home/$NB_USER/sPyNNakerGit && cd PACMAN && python setup.py develop"
RUN /bin/bash -c "source activate /home/$NB_USER/sPyNNakerGit && cd SpiNNMan && python setup.py develop"
RUN /bin/bash -c "source activate /home/$NB_USER/sPyNNakerGit && cd DataSpecification && python setup.py develop"
RUN /bin/bash -c "source activate /home/$NB_USER/sPyNNakerGit && cd SpiNNFrontEndCommon && python setup.py develop"
RUN /bin/bash -c "source activate /home/$NB_USER/sPyNNakerGit && cd SpiNNakerGraphFrontEnd && python setup.py develop"
RUN /bin/bash -c "source activate /home/$NB_USER/sPyNNakerGit && cd sPyNNaker && python setup.py develop"
RUN /bin/bash -c "source activate /home/$NB_USER/sPyNNakerGit && cd sPyNNaker8 && python setup.py develop"
RUN /bin/bash -c "source activate /home/$NB_USER/sPyNNakerGit && python -m spynnaker8.setup_pynn"
RUN /bin/bash -c "source activate /home/$NB_USER/sPyNNakerGit && python -m ipykernel install --user --name sPyNNakerGit --profile spynnaker"

WORKDIR /home/$NB_USER
ADD --chown=jovyan:users  .spynnaker.cfg /home/$NB_USER
ADD --chown=jovyan:users SynfireExample.ipynb /home/$NB_USER
ADD --chown=jovyan:users 01.RunningPyNNSimulations /home/$NB_USER/01.RunningPyNNSimulations

RUN echo "c.IPCompleter.greedy = True" >> .jupyter/jupyter_notebook_config.py

# Install things for robotics
USER root
RUN apt-get update
RUN apt-get install -y software-properties-common
RUN apt-get update
RUN apt-get install -y cmake g++ gcc make curl libz-dev
RUN apt-get install -y xvfb python-opengl libgl1-mesa-dev libharfbuzz-dev
RUN apt-get update && apt-get install -y ffmpeg 

# Install a proxy server to allow servers to run within Jupyter
RUN python3 -m pip install jupyter-server-proxy

