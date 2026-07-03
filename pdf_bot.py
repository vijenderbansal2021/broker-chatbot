import streamlit as st
from openai import OpenAI
from pypdf import PdfReader

client = OpenAI()

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

    st.success("PDF loaded successfully!")

    question = st.text_input("Ask a question about this policy:")

    if question:
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