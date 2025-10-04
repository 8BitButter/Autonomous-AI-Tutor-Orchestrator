import pydantic
from typing import Literal
from langchain.tools import tool

# --- Pydantic Schemas for Structured Input Validation ---

class UserInfo(pydantic.BaseModel):
    """Student profile information. This is required by all tools."""
    user_id: str = pydantic.Field(description="Unique identifier for the student.")
    name: str = pydantic.Field(description="Student's full name.")
    grade_level: str = pydantic.Field(description="Student's current grade level.")
    mastery_level_summary: str = pydantic.Field(description="Current mastery level, e.g., 'Level 4: Building foundational knowledge'.")
    emotional_state_summary: str = pydantic.Field(description="Current emotional state, e.g., 'Focused and motivated'.")


# --- Tool Functions ---
# The `@tool` decorator automatically converts a Python function into a format
# that LangChain and the LLM can understand. The docstring is critical as it
# tells the LLM what the tool does and when to use it.

@tool
def note_maker(
    topic: str,
    subject: str,
    note_taking_style: Literal["outline", "bullet_points", "narrative", "structured"],
    user_info: UserInfo
) -> dict:
    """
    Generates structured notes on a specific topic and subject for a student.
    Use this when a student wants to summarize, review, or get notes on a topic.
    The user's profile information MUST be passed in the user_info argument.
    """
    print(f"🤖 Calling Note Maker for topic: {topic}")
    # In a real application, this would make an API call to a note-making service.
    return {
        "status": "success",
        "title": f"Notes on {topic}",
        "summary": f"These are {note_taking_style} notes about {topic} in {subject}, prepared for {user_info.name}.",
        "note_sections": [{"title": "Key Point 1", "content": "Detailed content about the key point goes here..."}]
    }

@tool
def flashcard_generator(
    topic: str,
    subject: str,
    count: int,
    difficulty: Literal["easy", "medium", "hard"],
    user_info: UserInfo
) -> dict:
    """
    Creates a set of flashcards for a given topic to help a student study.
    Use this when a student asks for flashcards, a quiz, or practice questions.
    The number of flashcards is defined by 'count'. The difficulty can be 'easy', 'medium', or 'hard'.
    The user's profile information MUST be passed in the user_info argument.
    """
    print(f"🤖 Calling Flashcard Generator for topic: {topic}")
    # In a real application, this would make an API call to a flashcard service.
    return {
        "status": "success",
        "topic": topic,
        "flashcards": [
            {"question": f"What is a key aspect of {topic}?", "answer": "This is the answer."}
            for _ in range(count)
        ],
        "difficulty": difficulty
    }

@tool
def concept_explainer(
    concept_to_explain: str,
    subject: str,
    desired_depth: Literal["basic", "intermediate", "advanced"],
    user_info: UserInfo
) -> dict:
    """
    Explains a specific concept to a student in detail.
    Use this when a student asks 'what is X?', 'can you explain X?', or expresses confusion about a concept.
    The user's profile information MUST be passed in the user_info argument.
    """
    print(f"🤖 Calling Concept Explainer for concept: {concept_to_explain}")
    # In a real application, this would make an API call to an explanation service.
    return {
        "status": "success",
        "explanation": f"Here is a {desired_depth} explanation of {concept_to_explain} in {subject} for {user_info.name}.",
        "related_concepts": ["Related Concept A", "Related Concept B"]
    }

