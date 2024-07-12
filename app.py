from dotenv import load_dotenv
load_dotenv() ## load all the environemnt variables

import streamlit as st
import os
import sqlite3

import google.generativeai as genai
## Configure Genai Key

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

## Function To Load Google Gemini Model and provide queries as response

def get_gemini_response(question , prompt):
    model = genai.GenerativeModel('gemini-pro')
    response=model.generate_content([prompt[0],question])
    return response.candidates[0].content.parts[0].text

def read_sql_query(sql,db):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()
    for row in rows :
        print(row)
    return rows

prompt = [
"""
you are expert in converting english question  to sql query .
i will give you a 'student db'.so your work to provide me sql query
.and do not give extra words ,symbol, and symbol , focus only query.please do not give ``` 
"""
]

st.set_page_config(page_title="I can Retrieve Any SQL query")
st.header("Gemini App To Retrieve SQL Data")

question=st.text_input("Input: ",key="input")

submit=st.button("Ask the question")

if submit :
    response = get_gemini_response(question , prompt)
    print(response)
    response = read_sql_query(response,"student.db")
    st.subheader("The REsponse is")
    for row in response:
        print(row)
        st.header(row)