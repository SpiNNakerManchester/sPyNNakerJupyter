FROM jupyterhub/singleuser:0.8

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

USER $NB_USER

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

ENV SPINN_DIRS=/home/$NB_USER/spinnaker_tools
ENV PATH=${PATH}:/home/$NB_USER/spinnaker_tools/tools
ENV PERL5LIB=/home/$NB_USER/spinnaker_tools/tools
ENV NEURAL_MODELLING_DIRS=/home/$NB_USER/sPyNNaker/neural_modelling

RUN make -C /home/$NB_USER/spinnaker_tools
RUN make -C /home/$NB_USER/spinn_common
RUN make -C /home/$NB_USER/spinn_common install
RUN make -C /home/$NB_USER/SpiNNFrontEndCommon/c_common
RUN make -C /home/$NB_USER/SpiNNFrontEndCommon/c_common install
RUN make -C /home/$NB_USER/sPyNNaker/neural_modelling

RUN cd SpiNNUtils && python2 setup.py develop --user --no-deps
RUN cd SpiNNMachine && python2 setup.py develop --user --no-deps
RUN cd SpiNNStorageHandlers && python2 setup.py develop --user --no-deps
RUN cd spalloc && python2 setup.py develop --user --no-deps
RUN cd PACMAN && python2 setup.py develop --user --no-deps
RUN cd SpiNNMan && python2 setup.py develop --user --no-deps
RUN cd DataSpecification && python2 setup.py develop --user --no-deps
RUN cd SpiNNFrontEndCommon && python2 setup.py develop --user --no-deps
RUN cd SpiNNakerGraphFrontEnd && python2 setup.py develop --user --no-deps
RUN cd sPyNNaker && python2 setup.py develop --user --no-deps
RUN cd sPyNNaker8 && python2 setup.py develop --user --no-deps
RUN python2 -m pip install --user matplotlib pylru enum34 six "requests>=2.4.1" jsonschema "rig>=2.0.0,<3.0.0" "quantities>=0.12.1" "lazyarray>=0.2.9,<=0.2.9" "appdirs>=1.4.2,<2.0.0" "neo" numpy scipy "PyNN == 0.9.2" lxml
RUN python2 -m spynnaker8.setup-pynn

ADD .spynnaker.cfg /home/$NB_USER
ADD SynfireExample.ipynb /home/$NB_USER
ADD 02.RunningPyNNSimulations.pdf /home/$NB_USER
ADD 03.SimpleDataInputOutput.pdf /home/$NB_USER
ADD 04.ExternalDevices.pdf /home/$NB_USER
ADD 05.NewNeuronModels.pdf /home/$NB_USER
ADD 06.STDP.pdf /home/$NB_USER

#RUN echo "Installing python2"
#RUN conda create -n Python2 python=2 ipykernel -y
#RUN echo "Activating"
#RUN source activate Python2
