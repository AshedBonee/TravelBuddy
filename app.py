import streamlit as st
import os
import google.generativeai as genai
import time
from dotenv import load_dotenv

def configure():
    # Ensures environment variables are loaded from .env file
    load_dotenv()  # Fixed: Call the function to actually load the environment variables

configure()  # Call configure to load environment variables before using them

# Load API key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable with your Gemini API key.")
    exit()

# Configures the Gemini API with the obtained API key.
genai.configure(api_key=API_KEY)

# Check if a chat session exists, if not, initialize a new one.
if 'chat_session' not in st.session_state:
    model = genai.GenerativeModel('gemini-1.5-pro')
    st.session_state.chat_session = model.start_chat()
    st.session_state.chat_history = []  # Initialize chat history

def handle_chat(question):
    try:
        intro_response = "Hello! I am TravelBuddy, your virtual travel assistant. Let's plan your trip together."
        response = st.session_state.chat_session.send_message(question)
        full_response = f"{intro_response} {response.text} Anything else I can help you with?"

        st.session_state.chat_history.append({"type": "Question", "content": question})
        st.session_state.chat_history.append({"type": "Response", "content": full_response})
        return full_response
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        time.sleep(1)  # Slight delay to simulate thought process
        return "An error occurred. Please try again."

def display_history():
    with st.container():
        for entry in st.session_state.chat_history:
            if entry['type'] == "Question":
                st.markdown(f"<p style='font-size:16px; font-weight:bold;'>Your Inquiry:</p><p style='font-size:16px;'>{entry['content']}</p>", unsafe_allow_html=True)
            elif entry['type'] == "Response":
                formatted_response = entry['content'].replace("**", "<b>").replace("<b>", "</b>")
                st.markdown(f"<p style='font-size:16px; font-weight:bold;'>Response from TravelBuddy:</p><p style='font-size:16px;'>{formatted_response}</p>", unsafe_allow_html=True)

# Streamlit App setup
st.set_page_config(page_title="TravelBuddy - Your Virtual Travel Assistant")
st.header("TravelBuddy - Your Virtual Travel Assistant")

# Streamlit Sidebar Inputs
st.sidebar.title('🗺️ Trip Planner')
st.sidebar.write('Plan your trip effortlessly with TravelBuddy!')

place_input = st.sidebar.text_input("Where are you planning to go?")
duration_input = st.sidebar.text_input("How many days will you stay?")
people_input = st.sidebar.text_input("How many people are going?")

# Generate the itinerary and expenses
if st.sidebar.button('Plan my trip'):
    if place_input and duration_input and people_input:
        question = f"Plan a trip to {place_input} for {duration_input} days for {people_input} people. Include an itinerary and expected expenses."
        response = handle_chat(question)
        st.subheader("Here's your trip plan:")
        st.write(response)
    else:
        st.sidebar.error("Please fill in all the fields.")

# Display chat history
display_history()
