import os
import json
import re
import google.generativeai as genai
from dotenv import load_dotenv
from prompts import TEXT_TO_JSON_PROMPT, JSON_TO_TEXT_PROMPT

# Load environment variables from .env file
load_dotenv()

def configure_gemini():
    """Configures the Gemini API with the key from environment variables."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file.")
    genai.configure(api_key=api_key)

def clean_json_response(text_response: str) -> str:
    """Cleans the Gemini response to extract a valid JSON string."""
    # Use regex to find the content between the first { and the last }
    match = re.search(r'\{.*\}', text_response, re.DOTALL)
    if match:
        return match.group(0)
    # Fallback for simple cases
    return text_response.strip().lstrip('```json').rstrip('```')

def generate_tool_json(user_query: str, user_info: dict) -> dict:
    """
    First API call: Takes a user query and generates a structured JSON object
    for the appropriate educational tool.
    """
    print("Step 1: Converting text query to structured JSON...")
    
    # Format the prompt with the student's data
    prompt = TEXT_TO_JSON_PROMPT.format(
        user_info=json.dumps(user_info, indent=2),
        user_query=user_query
    )
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    
    try:
        # Clean the response to ensure it's valid JSON
        cleaned_response = clean_json_response(response.text)
        # Parse the JSON string into a Python dictionary
        return json.loads(cleaned_response)
    except (json.JSONDecodeError, IndexError) as e:
        print(f"Error: Failed to parse JSON from the response. Details: {e}")
        print(f"Raw Response:\n---\n{response.text}\n---")
        return None

def get_tutor_response(tool_json: dict) -> str:
    """
    Second API call: Takes the structured JSON and generates a
    user-friendly text response.
    """
    if not tool_json:
        return "I'm sorry, I encountered an issue processing your request. Please try again."

    print("\nStep 2: Generating a text response from the JSON...")
    
    prompt = JSON_TO_TEXT_PROMPT.format(
        tool_json=json.dumps(tool_json, indent=2)
    )
    
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    
    return response.text

def main():
    """Main function to run the orchestrator demonstration."""
    configure_gemini()
    
    # Mock student profile data, as described in the provided documents[cite: 633, 584].
    mock_user_info = {
        "user_id": "student123",
        "name": "Alex",
        "grade_level": "10",
        "learning_style_summary": "Prefers visual aids and clear examples.",
        "emotional_state_summary": "Curious and engaged",
        "mastery_level_summary": "Level 5: Developing competence"
    }

    # --- DEMONSTRATION SCENARIOS ---
    
    # Scenario 1: Student needs an explanation
    query1 = "I don't really get how photosynthesis works. Can you explain it simply?"
    
    # Scenario 2: Student wants to create flashcards for practice
    query2 = "I need to study for my Biology test on the human heart. Can you make me 5 medium-difficulty flashcards?"
    
    # Scenario 3: Student needs structured notes
    query3 = "Can you make me some outline-style notes on the main causes of World War II for my history class? Please include some analogies to help me understand."

    queries = [query1, query2, query3]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{'='*20} SCENARIO {i} {'='*20}")
        print(f"Student Query: \"{query}\"")
        print("-" * 52)
        
        # Step 1: Generate the JSON
        generated_json = generate_tool_json(query, mock_user_info)
        
        if generated_json:
            print("\n✅ Successfully generated JSON:")
            print(json.dumps(generated_json, indent=2))
        
            # Step 2: Generate the final text response
            final_response = get_tutor_response(generated_json)
            
            print("\n✅ Final Tutor Response:")
            print("-" * 25)
            print(final_response)
        
        print(f"{'='*52}\n")

if __name__ == "__main__":
    main()