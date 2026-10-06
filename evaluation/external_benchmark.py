"""External BANKING77 duplicate-charge slice; never a full support accuracy claim."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
from app.core import Copilot

SOURCE = 'https://github.com/PolyAI-LDN/task-specific-datasets'
INTENT = 'transaction_charged_twice'

def wilson(hits, n):
    z=1.96; p=hits/n; den=1+z*z/n
    center=(p+z*z/(2*n))/den
    half=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return [round(center-half,4),round(center+half,4)]

def run(path):
    rows=list(csv.DictReader(path.open()))
    subset=[(i,r) for i,r in enumerate(rows) if r['category']==INTENT]
    if len(rows)!=3080 or len(subset)!=40:
        raise ValueError('Expected original BANKING77 test split: 3080 rows / 40 duplicate-charge queries')
    c=Copilot(); outputs=[]
    for i,row in subset:
        pred=c.analyze(row['text'])
        outputs.append({'test_row_index':i,'category_correct':pred['category']=='billing',
            'retrieval_hit_at_3':'billing' in [s['id'] for s in pred['sources']],
            'escalated':pred['escalate'],'predicted_category':pred['category'],
            'top_source':pred['sources'][0]['id'] if pred['sources'] else None,
            'retrieval_score':pred['retrieval_score']})
    report={'source':SOURCE,'source_file':'banking_data/test.csv','source_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
        'selection_rule':'ALL test queries with existing category transaction_charged_twice; selected before scoring',
        'mapping':'transaction_charged_twice -> billing runbook; escalation expected by our policy, not original dataset labels',
        'scope':'External single-intent retrieval/triage transfer check. NOT overall real-world accuracy or answer-correctness evaluation.',
        'n':len(outputs),'mode':'retrieval','model_or_threshold_tuned_on_this_data':False,'metrics':{},'rows':outputs}
    for key in ['category_correct','retrieval_hit_at_3','escalated']:
        hits=sum(x[key] for x in outputs)
        report['metrics'][key]={'hits':hits,'n':len(outputs),'rate':hits/len(outputs),'wilson_95_interval':wilson(hits,len(outputs))}
    return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('csv_path',type=Path);a=p.parse_args()
    report=run(a.csv_path)
    Path(__file__).with_name('external_report.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='rows'},indent=2))
