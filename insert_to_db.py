
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
    print(sql_cmd)
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
        cursor.execute(sq)


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


def insert_tags_for_compet(cursor, tags_list, competition_id):
    '''
    insert data to compet_tags table
    :param cursor: cursor
    :param csvfilename: csv file with information about competitions
    :return: None
    '''
    for tag in tags_list:
        cursor.execute("SELECT tag_id FROM tags WHERE tag = '" + tag + "'")
        tag_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO compet_tags (tag_id, competition_id) VALUES (" + str(tag_id) + "," +
                       str(competition_id) + ")")



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


    args = parser.parse_args()

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