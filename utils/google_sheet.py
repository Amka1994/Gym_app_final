import gspread
from google.oauth2.service_account import Credentials
import streamlit as st
import pandas as pd
import datetime



#@st.cache_resource ашиглан Google sheets холболтыг кешлэх
@st.cache_resource
def connect_to_sheet():
    scope = ["https://www.googleapis.com/auth/spreadsheets", 
            "https://www.googleapis.com/auth/drive"]
    
    #creds = Credentials.from_service_account_file("D:\gym_app\json\credentials.json", scopes = scope)
    creds_dict = st.secrets["google_service_account"]
    creds = Credentials.from_service_account_info(creds_dict, scopes = scope)
    
    client = gspread.authorize(creds)
    sheet = client.open_by_key('1LXqGEarZMI74xgBntM_pRHUEK8cWAi7KzFL2S81Cwwo').sheet1
    return sheet
# Холболт хийх
sheet = connect_to_sheet()


