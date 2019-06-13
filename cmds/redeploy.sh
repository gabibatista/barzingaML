#!/bin/bash -xe

REGION=us-central1
ZONE=$REGION-c
PROJECT=barzinganow

gcloud compute ssh --zone $ZONE pythonapp@barzinga-ml -- 'cd /opt/app && git pull && supervisorctl update'
