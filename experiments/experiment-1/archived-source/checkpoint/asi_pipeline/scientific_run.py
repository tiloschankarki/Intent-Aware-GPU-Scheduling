"""All validation selections precede the experiment-wide freeze and all test work."""
import importlib.util
import json
from pathlib import Path
import sys
import uuid
from .execution import context,validate_selection,select_model,predict_selected
from .checkpoints import publish_unit,read_unit,code_state,versions
from .dataset import sha256
from .windows_monitor import supervise

def experiment_units(p):
    return [{'population':population,'comparison':'+'.join(pair['m0']),'seed':seed,'role':role}
            for population in ('broad','finite') for pair in p['paired_ablations']
            for seed in p['model']['seeds'] for role in ('m0','m1')]

def location(output,u):
    return Path(output)/'models'/u['population']/u['comparison']/str(u['seed'])/u['role']

def freeze_experiment(output,p,binding,units):
    if units!=experiment_units(p):raise ValueError('Experiment unit scope mismatch')
    selections=[]
    for u in units:
        folder=location(output,u)/'selection'
        unit=read_unit(folder)
        b=unit['binding'];validate_selection(folder,b,p)
        if b.get('versions')!=versions():raise ValueError('Global selection package versions changed')
        for key in ('protocol_sha256','dataset_manifest_sha256','code'):
            if b.get(key)!=binding.get(key):raise ValueError('Global selection binding mismatch')
        if (b['population'],b['comparison'],b['model_seed'],b['role'])!=(u['population'],u['comparison'],u['seed'],u['role']):raise ValueError('Global selection context mismatch')
        selections.append({'unit':u,'selection_sha256':sha256(folder/'manifest.json')})
    path=Path(output)/'selection-freeze'
    if path.exists():
        record=read_unit(path,binding)['record']
        if record['selections']!=selections:raise ValueError('Frozen selection changed')
    else:publish_unit(path,binding,{'selections':selections},{})
    return selections

def run(dataset,output,config,authorization):
    output=Path(output);output.mkdir(parents=True,exist_ok=True)
    p=json.loads(Path(config).read_bytes());units=experiment_units(p)
    p,dm,b=context(dataset,config,'broad','workload_disjoint','R+P+A',20260927,'m0',authorization)
    binding={k:b[k] for k in ('protocol_sha256','dataset_manifest_sha256','code')}
    script=Path(__file__).resolve().parents[1]/'scripts/run_windows_science.py'
    def launch(phase,u):
        dest=location(output,u)
        cmd=[sys.executable,'-B',str(script),phase,'--dataset',str(Path(dataset).resolve()),'--output',str(dest.resolve()),
             '--config',str(Path(config).resolve()),'--authorization',str(Path(authorization).resolve()),
             '--population',u['population'],'--comparison',u['comparison'],'--seed',str(u['seed']),'--role',u['role']]
        result=supervise(cmd,output/'monitor'/uuid.uuid4().hex,spill=Path(dataset)/'spill')
        if result['status']!='PASSED':raise RuntimeError('Scientific worker failed or stopped for safety; no further stages run')
    for u in units:
        dest=location(output,u)
        if (dest/'selection').exists():
            _,_,expected=context(dataset,config,u['population'],'workload_disjoint',u['comparison'],u['seed'],u['role'],authorization)
            validate_selection(dest/'selection',expected,p)
        else:launch('select',u)
    freeze_experiment(output,p,binding,units)
    for u in units:
        # Revalidate the global freeze before each test worker, including on resume.
        freeze_experiment(output,p,binding,units)
        launch('test',u)
    spec=importlib.util.spec_from_file_location('frozen_evaluation',script.with_name('06_generalization.py'))
    evaluator=importlib.util.module_from_spec(spec);spec.loader.exec_module(evaluator)
    reports=[]
    for u in units:
        if u['role']!='m0':continue
        parent=location(output,u).parent;dest=output/'evaluations'/u['population']/u['comparison']/str(u['seed'])
        if dest.exists():
            read_unit(dest)
            record=json.loads((dest/'evaluation.json').read_bytes())
            if record['provenance']['m0_manifest_sha256']!=sha256(parent/'m0/manifest.json') or record['provenance']['m1_manifest_sha256']!=sha256(parent/'m1/manifest.json'):raise ValueError('Evaluation resume mismatch')
        else:record=evaluator.evaluate(parent/'m0',parent/'m1',config,dest)
        reports.append({'unit':u,'report':record})
    if not (output/'complete').exists():publish_unit(output/'complete',binding,{'reports':reports},{})
    return reports
