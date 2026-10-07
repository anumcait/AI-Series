# 🚀 Day 20 — AI RAG Chatbot 🤖📚

Build a real-time conversational RAG chatbot using Python, Streamlit, Sentence Transformers, ChromaDB, and Ollama.

## 🎯 Goal

The chatbot should:

- Retrieve relevant information from a DevOps knowledge base
- Remember conversation history
- Understand follow-up questions
- Generate grounded answers using Ollama
- Display retrieved sources
- Handle questions outside the knowledge base
- Support clearing the conversation

## 🏗️ Architecture

User Question → Conversation History → Query Rewriting → Sentence Transformers → ChromaDB → Relevant Documents → Context + History → Ollama/Llama 3.2 → Answer + Sources

## 🛠️ Tech Stack

- Python
- Streamlit
- Sentence Transformers
- ChromaDB
- Ollama
- Llama 3.2 3B

## 📁 Project Structure

Day-20/
├── data/
│   └── devops.txt
├── chroma_db/
├── setup.py
├── rag.py
├── app.py
├── test_search.py
├── test_ollama.py
├── requirements.txt
└── .gitignore

## 1. Install Ollama

Download and install Ollama:

https://ollama.com/download/windows

Verify:

    ollama --version

Download the model:

    ollama pull llama3.2:3b

Test:

    ollama run llama3.2:3b

Ask:

    What is Terraform?

Exit:

    /bye

## 2. Create Project

    mkdir Day-20
    cd Day-20
    mkdir data

Create the virtual environment:

    python -m venv venv

Git Bash:

    source venv/Scripts/activate

## 3. requirements.txt

    streamlit
    chromadb
    sentence-transformers
    ollama

Install:

    python -m pip install -r requirements.txt

Check Streamlit:

    python -m streamlit --version

If ML package errors occur with Python 3.13, use Python 3.11 for the virtual environment.

## 4. data/devops.txt

    Terraform

    Terraform is an Infrastructure as Code tool used to define,
    provision, and manage infrastructure using configuration files.

    Terraform can manage infrastructure consistently and supports
    cloud providers such as AWS, Azure, and Google Cloud.


    AWS

    Amazon Web Services is a cloud computing platform.

    AWS provides services such as EC2, S3, RDS, Lambda, and VPC.

    Terraform can be used to manage AWS infrastructure.


    Docker

    Docker is a containerization platform used to package
    applications and their dependencies into containers.

    Containers provide consistent environments across development,
    testing, and production.


    Kubernetes

    Kubernetes is a container orchestration platform used to deploy,
    scale, and manage containerized applications.


    CI/CD

    CI/CD practices automate building, testing, and deploying software.

## 5. setup.py

    import chromadb
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path="chroma_db")

    collection = client.get_or_create_collection("devops")

    with open("data/devops.txt", "r", encoding="utf-8") as file:
        text = file.read()

    documents = [
        chunk.strip()
        for chunk in text.split("\n\n")
        if chunk.strip()
    ]

    embeddings = model.encode(documents).tolist()

    ids = [f"doc_{i}" for i in range(len(documents))]

    if collection.count() == 0:
        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings
        )

    print(f"Documents in ChromaDB: {collection.count()}")

Run:

    python setup.py

## 6. test_search.py

    import chromadb
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path="chroma_db")

    collection = client.get_collection("devops")

    question = "How can I automate AWS infrastructure?"

    embedding = model.encode(question).tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

    for document in results["documents"][0]:
        print("-" * 50)
        print(document)

Run:

    python test_search.py

## 7. test_ollama.py

    from ollama import chat

    response = chat(
        model="llama3.2:3b",
        messages=[
            {
                "role": "user",
                "content": "What is Terraform?"
            }
        ]
    )

    print(response["message"]["content"])

Run:

    python test_ollama.py

## 8. rag.py

    import chromadb
    from sentence_transformers import SentenceTransformer
    from ollama import chat

    model = SentenceTransformer("all-MiniLM-L6-v2")

    client = chromadb.PersistentClient(path="chroma_db")

    collection = client.get_collection("devops")


    def rewrite_query(question, history):

        if not history:
            return question

        conversation = "\n".join(
            f"{m['role']}: {m['content']}"
            for m in history[-6:]
        )

        prompt = f"""
    Rewrite the latest question as a standalone search query.

    Use the conversation to understand words such as:
    it, this, that, they, the tool.

    Return only the rewritten query.

    Conversation:
    {conversation}

    Latest question:
    {question}
    """

        response = chat(
            model="llama3.2:3b",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response["message"]["content"].strip()


    def retrieve(query):

        embedding = model.encode(query).tolist()

        results = collection.query(
            query_embeddings=[embedding],
            n_results=3
        )

        return results["documents"][0]


    def generate_answer(question, history, documents):

        context = "\n\n".join(documents)

        conversation = "\n".join(
            f"{m['role']}: {m['content']}"
            for m in history[-6:]
        )

        prompt = f"""
    You are a DevOps RAG assistant.

    Answer using ONLY the knowledge-base context.

    Use conversation history to understand follow-up questions.

    Do not invent information.

    If the answer is not present in the context, say:

    I couldn't find enough information in the knowledge base
    to answer this question.

    Conversation:
    {conversation}

    Knowledge Base:
    {context}

    Question:
    {question}
    """

        response = chat(
            model="llama3.2:3b",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        return response["message"]["content"].strip()


    def ask(question, history):

        search_query = rewrite_query(
            question,
            history
        )

        documents = retrieve(search_query)

        answer = generate_answer(
            question,
            history,
            documents
        )

        return answer, documents

## 9. app.py

    import streamlit as st
    from rag import ask

    st.set_page_config(
        page_title="DevOps RAG Chatbot",
        page_icon="🤖"
    )

    st.title("🤖 DevOps RAG Chatbot")

    st.caption(
        "ChromaDB + Sentence Transformers + Ollama"
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if st.button("🧹 Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            if "sources" in message:
                with st.expander("📚 Sources"):
                    for source in message["sources"]:
                        st.write(source)

    question = st.chat_input(
        "Ask a DevOps question..."
    )

    if question:

        with st.chat_message("user"):
            st.markdown(question)

        st.session_state.messages.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("assistant"):

            with st.spinner(
                "Searching knowledge base..."
            ):
                answer, sources = ask(
                    question,
                    st.session_state.messages[:-1]
                )

            st.markdown(answer)

            with st.expander("📚 Sources"):
                for source in sources:
                    st.write(source)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })

## 10. Run

Activate the environment:

    source venv/Scripts/activate

Start Streamlit:

    python -m streamlit run app.py

Open:

    http://localhost:8501

## 🧪 Test

Question:

    What can I use to automate infrastructure?

Follow-up:

    Why would I use it?

Follow-up:

    Does it work with AWS?

The chatbot should understand:

    it → Terraform

Test an unknown question:

    What is the population of India?

Expected:

    I couldn't find enough information in the knowledge base
    to answer this question.

Click:

    🧹 Clear Conversation

to reset the conversation.

## 🔄 Final Flow

Question
↓
Conversation History
↓
Query Rewriting
↓
Embedding
↓
ChromaDB Search
↓
Relevant Documents
↓
Context + History
↓
Ollama / Llama 3.2
↓
Grounded Answer
↓
Sources

## ✅ Completion Checklist

- [ ] Ollama installed
- [ ] Llama 3.2 downloaded
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Knowledge base created
- [ ] ChromaDB created
- [ ] Retrieval tested
- [ ] Ollama tested
- [ ] RAG pipeline created
- [ ] Streamlit UI created
- [ ] Conversation history works
- [ ] Follow-up questions work
- [ ] Sources displayed
- [ ] Unknown questions handled
- [ ] Clear conversation works

## 🏆 Final Result

A locally running conversational RAG chatbot using:

Sentence Transformers
+
ChromaDB
+
Conversation History
+
Ollama / Llama 3.2
+
Streamlit

This completes Day 20 with a practical, real-time conversational RAG application.
