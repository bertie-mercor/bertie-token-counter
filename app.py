import streamlit as st
import tiktoken
import PyPDF2
import pandas as pd
import io

ENCODING_NAME = "cl100k_base"

def count_tokens(text):
    encoding = tiktoken.get_encoding(ENCODING_NAME)
    return len(encoding.encode(text))

def extract_text_from_pdf(uploaded_file):
    try:
        reader = PyPDF2.PdfReader(uploaded_file)
        return "".join([page.extract_text() or '' for page in reader.pages])
    except Exception as e:
        return None

def extract_text_from_csv(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file, dtype=str)
        return df.to_string(index=False)
    except Exception as e:
        return None

def extract_text_from_txt(uploaded_file):
    try:
        return uploaded_file.read().decode("utf-8")
    except Exception as e:
        return None

def extract_text(file):
    name = file.name.lower()
    if name.endswith('.pdf'):
        return extract_text_from_pdf(file)
    elif name.endswith('.csv'):
        return extract_text_from_csv(file)
    elif name.endswith(('.txt', '.md', '.py')):
        return extract_text_from_txt(file)
    else:
        return None

st.title("📄 Token & Character Counter")
st.markdown("Upload a `.txt`, `.csv`, or `.pdf` file below:")

uploaded_file = st.file_uploader("Choose a file", type=["txt", "csv", "pdf"])

if uploaded_file is not None:
    content = extract_text(uploaded_file)

    if content:
        char_count = len(content)
        token_count = count_tokens(content)

        st.success(f"✅ File: `{uploaded_file.name}`")
        st.write(f"🧮 **Characters:** {char_count}")
        st.write(f"🔢 **Tokens:** {token_count}")
    else:
        st.error("Could not read file content.")