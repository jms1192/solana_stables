from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import requests
import plotly.express as px


def create_premade_layout(layout, data_link, type = '', num = 1):

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
        
        if num == 1:
            symbols3 = st.selectbox("", big_category)
            df = [x for x in data if x['BIG_CATEGORY'] == symbols3]
        else:
            big_category2 = big_category
            symbols4 = st.selectbox("", big_category2)
            df = [x for x in data if x['BIG_CATEGORY'] == symbols4]
            
        if len(df) > 10:
            df = sorted(df, key=lambda x: x['VALUE'], reverse=True)
            df = df[0:10]
        
        fig = px.pie(df, values='VALUE', names='SMALL_CATEGORY')
        st.plotly_chart(fig, use_container_width=True)


"""
## Introduction

### What is Solana?

Solana is a public blockchain platform with smart contract functionality. Its native cryptocurrency is SOL. Solana offers low fees and fast transaction times. Solana smart contracts are written in Rust rather than solidity.

### What are Stablecoins 

Stablecoins are cryptocurrencies where the price is designed to be pegged to a cryptocurrency, fiat money, or to exchange-traded commodities. Currently the vast majority of stable coins are pegged to the USD.  

### Methodology

- We will look at the transaction volume and number of users of stable coin on Solana.

- The stable coins we will look at are USDC, USDT, USDH, PAI, NIRV, DAI, and FRAX.

#### Monthly Solana Stablecoin Transfer Volume  
"""

create_premade_layout('2d-layout-1', 'https://node-api.flipsidecrypto.com/api/v2/queries/031a2b48-6fca-43d5-a4c7-db0699058798/data/latest', 'bar')

"""

The two graphs above show the monthly and total transaction volume of the stablecoins USDC, USDT, USDH, PAI, USDT, and USDX on Solanan. These graphs show that almost all of the stablecoin volume on Solanan is using USDC and USDT. Other than the top 2 stablecoins UST and PAI have made up most of the remaining stablecoin volume on Solana in 2022.

#### USDT/USDC Top contracts by Number of Stablecoin users 
"""    

create_premade_layout('pie-layout-1', 'https://node-api.flipsidecrypto.com/api/v2/queries/010e3f77-a7b3-4491-9450-44779c406edb/data/latest')

"""
#### USDT/USDC Top contracts by Number of Stablecoin Volume  
"""

create_premade_layout('pie-layout-1', 'https://node-api.flipsidecrypto.com/api/v2/queries/fdf89f39-1048-40f1-8fa8-83966d623d98/data/latest', num = 2)

"""
# Conclusion 

- USDC and USDT are the two Stablecoins with the most volume on Ethereum DEXs 

- Uniswap-v3 makes up the majority of stablecoin swaps in 2022 

- In early and mid May there was a massive spike in stablecoin volume on Curve 

- Sushiswap is the only major Ethereum DEX to have DIA being in the top 2 of stablecoin volume. 


"""   
  
