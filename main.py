import streamlit as st
import openai
# import os
# from os.path import join, dirname
# from dotenv import load_dotenv

# api key setting for local
# load_dotenv(join(dirname(__file__), '.env'))
# openai.api_key = os.environ.get("API_KEY")

# api key setting for deploy
openai.api_key = st.secrets.ChatGptKey.key


# ask openai when send-button clicked
def ask_chatgpt():

    # setting character
    condition = 'あなたは' + st.session_state.condition_input.strip() + 'です。'
    if condition and condition != st.session_state.condition:
        st.session_state.condition = condition
        st.session_state.messages.append({"role": "system", "content": condition})

    # setting question
    question = st.session_state.question_input.strip()
    if question:
        # add question
        st.session_state.messages.append({"role": "user", "content": question})
        st.session_state.question_input = ""

        # make response
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages
        )

        # add response to session
        st.session_state.messages.append(response.choices[0]["message"])


def main():

    # show title
    st.title("Character ChatBot")

    # initialize
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.condition = ""

    # choose character
    st.selectbox(
        'I am ',
        ['うずまきナルト', 'ルフィ', 'ピカチュウ', '坂田銀時'],
        key='condition_input'
    )

    # input question
    st.text_input("ask me anything !", key="question_input")

    # button click
    st.button("ask", on_click=ask_chatgpt)

    # show question and answer
    col1, col2 = st.columns(2)
    for message in st.session_state.messages:
        if message["role"] == "user":
            col1.write(message["content"])
        elif message["role"] == "assistant":
            col2.write(message["content"])
            col1, col2 = st.columns(2)


if __name__ == "__main__":
    main()
