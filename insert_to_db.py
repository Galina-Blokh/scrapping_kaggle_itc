import logging
import sys

import pymysql
import csv
import json
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('insert_to_db.log')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(logging.StreamHandler(sys.stdout))

def connect_to_db():

    db = pymysql.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="1!Chagall",  # your password
                         db="KaggleITC")  # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()
    logger.info('Connector cur for db is created')
    return cur, db


def sql_from_line(columns, line, table):
    sql_cmd = 'INSERT INTO ' + table + ' (' + columns + ') VALUES ("' + '","'.join(str(x) for x in line.values()) + '");'
    print(sql_cmd)
    logger.info('The column added into  table')
    return sql_cmd



def insert_competitions(cursor, csvfilename):
    csv_file = open(csvfilename, newline='', encoding="utf-8")
    comp_reader = csv.DictReader(csv_file, delimiter=',')
    columns = ','.join(comp_reader.fieldnames)

    for line in comp_reader:
        sq = sql_from_line(columns, line, 'competitions')
        cursor.execute(sq)
    logger.info('`Competitions` data is written from csv into db column')


def insert_tags(cursor,jsonfile):
    tags_dic = json.load(open(jsonfile, encoding="utf-8"))
    tags_set = set([item for sublist in tags_dic.values() for item in sublist])
    for tag in tags_set:
        cursor.execute("INSERT INTO tags (tag) VALUES ('" + tag + "')")
    logger.info('Tags data is written from csv into table `tags`')


def insert_tags_for_compet(cursor, tags_list, competition_id):
    for tag in tags_list:
        cursor.execute("SELECT tag_id FROM tags WHERE tag = '" + tag + "'")
        tag_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO compet_tags (tag_id, competition_id) VALUES (" + str(tag_id) + "," +
                       str(competition_id) + ")")
    logger.info('`tag_id`, `competition_id` inserted into table `compet_tags`')



def insert_compet_tags(cursor,jsonfile):
    tags_dic = json.load(open(jsonfile, encoding="utf-8"))
    for link in tags_dic.keys():
        cursor.execute("SELECT competition_id FROM competitions WHERE link = '" + link + "'")
        competition_id = cursor.fetchone()[0]
        insert_tags_for_compet(cursor,tags_dic[link], competition_id)


def insert_teams(cursor, csv_file):
    teams = open(csv_file, newline='', encoding="utf-8")
    teams_reader = csv.DictReader(teams, delimiter=',')
    teams_set = set()

    for row in teams_reader:
        if row['team_name'] not in teams_set:
            teams_set.add(row['team_name'])
            cursor.execute("INSERT INTO teams (name) VALUES ('" + row['team_name'].replace("\'", "\\\'") + "')")
        logger.info('`team_name` inserted into table `teams`')


def insert_leaderebord(cursor, csv_file):
    leadereboard = open(csv_file, newline='', encoding="utf-8")
    leadereboard_reader = csv.DictReader(leadereboard, delimiter=',')

    for row in leadereboard_reader:
        cursor.execute("SELECT team_id FROM teams WHERE name = '" + row['team_name'].replace("\'", "\\\'") + "'")
        team_id = cursor.fetchone()[0]
        cursor.execute("SELECT competition_id FROM competitions WHERE link = '" + row['link'] + "'")
        competition_id = cursor.fetchone()[0]
        del row['team_name']
        del row['link']
        row['competition_id'] = str(competition_id)
        row['team_id'] = str(team_id)
        columns = ','.join(row.keys())
        sq = sql_from_line(columns, row, 'leaderboard')
        try:
            cursor.execute(sq)
        except Exception as e:
            print("can't insert leaderboard entity")
            logger.exception("can't insert leaderboard entity into table `leaderboard`")
        logger.info("Inserted `leaderboard entity` into table `leaderboard`")


if __name__ == '__main__':
    cursor, db = connect_to_db()
    insert_competitions(cursor, 'kaggle_competition.csv')
    db.commit()
    insert_tags(cursor, 'tags.json')
    db.commit()
    insert_compet_tags(cursor, 'tags.json')
    db.commit()

    insert_teams(cursor, 'kaggle_leaders.csv')
    db.commit()

    insert_leaderebord(cursor, 'kaggle_leaders.csv')
    db.commit()
    logger.info('Main in `incert_to_db.py is finished')