#!/bin/bash

if [ $ENV = "aws" ]; then
  aws s3 cp s3://ss-common-s3/chkOnepanman/conf/conf_on-aws.yml $YML_PATH
fi
python3 main.py
