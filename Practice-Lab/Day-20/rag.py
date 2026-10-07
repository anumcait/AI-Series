import chromadb

from sentence_transformers import SentenceTransformer
from ollama import chat


# ==========================================
# Embedding model
# ==========================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# ==========================================
# ChromaDB
# ==========================================

client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_collection(
    name="devops"
)


# ==========================================
# Rewrite follow-up question
# ==========================================

def rewrite_query(question, history):

    if not history:
        return question

    conversation = ""

    for message in history[-6:]:

        conversation += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    prompt = f"""
Rewrite the user's latest question into a
standalone search query.

Use the conversation to understand words like:

it
this
that
they
the tool
the service

Do not answer the question.

Return ONLY the search query.

Conversation:

{conversation}

Latest question:

{question}
"""

    response = chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()


# ==========================================
# Retrieve documents
# ==========================================

def retrieve_documents(query):

    embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

    return results["documents"][0]


# ==========================================
# Generate answer
# ==========================================

def generate_answer(
    question,
    history,
    documents
):

    context = "\n\n".join(documents)

    conversation = ""

    for message in history[-6:]:

        conversation += (
            f"{message['role']}: "
            f"{message['content']}\n"
        )

    prompt = f"""
You are a DevOps RAG assistant.

Answer the question using ONLY the
knowledge-base context below.

Use conversation history to understand
follow-up questions.

Do not invent information.

If the answer is not present in the
knowledge base, respond:

I couldn't find enough information in the
knowledge base to answer this question.

CONVERSATION:

{conversation}

KNOWLEDGE BASE:

{context}

QUESTION:

{question}
"""

    response = chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"].strip()


# ==========================================
# Complete RAG
# ==========================================

def ask(question, history):

    # 1. Rewrite question
    search_query = rewrite_query(
        question,
        history
    )

    print(
        f"\n🔎 Search query: {search_query}"
    )

    # 2. Retrieve
    documents = retrieve_documents(
        search_query
    )

    print(
        f"📚 Retrieved: {len(documents)} documents"
    )

    # 3. Generate
    answer = generate_answer(
        question,
        history,
        documents
    )

    return answer, documents
