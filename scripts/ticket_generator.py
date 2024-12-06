from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
api_key=os.getenv('OPENAI_API_KEY')
PROMPT = os.getenv('MODEL_PROMPT', '')
    
# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def generate_ticket_content(category: str = None) -> tuple: # type: ignore
    """
    Generate synthetic ticket title and description using OpenAI.
    """
    base_prompt = PROMPT

    if category:
        base_prompt += f"\nThe ticket should be related to {category}."

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": base_prompt}
            ],
            temperature=0.7,
            max_tokens=250
        )
        
        content = response.choices[0].message.content
        
        # Parse the response to separate title and description
        parts = content.split('Description:', 1) # type: ignore
        title = parts[0].replace('Title:', '').strip()
        description = parts[1].strip() if len(parts) > 1 else parts[0]
        
        return title, description
        
    except Exception as e:
        print(f"Error generating ticket content: {str(e)}")
        return None, None