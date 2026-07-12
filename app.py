import os
import uuid

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from openai import OpenAI
from posthog import Posthog

if "question_count" not in st.session_state:
    st.session_state.question_count = 0
else:
    st.session_state.question_count += 1

if "posthog_session_id" not in st.session_state:
    st.session_state.posthog_session_id = str(uuid.uuid4())

if "posthog" not in st.session_state:
    st.session_state.posthog = Posthog(
        os.environ.get("POSTHOG_PROJECT_TOKEN", ""),
        host=os.environ.get("POSTHOG_HOST", "https://us.i.posthog.com"),
        enable_exception_autocapture=True,
    )

client = OpenAI()
posthog = st.session_state.posthog
session_id = st.session_state.posthog_session_id

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

    posthog.capture(
        distinct_id=session_id,
        event="question_asked",
        properties={
            "message_length": len(user_input),
            "question_count": st.session_state.question_count,
        },
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=st.session_state.messages
        )

        answer = response.choices[0].message.content

        st.session_state.messages.append({"role": "assistant", "content": answer})

        st.write("### Answer:")
        st.write(answer)
    except Exception as e:
        posthog.capture_exception(e, distinct_id=session_id)
        raise

st.sidebar.write("📊 Usage Tracking")
st.sidebar.write(f"Questions asked: {st.session_state.question_count}")
