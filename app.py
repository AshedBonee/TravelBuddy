import streamlit as st
import os
import google.generativeai as genai
from dotenv import load_dotenv

def configure():
    load_dotenv()  # Load environment variables from .env file for secure access

configure()  # Call configure function to initialize loading of environment variables

# Load API key from environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    st.error("Please set the GOOGLE_API_KEY environment variable with your Gemini API key.")
    exit()  # Exit the script if API key is not set, indicating a configuration error

# Configure the Gemini API with the obtained API key
genai.configure(api_key=API_KEY)

# Initialize or retrieve an existing chat session in the Streamlit session state
if 'chat_session' not in st.session_state:
    model = genai.GenerativeModel('gemini-1.5-pro')
    st.session_state.chat_session = model.start_chat()  # Start a new chat session with the API
    st.session_state.chat_history = []  # Initialize an empty list to track chat history

def handle_chat(question):
    try:
        response = st.session_state.chat_session.send_message(question)  # Send question to chat API and receive response
        return response.text  # Return only the text part of the response
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")  # Display error message in the Streamlit app
        return "An error occurred. Please try again."

# Streamlit App setup
st.set_page_config(page_title="TravelBuddy - Your Virtual Travel Assistant")
st.header("TravelBuddy - Your Virtual Travel Assistant")

# Sidebar inputs for trip planning
st.sidebar.title('🗺️ Trip Planner')
st.sidebar.write('Plan your trip effortlessly with TravelBuddy!')
place_input = st.sidebar.text_input("Where are you planning to go?")
duration_input = st.sidebar.text_input("How many days will you stay?")
people_input = st.sidebar.text_input("How many people are going?")
activity_input = st.sidebar.text_input("What kind of activities are you interested in? (e.g., hiking, city tour, beach)")
accommodation_input = st.sidebar.text_input("What type of accommodation do you prefer? (e.g., hotel, hostel, apartment)")
budget_input = st.sidebar.text_input("What is your budget per person? (in USD)")

# Button to generate the initial trip plan
if st.sidebar.button('Plan my trip'):
    if place_input and duration_input and people_input and activity_input and accommodation_input and budget_input:
        basic_info = f"Plan a trip to {place_input} for {duration_input} days for {people_input} with a budget of {budget_input} USD."
        detailed_info = f"Activities include: {activity_input}. Accommodation type: {accommodation_input}."
        final_question = f"{basic_info} {detailed_info} Include itinerary and expected expenses."
        
        response = handle_chat(final_question)  # Get response for the detailed trip plan
        st.session_state.chat_history.append({"type": "Question", "content": final_question})
        st.session_state.chat_history.append({"type": "Response", "content": response})
        
        st.subheader("Here's your detailed trip plan:")
        st.write(response)
    else:
        st.sidebar.error("Please fill in all the fields to proceed with the detailed trip plan.")

# Function to allow follow-up questions
def follow_up_question():
    follow_up = st.text_input("Ask a follow-up question:")
    if st.button("Submit Follow-up"):
        if follow_up:
            response = handle_chat(follow_up)  # Process and display response to follow-up questions
            st.session_state.chat_history.append({"type": "Question", "content": follow_up})
            st.session_state.chat_history.append({"type": "Response", "content": response})
            st.subheader("Response to your follow-up question:")
            st.write(response)
        else:
            st.error("Please enter a follow-up question.")

# Display follow-up question function
follow_up_question()
