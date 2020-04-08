
import pymysql
import csv

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
    csv_file = open(csvfilename, newline='', encoding = "utf-8")
    comp_reader = csv.DictReader(csv_file, delimiter=',')
    columns = ','.join(comp_reader.fieldnames)

    for line in comp_reader:
        sq = sql_from_line(columns, line)
        cursor.execute(sq)







if __name__ == '__main__':
    cursor, db = connect_to_db()
    insert_competitions(cursor, 'kaggle_competition.csv')
    db.commit()