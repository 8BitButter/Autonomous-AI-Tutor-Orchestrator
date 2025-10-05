# Autonomous AI Tutor Orchestrator

This project is an intelligent middleware orchestrator that connects a conversational AI tutor with multiple educational tools. It acts as the "brain" that understands a student's conversational query, determines which tool is needed (e.g., a note maker, flashcard generator), extracts the necessary parameters, and executes the tool.

The core of this project is a multi-tool agent built with LangChain, using Google's Gemini 1.5 Flash model for reasoning, and served via a FastAPI backend.

## Features

*   **Intelligent Tool Selection:** Dynamically chooses the correct educational tool based on the user's query.
*   **Automatic Parameter Extraction:** Extracts and infers required parameters from natural language.
*   **Scalable Architecture:** Tools are defined in a separate module, making it easy to add more.
*   **FastAPI Backend:** A robust and fast API server to handle requests.
*   **Simple Frontend:** A basic HTML/JavaScript interface to interact with the agent.

## Project Structure

```
.
├── .env                  # Your environment variables (API key)
├── main.py               # FastAPI application and agent logic
├── tools.py              # Definitions for all educational tools
├── requirements.txt      # Python dependencies
├── index.html            # Simple frontend for interaction
└── README.md             # This file
```

## Getting Started

### 1. Prerequisites

*   Python 3.9+
*   A Gemini API Key. You can get one from Google AI Studio.

### 2. Clone the Repository

Clone this project to your local machine.

### 3. Set Up Environment Variables

Create a `.env` file in the root directory by copying the `.env.example` file, and add your Gemini API Key:

```
GEMINI_API_KEY="your-gemini-api-key-here"
```

### 4. Install Dependencies

Install the required Python packages from `requirements.txt`:

```
pip install -r requirements.txt
```

### 5. Run the Backend Server

Start the FastAPI application using Uvicorn:

```
uvicorn main:app --reload
```

The server will be running at `http://127.0.0.1:8000`. You can access the API documentation at `http://127.0.0.1:8000/docs`.

### 6. Use the Frontend

Open the `index.html` file in your web browser. You can now type in queries and see the AI tutor agent in action