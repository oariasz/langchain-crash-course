# openai_tokens.py
import json
import os

def extract_tokens_and_cost(result, model_name="gpt-4"):
    """
    Extracts token usage and calculates cost from the result of a model invocation.
    
    Args:
        result: The response object from the ChatOpenAI model.
        model_name: The name of the OpenAI model used (default: "gpt-4").
    
    Returns:
        A dictionary with token usage and cost details.
    """
    # Token usage details (if available in result)
    token_usage = result.response_metadata.get("token_usage", {})
    completion_tokens = token_usage.get("completion_tokens", 0)
    prompt_tokens = token_usage.get("prompt_tokens", 0)
    total_tokens = token_usage.get("total_tokens", 0)
    
    # Approximate cost calculation
    # Adjust the pricing according to the model used
    pricing = {
        "gpt-4": {"prompt": 0.03, "completion": 0.06},  # per 1,000 tokens (USD)
        "gpt-4-32k": {"prompt": 0.06, "completion": 0.12},
        "gpt-3.5-turbo": {"prompt": 0.0015, "completion": 0.002}
    }
    cost = 0
    if model_name in pricing:
        cost = (
            (prompt_tokens / 1000) * pricing[model_name]["prompt"] +
            (completion_tokens / 1000) * pricing[model_name]["completion"]
        )
    
    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
        "total_cost": cost
    }


def print_token_usage(result, model_name="gpt-4"):
    """
    Calls `extract_tokens_and_cost`, formats the output, and prints token usage and cost details.
    
    Args:
        result: The response object from the ChatOpenAI model.
        model_name: The name of the OpenAI model used (default: "gpt-4").
    """
    usage_data = extract_tokens_and_cost(result, model_name)
    
    # Formatting and printing results
    print(f"{'Prompt Tokens:':<20} {usage_data['prompt_tokens']:>10,}")
    print(f"{'Completion Tokens:':<20} {usage_data['completion_tokens']:>10,}")
    print(f"{'Total Tokens:':<20} {usage_data['total_tokens']:>10,}")
    print(f"{'Total Cost ($):':<20} {usage_data['total_cost']:>10,.4f}")

TOKEN_USAGE_FILE = "token_usage.json"

def save_token_usage(usage_data, model_name):
    """
    Saves the token usage data to a JSON file, accumulating values across runs.

    Args:
        usage_data (dict): Dictionary with keys 'prompt_tokens', 'completion_tokens',
                           'total_tokens', 'total_cost', etc.
        model_name (str): The name of the model used.
    """
    # Initialize or load existing data
    if os.path.exists(TOKEN_USAGE_FILE):
        with open(TOKEN_USAGE_FILE, "r") as file:
            accumulated_data = json.load(file)
    else:
        accumulated_data = {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "total_cost": 0.0,
            "model_name": model_name
        }

    # Accumulate token usage
    accumulated_data["prompt_tokens"] += usage_data["prompt_tokens"]
    accumulated_data["completion_tokens"] += usage_data["completion_tokens"]
    accumulated_data["total_tokens"] += usage_data["total_tokens"]
    accumulated_data["total_cost"] += usage_data["total_cost"]

    # Save back to JSON file
    with open(TOKEN_USAGE_FILE, "w") as file:
        json.dump(accumulated_data, file, indent=4)

def get_total_token_usage():
    """
    Opens the JSON file and returns the total token usage and cost details.

    Returns:
        dict: Dictionary with keys 'prompt_tokens', 'completion_tokens',
              'total_tokens', 'total_cost', and 'model_name'.
    """
    if os.path.exists(TOKEN_USAGE_FILE):
        with open(TOKEN_USAGE_FILE, "r") as file:
            return json.load(file)
    else:
        return {
            "prompt_tokens": 0,
            "completion_tokens": 0,
            "total_tokens": 0,
            "total_cost": 0.0,
            "model_name": None
        }