🤖 AI Series

Welcome to my AI Series — a hands-on journey where I build practical AI projects, experiment with modern AI technologies, and document what I learn along the way.

The goal is simple: learn by building. 🚀

🎯 What This Series Covers

Throughout this series, I'll explore and build projects around:

🤖 Generative AI

🧠 Large Language Models (LLMs)

✍️ Prompt Engineering

🔗 AI APIs & Integrations

📚 RAG (Retrieval-Augmented Generation)

🕵️ AI Agents

⚙️ AI Automation

🐍 Python for AI

🚀 Practical AI Engineering

Each project focuses on solving a practical problem while understanding the concepts and tools behind it.

📂 Projects
| Day | Project | Technologies |
|---|---|---|
| Day 1 | AI Bug Description Clarifier | Python, OpenAI API, Prompt Engineering |
| Day 2 | AI Travel Guide Chatbot | Python, OpenAI API, Prompt Engineering |
| Day 3 | Coming Soon 🚀 | — |

🚀 Day 1 — AI Bug Description Clarifier

The first project focuses on improving the quality of developer-reported bug descriptions.

Problem

Developers often report bugs informally, for example:

"App keeps crashing when I click save."

Such descriptions may not provide enough structure for developers to quickly understand or reproduce the issue.

Solution

The AI Bug Description Clarifier uses an LLM to transform an informal bug report into a structured and professional issue summary.

Flow:

Raw Bug Description
        ↓
   AI Prompt
        ↓
    LLM / OpenAI
        ↓
Structured Bug Summary

Example

Input:

App keeps crashing when I click save.


Output:

Bug Summary:
Application crashes upon clicking the "Save" button.

Triggering Action:
User clicks the "Save" button.

Observed Behavior:
The application unexpectedly crashes after the "Save" button is clicked.

Technologies Used

Python 🐍

OpenAI API 🤖

Prompt Engineering

Virtual Environment

📖 Notes

Detailed learning notes and additional concepts will be documented here:

👉 Notes.md

📈 Learning Approach

For every project, I'll try to follow a simple approach:

Learn → Build → Experiment → Document → Improve


The focus is not just on writing code, but on understanding how AI can be applied to real-world problems.

🗂️ Repository Structure
AI-Series/
│
├── Day1 - Clarify Bugs with AI.md
├── Notes.md
└── README.md


As the series grows, new projects and supporting resources will be added here.

🚀 Follow the Journey

I'll be sharing each project, key learnings, and practical experiments throughout this AI journey.

If you're also learning AI, feel free to explore the projects, experiment with the code, and build along with me!

⭐ Learning AI by building one project at a time.

#AI #ArtificialIntelligence #GenerativeAI #AIEngineering #LLM #Python #OpenAI #PromptEngineering

🚀 Day 2 — AI Travel Guide Chatbot

The second project focuses on building a simple AI-powered chatbot using the OpenAI API.

Problem

A traditional travel application may provide predefined information, but it may not interact naturally with the user.

Solution

The AI Travel Guide Chatbot uses an LLM to act as a friendly travel guide. It starts the conversation by greeting the user and asking where they want to go.

Flow:

User
        ↓
   User Prompt
        ↓
    OpenAI API
        ↓
GPT-4.1-mini
        ↓
AI Travel Guide Response

Example

Prompt:

You are a friendly travel guide. Greet the user and ask where they want to go.

Output:

Hello, traveler! I'm your friendly travel guide. Where would you like to go?

Technologies Used

Python 🐍

OpenAI API 🤖

GPT-4.1-mini

Prompt Engineering

Virtual Environment

Environment Variables

📖 Notes

Detailed Day 2 learning notes:

👉 Notes.md

The notes cover the OpenAI client, API configuration, prompts, chat completions, model parameters, response extraction, and running the chatbot in a virtual environment.
