#from fabric.api import run, local, sudo
from fabric.api import *

env.user = 'ubuntu'

env.hosts = ['54.237.54.19', '54.146.64.168']

def push_files():
    put("./101-setup_web_static.pp", "./")

def execute_file():
    run("puppet apply 100-setup_web_static.pp")

def total():
    #get(remote_path="./3-redirection", local_path="./")
    push_files()
    #execute_file()
def restart():
    sudo("systemctl restart nginx")

def save_file():
    sudo("echo 'Fake static page' > tee /data/web_static/releases/test/index.html")

def loc():
    with lcd("versions"):
        local("ls -l")
