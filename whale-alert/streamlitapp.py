import streamlit as st
import pandas as pd

import os
import sys

st.markdown("Database transactions")
data = pd.read_csv('dataset/database_txo.csv')

data = data.drop(columns=['Unnamed: 0', 'id'])

# Select some rows using st.multiselect. This will break down when you have >1000 rows.
st.write(data)

os.system('httping -hlg http://localhost:8503')