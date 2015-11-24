#! /bin/bash

while getopts ":r :h" opt; do
  case $opt in
    r)
      echo "-r was triggered!" >&2
      cargo build --release
      ;;
    h)
      echo "+------------------------------------------------------------------------+"
      echo "|HELP:                                                                   |"
      echo "|------------------------------------------------------------------------|"
      echo "|Copies the release version of this program to drago.ninja/index.cgi     |"
      echo "|Add '-r' to rebuild the release brinary.                                |"
      echo "+------------------------------------------------------------------------+"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      ;;
  esac
done


cp -p target/release/index /home/andre/domains/keycellar/index.cgi
