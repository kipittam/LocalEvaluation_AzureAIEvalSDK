import os
from azure.ai.evaluation import evaluate

from groundedness_eval import groundedness_eval
#from answer_length_eval import answer_length

data_file = os.path.join(os.path.dirname(__file__), "..", "input", "data.jsonl")

result = evaluate(
    data=data_file, # Provide your data here:
    evaluators={
        "groundedness": groundedness_eval
        #"answer_length": answer_length
    },
    # Column mapping:
    evaluator_config={
        "groundedness": {
            "column_mapping": {
                "query": "${data.query}",
                "context": "${data.context}",
                "response": "${data.response}"
            } 
        }
    },
    # Optionally, provide your Foundry project information to track your evaluation results in your project portal.
   # azure_ai_project = azure_ai_project,
    # Optionally, provide an output path to dump a JSON file of metric summary, row-level data, and the metric and Foundry project URL.
    output_path=os.path.join(os.path.dirname(__file__), "..", "output_files", "myevalresults.json")
)