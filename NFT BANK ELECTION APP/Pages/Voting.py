## Imports

import streamlit as st
import pandas as pd
import hvplot.pandas
import numpy as np
import hvplot.pandas
import time
import plotly.express as px  # interactive charts
import bokeh as plt
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
import datetime
import re
import os
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Load in SMTP for OTP verification
GM_PASS="jltsmqhrjpafmsmp"
GM_LOGIN="protect3vote@gmail.com"

class SMTPauthorizer:
    def __init__(self, num_len=6):
        self.random_number = "".join([str(random.randint(1, 9)) for i in range(0, num_len)])
        self.re4mail = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        self.last_confirmation_code = None

    def email_is_valid(self, email):
        return bool(re.fullmatch(self.re4mail, email))

    def send_confirmation_code(self, email):
        message = MIMEMultipart()
        message['From'] = GM_LOGIN
        message['To'] = email
        message['Subject'] = 'auth'
        message.attach(MIMEText(self.random_number, 'plain'))
        with smtplib.SMTP('smtp.gmail.com', 587) as session:
            session.starttls()
            session.login(GM_LOGIN, GM_PASS)
            text = message.as_string()
            session.sendmail(GM_LOGIN, email, text)
            session.quit()
        self.last_confirmation_code = self.random_number

    def confirm_email(self, code):
        assert self.last_confirmation_code, "First send an email! There is nothing to check here."
        return code == self.random_number



## Define and connect a new Web3 provider
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

################################################################################
# Contract Helper function:
# 1. Loads the contract once using cache
# 2. Connects to the contract using the contract address and ABI
################################################################################


@st.cache(allow_output_mutation=True)
def make_otp():
    return SMTPauthorizer()

email_verifier = make_otp()
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

#load in Contract/Ganache Addresses
address = "0x9386008bAdE0B1e5DfF07FC187DecB80D8FbBd6c"
g_address = "0x7D7EB8f41b9fe127E6055c6Ad0a00B09d3a88AED"
r_address = "0x21205F43e7Ac29CE1bE70f009774A7B39E011979"
balance = contract.functions.balanceOf(address).call()
g_balance = contract.functions.balanceOf(g_address).call()
r_balance = contract.functions.balanceOf(r_address).call()
num_voted = 1000 - balance

## Create Dataframe function
def update_df():
    # Get the current time
    current_time = datetime.datetime.now()

    # Read the existing dataframe from the file
    try:
        df = pd.read_csv('Election_results_DF.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=['Timestamp', 'Gavin Sharp', 'Rochelle Grant', 'Voted', 'Votes Remaining'])

    # Add a new entry to the dataframe
    new_entry = pd.DataFrame({'Timestamp': [current_time], 'Gavin Sharp': [g_balance], 'Rochelle Grant': [r_balance], 'Voted' : [num_voted], 'Votes Remaining' : [balance]})
    df = df.append(new_entry, ignore_index=True)
    # Save the dataframe to the csv file
    df.to_csv('Election_results_DF.csv', index=False)
    
    return df
#Load Updated dataframe
new_df = pd.read_csv('Election_results_DF.csv')
new_df['pct_change'] = new_df['Votes Remaining'].pct_change()

## Title
st.write("# Shareholder Voting Rights Election")
## Subheader
st.write("## Election Overview")
st.write("Current Election Statistics:")

# Information Metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Gavin Sharp", f"{g_balance}", )
col2.metric("Rochelle Grant", f"{r_balance}", )
col3.metric("Votes Remaining", f"{balance}", )
col4.metric("Voted", f"{num_voted}")

#Initate SMPTauthorizer for OTP
otp_verifier = SMTPauthorizer()

## Create Tabs For User election functions and stats
tab1, tab2,  = st.tabs(["📈Election Stats", "Vote!"])


## Tab 1 - Election Statistics
with tab1:
    st.subheader("Voting Statistics")
    category = ['Overall', 'Gavin Sharp', 'Rochelle Grant']
    selected_category = st.selectbox("Choose a category", category)

# Provide statsistical information based on the election and selected candidate

    if selected_category == 'Overall':
        st.subheader("Overall Election Statistics")
        st.write(f"**Total Votes: {num_voted}    Votes Remaining : {balance}**   / **Votes for Candidates - Gavin Sharp : {g_balance}   Rochelle Grant: {r_balance}**")
        st.bar_chart(data=new_df, x="Timestamp", y=["Gavin Sharp", "Rochelle Grant"], use_container_width=True)
        st.line_chart(new_df, x="Timestamp", y=["Gavin Sharp", "Rochelle Grant"])
        st.write(new_df)

    elif selected_category == 'Gavin Sharp':
        st.subheader("Gavin Sharp")
        st.write(f"**Total Votes: {g_balance}**")
        st.line_chart(new_df, x="Timestamp", y=["Gavin Sharp"])

    elif selected_category == 'Rochelle Grant':
        st.subheader("Rochelle Grant ")
        st.write(f"**Total Votes: {r_balance}**")
        st.line_chart(new_df, x="Timestamp", y=["Rochelle Grant"])

##  Tab 3 - Vote function
with tab2:
    st.subheader("Vote!")
    # Input form for registering to vote
    _email = st.text_input("Email")
    _fullName = st.text_input("Full Name")
    # OTP system to authenticate the user
    if st.button("Send OTP"):
        # send OTP logic
        if email_verifier.email_is_valid(_email):
            email_verifier.send_confirmation_code(_email)
            st.success("OTP sent!")
        else:
            st.error("Invalid email address")
    is_otp_verified = False
    otp = st.text_input("Enter OTP")
    if st.button("Verify OTP"):
        # verify OTP logic
        with st.spinner('Wait for it...'):
            time.sleep(5)
        print(otp, email_verifier.random_number)
        if email_verifier.confirm_email(otp):
            st.success("OTP verified!")
            is_otp_verified = True
        else:
            st.error("Incorrect OTP. Please try again.")
   ## Create selectbox with candidates and connect information
    accounts = w3.eth.accounts
    owner = accounts[0]
    candidates = ['------', 'Gavin Sharp', 'Rochelle Grant']
    selected_candidate = st.selectbox("Choose a candidate", candidates)

    # Select the relevant address based on the selected candidate
    if selected_candidate == 'Gavin Sharp':
        c_address = accounts[1]
    elif selected_candidate == 'Rochelle Grant':
        c_address = accounts[2]

    # Selection Confirmation
    confirm_selection = st.checkbox(
        f"I **'{_fullName}'** consent to my photo being taken for identification purposes and also confirm my personal information and selection of **'{selected_candidate}'** is correct.")
    st.warning('Confirmation Warning: Please make sure your information and selection is correct.', icon="⚠️")
    if confirm_selection:
        st.success('Thank you, please proceed.', icon="✅")
        ## Photo/ID verification
        picture = st.camera_input("Take a picture", key="1")

        if picture:
            filename = f'{_fullName}.jpg'
            filepath = os.path.join('Images/Photo verification', filename)
            with open(filepath, 'wb') as file:
                file.write(picture.getbuffer())

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
                update_df()
                st.balloons()
                time.sleep(5)
                st.experimental_rerun()
                
