import os
import json

import chromadb
from sentence_transformers import SentenceTransformer
from google import genai

from documents import documents


# ============================================================
# CONFIGURATION
# ============================================================

CHROMA_PATH = "./chroma_db"

COLLECTION_NAME = "day19_devops_knowledge"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"

TOP_K = 3

# Use a Gemini model available to your API key.
GEMINI_MODEL = "gemini-3.8-flash"


# ============================================================
# 1. LOAD EMBEDDING MODEL
# ============================================================

print("\nLoading embedding model...")

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)


# ============================================================
# 2. CREATE PERSISTENT CHROMADB
# ============================================================

print("Creating ChromaDB...")

chroma_client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


# ============================================================
# 3. CREATE COLLECTION
# ============================================================

try:
    collection = chroma_client.get_collection(
        name=COLLECTION_NAME
    )

    print("Existing collection found.")

except Exception:

    collection = chroma_client.create_collection(
        name=COLLECTION_NAME
    )

    print("New collection created.")


# ============================================================
# 4. STORE INTERNAL DOCUMENTS
# ============================================================

existing_count = collection.count()

if existing_count == 0:

    print("\nCreating document embeddings...")

    embeddings = embedding_model.encode(
        documents
    ).tolist()


    ids = [
        f"doc_{i}"
        for i in range(len(documents))
    ]


    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings
    )


    print(
        f"Stored {len(documents)} internal documents."
    )

else:

    print(
        f"ChromaDB already contains {existing_count} documents."
    )


# ============================================================
# 5. CONNECT TO GEMINI
# ============================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:

    raise Exception(
        "GEMINI_API_KEY environment variable is not set."
    )


gemini_client = genai.Client(
    api_key=api_key
)


# ============================================================
# 6. RETRIEVE INTERNAL DOCUMENTS
# ============================================================

def retrieve_documents(question):

    print("\nCreating query embedding...")

    query_embedding = embedding_model.encode(
        question
    ).tolist()


    print("Searching internal ChromaDB...")

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=TOP_K
    )


    retrieved_documents = results["documents"][0]

    distances = results["distances"][0]


    return retrieved_documents, distances


# ============================================================
# 7. GENERATE GROUNDED ANSWER
# ============================================================

def generate_answer(
    question,
    retrieved_documents
):

    if not retrieved_documents:

        return {
            "answer": (
                "I couldn't find relevant information "
                "in the provided knowledge base."
            ),
            "sources": []
        }


    # Combine retrieved internal documents
    context = "\n\n".join(
        retrieved_documents
    )


    # IMPORTANT:
    # Gemini is explicitly restricted to the context.
    prompt = f"""
You are an internal DevOps knowledge assistant.

You must answer the user's question using ONLY
the INTERNAL KNOWLEDGE provided below.

Do NOT use your general knowledge.

Do NOT invent information.

Do NOT search for or assume information that is
not present in the provided context.

If the answer cannot be found in the context,
respond with exactly:

I couldn't find relevant information about this
in the provided knowledge base.

INTERNAL KNOWLEDGE:
-------------------------
{context}
-------------------------

USER QUESTION:
{question}

Answer concisely.
"""


    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )


    answer = response.text.strip()


    # ========================================================
    # 8. SOURCE HANDLING
    # ========================================================

    if (
        "couldn't find relevant information"
        in answer.lower()
    ):

        sources = []

    else:

        sources = retrieved_documents


    return {
        "answer": answer,
        "sources": sources
    }


# ============================================================
# 9. COMPLETE RAG PIPELINE
# ============================================================

def rag(question):

    print("\n")
    print("=" * 60)
    print("DAY 19 RAG")
    print("=" * 60)

    print("\nQuestion:")
    print(question)


    # --------------------------------------------------------
    # RETRIEVAL
    # --------------------------------------------------------

    retrieved_documents, distances = (
        retrieve_documents(question)
    )


    print("\n")
    print("=" * 60)
    print("RETRIEVED INTERNAL DOCUMENTS")
    print("=" * 60)


    for index, document in enumerate(
        retrieved_documents,
        start=1
    ):

        print(f"\n{index}. {document}")

        print(
            f"   Distance: {distances[index - 1]:.4f}"
        )


    # --------------------------------------------------------
    # GENERATION
    # --------------------------------------------------------

    print("\n")
    print("Sending retrieved context to Gemini...")


    result = generate_answer(
        question,
        retrieved_documents
    )


    # --------------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------------

    print("\n")
    print("=" * 60)
    print("FINAL ANSWER")
    print("=" * 60)

    print(result["answer"])


    print("\n")
    print("=" * 60)
    print("SOURCES")
    print("=" * 60)


    if result["sources"]:

        for source in result["sources"]:

            print(f"- {source}")

    else:

        print("No sources found.")


    print("\n")
    print("=" * 60)
    print("JSON RESPONSE")
    print("=" * 60)


    print(
        json.dumps(
            result,
            indent=2
        )
    )


# ============================================================
# 10. MAIN
# ============================================================

if __name__ == "__main__":

    print("\n")
    print("=" * 60)
    print("DAY 19 - INTERNAL RAG KNOWLEDGE ASSISTANT")
    print("=" * 60)

    print(
        "\nKnowledge source: Internal ChromaDB only"
    )

    while True:

        question = input(
            "\nAsk a question (or type 'exit'): "
        )


        if question.lower() == "exit":

            print("\nGoodbye!")

            break


        if not question.strip():

            print("Please enter a question.")

            continue


        rag(question)
