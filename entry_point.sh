#!/bin/bash

echo ENV=$ENV

if [ "$ENV" = "aws" ]; then
  echo "get yml conf from s3."
  aws s3 cp "$S3_YML_PATH" "$YML_PATH"
fi
python3 main.py
