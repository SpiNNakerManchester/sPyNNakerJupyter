# This Dockerfile makes a Jupyter Environment which can run the NRP
# NOTE: SpiNNaker is NOT installed here, to allow some modularisation

####################################################
#                   NRP Front End                  #
####################################################
FROM hbpneurorobotics/nrp_frontend:latest as nrp_frontend

####################################################
#      Combine NRP Backend and FrontEnd            #
####################################################
FROM hbpneurorobotics/nrp:latest

# Copy from frontend
COPY --chown=bbpnrsoa:bbp-ext --from=nrp_frontend $HOME/nrp/src/ExDFrontend $HOME/nrp/src/ExDFrontend
COPY --chown=bbpnrsoa:bbp-ext --from=nrp_frontend $HOME/nrp/src/nrpBackendProxy $HOME/nrp/src/nrpBackendProxy

# Install frontend dependencies
WORKDIR $HOME/nrp/src/ExDFrontend
USER root
RUN apt-get update && apt-get install -y ruby-dev
RUN gem install compass
RUN curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash - && apt-get update && apt-get install -y nodejs
RUN npm install -g grunt-cli
RUN npm install -g grunt

# Update the frontend and rebuild it
USER bbpnrsoa
RUN git init . && git config --global user.email "test@test.com" && git config --global user.name "test" && git add --all && git commit -m "Initial Files"
RUN git remote add agdr https://bitbucket.org/agdr/exdfrontend.git && git fetch agdr && git checkout fix_relative_paths_master
RUN /bin/bash -i -c "npm install --no-save && grunt build"

# Prepare the NRP for use
WORKDIR $HOME/nrp/src
RUN git clone --branch=development https://bitbucket.org/hbpneurorobotics/Models.git Models
RUN git clone --branch=development https://bitbucket.org/hbpneurorobotics/Experiments.git Experiments/
RUN sed -e 's\http://localhost:9000/proxy\../nrp/proxy\' -i $HBP/user-scripts/config_files/ExDFrontend/config.json.local
RUN bash -c "$HOME/nrp/src/user-scripts/rendering_mode cpu"
RUN bash -c "python $HOME/nrp/src/user-scripts/generatelowrespbr.py"
RUN bash -c 'cd $HOME/nrp/src && source $HOME/.opt/platform_venv/bin/activate && pyxbgen -u Experiments/bibi_configuration.xsd -m bibi_api_gen && pyxbgen -u Experiments/ExDConfFile.xsd -m exp_conf_api_gen && pyxbgen -u Models/environment_model_configuration.xsd -m environment_conf_api_gen && pyxbgen -u Models/robot_model_configuration.xsd -m robot_conf_api_gen && deactivate'
RUN bash -c 'gen_file_path=$HBP/ExDBackend/hbp_nrp_commons/hbp_nrp_commons/generated && filepaths=$HOME/nrp/src && sudo cp $filepaths/bibi_api_gen.py $gen_file_path &&  sudo cp $filepaths/exp_conf_api_gen.py $gen_file_path && sudo cp $filepaths/robot_conf_api_gen.py $gen_file_path && sudo cp $filepaths/environment_conf_api_gen.py $gen_file_path'
RUN bash -c 'export NRP_MODELS_DIRECTORY=$HBP/Models && mkdir -p $HOME/.gazebo/models && $HBP/Models/create-symlinks.sh'

# Update the user on first run
# RUN echo ". $HOME/.updateuser.sh" >> $HOME/.bashrc
# Fix the NRP paths on first run
RUN echo ". $HBP/user-scripts/fix_nrp.sh " >> $HOME/.bashrc

####################################################
#                       Jupyter                    #
####################################################
ARG NB_USER="bbpnrsoa"
ARG NB_UID="901325"
ARG NB_GID="11860"
ENV SHELL=/bin/bash \
    NB_USER=$NB_USER \
    NB_UID=$NB_UID \
    NB_GID=$NB_GID \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8

USER root

# Install fix_permissions
ADD fix-permissions /usr/local/bin/fix-permissions

# Install Tini
ADD https://github.com/krallin/tini/releases/download/v0.18.0/tini /bin/tini
RUN chmod ugo+x /bin/tini

# Remove any jupyter installed previously
RUN apt-get remove -y ipython3 python3-ipython python3-ipywidgets python3-ipykernel python3-pygments python3-nbconvert python3-notebook python3-widgetsnbextension jupyter-notebook jupyter-core jupyter-nbextension-jupyter-js-widgets  python3-jupyter-client python3-jupyter-core python3-tornado python3-terminado python3-jedi python3-parso python-jinja2

# Update python requirements
RUN pip3 install --upgrade pip setuptools wheel

# Install Jupyter Notebook, Lab, and Hub
# Generate a notebook server config
# Cleanup temporary files
# Correct permissions
# Do all this in a single RUN command to avoid duplicating all of the
# files across image layers when the permissions change
RUN pip3 --no-cache-dir install notebook jupyterhub jupyterlab jupyterlab-git ipympl jupyter-server-proxy \
    && jupyter notebook --generate-config \
    && rm -rf $HOME/.cache/yarn \
    && jupyter serverextension enable --py jupyterlab_git \
    && jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-matplotlib \
    && jupyter nbextension enable --py widgetsnbextension \
    && jupyter lab build \
    && jupyter serverextension enable --py jupyterlab --sys-prefix



RUN pip3 --no-cache-dir install --upgrade ipykernel \
    && pip3 --no-cache-dir install virtualenv

RUN apt-get update && apt-get install -y nano less iputils-ping run-one unzip bzip2 libxext-dev libsm6 libxrender1

RUN rm -rf $HOME/.cache $HOME/.config

RUN fix-permissions $HOME

COPY start.sh /usr/local/bin/
COPY start-notebook.sh /usr/local/bin/
COPY start-singleuser.sh /usr/local/bin/
COPY jupyter_notebook_config.py /etc/jupyter/

EXPOSE 8888

# Configure container startup
ENTRYPOINT ["tini", "-g", "--"]
CMD ["start-notebook.sh"]

##############################################
#                 Final Cleanup              #
##############################################
WORKDIR $HOME
USER bbpnrsoa

RUN bash -c "$HBP/user-scripts/add_new_database_storage_user -u nrpuser -p password"
RUN ln -s ~/.opt/nrpStorage ~/nrpStorage

# Add local files
ADD --chown=bbpnrsoa:bbp-ext frontend.conf $HBP/user-scripts/config_files/nginx/conf.d/frontend.conf
ADD --chown=bbpnrsoa:bbp-ext nrp-services.conf $HBP/user-scripts/config_files/nginx/conf.d/nrp-services.conf
ADD --chown=bbpnrsoa:bbp-ext fix_nrp.sh $HBP/user-scripts/fix_nrp.sh
ADD --chown=bbpnrsoa:bbp-ext fix_nrp.py $HBP/user-scripts/fix_nrp.py
