from flask import request
from database import engine
from sqlalchemy import text
import pandas as pd
import API
import cleanlink as cl
import os
import io

SELECT_COUNT_QUERY = text('SELECT COUNT(*) FROM main') #This is the query that checks the number of rows in the table

#This function is used to check if the table has more than 5 rows, if it does, it deletes the oldest row, and then returns the 5 most recent searches
def get_existing_link_result(conn, link):
    existing_link_query = text("SELECT COUNT(*) FROM main WHERE Link = (:link)")
    return conn.execute(existing_link_query, {"link": link}).fetchone()[0]

def insert_link(conn, link):
    update_query = text("INSERT INTO main (Link) VALUES (:link)")
    conn.execute(update_query, {"link": link})

def update_link_json_data(conn, link, apiidx):
    ss = text("UPDATE main SET jdata = (:json_data) WHERE link = (:link)")
    if apiidx == 1:
        json_data = API.search(API.get_links_in_reddit_post(link), API.reddit, apiidx = 1)
    elif apiidx == 2:
        json_data = API.search(link, API.reddit, apiidx = 1)
    else:
        json_data = API.search(link, API.reddit, apiidx = 0)
    jdata = pd.DataFrame(json_data).to_json(orient="records")
    conn.execute(ss, {"json_data": jdata, "link": link})

def get_jdata(conn, link):
    jdata_query = text("SELECT jdata FROM main WHERE link = (:link)")
    jdata_result = conn.execute(jdata_query, {"link": link}).fetchone()
    if jdata_result and jdata_result[0]:
        return pd.read_json(io.StringIO((jdata_result[0])))

def if_link_is_post(link):
    return 'reddit.com/r/' in link and '/comments/' in link

def delete_old_entries(conn):
    result = conn.execute(SELECT_COUNT_QUERY).fetchone()[0]
    if result > 5:
        conn.execute(text("DELETE FROM main WHERE created_at = (SELECT m.created_at FROM (SELECT created_at FROM main ORDER BY created_at LIMIT 1) m);"))

def insert_or_update_link(conn, link):
    existing_link_result = get_existing_link_result(conn, link)
    extension = os.path.basename(link)
    root, ext = os.path.splitext(extension)
    if existing_link_result == 0:
        if if_link_is_post(link):
            apiidx = 1
        elif ext:
            apiidx = 2
            update_link_json_data(conn, link.replace(extension, root), apiidx)
        else:
            apiidx = 0
        insert_link(conn, link)
        update_link_json_data(conn, link, apiidx)

def get_existing_link_result(conn, link):
    return conn.execute(text("SELECT COUNT(*) FROM main WHERE link = '{}'".format(link))).fetchone()[0]

def past_searches(aridx, pr):
    link = request.args.get('q') if pr == 'GET' else request.form.get('q')
    with engine.connect() as conn:
        if aridx == 0:
            delete_old_entries(conn)
            return conn.execute(text('SELECT link FROM main')).fetchall()
        elif aridx == 1:
            insert_or_update_link(conn, link)
            result = conn.execute(SELECT_COUNT_QUERY).fetchone()[0]
            if result > 5:
                delete_old_entries(conn)
            if result < 5:
                return conn.execute(text('SELECT link FROM main')).fetchall()
        else:
            return get_jdata(conn, link)
