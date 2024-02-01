#!/usr/bin/python3
from fabric.api import env, run, put
from os import path

env.hosts = ["54.144.134.116", "54.144.150.121"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_deploy(archive_path):
    """ Deploy archive to server """
    if not (path.exists(archive_path)):
        print("Path error")
        return False
    fd = archive_path.split("/")[1]
    try:
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
    except:
        print("Deployment failed!")
        return False
