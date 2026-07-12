import os
import uuid

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader

load_dotenv()

from posthog import Posthog

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

st.title("📄 Insurance PDF Broker Assistant")

# Upload PDF
uploaded_file = st.file_uploader("Upload Insurance Policy PDF", type=["pdf"])

def extract_text(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

if uploaded_file:
    pdf_text = extract_text(uploaded_file)

    posthog.capture(
        distinct_id=session_id,
        event="pdf_uploaded",
        properties={"extraction_successful": bool(pdf_text)},
    )

    st.success("PDF loaded successfully!")

    question = st.text_input("Ask a question about this policy:")

    if question:
        posthog.capture(
            distinct_id=session_id,
            event="pdf_question_asked",
            properties={"message_length": len(question)},
        )

        try:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=[
                    {
                        "role": "system",
                        "content": (
                            "You are a senior commercial insurance expert. "
                            "Answer ONLY using the provided policy document. "
                            "If information is missing, say you cannot find it in the document."
                        )
                    },
                    {
                        "role": "user",
                        "content": f"POLICY DOCUMENT:\n{pdf_text}\n\nQUESTION:\n{question}"
                    }
                ]
            )

            st.write("### Answer:")
            st.write(response.output_text)
        except Exception as e:
            posthog.capture_exception(e, distinct_id=session_id)
            raise
