import openai
import os

openai.api_type = "azure"
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_key = os.getenv("AZURE_OPENAI_KEY")
openai.api_version = "2023-05-15"

EMBED_MODEL = "text-embedding-ada-002"
DEPLOYMENT = os.getenv("AZURE_EMBEDDING_DEPLOYMENT")

def generate_embedding(text):
    response = openai.Embedding.create(
        input=[text],
        engine=DEPLOYMENT
    )
    return response["data"][0]["embedding"]
