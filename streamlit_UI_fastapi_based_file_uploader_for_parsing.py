import streamlit as st
import streamlit as st
import pandas as pd
from io import StringIO
import requests



parser_url="http://127.0.0.1:8000/uploadfile/"
#url='http://127.0.0.1:8000/download/'
file_name_url='http://127.0.0.1:8000/get_uploaded_file_name/'



st.header("PDF Parser")

option = st.selectbox(
'Do you want to download Parsed PDF',
('Yes', 'No'))


uploaded_file = st.file_uploader("Choose a file",key='upload_file')
if (uploaded_file is not None) and (option=='Yes'):
    # To read file as bytes:
    
    bytes_data = uploaded_file.getvalue()
    
    
    files={'file': uploaded_file}
    
    
    #Post Json content to FastAPI server
    
    
    st.markdown(option)
    
    #Post File Content to Fast API server
    response2 = requests.post(parser_url,files=files)
    
    print(response2.content)
    
    
    if response2.content is not None:
        st.download_button(
        label="Download data as pickle file",
        data=response2.content,
        file_name="parsed_pdf.pickle",
        mime="application/python-pickle",
    )
    
    #response = requests.post(url,json=detail_option)
    
    print("completed requests")
    
    
    