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
    _commitToTable(conn, cursor, "article", _getArticlesAsTupleList(dictArticle))
    conn.close()


def _createTables(conn, curser):
    print("creating tables...")
    curser.execute("CREATE TABLE keyword (id TEXT PRIMARY KEY, text TEXT, frequency INTEGER)")
    curser.execute("CREATE TABLE location (id TEXT PRIMARY KEY, name TEXT, lat TEXT, lon TEXT)")
    curser.execute("CREATE TABLE orga (id TEXT PRIMARY KEY, name TEXT, location REFERENCES location(id))")
    curser.execute("CREATE TABLE person (id TEXT PRIMARY KEY, firstname TEXT, lastname TEXT, orga REFERENCES orga(id))")
    curser.execute("CREATE TABLE email (id TEXT PRIMARY KEY, email TEXT, person REFERENCES author(id))")
    curser.execute("CREATE TABLE article (id TEXT PRIMARY KEY, title TEXT, abstract TEXT)")
    conn.commit()


def _getPeopleAsTupleList(dictPerson):
    return [(person["id"], person["firstName"], person["lastName"], person["orga"]) for person in dictPerson.values()]


def _getEmailsAsTupleList(dictPerson):
    return [(str(uuid.uuid1()), email, key) for key, person in dictPerson.items() for email in person["email"]]


def _getArticlesAsTupleList(dictArticle):
    return [(article["id"], article["title"], article["abstract"]) for article in dictArticle.values()]
# {"id": "4ff9ad92-8bb6-11e9-8a21-f46d04af11fe", "title": "VAnnotatoR: Ein Werkzeug zur Annotation multimodaler Netzwerke in dreidimensionalen virtuellen Umgebungen", "abstract": "ASSA!",
# "keywords": ["4ff9d49c-8bb6-11e9-b565-f46d04af11fe", "4ff9d49d-8bb6-11e9-88c0-f46d04af11fe", "4ff9d49e-8bb6-11e9-a816-f46d04af11fe", "4ff9d49f-8bb6-11e9-ac2e-f46d04af11fe", "4ff9d4a0-8bb6-11e9-837a-f46d04af11fe", "4ff9d4a1-8bb6-11e9-b91e-f46d04af11fe", "4ff9d4a2-8bb6-11e9-a047-f46d04af11fe", "4ff9d4a3-8bb6-11e9-a0c8-f46d04af11fe", "4ff9d4a4-8bb6-11e9-afda-f46d04af11fe", "4ff9d4a5-8bb6-11e9-9fd4-f46d04af11fe", "4ff9d4a6-8bb6-11e9-88ec-f46d04af11fe", "4ff9d4a7-8bb6-11e9-884f-f46d04af11fe"],
# "authors": ["person__abrami-em-uni-frankfurt-de", "person__s2717197-stud-uni-frankfurt-de", "person__mehler-em-uni-frankfurt-de"]},


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
