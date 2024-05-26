# TravelBuddy - Your Virtual Travel Assistant

TravelBuddy is a Streamlit-based web application designed to simplify your travel planning process. By interacting with a generative AI, TravelBuddy helps you create personalized travel itineraries based on your preferences for destination, duration, activities, accommodation type, and budget.

## Features
- **Interactive Trip Planning**: Input your travel details such as destination, duration, number of people, and preferences to get a customized travel plan.
- **Multi-Level Prompting**: The app engages you in a multi-level input process to refine the travel plans based on activities, accommodations, and budget.
- **Real-Time AI Interaction**: Uses Google's Generative AI to generate travel plans and itineraries dynamically.

## Setup Instructions

### Prerequisites
- Python 3.8+
- Streamlit
- An API key for Google's Generative AI services

### Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourgithubusername/travelbuddy.git
   cd travelbuddy
   
2. **Install dependencies:**
   ```bash
   Copy code
   pip install -r requirements.txt
   Set up environment variables:

3. **Create a .env file in the root directory of the project and add the following line:**
   ```bash
   plaintext
   Copy code
   GOOGLE_API_KEY=your_api_key_here
   Replace your_api_key_here with your actual API key for Google's Generative AI.

4. **Run the application:**
   ```bash
   Copy code
   streamlit run app.py

## How to Use
1. Input Basic Information:
   - Specify the destination, duration, and number of people traveling.
   - Specify Preferences:

2. Choose the types of activities you are interested in.
   - Select your preferred type of accommodation.
   - Define your budget per person in USD.
  
3. Generate Itinerary:
   - Click on 'Plan my trip' to generate a detailed itinerary including expected expenses.

## Contributing
Contributions to improve TravelBuddy are welcome. Please feel free to fork the repository, make changes, and submit pull requests. You can also open issues to discuss improvements or offer suggestions.

## Link
https://travelbuddy-chichirita.streamlit.app/
