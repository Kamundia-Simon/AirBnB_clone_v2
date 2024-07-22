#!/usr/bin/python3
# Fabric script to distribute an archive to a web server.
import os.path
from fabric.api import env
from fabric.api import put
from fabric.api import run

env.hosts = ["3.94.185.213", "18.233.63.176"]


def do_deploy(archive_path):
    """Distributes an archive to web servers

    Args:
        archive_path (str): path of the archive to distribute
    Returns:
        If the file doesn't exist at archive_path / error(s) occurs - False.
        Otherwise - True.
    """
    if os.path.isfile(archive_path) is False:
        return False
    file = archive_path.split("/")[-1]
    name = file.split(".")[0]

    if put(archive_path, "/tmp/{}".format(file)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("mkdir -p /data/web_static/releases/{}/".
           format(name)).failed is True:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".
           format(file, name)).failed is True:
        return False
    if run("rm /tmp/{}".format(file)).failed is True:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/".format(name, name)).failed is True:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static".
           format(name)).failed is True:
        return False
    if run("rm -rf /data/web_static/current").failed is True:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current".
           format(name)).failed is True:
        return False
    if run("echo '<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\" /><title>AirBnB clone</title></head><body style=\"margin: 0px; padding: 0px;\"><header style=\"height: 70px; width: 100%; background-color: #FF0000\"></header><footer style=\"position: absolute; left: 0; bottom: 0; height: 60px; width: 100%; background-color: #00FF00; text-align: center; overflow: hidden;\"><p style=\"line-height: 60px; margin: 0px;\">Holberton School</p></footer></body></html>' | sudo tee /data/web_static/releases/{}/0-index.html".format(name)).failed:
        return False
    return True
