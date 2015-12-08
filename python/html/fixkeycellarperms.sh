#! /bin/bash

cd /home/andre/domains/keycellar/
find ./ -type d -exec chmod 755 {} \;
find ./ -type f -name "*.cgi"  -exec chmod 750 {} \;
find ./ -type f -name "*.css"  -exec chmod 644 {} \;
find ./ -type f -name "*.py*" -o -name "*.html" -exec chmod 600 {} \;

