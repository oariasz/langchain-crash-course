# Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/
# OpenAI Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/openai/

# main_script.py

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mylib.openai_tokens import extract_tokens_and_cost, print_token_usage, DEFAULT_MODEL
from mylib.myutils import clear_screen

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model=DEFAULT_MODEL)

# Example Usage
prompt = "What is 81 divided by 9? Give me only the number"
result = model.invoke(prompt)



# Extract token usage and cost
info = extract_tokens_and_cost(result)

clear_screen()
# Display results
print(f"Response Content: {result.content}")
print('\n\n')

print_token_usage(result, DEFAULT_MODEL)
print('\n\n')
print_token_usage(result, DEFAULT_MODEL, saved_totals=True)