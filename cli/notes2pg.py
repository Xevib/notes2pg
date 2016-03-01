#!/usr/bin/env python
import psycopg2
from lxml import etree
import sys
import datetime


def create_schema(con):
    sql_drop = """
          DROP TABLE IF EXISTS planet_osm_notes;
          DROP TABLE IF EXISTS planet_osm_notes_comments;
        """
    query = """
        CREATE TABLE planet_osm_notes(
        id integer NOT NULL PRIMARY KEY,
        geom geometry NOT NULL,
        created_at timestamp,
        closed_at timestamp
        );
        CREATE TABLE planet_osm_notes_comments(
        note_id integer REFERENCES planet_osm_notes (id),
	    action text,
	    "timestamp" timestamp,
	    uid integer,
	    "user" text,
	    comment text
        );
        """
    cursor = con.cursor()
    cursor.execute(sql_drop)
    cursor.execute(query)
    cursor.close()


def load(filename, user=None, database=None, password=None, host=None,create=False):
    con = psycopg2.connect(database=database, user=user, password=password, host=host)
    if create:
        create_schema(con)
    print('Loading file')
    tree = etree.parse(filename)
    root = tree.getroot()
    cur = con.cursor()
    projection = str(4326)
    sql_insert_note = """
        INSERT INTO planet_osm_notes VALUES (%(id)s,
        ST_SETSRID(ST_MAKEPOINT(%(lat)s,%(lon)s),%(projection)s),%(created_at)s,%(closed_at)s)
    """
    sql_insert_comment = """
        INSERT INTO planet_osm_notes_comments VALUES(%(note_id)s,%(action)s,%(timestamp)s,%(uid)s,%(user)s,%(comment)s)
    """
    print('Writing notes')
    for note in root:
        data_note = {'projection':projection,'closed_at':None,'created_at':None}
        data_note['id'] = int(note.get('id'))
        data_note['lat'] = note.get('lat')
        data_note['lon'] = note.get('lon')
        if note.get('closed_at'):
            data_note['closed_at'] = datetime.datetime.strptime(note.get('closed_at'), "%Y-%m-%dT%H:%M:%SZ")
        if note.get('created_at'):
            data_note['created_at'] = datetime.datetime.strptime(note.get('created_at'), "%Y-%m-%dT%H:%M:%SZ")
        cur.execute(sql_insert_note, data_note)
        for comment in note:
            data_comment = {'action':comment.get('action'),'timestamp':comment.get('timestamp'),'uid':comment.get('uid'),'comment':comment.text,'note_id':data_note['id'],'user':comment.get('user')}
            cur.execute(sql_insert_comment,data_comment)
    con.commit()
    con.close()


def help():
    print('Usage:')
    print('\tnotes2pg planet-notes.osn [options]\n')
    print('Options:')
    print('\t-u Postgres username')
    print('\t-d Postgres database')
    print('\t-w Postgres password')
    print('\t-H Postgres host')
    print('\t-c create the table schema')


def main():
    x = 2
    if len(sys.argv)<2:
        help()
    else:
        filename = sys.argv[1]
        create = False
        while x < len(sys.argv):
            arg = sys.argv[x]
            if arg == '-u':
                user = sys.argv[x+1]
                x += 1
            elif arg == '-c':
                create = True
            elif arg == '-d':
                database = sys.argv[x+1]
                x += 1
            elif arg == '-w':
                password = sys.argv[x+1]
                x += 1
            elif arg == '-H':
                host = sys.argv[x+1]
                x += 1
            elif arg == '-a':
                append = sys.argv[x+1]
                x += 1
            elif arg == '--help':
                help()
                exit()
            else:
                print('Invalid option')
                help()
            x += 1
        load(filename, user, database, password, host, create)


if __name__ == "__main__":
    main()
