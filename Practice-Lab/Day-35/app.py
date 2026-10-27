
import time
import uuid

import chromadb
import pandas as pd
import streamlit as st
from ollama import Client
from sentence_transformers import SentenceTransformer

# Configuration
MODEL = "qwen3:4b"
EMBED_MODEL = "all-MiniLM-L6-v2"
PROMPT_VERSION = "day35-v1"


@st.cache_resource
def setup():
    encoder = SentenceTransformer(EMBED_MODEL)

    db = chromadb.PersistentClient(path="./chroma_cache")
    collection = db.get_or_create_collection(
        name="day35_answers",
        metadata={"hnsw:space": "cosine"}
    )

    ollama = Client(host="http://localhost:11434")
    return encoder, collection, ollama


encoder, collection, ollama = setup()

st.set_page_config(page_title="Day 35 - Semantic Cache")
st.title("Day 35 - AI Semantic Caching")
st.write("Local AI with Ollama, Qwen3 and ChromaDB")

threshold = st.sidebar.slider(
    "Minimum similarity", 0.80, 1.00, 0.93, 0.01
)

ttl_hours = st.sidebar.number_input(
    "Cache lifetime (hours)", min_value=1, value=24
)

if st.sidebar.button("Clear cache"):
    ids = collection.get()["ids"]
    if ids:
        collection.delete(ids=ids)
    st.sidebar.success("Cache cleared")

question = st.text_input(
    "Ask a general knowledge question",
    placeholder="What is Docker?"
)

if st.button("Ask", disabled=not question.strip()):
    try:
        start = time.perf_counter()

        # Step 1: Generate question embedding
        embedding = encoder.encode(question).tolist()

        # Step 2: Find nearest cached question
        result = None
        if collection.count() > 0:
            result = collection.query(
                query_embeddings=[embedding],
                n_results=1,
                where={"version": PROMPT_VERSION}
            )

        hit = False
        similarity = None

        # Step 3: Check similarity and expiration
        if result and result["ids"][0]:
            similarity = 1.0 - result["distances"][0][0]
            meta = result["metadatas"][0][0]

            age = time.time() - meta["created_at"]

            if (
                similarity >= threshold
                and age < ttl_hours * 3600
            ):
                answer = result["documents"][0][0]
                hit = True

        # Step 4: Generate new answer on cache miss
        if not hit:
            response = ollama.chat(
                model=MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "Answer general knowledge questions "
                            "clearly and concisely."
                        )
                    },
                    {
                        "role": "user",
                        "content": question
                    }
                ]
            )

            answer = response.message.content

            # Step 5: Save response for future reuse
            collection.add(
                ids=[str(uuid.uuid4())],
                embeddings=[embedding],
                documents=[answer],
                metadatas=[{
                    "question": question,
                    "created_at": time.time(),
                    "version": PROMPT_VERSION
                }]
            )

        elapsed = time.perf_counter() - start

        st.success(
            "CACHE HIT - Reused answer"
            if hit else
            "CACHE MISS - Ollama generated answer"
        )

        st.write(answer)

        col1, col2, col3 = st.columns(3)

        col1.metric("Response Time", f"{elapsed:.2f}s")
        col2.metric("Cache Status", "HIT" if hit else "MISS")
        col3.metric("Stored Answers", collection.count())

        if similarity is not None:
            st.caption(f"Nearest similarity: {similarity:.3f}")

    except Exception as e:
        st.error(f"Request failed: {e}")

st.divider()
st.subheader("Cached Questions")

records = collection.get(include=["metadatas"])

rows = [
    {
        "Question": m["question"],
        "Created": time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.localtime(m["created_at"])
        )
    }
    for m in records["metadatas"]
]

if rows:
    st.dataframe(pd.DataFrame(rows), use_container_width=True)
else:
    st.info("No cached questions yet.")
