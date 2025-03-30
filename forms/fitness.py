import streamlit as st
import datetime
import gspread


from utils.google_sheet import connect_to_sheet


#Class_list
class_list = ['Өглөөний анги', 'Цагийн хязгааргүй', '3 сар/цагийн хязгааргүй/', '6 сар/цагийн хязгааргүй/', '3 сар /өглөө/', '6 сар /өглөө/',
                    'Оюутан & Сурагч', 'Locker', '15 өдөр', 'Mina: Group', 'Mina: Personal', '1 удаагийн оролт']



#worker list
worker_list = ['Мина', 'Төгөлдөр', 'Галаа', 'Амка', 'Нямка']

Status_list = ['Төлсөн', 'Төлөөгүй']

#Price_list
class_price_dict = {
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

def fitness_form():
    with st.form("fitness_sales"):
        buyer = st.text_input('Үйлчлүүлэгч:')
        
        class_name = st.selectbox('Ангийн нэр:', ['Анги сонгоно уу'] + list(class_price_dict.keys()), index=0)

        if class_name != "Анги сонгоно уу":
            price = class_price_dict.get(class_name, {})
        else:
            price = 0
        type_value = "Fitness"

        sale = st.number_input('Хямдруулах дүн оруулна уу:')
        qty = st.number_input('Ширхэг:')
        amount = price - sale
        current_date = datetime.date.today()
        month_name = current_date.strftime('%B')
        describtion = st.text_area('Тэмдэглэл:'," ", height=150).encode('utf-8').decode('utf-8')
        worker = st.selectbox('Бүртгэсэн:', worker_list)

        status = st.selectbox('Төлбөр төлсөн эсэх:',['None'] + ['Төлсөн', 'Төлөөгүй'], index=0)

        payment_method = None
        if status == 'Төлсөн':
            payment_method = st.selectbox(
                "Төлбөрийн төрөл сонгох:",
                options=["QPay", "Данс", "Бэлэн", "POS", "StorePay"]
            )  
        
            
        submit_button = st.form_submit_button('Хадгалах')

    if submit_button:
        if not buyer:
            st.warning("📌 Үйлчлүүлэгчийн нэр оруулна уу.")
        elif class_name == "Анги сонгоно уу":
            st.warning("📌 Ямар ангид бүртгэх вэ.")
        elif status=='None':
             st.warning("📌 Төлөв сонгоно уу.")
        elif worker == "Хэн бүртгэж байна вэ?":
             st.warning("📌 Бүртгэсэн хэсгээс өөрийгөө сонгоорой.")
        else:
            sheet = connect_to_sheet()
            sheet.append_row([current_date.isoformat(), current_date.year, month_name, current_date.day, buyer, class_name, type_value, price, sale, qty, amount, status, payment_method, describtion, worker])
            st.success("✅ Амжилттай хадгалагдлаа!")


    

    