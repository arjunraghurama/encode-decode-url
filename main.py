import SessionState
import streamlit as st
import random
import sqlite3 as sl
from urllib.parse import quote
import datetime
import sqlite3 as sl

st.set_page_config(
        page_title="Encode Decode",
        page_icon="❤️",
        layout="centered"
    )


con = sl.connect('data.db')

ENCODE_LENGTH = 6
encode_char_choice = "0123456789abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWXY"

url_or_code = st.text_input("URL or Code")
_,en,_,de,_ = st.beta_columns([4,1,1,1,5])

def exits_in_LTOS(long_url) -> bool:
    query = "SELECT code FROM LTOS where url='{}'".format(long_url)
    with con:
        data = con.execute(query)
        for _ in data:
            return True
    return False

def exits_in_STOL(short_url) -> bool:
    query = "SELECT url FROM STOL where code='{}'".format(short_url)
    with con:
        data = con.execute(query)
        for _ in data:
            return True
    return False

def get_code(long_url):
    query = "SELECT code FROM LTOS where url='{}'".format(long_url)
    with con:
        data = con.execute(query)
        for row in data:
            return(row[0]) 

def get_url(code):
    query = "SELECT url FROM STOL where code='{}'".format(code)
    with con:
        data = con.execute(query)
        for row in data:
            return(row[0]) 
    return None

def save_to_LTOS(url,code, time):
    sql = 'INSERT INTO LTOS (url, code, time) values(?, ?, ?)'
    data = [
        (url,code, time)
    ]
    with con:
        con.executemany(sql, data)

def save_to_STOL(code, url, time):
    sql = 'INSERT INTO STOL (code, url, time) values(?, ?, ?)'
    data = [
        (code,url, time)
    ]
    with con:
        con.executemany(sql, data)

def encode(long_url : str) -> str:
    long_url = quote(long_url, safe=":/?=%&.")
    while(not exits_in_LTOS(long_url)):
        code = "".join([ random.choice(encode_char_choice) for _ in range(ENCODE_LENGTH)])
        if not exits_in_STOL(code):
            time = datetime.date.today().strftime("%Y%m%d")
            save_to_LTOS(long_url,code, time)
            save_to_STOL(code,long_url, time)
    return get_code(long_url)

def decode(short_url : str) -> str:
    short_url = quote(short_url)
    url = get_url(short_url) 
    if url:
        return url
    else:
        raise KeyError

if(en.button("Encode")):
    code = encode(url_or_code)
    st.markdown(""" <p><span>URL has been encoded as : {}</p>""".format(code),unsafe_allow_html=True)

if(de.button("Decode")):
    try:
        url = decode(url_or_code)
        st.markdown(""" <p><span>Decoded URL is : </span><a href="{}">{}</a></p>""".format(url,url),unsafe_allow_html=True)
    except KeyError:
        er = "404 Oh Snap!! We are unable to find the URL for you. 😞"
        st.markdown(""" <p><span align="center">{}</span></p>""".format(er),unsafe_allow_html=True)

def clear_cache():
    time = (datetime.date.today() - datetime.timedelta(days=30)).strftime("%Y%m%d")
    with con:
        query_l = "DELETE FROM LTOS WHERE time < {}".format(time)
        query_s = "DELETE FROM STOL WHERE time < {}".format(time)
        con.execute(query_l)
        con.execute(query_s)
clear_cache()
