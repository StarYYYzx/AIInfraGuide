"""Validate canonical progress and regenerate readable views; never invent mastery."""
from pathlib import Path
import json, csv, io, argparse, re
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[2]
HOME=ROOT/'learning'
LEVELS=['unverified','read','explained','exercise_passed','measured']
STATUSES=['not_started','in_progress','blocked','passed']
def load():
    return json.loads((HOME/'progress.json').read_text(encoding='utf-8')),json.loads((HOME/'curriculum.json').read_text(encoding='utf-8'))
def validate(p,c):
    assert p['schema_version']==1
    assert p['revision']>=1
    assert 1<=p['cursor']['day']<=120
    assert set(p['days'])=={str(i) for i in range(1,121)}
    assert len(c['days'])==120
    def ref(path):
        assert path and not Path(path).is_absolute() and '..' not in Path(path).parts,path
        assert (ROOT/path).is_file(),path
    for n in c['nodes'].values():ref(n['path'])
    for k,d in p['days'].items():
        assert d['status'] in STATUSES,(k,d)
        assert d['level'] in LEVELS,(k,d)
        for path in d['sessions']+d['evidence']:ref(path)
        if d['level']!='unverified':assert d['sessions'],('claimed level without session',k)
        if d['level'] in ['exercise_passed','measured']:assert d['evidence'],('no evidence',k)
        if d['status']=='passed':assert d['level'] in ['exercise_passed','measured'] and d['gate'] in ['exercise','measurement']
        if d['level']=='measured':assert d['gate']=='measurement'
    for id,n in p['nodes'].items():
        assert id in c['nodes'] and n['level'] in LEVELS
        for path in n['evidence']:ref(path)
        if n['level']!='unverified':assert n['evidence'],('node claim without evidence',id)
    for path in p['recent_sessions']:ref(path)
    assert p['cursor']['target_node'] in c['nodes']
    passed={int(k) for k,d in p['days'].items() if d['status']=='passed'}
    if passed:assert passed==set(range(1,max(passed)+1)),('mainline must remain contiguous',passed)
    assert p['cursor']['day']==len(passed)+1 if len(passed)<120 else p['cursor']['day']==120
    visiting=set();done=set()
    def walk(id):
        assert id not in visiting,('dependency cycle',id)
        if id in done:return
        visiting.add(id)
        for e in c['nodes'][id]['requires']:walk(e['id'])
        visiting.remove(id);done.add(id)
    for id in c['nodes']:walk(id)
    return len(passed)
def render(p,c,count):
    day=p['cursor']['day']; unit=c['days'][day-1]; nodes=c['nodes']; cursor=p['cursor']
    lines=['# AI Infra 学习进展记录','','> 自动由 progress.json 生成。修改真实状态后运行 python learning/tools/progress.py render；不直接改本文件。','',f"- 更新：{p['updated_at']}（revision {p['revision']}）",f'- 主线验收通过：{count}/120 学习日',f"- 当前：第{day}学习日 / W{unit['week']}D{unit['weekday']} / {unit['topic']}",f"- 状态：{p['days'][str(day)]['status']}；能力证据等级：{p['days'][str(day)]['level']}",'- 已核实学习事实：'+p['baseline']['verified_learning'],'', '## 下一位AI从这里继续', '', '- 首读顺序：'+' → '.join(f"[{id} · {nodes[id]['name']}]({quote('../'+nodes[id]['path'],safe='/')})" for id in unit['ids']),'- 当前计划版本：'+(c.get('plan_update') or {}).get('version','original')+'（[近期更新]('+quote(Path((c.get('plan_update') or {}).get('guide','README.md')).name)+')，实际回补栈优先）','- 当天限定范围：'+unit['scope'],'- 当前精确断点：'+cursor['section'],'- 下一动作：'+cursor['next_action'],'- 待提问：'+cursor['pending_question'],'- 回补栈：'+(' → '.join(cursor['remediation_stack']) or '空；先诊断，不预设需要补完整基础'),'- 下次汇报：'+cursor['next_report'],'', '## 当前阻塞与环境', '']
    lines += ['- '+x for x in p['blockers']]+['','- 环境：'+p['environment']['summary'],'- 实验条件：'+p['environment']['experimental_capability'],'','## 最近会话','']
    lines += ([f'- [{x}]({quote(x.removeprefix("learning/"),safe="/")})' for x in p['recent_sessions']] or ['尚无经验证的学习会话。准备导航/档案不等于学习完成。'])
    lines += ['','## 120学习日进度','','[完整逐日进度表](DAY_PROGRESS.csv) · [文档能力清单](NODE_PROGRESS.csv) · [课程索引](2026-11-16_AIInfra_逐日文档与概念回补索引.md)','','| 学习日 | 主课 | 状态 | 证据等级 | 最近会话 |','|---|---|---|---|---|']
    for d in c['days']:
        s=p['days'][str(d['day'])];lines.append(f"| {d['day']} / W{d['week']}D{d['weekday']} | {' → '.join(d['ids'])} | {s['status']} | {s['level']} | {', '.join(s['sessions']) or '—'} |")
    (HOME/'PROGRESS.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    for filename,header,rows in [
        ('DAY_PROGRESS.csv',['day','week','weekday_slot','topic','documents','status','level','gate','sessions','evidence','notes'],[[d['day'],d['week'],d['weekday'],d['topic'],' '.join(d['ids']),p['days'][str(d['day'])]['status'],p['days'][str(d['day'])]['level'],p['days'][str(d['day'])]['gate'],';'.join(p['days'][str(d['day'])]['sessions']),';'.join(p['days'][str(d['day'])]['evidence']),p['days'][str(d['day'])]['notes']] for d in c['days']]),
        ('NODE_PROGRESS.csv',['id','document','kind','path','level','evidence','notes'],[[id,n['name'],n['kind'],n['path'],p['nodes'][id]['level'],';'.join(p['nodes'][id]['evidence']),p['nodes'][id]['notes']] for id,n in nodes.items()])]:
        buff=io.StringIO(newline='');w=csv.writer(buff,lineterminator='\n');w.writerow(header);w.writerows(rows);(HOME/filename).write_text(buff.getvalue(),encoding='utf-8')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['init','check','render']);args=parser.parse_args()
    if args.command=='init':
        assert not (HOME/'progress.json').exists(),'Existing progress will not be overwritten'
        c=json.loads((HOME/'curriculum.json').read_text(encoding='utf-8'))
        p={'schema_version':1,'revision':1,'updated_at':'2026-11-16','course_commit':'bffa2b0bcbf1b3d5d33c5ba0869611a74f6c59e4','repository':'https://github.com/StarYYYzx/AIInfraGuide','policy':{'mainline':'Infra-first','weekends':'no study, no preparation, no catch-up','weekday_minutes':75,'report':'previous workday if morning; Monday prepared Friday','advance':'only after evidence-based gate'},'baseline':{'verified_learning':'仅完成课程规划、文档索引和接手档案；尚无用户答题、练习或实验结果证明掌握。','assumptions':'不预设CUDA Reduce完成，不预设周末学习或某模型已跑通。'},'cursor':{'day':1,'target_node':'I11','section':'1.1-LLM推理基础：§1–3，先诊断后限定阅读','mode':'diagnostic_pending','remediation_stack':[],'next_action':'确认今天可用时长；询问用户对Prefill/Decode、KV、TTFT/TPOT/E2E的理解，先提一题并等待回答。','pending_question':'请用自己的话说明Prefill和Decode分别在做什么；当前只提这一题，后续按答题情况再诊断。','next_report':'尚无学习结果；初次汇报只讲课程主线与待验证问题，不讲已掌握。'},'days':{str(i):{'status':'not_started','level':'unverified','gate':'pending','sessions':[],'evidence':[],'notes':''} for i in range(1,121)},'nodes':{id:{'level':'unverified','evidence':[],'notes':''} for id in c['nodes']},'recent_sessions':['learning/sessions/2026-11-16_00_setup.md'],'blockers':['尚无基线诊断；实际掌握程度待确认。'],'environment':{'summary':'本地课程可读；跨设备应重新核对软件与硬件。','experimental_capability':'GPU型号、运行时、模型/数据权限和多卡条件均未确认。'}}
        (HOME/'progress.json').write_text(json.dumps(p,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    p,c=load();count=validate(p,c)
    if args.command in ['init','render']:render(p,c,count)
    print(json.dumps({'valid':True,'passed_days':count,'cursor_day':p['cursor']['day'],'nodes':len(c['nodes']),'relative_paths_valid':True},ensure_ascii=False))
if __name__=='__main__':main()
