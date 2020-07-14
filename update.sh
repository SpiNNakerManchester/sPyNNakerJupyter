echo "c.NotebookApp.tornado_settings = { \
    'headers': { \
        'Content-Security-Policy': \"frame-ancestors 'self' https://collab.humanbrainproject.eu\" \
    } \
}" >> /home/$NB_USER/.jupyter/jupyter_notebook_config.py

curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
apt-get install -y nodejs
pip3 --no-cache-dir install --pre jupyterlab==2.1.1 jupyterlab-git==0.20.0rc0 ipympl
jupyter serverextension enable --py jupyterlab_git && jupyter labextension install @jupyter-widgets/jupyterlab-manager jupyter-matplotlib && jupyter nbextension enable --py widgetsnbextension && jupyter lab build

su jovyan -c /bin/bash -c "source sPyNNaker/bin/activate && pip install ipympl"
su jovyan -c /bin/bash -c "source sPyNNakerGit/bin/activate && pip install ipympl"
su jovyan -c "sed 's/notebook/widget/' -i .ipython/profile_spynnaker/ipython_kernel_config.py"

