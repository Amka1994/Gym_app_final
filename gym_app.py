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
    
    creds = Credentials.from_service_account_file('D:\gym_app\json\credentials.json', scopes = scope)

    

    client = gspread.authorize(creds)
    sheet = client.open_by_key('1LXqGEarZMI74xgBntM_pRHUEK8cWAi7KzFL2S81Cwwo').sheet1
    return sheet
# Холболт хийх
sheet = connect_to_sheet()

#Read data from google sheet
def read_data():
    data = sheet.get_all_records()
    return pd.DataFrame(data)

#add data to google sheet
def add_data(row):
    sheet.append_row(row)

#Product_list
product_list = ['Өглөөний анги', 'Цагийн хязгааргүй', '3 сар/цагийн хязгааргүй/', '6 сар/цагийн хязгааргүй/', '3 сар /өглөө/', '6 сар /өглөө/',
                'Оюутан & Сурагч', 'Locker', '15 өдөр', 'Mina: Group', 'Mina: Personal', '1 удаагийн оролт']

#worker list
worker_list = ['Мина', 'Төгөлдөр', 'Галаа', 'Амка', 'Нямка']

#Price_list
price_dict = {
    'Өглөөний анги': 110000,
    'Цагийн хязгааргүй': 130000,
    '3 сар/цагийн хязгааргүй/': 330000,
    '6 сар/цагийн хязгааргүй/': 600000,
    '3 сар /өглөө/': 290000,
    '6 сар /өглөө/': 540000,
    'Оюутан & Сурагч': 95000,
    'Locker': 39000,
    '15 өдөр':69000,
    'Mina: Group': 350000,
    'Mina: Personal':700000,
    '1 удаагийн оролт':29000
}

#PayedorNot
Status_list = ['Төлсөн', 'Төлөөгүй']

#Streamlit дээр мэдээлэл оруулах хэсэг
with st.sidebar:
    st.header('Борлуулалт')
    
    with st.form(key='data_form'):
        buyer = st.text_input('Үйлчлүүлэгч:')
        class_name = st.selectbox('Ангийн нэр:', ['Анги сонгоно уу'] + list(price_dict.keys()), index=0)
        price = price_dict.get(class_name, 0)
        sale = st.number_input('Хямдруулах дүн оруулна уу:')
        amount = price - sale
        status = st.selectbox('Төлбөр төлсөн эсэх:', Status_list)
        current_date = datetime.date.today().strftime('%Y-%m-%d')
        describtion = st.text_area('Тэмдэглэл:'," ", height=150).encode('utf-8').decode('utf-8')
        worker = st.selectbox('Бүртгэсэн:', worker_list)
       
           


        submit_button = st.form_submit_button('Хадгалах')

    if submit_button:
        sheet.append_row([current_date,buyer, class_name, price, sale, amount, status, describtion, worker])
        st.success('Мэдээлэл амжилттай хадгалагдлаа')

col1, col2 =st.columns(2)
with col1:
    st.header('Gym_main')
    df = read_data()

# Огноо талбарыг хөрвүүлэх
df['Огноо'] = pd.to_datetime(df['Огноо'])

col1, col2 =st.columns(2)
# Огноогоор фильтр хийх
with col1:
    start_date = st.date_input("Эхлэх огноо", df['Огноо'].min())
with col2:
    end_date = st.date_input("Төгсгөл огноо", df['Огноо'].max())



# Огноогоор фильтр хийх
filtered_df = df[(df['Огноо'] >= pd.to_datetime(start_date)) & (df['Огноо'] <= pd.to_datetime(end_date))]


# Streamlit дээр харуулах
st.dataframe(filtered_df, width=1200)
