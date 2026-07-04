import streamlit as st

if "question_count" not in st.session_state:
    st.session_state.question_count = 0
else:
    st.session_state.question_count += 1

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

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=st.session_state.messages
    )

    answer = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": answer})

    st.write("### Answer:")
    st.write(answer)

st.sidebar.write("📊 Usage Tracking")
st.sidebar.write(f"Questions asked: {st.session_state.question_count}")
