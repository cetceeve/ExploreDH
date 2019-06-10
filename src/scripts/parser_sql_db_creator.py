import sqlite3
from sqlite3 import Error
import uuid
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
    _commitKeywords(conn, cursor, dictKeyword)
    _commitLocations(conn, cursor, dictLocation)
    _commitOrgas(conn, cursor, dictOrga)
    _commitPeople(conn, cursor, dictPerson)
    _commitEmails(conn, cursor, dictPerson)
    conn.close()


def _createTables(conn, curser):
    print("creating tables...")
    curser.execute("CREATE TABLE keyword (id TEXT PRIMARY KEY, text TEXT, frequency INTEGER)")
    curser.execute("CREATE TABLE location (id TEXT PRIMARY KEY, name TEXT, lat TEXT, lon TEXT)")
    curser.execute("CREATE TABLE orga (id TEXT PRIMARY KEY, name TEXT, location REFERENCES location(id))")
    curser.execute("CREATE TABLE person (id TEXT PRIMARY KEY, firstName TEXT, lastName TEXT, orga REFERENCES orga(id))")
    curser.execute("CREATE TABLE email (id TEXT PRIMARY KEY, email TEXT, person REFERENCES author(id))")
    conn.commit()


def _commitKeywords(conn, curser, dictKeyword):
    print("writing keywords...")
    keywords = _getValuesAsTuples(dictKeyword)
    curser.executemany("INSERT INTO keyword VALUES (?,?,?)", keywords)
    conn.commit()


def _commitLocations(conn, cursor, dictLocation):
    print("writing locations...")
    locations = _getValuesAsTuples(dictLocation)
    cursor.executemany("INSERT INTO location VALUES (?,?,?,?)", locations)
    conn.commit()


def _commitOrgas(conn, cursor, dictOrga):
    print("writing orgas...")
    orgas = _getValuesAsTuples(dictOrga)
    cursor.executemany("INSERT INTO orga VALUES (?,?,?)", orgas)
    conn.commit()


def _commitPeople(conn, cursor, dictPerson):
    print("writing people...")
    people = [(person["id"], person["firstName"], person["lastName"], person["orga"]) for person in dictPerson.values()]
    cursor.executemany("INSERT INTO person VALUES (?,?,?,?)", people)
    conn.commit()


def _commitEmails(conn, cursor, dictPerson):
    print("writing emails...")
    emails = [(str(uuid.uuid1()), email, key) for key, person in dictPerson.items() for email in person["email"]]
    cursor.executemany("INSERT INTO email VALUES (?,?,?)", emails)
    conn.commit()


def _getValuesAsTuples(dictonary):
    return [tuple(el.values()) for el in dictonary.values()]
