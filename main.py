from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

# Using Google Generative AI for portability with an API key
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Import the functions and their input schemas from your tools file
from tools import (
    note_maker,
    flashcard_generator,
    concept_explainer,
    UserInfo
)

# Load environment variables from .env file
load_dotenv()

# --- 1. Set up the LLM and the list of available tools ---
# We explicitly pass the API key from the environment variable.
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0,
    google_api_key=os.getenv("GEMINI_API_KEY")
)

# This list contains the functions the LLM can choose from.
tools = [
    note_maker,
    flashcard_generator,
    concept_explainer,
]


# --- 2. Create the Agent ---
# The prompt is a set of instructions that guides the LLM's behavior.
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI tutor assistant. You have access to several tools to help students. Use them when appropriate. The user's profile information is included in their message."),
        ("user", "{input}"),
        ("placeholder", "{agent_scratchpad}"), # This is where the agent's intermediate steps are stored
    ]
)

# Create the agent that will use the LLM, tools, and prompt to make decisions.
agent = create_tool_calling_agent(llm, tools, prompt)

# The AgentExecutor is the runtime for the agent. It executes the tool calls.
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# --- 3. Set up the FastAPI server ---
app = FastAPI(
    title="AI Tutor Orchestrator",
    description="An intelligent middleware to connect an AI tutor with educational tools."
)

# Add CORS middleware to allow the frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your frontend's domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str
    user_info: UserInfo

@app.post("/invoke-agent")
def invoke_agent_endpoint(request: QueryRequest):
    """
    This endpoint receives a user query and user info, invokes the agent,
    and returns the final, user-friendly response.
    """
    print(f"Received query: {request.query}")
    
    # We combine the query and user info into a single input for the agent.
    # This ensures the LLM has all context needed to populate tool parameters.
    input_prompt = f"User Query: '{request.query}'\n\nUser Info: {request.user_info.model_dump_json(indent=2)}"

    # The .invoke() method runs the entire agent chain
    response = agent_executor.invoke({
        "input": input_prompt,
    })

    return {"response": response["output"]}

