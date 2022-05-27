from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import requests
import plotly.express as px


def create_premade_layout(layout, data_link, type = ''):

    data = requests.get(data_link).json()

    if layout == '2d-layout-1':

        ## get symbols 
        symbols = [x['ASSET'] for x in data]
        all_symbols = []
        for i in symbols:
            if i not in all_symbols:
                all_symbols.append(i)

        ## drop text box 
        symbols = st.multiselect("Choose asset to visualize", all_symbols, all_symbols[:9])
        st.text("")

        ## sort data 
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

        ## create data frames
        chart = pd.DataFrame(
            vol_data,
            index=date_data
        )

        chart2 = pd.DataFrame(
            [sum(vol_data[x]) for x in vol_data],
            index=[x for x in vol_data]
        )

        ## place data frame 
        if type == 'line':
            st.line_chart(chart)
        elif type == 'bar':
            st.bar_chart(chart)
        elif type == 'area':
            st.area_chart(chart)
        else:
            st.area_chart(chart)
            
        st.bar_chart(chart2)
        
    elif layout == 'pie-layout-1':
        ### data needs to made like {BIG_CATEGORY, SMALL_CATEGORY, VALUE}
        symbols = [x['BIG_CATEGORY'] for x in data]
        big_category = []
        for i in symbols:
            if i not in big_category:
                big_category.append(i)
                
        symbols3 = st.selectbox("", big_category)

        df = [x for x in data if x['BIG_CATEGORY'] == symbols3]
        if len(df) > 10:
            df = sorted(df, key=lambda x: x['VALUE'], reverse=True)
            df = df[0:10]
        
        fig = px.pie(df, values='VALUE', names='SMALL_CATEGORY')
        st.plotly_chart(fig, use_container_width=True)


"""
# Symmetric vs Asymmetric LPs
    
On THORChain, you are allowed to add liquidity in 1 of 3 ways: Rune-only, asset-only, or symmetric (both Rune + asset). What is the breakdown of liquidity being added, according to those categories? Are there any trends over time or by pool?

### What is YLDLY?

Yieldly is a DeFi staking protocol built for Algorand, that allows holders of Algo to stake their assets and have the chance to earn a disproportionate reward. The native token of the Yieldly ecosystem is YLDLY.

### Methodology

- We will look at the YLDLY token swap volume in terms of swap to asset and DEX. 

- We are looking to see where and what assets people are swapping with YLDlY in the passt 30 days.

## YLDLY token swap metrics 

"""

create_premade_layout('2d-layout-1', 'https://node-api.flipsidecrypto.com/api/v2/queries/57d05aaf-2994-4ad7-b310-005a6ad92c1f/data/latest')

"""
### Observations 

- The vast majority of all YLDLY swap volume was with the ALGO token.

- The YLDLY token's swap volume has been declining over the past 30 days.
"""
create_premade_layout('pie-layout-1', 'https://node-api.flipsidecrypto.com/api/v2/queries/513968aa-82a9-4448-b670-9466a13e6dd1/data/latest')
    
"""
## Conclusion
- Out of the 50 - 100 million YLDLY tokens swapped daily only between 1 and 3 million of them are swapped on DEXs other than Tinyman.

- There were 2 days in the past month where the YLDLY token swap Volume was over 120 Million tokens.

"""    

 
   
