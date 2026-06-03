# # Custom evaluator: Answer Length
# # Measures the length of the response (character count and word count).
# # This is a simple, non-AI evaluator — no LLM calls required.
# import json
# import os
# from dotenv import load_dotenv
# from azure.ai.evaluation import Conversation

# load_dotenv()


# class AnswerLengthEvaluator:
#     """Evaluates the length of an answer/response."""

#     def __init__(self):
#         pass

#     def __call__(self, *, response: str, **kwargs) -> dict:
#         """Compute the length metrics for a given response.

#         Args:
#             response: The response text to measure.

#         Returns:
#             A dictionary with answer length metrics.
#         """
#         return {
#             "answer_length": len(response),
#             "answer_word_count": len(response.split()),
#         }


# # Initialize the evaluator instance (imported by evaluate.py)
# answer_length = AnswerLengthEvaluator()


# conversation = Conversation(
#     messages=[
#         { "content": "Which tent is the most waterproof?", "role": "user" },
#         { "content": "The Alpine Explorer Tent is the most waterproof", "role": "assistant", "context": "From the our product list the alpine explorer tent is the most waterproof. The Adventure Dining Table has higher weight." },
#         { "content": "How much does it cost?", "role": "user" },
#         { "content": "$120.", "role": "assistant", "context": "The Alpine Explorer Tent is $120."}
#     ]
# )

# # Evaluate each assistant response in the conversation
# answer_length_results = []
# for msg in conversation["messages"]:
#     if msg["role"] == "assistant":
#         content = str(msg["content"])
#         result = answer_length(response=content)
#         result["response"] = content
#         answer_length_results.append(result)

# # Save results to output folder
# output_dir = os.path.join(os.path.dirname(__file__), "output")
# os.makedirs(output_dir, exist_ok=True)
# output_file = os.path.join(output_dir, "answer_length_result.json")
# with open(output_file, "w") as f:
#     json.dump(answer_length_results, f, indent=4)

# print(f"Results saved to {output_file}")
