# QA Evaluator: Demonstrates multiple evaluators from azure.ai.evaluation
# Evaluators: Groundedness, Relevance, Coherence, Fluency, Similarity, F1Score
import json
import os
from dotenv import load_dotenv
from azure.ai.evaluation import (
    QAEvaluator,
    GroundednessEvaluator,
    RelevanceEvaluator,
    CoherenceEvaluator,
    FluencyEvaluator,
    SimilarityEvaluator,
    F1ScoreEvaluator,
)

load_dotenv()

# Azure OpenAI model configuration (used by AI-assisted evaluators)
model_config = {
    "azure_endpoint": os.environ.get("AZURE_ENDPOINT"),
    "api_key": os.environ.get("AZURE_API_KEY"),
    "azure_deployment": os.environ.get("AZURE_DEPLOYMENT_NAME"),
    "api_version": os.environ.get("AZURE_API_VERSION"),
    "type": "azure_openai",
}

# --- Sample QA data ---
query = "Which tent is the most waterproof?"
context = (
    "From our product list, the Alpine Explorer Tent is the most waterproof. "
    "It has a waterproof rating of 3000mm and uses double-sealed seams. "
    "The Adventure Dining Table has higher weight but is not waterproof."
)
response = "The Alpine Explorer Tent is the most waterproof, with a 3000mm rating and double-sealed seams."
ground_truth = "The Alpine Explorer Tent is the most waterproof tent available."

# ============================================================
# 1. QAEvaluator — runs all built-in QA evaluators in one call
# ============================================================
print("=" * 60)
print("1. QAEvaluator (composite — runs all QA metrics at once)")
print("=" * 60)

qa_eval = QAEvaluator(model_config=model_config)

qa_result = qa_eval(
    query=query,
    context=context,
    response=response,
    ground_truth=ground_truth,
)
print(json.dumps(qa_result, indent=4))

# ============================================================
# 2. Individual evaluators — run each one separately
# ============================================================
results = {}

# --- Groundedness ---
print("\n" + "=" * 60)
print("2. GroundednessEvaluator")
print("=" * 60)

groundedness_eval = GroundednessEvaluator(model_config)
groundedness_result = groundedness_eval(
    query=query,
    context=context,
    response=response,
)
print(json.dumps(groundedness_result, indent=4))
results["groundedness"] = groundedness_result

# --- Relevance ---
print("\n" + "=" * 60)
print("3. RelevanceEvaluator")
print("=" * 60)

relevance_eval = RelevanceEvaluator(model_config)
relevance_result = relevance_eval(
    query=query,
    response=response,
)
print(json.dumps(relevance_result, indent=4))
results["relevance"] = relevance_result

# --- Coherence ---
print("\n" + "=" * 60)
print("4. CoherenceEvaluator")
print("=" * 60)

coherence_eval = CoherenceEvaluator(model_config)
coherence_result = coherence_eval(
    query=query,
    response=response,
)
print(json.dumps(coherence_result, indent=4))
results["coherence"] = coherence_result

# --- Fluency ---
print("\n" + "=" * 60)
print("5. FluencyEvaluator")
print("=" * 60)

fluency_eval = FluencyEvaluator(model_config)
fluency_result = fluency_eval(
    response=response,
)
print(json.dumps(fluency_result, indent=4))
results["fluency"] = fluency_result

# --- Similarity ---
print("\n" + "=" * 60)
print("6. SimilarityEvaluator")
print("=" * 60)

similarity_eval = SimilarityEvaluator(model_config)
similarity_result = similarity_eval(
    query=query,
    response=response,
    ground_truth=ground_truth,
)
print(json.dumps(similarity_result, indent=4))
results["similarity"] = similarity_result

# --- F1 Score ---
print("\n" + "=" * 60)
print("7. F1ScoreEvaluator")
print("=" * 60)

f1_eval = F1ScoreEvaluator()
f1_result = f1_eval(
    response=response,
    ground_truth=ground_truth,
)
print(json.dumps(f1_result, indent=4))
results["f1_score"] = f1_result

# ============================================================
# Save all results to the output folder
# ============================================================
all_results = {
    "qa_evaluator_composite": qa_result,
    "individual_evaluators": results,
}

output_dir = os.path.join(os.path.dirname(__file__), "..", "output_files")
os.makedirs(output_dir, exist_ok=True)
output_file = os.path.join(output_dir, "composite_qa_evaluator_result.json")
with open(output_file, "w") as f:
    json.dump(all_results, f, indent=4)

print(f"\nAll results saved to {output_file}")
