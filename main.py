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

#  SQLite DB connection
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
    #  Check for valid URL
    parse_result = urlparse(long_url)
    if not parse_result.scheme and not parse_result.netloc:
        er = "400 Oh Snap!! We are unable to parse the URL. 😞"
        st.markdown(""" <p><span align="center">{}</span></p>""".format(er),unsafe_allow_html=True)
        return None

    long_url = quote(long_url, safe=":/?=%&.-_")
    while(not exits_in_LTOS(long_url)):
        code = "".join([ random.choice(encode_char_choice) for _ in range(ENCODE_LENGTH)])
        if not exits_in_STOL(code):
            time = datetime.date.today().strftime("%Y%m%d")
            save_to_LTOS(long_url,code, time)
            save_to_STOL(code,long_url, time)
    return get_code(long_url)

def decode(short_url : str) -> str:
    #  Check for valid code
    if len(url_or_code) < ENCODE_LENGTH and len(url_or_code) > ENCODE_LENGTH:
            raise KeyError
    for ch in url_or_code:
        if ch not in encode_char_choice:
                raise KeyError
                
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

footer="""<style>
a:link , a:visited{
color: #ecedf3;
background-color: transparent;
text-decoration: underline;
}
a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}
.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: black;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p style='color: #ecedf3;'> Made with <a style="text-decoration:none" href="https://streamlit.io/" target="blank"> Streamlit </a>❤  <a> by</a><a style='display: block; text-align: center; text-decoration:none;' href="https://github.com/arjunraghurama" target="blank">Arjun</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
