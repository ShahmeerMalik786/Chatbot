import streamlit as st
import google.generativeai as genai

# Configure generativeai library
genai.configure(api_key="AIzaSyCm70VZ7dxFzRIPx3_3ZSvW-LG3wZLb4fA")

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel(model_name="gemini-pro", generation_config=generation_config)

# Create a session state to persist data
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

def on_submit():
    user_input = st.session_state.user_input
    if user_input:
        # Store user input in the chat history
        st.session_state.chat_history.append(("User", user_input))

        # Generate response
        response = model.generate_content([user_input])

        # Print the response for debugging
        st.write("Raw Response:", response)

        # Check if response.parts is available
        if hasattr(response, 'parts') and response.parts:
            # Assuming response.parts[0].text is a property available in your response
            try:
                response_text = response.parts[0].text
            except AttributeError:
                # If response.parts[0].text is not available, try another approach based on the response structure
                response_text = str(response.parts[0])  # Convert the response object to a string
        else:
            # Use an alternative approach based on the response structure
            response_text = str(response)  # Convert the response object to a string

        # Store chatbot response in the chat history
        st.session_state.chat_history.append(("Chatbot", response_text))

        # Clear the user input after submitting
        st.session_state.user_input = ""

def main():
    st.title("Chatbot App")

    # Listen for changes in the text_input
    st.text_input("You:", key="user_input", on_change=on_submit, args=())

    if st.button("Submit"):
        on_submit()

    # Display chat history
    st.text("Chat History:")
    for speaker, message in st.session_state.chat_history:
        st.text(f"{speaker}: {message}")

if __name__ == "__main__":
    main()
