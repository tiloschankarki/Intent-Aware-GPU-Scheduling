import sys,json,math,hashlib
from pathlib import Path
sys.path.insert(0,"/private/tmp/asi-audit-20261029/deps")
import duckdb
root=Path(sys.argv[1] if len(sys.argv)>1 else "/private/tmp/asi-audit-20261029"); c=duckdb.connect(); out=[]
for p in sorted(root.glob("*.parquet")):
 rows=c.execute("select workload_id,executions,m0_loss_sum,m1_loss_sum from read_parquet(?)",[str(p)]).fetchall()
 G=len(rows);N=sum(r[1] for r in rows);s0=sum(r[2] for r in rows);s1=sum(r[3] for r in rows)
 sortedrows=sorted(rows,key=lambda r:(-r[1],r[0]))
 item=dict(seed=int(p.stem),workloads=G,executions=N,unique_workloads=len(set(r[0] for r in rows)),positive_counts=all(r[1]>0 for r in rows),
 m0_micro=s0/N,m1_micro=s1/N,m0_macro=sum(r[2]/r[1] for r in rows)/G,m1_macro=sum(r[3]/r[1] for r in rows)/G,
 favor_m1_percent=100*sum(r[2]>r[3] for r in rows)/G,ties=sum(r[2]==r[3] for r in rows),net_loss_difference=s0-s1,sha256=hashlib.sha256(p.read_bytes()).hexdigest())
 for mode,k in [("floor",G//100),("ceil",math.ceil(G/100))]:
  top=sortedrows[:k]; item["top1_"+mode]=dict(k=k,execution_share=sum(r[1] for r in top)/N,delta=sum(r[2]-r[3] for r in top),rest_delta=sum(r[2]-r[3] for r in sortedrows[k:]))
 item["capped"]={}
 for cap in [100,1000]:
  den=sum(min(cap,r[1]) for r in rows)
  item["capped"][str(cap)]={f"m{j}_loss":sum(min(cap,r[1])*r[j+2]/r[1] for r in rows)/den for j in [0,1]}
 item["bands"]=[]
 for lo,hi in [(1,1),(2,10),(11,100),(101,1000),(1001,10**12)]:
  rr=[r for r in rows if lo<=r[1]<=hi];item["bands"].append(dict(lo=lo,hi=hi,workloads=len(rr),executions=sum(r[1] for r in rr),delta=sum(r[2]-r[3] for r in rr)))
 out.append(item)
(root/"arithmetic_verification.json").write_text(json.dumps(out,indent=2))
for x in out:
 print(json.dumps({k:v for k,v in x.items() if k not in ["sha256","bands"]}))
 if x["seed"] in [20261101,20261102,20261106]: print("bands",x["seed"],x["bands"])

