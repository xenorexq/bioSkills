#!/usr/bin/env python3
"""Read-only staged question selector. No defaults become confirmations."""
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATES = {'unknown', 'documented', 'user_confirmed', 'proposed', 'conflicting', 'not_applicable'}

def resolved(question, answer):
    status = answer.get('status', 'unknown')
    if status not in STATES:
        raise ValueError(f'Invalid status for {question["id"]}: {status}')
    value = answer.get('value')
    if status == 'not_applicable':
        return bool(answer.get('source')) and (not question['required_for'] or question['id'] in {'clinical_context','purity','preservation'})
    if value is None or (isinstance(value, str) and value.strip().lower() in {'', 'unknown','na','n/a','null','不知道','不清楚','未知'}):
        return False
    if not answer.get('source'):
        return False
    if question['kind'] == 'choice' and status != 'user_confirmed':
        return False
    if status not in {'documented', 'user_confirmed'}:
        return False
    if question['id'] == 'differential_fdr':
        return isinstance(value, (int,float)) and not isinstance(value,bool) and 0 < value < 1
    if question['id'] == 'plan_approval':
        return value is True or value in ('execute','pilot','执行','开始执行')
    return True

def select_questions(bank, state, mode, stage, limit=4, include_optional=False):
    if not isinstance(state.get('pilot_authorized',False),bool):
        raise ValueError('pilot_authorized must be a JSON boolean, not a string')
    if mode not in {'whole','phospho','kgg','multi'} or stage not in {'audit','analysis','rerun'}:
        raise ValueError('Unknown mode or stage')
    answers = state.get('answers', {})
    relevant = [q for q in bank if 'all' in q['modes'] or mode in q['modes']]
    unresolved, blocking, pilot_items, queue = [], [], [], []
    for q in relevant:
        a = answers.get(q['id'], {})
        if resolved(q,a):
            continue
        required = stage in q['required_for'] or (stage == 'audit' and q['id'] in {
            'alkylation','digestion','ptm_goal','diann_version','fasta','search_modifications',
            'library_workflow','scoring_quantification','id_fdr','cache_warnings'})
        if not required and not include_optional:
            continue
        unresolved.append(q['id'])
        conflict = a.get('status') == 'conflicting'
        # Pilot consent permits only specifically pilot-eligible uncertainties.
        if required:
            if q['unknown_policy'] == 'pilot' and not conflict:
                pilot_items.append(q['id'])
                if not state.get('pilot_authorized',False):blocking.append(q['id'])
            else:blocking.append(q['id'])
        if not a.get('asked',False) or conflict:
            queue.append(q)
    queue.sort(key=lambda q:(answers.get(q['id'],{}).get('status')!='conflicting',q['round']))
    # Ask plan approval only after prior decisions have been considered/resolved or
    # explicitly marked unknown. Never conceal earlier unresolved decisions.
    candidates=[q for q in queue if q['id']!='plan_approval']
    if not candidates:candidates=queue
    return {'mode':mode,'stage':stage,'next_questions':candidates[:limit],
            'unresolved_items':unresolved,'blocking_items':blocking,'pilot_only_items':pilot_items,
            'required_items_resolved_or_pilot_accepted':not blocking,
            'execution_authorized':False,
            'notice':'This selector never authorizes execution. Review scope, plan approval, chemistry/design gates and actual tool permissions separately.'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mode',choices=['whole','phospho','kgg','multi'],required=True)
    p.add_argument('--stage',choices=['audit','analysis','rerun'],default='analysis')
    p.add_argument('--state',type=Path)
    p.add_argument('--limit',type=int,default=4)
    p.add_argument('--include-optional',action='store_true')
    a=p.parse_args()
    if a.limit<1:p.error('--limit must be positive')
    bank=json.loads((ROOT/'configs/question_bank.json').read_text())
    state=json.loads(a.state.read_text()) if a.state else {}
    print(json.dumps(select_questions(bank,state,a.mode,a.stage,a.limit,a.include_optional),ensure_ascii=False,indent=2))
    return 0
if __name__=='__main__':raise SystemExit(main())
