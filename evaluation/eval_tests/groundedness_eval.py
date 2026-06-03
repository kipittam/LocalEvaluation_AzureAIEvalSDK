# Conversation mode:
import json
import os
from dotenv import load_dotenv
from azure.ai.evaluation import GroundednessEvaluator, Conversation

load_dotenv()


model_config = {
    "azure_endpoint": os.environ.get("AZURE_ENDPOINT"),
    "api_key": os.environ.get("AZURE_API_KEY"),
    "azure_deployment": os.environ.get("AZURE_DEPLOYMENT_NAME"),
    "api_version": os.environ.get("AZURE_API_VERSION"),
    "type": "azure_openai",
}

# Initialize the Groundedness evaluator:
groundedness_eval = GroundednessEvaluator(model_config, threshold=3)



conversation = Conversation(
    messages=[
        { "content": "Which tent is the most waterproof?", "role": "user" },
        { "content": "The Alpine Explorer Tent is the most waterproof", "role": "assistant", "context": "From the our product list the alpine explorer tent is the most waterproof. The Adventure Dining Table has higher weight." },
        { "content": "How much does it cost?", "role": "user" },
        { "content": "$120.", "role": "assistant", "context": "The Alpine Explorer Tent is $120."}
    ]
)

# Alternatively, you can load the same content from a JSONL file.
groundedness_conv_score = groundedness_eval(conversation=conversation)

output_dir = os.path.join(os.path.dirname(__file__), "..", "output_files")
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "groundedness_result.json")
with open(output_file, "w") as f:
    json.dump(groundedness_conv_score, f, indent=4)

print(f"Results saved to {output_file}")

