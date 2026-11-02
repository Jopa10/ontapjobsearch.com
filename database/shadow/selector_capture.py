"""Read-only observer for existing selectors; never evaluates selection policy.

Executed continue statements identify actual rejection gates. Production CSV
reports take precedence. Unobserved records stay unknown, never inferred excluded.
"""
import ast
import sys
from pathlib import Path

MODULES = {
    'customer_sales_pipeline': 'customer_sales',
    'finance_accounts_pipeline': 'finance_accounts',
    'marketing_pipeline': 'marketing',
    'hr_recruitment_pipeline': 'hr_recruitment',
    'legal_assistant_pipeline': 'legal_assistant_paralegal',
    'registered_category_pipeline': 'customer_service_contact_centre',
    'customer_sales_production_refine': 'customer_sales',
}


class Capture:
    def __init__(self, scripts):
        self.sites = {}
        self.records = {}
        for name, family in MODULES.items():
            path = (Path(scripts) / (name + '.py')).resolve()
            source = path.read_text()
            tree = ast.parse(source)
            parents = {child: node for node in ast.walk(tree) for child in ast.iter_child_nodes(node)}
            gates = {}
            for node in ast.walk(tree):
                if not isinstance(node, ast.Continue):
                    continue
                ancestor = parents.get(node)
                in_feed = False
                while ancestor:
                    if isinstance(ancestor, ast.For) and isinstance(ancestor.iter, ast.Call) and isinstance(ancestor.iter.func, ast.Attribute) and ancestor.iter.func.attr == 'iterrows':
                        in_feed = True
                    ancestor = parents.get(ancestor)
                if not in_feed:
                    continue
                parent = parents.get(node)
                while parent and not isinstance(parent, (ast.If, ast.For)):
                    parent = parents.get(parent)
                if isinstance(parent, ast.If):
                    gates[node.lineno] = ast.get_source_segment(source, parent.test)
            self.sites[str(path)] = (family, gates)

    def trace(self, frame, event, arg):
        spec = self.sites.get(frame.f_code.co_filename)
        if spec is None or frame.f_code.co_name not in {'main', 'run_live_registered_categories', 'keep_job'}:
            return None
        if event == 'return':
            local = frame.f_locals
            if frame.f_code.co_name == 'keep_job' and isinstance(arg, tuple) and not arg[0]:
                ref = str(local['job'].get('job_id', ''))
                self.records[(spec[0], ref)] = {'decision': 'exclude', 'reason': str(arg[1]), 'gate': 'production Customer Sales QA'}
            elif frame.f_code.co_name == 'main':
                candidates = local.get('candidates', local.get('outputs', {}))
                for jobs in candidates.values():
                    for job in jobs:
                        ref = str(job.get('job_id', ''))
                        if ref:
                            self.records.setdefault((spec[0], ref), {'decision': 'exclude', 'reason': 'Eligible production candidate withheld by final output/campaign gate', 'gate': 'production candidate; final output gate'})
        if event == 'line' and frame.f_lineno in spec[1]:
            local = frame.f_locals
            raw = local.get('row')
            # Only the raw-feed loop; later campaign loops have a job dictionary.
            if raw is not None and hasattr(raw, 'get'):
                ref = str(raw.get('/Job/DisplayReference', '')).strip()
                if ref:
                    gate = spec[1][frame.f_lineno]
                    detail = ''
                    if gate == 'not keep':
                        detail = str(local.get('reason') or '')
                    elif gate == 'conflict':
                        detail = str(local.get('conflict') or '')
                    self.records[(spec[0], ref)] = {
                        'decision': 'exclude',
                        'reason': detail or 'Production gate: ' + gate,
                        'gate': gate,
                    }
        return self.trace

    def __enter__(self):
        if sys.gettrace() is not None:
            raise RuntimeError('A trace observer is already installed')
        sys.settrace(self.trace)
        return self

    def __exit__(self, *args):
        sys.settrace(None)
