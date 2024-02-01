#!/usr/bin/python3
from fabric.api import env, run, local

env.hosts = ["54.144.134.116", "54.144.150.121"]
env.user = "ubuntu"
env.key_filename = "~/.ssh/id_rsa"


def do_clean(number=0):
    """ Deletes out-of-date archives.

    Args:
        number(int): number of the archives, including the most
        recent, to keep.

    If number is 0 or 1, keep only the most recent version of your archive.
    if number is 2, keep the most recent,
    and second most recent versions of your archive. etc.
    """
    # number = 2 if int(number) == 0 else int(number)
    number = int(number)

    if number == 0:
        number = 2
    else:
        number += 1

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(number))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, number))
