import sqlite3
from sqlite3 import Error
import uuid
import sys_io_json as io


def create_db(db_file, dictPerson, dictOrga, dictLocation, dictArticle, dictKeyword):
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    cursor = conn.cursor()
    _createTables(conn, cursor)
    _commitToTable(conn, cursor, "keyword", _getValuesAsTupleList(dictKeyword))
    _commitToTable(conn, cursor, "location", _getValuesAsTupleList(dictLocation))
    _commitToTable(conn, cursor, "orga", _getValuesAsTupleList(dictOrga))
    _commitToTable(conn, cursor, "person", _getPeopleAsTupleList(dictPerson))
    _commitToTable(conn, cursor, "email", _getEmailsAsTupleList(dictPerson))
    conn.close()


def _createTables(conn, curser):
    print("creating tables...")
    curser.execute("CREATE TABLE keyword (id TEXT PRIMARY KEY, text TEXT, frequency INTEGER)")
    curser.execute("CREATE TABLE location (id TEXT PRIMARY KEY, name TEXT, lat TEXT, lon TEXT)")
    curser.execute("CREATE TABLE orga (id TEXT PRIMARY KEY, name TEXT, location REFERENCES location(id))")
    curser.execute("CREATE TABLE person (id TEXT PRIMARY KEY, firstname TEXT, lastname TEXT, orga REFERENCES orga(id))")
    curser.execute("CREATE TABLE email (id TEXT PRIMARY KEY, email TEXT, person REFERENCES author(id))")
    conn.commit()


def _getPeopleAsTupleList(dictPerson):
    return [(person["id"], person["firstName"], person["lastName"], person["orga"]) for person in dictPerson.values()]


def _getEmailsAsTupleList(dictPerson):
    return [(str(uuid.uuid1()), email, key) for key, person in dictPerson.items() for email in person["email"]]


def _getValuesAsTupleList(dictonary):
    return [tuple(el.values()) for el in dictonary.values()]


def _commitToTable(conn, cursor, table, data):
    print("commiting {}...".format(table))
    insertString = "INSERT INTO {table} VALUES ({qms})".format(table=table, qms=_qmsBuilder(len(data[0])))
    cursor.executemany(insertString, data)
    conn.commit()


def _qmsBuilder(quantity):
    res = ""
    for i in range(quantity):
        res += "?,"
    return res[:-1]
