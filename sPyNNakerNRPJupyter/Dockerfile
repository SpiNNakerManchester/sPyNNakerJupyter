# This adds SpiNNaker to the NRP Jupyter installation

FROM nrpjupyter:latest

USER root
RUN apt-get update && apt-get install -y openjdk-11-jdk maven gcc-arm-none-eabi libnewlib-arm-none-eabi ffmpeg

USER $NB_USER
WORKDIR $HOME

# Set up Jupyter properly
RUN ipython profile create spynnaker
RUN echo "c.InteractiveShellApp.matplotlib = 'ipympl'" >> .ipython/profile_spynnaker/ipython_kernel_config.py

# Install the release version
RUN python3 -m virtualenv sPyNNaker
ADD --chown=bbpnrsoa:bbp-ext activate $HOME/sPyNNaker/bin/
RUN /bin/bash -c "source sPyNNaker/bin/activate \
                  && pip install numpy scipy matplotlib ipympl pyNN \
                  && pip install ipykernel spynnaker \
                  && python -m spynnaker8.setup_pynn \
                  && python -m ipykernel install --user --name sPyNNaker --profile spynnaker"
RUN mkdir -p sPyNNaker/lib/python3.8/JavaSpiNNaker/SpiNNaker-front-end/target/ \
    && wget https://github.com/SpiNNakerManchester/JavaSpiNNaker/releases/download/6.0.0/spinnaker-exe.jar -O  sPyNNaker/lib/python3.8/JavaSpiNNaker/SpiNNaker-front-end/target/spinnaker-exe.jar

# Install the git version
RUN python3 -m virtualenv sPyNNakerGit
ADD --chown=bbpnrsoa:bbp-ext activate $HOME/sPyNNakerGit/bin/
WORKDIR $HOME/sPyNNakerGit
RUN git clone https://github.com/SpiNNakerManchester/SupportScripts.git support \
    && support/install.sh 8 -y \
    && /bin/bash -c "source bin/activate && cd SpiNNUtils && python setup.py develop" \
    && /bin/bash -c "source bin/activate \
                  && pip install ipykernel matplotlib ipympl pyNN \
                  && support/automatic_make.sh \
                  && support/setup.sh \
                  && python -m spynnaker8.setup_pynn \
                  && python -m ipykernel install --user --name sPyNNakerGit --profile spynnaker \
                  && git clone https://github.com/SpiNNakerManchester/JavaSpiNNaker \
                  && mvn -f JavaSpiNNaker package -Dmaven.test.skip=true"

# Add SpiNNaker to NRP
WORKDIR $HOME/.opt/platform_venv
ADD --chown=bbpnrsoa:bbp-ext activate $HOME/.opt/platform_venv/bin/
RUN /bin/bash -c "source bin/activate \
                  && pip install spynnaker \
                  && python -m spynnaker8.setup_pynn"
RUN mkdir -p lib/python3.8/JavaSpiNNaker/SpiNNaker-front-end/target/ \
    && wget https://github.com/SpiNNakerManchester/JavaSpiNNaker/releases/download/6.0.0/spinnaker-exe.jar -O  lib/python3.8/JavaSpiNNaker/SpiNNaker-front-end/target/spinnaker-exe.jar

# Update the user on first run
RUN echo ". $HOME/.updateuser.sh" >> $HOME/.bashrc

WORKDIR $HOME
USER bbpnrsoa

ADD --chown=bbpnrsoa:bbp-ext run_xvfb.sh $HBP/user-scripts/run_xvfb.sh
ADD --chown=bbpnrsoa:bbp-ext updateuser.sh $HOME/.updateuser.sh
ADD --chown=bbpnrsoa:bbp-ext .spynnaker.cfg $HOME
ADD --chown=bbpnrsoa:bbp-ext SpaceInvaders.ipynb $HOME
ADD --chown=bbpnrsoa:bbp-ext SynfireExample.ipynb $HOME
ADD --chown=bbpnrsoa:bbp-ext 01.RunningPyNNSimulations $HOME/01.RunningPyNNSimulations
ADD --chown=bbpnrsoa:bbp-ext 02.LiveInputAndOutput $HOME/02.LiveInputAndOutput
ADD --chown=bbpnrsoa:bbp-ext 03.NeuroroboticsPlatform $HOME/03.NeuroroboticsPlatform
