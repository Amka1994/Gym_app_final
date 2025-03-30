import pandas as pd
import numpy as np
import streamlit as st
import datetime

import altair as alt


def format_number(num):
    return f"<span style='font-size:14px; color:#333;'>{num:,.0f} ₮</span>"



def get_category_filters(fitness_list, product_list):
        type_options = ['Fitness', 'Product']
        selected_types = st.multiselect(
                'Төрөл сонгох',
                options=type_options,
                default=type_options,
                key='type_filter_main'
        )
        if not selected_types:
            st.warning('Төрөл сонгоно уу.')
            st.stop()
        
        if 'Fitness' in selected_types:
               selected_fitness = st.multiselect(
                    'Ангилал сонгох',
                      options=['All'] + fitness_list,
                      default=['All'],
                      key='fitness_filter_main'
               )
        else:
               selected_fitness = ['All']
        
        if 'Product' in selected_types:
               selected_product = st.multiselect(
                      'Бүтээгдэхүүн сонгох',
                      options=['All'] + product_list,
                      default=['All'],
                      key='product_filter_main'      
               )
        else: 
              selected_product = ['All']

        return selected_types, selected_fitness, selected_product



       
