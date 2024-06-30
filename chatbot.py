import streamlit as st
from hugchat import hugchat
from hugchat.login import Login

# Function for generating LLM response
def generate_response(prompt_input, email, passwd):
    # Hugging Face Login
    sign = Login(email, passwd)
    cookies = sign.login()

    # Create ChatBot
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

    return chatbot.chat(prompt_input)


def main():
    st.title('Simple Chatbot')

    with st.sidebar:
        st.title('Login HugChat')

        email = st.text_input('Enter E-mail')
        password = st.text_input('Enter Password', type='password')

        if not email or not password:
            st.warning('Please enter your account!')
        else:
            st.success('Login details provided')

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": "How may I help you?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # User-provided prompt
    if prompt := st.chat_input(disabled=not (email and password)):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

        # Generate a new response if the last message is not from assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_response(prompt, email, password)
                    st.write(response)
                    message = {"role": "assistant", "content": response}
                    st.session_state.messages.append(message)


if __name__ == "__main__":
    main()
