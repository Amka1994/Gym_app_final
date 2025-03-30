import gspread
from google.oauth2.service_account import Credentials


def connect_to_sheet():
    scope = ["https://www.googleapis.com/auth/spreadsheets", 
            "https://www.googleapis.com/auth/drive"]
    
    creds = Credentials.from_service_account_file("D:\gym_app\json\credentials.json", scopes = scope)
    
   

    client = gspread.authorize(creds)
    sheet = client.open_by_key('1LXqGEarZMI74xgBntM_pRHUEK8cWAi7KzFL2S81Cwwo').sheet1
    return sheet

sheet = connect_to_sheet()


