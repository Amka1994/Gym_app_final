import streamlit as st
import gspread
import pandas as pd
from utils.google_sheet import connect_to_sheet
import datetime
from utils.functions import format_number


from forms.fitness import fitness_form
from forms.product import product_form

def load_data():
    sheet = connect_to_sheet()
    records = sheet.get_all_records()
    df = pd.DataFrame(records)

    # Огноог зөвхөн date болгох
    df['Огноо'] = pd.to_datetime(df['Огноо'], errors='coerce').dt.date
    df = df[df['Огноо'].notna()]  # NaT мөрүүдийг хасах

    return df


st.markdown("""
    <style>
    .dataframe tbody tr th {
        font-size: 12px !important;
    }
    .dataframe tbody tr td {
        font-size: 12px !important;
    }
    </style>
    """, unsafe_allow_html=True)

col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

@st.dialog("Фитнесс анги")
def fitness_sales():
    fitness_form()

@st.dialog("Бүтээгдэхүүн")
def product_sales():
    product_form()


with col1:
    if st.button("💪 Фитнесс анги"):
        fitness_sales()

with col2:       
    if st.button("🍭 Бүтээгдэхүүн"):
        product_sales()
    

df = load_data()

today = datetime.date.today()

# Огнооны шүүлт UI
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("Эхлэх огноо", df['Огноо'].min())
with col2:
    end_date = st.date_input("Төгсгөл огноо", df['Огноо'].max())

filtered_df = df[(df['Огноо'] >= start_date) & (df['Огноо'] <= end_date)]



# Огноогоор фильтр хийх
#"filtered_df = df[(df['Огноо'] >= pd.to_datetime(start_date)) & (df['Огноо'] <= pd.to_datetime(end_date))]"

Status_list = ['Төлсөн', 'Төлөөгүй']
selected_status = st.selectbox("Төлбөр төлсөн эсэх шүүх", options=['Бүгд'] + Status_list)

Active_list = ['Fitness', 'Product']
selected_active = st.selectbox('Төрөлөө сонгоно уу', options=['Бүгд'] + Active_list)

# Шүүлт хийх
if selected_status != 'Бүгд':
    filtered_df = filtered_df[filtered_df['Төлсөн эсэх'] == selected_status]

if selected_active != 'Бүгд':
    filtered_df = filtered_df[filtered_df['Type'] == selected_active]

# Streamlit дээр харуулах

columns_to_show = ['Month', 'Day', 'Үйлчлүүлэгч', 'Анги', 'Ширхэг', 'Дүн', 'Төлсөн эсэх', 'Бүртгэсэн']

columns_to_show_details = ['Огноо', 'Үйлчлүүлэгч', 'Анги', 'Type', 'Төлбөр', 'Хямдрал', 'Ширхэг', 'Дүн', 'Төлсөн эсэх', 'Method', 'Тэмдэглэл', 'Бүртгэсэн']
show_detials = st.checkbox('Дэлгэрэнгүй харах', value=False)

if show_detials:
    st.dataframe(filtered_df[columns_to_show_details], use_container_width=True)
else:
    st.dataframe(filtered_df[columns_to_show], use_container_width=True)


# 6. Өнөөдрийн орлого
today_income = df[(df['Огноо'] == today) & (df['Төлсөн эсэх'] == 'Төлсөн')]
today_income_nopay = df[(df['Огноо'] == today) & (df['Төлсөн эсэх'] == 'Төлөөгүй')]['Дүн'].sum()


col1, col2 = st.columns(2)
with col1:
    today_income_payed = today_income['Дүн'].sum()
    st.metric("🟢 Өнөөдрийн төлөгдсөн орлого", f"{today_income_payed:,.0f} ₮")
    method_summary = today_income.groupby('Method')['Дүн'].sum().reset_index()
    for i, row in method_summary.iterrows():
        st.markdown(f"**{row['Method']} орлого:** {format_number(row['Дүн'])}", unsafe_allow_html=True)
with col2:
    st.metric("🔴 Өнөөдрийн төлөөгүй орлого", f"{today_income_nopay:,.0f} ₮")












