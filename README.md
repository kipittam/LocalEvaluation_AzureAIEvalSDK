# Local Evaluation with Azure AI Evaluation SDK

## Project Objective

This project demonstrates how to run **local AI quality evaluations** using the [Azure AI Evaluation SDK](https://learn.microsoft.com/en-us/azure/ai-studio/how-to/develop/evaluate-sdk). It provides ready-to-run scripts that assess LLM-generated responses for groundedness, relevance, coherence, fluency, similarity, and F1 score — all executed locally against an Azure OpenAI endpoint without requiring an Azure AI Foundry project.

## Project Folder Structure

```
LocalEvaluation_AzureAIEvalSDK/
├── requirements.txt                  # Python dependencies
├── evaluation/
│   ├── .env                          # Environment variables (Azure OpenAI credentials)
│   ├── input/
│   │   └── data.jsonl                # Sample QA dataset (query, context, response, ground_truth)
│   ├── output_files/                 # Generated evaluation results (JSON + dashboard image)
│   │   ├── groundedness_result.json
│   │   ├── qa_evaluator_result.json
│   │   ├── myevalresults.json
│   │   ├── myevalresults_001.json
│   │   ├── myeval_test_results.json
│   │   └── eval_dashboard.png
│   └── eval_tests/
│       ├── __init__.py
│       ├── evaluate.py               # Batch evaluation using the evaluate() API with data.jsonl
│       ├── groundedness_eval.py      # Standalone groundedness evaluation on a conversation
│       ├── quality_evals.py          # Reusable evaluator instances (coherence, fluency, relevance, F1)
│       ├── qa_evaluator.py           # Comprehensive QA evaluation (composite + individual evaluators)
│       ├── dashboard.py              # Matplotlib dashboard — visualizes batch evaluation results
│       ├── dashboard.ipynb           # Interactive notebook version of the dashboard
│       ├── f1_score_calcualtion_Conversation.md  # Walkthrough of token-level F1 score calculation
│       └── archive/
│           ├── answer_length_eval.py # Archived: custom answer-length evaluator
│           └── safety_evaluator.py   # Archived: safety evaluator
```

## Dependencies

All dependencies are listed in `requirements.txt`:

| Package                | Description                                                        |
|------------------------|--------------------------------------------------------------------|
| `azure-ai-evaluation`  | Azure AI Evaluation SDK — provides built-in evaluators and the `evaluate()` API |
| `azure-identity`       | Azure Identity library for authentication                          |
| `python-dotenv`        | Loads environment variables from a `.env` file                     |
| `matplotlib`           | Plotting library used for the evaluation dashboard                 |
| `numpy`                | Numerical computing library used for dashboard data processing     |

## How to Execute This Project

### Prerequisites

- **Python 3.9+** installed
- An **Azure OpenAI** resource with a deployed model (e.g., `gpt-4o`)

### 1. Clone the repository

```bash
git clone <repository-url>
cd LocalEvaluation_AzureAIEvalSDK
```

### 2. Create and activate a virtual environment

```bash
python -m venv .azureaieval
# Windows PowerShell:
.azureaieval\Scripts\Activate.ps1
# macOS / Linux:
source .azureaieval/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create or update `evaluation/.env` with your Azure OpenAI credentials:

```env
AZURE_ENDPOINT=https://<your-resource>.openai.azure.com/
AZURE_API_KEY=<your-api-key>
AZURE_DEPLOYMENT_NAME=<your-deployment-name>
AZURE_API_VERSION=2024-12-01-preview
```

### 5. Run the evaluations

Navigate to the test scripts directory and run any of the evaluation scripts:

```bash
cd evaluation/eval_tests
```

| Script                   | What it does                                                                                       |
|--------------------------|----------------------------------------------------------------------------------------------------|
| `python groundedness_eval.py` | Evaluates groundedness on a hardcoded multi-turn conversation. Outputs `groundedness_result.json`. |
| `python qa_evaluator.py`      | Runs composite QA evaluation + individual evaluators (groundedness, relevance, coherence, fluency, similarity, F1). Outputs `qa_evaluator_result.json`. |
| `python evaluate.py`          | Batch-evaluates the dataset in `input/data.jsonl` using the SDK's `evaluate()` API with groundedness, coherence, fluency, relevance, and F1 evaluators. Outputs `myeval_test_results.json`. |
| `python dashboard.py`         | Generates a multi-panel matplotlib dashboard (radar chart, heatmap, bar charts, token usage) from `myeval_test_results.json`. Saves `eval_dashboard.png`. |

The `dashboard.ipynb` notebook provides the same dashboard visualizations in an interactive, cell-by-cell format.

All results are written to the `evaluation/output_files/` folder.
