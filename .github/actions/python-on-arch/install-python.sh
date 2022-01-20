#!/bin/bash

PYTHON_VERSION=$1

apt-get update -y
apt-get install -y software-properties-common
add-apt-repository ppa:deadsnakes/ppa

apt-get install -y build-essential curl
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py

if [ "$PYTHON_VERSION" = "py39" ]; then
    apt-get install -y python3.9 python3.9-distutils python3.9-dev python3.9-venv
    ln -s /usr/bin/python3.9 /usr/bin/python
elif [ "$PYTHON_VERSION" = "py10" ]; then
    apt-get install -y python3.10 python3.10-distutils python3.10-dev python3.10-venv
    ln -s /usr/bin/python3.10 /usr/bin/python
fi

python get-pip.py --user
mv /root/.local/bin/* /usr/bin/
python -m pip install packaging