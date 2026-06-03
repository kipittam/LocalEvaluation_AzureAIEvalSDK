import os
from dotenv import load_dotenv
from azure.ai.evaluation import (
    CoherenceEvaluator,
    FluencyEvaluator,
    RelevanceEvaluator,
    F1ScoreEvaluator,
)

load_dotenv()

model_config = {
    "azure_endpoint": os.environ.get("AZURE_ENDPOINT"),
    "api_key": os.environ.get("AZURE_API_KEY"),
    "azure_deployment": os.environ.get("AZURE_DEPLOYMENT_NAME"),
    "api_version": os.environ.get("AZURE_API_VERSION"),
    "type": "azure_openai",
}

coherence_eval = CoherenceEvaluator(model_config, threshold =3)
fluency_eval = FluencyEvaluator(model_config, threshold =3)
relevance_eval = RelevanceEvaluator(model_config, threshold =3)
f1_score_eval = F1ScoreEvaluator(threshold =0.5)
