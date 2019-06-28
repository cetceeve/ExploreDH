import sqlite3
from sqlite3 import Error
import uuid
import sys_io_json as io


def create_db(db_file, dictPerson, dictOrga, dictLocation, dictArticle, dictKeyword):
    try:
        conn = sqlite3.connect(db_file)
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
    _commitToTable(conn, cursor, "article_person_link", _getArticleAuthorLink(dictArticle))
    _commitToTable(conn, cursor, "article_keyword_link", _getArticleKeywordLink(dictArticle))
    conn.close()


def _createTables(conn, curser):
    print("creating tables...")
    curser.execute("CREATE TABLE keyword (id TEXT PRIMARY KEY, text TEXT, frequency INTEGER)")
    curser.execute("CREATE TABLE location (id TEXT PRIMARY KEY, name TEXT, lat TEXT, lon TEXT)")
    curser.execute("CREATE TABLE orga (id TEXT PRIMARY KEY, name TEXT, location REFERENCES location(id), lat TEXT, lon TEXT)")
    curser.execute("CREATE TABLE person (id TEXT PRIMARY KEY, firstname TEXT, lastname TEXT, orga REFERENCES orga(id))")
    curser.execute("CREATE TABLE email (id TEXT PRIMARY KEY, email TEXT, person REFERENCES person(id))")
    curser.execute("CREATE TABLE article (id TEXT PRIMARY KEY, title TEXT, abstract TEXT)")
    curser.execute("CREATE TABLE article_person_link (article_id TEXT , person_id TEXT, PRIMARY KEY (article_id, person_id), FOREIGN KEY(article_id) REFERENCES article(id), FOREIGN KEY(person_id) REFERENCES person(id))")
    curser.execute("CREATE TABLE article_keyword_link (article_id TEXT , keyword_id TEXT, PRIMARY KEY (article_id, keyword_id), FOREIGN KEY(article_id) REFERENCES article(id), FOREIGN KEY(keyword_id) REFERENCES keyword(id))")
    conn.commit()


def _getPeopleAsTupleList(dictPerson):
    return [(person["id"], person["firstName"], person["lastName"], person["orga"]) for person in dictPerson.values()]


def _getEmailsAsTupleList(dictPerson):
    return [(hash(email), email, personID) for personID, person in dictPerson.items() for email in person["email"]]


def _getArticlesAsTupleList(dictArticle):
    return [(article["id"], article["title"], article["abstract"]) for article in dictArticle.values()]


def _getArticleAuthorLink(dictArticle):
    return [(articleID, personID) for articleID, article in dictArticle.items() for personID in article["authors"]]


def _getArticleKeywordLink(dictArticle):
    return [(articleID, keywordID) for articleID, article in dictArticle.items() for keywordID in article["keywords"]]


def _getValuesAsTupleList(dictonary):
    return [tuple(el.values()) for el in dictonary.values()]


def _commitToTable(conn, cursor, table, data):
    print("commiting {}...".format(table))
    insertString = "INSERT INTO {table} VALUES ({qms})".format(table=table, qms=_qmsBuilder(len(data[0])))
    cursor.executemany(insertString, data)
    conn.commit()


def _qmsBuilder(quantity):
    res = "?," * quantity
    return res[:-1]
