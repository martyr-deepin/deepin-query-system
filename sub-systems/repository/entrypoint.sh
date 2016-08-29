#!/bin/bash -e
cd /data/deepin-query-system

# fetch source
git fetch
git checkout origin/master

# cover the system sources.list
cp sub-systems/repository/sources.list /etc/apt/sources.list

# update apt list before launching
apt-get update

# launch
python3 sub-systems/repository/source/repository-server.py
