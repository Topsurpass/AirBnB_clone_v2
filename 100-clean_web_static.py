#!/usr/bin/python3
"""
A Fabric script (based on the file 3-deploy_web_static.py) that deletes
out-of-date archives, using the function do_clean:

     Prototype: def do_clean(number=0):
         number is the number of the archives, including the most recent,
         to keep.
         If number is 0 or 1, keep only the most recent version of your
         archive.
         if number is 2, keep the most recent, and second most recent
         versions of your archive.
         etc.
         Your script should:
             Delete all unnecessary archives (all archives minus the number to
             keep) in the versions folder
             Delete all unnecessary archives (all archives minus the number to
             keep) in the /data/web_static/releases folder of both of your web
             servers
             All remote commands must be executed on both of your web servers
             (using the env.hosts = ['<IP web-01>', 'IP web-02'] variable
             in your script)
"""
from fabric.api import *
import os

env.hosts = ["54.237.54.19", "54.146.64.168"]
env.user = "ubuntu"


def do_clean(number=0):
    """deletes out-of-date archives"""
    if int(number) == 0:
        number = 1
    else:
        int(number)

    archv = sorted(os.listdir("versions"))
    [archv.pop() for i in range(number)]
    with lcd("versions"):
        [local("rm ./{}".format(j)) for j in archv]

    with cd("/data/web_static/releases"):
        archv = run("ls -tr").split()
        archv = [j for j in archv if "web_static_" in j]
        [archv.pop() for i in range(number)]
        [run("rm -rf ./{}".format(j)) for j in archv]
