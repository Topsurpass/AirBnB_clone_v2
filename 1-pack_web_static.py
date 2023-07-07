#!/usr/bin/python3
"""
a Fabric script that generates a .tgz archive from the contents of the
web_static
folder of your AirBnB Clone repo, using the function do_pack.

Prototype: def do_pack():
    All files in the folder web_static must be added to the final archive
    All archives must be stored in the folder versions (your function should
    create this folder if it doesn’t exist)
    The name of the archive created must be
    web_static_<year><month><day><hour><minute><second>.tgz
    The function do_pack must return the archive path if the archive has been
    correctly generated. Otherwise, it should return None
"""
from fabric.api import *
from time import strftime
import os


@runs_once
def do_pack():
    """
    Fabric script that generates a .tgz archive from the contents of the
    web_static folder of your AirBnB Clone repo.
    """
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    present_time = strftime("%Y%M%d%H%M%S")
    output = "versions/web_static_{}.tgz".format(present_time)
    try:
        print("Packing web_static to {}".format(output))
        local("tar -cvzf {} web_static".format(output))
        archize_size = os.stat(output).st_size
        print("web_static packed: {} -> {} Bytes".format(output, archize_size))
    except Exception:
        output = None
    return output
