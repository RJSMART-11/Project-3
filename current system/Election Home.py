## Imports

import streamlit as st
import pandas as pd
import numpy as np
import time
import streamlit_authenticator as stauth
import plotly as plotly
import bokeh as plt
import os
import json
from web3 import Web3
from pathlib import Path
from dotenv import load_dotenv
from PIL import Image



# Define and connect a new Web3 provider
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
        contract_abi = json.load(f)

    # Set the contract address (this is the address of the deployed contract)
    contract_address = "0x4eE734740c5993f54A71304167Edad08dc4bB9b6"

    # Get the contract
    contract = w3.eth.contract(
        address=contract_address,
        abi=contract_abi
    )

    return contract

# Load the contract
contract = load_contract()

## Call blockchain information
address = "0x9386008bAdE0B1e5DfF07FC187DecB80D8FbBd6c"
balance = contract.functions.balanceOf(address).call()

## Title
st.write("# Election Home")
## Subheader
st.write("## Information")
st.write("Today's Election movement:")

## Column metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Votes", "1000" )
col2.metric("Votes Remaining", f"{balance}")
col3.metric("Time Remaining", "5hrs")

## Crete Tabs for Home Page information
tab1, tab2, tab3 = st.tabs(["📈 Election Home", "🗃 Candidates", "Election Details"])
data = np.random.randn(10, 1)

## Tab 1 - Election Home
with tab1:
    st.subheader("Election Home")
    st.write("")


## Tab 3 - Candidates Details
with tab2:
    st.subheader("Candidates")
    candidates = ['Gavin Sharp', 'Rochelle Grant']
    selected_candidate = st.selectbox("Choose a candidate", candidates)

# Provide information based on the selected candidate

    if selected_candidate == 'Gavin Sharp':
        st.subheader("Professor Gavin Sharp ")
        image = Image.open('Images/Gavin_Sharp.png')
        st.image(image, caption='Gavin Sharp')
        st.subheader("Current Role: CEO and Founding Partner NFT Band")
        st.write("Gavin’s background includes establishing the Centre for IT and Blockchain Studies (CIBS), at Melbourne University in 2015. Previous to heading up the department at CIBS he lead covert research and development programs for the Australian military department and is recognised as a world leading authority in the application of blockchain technology for ballistic missile and defence systems. ")
        st.write("Gavin was one of the founders of NFT bank in 2018 and is actively involved in the day to day operation and growth of the business.In addition to his responsibilities at NFT Bank, Gavin is on the board of directors for Australian Innovation in Aerospace, The Austin Hospital, and is actively involved in the not-for-profit Sperry Street Kids. As someone who cannot sit still and an impossible cinema potato chip bag rustler Gavin has the experience and ability to deliver the goods as chairman of NFT Bank")

    elif selected_candidate == 'Rochelle Grant':
        st.subheader("Rochelle Grant ")
        image = Image.open('Images/Rochelle Grant.png')
        st.image(image, caption='Rochelle Grant')
        st.subheader("Current Role: Acting Chairperson NFTBank")
        st.write("Previous roles as Head of Innovation and Technology at Deloitte, and Partner for Technology Innovation at Accenture, Rochelle Grant has the experience and demonstrated outstanding ability to take world class organisations to the forefront of the digital eco-system. Rochelle’s successes include the implementation of a secure blockchain based healthcare and patient record keeping system for the United Kingdom, and the transfer of client records to a anonymous and hacker proof blockchain database for Medibank in Australia.")
        st.write("Rochelle is an advisor the Australian Federal Government’s Future Innovation and Technolgy think tank, is a board member of The Royal Children’s Hospital, World Wildlife Fund and the St Kilda Drum for Fun social group. She is a woeful drummer, but a chronic over achiever and probably perfectly suited to the role of Chairperson at NFT Bank.")


    ## Tab 3 - Election Details
with tab3:
    st.subheader("Election Details")
    st.write("Total Vote supply: 1000")
    st.write(f"Total Remaining: {balance}")
    st.write("Duration:")
    st.write("Voting Rules: ")
    st.write("- One vote per shareholder")
    st.write("- OTP require to authenticate Identification")
    st.write("- All votes are required to be entered by the end of the'Election Duration' to be deemed as vaild")



