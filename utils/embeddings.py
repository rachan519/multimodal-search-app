import openai
import streamlit as st

def embed_text(text: str):
    openai.api_key = st.secrets["OPENAI_API_KEY"]

    response = openai.Embedding.create(
        input=[text],
        model=st.secrets["OPENAI_EMBEDDING_MODEL"]
    )
    return response["data"][0]["embedding"]
