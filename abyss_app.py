import streamlit as st

#--- Page setup ---


sales_page = st.Page(
    page="views/Sales.py",
    title= "Sales",
    icon=":material/account_circle:",
    default=True
)

project_1_page = st.Page(
    page="views/Dashboard.py",
    title="Sales Dashboard",
    icon=":material/bar_chart:",
)

pg = st.navigation(pages=[sales_page, project_1_page])

st.set_page_config(page_title="ABYSS Fitness", page_icon="💪")

with st.sidebar:
    st.markdown("---")
    st.markdown("<p style='text-align: center; font-size: 16px; color: gray;'>Created by Amka for Mina ❤️ : v1</p>", unsafe_allow_html=True)

pg.run()

