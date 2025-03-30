import streamlit as st
import datetime
import gspread

from utils.google_sheet import connect_to_sheet


#Product_list
product_list = ['Тос ус', 'Жижиг ус', 'Gatorade', 'Уураг/1 уулт/', 'Sporica', 'Target', 'Delice', 'Shaker', 'Shock', 'Rex', 'Lamington', 'Гаа',
              'Ultra whey 15 уулттай', 'Ultra whey 10 уулттай', 'Bcaa (be first)', 'Bcaa (syntime)', 'Creatine (syntime)', 'Өөх шатаагч', 
              'Strong', 'Хоол', 'Bcaa/1 уулт/', 'onlyfit', 'wellnut', 'Cake']

#Price_list
product_price_dict = {
        'Том ус': 3500,
        'Жижиг ус': 2500,
        'Gatorade': 7500,
        'Уураг/1 уулт/': 8000,
        'Sporica': 7500,
        'Target': 5000,
        'Delica': 10000,
        'Shaker' : 6000,
        'Shock' : 8000,
        'Rex' : 9000,
        'Lamington' : 10000,
        'Гаа' : 6000,
        'Ultra whey 15 уулттай':120000,
        'Ultra whey 10 уулттай':90000,
        'Bcaa (be first)':75000,
        'Bcaa (syntime)':95000,
        'Creatine (syntime)':100000,
        'Өөх шатаагч':140000,
        'Strong' : 11500,
        'Bcaa/1 уулт/':5000,
        'onlyfit' : 3000,
        'Хоол' : 13000,
        'wellnut' : 6500,
        'Cake' : 14000
    }
#worker list
worker_list = ['Мина', 'Төгөлдөр', 'Галаа', 'Амка', 'Нямка']


def product_form():
    current_date = datetime.date.today()
    month_name = current_date.strftime('%B')
    
    # Form эхэлж байна
    with st.form("fitness_sales"):
        buyer = st.text_input('Үйлчлүүлэгч:')
        
        product_name = st.selectbox('Бүтээгдэхүүн:', ['Бүтээгдэхүүн сонгоно уу'] + list(product_price_dict.keys()), index=0)
        
        if product_name != "Бүтээгдэхүүн сонгоно уу":
            price = product_price_dict.get(product_name, 0)
        else:
            price = 0

        type_value = "Product"
        sale = st.number_input('Хямдруулах дүн оруулна уу:', min_value=0)
        qty = st.number_input('Ширхэг:', min_value=0)
        amount = price - sale
        net_amount = amount * qty

        describtion = st.text_area('Тэмдэглэл:', " ", height=150).encode('utf-8').decode('utf-8')

        worker = st.selectbox('Бүртгэсэн:', ['Хэн бүртгэж байна вэ?'] + list(worker_list), index=0)

        status = st.selectbox('Төлбөр төлсөн эсэх:', ['None', 'Төлсөн', 'Төлөөгүй'], index=0)

        payment_method = None
        if status == 'Төлсөн':
            payment_method = st.selectbox(
                "Төлбөрийн төрөл сонгох:",
                options=["Сонгоно уу","QPay", "Данс", "Бэлэн", "POS", "StorePay"]
            )

        # ❗ Submit button яг энд байх ёстой!
        submit_button = st.form_submit_button('Хадгалах')

    # Submit дарагдсан үед гадаа логик ажиллана
    if submit_button:
        if not buyer:
            st.warning("📌 Үйлчлүүлэгчийн нэр оруулна уу.")
        elif product_name == "Бүтээгдэхүүн сонгоно уу":
            st.warning("📌 Бүтээгдэхүүн сонгоно уу.")
        elif qty <= 0:
            st.warning("📌 Ширхэг оруулна уу.")
        elif status == 'None':
            st.warning("📌 Төлөв сонгоно уу.")
        elif payment_method == 'Сонгоно уу':
            st.warning("📌 Төлбөрийн төрлөө сонгоно уу.")
        elif worker == "Хэн бүртгэж байна вэ?":
            st.warning("📌 Бүртгэсэн хэсгээс өөрийгөө сонгоорой.")
        else:
            sheet = connect_to_sheet()
            sheet.append_row([
                current_date.isoformat(), current_date.year, month_name, current_date.day,
                buyer, product_name, type_value, price, sale, qty, net_amount,
                status, payment_method, describtion, worker
            ])
            st.success("✅ Амжилттай хадгалагдлаа!")
