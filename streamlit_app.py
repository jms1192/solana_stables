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
    
    data = requests.get('https://node-api.flipsidecrypto.com/api/v2/queries/5c5ecaee-e9da-4ff6-b62d-651711f9d324/data/latest').json()
    
    chart_data = pd.DataFrame(
        [x['SWAP_VOLUME'] for x in data],
        [x['DAY'] for x in data]
        
        
    )
    st.bar_chart(chart_data)
    
    source = data
    all_symbols = [x['ASSET'] for x in data].unique()
    symbols = st.multiselect("Choose stocks to visualize", all_symbols, all_symbols[:3])

    space(1)

    source = source[source.symbol.isin(symbols)]
    chart = chart.get_chart(source)
    st.altair_chart(chart, use_container_width=True)
