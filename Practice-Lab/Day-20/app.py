import streamlit as st

from rag import ask


# ==========================================
# Page
# ==========================================

st.set_page_config(
    page_title="DevOps RAG Chatbot",
    page_icon="🤖"
)


st.title("🤖 DevOps RAG Chatbot")

st.caption(
    "Local RAG using ChromaDB + Ollama"
)


# ==========================================
# Conversation memory
# ==========================================

if "messages" not in st.session_state:

    st.session_state.messages = []


# ==========================================
# Clear
# ==========================================

if st.button("🧹 Clear Conversation"):

    st.session_state.messages = []

    st.rerun()


# ==========================================
# Display history
# ==========================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )

        if "sources" in message:

            with st.expander(
                "📚 Sources"
            ):

                for source in message["sources"]:

                    st.write(source)


# ==========================================
# Chat input
# ==========================================

question = st.chat_input(
    "Ask a DevOps question..."
)


# ==========================================
# Process
# ==========================================

if question:

    # User message

    with st.chat_message("user"):

        st.markdown(question)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # AI response

    with st.chat_message("assistant"):

        with st.spinner(
            "Searching knowledge base..."
        ):

            answer, documents = ask(
                question,
                st.session_state.messages[:-1]
            )

        st.markdown(answer)


        # Sources

        with st.expander(
            "📚 Sources"
        ):

            for document in documents:

                st.write(document)


    # Save response

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
            "sources": documents
        }
    )
