#from fabric.api import run, local, sudo
from fabric.api import *

env.user = 'ubuntu'

env.hosts = ['54.237.54.19', '54.146.64.168']

def push_files():
    put("./0-setup_web_static.sh", "./")

def execute_file():
    run("chmod 755 0-setup_web_static.sh")
    run("./0-setup_web_static.sh")

def total():
    #get(remote_path="./3-redirection", local_path="./")
    push_files()
    execute_file()
def restart():
    sudo("systemctl restart nginx")

def loc():
    with lcd("versions"):
        local("ls -l")
