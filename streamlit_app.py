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
    
    data = requests.get('https://api.flipsidecrypto.com/api/v2/queries/0b221009-cbdd-4c47-b815-cd7cf837462d/data/latest').json()
    
    chart_data = pd.DataFrame(
        [x['SWAP_FEES'] for x in data],
        [x['DAY'] for x in data],
        columns=["a", "b", "c"])

    st.bar_chart(chart_data)
