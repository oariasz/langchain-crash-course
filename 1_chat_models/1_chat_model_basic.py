# Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/
# OpenAI Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/openai/

# main_script.py

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mylib.openai_tokens import extract_tokens_and_cost

# Load environment variables from .env
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4")

# Example Usage
prompt = "What is 81 divided by 9?"
result = model.invoke(prompt)



# Extract token usage and cost
info = extract_tokens_and_cost(result)

# Display results
print(f"Response Content: {result.content}")
print('\n\n')

print('result = ')
print(type(result))
print(result)

print(f"Prompt Tokens:     {info['prompt_tokens']}")
print(f"Completion Tokens: {info['completion_tokens']}")
print(f"Total Tokens:      {info['total_tokens']}")
print(f"Total Cost (USD): ${info['total_cost']:.6f}")
