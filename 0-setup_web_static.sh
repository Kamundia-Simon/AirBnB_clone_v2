#!/usr/bin/env bash
#Setup web servers for deployment of web_static

#check if nginx is installed 
sudo apt-get update
sudo apt-get -y install nginx

#create  directories 
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/
sudo touch /data/web_static/releases/test/index.html

#create fake HTML file
echo "<html>
<head>
</head>
<body>
  Holberton School
</body>
</html>" | sudo tee /data/web_static/releases/test/index.html > /dev/null
#create symbolic link
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of data folder to ubuntu user
sudo chown -R ubuntu:ubuntu /data/

#update nginx configaration
nginx_config="/etc/nginx/sites-enabled/default"
sudo sed -i '/server_name _;/ a\\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n' "$nginx_config"

#check for error
sudo nginx -t

#restart nginx
sudo service nginx restart
