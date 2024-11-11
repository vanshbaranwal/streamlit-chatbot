import streamlit as st


# Set up session state for storing messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Title and header
st.title("Chat BOT! 💡")
st.header("Let's Chat..🚀🚀")

bot_icon="🧠"
user_icon="👨‍💻"

# Display previous messages
for message in st.session_state.messages:
    role = user_icon if message["role"] == "user" else bot_icon
    st.write(f"{role}: {message['content']}\n")

# User input and bot response
user_input = st.chat_input("Type your message here...")

# Process user input if it exists
if user_input:
    # Check if the user wants to delete history
    if user_input.lower() == "delete history":
        st.session_state.messages.clear()
        st.write(f"{bot_icon} Chat history has been deleted.")
    
    # Check if the user wants to view history
    elif user_input.lower() == "history":
        # Compile chat history
        history = "\n".join(
            [f"\n{user_icon if msg['role'] == 'user' else bot_icon}: {msg['content']}\n" 
             for msg in st.session_state.messages]
        )
        bot_response = f"Here is your chat history:\n{history}\n" if history else "No chat history available."
        
        # Display bot response with history
        st.write(f"{bot_icon} {bot_response}")
        st.session_state.messages.append({"role": "bot", "content": bot_response})
    
    # Normal echo response
    else:
        # Add user message to session state
        st.session_state.messages.append({"role": "user", "content": user_input})

        # Display user message
        st.write(f"{user_icon} {user_input}")

        # Echo response from the bot
        bot_response = f"You said: {user_input}"
        st.session_state.messages.append({"role": "bot", "content": bot_response})

        # Display bot response
        st.write(f"{bot_icon} {bot_response}")