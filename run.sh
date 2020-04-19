#!/bin/bash


LINKS_FILE=test_links.txt
COMPET_FILE=competition.csv
LEADERS_FILE=leaders.csv
TAGS_FILE=tags.json
PASSWORD='' #Your DB password

if [ $# != 1 ]; then
  echo "This script scrap data from kaggle.com and store it to db."
  echo "NB If your database required password, please set up in this script."
  echo "Usage: $0  <start_stage>"
  echo " e.g.: start_stage 1 - get competition links, extract data, create db and store to db"
  echo "       start_stage 2 - extract data, store to db"
  echo "       start_stage 3 - only create db and store to db"
  echo "example:$0 2"
  exit 1;
fi

stage=$1

if [ "$stage" -lt 2 ]; then
    echo "Stage 1"
    python3 get_links.py --links_file $LINKS_FILE
fi

if [ "$stage" -lt 3 ]; then
    echo "Stage 2"
    python3 main.py --links_file $LINKS_FILE --compet_file $COMPET_FILE --leader_file $LEADERS_FILE --tags_file $TAGS_FILE
fi

if [ "$stage" -lt 4 ]; then
    echo "Stage 3"
    mysql -u root --password=$PASSWORD < Kaggle_Scrap.sql
    python3 insert_to_db.py --compet_file $COMPET_FILE --leader_file $LEADERS_FILE --tags_file $TAGS_FILE --password $PASSWORD
fi