#!/usr/bin/python3
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generate a .tgz file of the web_static dir
    """
    try:
        name = "web_static_" + datetime.now().strftime("%Y%m%d%H%M%S")
        local('mkdir -p versions')
        local("tar -cvzf versions/{}.tgz {}".format(
            name, "web_static/"))
        return "versions/{}.tgz".format(name)
    except Exception as ex:
        return None
