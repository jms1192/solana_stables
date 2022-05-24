from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import requests

"""
# Tracking GMT into StepN

Is swapping for YLDY more popular on some DEXs than others? 
What assets are users swapping for YLDLY?
Are there any standout days of swap volume for Yieldly?
### What is YLDLY?
Yieldly is a DeFi staking protocol built for Algorand, that allows holders of Algo to stake their assets and have the chance to earn a disproportionate reward. The native token of the Yieldly ecosystem is YLDLY.
### Methodology
- We will look at the YLDLY token swap volume in terms of swap to asset and DEX. 
- We are looking to see where and what assets people are swapping with YLDlY in the passt 30 days.
## YLDLY token swap metrics 
"""

##with st.echo(code_location='below'):
    
  
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
    index=[x for x in vol_data]
)
   
st.bar_chart(chart)
st.bar_chart(chart2)
"""
### Observations 
- The vast majority of all YLDLY swap volume was with the ALGO token.
- The YLDLY token's swap volume has been declining over the past 30 days.
"""

data = requests.get('https://node-api.flipsidecrypto.com/api/v2/queries/1cbd998e-fe68-4992-bd31-5c204fdf426a/data/latest').json()
symbols = [x['ASSET'] for x in data]
all_symbols = []
for i in symbols:
    if i not in all_symbols:
        all_symbols.append(i)
    
symbols = st.multiselect("Choose DEX to visualize", all_symbols, all_symbols[:9])
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
    index=[x for x in vol_data]
)
   
st.bar_chart(chart)
st.bar_chart(chart2)
    
"""
## Conclusion
- Out of the 50 - 100 million YLDLY tokens swapped daily only between 1 and 3 million of them are swapped on DEXs other than Tinyman.
- There were 2 days in the past month where the YLDLY token swap Volume was over 120 Million tokens.
"""    
  
    
