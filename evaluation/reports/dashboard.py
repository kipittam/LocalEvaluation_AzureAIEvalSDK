import json
import os
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np

# Load evaluation results
results_path = os.path.join(os.path.dirname(__file__), "..", "output_files", "myeval_test_results.json")
with open(results_path, "r") as f:
    data = json.load(f)

rows = data["rows"]
metrics = data["metrics"]

# Extract per-row data
queries = [r["inputs.query"] for r in rows]
short_queries = [q if len(q) <= 30 else q[:27] + "..." for q in queries]

groundedness_scores = [r["outputs.groundedness.groundedness"] for r in rows]
coherence_scores = [r["outputs.coherence.coherence"] for r in rows]
fluency_scores = [r["outputs.fluency.fluency"] for r in rows]
relevance_scores = [r["outputs.relevance.relevance"] for r in rows]
f1_scores = [r["outputs.f1_score.f1_score"] for r in rows]

groundedness_results = [r["outputs.groundedness.groundedness_result"] for r in rows]
coherence_results = [r["outputs.coherence.coherence_result"] for r in rows]
fluency_results = [r["outputs.fluency.fluency_result"] for r in rows]
relevance_results = [r["outputs.relevance.relevance_result"] for r in rows]
f1_results = [r["outputs.f1_score.f1_result"] for r in rows]

# --- Dashboard ---
fig = plt.figure(figsize=(22, 18), facecolor="#f8f9fa")
fig.suptitle("Azure AI Evaluation Dashboard", fontsize=22, fontweight="bold", y=0.98, color="#1a1a2e")

gs = gridspec.GridSpec(3, 3, hspace=0.45, wspace=0.35, top=0.93, bottom=0.06, left=0.07, right=0.95)

colors = {
    "groundedness": "#e74c3c",
    "coherence": "#3498db",
    "fluency": "#2ecc71",
    "relevance": "#f39c12",
    "f1_score": "#9b59b6",
}

# ── Panel 1: Aggregate Metrics Bar Chart ──
ax1 = fig.add_subplot(gs[0, 0])
agg_labels = ["Groundedness", "Coherence", "Fluency", "Relevance", "F1 Score"]
agg_values = [
    metrics["groundedness.groundedness"],
    metrics["coherence.coherence"],
    metrics["fluency.fluency"],
    metrics["relevance.relevance"],
    metrics["f1_score.f1_score"],
]
bar_colors = [colors["groundedness"], colors["coherence"], colors["fluency"], colors["relevance"], colors["f1_score"]]
bars = ax1.bar(agg_labels, agg_values, color=bar_colors, edgecolor="white", linewidth=1.2)
for bar, val in zip(bars, agg_values):
    ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.08, f"{val:.2f}",
             ha="center", va="bottom", fontsize=10, fontweight="bold")
ax1.set_ylim(0, 5.5)
ax1.set_ylabel("Average Score", fontsize=11)
ax1.set_title("Overall Average Scores", fontsize=13, fontweight="bold", pad=10)
ax1.tick_params(axis="x", rotation=20)
ax1.axhline(y=3, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)
ax1.text(4.5, 3.1, "threshold=3", fontsize=8, color="gray", ha="right")

# ── Panel 2: Binary Pass Rate (Donut Charts) ──
ax2 = fig.add_subplot(gs[0, 1])
binary_labels = ["Groundedness", "Coherence", "Fluency", "Relevance", "F1 Score"]
binary_values = [
    metrics["groundedness.binary_aggregate"],
    metrics["coherence.binary_aggregate"],
    metrics["fluency.binary_aggregate"],
    metrics["relevance.binary_aggregate"],
    metrics["f1_score.binary_aggregate"],
]
bar_positions = np.arange(len(binary_labels))
bars2 = ax2.barh(bar_positions, binary_values, color=bar_colors, edgecolor="white", height=0.6)
for bar, val in zip(bars2, binary_values):
    ax2.text(val + 0.02, bar.get_y() + bar.get_height() / 2, f"{val * 100:.0f}%",
             ha="left", va="center", fontsize=10, fontweight="bold")
ax2.set_yticks(bar_positions)
ax2.set_yticklabels(binary_labels, fontsize=10)
ax2.set_xlim(0, 1.25)
ax2.set_xlabel("Pass Rate", fontsize=11)
ax2.set_title("Binary Pass Rate per Metric", fontsize=13, fontweight="bold", pad=10)
ax2.axvline(x=1.0, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)

# ── Panel 3: Per-Query Radar Chart ──
ax3 = fig.add_subplot(gs[0, 2], polar=True)
categories = ["Groundedness", "Coherence", "Fluency", "Relevance", "F1 (×5)"]
n_cats = len(categories)
angles = np.linspace(0, 2 * np.pi, n_cats, endpoint=False).tolist()
angles += angles[:1]

for i, query in enumerate(short_queries):
    values = [
        groundedness_scores[i],
        coherence_scores[i],
        fluency_scores[i],
        relevance_scores[i],
        f1_scores[i] * 5,  # scale F1 to 0-5 range for comparison
    ]
    values += values[:1]
    ax3.plot(angles, values, "o-", linewidth=1.5, label=query, markersize=4)
    ax3.fill(angles, values, alpha=0.08)

ax3.set_xticks(angles[:-1])
ax3.set_xticklabels(categories, fontsize=8)
ax3.set_ylim(0, 5.5)
ax3.set_title("Per-Query Radar", fontsize=13, fontweight="bold", pad=20)
ax3.legend(loc="upper right", bbox_to_anchor=(1.35, 1.15), fontsize=7)

# ── Panel 4: Per-Query Scores Grouped Bar Chart ──
ax4 = fig.add_subplot(gs[1, :2])
x = np.arange(len(queries))
width = 0.15
ax4.bar(x - 2 * width, groundedness_scores, width, label="Groundedness", color=colors["groundedness"])
ax4.bar(x - width, coherence_scores, width, label="Coherence", color=colors["coherence"])
ax4.bar(x, fluency_scores, width, label="Fluency", color=colors["fluency"])
ax4.bar(x + width, relevance_scores, width, label="Relevance", color=colors["relevance"])
ax4.bar(x + 2 * width, [s * 5 for s in f1_scores], width, label="F1 (×5)", color=colors["f1_score"])
ax4.set_xticks(x)
ax4.set_xticklabels(short_queries, fontsize=8, rotation=15, ha="right")
ax4.set_ylabel("Score", fontsize=11)
ax4.set_ylim(0, 6)
ax4.set_title("Per-Query Metric Breakdown", fontsize=13, fontweight="bold", pad=10)
ax4.legend(fontsize=8, ncol=5, loc="upper center")
ax4.axhline(y=3, color="gray", linestyle="--", linewidth=0.8, alpha=0.6)

# ── Panel 5: Pass/Fail Heatmap ──
ax5 = fig.add_subplot(gs[1, 2])
result_matrix = []
for r in rows:
    row_results = [
        1 if r["outputs.groundedness.groundedness_result"] == "pass" else 0,
        1 if r["outputs.coherence.coherence_result"] == "pass" else 0,
        1 if r["outputs.fluency.fluency_result"] == "pass" else 0,
        1 if r["outputs.relevance.relevance_result"] == "pass" else 0,
        1 if r["outputs.f1_score.f1_result"] == "pass" else 0,
    ]
    result_matrix.append(row_results)

result_array = np.array(result_matrix)
cmap = plt.cm.colors.ListedColormap(["#e74c3c", "#2ecc71"])
im = ax5.imshow(result_array, cmap=cmap, aspect="auto", vmin=0, vmax=1)
ax5.set_xticks(range(5))
ax5.set_xticklabels(["Ground.", "Coher.", "Fluency", "Relev.", "F1"], fontsize=8, rotation=30)
ax5.set_yticks(range(len(queries)))
ax5.set_yticklabels([f"Q{i+1}" for i in range(len(queries))], fontsize=9)
ax5.set_title("Pass/Fail Heatmap", fontsize=13, fontweight="bold", pad=10)
for i in range(result_array.shape[0]):
    for j in range(result_array.shape[1]):
        label = "Pass" if result_array[i, j] == 1 else "Fail"
        ax5.text(j, i, label, ha="center", va="center", fontsize=8,
                 color="white", fontweight="bold")

# ── Panel 6: Token Usage per Metric ──
ax6 = fig.add_subplot(gs[2, 0])
metric_names = ["Groundedness", "Coherence", "Fluency", "Relevance"]
total_tokens = []
for metric_key in ["groundedness", "coherence", "fluency", "relevance"]:
    tokens = sum(r[f"outputs.{metric_key}.{metric_key}_total_tokens"] for r in rows)
    total_tokens.append(tokens)
wedges, texts, autotexts = ax6.pie(
    total_tokens, labels=metric_names, autopct="%1.1f%%",
    colors=[colors["groundedness"], colors["coherence"], colors["fluency"], colors["relevance"]],
    startangle=90, textprops={"fontsize": 9}
)
for t in autotexts:
    t.set_fontweight("bold")
ax6.set_title(f"Token Usage by Metric\n(Total: {sum(total_tokens):,} tokens)", fontsize=13, fontweight="bold", pad=10)

# ── Panel 7: F1 Score Detail ──
ax7 = fig.add_subplot(gs[2, 1])
f1_colors_bar = ["#2ecc71" if s >= 0.5 else "#e74c3c" for s in f1_scores]
bars7 = ax7.bar(short_queries, f1_scores, color=f1_colors_bar, edgecolor="white")
for bar, val in zip(bars7, f1_scores):
    ax7.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, f"{val:.3f}",
             ha="center", va="bottom", fontsize=9, fontweight="bold")
ax7.axhline(y=0.5, color="gray", linestyle="--", linewidth=1)
ax7.text(len(queries) - 0.5, 0.51, "threshold=0.5", fontsize=8, color="gray", ha="right")
ax7.set_ylim(0, 0.75)
ax7.set_ylabel("F1 Score", fontsize=11)
ax7.set_title("F1 Score per Query (vs Ground Truth)", fontsize=13, fontweight="bold", pad=10)
ax7.tick_params(axis="x", rotation=20, labelsize=7)

# ── Panel 8: Groundedness Deep Dive ──
ax8 = fig.add_subplot(gs[2, 2])
g_colors = ["#2ecc71" if s >= 3 else "#e74c3c" for s in groundedness_scores]
bars8 = ax8.barh([f"Q{i+1}" for i in range(len(queries))], groundedness_scores, color=g_colors, edgecolor="white")
for bar, val in zip(bars8, groundedness_scores):
    ax8.text(val + 0.05, bar.get_y() + bar.get_height() / 2, f"{val:.1f}",
             ha="left", va="center", fontsize=10, fontweight="bold")
ax8.axvline(x=3, color="gray", linestyle="--", linewidth=1)
ax8.set_xlim(0, 5.5)
ax8.set_xlabel("Score", fontsize=11)
ax8.set_title("Groundedness per Query", fontsize=13, fontweight="bold", pad=10)

# Save and show
output_path = os.path.join(os.path.dirname(__file__), "..", "output_files", "eval_dashboard.png")
plt.savefig(output_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print(f"Dashboard saved to: {output_path}")
plt.show()
