# Using JupyterHub and SpiNNaker
The Jupyter Notebook is a tool where code can be executed in cells within a browser interface. The code is executed by the Kernel which receives instructions from the Jupyter Notebook frontend.

JupyterHub is a tool allowing multiple users to spawn instances of a Jupyter Notebook server installed on a local machine, so that other people can run Jupyter notebooks as if they were on the local machine.

This means that in demonstrations, users can access a SpiNNaker installation and use PyNN from any device, as long as they have a user account on the serving machine.

### Installing JupyterHub
Make sure all services are installed into the system as **root** instead of into a user directory so that all users can access it.

- Install [Jupyter](http://jupyter.org/install.html) using `pip3` and `sudo` to ensure that Jupyter runs from a Python3 installation. Do not use Anaconda as it creates a Python installation in the local user directory.
- Install [JupyterHub](https://jupyterhub.readthedocs.io/en/latest/) - requires Python3.4 or greater.
- [Create](https://jupyterhub.readthedocs.io/en/latest/config-basics.html) a `jupyter_config.py` file and [add your user as admin](https://jupyterhub.readthedocs.io/en/latest/authenticators-users-basics.html)
- Start JupyterHub by running `sudo jupyterhub` from the folder which contains the config file.

By nature, root can control the amount of access users have. For more security, use a [HTTPS connection](https://jupyterhub.readthedocs.io/en/latest/security-basics.html)

### Using sPyNNaker8
- Make sure the SpiNNaker files are in a system directory (e.g. `/usr/share/`) and that the correct system environmental variables are setup in `/etc/profile.d` or `/etc/profile/`
- Move the `.spynnaker.cfg` file to `/etc/xdg` instead of a user directory so that all users read that instead of creating their own.

## Custom Kernels
A custom kernel has been created to provide additional commands to be used in the notebook. This works by intercepting the code sent by the notebook. The kernel runs **python2.7** so it's compatible with sPyNNaker.

Current commands include:

- `##printmysession` prints a record of all code run in the notebook since restart/reset, to provide easy debug.
- `##rerun x y` executes all the code in cells between cell x and cell y, so you can for example rerun a set of setup cells without executing them individually. `##rerun x` just executes cell x.

More commands can be easily added.

The kernel (which runs python2.7) consists of:

- The `.py` file which should be placed in the `python2.7/site-packages` folder
- The kernel folder containing the `kernel.json`, which should be placed in either `/usr/local/share/jupyter/kernels/` or `/usr/share/jupyter/kernels` depending on your system.

The kernel can then be used in a Notebook by selecting it from the dropdown.

## Using JupyterHub
- Create a local user for each person:
    - `sudo useradd -d /home/[username]/ -m [username]`
    - `sudo passwd [username]`
- Allow the connection through port `8000` in the firewall (note this is reset on reboot):
    - `sudo iptables -A INPUT -p tcp --dport 8000 -j ACCEPT`
- Start the server (see above). Anyone can access the server and login as a local user from `http://[your ip]:8000`

### Other notes
`matplotlib` can be used to plot inline graphs in a notebook. Ensure that it is higher than version 1.3. If TKinter is throwing up display problems, you need to change the matplotlib backend to `Agg` in the config files:
- `/etc/matplotlibrc`
- `/usr/lib64/python2.7/site-packages/matplotlib......../matplotlib/mpl-data/matplotlibrc
