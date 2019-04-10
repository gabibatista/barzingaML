# barzingaML

Flask API for barzinga

## Setup

To install deps, run

```bash
./cmds/deps.sh
```

Then, you must create the H5 file with the network; run

```bash
./cmds/model.sh
```

## Install on a plain Ubuntu 18 machine

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install vim git python3-pip

sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10

git clone https://github.com/gabibatista/barzingaML.git
```
