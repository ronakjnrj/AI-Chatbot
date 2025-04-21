from dotenv import load_dotenv
import streamlit as st
import os
import google.generativeai as genai
from pypdf import PdfReader
# import PyPDF2

# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Gemini Model
model = genai.GenerativeModel("gemini-1.5-pro-latest")
chat = model.start_chat(history=[])

def extract_text_from_pdf(pdf_file):
    """Extract text from uploaded PDF file."""
    pdf_reader = PdfReader(pdf_file)
    text = "".join(page.extract_text() or "" for page in pdf_reader.pages)
    return text

def get_gemini_response(question, context):
    """Fetch response from Gemini AI based on the PDF content."""
    prompt = f"Context: {context}\nQuestion: {question}\nAnswer:"
    response = chat.send_message(prompt, stream=True)
    return response

# Streamlit Configuration
st.set_page_config(page_title="PDF Chatbot", layout="wide")
st.header("📄 ChatBot")

# File Upload
pdf_file = st.file_uploader("Upload a PDF", type=["pdf"])

if pdf_file:
    pdf_text = extract_text_from_pdf(pdf_file)
    st.session_state["pdf_text"] = pdf_text  # Store in session state
    st.success("PDF Uploaded Successfully!")

# Initialize session
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# User Input
user_input = st.text_input("Ask a question from the PDF: ", key="input")
submit = st.button("Ask")

if submit and user_input:
    if "pdf_text" not in st.session_state:
        st.error("Please upload a PDF first.")
    else:
        response = get_gemini_response(user_input, st.session_state["pdf_text"])
        
        # Add user message to history
        st.session_state["chat_history"].append(("You", user_input))

        st.subheader("Response")
        bot_response = ""
        
        response_container = st.empty()  # To display streamed response
        for chunk in response:
            if hasattr(chunk, "text"):  # Ensure chunk has a text attribute
                bot_response += chunk.text
                response_container.write(bot_response)  # Stream output
        
        # Add bot response to history
        st.session_state["chat_history"].append(("Bot", bot_response))

# Display Chat History
st.subheader("Chat History")
for role, text in st.session_state["chat_history"]:
    st.write(f"**{role}**: {text}")

"""
if submit and user_input:
    pdf_text = st.session_state.get("pdf_text", "")
    response = get_gemini_response(user_input, st.session_state["pdf_text"])
        
    # Add user message to history
    st.session_state["chat_history"].append(("You", user_input))

    st.subheader("Response")
    bot_response = ""
        
    response_container = st.empty()  # To display streamed response
    for chunk in response:
        if hasattr(chunk, "text"):  # Ensure chunk has a text attribute
            bot_response += chunk.text
            response_container.write(bot_response)  # Stream output
        
        # Add bot response to history
    st.session_state["chat_history"].append(("Bot", bot_response))
"""