import importlib.util
from pathlib import Path
import unittest
s=importlib.util.spec_from_file_location('plan',Path(__file__).parents[1]/'scripts/plan_shadow_jobg8_import.py')
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
def plan(day, values):
 return m.build_plan([{'/Job/DisplayReference':k,'/Job/Position':v,'/Job/ApplicationURL':'https://example.org/'+k} for k,v in values],day)
class TurnoverTests(unittest.TestCase):
 def test_update_gap_return_and_unknown_history(self):
  a=plan('2026-11-02',[('1','Admin'),('2','Office')]);b=plan('2026-11-03',[('1','New title'),('3','Admin')])
  c=m.compare_plans(a,b)
  self.assertEqual((c['overlap'],c['changed'],c['added_vs_previous'],c['absent_vs_previous']),(1,1,1,1))
  self.assertIsNone(c['returned_from_earlier_history'])
  self.assertEqual(m.compare_plans(a,b,{'3'})['returned_from_earlier_history'],1)
 def test_unchanged_and_invalid_date(self):
  a=plan('2026-11-02',[('1','Admin')]);b=plan('2026-11-03',[('1','Admin')])
  self.assertEqual(m.compare_plans(a,b)['unchanged'],1)
  with self.assertRaises(ValueError):m.compare_plans(a,a)
 def test_duplicate_quarantine_keeps_clean_remainder(self):
  def row(ref,title):return {'/Job/DisplayReference':ref,'/Job/Position':title,'/Job/ApplicationURL':'https://example.org/'+ref}
  clean,d=m.quarantine_rows([row('1','Admin'),row('1','Admin'),row('2','Office'),row('2','Changed'),row('3','Admin')])
  self.assertEqual([x['/Job/DisplayReference'] for x in clean],['1','3'])
  self.assertEqual(d['exact_repeat_rows'],1)
  self.assertEqual(d['conflicting_ids_held'],['2'])
  with self.assertRaises(ValueError):m.quarantine_rows([row(str(i),v) for i in range(16) for v in ['A','B']])
 def test_budget_fails_closed_and_counts_nine_scopes(self):
  baseline={'database':{'bytes':'750000000'},'maximumDatabaseBytes':838860800,'adverts':{'rows':'100'},'tables':[{'name':k,'total_bytes':v} for k,v in [('jobs',10000),('supplier_adverts',100000),('advert_appearances',10000),('selection_decisions',80000)]],'decisions':[{'scope':'production:admin','rows':'800'}]}
  c={'current_count':10000,'added_vs_previous':1000,'changed':100}
  r=m.project_storage(c,baseline)
  self.assertEqual(r['components_before_headroom']['nine_scoped_decision_bytes'],9000000)
  baseline['database']['bytes']='830000000'
  self.assertFalse(m.project_storage(c,baseline)['estimate_fits'])
  self.assertFalse(r['import_authorized'])
  with self.assertRaises(ValueError):m.project_storage(c,baseline,safety_factor=1)
if __name__=='__main__':unittest.main()
