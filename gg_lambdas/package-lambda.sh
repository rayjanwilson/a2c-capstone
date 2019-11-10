#!/usr/bin/env bash
# enable extension globbing for the cp command
shopt -s extglob

# delete build/ and lambda.zip
echo "Cleaning previous build..."
[ -d ./build ] && rm -rf build
[ -f ./lambda.zip ] && rm lambda.zip

echo "Creating build directory ..."
mkdir build
echo "Installing python dependencies into build/ ..."
pipenv lock --keep-outdated -r > ./build/requirements.txt
pip install -r ./build/requirements.txt -t build

# copy everything from the current directory into build/ except for build directory itself
echo "Copying lambda code into build/ ..."
cp -r !(build) build/
# https://stackoverflow.com/questions/4585929/how-to-use-cp-command-to-exclude-a-specific-directory

# reduces the zip size
echo "Slimming the package size..."
find build -name '*.so' -exec strip {} \+
find build -name '*__pycache__*' -exec rm -rf {} \+
find build -name '*.dist-info*' -exec rm -rf {} \+
find build -name '*.py[c|o]' -exec rm {} \+

# create the zip file using python3, so zip doesn't need to be on the system
echo "Creating lambda.zip ..."
pipenv run python -m zipfile -c lambda.zip ./build/*
# https://github.com/pypa/pipenv/issues/2705
echo ""
echo "Lambda zip file size:"
du -sh lambda.zip
echo ""
echo "Done"
