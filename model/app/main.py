from openai import OpenAI
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("API_KEY"), base_url=os.getenv("BASE_URL"))

st.title("Sample Chat App")
prompt = st.text_area("Enter your prompt: ", "How are you ?")

if st.button("send"):
    with st.spinner("Getting response..."):
        messages = [
            {
                "role":"user",
                "content":prompt
            }
        ]

        try:
            response = client.chat.completions.create(
                model= os.getenv("MODEL"),
                messages= messages
            )
            st.success("Response:")
            st.write(response.choices[0].message.content)

        except Exception as e:
            st.write(e)
