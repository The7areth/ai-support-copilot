import argparse
import hashlib
import json
from pathlib import Path
from app.core import Copilot

def run():
    path=Path(__file__).with_name("dataset.json")
    rows=json.loads(path.read_text()); c=Copilot(); predictions=[]
    for row in rows:
        result=c.analyze(row["text"])
        predictions.append({**row,"predicted_category":result["category"],"predicted_escalate":result["escalate"],
            "retrieved":[s["id"] for s in result["sources"]]})
    known=[p for p in predictions if p["source"]]
    positives=[p for p in predictions if p["escalate"]]
    report={"dataset":"Hand-authored synthetic regression set; not an independent holdout", "mode":"retrieval", "n":len(rows),
        "dataset_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
        "category_accuracy":sum(p["category"]==p["predicted_category"] for p in predictions)/len(rows),
        "retrieval_recall_at_3":sum(p["source"] in p["retrieved"] for p in known)/len(known),
        "escalation_accuracy":sum(p["escalate"]==p["predicted_escalate"] for p in predictions)/len(rows),
        "escalation_recall":sum(p["predicted_escalate"] for p in positives)/len(positives),
        "failures":[p for p in predictions if p["category"]!=p["predicted_category"] or p["escalate"]!=p["predicted_escalate"]]}
    return report
if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--check",action="store_true");args=parser.parse_args()
    report=run();Path(__file__).with_name("report.json").write_text(json.dumps(report,indent=2)+"\n")
    print(json.dumps(report,indent=2))
    if args.check and (report["category_accuracy"]<0.8 or report["escalation_recall"]<0.9):
        raise SystemExit(1)
