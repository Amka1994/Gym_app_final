import streamlit as st
import pandas as pd
from utils.google_sheet import connect_to_sheet
import datetime
import altair as alt
from forms.fitness import class_list
from forms.product import product_list

from utils.functions import format_number
from utils.functions import get_category_filters

def load_data():
    sheet = connect_to_sheet()
    records = sheet.get_all_records()
    df = pd.DataFrame(records)
    return df
df = load_data()

fitness_category_list = ['All']
fitness_category_list.extend(list(df[df['Type']=='Fitness']['Анги'].unique()))
product_category_list = ['All']
product_category_list.extend(list(df[df['Type']=='Product']['Анги'].unique()))
month_list = ['All']
month_list.extend(list(df['Month'].unique()))


st.title("Sales_dashboard")


with st.sidebar:
    st.title('Дашбоардын удирдлага')

    with st.form("filter_form"):
        # Сар сонгох
        month = st.multiselect('Тайлагнах сар', month_list, default=month_list[0])

        # Төрөл, анги сонголт
        selected_types, selected_fitness, selected_product = get_category_filters(fitness_category_list, product_category_list)

        # 🔘 Шүүлт товч
        submitted = st.form_submit_button("Шүүлт хийх")

if submitted:
    # 🎯 Фильтр хийх логик
    if (len(selected_fitness) == 1 and selected_fitness[0] == 'All') & (len(selected_product) == 1 and selected_product[0] == 'All'):
        filtered_df = df
    else:
        filtered_df = df[
            df['Анги'].isin(selected_fitness) | df['Анги'].isin(selected_product)
        ]

    # 🧮 Нийт борлуулалт
    col1, col2, col3 = st.columns((10, 20, 10))
    with col1:
        st.markdown('Нийт борлуулалт')
        st.markdown("**Орлого:** " + format_number(sum(filtered_df['Дүн'])), unsafe_allow_html=True)
        unpaid_amount = filtered_df[filtered_df['Төлсөн эсэх'] == 'Төлөөгүй']['Дүн'].sum()
        st.markdown("**Төлөгдөөгүй орлого:** " + format_number(unpaid_amount), unsafe_allow_html=True)
        

    # 📊 Борлуулалт сараар
    with col2:
        st.markdown('Борлуулалт сараар')
        chart = alt.Chart(filtered_df,
                          height=300,
                          width=600)\
            .mark_line(point=True, strokeWidth=3)\
            .encode(
                x="Month:N",
                y='sum_sales:Q'
            ).transform_aggregate(
                groupby=['Month'],
                sum_sales='sum(Дүн)'
            ).configure_point(size=150)
        st.altair_chart(chart)
