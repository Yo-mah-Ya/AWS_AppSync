#!/usr/bin/env bash
BUCKET_NAME="your-bucket-name-here"
STACK_NAME="AppSync-to-SQS"
aws cloudformation package \
    --template-file template.yml \
    --output-template-file packaged_template.yml \
    --s3-bucket ${BUCKET_NAME}

aws cloudformation deploy \
    --template-file packaged_template.yml \
    --stack-name ${STACK_NAME} \
    --capabilities CAPABILITY_NAMED_IAM
