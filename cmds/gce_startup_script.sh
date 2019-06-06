#!/bin/bash -ve

# Talk to the metadata server to get the project id
PROJECTID=$(curl -s "http://metadata.google.internal/computeMetadata/v1/project/project-id" -H "Metadata-Flavor: Google")

# Install logging monitor. The monitor will automatically pickup logs sent to syslog
curl -s "https://storage.googleapis.com/signals-agents/logging/google-fluentd-install.sh" | bash
service google-fluentd restart &

# Install dependencies from apt
apt-get update
apt-get install -yq vim git build-essential supervisor python python-dev python-pip libffi-dev libssl-dev authbind

# Create a pythonapp user if doesnt exist. The application will run as this user
id -u pythonapp &>/dev/null || useradd -m -d /home/pythonapp pythonapp

# pip from apt is out of date, so make it update itself and install virtualenv
pip install --upgrade pip virtualenv

# Get the source code from the Google Cloud Repository

# git requires $HOME and it's not set during the startup script
export HOME=/root
sudo git clone https://github.com/gabibatista/barzingaML.git /opt/app

# Install app dependencies
virtualenv -p python3 /opt/app/env
source /opt/app/env/bin/activate
/opt/app/env/bin/pip install -r /opt/app/requirements.txt

# Make sure the pythonapp user owns the application code
chown -R pythonapp:pythonapp /opt/app

cd /opt/app
./cmds/model.sh

# allow running on 80 with authbind
sudo touch /etc/authbind/byport/80
sudo chmod 777 /etc/authbind/byport/80
sudo chown pythonapp:pythonapp /etc/authbind/byport/80

# Configure supervisor to start gunicorn inside of our virtualenv and run the application
cat >/etc/supervisor/conf.d/python-app.conf << EOF
[program:pythonapp]
directory=/opt/app
command=authbind --deep /opt/app/env/bin/honcho start -f ./procfile web
autostart=true
autorestart=true
user=pythonapp
# environment variables ensure that the application runs inside of the configured virtualenv.
environment=VIRTUAL_ENV="/opt/app/env",PATH="/opt/app/env/bin",HOME="/opt/app",USER="pythonapp"
stdout_logfile=syslog
stderr_logfile=syslog
EOF

supervisorctl reread
supervisorctl update

# Application should now be running under supervisor!
