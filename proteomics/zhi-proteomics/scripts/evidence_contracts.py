#!/usr/bin/env python3
"""Small deterministic evidence checks; not a statistical inference engine."""
import argparse
import hashlib
import json
import math
import re

AA = dict(zip('ARNDCEQGHILKMFPSTWYV', [71.037113805,156.10111105,114.04292747,115.026943065,103.009184505,129.042593135,128.05857754,57.021463735,137.058911875,113.084063975,113.084063975,128.094963015,131.040484645,147.068413945,97.052763875,87.032028435,101.047678505,186.07931298,163.063328575,99.068413945]))
MODS={'1':42.010565,'4':57.021464,'35':15.994915,'21':79.966331,'121':114.042927}
MISSING={'','na','n/a','nan','null','none','unknown','未知','不知道','不清楚'}

def missing(value):
    return value is None or isinstance(value,float) and not math.isfinite(value) or isinstance(value,str) and value.strip().lower() in MISSING

def cache_fingerprint(manifest):
    required={'software_build','fasta_sha256','library_sha256','raw_sha256','search_parameters'}
    if not required <= set(manifest) or any(missing(manifest[x]) for x in required):
        raise ValueError('Fingerprint needs software build, FASTA/library/raw hashes and exact search parameters')
    return hashlib.sha256(json.dumps(manifest,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def precursor_mz(modified_sequence, charge):
    if not isinstance(charge,int) or isinstance(charge,bool) or charge<1:raise ValueError('Positive integer charge required')
    ids=re.findall(r'\(UniMod:(\d+)\)',modified_sequence)
    stripped=re.sub(r'\(UniMod:\d+\)','',modified_sequence)
    if not stripped or any(a not in AA for a in stripped):raise ValueError('Unsupported sequence syntax/residue; do not guess masses')
    if any(x not in MODS for x in ids):raise ValueError('Unsupported modification; use an explicitly versioned mass dictionary')
    return (sum(AA[a] for a in stripped)+18.010564684+sum(MODS[x] for x in ids))/charge+1.007276467

def compare_cysteine_mass(sequence, charge, observed_mz):
    expected=precursor_mz(sequence,charge)
    stripped=re.sub(r'\(UniMod:\d+\)','',sequence)
    unmarked_c=len(re.findall(r'C(?!\(UniMod:4\))',sequence))
    hypothetical=expected+unmarked_c*MODS['4']/charge
    return {'cysteines':stripped.count('C'),'explicit_mods_mz':expected,
            'absolute_error_Th':abs(float(observed_mz)-expected),
            'hypothetical_fixed_C_mz':hypothetical,'hypothetical_error_Th':abs(float(observed_mz)-hypothetical),
            'interpretation':'Search-mass diagnostic only; cannot establish actual wet-lab alkylation.'}

def site_id(accession, residue, position, modification, fasta_sha256):
    if not accession or not fasta_sha256 or residue not in AA or not isinstance(position,int) or isinstance(position,bool) or position<1:raise ValueError('Unambiguous accession, residue, position and FASTA hash required')
    if not re.fullmatch(r'UniMod:\d+',modification):raise ValueError('Explicit UniMod identifier required')
    return '|'.join(map(str,[fasta_sha256,accession,residue,position,modification]))

def precursor_id(peptidoform, charge):
    precursor_mz(peptidoform,charge)  # rejects unsupported syntax rather than merging it
    return f'{peptidoform}|z={charge}'

def common_changes(primary, recurrent, fold_change, majority_fraction):
    if len(primary)!=len(recurrent) or not primary:raise ValueError('Equal nonempty paired arrays required')
    if fold_change<=1 or not 0<majority_fraction<=1:raise ValueError('Invalid common-change thresholds')
    deltas=[]
    for a,b in zip(primary,recurrent):
        deltas.append(None if missing(a) or missing(b) or float(a)<=0 or float(b)<=0 else math.log2(float(b)/float(a)))
    threshold=math.log2(fold_change);up=sum(d is not None and d>=threshold for d in deltas);down=sum(d is not None and d<=-threshold for d in deltas)
    n=len(deltas);observed=sum(d is not None for d in deltas)
    return {'deltas':deltas,'cohort_pairs':n,'complete_pairs':observed,'up':up,'down':down,
            'support_fraction_all':max(up,down)/n,'support_fraction_observed':max(up,down)/observed if observed else None,
            'strict_all':up==n or down==n,'majority':max(up,down)>=math.ceil(majority_fraction*n),
            'endpoint':'descriptive_common_change_NOT_individual_significance'}

def contaminant_class(group, tag='CONTAMINANT_'):
    members=[x.strip() for x in str(group).split(';') if x.strip()]
    if not members:return 'unknown'
    tagged=[x.startswith(tag) for x in members]
    return 'all_contaminant' if all(tagged) else 'mixed_review' if any(tagged) else 'noncontaminant'

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--sequence',required=True);p.add_argument('--charge',required=True,type=int);p.add_argument('--mz',type=float,required=True)
    a=p.parse_args();print(json.dumps(compare_cysteine_mass(a.sequence,a.charge,a.mz),indent=2));return 0
if __name__=='__main__':raise SystemExit(main())
