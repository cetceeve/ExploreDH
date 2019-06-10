import sqlite3
from sqlite3 import Error
import sys_io_json as io


def create_db(db_file, dictPerson, dictOrga, dictLocation, dictArticle, dictKeyword):
    # create a database connection to a SQLite database
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    cursor = conn.cursor()
    _commitKeywordDictionary(conn, cursor, _getValuesAsTuples(dictKeyword))

    for row in cursor.execute('SELECT * FROM keyword LIMIT 10'):
        print(row)

    conn.close()


def _commitKeywordDictionary(conn, curser, keywords):
    curser.execute(
        "CREATE TABLE keyword (id TEXT PRIMARY KEY, text TEXT, frequency INTEGER)")
    curser.executemany(
        "INSERT INTO keyword VALUES (?,?,?)", keywords)
    conn.commit()


def _getValuesAsTuples(dictonary):
    return [tuple(el.values()) for el in dictonary.values()]
