#!/usr/bin/python3
from fabric.api import env, local, run, put
from os import path
from datetime import datetime

env.hosts = ["54.144.134.116", "54.144.150.121"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_pack():
    """ Packs the web static files into .tgz """
    try:
        file = "web_static_" + datetime.now().strftime("%Y%m%d%H%M%S")
        local('mkdir -p versions')
        local("tar -cvzf versions/{}.tgz {}".format(file, "web_static/"))
        return ("versions/{}.tgz".format(file))
    except Exception:
        return None


def do_deploy(archive_path):
    """ Deploy archive to server

    Args:
        archive_path(str): the path of the archive to distribute
    Returns:
        if file doesn't exists - False,
        otherwise - True.
    """
    if (path.isfile(archive_path) is False):
        print("Not a file")
        return False

    try:
        fd = archive_path.split("/")[1]
        put(archive_path, "/tmp/{}".format(fd))
        run("mkdir -p /data/web_static/releases/{}".format(fd))
        run("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(fd, fd))
        run("rm /tmp/{}".format(fd))
        run("mv /data/web_static/releases/{}/web_static/*\
        /data/web_static/releases/{}/".format(fd, fd))
        run("rm -rf /data/web_static/releases/{}/web_static".format(fd))
        run("rm -rf /data/web_static/current")
        run("ln -s /data/web_static/releases/{}/\
        /data/web_static/current".format(fd))
        print("New version deployed!")
        return True
    except Exception:
        print("Deployment failed!")
        return False


def deploy():
    """ Creates and distribute the archive to a web server """
    try:
        p_file = do_pack()
        return do_deploy(p_file)
    except:
        return False
