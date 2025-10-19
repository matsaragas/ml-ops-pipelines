import json
from pathlib import Path


def score_risk(metrics: dict) -> float:
    acc = metrics.get('accuracy', 0)
    if acc >= 0.95:
        return 0.05
    if acc >= 0.9:
        return 0.15
    if acc >= 0.8:
        return 0.35

    return 0.7


metrics = json.loads(Path('evaluation_results.json').read_text())
risk = score_risk(metrics)
report = f"""
# Model Evaluation Report


**Accuracy:** {metrics['accuracy']:.3f}
**Precision:** {metrics['precision']:.3f}
**Recall:** {metrics['recall']:.3f}


**Risk Score:** {risk:.3f}


---


Recommended action: {'Promote to staging' if risk < 0.3 else 'Needs review'}
"""
Path('report.md').write_text(report)
print('Report written to report.md')