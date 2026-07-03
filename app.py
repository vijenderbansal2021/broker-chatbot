import streamlit as st
from openai import OpenAI

client = OpenAI()

st.title("🏦 Insurance Broker AI Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a senior commercial insurance broker with 20+ years of experience."
        }
    ]

user_input = st.text_input("Ask your insurance question:")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=st.session_state.messages
    )

    answer = response.output_text

    st.session_state.messages.append({"role": "assistant", "content": answer})

    st.write("### Answer:")
    st.write(answer)