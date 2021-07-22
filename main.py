import SessionState
import streamlit as st
import random

st.set_page_config(
        page_title="Encode Decode",
        page_icon="❤️",
        layout="centered"
    )

state = SessionState.get(long_url_to_short_url = {}, short_url_to_long_url={})
ENCODE_LENGTH = 6
encode_char_choice = "0123456789abcdefghijklmnopqrstuvwxyABCDEFGHIJKLMNOPQRSTUVWXY"

url_or_code = st.text_input("URL or Code")
_,en,_,de,_ = st.beta_columns([4,1,1,1,5])

def encode(long_url : str) -> str:
    while(long_url not in state.long_url_to_short_url):
        code = "".join([ random.choice(encode_char_choice) for _ in range(ENCODE_LENGTH)])
        if code not in state.short_url_to_long_url:
            state.short_url_to_long_url[code] = long_url
            state.long_url_to_short_url[long_url] = code
    return state.long_url_to_short_url[long_url]

def decode(short_url : str) -> str:
    return state.short_url_to_long_url[short_url]

if(en.button("Encode")):
    code = encode(url_or_code)
    st.markdown(""" <p><span>URL has been encoded as : {}</p>""".format(code),unsafe_allow_html=True)

if(de.button("Decode")):
    try:
        url = decode(url_or_code)
        st.markdown(""" <p><span>Decoded URL is : </span><a href="{}">{}</a></p>""".format(url,url),unsafe_allow_html=True)
    except KeyError:
        er = "404 Oh Snap!! We are unable to find the URL for you. 😞"
        st.markdown(""" <p><span>{}</span></p>""".format(er),unsafe_allow_html=True)
