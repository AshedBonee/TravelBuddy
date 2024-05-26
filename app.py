import streamlit as st
import os
import google.generativeai as genai
import time
from dotenv import load_dotenv
import pandas as pd

def configure():
    load_dotenv()

configure()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable with your Gemini API key.")
    exit()

genai.configure(api_key=API_KEY)

if 'chat_session' not in st.session_state:
    model = genai.GenerativeModel('gemini-1.5-pro')
    st.session_state.chat_session = model.start_chat()
    st.session_state.chat_history = []

def handle_chat(question):
    try:
        intro_response = "Hello! I am TravelBuddy, your virtual travel assistant. Let's plan your trip together."
        response = st.session_state.chat_session.send_message(question)
        full_response = f"{intro_response} {response.text} Anything else I can help you with?"
        st.session_state.chat_history.append({"type": "Question", "content": question})
        st.session_state.chat_history.append({"type": "Response", "content": full_response})
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        time.sleep(1)
        return None

def display_history():
    with st.container():
        for entry in st.session_state.chat_history:
            if entry['type'] == "Question":
                st.markdown(f"<p style='font-size:16px; font-weight:bold;'>Your Inquiry:</p><p style='font-size:16px;'>{entry['content']}</p>", unsafe_allow_html=True)
            elif entry['type'] == "Response":
                formatted_response = entry['content'].replace("**", "<b>").replace("<b>", "</b>")
                st.markdown(f"<p style='font-size:16px; font-weight:bold;'>Response from TravelBuddy:</p><p style='font-size:16px;'>{formatted_response}</p>", unsafe_allow_html=True)

st.set_page_config(page_title="TravelBuddy - Your Virtual Travel Assistant")
st.header("TravelBuddy - Your Virtual Travel Assistant")
st.sidebar.title('🗺️ Trip Planner')
st.sidebar.write('Plan your trip effortlessly with TravelBuddy!')
place_input = st.sidebar.text_input("Where are you planning to go?")
duration_input = st.sidebar.text_input("How many days will you stay?")
people_input = st.sidebar.text_input("How many people are going?")

if st.sidebar.button('Plan my trip'):
    if place_input and duration_input and people_input:
        question = f"Plan a trip to {place_input} for {duration_input} days for {people_input} people. Include an itinerary and expected expenses."
        response = handle_chat(question)
        if response:
            try:
                data = [item.strip().split(',') for item in response.split(';') if item.strip()]
                if all(len(x) == 3 for x in data):  # Check if all items have 3 elements
                    df = pd.DataFrame(data, columns=['Day', 'Activity', 'Cost'])
                    st.subheader("Here's your trip plan in a table format:")
                    st.table(df)
                else:
                    st.error("Received data is not in the expected format.")
            except Exception as e:
                st.error(f"An error occurred while parsing the data: {str(e)}")
        else:
            st.write("Could not retrieve a valid response for itinerary planning.")
    else:
        st.sidebar.error("Please fill in all the fields.")

display_history()
