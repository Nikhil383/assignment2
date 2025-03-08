import json
import torch  # Added import for torch.dtype
from langchain.llms import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Load smaller model: facebook/opt-125m
model_name = "facebook/opt-125m"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, torch_dtype=torch.float16)  # Fixed: Use torch.float16
pipe = pipeline("text-generation", model=model, tokenizer=tokenizer, max_length=100)
llm = HuggingFacePipeline(pipeline=pipe)

QUERIES_FILE = "Queries_generated.txt"

def generate_mongo_query(user_input):
    """Generate a MongoDB query using the LLM."""
    prompt = f"""
    Given the user query: "{user_input}", generate a MongoDB query in JSON format.
    Example: For "Products with price > 50", output: {{"Price": {{"$gt": 50}}}}
    Only return the JSON query string, nothing else.
    """
    try:
        print(f"Generating query for: {user_input}")
        response = llm(prompt)
        raw_output = response[0]['generated_text'].strip()
        print(f"Raw model output: {raw_output}")

        # Attempt to extract JSON from output
        if "{" in raw_output and "}" in raw_output:
            query_str = raw_output[raw_output.index('{'):raw_output.rindex('}')+1]
        else:
            # Fallback: Parse simple "field > value" queries manually
            if ">" in user_input:
                field, value = user_input.split("with")[1].split(">")
                query_str = f'{{"{field.strip()}": {{"$gt": {value.strip()}}}}}'
            else:
                raise ValueError("No valid JSON or supported query format found in output")

        query = json.loads(query_str)
        print(f"Parsed query: {query}")

        with open(QUERIES_FILE, "a") as f:
            f.write(f"User Input: {user_input}\nQuery: db.collection.find({json.dumps(query)})\n\n")
        return query
    except Exception as e:
        print(f"Error generating query: {e}")
        return None