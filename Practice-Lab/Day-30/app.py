
import io

import ollama
import streamlit as st
from PIL import Image, UnidentifiedImageError

MODEL = "gemma3:4b"

st.set_page_config(
    page_title="Day 30 - Vision Assistant",
    page_icon="🖼️",
    layout="wide",
)

st.title("🖼️ Local Multimodal AI Assistant")
st.caption("Ask questions about images using Python + Ollama.")

with st.sidebar:
    st.header("Model status")
    st.write(f"Selected model: `{MODEL}`")
    st.write("Ollama must be running on this computer.")
    if st.button("Clear conversation"):
        st.session_state.pop("history", None)
        st.rerun()

uploaded_file = st.file_uploader(
    "Upload a JPG, JPEG, PNG, or WEBP image",
    type=["jpg", "jpeg", "png", "webp"],
)

if uploaded_file is None:
    st.info("Upload an image to get started.")
    st.stop()

image_bytes = uploaded_file.getvalue()

try:
    with Image.open(io.BytesIO(image_bytes)) as image:
        image.verify()

    with Image.open(io.BytesIO(image_bytes)) as image:
        st.image(image, caption="Your uploaded image", width="stretch")

except (UnidentifiedImageError, OSError, ValueError):
    st.error("This image is invalid or damaged. Please upload another image.")
    st.stop()

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Describe this image", type="primary"):
    st.session_state.history.append({
        "role": "user",
        "content": (
            "Describe this image in detail. Identify visible objects, "
            "their positions and relationships, and any readable text. "
            "Do not guess details that are not visible."
        ),
    })
    st.session_state.run_model = True

for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask a question about this image...")

if question:
    st.session_state.history.append({
        "role": "user",
        "content": question,
    })
    st.session_state.run_model = True

if st.session_state.get("run_model", False):
    st.session_state.run_model = False

    # Attach the image to the latest question.
    messages = [
        {
            "role": message["role"],
            "content": message["content"],
        }
        for message in st.session_state.history[-10:]
    ]
    messages[-1]["images"] = [image_bytes]

    with st.spinner("Analyzing image with your local AI model..."):
        try:
            response = ollama.chat(
                model=MODEL,
                messages=messages,
                stream=False,
            )
            answer = response.message.content

            st.session_state.history.append({
                "role": "assistant",
                "content": answer,
            })

            with st.chat_message("assistant"):
                st.markdown(answer)

        except ollama.ResponseError as error:
            st.error(f"Ollama model error: {error}")
        except Exception as error:
            st.error(
                "Could not contact Ollama or complete the analysis. "
                "Check that Ollama is running and the model is installed."
            )
            st.caption(f"Technical details: {error}")
