# db.py
import os
from sqlalchemy import create_engine, text
from urllib.parse import quote
from dotenv import load_dotenv
import pandas as pd
import streamlit as st

load_dotenv()

@st.cache_resource
def get_engine():
    encoded_password = quote(os.getenv("DB_PASSWORD"), safe='')
    return create_engine(
        f"mysql+mysqlconnector://{os.getenv('DB_USER')}:{encoded_password}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )

@st.cache_data(ttl=60)
def run_query(query, params=None):
    with get_engine().connect() as conn:
        return pd.read_sql(text(query), conn, params=params)