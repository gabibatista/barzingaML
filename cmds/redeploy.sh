#!/bin/bash -xe

REGION=us-central1
ZONE=$REGION-c
PROJECT=barzinganow

gcloud compute ssh --zone $ZONE barzinga-ml -- 'cd /opt/app && git pull && supervisorctl update'
