"""
    Example to show how to use the OpenAI assistants work.

    To get more information about the OpenAI Asssistants, see the documentation: https://platform.openai.com/docs/assistants/how-it-works/objects
    At creation time it was still in beta. 
"""

import os
from dotenv import load_dotenv
import openai
import logging  # Import the logging module
import time # used to wait for the assistant to answer

####################################################################################################
### A) Initialize the OpenAI client

# Setup basic configuration for logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def initialize_openai_client():
    """
    Initializes the OpenAI client by loading the API key from environment variables.
    """
    load_dotenv()  # Load environment variables from .env file
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key is None:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    openai.api_key = api_key
    return openai  # Return the openai module for convenience

# Initialize the OpenAI client
client = initialize_openai_client()

####################################################################################################
### B) Create an assistant
"""
    Purpose-built AI that uses OpenAI’s models and calls tools.
    You should not create this with every request, but rather once per assistant.

"""

# Create a new assistant
assistant = client.beta.assistants.create(
    name = "Math Tutor",
    instructions = "You are a personal math tutor. Write and run code to answer math questions.",
    tools = [{"type": "code_interpreter"}], # The tools that the assistant can use, her it is the code interpreter tool, could be also file interpreter etc.
    model = "gpt-4-1106-preview" # The newes model that support assistants
)

####################################################################################################
### C) Create a thread (session)
"""
    A conversation session between an Assistant and a user.
    Threads store Messages and automatically handle truncation to fit content into a model’s context.

"""
thread = client.beta.threads.create()
logging.info(f'Thread Object: {thread}')  # DEBUG: Info about the thread object


####################################################################################################
### D) Add a message to the thread (form a message)
"""
    A message created by an Assistant or a user. 
    Messages can include text, images, and other files. Messages stored as a list on the Thread.
"""
message = client.beta.threads.messages.create(
    thread_id = thread.id, # To which thread do you want to link the message to?
    role = "user",
    content = "Solve this problem: 3x + 11 = 14" # The message that you would normally send to the assistant. 
)
logging.info(f'Message Object: {message}')  # DEBUG: Info about the message object


####################################################################################################
### E) Run the assistant on the thread (send the message to the assistant)
"""
    An invocation of an Assistant on a Thread. 
    The Assistant uses it’s configuration and the Thread’s Messages to perform tasks by calling models and tools. 
    As part of a Run, the Assistant appends Messages to the Thread.

"""
run = client.beta.threads.runs.create(
    thread_id = thread.id,
    assistant_id = assistant.id
)




####################################################################################################
### F) Check the status of the run

# the code should only continue if the run is completed, see also: https://platform.openai.com/docs/assistants/how-it-works/runs-and-run-steps 
while True:
    # Retrieve the latest status of the run
    run_status = client.beta.threads.runs.retrieve(
        thread_id=thread.id,
        run_id=run.id
    ).status

    # Log the current status
    logging.debug(f'Checking run status: {run_status}')

    # Check if the status is 'completed'
    if run_status == 'completed':
        break  # Exit the loop if completed

    # Wait for 1 second before checking again
    time.sleep(1)

# Continue with your script after the run is completed
logging.debug(f'Run completed with status: {run_status}')


####################################################################################################
### G) Retrieve the messages from the thread

# Retrive all the messages which are inside run
messages = client.beta.threads.messages.list(
    thread_id = thread.id,
)

# Print out all the messages that have been sent between the user and the assistant
#   in reverse because the oldest messages should be shown first
print("\n\n### Messages ###")
for message in reversed(messages.data):
    print(message.role + ": " + message.content[0].text.value)


