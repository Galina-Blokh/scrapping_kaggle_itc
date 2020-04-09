
import pymysql
import csv
import json

def connect_to_db():

    db = pymysql.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="1!Chagall",  # your password
                         db="KaggleITC")  # name of the data base

    # you must create a Cursor object. It will let
    #  you execute all the queries you need
    cur = db.cursor()
    return cur, db


def sql_from_line(columns, line):
    sql_cmd = 'INSERT INTO competitions (' + columns + ') VALUES ("' + '","'.join(str(x) for x in line.values()) + '");'
    print(sql_cmd)
    return sql_cmd



def insert_competitions(cursor, csvfilename):
    csv_file = open(csvfilename, newline='', encoding="utf-8")
    comp_reader = csv.DictReader(csv_file, delimiter=',')
    columns = ','.join(comp_reader.fieldnames)

    for line in comp_reader:
        sq = sql_from_line(columns, line)
        cursor.execute(sq)


def insert_tags(cursor,jsonfile):
    tags_dic = json.load(open(jsonfile, encoding="utf-8"))
    tags_set = set([item for sublist in tags_dic.values() for item in sublist])
    for tag in tags_set:
        cursor.execute("INSERT INTO tags (tag) VALUES ('" + tag + "')")


def insert_tags_for_compet(cursor, tags_list, competition_id):
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





if __name__ == '__main__':
    cursor, db = connect_to_db()
    insert_competitions(cursor, 'kaggle_competition.csv')
    db.commit()
    insert_tags(cursor, 'tags.json')
    db.commit()
    insert_compet_tags(cursor, 'tags.json')
    db.commit()