import os, sys

__dir__ = os.path.dirname(os.path.abspath(__file__))
sys.path.append(__dir__)
sys.path.append(os.path.abspath(os.path.join(__dir__, "..")))

import cv2
import numpy as np
import sqlite3
from tools.utils import cosine_similarity, Embedded, parse_text_from_html, load_vector_from_path_db


data_path = 'data/HIME.db'
embedded = Embedded()

def get_all_lessons():
    rs = []
    try:
        sqliteConnection = sqlite3.connect('./data/HIME.db')
        query = "SELECT * from STORY"
        cursor = sqliteConnection.execute(query)
        for row in cursor:
            text = parse_text_from_html(row[4])
            rs.append(text)
    except sqlite3.Error as error:
        print("Failed to execute the above query", error)
    
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    return rs

def get_story_by_id(id_story):
    return 'not yet implement :v'

def get_relative_lesson(image):
    query_vec =  embedded.get_vector(image)
    table = []
    try:
        sqliteConnection = sqlite3.connect('./data/HIME.db')
        query = "SELECT * from IMAGINE"
        cursor = sqliteConnection.execute(query)
        data = cursor.fetchall()
        for row in data:
            db_vec = load_vector_from_path_db(row[3])
            score = cosine_similarity(db_vec, query_vec)
            table.append(score)

        min_value = min(table)
        min_index = table.index(min_value)

        rs = data[min_index]
        
    except sqlite3.Error as error:
        print("Failed to execute the above query", error)
    
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    
    return rs