import streamlit as st
import os
import google.generativeai as genai
import time
from dotenv import load_dotenv

def configure():
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
        response = st.session_state.chat_session.send_message(question)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "An error occurred. Please try again."

# Streamlit App setup
st.set_page_config(page_title="TravelBuddy - Your Virtual Travel Assistant")
st.header("TravelBuddy - Your Virtual Travel Assistant")

# Streamlit Sidebar Inputs for initial planning
st.sidebar.title('🗺️ Trip Planner')
st.sidebar.write('Plan your trip effortlessly with TravelBuddy!')

# Collect initial trip information
place_input = st.sidebar.text_input("Where are you planning to go?")
duration_input = st.sidebar.text_input("How many days will you stay?")
people_input = st.sidebar.text_input("How many people are going?")

# Multi-Level Prompting
activity_input = st.sidebar.text_input("What kind of activities are you interested in? (e.g., hiking, city tour, beach)")
accommodation_input = st.sidebar.text_input("What type of accommodation do you prefer? (e.g., hotel, hostel, apartment)")
budget_input = st.sidebar.text_input("What is your budget per person? (in USD)")

# Generate the itinerary and expenses
if st.sidebar.button('Plan my trip'):
    if place_input and duration_input and people_input and activity_input and accommodation_input and budget_input:
        basic_info = f"Plan a trip to {place_input} for {duration_input} days for {people_input} people."
        detailed_info = f"Activities include: {activity_input}. Accommodation type: {accommodation_input}. Budget per person: {budget_input} USD."
        final_question = f"{basic_info} {detailed_info} Include an itinerary and expected expenses."
        
        response = handle_chat(final_question)
        st.subheader("Here's your detailed trip plan:")
        st.write(response)
    else:
        st.sidebar.error("Please fill in all the fields to proceed with the detailed trip plan.")

# Function to display chat history (optional)
def display_history():
    with st.container():
        for entry in st.session_state.chat_history:
            if entry['type'] == "Question":
                st.markdown(f"<p style='font-size:16px; font-weight:bold;'>Your Inquiry:</p><p style='font-size:16px;'>{entry['content']}</p>", unsafe_allow_html=True)
            elif entry['type'] == "Response":
                st.markdown(f"<p style='font-size:16px; font-weight:bold;'>Response from TravelBuddy:</p><p style='font-size:16px;'>{entry['content']}</p>", unsafe_allow_html=True)

display_history()
