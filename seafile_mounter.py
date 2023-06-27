import flask
import os
import subprocess
from configparser import ConfigParser
from flask import request
import traceback
import signal
import argparse


app = flask.Flask(__name__)
app.config["DEBUG"] = True


__processes_by_user = dict()
__mount_dir = None
__data_dir = None
__default_drive_config = None


def __mkdir(d):
    if not os.path.exists(d):
        os.makedirs(d)
        return True
    return False


@app.route("/prepare/<username>")
def prepare(username):
    global __data_dir
    global __mount_dir
    global __default_drive_config

    token = request.args.get("token")
    if token is None:
        app.logger.error("No token for {}".format(username))
        return "Missing token", 500

    user_drive_mnt = os.path.join(__mount_dir, username)

    # Unmount if the directory exists (ignore errors)
    try:
        if os.path.exists(user_drive_mnt):
            unmount(username)
    except Exception:
        app.logger.exception("Ignoring unmount error for {}".format(username))
        pass

    try:
        # Make directories to do the mounting
        user_drive_data = os.path.join(__data_dir, username)
        __mkdir(user_drive_data)
        __mkdir(user_drive_mnt)

        # Write the config for mounting the drive
        user_drive_cfg = os.path.join(user_drive_data, "seadrive.conf")
        config = ConfigParser()
        config.read(__default_drive_config)
        config['account']['username'] = username
        config['account']['token'] = token
        with open(user_drive_cfg, "w") as configfile:
            config.write(configfile)

    except Exception:
        app.logger.exception("Error mounting for {}".format(username))
        return {
            "result": False,
            "error": traceback.format_exc()
        }, 500

    return {"result": True}


@app.route("/mount/<username>")
def mount(username):
    global __processes_by_user
    global __data_dir
    global __mount_dir

    try:
        user_drive_mnt = os.path.join(__mount_dir, username)
        user_drive_data = os.path.join(__data_dir, username)
        user_drive_cfg = os.path.join(user_drive_data, "seadrive.conf")
        user_drive_data_folder = os.path.join(user_drive_data, "data")

        # Do the mount (fuse)
        app.logger.info("Starting the mount for {} in {}".format(username, user_drive_mnt))
        drive_process = subprocess.Popen(" ".join([
            "/usr/bin/seadrive", "-c", user_drive_cfg, "-f",
            "-d", user_drive_data_folder, "-o", "uid=901325,gid=11860,allow_other,umask=002",
            user_drive_mnt]), shell=True)
        app.logger.info("Mount done for {} in {}".format(username, user_drive_mnt))

        # Store the process to be cleared later
        __processes_by_user[username] = drive_process

    except Exception:
        app.logger.exception("Error mounting for {}".format(username))
        return {
            "result": False,
            "error": traceback.format_exc()
        }, 500
    
    return {"result": True}


@app.route("/unmount/<username>")
def unmount(username):
    global __processes_by_user

    # Unmount using fusermount
    app.logger.info("Unmounting for {} using fusermount".format(username))
    user_drive_mnt = os.path.join(__mount_dir, username)
    subprocess.run(["fusermount", "-u", user_drive_mnt])

    # If the process was started here, stop it now
    if username in __processes_by_user:
        app.logger.info("Stopping mount process for {}".format(username))
        drive_process = __processes_by_user[username]
        del __processes_by_user[username]
        drive_process.send_signal(signal.SIGINT)
        drive_process.wait()
        del drive_process

    return {"result": True}


parser = argparse.ArgumentParser(
    description="REST service for mounting Seadrive for docker users")
parser.add_argument("-m", "--mountdir", required=True,
                    help="Directory to mount into")
parser.add_argument("-d", "--datadir", required=True,
                    help="Directory to store data in")
parser.add_argument("-c", "--config", required=True,
                    help="Default config file to fill in")
parser.add_argument("-p", "--port", required=False, default=5000,
                    help="Port to listen on")

args = parser.parse_args()
__mount_dir = args.mountdir
__data_dir = args.datadir
__default_drive_config = args.config

app.run(host="0.0.0.0", port=args.port)

