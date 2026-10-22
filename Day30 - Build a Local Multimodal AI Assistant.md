# 🚀 Day 30 — Build a Local Multimodal AI Assistant 🖼️🧠

## Objective

Build a local AI application using Python, Ollama, Gemma 3 Vision, and Streamlit that accepts an image, describes its contents, and answers follow-up questions.

The key lesson is:

**AI can understand both images and natural language, not just text.**

## 1\. Technology Stack

- Python
- Ollama
- Gemma 3 Vision (`gemma3:4b`)
- Streamlit
- Pillow
- Multimodal AI

## 2\. Project Structure

Create the project in:

```
D:\AI-Series\Practice-Lab\Day-30
```

Project files:

```
Day-30/
├── app.py
├── requirements.txt
└── day.md
```

File descriptions:

- `app.py` — image upload, validation, AI inference, and response display.
- `requirements.txt` — Python dependencies.
- `day.md` — project documentation and completed work.

## 3\. Environment Setup

### Step 1: Check Python

```
python --version
```

### Step 2: Check Ollama

```
ollama --version
```

### Step 3: Download the Vision Model

```
ollama pull gemma3:4b
```

### Step 4: Test the Model

```
ollama run gemma3:4b
```

Confirm the model responds, then exit using:

```
/bye
```

### Step 5: Install Dependencies

The Python virtual environment is located at `D:\AI-Series\venv`.

From the Day-30 directory, install dependencies using:

```
../venv/Scripts/python.exe -m pip install streamlit ollama pillow
```

## 4\. Implement the Application

Create `app.py` using Streamlit, Ollama, and Pillow.

The application should:

1. Allow the user to upload a JPG, JPEG, PNG, or WEBP image.
2. Validate the uploaded image.
3. Display the image in the browser.
4. Generate a detailed image description.
5. Accept follow-up questions about the image.
6. Retain recent conversation history during the session.
7. Display model errors and invalid-image messages.

Configure the model:

```
MODEL = "gemma3:4b"
```

The Python application sends the image and question to Ollama using `ollama.chat()`. The model processes the visual information and generates a natural-language response.

## 5\. Run the Application

From the Day-30 project directory, run:

```
../venv/Scripts/python.exe -m streamlit run app.py
```

Open:

```
http://localhost:8501
```

Expected result: The Streamlit interface opens in the browser and displays the image uploader.

## 6\. How Real-Time Image Analysis Works

1. The user uploads an image and submits a question.
2. Streamlit receives the image and question.
3. Python sends both to the local Ollama API.
4. Gemma 3 Vision analyzes the image and generates a response.
5. Streamlit displays the answer.

This provides interactive, on-demand image analysis. It does not continuously analyze live video.

## 7\. Model Troubleshooting

Initially attempted to use `llama3.2-vision`, but Ollama version `0.40.5` returned:

```
unknown model architecture: 'mllama'
```

The model could not load with the installed runtime. Gemma 3 was selected as an alternative vision-capable model.

Update `app.py` to use:

```
MODEL = "gemma3:4b"
```

After confirming that Gemma 3 successfully analyzes images, remove the incompatible model if it is no longer needed:

```
ollama rm llama3.2-vision
```

Verify installed models:

```
ollama list
```

Keep `llama3.2:3b` if it is still needed for text-only projects.

## 8\. Testing Checklist

- [ ]Streamlit starts without import errors.
- [ ]An image uploads and displays correctly.
- [ ]The model generates a detailed image description.
- [ ]Follow-up questions receive relevant answers.
- [ ]Readable text in images can be extracted when supported by the model.
- [ ]Invalid images produce an error message.
- [ ]Ollama errors are displayed instead of silently failing.
- [ ]The replacement vision model works before the old model is removed.

## 9\. Key Learning

Day 30 introduces multimodal AI by extending a text-focused application to understand images and answer visual questions.

Python manages the interface and model requests, Streamlit provides the user experience, and Ollama runs the vision-capable model locally.

**Expected outcome:** A working local image-understanding assistant that accepts images, describes visible objects, and answers questions about their contents.

### Screenshots
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/3a80193d-f6d3-48e2-a4c7-32afc684f4a9" />
<img width="500" height="250" alt="image" src="https://github.com/user-attachments/assets/03f3ffeb-5e47-4db1-b302-b72853181286" />


