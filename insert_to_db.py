import logging
import sys
import pymysql
import csv
import json
import argparse


def connect_to_db(db_name, password):
    '''
    connecting to database
    :return: cursor, db name
    '''

    db = pymysql.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd=password,  # your password
                         db=db_name)  # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()
    logger.info('Connector cursor for database is created')
    return cur, db


def sql_from_line(columns, line, table):
    '''
    insert to table from a dictionary
    :param columns: keys of dictionary with the same names as db columns
    :param line: line in the file
    :param table: name of db table to insert to
    :return: sql command
    '''
    sql_cmd = 'INSERT INTO ' + table + ' (' + columns + ') VALUES ("' + '","'.join(str(x) for x in line.values()) + '");'
    logger.debug(sql_cmd)
    return sql_cmd



def insert_competitions(cursor, csvfilename):
    '''
    insert data to competition table
    :param cursor: cursor
    :param csvfilename: csv file with information about competitions
    :return: None
    '''
    csv_file = open(csvfilename, newline='', encoding="utf-8")
    comp_reader = csv.DictReader(csv_file, delimiter=',')
    columns = ','.join(comp_reader.fieldnames)

    for line in comp_reader:
        sq = sql_from_line(columns, line, 'competitions')
        try:
            cursor.execute(sq)
        except Exception as e:
            logger.warning("Can't insert competition " + line['link'] + str(e))
    logger.info('`Competitions` data is written from csv into db column')


def insert_tags(cursor,jsonfile):
    '''
    insert data to tags table
    :param cursor: cursor
    :param csvfilename: json file with tags
    :return: None
    '''
    tags_dic = json.load(open(jsonfile, encoding="utf-8"))
    tags_set = set([item for sublist in tags_dic.values() for item in sublist])
    for tag in tags_set:
        cursor.execute("INSERT INTO tags (tag) VALUES ('" + tag + "')")
    logger.info('Tags data is written from csv into table `tags`')


def insert_tags_for_compet(cursor, tags_list, competition_id):
    '''
    insert tag_id - competition_id to compet_tags table
    :param cursor: cursor
    :param csvfilename: csv file with information about competitions
    :return: None
    '''
    for tag in tags_list:
        cursor.execute("SELECT tag_id FROM tags WHERE tag = '" + tag + "'")
        tag_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO compet_tags (tag_id, competition_id) VALUES (" + str(tag_id) + "," +
                       str(competition_id) + ")")
    logger.debug('`tag_id`, `competition_id` inserted into table `compet_tags`' + str(competition_id))


def insert_compet_tags(cursor, jsonfile):
    '''
    insert tags to compet_tags table
    :param cursor: cursor
    :param jsonfile: input data
    :return: None
    '''
    tags_dic = json.load(open(jsonfile, encoding="utf-8"))
    for link in tags_dic.keys():
        cursor.execute("SELECT competition_id FROM competitions WHERE link = '" + link + "'")
        if cursor.rowcount == 0:
            logger.warning("Can't get competition from " + link)
            continue
        competition_id = cursor.fetchone()[0]
        insert_tags_for_compet(cursor, tags_dic[link], competition_id)
    logger.info("Competition tags inserted")


def insert_teams(cursor, csv_file):
    '''
    insert team name into teams table
    :param cursor: cursor
    :param csv_file: input data
    :return:None
    '''
    teams = open(csv_file, newline='', encoding="utf-8")
    teams_reader = csv.DictReader(teams, delimiter=',')
    teams_set = set()

    for row in teams_reader:
        if row['team_name'] not in teams_set:
            teams_set.add(row['team_name'])
            try:
                cursor.execute("INSERT INTO teams (name) VALUES ('" + row['team_name'].replace("\'", "\\\'") + "')")
            except Exception as e:
                logger.warning("We don't like teams with slash in names")

            logger.debug('`team_name` inserted into table `teams`' + row['team_name'])
    logger.info("Inserted tags to compet_tags")


def insert_leaderebord(cursor, csv_file):
    '''
    insert data to leadreboard table
    :param cursor: cursor
    :param csv_file: input_file
    :return: None
    '''
    leadereboard = open(csv_file, newline='', encoding="utf-8")
    leadereboard_reader = csv.DictReader(leadereboard, delimiter=',')

    for row in leadereboard_reader:
        try:
            cursor.execute("SELECT team_id FROM teams WHERE name = '" + row['team_name'].replace("\'", "\\\'") + "'")
        except Exception as e:
            logger.warning("We don't like teams with slash in names")
        if cursor.rowcount == 0:
            logger.info('there are no team for the kernel ' + row['link'])
            continue


        team_id = cursor.fetchone()[0]
        cursor.execute("SELECT competition_id FROM competitions WHERE link = '" + row['link'] + "'")
        if cursor.rowcount == 0:
            logger.warning("Can't get competition for " + row['link'])
            continue

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
            logger.warning("can't insert leaderboard entity into table `leaderboard`" + str(row) + str(e))
        logger.info("Inserted `leaderboard entities` into table `leaderboard`")

def insert_kernels(cursor, csvfilename):
    '''
    insert data to kernels table
    :param cursor: cursor
    :param csv_file: input_file
    :return: None
    '''
    csv_file = open(csvfilename, newline='', encoding="utf-8")
    comp_reader = csv.DictReader(csv_file, delimiter=',')

    for row in comp_reader:
        cursor.execute("SELECT competition_id FROM competitions WHERE link = '" + row['link'] + "'")
        if cursor.rowcount == 0:
            logger.info('there are no competition for the kernel ' + row['link'])
            continue
        competition_id = cursor.fetchone()[0]
        del row['link']
        row['competition_id'] = str(competition_id)
        columns = ','.join(row.keys())
        sq = sql_from_line(columns, row, 'kernels')
        try:
            cursor.execute(sq)
        except Exception as e:
            logger.warning("can't insert kernel entity into table 'kernels'`" + str(row) + str(e))
        logger.debug("Inserted `kernels entities` into table `kernels`")


def update_competitions(cursor, csvfilename):
    '''
    update competitions table with information from kaggle API
    :param cursor: cursor
    :param csv_file: input_file
    :return: None
    '''
    csv_file = open(csvfilename, newline='', encoding="utf-8")
    comp_reader = csv.DictReader(csv_file, delimiter=',')

    for row in comp_reader:
        cursor.execute("SELECT competition_id FROM competitions WHERE link = '" + row['link'] + "'")
        if cursor.rowcount == 0:
            logger.info('there are no competition for update ' + row['link'])
            continue
        competition_id = cursor.fetchone()[0]
        sq = "UPDATE competitions SET   got_by_api = 1, category = '" + row['category'] + "', maxDailySubmissions = " +\
        row['maxDailySubmissions'] + " WHERE competition_id = " + str(competition_id)
        try:
            cursor.execute(sq)
        except Exception as e:
            logger.warning("can't insert got_by_api, category to competitions table'`" + str(row) + str(e))
        logger.debug("Inserted got_by_api, category to competitions table")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Insert to database')

    parser.add_argument('--compet_file', type=str, help='File with data about competition for "competition" table',
                        default='kaggle_competition.csv')
    parser.add_argument('--tags_file', type=str, help='File with competition tags for "tags" and "compet_tags" tables',
                        default='tags.json')
    parser.add_argument('--leader_file', type=str, help='File with data from competition leaderboard to build\
                        "leadeboard" and "teams" tables', default='kaggle_leaders.csv')

    parser.add_argument('--db_name', type=str, help='Name of database to build', default='KaggleITC')

    parser.add_argument('--password', type=str, help='Password to database', default='')

    parser.add_argument('--kernels_file', type=str, help='Where to store kernelsfrom competition page',
                        default='kernels_file.csv')

    parser.add_argument('--competitions_api_file', type=str, help='Where to store data for competitons from API',
                        default='competitions_api_file.csv')

    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler('insert_to_db.log')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(logging.StreamHandler(sys.stdout))

    cursor, db = connect_to_db(args.db_name, args.password)
    insert_competitions(cursor, args.compet_file)
    db.commit()
    insert_tags(cursor, args.tags_file)
    db.commit()
    insert_compet_tags(cursor, args.tags_file)
    db.commit()

    insert_teams(cursor,args.leader_file)
    db.commit()

    insert_leaderebord(cursor, args.leader_file)
    db.commit()

    insert_kernels(cursor, args.kernels_file)
    db.commit()

    update_competitions(cursor, args.competitions_api_file)
    db.commit()

    logger.info('Main in `insert_to_db.py is finished')
