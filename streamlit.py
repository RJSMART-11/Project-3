import streamlit as st
import re
import json

from smtp_authorization import SMTPauthorizer

# Read the secret data from env file
with open("env", "r") as f:
    secret = json.loads(f.read())


@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return SMTPauthorizer(secret)


st.markdown("# New Zealand - Blockchain Voting System")
st.markdown("## Enter your email to confirm your identity we will send you a code. Please enter your email.")

so = setup()
email = st.text_input("Your email")
input_amount = st.text_input("Verification code")

if so.email_is_valid(email) and not input_amount:
    so.send_confirmation_code(email=email)
    st.write(f'Email {email} is valid! We sent code to you. Check your mail.')

elif so.last_confirmation_code and so.confirm_email(code=input_amount):
    st.write(f'Thank you! Your email is confirmed.')
    st.balloons()
elif re.fullmatch(re.compile(r'[\d]{6}'), email)  and  input_amount :
    st.write(f'You entered a wrong code.')
elif  not input_amount:
    st.write(f'Email {email} is not valid! Try again.')
else:
    st.write(f'Try again.')



