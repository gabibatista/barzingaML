#!/bin/bash -xe

REGION=us-central1
ZONE=$REGION-c
PROJECT=barzinganow

gcloud compute addresses delete barzinga-ml-ip -q \
    --project=$PROJECT \
    --region=$REGION || true

gcloud compute addresses create barzinga-ml-ip \
    --project=$PROJECT \
    --region=$REGION \
    --description="An IP for the barzinga-ml backend service." \
    --network-tier=PREMIUM

ip=`gcloud compute addresses describe barzinga-ml-ip --region $REGION | grep 'address:' | perl -pe 's/address: ([\d.]*)$/$1/'`

echo "Will use ip address: $ip"

gcloud compute instances delete barzinga-ml -q \
    --project=$PROJECT \
    --zone $ZONE || true

gcloud compute instances create barzinga-ml \
    --project=$PROJECT \
    --zone $ZONE \
    --image-family=debian-9 \
    --image-project=debian-cloud \
    --machine-type=g1-small \
    --scopes userinfo-email,cloud-platform \
    --metadata-from-file startup-script=cmds/gce_startup_script.sh \
    --tags default-allow-http \
    --tags default-allow-https \
    --network-interface address=$ip