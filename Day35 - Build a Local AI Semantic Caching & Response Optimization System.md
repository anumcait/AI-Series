# 🚀 Day 35 — Build a Local AI Semantic Caching & Response Optimization System ⚡🧠

## 1. Project Overview

Built a local AI application using Python, Ollama, Qwen3, Sentence Transformers, ChromaDB, and Streamlit.

The application stores previously generated AI answers and reuses them when users ask sufficiently similar questions. This reduces unnecessary LLM calls and improves response time.

### Objective

- Understand semantic embeddings and similarity search.
- Implement persistent AI response caching.
- Identify cache HIT and MISS.
- Configure similarity thresholds and cache expiration.
- Compare cached and uncached response times.

## 2. Tech Stack

| Technology | Purpose |
|---|---|
| Python | Application logic |
| Ollama | Local LLM inference |
| Qwen3:4b | AI response generation |
| Sentence Transformers | Generate question embeddings |
| ChromaDB | Persistent vector cache |
| Streamlit | Web interface |
| Pandas | Display cached questions |

## 3. How It Works

```text
User Question
      |
      v
Sentence Transformer
(Generate Embedding)
      |
      v
ChromaDB Similarity Search
      |
      +---- Cache HIT ----> Return Cached Answer
      |
      +---- Cache MISS ---> Ollama + Qwen3
                                  |
                                  v
                           Generate Answer
                                  |
                                  v
                           Save to ChromaDB
                                  |
                                  v
                           Return Answer
```

**Cache HIT:** A sufficiently similar, unexpired answer exists. Ollama generation is skipped.

**Cache MISS:** No suitable cached answer exists. Ollama generates a new answer, which is saved for future use.

## 4. Step 1 — Verify Prerequisites

Open VS Code and launch a PowerShell terminal.

```powershell
python --version
ollama --version
ollama list
```

**Why:** Confirm Python, Ollama, and available models.

If Qwen3 is missing:

```powershell
ollama pull qwen3:4b
```

Test the model:

```powershell
ollama run qwen3:4b
```

Enter:

```text
What is Docker?
```

**Expected:** Qwen3 generates an answer locally.

Type `/bye` to exit.

## 5. Step 2 — Create Project

```powershell
mkdir Day35-Semantic-Cache
cd Day35-Semantic-Cache

python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is blocked:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

**Why:** Keep project dependencies isolated.

Expected terminal prefix:

```text
(.venv)
```

## 6. Step 3 — Install Dependencies

```powershell
python -m pip install --upgrade pip

pip install streamlit ollama chromadb sentence-transformers pandas
```

Create the application file:

```powershell
New-Item app.py -ItemType File
```

## 7. Step 4 — Create `app.py`

Paste the following complete code into `app.py`.

```python
import time
import uuid

import chromadb
import pandas as pd
import streamlit as st
from ollama import Client
from sentence_transformers import SentenceTransformer

MODEL = "qwen3:4b"
EMBED_MODEL = "all-MiniLM-L6-v2"
PROMPT_VERSION = "day35-v1"

st.set_page_config(page_title="Day 35 - Semantic Cache")

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

st.title("Day 35 - AI Semantic Caching")
st.write("Local AI using Ollama, Qwen3 and ChromaDB")

threshold = st.sidebar.slider(
    "Minimum similarity",
    0.80, 1.00, 0.93, 0.01
)

ttl_hours = st.sidebar.number_input(
    "Cache lifetime (hours)",
    min_value=1,
    value=24
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

        # Generate embedding
        embedding = encoder.encode(question).tolist()

        # Search existing cache
        result = None

        if collection.count() > 0:
            try:
                result = collection.query(
                    query_embeddings=[embedding],
                    n_results=1,
                    where={"version": PROMPT_VERSION}
                )
            except Exception:
                result = None

        hit = False
        similarity = None

        # Check similarity and expiration
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

        # Generate answer when cache misses
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

            # Store new answer
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
            "CACHE MISS - Generated new answer"
        )

        st.write(answer)

        col1, col2, col3 = st.columns(3)

        col1.metric("Response Time", f"{elapsed:.2f}s")
        col2.metric("Cache Status", "HIT" if hit else "MISS")
        col3.metric("Stored Answers", collection.count())

        if similarity is not None:
            st.caption(
                f"Nearest similarity: {similarity:.3f}"
            )

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
    st.dataframe(
        pd.DataFrame(rows),
        use_container_width=True
    )
else:
    st.info("No cached questions yet.")
```

### Code Explanation

1. `SentenceTransformer` converts questions into numerical embeddings.
2. `ChromaDB` searches previously saved embeddings.
3. Cosine similarity determines how closely questions match.
4. The similarity threshold decides whether a cached answer is reusable.
5. TTL determines how long an answer remains valid.
6. `Ollama` generates answers only when needed.
7. `Streamlit` displays answers, cache status, and response times.

## 8. Step 5 — Run Application

Start Ollama if it is not already running.

From the project directory:

```powershell
streamlit run app.py
```

Expected:

```text
Local URL: http://localhost:8501
```

Open:

http://localhost:8501

**Expected:** The Semantic Caching application appears with a question input, similarity slider, TTL setting, and cached-question table.

The embedding model may download automatically on the first run.

## 9. Step 6 — Test the Application

### Test 1 — Cache MISS

Enter:

```text
What is Docker?
```

Expected:

```text
CACHE MISS
```

Ollama generates an answer and stores it in ChromaDB.

### Test 2 — Cache HIT

Ask the same question again:

```text
What is Docker?
```

Expected:

```text
CACHE HIT
```

The saved answer is reused without generating a new LLM response.

### Test 3 — Semantic Similarity

Enter:

```text
Explain Docker in simple words.
```

Expected: A cache HIT is possible if similarity meets the configured threshold.

If it returns MISS, inspect the similarity score. You can experiment with a threshold of `0.90`.

### Test 4 — Different Question

Enter:

```text
What is Kubernetes?
```

Expected: Usually CACHE MISS because this is a different question.

### Test 5 — Persistent Cache

Stop Streamlit:

```text
Ctrl + C
```

Restart:

```powershell
streamlit run app.py
```

Ask:

```text
What is Docker?
```

Expected: CACHE HIT if the stored entry has not expired.

This confirms ChromaDB persistence.

### Test 6 — Clear Cache

Click **Clear cache** in the sidebar.

Ask the Docker question again.

Expected: CACHE MISS because the previous entries were deleted.

### Test 7 — Cache Expiration

Set the cache lifetime to 1 hour.

For a quick expiration test, temporarily change:

```python
age < ttl_hours * 3600
```

to:

```python
age < 10
```

Ask a new question, wait more than 10 seconds, and repeat it.

Expected: CACHE MISS because the saved entry expired.

Restore the original condition afterward.

## 10. Performance Comparison

| Measurement | Cache MISS | Cache HIT |
|---|---|---|
| Embedding generation | Yes | Yes |
| Vector search | Yes | Yes |
| Ollama generation | Yes | No |
| Answer storage | Yes | No |
| Response time | Usually higher | Usually lower |

Actual response times depend on local hardware, model size, and cache size.

## 11. Final Project Structure

```text
Day35-Semantic-Cache/
├── app.py
├── chroma_cache/
│   └── Persistent vector database files
└── .venv/
    └── Python environment
```

## 12. Important Limitations

- Similar questions do not always require identical answers.
- A high similarity score does not guarantee correctness.
- This implementation is best suited to stable general-knowledge questions.
- Do not share cached personal or sensitive answers between users.
- Cache entries should be invalidated when the model, prompt, permissions, or underlying knowledge changes.
- This introductory implementation displays request-level timing but does not maintain a historical analytics report.

## 13. Key Learning

Through this project, I learned how semantic caching can optimize local AI applications by reusing relevant responses.

I practiced:

- Text embeddings
- Semantic similarity search
- Vector database persistence
- Cache HIT and MISS handling
- TTL-based cache expiration
- Ollama inference optimization
- Streamlit application development

## 14. Final Outcome

Successfully implemented a local AI Semantic Caching System that:

- Accepts natural-language questions.
- Searches previously cached answers.
- Reuses sufficiently similar, unexpired responses.
- Generates new answers using Ollama and Qwen3 when necessary.
- Stores embeddings and responses persistently in ChromaDB.
- Displays cache status, similarity, and response time.
- Supports cache clearing and expiration.

**Takeaway:** Efficient AI engineering is not only about generating intelligent answers. It is also about reducing unnecessary computation while preserving response relevance.

### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/02a3a5c7-0532-4527-86ec-5424425d0339" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/0be5b38d-9414-45be-a276-a695644e95cd" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/101c00f5-5b7d-49d0-b387-db6b11303419" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/f1bb6421-7810-42b3-a85b-231f37afdf17" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/ebfd6c09-7586-479c-a801-22db68b03cde" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/46f83812-351c-4d50-b6f3-b9fe170da8ab" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/6bd1a128-b0dc-447d-abf0-06ef7ebe4c1f" />







