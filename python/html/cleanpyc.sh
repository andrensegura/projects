#! /bin/bash

find /home/andre/projects/python/html/ -type f -name "*.pyc" -exec rm -f {} \;
find /home/andre/domains/keycellar/ -type f -name "*.pyc" -exec rm -f {} \;
