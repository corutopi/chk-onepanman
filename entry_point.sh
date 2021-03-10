#!/bin/bash

echo ENV=$ENV

if [ "$ENV" = "aws" ]; then
  aws s3 cp "$S3_YML_PATH" "$YML_PATH"
fi
python3 main.py
