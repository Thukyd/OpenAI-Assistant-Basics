import openai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set the API key
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("OPENAI_API_KEY environment variable not set")

openai.api_key = api_key

# Now you can use the openai library functions
# Example: creating a completion
# Replace with your actual function call as needed
completion = openai.chat.completions.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair."},
    {"role": "user", "content": "Compose a poem that explains the concept of recursion in programming."}
  ]
)

print(completion.choices[0].message)