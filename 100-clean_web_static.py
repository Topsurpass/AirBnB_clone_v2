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
from time import strftime
import os.path
env.hosts = ["54.237.54.19", "54.146.64.168"]
env.user = "ubuntu"


def do_pack():
    """
    Fabric script that generates a .tgz archive from the contents of the
    web_static folder of your AirBnB Clone repo.
    """
    present_time = strftime("%Y%M%d%H%M%S")
    try:
        local("mkdir -p versions")
        archived_file_name = "versions/web_static_{}.tgz".format(present_time)
        local("tar -cvzf {} web_static/".format(archived_file_name))
        return archived_file_name
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to your web servers"""
    if not os.path.isfile(archive_path):
        return False
    try:
        filename = archive_path.split("/")[-1]
        rmv_ext = filename.split(".")[0]
        path_rmv_ext = "/data/web_static/releases/{}/".format(rmv_ext)
        symlink = "/data/web_static/current"
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(path_rmv_ext))
        run("tar -xzf /tmp/{} -C {}".format(filename, path_rmv_ext))
        run("rm /tmp/{}".format(filename))
        run("mv {}web_static/* {}".format(path_rmv_ext, path_rmv_ext))
        run("rm -rf {}web_static".format(path_rmv_ext))
        run("rm -rf {}".format(symlink))
        run("ln -s {} {}".format(path_rmv_ext, symlink))
        return True
    except Exception:
        return False


def deploy():
    """creates and distributes an archive to your web servers"""
    created_archive_path = do_pack()
    if not created_archive_path:
        return False
    now_deploy = do_deploy(created_archive_path)
    return now_deploy


def do_clean(number=0):
    """deletes out-of-date archives"""
    if number == 0:
        number = 1
    with lcd('./versions'):
        local("ls -lt | tail -n +{} | rev | cut -f1 -d" " | rev | \
            xargs -d '\n' rm".format(1 + number))
    with cd('/data/web_static/releases/'):
        run("ls -lt | tail -n +{} | rev | cut -f1 -d" " | rev | \
            xargs -d '\n' rm".format(1 + number))
