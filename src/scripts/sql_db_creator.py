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
    _createTables(conn, cursor)
    _commitKeywordDictionary(conn, cursor, dictKeyword)
    _commitLocationDictionary(conn, cursor, dictLocation)
    _commitOrgaDictionary(conn, cursor, dictOrga)
    conn.close()


def _createTables(conn, curser):
    print("creating tables...")
    curser.execute(
        "CREATE TABLE keyword (id TEXT PRIMARY KEY, text TEXT, frequency INTEGER)")
    curser.execute(
        "CREATE TABLE location (id TEXT PRIMARY KEY, name TEXT, lat TEXT, lon TEXT)")
    curser.execute(
        "CREATE TABLE orga (id TEXT PRIMARY KEY, name TEXT, location REFERENCES location(id))")


def _commitKeywordDictionary(conn, curser, dictKeyword):
    print("writing keywords...")
    keywords = _getValuesAsTuples(dictKeyword)
    curser.executemany("INSERT INTO keyword VALUES (?,?,?)", keywords)
    conn.commit()


def _commitLocationDictionary(conn, cursor, dictLocation):
    print("writing locations...")
    locations = _getValuesAsTuples(dictLocation)
    cursor.executemany("INSERT INTO location VALUES (?,?,?,?)", locations)
    conn.commit()


def _commitOrgaDictionary(conn, cursor, dictOrga):
    print("writing orgas...")
    orgas = _getValuesAsTuples(dictOrga)
    cursor.executemany("INSERT INTO orga VALUES (?,?,?)", orgas)
    conn.commit()


def _getValuesAsTuples(dictonary):
    return [tuple(el.values()) for el in dictonary.values()]
