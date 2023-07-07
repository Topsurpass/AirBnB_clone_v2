#!/usr/bin/python3
"""
A Fabric script (based on the file 2-do_deploy_web_static.py) that creates
and distributes an archive to your web servers, using the function deploy:

    Prototype: def deploy():
    The script should take the following steps:
    Call the do_pack() function and store the path of the created archive
    Return False if no archive has been created
    Call the do_deploy(archive_path) function, using the new path of the new
    archive
    Return the return value of do_deploy
    All remote commands must be executed on both of web your servers
    (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in your script)
    You must use this script to deploy it on your servers: xx-web-01 and
    xx-web-02
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
        print("New version deployed!")
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
