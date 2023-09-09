from logging import currentframe
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


default_img_host = "daylacaiimageendpoint"
default_avatar = "avatar.png"
current_img_host = os.getenv("NGROK_ENDPOINT", default="") + "/data"


def ser_baihoc(baihoc):
    print(baihoc)
    res = {}

    res["id"] = baihoc["ID_BAIHOC"]
    res["title"] = baihoc["Title_baihoc"]
    res["shorttext"] = baihoc["short_text"]
    res["html"] = baihoc["ND_baihoc"]
    res["avatar"] = (
        current_img_host
        + "/images/"
        + (default_avatar if (len(baihoc["avatar"]) == 0) else baihoc["avatar"])
    )

    try:
        res["html"] = res["html"].replace(default_img_host, current_img_host)
    except Exception as e:
        pass

    return res


def get_baihoc(id=None):
    query = "SELECT * from BAI_HOC"

    if id != None:
        query = query + " WHERE ID_BAIHOC = " + id

    res_query = query_thing(query)
    res = []

    for baihoc in res_query:
        baihoc = ser_baihoc(baihoc)
        res.append(baihoc)

    return res


def ser_story(story):
    res = {}

    res["id"] = story["ID_Content"]
    res["title"] = story["TITLE"]
    res["shorttext"] = story["short_text"]
    res["html"] = story["CONTENT"]
    res["avatar"] = (
        current_img_host
        + "/images/"
        + (default_avatar if (len(story["avatar"]) == 0) else story["avatar"])
    )

    try:
        res["html"] = res["html"].replace(default_img_host, current_img_host)
    except Exception as e:
        pass

    return res


def get_story(id=None):
    query = "SELECT * from STORY"

    if id != None:
        query = query + " WHERE ID_Content = " + id

    res_query = query_thing(query)
    res = []

    for story in res_query:
        story = ser_story(story)
        res.append(story)

    return res


def query_search(keyword=""):
    query_baihoc = "SELECT * from BAI_HOC"
    column_baihoc = "ND_baihoc"
    if keyword != None:
        query_baihoc = (
            query_baihoc + " WHERE INSTR(" + column_baihoc + ", '" + keyword + "') > 0;"
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

    res = []

    res_query_baihoc = query_thing(query_baihoc)
    res_query_cauchuyen = query_thing(query_cauchuyen)

    for baihoc in res_query_baihoc:
        baihoc = ser_baihoc(baihoc)
        res.append(baihoc)

    for story in res_query_cauchuyen:
        story = ser_story(story)
        res.append(story)

    return res


def get_story_by_image(id=None):
    query = "SELECT * from STORY"

    if id != None:
        query = query + " WHERE ID_IMG = " + str(id)

    res_query = query_thing(query)
    res = []

    for story in res_query:
        story = ser_story(story)
        res.append(story)

    return res


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
        rs = data[max_index][0]

    except sqlite3.Error as error:
        print("Failed to execute the above query", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()

    return rs
