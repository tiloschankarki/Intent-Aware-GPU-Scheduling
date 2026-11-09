"""Static organization checks only; does not import or execute research code."""
import ast
import csv
import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path
from urllib.parse import unquote

ROOT = Path(__file__).resolve().parents[1]


def read_json(relative):
    return json.loads((ROOT / relative).read_text(encoding='utf-8-sig'))


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def near(a, b, tol=1e-11):
    assert math.isclose(float(a), float(b), rel_tol=tol, abs_tol=tol), (a, b)


def rows(relative):
    with (ROOT / relative).open(newline='', encoding='utf-8-sig') as stream:
        return list(csv.DictReader(stream))


def verify_notebook(path):
    nb = json.loads(path.read_text())
    assert nb['nbformat'] == 4 and isinstance(nb['nbformat_minor'], int)
    assert isinstance(nb['metadata'], dict) and isinstance(nb['cells'], list)
    ids = []
    for cell in nb['cells']:
        assert cell['cell_type'] in {'code', 'markdown', 'raw'}
        assert isinstance(cell['metadata'], dict)
        assert isinstance(cell['source'], (str, list))
        if isinstance(cell['source'], list):
            assert all(isinstance(x, str) for x in cell['source'])
        if 'id' in cell:
            assert re.fullmatch(r'[A-Za-z0-9_-]{1,64}', cell['id'])
            ids.append(cell['id'])
        if cell['cell_type'] == 'code':
            count = cell['execution_count']
            assert count is None or isinstance(count, int)
            assert isinstance(cell['outputs'], list)
            for output in cell['outputs']:
                kind = output['output_type']
                assert kind in {'stream', 'display_data', 'execute_result', 'error'}
                if kind == 'stream':
                    assert output['name'] in {'stdout', 'stderr'}
                    assert isinstance(output['text'], (str, list))
                elif kind in {'display_data', 'execute_result'}:
                    assert isinstance(output['data'], dict)
                    assert isinstance(output['metadata'], dict)
                    if kind == 'execute_result':
                        assert output['execution_count'] is None or isinstance(output['execution_count'], int)
                else:
                    assert all(k in output for k in ['ename', 'evalue', 'traceback'])
    assert len(ids) == len(set(ids))
    return nb


def verify():
    manifest = read_json('docs/repository-files.json')
    for name, expected in manifest['files'].items():
        p = ROOT / name
        assert p.is_file() and digest(p) == expected, ('changed/missing file', name)
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*')
              if p.is_file() and '.git' not in p.relative_to(ROOT).parts}
    assert actual == set(manifest['files']) | set(manifest['excluded_metadata_files']), 'file set changed'
    print('PASS: deliverable hashes and file set:', len(manifest['files']))

    files = [ROOT / name for name in actual]
    py = [p for p in files if p.suffix == '.py']
    for p in py:
        ast.parse(p.read_bytes(), filename=str(p))
    for p in files:
        if p.suffix == '.json':
            json.loads(p.read_text(encoding='utf-8-sig'))
    notebooks = {str(p.relative_to(ROOT)): verify_notebook(p) for p in files if p.suffix == '.ipynb'}
    for exp, original, formatted in [
        (2, 'exp02_colab_execution_original.ipynb', 'exp02_colab_execution.ipynb'),
        (2, 'exp02_colab_diagnostics_original.ipynb', 'exp02_colab_diagnostics.ipynb'),
        (3, 'exp03_colab_cpu_original.ipynb', 'exp03_colab_cpu.ipynb'),
    ]:
        prefix = f'experiments/experiment-{exp}/notebooks/'
        a, b = notebooks[prefix + original], notebooks[prefix + formatted]
        assert {k: v for k, v in a.items() if k != 'cells'} == {k: v for k, v in b.items() if k != 'cells'}
        assert [c for c in a['cells'] if c['cell_type'] == 'code'] == [c for c in b['cells'] if c['cell_type'] == 'code']
        index = 0
        for cell in b['cells']:
            if index < len(a['cells']) and cell == a['cells'][index]:
                index += 1
            else:
                assert cell['cell_type'] == 'markdown'
        assert index == len(a['cells'])
    print('PASS: Python syntax:', len(py), '; notebook structure/preservation:', len(notebooks))

    links = 0
    for name in manifest['authored_markdown']:
        p = ROOT / name
        text = re.sub(r'```.*?```', '', p.read_text(), flags=re.S)
        for target in re.findall(r'\[[^\]]*\]\(([^\)]+)\)', text):
            target = target.strip('<>').split('#', 1)[0]
            if not target or re.match(r'[a-zA-Z][a-zA-Z0-9+.-]*:', target):
                continue
            assert (p.parent / unquote(target)).exists(), ('broken authored link', name, target)
            links += 1
    print('PASS: authored local Markdown links:', links)

    summary = read_json('experiments/experiment-1/archived-source/resume_reports/results-summary.json')
    e1 = rows('experiments/experiment-1/exp1_historical_report_values.csv')
    weak = []
    for row in e1:
        for comparison, column in [('R+P', 'resource_priority_gain_percent'), ('R+P+A', 'strong_control_gain_percent')]:
            rec = next(x for x in summary if x['population'] == 'broad' and x['comparison'] == comparison and x['seed'] == int(row['model_seed']))
            near(row[column], rec['relative_gain_percent'], tol=1e-6)
            near(rec['relative_gain_percent'], 100 * (rec['m0_logmae'] - rec['m1_logmae']) / rec['m0_logmae'])
            assert rec['test_rows'] == 711321
            if comparison == 'R+P':
                weak.append(rec['relative_gain_percent'])
            else:
                near(row['strong_ci_low'], rec['relative_ci95'][0])
                near(row['strong_ci_high'], rec['relative_ci95'][1])
                assert rec['relative_ci95'][0] < 0 < rec['relative_ci95'][1]
    assert round(sum(weak) / len(weak), 2) == 5.88
    print('PASS: Experiment 1 saved test gains, intervals and broad test count')

    e2 = rows('experiments/experiment-2/exp2_reported_validation_values.csv')
    assert [int(x['partition_seed']) for x in e2] == [20260927, 20261020]
    for row in e2:
        report = (ROOT / 'experiments/experiment-2/exp2_phase1_findings_original.md').read_text()
        assert f"{abs(float(row['execution_gain_percent'])):.6f}" in report
        assert f"{abs(float(row['equal_workload_gain_percent'])):.6f}" in report
    chosen = []
    for role in ['m0', 'm1']:
        s = read_json(f'experiments/experiment-2/results/cloud-results/run_colab_02/{role}/selection.json')
        assert len(s['records']) == 12 and not s['test_used_for_selection']
        best = min(s['records'], key=lambda x: (x['validation_log_mae'], x['candidate_id']))
        assert s['selected']['candidate_id'] == best['candidate_id']
        chosen.append(best['validation_log_mae'])
    near(100 * (chosen[0] - chosen[1]) / chosen[0], e2[1]['execution_gain_percent'], tol=1e-6)
    print('PASS: Experiment 2 validation signs and recovered second-partition selection')

    prefix = 'experiments/experiment-3/'
    spec = read_json(prefix + 'exp3_preregistration_original.json')['spec']
    report = read_json(prefix + 'exp3_report_original.json')
    population = read_json(prefix + 'archived-source/population_audit.json')
    assert population == spec['population']
    assert population['original_executions'] == 4709624
    assert population['original_workloads'] == 473265
    assert population['original_executions'] - population['excluded_union_executions'] == population['eligible_executions'] == 3372430
    assert population['original_workloads'] - population['excluded_union_workloads'] == population['eligible_workloads'] == 341617
    assert sum(population['historical_test_workloads']) - population['overlap_workloads'] == population['excluded_union_workloads']
    for key, name in [('runner_sha256', 'exp3_runner.py'), ('reference_sha256', 'frozen_reference.py'), ('protocol_sha256', 'original_protocol.json')]:
        assert digest(ROOT / prefix / 'archived-source' / name) == spec[key]
    package = read_json(prefix + 'archived-source/PACKAGE_MANIFEST.json')
    for name, expected in package.items():
        if name == 'inputs/eligible.parquet':
            assert not (ROOT / prefix / 'archived-source' / name).exists()
        else:
            assert digest(ROOT / prefix / 'archived-source' / name) == expected
    candidates = report['candidate_outcomes']
    assert len(candidates) == 240 and len(spec['split_seeds']) == 10
    assert report['all_ten_complete'] and report['seed_status_counts'] == {'complete': 10}
    assert report['confirmatory_tests'] == 'untouched and unevaluated'
    selected = rows(prefix + 'exp3_selected_validation.csv')
    assert len(selected) == 10 and len(rows(prefix + 'exp3_candidate_records.csv')) == 240
    csv_by_seed = {int(x['split_seed']): x for x in selected}
    wins = Counter()
    for outcome in report['seed_outcomes']:
        seed = outcome['split_seed']
        assert seed in spec['split_seeds'] and outcome['status'] == 'complete'
        stored = csv_by_seed[seed]
        for key, value in outcome.items():
            if isinstance(value, (float, int)):
                near(stored[key], value)
            else:
                assert stored[key] == value
        for role in ['m0', 'm1']:
            cs = [c for c in candidates if c['split_seed'] == seed and c['role'] == role]
            assert sorted(c['candidate_id'] for c in cs) == list(range(1, 13))
            best = min(cs, key=lambda c: (c['validation_log_mae'], c['candidate_id']))
            assert best['candidate_id'] == outcome[role + '_candidate_id']
            for metric in ['execution', 'equal_workload']:
                near(best['validation_metrics'][metric + '_logmae'], outcome[role + '_' + metric + '_logmae'])
        for metric in ['execution', 'equal_workload']:
            m0, m1 = outcome['m0_' + metric + '_logmae'], outcome['m1_' + metric + '_logmae']
            near(m0 - m1, outcome[metric + '_logmae_m0_minus_m1'])
            near(100 * (m0 - m1) / m0, outcome[metric + '_logmae_relative_improvement_percent'])
            wins[metric] += int(m0 > m1)
    assert wins == {'execution': 8, 'equal_workload': 9}
    for metric in wins:
        assert report[metric + '_logmae_seed_summary']['m1_better_seeds'] == wins[metric]
    assert {int(x['split_seed']) for x in selected if float(x['execution_logmae_m0_minus_m1']) < 0} == {20261101, 20261102}
    assert float(csv_by_seed[20261102]['equal_workload_logmae_m0_minus_m1']) > 0
    print('PASS: Experiment 3 source binding, population, 240 candidates, winners and validation tables')

    banned = {'.parquet', '.arrow', '.feather', '.duckdb', '.sqlite', '.npy', '.npz', '.pkl', '.pickle', '.joblib', '.bin', '.pt', '.pth', '.onnx', '.zip', '.gz'}
    for p in files:
        assert p.suffix.lower() not in banned and p.name != 'model.txt', ('excluded asset', p)
        assert p.stat().st_size < 5 * 1024**2, ('large file', p)
        assert p.name != '.DS_Store' and '__pycache__' not in p.parts
    print('PASS: no datasets, trained model files, archives, caches or files >= 5 MiB')
    print('All static checks passed. No experiment code, training or outcome evaluation executed.')


if __name__ == '__main__':
    verify()
