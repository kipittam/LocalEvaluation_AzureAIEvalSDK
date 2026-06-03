import os
from azure.ai.evaluation import evaluate

from groundedness_eval import groundedness_eval
from quality_evals import coherence_eval, fluency_eval, relevance_eval, f1_score_eval


data_file = os.path.join(os.path.dirname(__file__), "..", "input", "data.jsonl")

result = evaluate(
    data=data_file, # Provide your data here:
    evaluators={
        "groundedness": groundedness_eval,
        "coherence": coherence_eval,
        "fluency": fluency_eval,
        "relevance": relevance_eval,
        "f1_score": f1_score_eval,
    },
    # Column mapping:
    evaluator_config={
        "groundedness": {
            "column_mapping": {
                "query": "${data.query}",
                "context": "${data.context}",
                "response": "${data.response}"
            } 
        },
        "coherence": {
            "column_mapping": {
                "query": "${data.query}",
                "context": "${data.context}",
                "response": "${data.response}"
            }
        },
        "fluency": {
            "column_mapping": {
                "query": "${data.query}",
                "context": "${data.context}",
                "response": "${data.response}"
            }
        },
        "relevance": {
            "column_mapping": {
                "query": "${data.query}",
                "context": "${data.context}",
                "response": "${data.response}"
            }
        },
        "f1_score": {
            "column_mapping": {
                "response": "${data.response}",
                "context": "${data.context}",
                "ground_truth": "${data.ground_truth}"
            }
        },
    },
    # Optionally, provide your Foundry project information to track your evaluation results in your project portal.
   # azure_ai_project = azure_ai_project,
    # Optionally, provide an output path to dump a JSON file of metric summary, row-level data, and the metric and Foundry project URL.
    output_path=os.path.join(os.path.dirname(__file__), "..", "output_files", "myeval_test_results.json")
)