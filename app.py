import streamlit as st
from utils.pdf_parser import extract_text_and_images
from utils.ocr import extract_text_from_image
from utils.embeddings import generate_embedding
from utils.vector_store import upsert_to_pgvector, search_similar

st.title("📄 Multimodal PDF Search")

uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.read())

    texts, image_paths = extract_text_and_images("temp.pdf")

    # Combine text + OCR
    full_text_blocks = texts[:]
    for img_path in image_paths:
        ocr_text = extract_text_from_image(img_path)
        full_text_blocks.append(ocr_text)

    st.success("PDF parsed. Generating embeddings...")
    for block in full_text_blocks:
        embedding = generate_embedding(block)
        upsert_to_pgvector(block, embedding)

    st.success("Document indexed successfully!")

query = st.text_input("Enter your query")
if query:
    result = search_similar(query)
    st.write("### Top Result:", result)
