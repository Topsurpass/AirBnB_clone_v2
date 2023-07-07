# Redo the task #0 but by using Puppet

exec {'update':
  provider => shell,
  command  => 'sudo apt-get -y update',
} ->

exec {'install Nginx':
  provider => shell,
  command  => 'sudo apt-get -y install nginx',
} ->

exec {'start Nginx':
  provider => shell,
  command  => 'sudo service nginx start',
} ->

exec {'create first directory':
  provider => shell,
  command  => 'sudo mkdir -p /data/web_static/releases/test/',
} ->

exec {'create second directory':
  provider => shell,
  command  => 'sudo mkdir -p /data/web_static/shared/',
} ->

exec {'add content to html file':
  provider => shell,
  command  => 'echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html',
} ->

exec {'create symbolic link':
  provider => shell,
  command  => 'sudo ln -sf /data/web_static/releases/test/ /data/web_static/current',
} ->

exec {'add new location to default file':
  provider => shell,
  command  => 'sudo sed -i \'38i\\tlocation /hbnb_static/ {\n\t\talias /data/web_static/current/;\n\t\tautoindex off;\n\t}\n\' /etc/nginx/sites-available/default',
} ->

exec {'restart Nginx':
  provider => shell,
  command  => 'sudo service nginx restart',
} ->

file {'/data/':
  ensure  => directory,
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}
