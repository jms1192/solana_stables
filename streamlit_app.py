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
        symbols = st.multiselect("", all_symbols, all_symbols[:9])
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
# Stablecoin Landscape on DEXs

Analyse the stablecoin landscape on Sushiswap, identifying the various tokens available and their main metrics (volume, number of swaps, TVL, and other relevant for you). Which one is the most successful? Is it the same at Uniswap?

### What is Sushiswap? 

SushiSwap is a decentralized cryptocurrency exchange and automated market maker built on Ethereum. Holders of SUSHI can participate in community governance and stake their tokens to receive a portion of SushiSwap's transaction fees.

### Methodology

- We will look at the metrics of stablecoins USDC, USDT, DAI, UST, and FRAX on Uniswap, Curve, and Sushiswap  

- We are looking to what has the stablecoin landscape has been on Ethereum DEXs in 2022

## Stablecoin Swap Metrics 

The 2 graphs below show the swap volume of DAI, USDC, USDT, FRAX, and UST on Curve, Uniswap, and Sushiswap since the start of 2022. Most weeks there has been between 3 and 8 Billion of stablecoin swap volume with most of the volume coming from USDC and USDT. Out of the algorithmic stablecoins in this chart DAI has had the largest swap volume on these DEXs. 
"""

create_premade_layout('2d-layout-1', 'https://node-api.flipsidecrypto.com/api/v2/queries/2ed8a2cc-6bf5-46db-8e8d-d10d234bc5c8/data/latest', 'bar')

"""
The figure below shows the LP volume breakdown by pool of the diffrent Thorchain liquidity actions. Nearly half of all Rune-only LP action volume have gone into the BTC.BTC and ETH.ETH pool, while nealy half of all asset-only deposits have gone into the TERRA.UST and the BNB.BUSD pool.  
"""
create_premade_layout('2d-layout-1', 'https://node-api.flipsidecrypto.com/api/v2/queries/1af3facf-735b-4a48-9818-f7cda8e49000/data/latest', 'bar')
    
"""
## Conclusion

- In 2022 providing Rune-only liquidity has been the most popular way to provide liquidity on The Chain and asset-only liquidity seems to be the least popular way to provide liquidity.   

- People providing liquidity to in rune-only and asset-only liquidity pools seem to provide liquidity in very different ways. Most of the volume coming in rune-only are going to the BTC.BTC and the ETH.ETH pool and the assets only liquidity is coming in to the stablecoin pools TERRA.UST and BNB.BUSD. 

"""    

create_premade_layout('pie-layout-1', 'https://node-api.flipsidecrypto.com/api/v2/queries/ddbccbf5-0560-4f67-943f-246ee7864873/data/latest')
   
