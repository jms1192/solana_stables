from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import requests




"""
# Swapping for YLDLY on DEXs

Is swapping for YLDY more popular on some DEXs than others? 

What assets are users swapping for YLDLY?

Are there any standout days of swap volume for Yieldly?
"""

with st.echo(code_location='below'):
    
  
    ### pick symbols
    data = requests.get('https://node-api.flipsidecrypto.com/api/v2/queries/5c5ecaee-e9da-4ff6-b62d-651711f9d324/data/latest').json()
    symbols = [x['ASSET'] for x in data]
    all_symbols = []
    for i in symbols:
        if i not in all_symbols:
            all_symbols.append(i)
    
    symbols = st.multiselect("Choose asset to visualize", all_symbols, all_symbols[:9])
    st.text("")
    
    ### Sort Data  
    vol_data = {}
    vol_data_sum = {}
    date_data = []
    vol = []
    asset = ''
    for x in data:
        if x['ASSET'] in symbols:
            if not x['ASSET'] == asset:
                if asset == '':
                    asset = x['ASSET']
        
                else:
                    vol_data_sum[asset] = sum(vol)
                    vol_data[asset] = vol
                    asset = x['ASSET']
                  
                vol = []
                vol.append(x['SWAP_VOLUME'])
                date_data = []
                date_data.append(x['DAY'])
            else:
                date_data.append(x['DAY'])
                vol.append(x['SWAP_VOLUME'])
    vol_data[asset] = vol           
                
    symbols.sort()
    ### Display Bar chart
    
    chart = pd.DataFrame(
        vol_data,
        index=date_data
    )
    
    
    ### Pie chart 
  
        
    chart2 = pd.DataFrame(
       [sum(vol_data[x]) for x in vol_data],
       ##vol_data_sum
       index=[x for x in vol_data]
    )
    
    
    st.bar_chart(chart)
    st.bar_chart(chart2)

    
    
