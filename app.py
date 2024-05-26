import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

def configure():
    load_dotenv()  # Load environment variables

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
        st.session_state.chat_history.append({'type': 'Question', 'content': question})
        st.session_state.chat_history.append({'type': 'Response', 'content': response.text})
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return "An error occurred. Please try again."

# Streamlit App setup
st.set_page_config(page_title="TravelBuddy - Your Virtual Travel Assistant")
st.header("TravelBuddy - Your Virtual Travel Assistant")

# Collect initial trip information
place_input = st.text_input("Where are you planning to go?")
duration_input = st.text_input("How many days will you stay?")
people_input = st.text_input("How many people are going?")

if st.button('Generate Trip Information'):
    if place_input and duration_input and people_input:
        basic_info = f"Plan a trip to {place_input} for {duration_input} days for {people_input} people."
        response = handle_chat(basic_info)
        st.subheader("Here's your initial trip information:")
        st.write(response)
    else:
        st.error("Please fill in all the fields to proceed with the initial trip information.")

# Allow for follow-up questions
follow_up_question = st.text_input("Have any follow-up questions? Ask here:")
if st.button('Ask'):
    if follow_up_question:
        response = handle_chat(follow_up_question)
        st.write(response)

# Function to display chat history (optional)
def display_history():
    with st.container():
        for entry in st.session_state.chat_history:
            if entry['type'] == "Question":
                st.markdown(f"<p style='font-size:16px; font-weight:bold;'>Your Inquiry:</p><p style='font-size:16px;'>{entry['content']}</p>", unsafe_allow_html=True)
            elif entry['type'] == "Response":
                st.markdown(f"<p style='font-size:16px; font-weight:bold;'>Response from TravelBuddy:</p><p style='font-size:16px;'>{entry['content']}</p>", unsafe_allow_html=True)

display_history()
