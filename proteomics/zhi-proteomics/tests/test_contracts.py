"""Synthetic, patient-free regression tests for evidence and question behavior."""
import importlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from evidence_contracts import (cache_fingerprint,common_changes,compare_cysteine_mass,
    contaminant_class,missing,precursor_mz,precursor_id,site_id)
from intake_questions import select_questions,resolved
from inspect_diann_project import count_tsv,find_file,inspect_log

class IntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.bank=json.loads((ROOT/'configs/question_bank.json').read_text())
    def q(self,id):return next(q for q in self.bank if q['id']==id)
    def test_bank_unique_and_explanatory(self):
        self.assertEqual(len(self.bank),len({q['id'] for q in self.bank}))
        for q in self.bank:
            for k in ['zh','en','why','suggestion']:self.assertTrue(q[k])
    def test_beginner_gets_short_round_not_execution(self):
        r=select_questions(self.bank,{},'whole','analysis')
        self.assertEqual(len(r['next_questions']),4)
        self.assertFalse(r['execution_authorized'])
        self.assertIn('pairing',r['blocking_items'])
    def test_proposal_is_not_confirmation(self):
        self.assertFalse(resolved(self.q('differential_fdr'),{'value':.05,'status':'proposed','source':'suggestion'}))
    def test_confirmed_threshold(self):
        self.assertTrue(resolved(self.q('differential_fdr'),{'value':.05,'status':'user_confirmed','source':'user'}))
        self.assertFalse(resolved(self.q('differential_fdr'),{'value':5,'status':'user_confirmed','source':'user'}))
    def test_unknown_not_repeated_or_filled(self):
        s={'answers':{'alkylation':{'value':None,'status':'unknown','asked':True,'source':'user does not know'}}}
        r=select_questions(self.bank,s,'whole','analysis',100)
        self.assertIn('alkylation',r['unresolved_items'])
        self.assertNotIn('alkylation',[q['id'] for q in r['next_questions']])
        self.assertIsNone(s['answers']['alkylation']['value'])
    def test_explicit_no_alkylation_is_a_fact(self):
        self.assertTrue(resolved(self.q('alkylation'),{'value':False,'status':'user_confirmed','source':'SOP confirmation'}))
    def test_source_required(self):
        self.assertFalse(resolved(self.q('alkylation'),{'value':'CAA','status':'documented'}))
    def test_ptm_routing(self):
        a=select_questions(self.bank,{},'whole','analysis',100)
        b=select_questions(self.bank,{},'phospho','analysis',100)
        self.assertNotIn('localization',a['unresolved_items']);self.assertIn('localization',b['unresolved_items'])
    def test_pilot_does_not_override_identity(self):
        r=select_questions(self.bank,{'pilot_authorized':True},'whole','analysis')
        self.assertNotIn('alkylation',r['blocking_items']);self.assertIn('groups',r['blocking_items'])
    def test_conflict_overrides_pilot_and_prior_asked(self):
        r=select_questions(self.bank,{'pilot_authorized':True,'answers':{'alkylation':{'value':'CAA vs absent','status':'conflicting','asked':True,'source':'SOP/log'}}},'whole','analysis')
        self.assertIn('alkylation',r['blocking_items']);self.assertEqual(r['next_questions'][0]['id'],'alkylation')
    def test_hold_instruction_is_not_execution_approval(self):
        self.assertFalse(resolved(self.q('plan_approval'),{'value':'do not run','status':'user_confirmed','source':'user'}))
    def test_pilot_boolean_not_string(self):
        with self.assertRaises(ValueError):select_questions(self.bank,{'pilot_authorized':'false'},'whole','analysis')
    def test_audit_asks_chemistry_not_statistical_thresholds(self):
        r=select_questions(self.bank,{},'whole','audit',100)
        self.assertIn('alkylation',r['unresolved_items']);self.assertNotIn('differential_fdr',r['unresolved_items'])

class EvidenceTests(unittest.TestCase):
    def test_missing_markers_and_zero(self):
        for v in [None,float('nan'),'NA',' N/A ','unknown','不知道']:self.assertTrue(missing(v))
        self.assertFalse(missing(0));self.assertFalse(missing(False))
    def test_swap_contrast(self):
        x=common_changes([10,20],[20,10],1.5,.8);y=common_changes([20,10],[10,20],1.5,.8)
        self.assertEqual(x['deltas'],[-v for v in y['deltas']])
    def test_missing_is_not_support(self):
        r=common_changes([10,10,None,None],[20,20,None,None],1.5,.8)
        self.assertFalse(r['majority']);self.assertEqual(r['support_fraction_all'],.5);self.assertEqual(r['support_fraction_observed'],1)
    def test_zero_not_infinite_fc(self):
        self.assertIsNone(common_changes([0],[100],2,1)['deltas'][0])
    def test_all_missing_and_zero_discoveries(self):
        r=common_changes([None,None],[None,None],1.5,.8)
        self.assertFalse(r['strict_all']);self.assertIsNone(r['support_fraction_observed'])
        self.assertFalse(common_changes([10]*5,[10]*5,1.5,.8)['majority'])
    def test_carbamidomethyl_mass(self):
        a=precursor_mz('ACDEK',2);b=precursor_mz('AC(UniMod:4)DEK',2)
        self.assertAlmostEqual(b-a,57.021464/2,places=7)
        r=compare_cysteine_mass('ACDEK',2,b)
        self.assertAlmostEqual(r['hypothetical_error_Th'],0,places=7)
    def test_already_explicit_c_not_doubled(self):
        mz=precursor_mz('AC(UniMod:4)DEK',2)
        self.assertEqual(compare_cysteine_mass('AC(UniMod:4)DEK',2,mz)['hypothetical_error_Th'],0)
    def test_unsupported_mod_fails(self):
        with self.assertRaises(ValueError):precursor_mz('AC(UniMod:99999)DEK',2)
    def test_site_independent_of_precursor_charge(self):
        site=site_id('P_SYNTH','S',10,'UniMod:21','db-v1')
        evidence=[(site,precursor_id('AS(UniMod:21)K',z)) for z in [2,3]]
        self.assertEqual(len({x[0] for x in evidence}),1);self.assertEqual(len({x[1] for x in evidence}),2)
        self.assertNotEqual(site,site_id('P_SYNTH','S',10,'UniMod:21','db-v2'))
    def test_cache_invalidation(self):
        a=dict(software_build='2.6.1-build',fasta_sha256='f',library_sha256='l',raw_sha256=['r'],search_parameters={'scoring':'Generic'})
        b={**a,'search_parameters':{'scoring':'Peptidoforms'}}
        self.assertNotEqual(cache_fingerprint(a),cache_fingerprint(b))
        self.assertNotEqual(cache_fingerprint(a),cache_fingerprint({**a,'raw_sha256':['other']}))
        with self.assertRaises(ValueError):cache_fingerprint({})
    def test_contaminant_member_order(self):
        self.assertEqual(contaminant_class('P_SYNTH;CONTAMINANT_X'),'mixed_review')
        self.assertEqual(contaminant_class('CONTAMINANT_X;P_SYNTH'),'mixed_review')

class FileTests(unittest.TestCase):
    def test_named_matrix_columns(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'report.pg_matrix.tsv';p.write_text('Genes\tProtein.Group\trun1\nG\tCONTAMINANT_X\t5\n')
            r=count_tsv(p,'CONTAMINANT_');self.assertEqual(r['sample_headers'],['run1']);self.assertEqual(r['leading_contaminant_rows'],1)
    def test_ambiguous_outputs_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            for sub in ['a','b']:
                p=Path(d)/sub;p.mkdir();(p/'report.parquet').touch()
            with self.assertRaises(ValueError):find_file(Path(d),'report.parquet')
    def test_log_not_chemistry_proof(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'report.log.txt';p.write_text('DIA-NN 2.6.1\ndiann.exe --fasta-search --predictor --dir raw --use-quant\n')
            r=inspect_log(p);self.assertEqual(r['chemistry_status'],'unknown_until_SOP_or_user_confirmation')
            self.assertIn('combined_prediction_search',[x['code'] for x in r['findings']])
    def validate(self,body,*extra):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'metadata.csv';p.write_text(body)
            run=subprocess.run([sys.executable,str(ROOT/'scripts/validate_paired_design.py'),str(p),'--sample','sample','--subject','subject','--condition','condition',*extra],capture_output=True,text=True)
            return run.returncode,json.loads(run.stdout)
    def test_unknown_subject_invalid(self):
        code,r=self.validate('sample,subject,condition\na,NA,A\nb,NA,B\n')
        self.assertNotEqual(code,0);self.assertFalse(r['valid'])
    def test_technical_repeat_not_new_patient(self):
        code,r=self.validate('sample,subject,condition,bio,run\na,S,A,BA,r1\na,S,A,BA,r2\nb,S,B,BB,r3\n','--biosample','bio','--run','run')
        self.assertEqual(code,0);self.assertEqual(r['subjects'],1);self.assertEqual(r['biological_specimen_rows'],2);self.assertEqual(len(r['technical_repeats']),1)
    def test_technical_repeat_conflicting_identity(self):
        code,r=self.validate('sample,subject,condition,bio,run\na,S,A,BA,r1\na,T,A,BA,r2\nb,S,B,BB,r3\n','--biosample','bio','--run','run')
        self.assertNotEqual(code,0)
    def test_batch_confounding(self):
        code,r=self.validate('sample,subject,condition,batch\na,S,A,x\nb,S,B,y\n','--batch','batch')
        self.assertNotEqual(code,0);self.assertTrue(r['fully_confounded'])
    def test_empty_metadata_is_not_valid_design(self):
        code,r=self.validate('sample,subject,condition\n')
        self.assertNotEqual(code,0)
    def test_single_condition_not_a_pair(self):
        code,r=self.validate('sample,subject,condition\na,S,A\n')
        self.assertNotEqual(code,0)

if __name__=='__main__':unittest.main()
