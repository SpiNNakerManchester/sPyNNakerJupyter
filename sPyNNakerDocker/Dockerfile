FROM jupyterhub/singleuser:0.8

USER root

RUN apt-get update -qq && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq --no-install-recommends \
    curl git python python-dev build-essential unzip libxext-dev libsm6 libxrender1

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN curl -O https://bootstrap.pypa.io/get-pip.py
RUN python2 get-pip.py
RUN rm get-pip.py
RUN pip2 --no-cache-dir install requests[security]
RUN rm -rf /root/.cache
RUN echo "Installing Kernel"
RUN python2 -m pip install --upgrade ipykernel
RUN python2 -m ipykernel install
RUN python2 -m pip install sPyNNaker8 matplotlib
RUN python2 -m spynnaker8.setup-pynn

USER $NB_USER

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
