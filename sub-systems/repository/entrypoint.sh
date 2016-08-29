#!/bin/bash
apt-get update

cd /data/source
python3 repository-server.py
