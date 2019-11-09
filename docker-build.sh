#!/usr/bin/env bash
docker run --rm -v "$PWD":/var/task lambci/lambda:build-python3.7 ./package-lambda.sh
