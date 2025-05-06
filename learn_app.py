import streamlit as st
from groq import Groq
import os 

st.set_page_config(page_title="Summarizer", page_icon="💬", layout="centered")
st.title("💬 Groq Summarizer")


groq_api_key = None
groq_api_key = st.secrets.get("GROQ_API_KEY")
if not groq_api_key:
    st.error("NO API KEY FOUND")
    st.stop()

selected_model = "llama3-8b-8192"
if 'summary_output' not in st.session_state:
    st.session_state.summary_output = "" 


st.subheader("Enter Text to Summarize")
text_to_summarize = st.text_area("Paste your text here:", height=100, key="input_textarea")
submit_text_button = st.button("Generate Summary")

if submit_text_button:
    st.session_state.summary_output = "" 
    if not text_to_summarize:
        st.warning("Please enter some text in the text area above.", icon="🚨")
    else:
        with st.spinner(f"Summarizing text with {selected_model}..."):
                client = Groq(api_key=groq_api_key)
                messages = [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that summarizes text concisely and accurately.You provide the summaries in points"
                    },
                    {
                        "role": "user",
                        "content": f"Please summarize the following text:\n\n{text_to_summarize}"
                    }
                ]
                chat_completion = client.chat.completions.create(
                    messages=messages,
                    model=selected_model,
                    temperature=0.3,
                    max_tokens=1024,
                    top_p=0.9
                )
                summary = chat_completion.choices[0].message.content
                st.session_state.summary_output = summary # Store result
                st.success("Text summary generated!")

st.divider()
st.subheader("Summary Result")
if st.session_state.summary_output:
    st.markdown(st.session_state.summary_output)
else:
    st.info("Summary from the text area will appear here.")