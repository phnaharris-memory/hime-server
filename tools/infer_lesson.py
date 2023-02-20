import os, sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, "..")))

import cv2
import numpy as np
import sqlite3
from tools.utils import (
    cosine_similarity,
    Embedded,
    parse_text_from_html,
    load_vector_from_path_db,
)


data_path = "data/HIME.db"
embedded = Embedded()


def query_thing(query):
    result = []
    sqliteConnection = None

    try:
        sqliteConnection = sqlite3.connect("./data/HIME.db")

        cursor = sqliteConnection.execute(query)
        result = [
            dict((cursor.description[i][0], value) for i, value in enumerate(row))
            for row in cursor.fetchall()
        ]

    except sqlite3.Error as error:
        print("Failed to execute the above query", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()

    return result


def get_baihoc(id=None):
    query = "SELECT * from BAI_HOC"

    if id != None:
        query = query + " WHERE ID_BAIHOC = " + id

    return query_thing(query)


def get_story(id=None):
    query = "SELECT * from STORY"

    if id != None:
        query = query + " WHERE ID_Content = " + id

    return query_thing(query)


def query_search(keyword=""):
    query_baihoc = "SELECT * from BAI_HOC"
    column_baihoc = "ND_baihoc"
    if keyword != None:
        query_baihoc = (
            query_baihoc + " WHERE instr(" + column_baihoc + ", '" + keyword + "') > 0;"
        )

    query_cauchuyen = "SELECT * from STORY"
    column_cauchuyen = "CONTENT"
    if keyword != None:
        query_cauchuyen = (
            query_cauchuyen
            + " WHERE instr("
            + column_cauchuyen
            + ", '"
            + keyword
            + "') > 0;"
        )

    return query_thing(query_baihoc) + query_thing(query_cauchuyen)


def get_relative_lesson(image):
    print("get rela")
    query_vec = embedded.get_vector(image)
    print("get rela1")
    table = []
    sqliteConnection = None
    rs = []
    try:
        sqliteConnection = sqlite3.connect("./data/HIME.db")
        print("get rela2")
        query = "SELECT * from IMAGINE"
        cursor = sqliteConnection.execute(query)
        data = cursor.fetchall()
        print("get rela3")
        print(data)

        for row in data:
            db_embedding_path = "./data/embedding/" + row[3]
            db_vec = load_vector_from_path_db(db_embedding_path)
            score = cosine_similarity(db_vec, query_vec)
            table.append(score)

        max_value = max(table)
        max_index = table.index(max_value)
        rs = data[max_index]

    except sqlite3.Error as error:
        print("Failed to execute the above query", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()

    return rs
