import streamlit as st
import requests

st.set_page_config(page_title="Clinical RAG – Hypertension")

st.title("🩺 Clinical RAG – Hypertension")
st.write("Ask an evidence-based clinical question about adult hypertension.")

question = st.text_area(
    "Enter your question:",
    placeholder="e.g. What is the first-line treatment for stage 1 hypertension?"
)

if st.button("Submit"):
    if question.strip() == "":
        st.warning("Please enter a question.")
    else:
        with st.spinner("Retrieving evidence-based answer..."):
            response = requests.post(
                "http://127.0.0.1:8000/query",
                json={"question": question},
                timeout=60
            )

        if response.status_code == 200:
            answer = response.json()["answer"]
            st.subheader("Answer")
            st.write(answer)
        else:
            st.error("Error contacting backend.")
