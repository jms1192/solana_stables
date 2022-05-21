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
    total_points = st.slider("Number of points in spiral", 1, 9000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
  
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

    
    
