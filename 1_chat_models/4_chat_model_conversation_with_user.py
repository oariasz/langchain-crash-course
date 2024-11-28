from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
from mylib.openai_tokens import extract_tokens_and_cost, print_token_usage, DEFAULT_MODEL, print_all_token_usage
from mylib.myutils import clear_screen
from pprint import pprint

clear_screen()

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model=DEFAULT_MODEL)


chat_history = []  # Use a list to store messages

# Set an initial system message (optional)
system_message = SystemMessage(content="You are a helpful AI assistant.")
chat_history.append(system_message)  # Add system message to chat history

# Chat loop
while True:
    query = input("You: ")
    if query.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=query))  # Add user message

    # Get AI response using history
    result = model.invoke(chat_history)
    response = result.content
    chat_history.append(AIMessage(content=response))  # Add AI message
    pprint(f"AI: {response}")
    # print_all_token_usage(result=result)


print("---- Message History ----")
print(chat_history)

