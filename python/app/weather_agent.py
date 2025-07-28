import streamlit as st
import requests
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()

def get_weather(city):
    try:
        response = requests.get(f"https://wttr.in/{city}?format=%C+%t")
        if response.status_code == 200:
            return response.text.strip()
        else:
            return "Sorry, couldn't fetch weather data."
    except:
        return "Error connecting to weather service."

def ask_openai(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful weather assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"OpenAI error: {str(e)}"

# Streamlit UI
st.title("🌤️ Weather AI Assistant")

user_city = st.text_input("Enter city name:")
if user_city:
    weather_info = get_weather(user_city)
    st.success(f"Weather in {user_city}: {weather_info}")

    # Ask AI
    user_question = st.text_input("Ask something about the weather:")
    if user_question:
        ai_prompt = f"The weather in {user_city} is {weather_info}. User asked: {user_question}"
        ai_response = ask_openai(ai_prompt)
        st.info("🤖AI:")
        st.write(ai_response)
