import psycopg2
import os
import openai
from utils.embeddings import generate_embedding

conn = psycopg2.connect(
    host=os.getenv("PG_HOST"),
    dbname=os.getenv("PG_DB"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    port=os.getenv("PG_PORT")
)

cur = conn.cursor()

# Make sure PGVector extension is enabled and table created
cur.execute("""
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding VECTOR(1536)
);
""")
conn.commit()

def upsert_to_pgvector(content, embedding):
    cur.execute(
        "INSERT INTO documents (content, embedding) VALUES (%s, %s)",
        (content, embedding)
    )
    conn.commit()

def search_similar(query):
    query_vec = generate_embedding(query)
    cur.execute(
        """
        SELECT content FROM documents
        ORDER BY embedding <#> %s
        LIMIT 1;
        """,
        (query_vec,)
    )
    return cur.fetchone()[0]
