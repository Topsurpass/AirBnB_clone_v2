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
    num = int(number)
    if num == 0:
        num = 2
    else:
        num += 1

    local('cd versions ; ls -t | tail -n +{} | xargs rm -rf'.format(num))
    path = '/data/web_static/releases'
    run('cd {} ; ls -t | tail -n +{} | xargs rm -rf'.format(path, num))
