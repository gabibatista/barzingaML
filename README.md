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
sudo apt-get -y upgrade
sudo apt-get -y install vim git python3-pip

sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 10
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 10

git clone https://github.com/gabibatista/barzingaML.git
```

## Scripts for data creation

### Extract data

resize:

```bash
for foo in `ls *.jpg | cut -d \. -f 1`; do convert $foo.jpg -resize 50x50\! -quality 100 data/$foo.jpg; done
```

extract rgb:

```bash
for foo in `ls *.jpg | cut -d \. -f 1`; do convert $foo.jpg txt/$foo.txt ; done
```

create dataset:

```bash
for foo in `ls *.txt | cut -d \. -f 1`; do echo "$(tail -n +2 $foo.txt  | cut -d " " -f 2 | cut -c2- | rev | cut -c2- | rev  | tr '\n' ',')$(grep $foo\, labels.csv | cut -d "," -f 2)"; done > dataset.csv
```

### From video

extract frames

```bash
ffmpeg -i duo.mp4 -r 8 videos/duo_%04d.jpg
```

create dataset

```bash
for foo in `ls *.txt | cut -d \. -f 1`; do echo "$(tail -n +2 $foo.txt  | cut -d " " -f 2 | cut -c2- | rev | cut -c2- | rev  | tr '\n' ',')$(echo $foo |cut -d _ -f 1)"; done > dataset.csv
```
