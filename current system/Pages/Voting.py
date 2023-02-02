## Imports

import streamlit as st
import pandas as pd
import hvplot.pandas
import numpy as np
import hvplot.pandas
import time
import plotly as plotly
import bokeh as plt
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import datetime

## Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def load_contract():

    # Load the contract ABI
    with open(Path('contracts/compiled/vote_abi.json')) as f:
        artwork_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = "0x4eE734740c5993f54A71304167Edad08dc4bB9b6"


    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=artwork_abi
    )

    return contract


# Load the contract
contract = load_contract()

address = "0x9386008bAdE0B1e5DfF07FC187DecB80D8FbBd6c"
g_address = "0x7D7EB8f41b9fe127E6055c6Ad0a00B09d3a88AED"
r_address = "0x21205F43e7Ac29CE1bE70f009774A7B39E011979"
balance = contract.functions.balanceOf(address).call()
g_balance = contract.functions.balanceOf(g_address).call()
r_balance = contract.functions.balanceOf(r_address).call()

## Create Dataframe function

def update_df():
    timestamp = [datetime.datetime.now() for i in range(10)]
    df = pd.DataFrame({'Timestamp': timestamp, 'g_balance': g_balance, 'r_balance': r_balance})

    # Get the current time
    current_time = datetime.datetime.now()

    # Check if 1 minute has passed since the last entry
    if len(df) == 0 or (current_time - df.iloc[-1]['Timestamp']).total_seconds() >= 60:
        # Add a new entry to the dataframe
        df = df.append({'Timestamp': current_time, 'g_balance': g_balance, 'r_balance': r_balance}, ignore_index=True)

    df['Total Votes'] = df['g_balance'] + df['r_balance']
    df['Votes remaining'] = balance
    
    return df

df = update_df()

## Percentage Change function for DateFrame
initial_g_balance = df['g_balance'][0]
initial_r_balance = df['r_balance'][0]
df_change = ((df['g_balance'].sum() - initial_g_balance * len(df)) + (df['r_balance'].sum() - initial_r_balance * len(df))) / (initial_g_balance * len(df) + initial_r_balance * len(df)) * 100
df_g_change = ((df['g_balance'].sum() - initial_g_balance * len(df))) / (initial_g_balance * len(df)) * 100
df_r_change = ((df['r_balance'].sum() - initial_r_balance * len(df))) / (initial_r_balance * len(df)) * 100
df["% Change"] = df_change

## Titie
st.write("# Shareholder Voting Rights Election")
## Subheader
st.write("## Election Overview")
st.write("Today's Election movement:")

# Information Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Gavin Sharp", f"{g_balance}", f"{df_g_change}")
col2.metric("Rochelle Grant", f"{r_balance}", f"{df_r_change}")
col3.metric("Votes Remaining", f"{balance}", f"-{df_change:.2f}%")
col4.metric("Time Remaining", "12hrs", "1Day")


## Create Tabs For User election functions and stats
tab1, tab2, tab3, tab4 = st.tabs(["📈 Gavin Sharp", "🗃 Rochelle Grant", "Vote!", "Election Stats"])

##  Tab 1 - Gavin Sharp
with tab1:
    st.subheader("Gavin Sharp")
    st.write(f"Total Votes: {g_balance}")
    df.drop(columns="r_balance")
    df


##  Tab 2 - Rochelle Grant
with tab2:
    st.subheader("Rochelle Grant")
    st.subheader(f"Total Votes: {r_balance}")

##  Tab 3 - Vote function
with tab3:
    st.subheader("Vote!")
    
    # Input form for registering to vote
    _email = st.text_input("Email")
    _fullName = st.text_input("Full Name")

    # OTP system to authenticate the user
    if st.button("Send OTP"):
     # send OTP logic
        st.success("OTP sent!")

    otp = st.text_input("Enter OTP")
    if st.button("Verify OTP"):
        # verify OTP logic
        with st.spinner('Wait for it...'):
            time.sleep(5)
        st.success("OTP verified!")

    ## Create selectbox with candidates and connect information
    accounts = w3.eth.accounts
    owner=accounts[0]
    candidates = ['Gavin Sharp', 'Rochelle Grant']
    selected_candidate = st.selectbox("Choose a candidate", candidates)

    # Select the relevant address based on the selected candidate
    if selected_candidate == 'Gavin Sharp':
        c_address = accounts[1]
    elif selected_candidate == 'Rochelle Grant':
        c_address = accounts[2]

    # Selection Confirmation
    confirm_selection = st.checkbox(f"I {_fullName} confirm my information and selection '{selected_candidate}' is correct.")
    st.warning('Confirmation Warning: Please make sure your information and selection is correct.', icon="⚠️")
    if confirm_selection:

        ## Cast Vote function
        if st.button("Cast Vote"):
                st.markdown("---")
                tx_hash = contract.functions.vote(
                    w3.toChecksumAddress(c_address),
                    int(otp), 
                    _email,
                    _fullName 

                ).transact({'from': owner, 'gas': 1000000})
                receipt = w3.eth.waitForTransactionReceipt(tx_hash)
                st.write("Transaction receipt mined:")
                st.write(dict(receipt))
                st.markdown("---")
            
            # send voting token logic
                with st.spinner('Wait for it...'):
                    time.sleep(3)
                st.success("Vote cast!")
                st.balloons()
                time.sleep(5)
                st.experimental_rerun()

## Tab 4 - Election Statistics
with tab4:
    st.subheader("Election Statistics")
    df
    st.line_chart(df,  x="Timestamp", y=["g_balance", "r_balance"], use_container_width=True)

    