import streamlit as st
import random
from datetime import datetime
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets Authentication
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("streamlitchatbotdata.json", scope)
    client = gspread.authorize(creds)
    return client

def open_google_sheet(sheet_name="streamlit chatbot data"):
    client = authenticate_google_sheets()
    sheet = client.open(sheet_name).sheet1
    return sheet    

def store_chat_in_google_sheets(user_name, user_message, bot_response):
    try:
        sheet = open_google_sheet()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([user_name, user_message, bot_response, timestamp])
    except Exception as e:
        st.error(f"Error storing data to Google Sheets: {e}")

# Initialize session state
if "user_name" not in st.session_state:
    st.session_state.user_name = None
if "messages" not in st.session_state:
    st.session_state.messages = []
if "name_entered" not in st.session_state:
    st.session_state.name_entered = False
if "chat_started" not in st.session_state:
    st.session_state.chat_started = False
if "conversation_ended" not in st.session_state:
    st.session_state.conversation_ended = False

# Fun greeting messages
greetings = [
    "Hello! What's your name today?",
    "Hey! Let’s start by getting to know you. What’s your name?",
    "Greetings! Tell me your name, and we'll begin our journey."
]

quotes = [
    "Keep smiling! 😄",
    "What do you call a bot with a sense of humor? A chatty-bot! 😂",
    "Life is better with friends—and bots! 🚀"
]

# Page 1: Name Input
if st.session_state.user_name is None or not st.session_state.chat_started:
    st.title("Welcome to Chat BOT! 💡")
    st.subheader("Hi there! I'm your chatbot 🤖. Let's get started!")
    
    current_hour = datetime.now().hour
    if current_hour < 12:
        greeting = "Good Morning! Tell me your name."
    elif current_hour < 18:
        greeting = "Good Afternoon! Tell me your name."
    else:
        greeting = "Good Evening! Ready to chat?"
    
    st.header(greeting)
    st.divider()
    
    user_name = st.text_input("Your Name", key="name_input", placeholder="Type your name here...")
    
    if st.button("Enter"):
        if user_name.strip():
            st.session_state.user_name = user_name.strip()
            st.session_state.name_entered = True
        else:
            st.error("Name cannot be empty. Please enter your name.")
    
    st.write(random.choice(quotes))
    
    if st.session_state.name_entered:
        st.write(f"✨ Welcome, {st.session_state.user_name}")
        st.success("Press the Start Chat button to continue to the chatbot.")

    if st.button("Start Chatting"):
        if st.session_state.name_entered:
            st.session_state.chat_started = True
            with st.spinner("Loading your chatbot..."):
                progress = st.progress(0)
                for i in range(101):
                    time.sleep(0.01)
                    progress.progress(i)
                st.success("Chatbot loaded! 🚀")
        else:
            st.error("Please enter your name and press Enter first.")

# Page 2: Chatbot
elif st.session_state.chat_started and not st.session_state.conversation_ended:
    st.title(f"Welcome, {st.session_state.user_name}! 🤖")
    st.header("Chat BOT: Let's Chat... 🚀")
    st.divider()

    bot_icon = "🤖"
    user_icon = "👨‍💻"

    for message in st.session_state.messages:
        role = user_icon if message["role"] == "user" else bot_icon
        st.write(f"{role}: {message['content']}")

    user_input = st.chat_input("Type your message here...")
    if user_input:
        if user_input.lower() == "delete history":
            st.session_state.messages.clear()
            st.write(f"{bot_icon} : Chat history has been deleted.")
        elif user_input.lower() == "history":
            if st.session_state.messages:
                st.divider()
                st.write(f"{bot_icon} : Here is your chat history:")
                st.divider()
                for msg in st.session_state.messages:
                    role = user_icon if msg["role"] == "user" else bot_icon
                    st.markdown(f"**{role}**: {msg['content']}")
                st.divider()
            else:
                bot_response = "No chat history available."
                st.write(f"{bot_icon} : {bot_response}")
                st.session_state.messages.append({"role": "bot", "content": bot_response})
        elif user_input.lower() == "exit":
            st.write(f"{bot_icon} : Bye, {st.session_state.user_name}!")
            st.session_state.conversation_ended = True
            st.session_state.messages.clear()
        else:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.write(f"{user_icon} : {user_input}")
            
            bot_response = f"You said: {user_input}"
            st.session_state.messages.append({"role": "bot", "content": bot_response})
            st.write(f"{bot_icon} : {bot_response}")
            
            # Store conversation in Google Sheets
            store_chat_in_google_sheets(st.session_state.user_name, user_input, bot_response)

# Page 3: Conversation Ended
elif st.session_state.conversation_ended:
    st.title("Conversation Ended!")
    st.markdown(f"**It was great talking to you, {st.session_state.user_name}!** 😊")
    st.write("Thanks for chatting with me! Hope to see you again soon. 👋")
