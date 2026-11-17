from pathlib import Path
import re, json, html
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[2]
BASE=ROOT/'docs/guides'
OUT=ROOT/'learning'
files=sorted(BASE.rglob('*.md'))
assert len(files)==102, len(files)
nodes={}
def add(id,name,kind='正文'):
    found=[p for p in files if p.name==name]
    assert len(found)==1,(id,name,found)
    p=found[0]; text=p.read_text(encoding='utf-8')
    heads=[]; fence=None
    for i,line in enumerate(text.splitlines(),1):
        token=re.match(r'^\s*(`{3,}|~{3,})',line)
        if token:
            if fence is None:fence=token[1][0]
            elif token[1][0]==fence:fence=None
            continue
        if fence is None and (m:=re.match(r'^(#{2,4})\s+(.+)',line)):
            heads.append({'level':len(m[1]),'title':m[2].strip(),'line':i})
    nodes[id]={'id':id,'name':p.stem,'path':p.as_posix(),'rel':p.relative_to(BASE).as_posix(),'kind':kind,'headings':heads,'requires':[],'review':[],'covers':[],'note':''}
    return id
fixed={'P1':'第1章-编程语言基础.md','P2':'第2章-数学基础.md','P3':'PyTorch框架入门.md','P4':'gpu-basics.md','P5':'nvidia-gpu-evolution.md','P6':'collective-communication-primer.md','R0':'AI Infra学习路线.md','R1':'Transformer架构快速入门.md','R2':'CUDA编程入门指南.md'}
for id,name in fixed.items():add(id,name,'导航' if id=='R0' else '概览' if id in ['R1','R2'] else '正文')
for i in range(1,10): add('T'+str(i),next(p.name for p in files if p.parent.name=='transformer' and p.name.startswith('3.'+str(i)+' ')))
for a,names in {
'C':['1.1-CUDA开发环境搭建','1.2-CUDA编程模型','1.3-CUDA内存模型','1.4-第一个实用Kernel','2.1-Warp与执行模型','2.2-内存访问优化','2.3-Occupancy与资源分配','2.4-同步与原子操作','3.1-CUDA Reduce算子优化','4.1-CUDA GEMM算子性能优化','5.1-CUDA Softmax朴素实现优化','5.2-CUDA Online Softmax实现','6.1-FlashAttention V1详解','6.2-FlashAttention V2详解','7.1-Triton编程框架'],
'D':['1.1 分布式训练总论','1.2 环境搭建与分布式启动','2.1 集合通信原语详解','3.1 优化器原理与显存开销分析','4.1 数据并行详解','4.2 PyTorch 数据并行从原理到实战'],
'I':['1.1-LLM推理基础','1.2-vLLM快速入门','2.1-PagedAttention','2.2-Continuous Batching','2.3-Prefix Cache 与 RadixAttention','2.4-Chunked Prefill 与统一调度','2.5-Attention 后端与图优化'],
'N':['3.1-项目全景与四层架构','3.2-配置入口与推理主循环','3.3-模型与核心算子','3.4-KVCache与BlockManager','3.5-Scheduler与连续批处理','3.6-ModelRunner引擎循环与性能'],
'Q':['4.1-量化基础','4.2-W8A8与SmoothQuant','4.3-Weight-only-INT4','4.4-KV-Cache量化','4.5-FP8与NVFP4-MXFP4','4.6-量化选型与vLLM实战'],
'S':['5.1-投机解码核心原理','5.2-Draft模型与无模型方案','5.3-Medusa与EAGLE','5.4-收益边界与限制','5.5-vLLM投机解码实战'],
'V':['6.1-推理并行策略总览','6.2-张量并行推理','6.3-流水线并行推理','6.4-数据并行与专家并行','6.5-多节点部署','6.6-vLLM分布式部署实战'],
'E':['9.1-端侧推理基础']}.items():
    for name in names:add(a+name[:3].replace('.',''),name+'.md')
used={n['path'] for n in nodes.values()}
for p in files:
    if p.as_posix() in used:continue
    num=re.match(r'第(\d+)章',p.name)[1]
    mod='P' if '模块一' in str(p) else 'C' if '模块二' in str(p) else 'D' if '模块三' in str(p) else 'I'
    add('O'+mod+num,p.name,'提纲')
# Edges point from reading target to prerequisite; section notes limit the requirement.
raw='''P3|P1:§2 Python对象/控制流;P2:§2 张量与矩阵、§6反向、§7优化
P5|P4:SM/显存/Tensor Core
P6|P4:互联与设备；代码实验另看P1/P3
T9|P1:§2 Python;P2:§2.1/2.4/2.6;P3:Tensor与Embedding
T2|P3:Tensor/Module;P2:§2;T9:输入与词嵌入（结构概览可先读）
T3|T2:结构数据流;P2:§2.4/2.6/2.7、§4.6、§5.2;P3:Tensor shape
T4|T2:线性层;P2:§2.3/2.6/2.8;P3:nn.Linear
T5|T3:QK计算;T9:token位置;P2:§2.4/2.6/2.9
T6|T2:Block结构;P2:§4.6、§6.4、§7.4–7.8;P3:autograd
T7|T3:Attention;T4:FFN;T5:位置编码;T6:Norm/残差;T9:词嵌入
T8|T7:Decoder;P2:§4.2、§5.1–5.5/5.9
C11|P1:§4、§5、§7、§8 编程与环境;P4:GPU
C12|C11:环境;P4:SM;P1:§4.1–4.2 指针与数组
C13|C12:线程模型;P1:§4.2–4.4 内存与生命周期
C14|C11:构建;C12:索引;C13:内存;P1:§3.6 计时
C21|C12:线程模型;C14:最小kernel;P4:SM
C22|C13:存储层次;C21:warp;P2:§2.2 stride
C23|C13:寄存器/shared;C21:执行单元
C24|C13:可见性;C21:执行模型
C31|C14:正确性;C21:warp;C22:访存;C24:同步;P2:§8.4 归约顺序
C41|C14:kernel;C22:访存;C23:资源;C24:同步;P2:§2.6、§3 GEMM
C51|C31:归约;P2:§5.2、§8.5
C52|C51:稳定Softmax;P2:§9.4 分块合并
C61|T3:Attention;C41:GEMM;C52:在线归一化;P2:反向部分§6
C62|C61:V1;C23:资源;C21:工作分配
C71|P1:§2 Python;P3:Tensor;C13:仅存储层次概念;P2:§5.2
D11|P3:完整训练循环;P4:资源;P2:§9.7 显存
D12|D11:训练问题;P6:通信环境;P1:§3.4/7/8;P3:训练循环
D21|D12:rank/进程组，数学示意无需先运行;P6:原语;P2:§2.1/4.5
D31|P3:训练循环;P2:§6/7.1–7.3/8
D41|D11:显存;D21:通信;D31:优化器状态;P2:§9.6加权均值
D42|D41:数据并行;D12:启动;P3:训练循环
I11|T8:自回归/KV，仅术语导入可先读;P4:带宽/算力;P2:§3.3/9.7
I12|I11:阶段/指标;P1:§7–8 环境;P3:设备/dtype
I21|I11:KV Cache;P1:§4.2 地址/连续内存
I22|I11:两阶段;I21:分页缓存
I23|I21:缓存块;T3:因果依赖;T9:Token ID
I24|I22:调度;I11:阶段;I21:缓存容量
I25|I24:调度;C61:后端原理（选型概览不用先写kernel）;P3:§6 Profiler;P1:§3.6计时
N31|I21:分页;I22:批处理;I23:复用;I24:调度;I25:后端
N32|N31:架构;T8:generate;P1:§2.4/2.9/3.4
N33|N32:入口;T7:模型;T8:自回归;C71:Triton;I25:后端;P6:TP通信
N34|N32:状态入口;I21:块;I23:哈希;P1:§2对象
N35|N34:缓存分配;I22:批处理;I24:token预算
N36|N33:算子;N34:块;N35:调度;I25:图优化
Q41|P2:§2.2/2.8/4.6/8.1–8.5;P3:§1 dtype
Q42|Q41:scale/粒度;T4:线性层;P2:§2.6/2.9
Q43|Q41:基础;Q42:异常值;P2:GPTQ补§2.5/2.9/4.7/6.3/8.7
Q45|Q41:缩放;P5:架构（先掌握P4）;P2:§8数值
Q44|Q41:基础;I11:KV容量;T3:Key/Value;Q45:仅FP8基础§1–2
Q46|I12:运行;I11:指标;Q41:基础;Q42:INT8;Q43:INT4;Q44:KV;Q45:FP格式
S51|T8:生成分布;I11:阶段;P2:§4.1–4.5/5.1–5.4/5.9
S52|S51:验收;T9:tokenizer兼容;I11:成本
S53|S51:拒绝采样;T7:结构;T5:位置
S54|S51:原理;S52:draft成本;S53:方案;I22:负载;I24:调度;I25:后端
S55|I12:部署;S51:原理;S52:选型;S53:方案;S54:边界;P1:§3.5–3.6/7–8
V61|I11:推理;T7:模型;P6:通信
V62|V61:并行全景;T3:KV头;T4:线性切分;P6:AllReduce
V63|V61:并行;T7:层结构;I22:batch;I24:调度
V64|V61:并行;T4:§8 MoE;P6:通信;D21:All-to-All
V65|I12:服务;V62:TP;V63:PP;V64:DP/EP;D12:启动;P6:网络;P1:§7–8
V66|I12:服务;V62:TP;V63:PP;V64:DP/EP;I21:缓存;I22:批处理;I24:调度;P1:§3.6计时
E91|P3:导出;P1:§4–5/8;Q41:只在量化节回补；CPU入门无需量化;I11:仅LLM应用需要'''
for line in raw.splitlines():
    id,rest=line.split('|');nodes[id]['requires']=[{'id':s.split(':',1)[0],'why':s.split(':',1)[1]} for s in rest.split(';')]
reviews={'P4':['P2'],'P6':['P1','P3'],'T2':['R1','T1'],'T3':['R1'],'T7':['R1','T2'],'T8':['I11'],'C24':['P1'],'C31':['R2'],'C41':['R2'],'C51':['R2'],'C71':['C51','C52','R2'],'D11':['T7'],'I11':['R0','E91'],'N33':['D21','V62'],'N36':['D12','P1','P6'],'Q43':['C41'],'S53':['P2'],'S54':['Q41','Q43','Q45'],'V62':['D21'],'V63':['V62'],'V64':['V62'],'V66':['V65'],'E91':['T8']}
for id,rs in reviews.items():nodes[id]['review']=rs
covers={'OP3':['T'+str(i) for i in range(1,10)]+['R1'],'OP4':['P3'],'OP5':['P4','P5'],'OP6':['P6']}
for num in range(1,9):covers['OC'+str(num)]=[id for id in nodes if id.startswith('C'+str(num))]+(['R2'] if num==8 else [])
for num in range(1,5):covers['OD'+str(num)]=[id for id in nodes if id.startswith('D'+str(num))]
for num,lead in [(1,'I1'),(2,'I2'),(3,'N3'),(4,'Q4'),(5,'S5'),(6,'V6'),(9,'E9')]:covers['OI'+str(num)]=[id for id in nodes if id.startswith(lead)]
for id,cs in covers.items():nodes[id]['covers']=cs
outline_prereq={'OD5':['D31','D41','D42'],'OD6':['T4','P6','D21','V62'],'OD7':['D11','D21','T7','V63'],'OD8':['P2','P3','D31'],'OD9':['T3','C61','P6','D21'],'OD10':['T4','D21','V64'],'OD11':['D12','D21','V61'],'OC8':['P3','R2','C14'],'OI7':['I11','I24','R0'],'OI8':['I12','V65','V66']}
for id,ids in outline_prereq.items():
    nodes[id]['requires']=[{'id':x,'why':'已有相关基础；不能替代该专题完整教程'} for x in ids]
    nodes[id]['note']='本文件是提纲，课程内没有对应完整展开正文；只用于定目标。推理PP/EP/DCP不等于训练PP/EP/CP。'
nodes['T9']['note']='文中旧引用“3.6位置编码”应对应实际3.5位置编码（T5），不是LayerNorm（T6）。'
nodes['N35']['note']='nano-vllm支持部分chunked prefill，但不等于vLLM V1混合统一调度。'
nodes['N33']['note']='nano-vllm教学代码与生产vLLM不是相同功能集合；文中Triton、TP、词表并行需按小节回补。'
nodes['Q43']['note']='Cholesky/阻尼虽有提及，但目录中没有独立系统教程；不能假装已经完整覆盖。'
# Five bounded learning units per week, not one full file per day.
weeks=[
('系统地图与培训前导入',[
('I11 R0','I11§1–3：只读Prefill/Decode、KV和TTFT/TPOT/E2E；R0只看路线与验收','链路图＋三个指标算例'),
('P4 P2','P4§2–4：SM、显存、带宽/算力；P2§8.1–8.5数值','规格字段表＋权重存储量'),
('Q41','§2–5：scale/zero-point、粒度、校准、PTQ/QAT，不进入完整算法','量化/反量化算例'),
('P3 P2','P3§4训练循环仅概览；P2§2.13低秩更新','训练图＋LoRA参数算例'),
('I11 P4 Q41 P2','复验本周四个问题；培训输入只做事实/建议/待验证分栏','四张卡＋周一汇报材料')]),
('模型全景与端侧测量入口',[
('R1 T2 T9','R1结构概览→T9输入/Embedding→T2结构段，不精读全部实现','模型数据流与维度图'),
('T8 I12 P3','T8两阶段概览；I12离线调用段；缺框架补P3 Tensor/Module','一次generate走读或冒烟'),
('E91 I11','E91§1–3约束、§7可信Benchmark；I11§3测量边界','新板验收框架'),
('P1','§4.1–4.5生命周期→§5.3–5.4动态库/ABI→§6.2 ctypes','接口状态图＋边界检查'),
('I11 T2 E91','复用本周图表进行验收，不引入新课','两周证据与未过关清单')]),
('数学与PyTorch必要前置',[
('P2 P3','P2§2.1–2.8 shape/stride/广播/BMM；P3§1 Tensor','矩阵维度与stride算例'),
('P2','§5.1–5.5 logits/稳定softmax/交叉熵','稳定性与loss例题'),
('P2 P3','P2§6.1–6.6/6.9；P3§2 autograd','一个梯度检查'),
('P3 P2','P3§3–4 Module/优化器；P2§7.1–7.3','一个训练步追踪'),
('P3','§4完整循环验收；不了解数据加载只补必要小节','手写前向到update流程')]),
('Transformer上半',[
('T1 T9 T2','T1动机→T9词表/Embedding→T2数据流','输入到logits结构图'),
('T3 P2','T3§2–6 QKV与维度；P2§9.2–9.3算例','QKV维度推导'),
('T3','因果mask及softmax对应小节','带mask注意力算例'),
('T4 P2','T4基础FFN/SwiGLU；P2§9.1线性层代价','FFN参数/FLOPs账本'),
('T3 T4 T2','Attention/FFN复验；完整实现以后再深入','白板解释与错题')]),
('Transformer下半',[
('T5 T9','位置编码基础/RoPE；不扩展全部长上下文方案','位置编码作用与shape'),
('T6 P2','Norm/残差；P2§7.4–7.8','梯度与Norm数据流'),
('T7 T2','组装Decoder Block；回看T2完整结构','Block白板默写'),
('T8 T9 P2','生成/KV；P2§5.4/5.9 temperature/top-k/top-p','token到生成追踪'),
('T7 T8 P2','参数/激活/KV估算；P2§9.7','显存账本及假设')]),
('训练与评测闭环',[
('P3 P1','P3§4.1 Dataset/DataLoader；P1§2.5生成器','数据分割与加载清单'),
('P3','§4训练/验证及eval/no_grad','两模式对照'),
('P3','§4.4 checkpoint保存/恢复','保存加载一致性'),
('P3 P2','训练/验证协议与分类loss；检测IoU/mAP在本目录无完整主讲，另列待补','评测协议＋检测知识缺口'),
('P3','完整小模型训练/验证；无环境则代码与数据验证','曲线/错误样本或明确未测')]),
('训练显存与微调桥接',[
('D31 D11 P2','优化器状态与显存；P2§9.7','训练账本'),
('P2','§2.10–2.13秩/LoRA、§9.5算例','低秩新增参数与计算'),
('P3 P2','P3 loss/数据；P2§5.5/6.8；完整SFT/PEFT教程为课程缺口','样本/loss mask检查方案'),
('P3 P2','用已有训练循环与LoRA数学验收；adapter工程需外补，未补不宣称跑通','训练参数/保存设计'),
('P3 I11','同一验证集比较；资源不足给评测设计','基线/微调对照或未测项')]),
('GPU到CUDA',[
('C11 P1 P4','C11环境；P1§8.3–8.4软件栈','环境字段与诊断顺序'),
('C12','grid/block/thread索引与边界','索引覆盖证明'),
('C13','global/shared/register','存储层次图'),
('C14','向量加法与边界；先正确再优化','正确性结果或代码检查'),
('C14 P1','CUDA同步/计时；P1§3.6','baseline与测量协议')]),
('CUDA执行访存同步',[
('C21','warp/SIMT/分支','执行示意'),
('C22 P2','合并访问/stride；P2§2.2','布局算例'),
('C23','寄存器/shared/occupancy','资源账本'),
('C24','同步/原子/可见性','正确与错误场景'),
('C22 C23 C24','一个受控访存对照','结果或待测计划')]),
('Reduce',[
('C31','问题与朴素版本','正确性baseline'),
('C31 C24','共享内存树形、同步','归约数据流'),
('C31 C21','warp shuffle版本','warp内归约'),
('C31 P2','对照与误差；P2§8.4','延迟/带宽/误差'),
('C31','复验三方案，不达标顺延','正确性、收益和限制')]),
('GEMM第一轮',[
('P2 C41','P2§2.6、§3；C41问题与算量','FLOPs/访存估算'),
('C41','naive实现与小矩阵','baseline正确性'),
('C41 C13','shared tiling与数据复用','tile数据图'),
('C41 P2','尾块/边界；P2§3.5','多shape正确性集'),
('C41','naive/tiling/cuBLAS对照','控制变量对照')]),
('GEMM第二轮',[
('C41 C23','寄存器分块与资源','复用/资源图'),
('C22 C41','bank conflict/布局','一个布局算例'),
('C41','只改一个tile/参数','调参记录'),
('C41 P4','库基线/Roofline瓶颈','性能差距解释'),
('C41','复盘而不是追固定百分比','优化证据与限制')]),
('Softmax',[
('P2 C51','P2§5.2–5.3；C51数值稳定','溢出与max-subtract算例'),
('C51 C31','朴素softmax与归约','正确性baseline'),
('C52 P2','在线max/sum递推；P2§9.4','分块合并推导'),
('C51 C52','读写融合与访存','IO账本'),
('C51 C52','多长度/多精度对照','误差与性能')]),
('Attention算子',[
('T3 C61','T3机制复习；C61 IO问题','中间张量账本'),
('C61 C41','V1分块与GEMM','tiling图'),
('C52 C61','在线归一化与attention对应','公式对应'),
('C62 C23','V2工作分配/资源','V1/V2对照'),
('C61 C62','推导/代码走读/条件允许实测','IO收益边界')]),
('Triton与Profiler',[
('C71','program/block/tl.load/tl.store','CUDA/Triton映射'),
('C71 C51','最小fused softmax','正确性证据'),
('P3 R2 OC8','P3§6 profiler；R2工具章节；OC8仅目标','时间线解释'),
('C23 C22 P4','kernel资源/带宽指标','瓶颈解释'),
('C71','一项算子全流程复验','代码/原理/基线/限制')]),
('通信与分布式入口',[
('D11 D31','训练状态账本','显存估算'),
('P6 D21','AllReduce基础与小数组；代码部分以后','通信量与数据流'),
('D21 P6','AllGather/ReduceScatter','原语演示'),
('D12 P1','rank/world_size/启动/进程组；P1§3.4','进程拓扑'),
('D12 D21','多卡条件核对；单卡只验推导','实验方案与未测项')]),
('数据并行与训练策略',[
('D41 D42','DP/DDP基础→实战代码结构','梯度同步图'),
('P3 OD8 P2','梯度累积/mixed precision；OD8提纲；P2§8','等效batch例题'),
('D41 D42 OD5','FSDP/ZeRO账本，提纲不作完整教程','分片账本'),
('OD6 OD7 T4 V62 V63','先看提纲→T4线性切分→V62/V63相关推理解释；训练细节仍缺','TP/PP取舍与缺口'),
('D42','条件允许最小DDP/FSDP；否则通信走读','结果或代码/账本验收')]),
('推理引擎核心',[
('I21 I11','PagedAttention块表/碎片','分配图'),
('I22','连续批处理/抢占','时序对照'),
('I23 T9','Prefix/Radix哈希与Token ID','复用条件'),
('I24 I25','token预算/后端选型；图优化原理卡住回CUDA','调度取舍'),
('I12 I11','固定请求负载与指标','吞吐/尾延迟方案')]),
('nano-vllm源码',[
('N31 N32','四层架构→config/入口','调用图'),
('N33','Norm/RoPE/FFN/TP/Triton各取关键小节；太多则顺延','shape追踪'),
('N34','BlockManager分配/哈希/释放','状态追踪'),
('N35 N36','Scheduler→ModelRunner主循环；图与多进程可分日','一次generate路径'),
('N32 N34 N35 N36','一次请求全链路复验','定位证据与尚未懂的小节')]),
('量化基础与INT量化',[
('Q41 P2','scale/zero-point/粒度；P2数值复验','量化算例'),
('Q41 Q42','校准/异常值/等价缩放','误差解释'),
('Q42','W8A8/SmoothQuant推导','缩放证明'),
('Q43 P2','GPTQ/AWQ/Marlin；Hessian卡住补P2§6.3','方法/格式/kernel分层'),
('Q46 I12','固定baseline/一种支持的量化','质量/内存/时延同表')]),
('KV与FP量化',[
('Q44 Q45','Q44 KV账本；遇到FP8先补Q45§1–2','KV容量与误差'),
('Q45 P2 P5','FP8/FP4/MXFP格式与硬件条件','格式/缩放图'),
('Q45','NVFP4/MXFP4差别与执行路径','块尺度/支持条件'),
('E91 Q46','运行时/量化选型；GGUF/Q4_K_M目录无完整讲解，标外补','容器/预设/后端区分'),
('Q46','只测一项可运行量化；不支持如实记录','收益边界')]),
('端侧与图像案例',[
('E91','§1–5约束/链路/运行时','需求与资源表'),
('C12 P2 E91','C12§7.1二维图像索引；P2 shape；crop/resize算法无完整独立教程','坐标/数据正确性方案'),
('E91 P3','Benchmark/Profiler分段，CPU/GPU迁移需真实实现','分段时延方案或结果'),
('Q46 E91','精度/分辨率/并发只改一个','单变量对照'),
('E91 I11','质量/延迟/内存/功耗整合','端侧方案取舍')]),
('高阶推理概览',[
('S51 S54','先S51原理，S54读成本边界；方案卡住补S52/S53','投机收益条件'),
('V61 V62 V63 V64','总览优先；各方案只读结构，详细推导可延后','TP/PP/DP/EP部署图'),
('V65 V66 D12','核对单机/多节点实验条件，不直接照8卡命令','资源条件'),
('S55 V66','二选一读适用方案，不要求两项都实验','方案走读或实测'),
('S54 V61','解释为何暂不使用某技术','场景适配与限制')]),
('综合验收与后续分支',[
('R0 I11 Q46 E91','固定任务/数据/模型/测量协议','协议版本'),
('I12 I11','baseline回归与质量检查','质量/性能记录'),
('Q46 C31 C41','择一个优化；不要求三个都做','唯一改变量'),
('P3 R2 N36','Profiler/时间线/运行路径归因','证据链'),
('R0','阶段验收；未完成正文与提纲分支另排','独立可复现程度与缺口')])]
days=[]
for wi,(title,rows) in enumerate(weeks,1):
    assert len(rows)==5
    for di,(ids,scope,evidence) in enumerate(rows,1):days.append({'day':(wi-1)*5+di,'week':wi,'weekday':di,'topic':title,'ids':ids.split(),'scope':scope,'evidence':evidence})
assert len(days)==120
# Curated concept routes; heading search below exposes all actual subsection titles.
concept_text='''shape / stride / 广播 / BMM|P2 P3|P2§2.1–2.7→P3§1|T3 T7 N33
Python对象 / 引用 / dataclass / 生成器|P1|§2.1–2.9|N32 N34 N35
C ABI / 指针 / 动态库 / 生命周期|P1|§4→§5.3–5.4→§6.2–6.4|C11 I21 E91
软件栈 / CUDA版本 / 环境 / 启动错误|P1 C11|P1§7–8→C11|D12 I12
Tokenization / BPE / Embedding / 词表|T9|先词表/Token ID/Embedding|T2 N33 S52
QKV / Attention / 缩放 / mask|T3 P2|T3§2–6；P2§9.2–9.3|T2 T7
GQA / MQA / MHA / MLA / KV头|T3|T3相关变体章节|T7 V62 N33
FFN / SwiGLU / GELU|T4|基础FFN→激活→门控|T7 N33
RoPE / ALiBi / 位置编码|T5|基础位置→RoPE|T9 N33
Norm / RMSNorm / LayerNorm / 残差|T6 P2|P2§7.4–7.8→T6|T7 N33
Decoder / 参数量 / FLOPs|T7 P2|P2§9.1/9.7→T7|T2 D11
自回归 / temperature / top-k / top-p|T8 P2|P2§5.1–5.5/5.9→T8|I11 N32
KV Cache / prefill / decode|T8 I11|T8§6→I11§1–2|T3 T7
TTFT / TPOT / ITL / E2E / goodput|I11|§3关键指标；先明确计时边界|R0 E91 S54 V66
量化 / scale / zero-point / 粒度 / PTQ / QAT|Q41 P2|P2§8→Q41§2–5|P3 Q46
W8A8 / INT8 / SmoothQuant / 异常值|Q42|Q41不懂先补→Q42等价缩放|Q43
GPTQ / Hessian / AWQ / Marlin / INT4|Q43 P2|P2§2.9/4.7/6.3/8.7→Q43|Q42 C41
FP8 / FP4 / MXFP4 / NVFP4|Q45 P2 P5|P2§8→Q45格式/缩放/执行|Q46
KV量化 / KIVI / FP8 KV|Q44 Q45|先Q45的FP8小节，再Q44|I11 T8
LoRA / rank / 低秩|P2|§2.10–2.13→§9.5|P3
loss / 交叉熵 / perplexity / KL|P2 P3|P2§5→P3训练循环|T8 Q46
梯度 / autograd / 反向传播|P2 P3|P2§6→P3§2|D31
AdamW / SGD / 优化器状态 / master weight|D31 P2|P2§7.1–7.3/8→D31|D11 P3
Dataset / DataLoader / checkpoint / train / eval|P3|§4.1–4.4|P1
SM / SIMT / Warp / thread / grid|P4 C12 C21|P4→C12→C21|R2
Roofline / 带宽 / 算术强度|P4 P2|P4§3.3与P2§3|I11 C41
内存层次 / shared / register|C13|P1指针/数组→C13|P4
coalescing / bank conflict / float4|C22|C13与C21→C22|C41 R2
occupancy / 资源分配|C23|寄存器/shared与warp→C23|C41 P4
同步 / 原子 / memory fence|C24|C13可见性与C21→C24|P1 C31
Reduce / shuffle / 浮点非结合|C31 P2|P2§8.4→C31|C21
GEMM / tiling / 分块矩阵|P2 C41|P2§2.6/3→C41|C22 C23
Softmax / LogSumExp / online合并|P2 C51 C52|P2§5.2–5.3→C51→C52；算例§9.4|T3
FlashAttention V1 / V2|C61 C62|T3＋C41＋C52→C61→C62|R2
Triton / tl.load / tl.store / fused|C71|不要求全部CUDA算法，补C13存储概念|C51 R2
Profiler / Nsight / benchmark|P3 R2|P3§6与R2工具章节；提纲不是完整工具课|OC8 C14
NVLink / IB / RoCE / RDMA / NCCL|P6 D12|硬件通信→分布式环境与启动|P4 V65
AllReduce / AllGather / ReduceScatter / All-to-All|P6 D21|先原语数据流，再通信量/代码|D41 V62 V64
rank / world_size / rendezvous / 进程组|D12 P1|P1§3.4/7/8→D12|P6
DDP / FSDP / ZeRO|D41 D42 D31|优化器状态＋原语→D41→D42；ZeRO完整系列仅提纲|OD5
TP / column / row / 词表并行|T4 V62 N33|T4线性切分→V62→N33实现|OD6 D21
PP / pipeline / 层切分|V63|推理PP正文；训练1F1B只有提纲|OD7 V61
MoE / router / EP / dispatch / combine|T4 V64|T4§8→V64；训练EP仍是提纲|OD10 D21
PagedAttention / 块表 / 引用计数|I21 N34|I11 KV→I21→N34|N36
Prefix Cache / 哈希 / RadixAttention|I23 N34|I21→I23→N34|T9
Continuous Batching / 抢占 / recompute|I22 N35|I11→I21→I22→N35|I24
Chunked Prefill / token budget|I24 N35|I22→I24→N35|N34 N36
CUDA Graph / 固定地址 / torch.compile|I25 N36|图优化概念→N36执行图；kernel原理补C61|P3 N33 R2
nano-vllm入口 / BlockManager / Scheduler / ModelRunner|N31 N32 N34 N35 N36|按入口→状态→调度→执行追踪；算子补N33|I21 I22 I24
投机 / 拒绝采样 / 保分布 / acceptance|S51 P2|P2§4–5→S51，不等于随机输出逐次相同|S54
Draft / N-gram / Suffix / tokenizer兼容|S52 T9|T9词表→S51→S52|S55
Medusa / EAGLE / MTP / tree / block verification|S53|S51验收＋T7结构→S53|S54
DCP / KV头复制 / 并行部署|V66 V62|区分推理DCP、训练CP与SP|OD9 V61
端侧 / 导出 / ExecuTorch / XNNPACK|E91|P3框架与P1构建→E91|Q41
GPU二维图像索引 / crop / resize|C12 P2|C12§7.1与P2shape；裁剪/resize完整算法是缺口|E91'''
concepts=[]
for line in concept_text.splitlines():
    name,ids,scope,review=line.split('|');concepts.append({'name':name,'ids':ids.split(),'scope':scope,'review':review.split()})
gaps=[('SFT / QLoRA / PEFT工程','P3 P2','数学LoRA和训练循环已有；模板/loss mask/packing/adapter完整训练无独立教程。'),('YOLO / mAP / IoU / 检测训练','P3 P2','通用训练和数学已有；检测标注/损失/匹配/mAP完整讲解未覆盖。'),('VLM / 图像编码器 / 图文评测','T3 T7 T8 I11','Transformer和推理可回补；视觉编码器/投影/图像token/任务评分未形成完整教程。'),('Q4_K_M / GGUF','Q41 Q43 E91','端侧运行时提及llama.cpp/GGUF；Q4_K_M本身无完整讲解。'),('Orin / JetPack / FPGA / VIC','P4 P5 E91 C12','只有GPU原理、端侧和二维索引；具体Orin/FPGA/VIC需真实型号专项文档。'),('训练SP / CP / EP / 1F1B / 3D','OD6 OD7 OD9 OD10 OD11','提纲已收录全部路径；相关推理正文不等价于训练完整实战。'),('PD解耦 / Kubernetes / HPA','OI7 OI8 I12 V65','只有提纲和部署基础，没有对应完整展开系列。'),('Cholesky / 阻尼 / GPTQ数学深化','P2 Q43','Hessian/逆矩阵/条件数已有；Cholesky系统推导没有独立课文。')]
for id,n in nodes.items():
    for edge in n['requires']:assert edge['id'] in nodes,(id,edge)
    for key in ['review','covers']:
        assert all(x in nodes for x in n[key]),(id,key)
seen=set();active=set()
def visit(id):
    assert id not in active,('cycle',id)
    if id in seen:return
    active.add(id)
    for e in nodes[id]['requires']:visit(e['id'])
    active.remove(id);seen.add(id)
for id in nodes:visit(id)
for d in days:assert all(id in nodes for id in d['ids'])
for n in nodes.values():
    n['path']='docs/guides/'+n['rel']
    n['href']='../'+n['path']
update_file=OUT/'plan_update.json'
plan_update=json.loads(update_file.read_text(encoding='utf-8')) if update_file.exists() else None
if plan_update:
    for day_id,override in plan_update['overrides'].items():
        days[int(day_id)-1].update(override)
        assert all(id in nodes for id in days[int(day_id)-1]['ids'])
DATA={'nodes':nodes,'days':days,'concepts':concepts,'gaps':gaps,'root':'docs/guides/','repository':'https://github.com/StarYYYzx/AIInfraGuide','plan_update':plan_update}
(OUT/'curriculum.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
payload=json.dumps(DATA,ensure_ascii=False).replace('</','<\\/')
TEMPLATE=r'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>AI Infra · 文档级学习图谱</title><style>
:root{color-scheme:dark;--bg:#101820;--panel:#18232e;--line:#354655;--text:#e5edf4;--muted:#a7b9c9;--blue:#8cc9f3;--teal:#91d8c5}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.65 "Microsoft YaHei",sans-serif}header,main{max-width:1440px;margin:auto;padding:24px 30px}header{padding-bottom:10px}h1{font-size:28px;font-weight:500;margin:4px 0}h2{font-size:20px;font-weight:500}h3{font-size:16px;font-weight:500}p{margin:8px 0}.muted,small{color:var(--muted)}a{color:var(--blue);overflow-wrap:anywhere}button,select,input{font:inherit;color:var(--text);background:#203140;border:1px solid var(--line);border-radius:7px;padding:7px 12px}button{cursor:pointer}button:hover,button.active{border-color:var(--blue);background:#29475d}input{min-width:260px}nav,.controls,.chips{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}.panel,.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px;margin:12px 0}.grid{display:grid;grid-template-columns:minmax(340px,1fr) minmax(450px,1.6fr);gap:20px}.card h3{margin:0 0 8px}.badge{font-size:12px;color:var(--teal);border:1px solid #446d64;border-radius:5px;padding:2px 6px;margin-right:6px}.file{font-size:13px;word-break:break-all}.hidden{display:none}table{border-collapse:collapse;width:100%}th,td{text-align:left;vertical-align:top;border-bottom:1px solid var(--line);padding:10px}th{color:var(--blue)}details{margin:12px 0}summary{cursor:pointer;color:var(--teal)}.scroll{overflow:auto}.callout{border-left:3px solid var(--teal);padding:10px 14px;background:#18312e;margin:12px 0}.map-row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.map-row .card{border-top:3px solid var(--blue)}svg text{fill:var(--text)}svg .node{cursor:pointer}svg .node:hover rect{stroke:#fff}#graph{max-height:740px;overflow:auto;background:#121e28;border-radius:9px;border:1px solid var(--line)}.path{display:block;font:12px/1.5 Consolas,monospace;color:var(--muted);margin:6px 0}.result{padding:10px 0;border-bottom:1px solid var(--line)}.toast{min-height:24px;color:var(--teal)}@media(max-width:900px){.grid,.map-row{grid-template-columns:1fr}header,main{padding:18px}input{min-width:200px}h1{font-size:23px}}@media print{nav,.controls,button{display:none}.hidden{display:block}body{background:white;color:black}.panel,.card{background:white}a{color:#185fa5}}
</style></head><body><header><span class="badge">本地课程核对 · 2026-11-16</span><h1>AI Infra · 自顶向下文档学习图谱</h1><p><a href="README.md">使用说明</a> · <a href="PROGRESS.md">真实学习进度</a> · <a href="progress.json">机器可读状态</a></p><p class="muted">本页是课程导航，不会自动保存或同步进度；选中学习日不等于完成。以progress.json及会话证据为准。</p><p class="muted">先带着系统问题读目标课文；遇到概念缺口，沿依赖回补指定小节，再回到原文。课程为主线，周末不学。</p><nav><button data-tab="daily" class="active">120学习日</button><button data-tab="graphpage">依赖知识图谱</button><button data-tab="conceptpage">概念补课索引</button><button data-tab="catalogpage">全部102篇课文</button><button data-tab="rulespage">使用规则与课程缺口</button></nav></header><main>
<section id="daily"><div class="controls"><label>主题周 <select id="week"></select></label><label>学习日 <select id="day"></select></label><button id="prev">上一日</button><button id="next">下一日</button></div><div class="callout">时间灵活，75分钟仅参考，不固定计时/报告超支。最新安排见 <a href="PLAN_UPDATE_2026-11-17.md">11-17更新</a>：Day1回补优先→指标验收→环境核对→最小推理；前置未过就顺延，不借用周末。首读列按顺序；概览与精读的门槛不同，不需要先学完所有祖先才能看系统地图。</div><div id="dailycontent"></div></section>
<section id="graphpage" class="hidden"><div class="map-row"><div class="card"><h3>① 系统问题</h3><p>推理、评测、训练、资源约束</p><button onclick="focusNode('I11')">从推理1.1出发</button></div><div class="card"><h3>② 模型与计算</h3><p>Tensor、数学、Transformer</p><button onclick="focusNode('T7')">从Decoder出发</button></div><div class="card"><h3>③ 执行与通信</h3><p>CUDA、算子、集合通信</p><button onclick="focusNode('C61')">从FlashAttention出发</button></div><div class="card"><h3>④ 优化与交付</h3><p>引擎、量化、端侧、并行</p><button onclick="focusNode('Q43')">从INT4/GPTQ出发</button></div></div><div class="controls"><label>目标课文 <select id="target"></select></label><label>展开 <select id="depth"><option value="1">直接前置</option><option value="2" selected>两层前置</option><option value="99">全部递归前置</option></select></label><button id="draw">更新图谱</button></div><p class="muted">箭头方向：<strong>当前目标 → 需要回补的前置</strong>。实线是建议的核心前置；虚线是辅助复习。前置边的小节与原因列在图下，不能误解为整篇必读。灰蓝提纲不冒充正文。</p><div id="graph"></div><div id="nodedetail"></div><div id="edgeinfo"></div></section>
<section id="conceptpage" class="hidden"><h2>遇到不懂的概念：先查这里</h2><input id="conceptquery" placeholder="例如 KV、Hessian、LoRA、stride、Orin"><p class="muted">整理了核心概念的优先补课链，并可检索全部课文的真实二至四级标题。辅助复习只作补充，不反向当作硬前置。</p><div id="conceptresults"></div><h3>真实小节标题检索</h3><div id="headingresults"></div></section>
<section id="catalogpage" class="hidden"><h2>完整课程目录与文件级前置</h2><div class="controls"><input id="catalogquery" placeholder="文件名、ID、概念或路径"><select id="kind"><option value="">全部类型</option><option>正文</option><option>概览</option><option>导航</option><option>提纲</option></select></div><p class="muted">102个Markdown＝67篇正文＋2篇综合概览＋1篇路线导航＋32篇章节提纲。课程根目录：<span id="rootpath"></span>。不包括面试题，不把图片/代码块当作本地可运行工程。</p><div id="catalogresults"></div></section>
<section id="rulespage" class="hidden"><div class="panel"><h2>怎么使用，而不是再次铺开资料海</h2><ol><li>先选今天的学习日，只按首读顺序读限定范围。</li><li>遇到概念卡点，查补课索引；进入相关文档的小节，不默认通读整篇。</li><li>点击“全部递归前置”可列出本课程内上游所有文件；只补不懂的部分。</li><li>回到原目标，做当天一项验收。不能独立解释，就下一工作日接续。</li><li>每天汇报：问题→解释/推导→证据→未知项→下一工作日。已读、能解释、练习通过、实测通过分开。</li></ol><p>工作日时间灵活，75分钟仅参考，不固定计时/报告超支；周末与节假日休息。早晨汇报上一工作日，周一材料周五准备。学习日按实际验收顺延，日期只是槽位；当前Day1先执行11-17回补覆盖，不把培训Day等同学习Day。</p><p><strong>性质说明：</strong>这是根据实际课文概念编排的教学依赖图，不是仓库官方引用图，也不是作者明确声明的先修表。页面自动提取真实标题和路径；依赖与日序为人工教学编排。先导概览允许先读，深入证明/代码再回补，避免“全学完基础才看系统”的死锁。</p></div><div id="gaps"></div><div class="panel"><h3>需要注意的目录与引用</h3><ul><li>PyTorch实际目录拼写为 <code>pyroch</code>。</li><li>编程、数学的“第N章”文件有完整正文，不能一律跳过。</li><li>Tokenization 3.9在输入层应提前补；原文“3.6位置编码”旧引用对应真实3.5，而3.6是Norm。</li><li>FP8 KV的小节可先补4.5 FP8基础；GPTQ卡点需要Hessian/逆矩阵/相关性，不只是位宽。</li><li>nano-vllm不是生产vLLM完整功能集；有chunked prefill不等于混合统一调度。</li><li>本目录未提供独立.py/.cu实验工程；正文代码、外部仓库与实际实验是三种素材。</li><li>服务器与新板具体型号、支持格式、运行时、权限未确认。不预设多卡、JetPack或FP4原生支持。</li></ul></div></section><div id="toast" class="toast" role="status"></div>
</main><script id="dataset" type="application/json">__DATA__</script><script>
const DATA=JSON.parse(document.getElementById('dataset').textContent),N=DATA.nodes,$=id=>document.getElementById(id);let current=1;
const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
function switchTab(id){document.querySelectorAll('main>section').forEach(x=>x.classList.toggle('hidden',x.id!==id));document.querySelectorAll('nav button').forEach(x=>x.classList.toggle('active',x.dataset.tab===id))}
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>switchTab(b.dataset.tab));
function filelink(id){const n=N[id];return `<a href="${encodeURI(n.href)}" title="${esc(n.path)}">${esc(id+' · '+n.name)}</a> <a target="_blank" rel="noopener" href="${DATA.repository+'/blob/main/'+encodeURI(n.path)}">GitHub</a>`}
function chip(id){return `<button onclick="focusNode('${id}')">${esc(id+' '+N[id].name.replace(/^\d+[.\d]*[- ]?/,''))}</button>`}
async function copyPath(id){try{await navigator.clipboard.writeText(N[id].path);$('toast').textContent='已复制路径：'+N[id].path}catch(e){$('toast').textContent='浏览器未授权剪贴板，请从显示的完整路径手动复制：'+N[id].path}}
function ancestors(id){let s=new Set();function walk(x){for(const e of N[x].requires){if(!s.has(e.id)){s.add(e.id);walk(e.id)}}}walk(id);return [...s]}
function topo(ids){let result=[],seen=new Set(),set=new Set(ids);function rec(x){if(seen.has(x))return;seen.add(x);for(const e of N[x].requires)if(set.has(e.id))rec(e.id);result.push(x)}ids.forEach(rec);return result}
function docCard(id,expanded=false){let n=N[id];return `<div class="card"><span class="badge">${esc(n.kind)}</span>${filelink(id)} <button onclick="copyPath('${id}')">复制路径</button><span class="path">${esc(n.path)}</span>${n.note?'<p>'+esc(n.note)+'</p>':''}<p>直接前置：${n.requires.length?n.requires.map(e=>filelink(e.id)+' <small>（'+esc(e.why)+'）</small>').join('；'):'无课程内硬前置'}</p>${n.review.length?'<p>辅助复习：'+n.review.map(filelink).join('；')+'</p>':''}${n.covers.length?'<p>提纲对应正文：'+n.covers.map(filelink).join('；')+'</p>':''}<details ${expanded?'open':''}><summary>本篇真实小节标题（'+n.headings.length+'项）</summary>${n.headings.map(h=>`<div style="margin-left:${(h.level-2)*16}px"><small>L${h.line}</small> ${esc(h.title)}</div>`).join('')}</details><button onclick="focusNode('${id}')">查看依赖图与全部上游</button></div>`}
for(let w=1;w<=24;w++)$('week').innerHTML+=`<option value="${w}">W${w} · ${esc(DATA.days[(w-1)*5].topic)}</option>`;
for(let d=1;d<=5;d++)$('day').innerHTML+=`<option value="${d}">D${d} · 周${'一二三四五'[d-1]}槽位</option>`;
function renderDay(){const d=DATA.days[current-1];$('week').value=d.week;$('day').value=d.weekday;let upstream=topo([...new Set(d.ids.flatMap(ancestors))]);$('dailycontent').innerHTML=`<div class="panel"><span class="badge">学习日 ${d.day}/120 · W${d.week} D${d.weekday}</span><h2>${esc(d.topic)}</h2><p><strong>首读顺序：</strong>${d.ids.map((id,i)=>`<span>${i+1}. ${filelink(id)}</span>`).join(' → ')}</p><p><strong>只读范围：</strong>${esc(d.scope)}</p><p><strong>下次汇报证据：</strong>${esc(d.evidence)}</p><p class="muted">这是任务安排，不是已经完成的结果；训练/微调/性能必须有实际证据才标实测。</p><div class="chips">${d.ids.map(chip).join('')}</div><details><summary>今天这些目标的全部课程内递归前置（${upstream.length}篇）</summary><p>以下按基础到目标的参考顺序列全；不是今天需要全读。优先依据概念索引及直接边的小节回补。</p>${upstream.map(id=>docCard(id)).join('')}</details></div><h3>首读文档与小节目录</h3>${d.ids.map(id=>docCard(id)).join('')}`}
$('week').onchange=()=>{current=(+$('week').value-1)*5+1;renderDay()};$('day').onchange=()=>{current=(+$('week').value-1)*5+(+$('day').value);renderDay()};$('prev').onclick=()=>{current=Math.max(1,current-1);renderDay()};$('next').onclick=()=>{current=Math.min(120,current+1);renderDay()};
Object.values(N).forEach(n=>$('target').innerHTML+=`<option value="${n.id}">${esc(n.id+' · '+n.name+' ['+n.kind+']')}</option>`);$('target').value='I11';
function focusNode(id){switchTab('graphpage');$('target').value=id;drawGraph();$('graphpage').scrollIntoView({behavior:'smooth',block:'start'})}
function drawGraph(){const target=$('target').value,max=+$('depth').value,levels=new Map([[target,0]]),edges=[],queue=[target];while(queue.length){let x=queue.shift(),l=levels.get(x);if(l>=max)continue;for(let e of N[x].requires){edges.push({from:x,to:e.id,why:e.why});if(!levels.has(e.id)){levels.set(e.id,l+1);queue.push(e.id)}}}for(const r of N[target].review){if(!levels.has(r))levels.set(r,1)}let groups=[];for(let [id,l]of levels){(groups[l]??=[]).push(id)}const width=Math.max(1080,...groups.map(a=>a.length*224+40)),height=groups.length*126+100,pos={};groups.forEach((a,l)=>a.forEach((id,i)=>pos[id]={x:(width-a.length*224)/2+i*224+12,y:30+l*126}));let svg=`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" role="img" aria-label="目标课文向下回补前置依赖图"><defs><marker id="arr" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1L9 5L1 9" fill="none" stroke="#72a6cf"/></marker></defs>`;for(let e of edges){let a=pos[e.from],b=pos[e.to];svg+=`<path d="M${a.x+100} ${a.y+72} C${a.x+100} ${a.y+100},${b.x+100} ${b.y-25},${b.x+100} ${b.y}" fill="none" stroke="#49667d" stroke-width="1" marker-end="url(#arr)"><title>${esc(e.from+' → '+e.to+'：'+e.why)}</title></path>`}for(let [id,p] of Object.entries(pos)){let name=N[id].name.replace(/^\d+[.\d]*[- ]?/,''),lines=[name.slice(0,13),name.slice(13,26),name.slice(26,39)].filter(Boolean);svg+=`<g class="node" tabindex="0" role="button" onclick="focusNode('${id}')" onkeydown="if(event.key==='Enter')focusNode('${id}')"><rect x="${p.x}" y="${p.y}" width="200" height="72" rx="7" fill="${id===target?'#194c60':N[id].kind==='提纲'?'#35404a':'#203343'}" stroke="${id===target?'#91d8c5':'#698399'}"/><text x="${p.x+10}" y="${p.y+19}" font-size="12">${esc(id+' · '+N[id].kind)}</text>${lines.map((s,i)=>`<text x="${p.x+10}" y="${p.y+38+i*14}" font-size="12">${esc(s)}</text>`).join('')}<title>${esc(N[id].path)}</title></g>`}for(let r of N[target].review){if(!pos[r])continue;let a=pos[target],b=pos[r];svg+=`<path d="M${a.x+190} ${a.y+40}L${b.x+190} ${b.y+40}" fill="none" stroke="#91d8c5" stroke-dasharray="4 5" opacity=".6"/>`}svg+='</svg>';$('graph').innerHTML=svg;$('nodedetail').innerHTML=docCard(target);let all=topo(ancestors(target));$('edgeinfo').innerHTML=`<details open><summary>图中的依赖边与回补小节（${edges.length}条）</summary><table><thead><tr><th>目标</th><th>先补课文</th><th>限定内容/原因</th></tr></thead><tbody>${edges.map(e=>`<tr><td>${filelink(e.from)}</td><td>${filelink(e.to)}</td><td>${esc(e.why)}</td></tr>`).join('')}</tbody></table></details><details><summary>全部递归前置：${all.length}篇（基础到目标参考顺序）</summary>${all.map(id=>docCard(id)).join('')}</details>`}
$('draw').onclick=drawGraph;$('target').onchange=drawGraph;$('depth').onchange=drawGraph;
function renderConcept(){let q=$('conceptquery').value.trim().toLowerCase(),cs=DATA.concepts.filter(c=>(c.name+' '+c.scope).toLowerCase().includes(q));$('conceptresults').innerHTML=cs.map(c=>`<div class="card"><h3>${esc(c.name)}</h3><p><strong>优先补课：</strong>${c.ids.map(filelink).join(' → ')}</p><p>${esc(c.scope)}</p><p class="muted">辅助/实现对照：${c.review.map(filelink).join('；')}</p><div class="chips">${c.ids.map(chip).join('')}</div></div>`).join('');let matches=[];if(q)for(let n of Object.values(N)){let hs=n.headings.filter(h=>h.title.toLowerCase().includes(q));if(hs.length)matches.push(`<div class="result">${filelink(n.id)} <span class="badge">${esc(n.kind)}</span>${hs.map(h=>'<div><small>L'+h.line+'</small> '+esc(h.title)+'</div>').join('')}</div>`)}$('headingresults').innerHTML=q?(matches.join('')||'<p>没有匹配的真实小节标题；不代表正文完全没提及，请查看课程缺口与全文。</p>'):'<p class="muted">输入关键词后检索全部102篇文件的真实小节标题，不截断结果。</p>';let gs=DATA.gaps.filter(g=>!q||(g[0]+' '+g[2]).toLowerCase().includes(q));if(gs.length)$('conceptresults').innerHTML+=`<h3>相关课程缺口</h3>${gs.map(g=>gapCard(g)).join('')}`}
function gapCard(g){return `<div class="card"><h3>${esc(g[0])}</h3><p>${esc(g[2])}</p><p>已有相关基础（不是完整专项）：${g[1].split(' ').map(filelink).join('；')}</p></div>`}
$('conceptquery').oninput=renderConcept;
function catalog(){let q=$('catalogquery').value.toLowerCase(),k=$('kind').value,list=Object.values(N).filter(n=>(!k||k===n.kind)&&[n.id,n.name,n.rel,...n.headings.map(h=>h.title)].join(' ').toLowerCase().includes(q));$('catalogresults').innerHTML=`<p>显示 ${list.length} / 102 篇</p>`+list.map(n=>docCard(n.id)).join('')}
$('catalogquery').oninput=catalog;$('kind').onchange=catalog;$('rootpath').textContent=DATA.root;$('gaps').innerHTML='<h2>目录内有基础，但没有完整专题的地方</h2>'+DATA.gaps.map(gapCard).join('');renderDay();drawGraph();renderConcept();catalog();
</script></body></html>'''
OUT.mkdir(exist_ok=True)
(OUT/'2026-11-16_AIInfra_文档级学习知识图谱.html').write_text(TEMPLATE.replace('__DATA__',payload),encoding='utf-8')
# Plain-text companion for stable reading and searching in the editor.
md=['# AI Infra 文档级学习导航与前置依赖（2026-11-16）','', '> 最新120学习日细化版；课程为主，周末不学。图谱是教学依赖建议，不是仓库官方引用图。', '', '可视化入口：[交互知识图谱](2026-11-16_AIInfra_文档级学习知识图谱.html)','', '## 使用顺序','', '1. 看当天首读及范围；2. 概念卡住查补课索引；3. 只补对应小节；4. 返回目标验收；5. 下次导师汇报一项真实证据。', '时间灵活，75分钟仅参考，不固定计时或报告超支。最新覆盖见[11-17更新](PLAN_UPDATE_2026-11-17.md)，Day1回补优先，前置不过按工作日顺延，周一材料周五备好。', '深入理解的前置不阻止先导概览。上游列表不代表全部要精读，不代表每天读完一篇。','', '## 一、全部课程文档ID（102篇）','', '67正文＋2概览＋1导航＋32提纲。只纳入docs/guides，不把面试/图片/正文代码块当完整本地课程或可运行脚本。']
def ml(id):return f"[{id} · {nodes[id]['name']}]({quote(nodes[id]['href'],safe='/')})"
for id,n in nodes.items():md+=['',f"### {id} · {n['name']} [{n['kind']}]",f"- 文档：{ml(id)}",f"- 相对课程根路径：`{n['rel']}`",'- 直接前置：'+('；'.join(ml(e['id'])+'：'+e['why'] for e in n['requires']) or '无课程内硬前置'),'- 辅助复习：'+('；'.join(ml(x) for x in n['review']) or '无额外指定')]+(['- 提纲对应正文：'+'；'.join(ml(x) for x in n['covers'])] if n['covers'] else [])+(['- 注意：'+n['note']] if n['note'] else [])
md+=['','## 二、每天首读文档、限定范围与汇报证据','']
for wi,(title,_) in enumerate(weeks,1):
    md+=['',f'### 第{wi}主题周：{title}','']
    for d in days[(wi-1)*5:wi*5]:
        md += [f"#### 学习日{d['day']} / W{wi}D{d['weekday']}（周{'一二三四五'[d['weekday']-1]}槽位）",'- 首读顺序：'+' → '.join(ml(x) for x in d['ids']),'- 限定范围：'+d['scope'],'- 下次汇报证据：'+d['evidence'],'- 当天目标直接回补：'+'；'.join(ml(e['id'])+'（'+e['why']+'）' for id in d['ids'] for e in nodes[id]['requires']) if any(nodes[id]['requires'] for id in d['ids']) else '- 当天目标直接回补：按实际卡点查概念索引。','']
md+=['','## 三、核心概念补课与复习索引','']
for c in concepts:md += [f"### {c['name']}",'- 优先：'+' → '.join(ml(x) for x in c['ids']),'- 小节：'+c['scope'],'- 辅助/对照：'+'；'.join(ml(x) for x in c['review']),'']
md+=['','## 四、课内缺口（有相关基础不等于有完整专题）','']
for name,ids,note in gaps:md += ['### '+name,note,'相关已有文件：'+'；'.join(ml(x) for x in ids.split()),'']
md+=['','## 五、主干依赖图（目标向下回补）','','```mermaid','flowchart TD','  I11[推理1.1] --> T8[自回归3.8]','  T8 --> T7[Decoder3.7]','  T7 --> T3[Attention3.3]','  T7 --> T4[FFN3.4]','  T7 --> T5[位置3.5]','  T7 --> T6[Norm3.6]','  T7 --> T9[Tokenization3.9]','  T3 --> P2[数学基础]','  T3 --> P3[PyTorch]','  P3 --> P1[编程基础]','  I11 --> P4[GPU基础]','  Q43[INT4/GPTQ4.3] --> Q41[量化4.1]','  Q43 --> P2','  Q41 --> P2','  C61[FlashAttention6.1] --> C41[GEMM4.1]','  C61 --> C52[OnlineSoftmax5.2]','  C61 --> T3','  C52 --> C51[Softmax5.1]','  C51 --> C31[Reduce3.1]','  C31 --> C24[同步2.4]','  C31 --> C22[访存2.2]','  C22 --> C13[内存1.3]','  C13 --> C12[编程模型1.2]','  D42[DDP/FSDP4.2] --> D41[数据并行4.1]','  D41 --> D21[通信原语2.1]','  D41 --> D31[优化器3.1]','  D21 --> P6[通信基础]','  N36[ModelRunner3.6] --> N35[Scheduler3.5]','  N35 --> N34[BlockManager3.4]','  N34 --> I21[PagedAttention2.1]','  N36 --> N33[模型算子3.3]','  N33 --> T7','  N33 --> C71[Triton7.1]','```','', '这张图仅为主干，不替代完整前置表；交互页可展开每一篇的全部递归前置。文件内小节依赖不要求整篇先读，复习边与提纲覆盖边不参与硬前置排序。','', '## 六、完整真实小节标题（按文件；行号用于定位）','']
for id,n in nodes.items():
    md += [f"### {id} · {n['name']}"]+[f"- L{h['line']} {'  '*(h['level']-2)}{h['title']}" for h in n['headings']]+['']
(OUT/'2026-11-16_AIInfra_逐日文档与概念回补索引.md').write_text('\n'.join(md),encoding='utf-8')
print(json.dumps({'files':len(nodes),'body':sum(n['kind']=='正文' for n in nodes.values()),'outline':sum(n['kind']=='提纲' for n in nodes.values()),'days':len(days),'concept_routes':len(concepts),'heading_count':sum(len(n['headings']) for n in nodes.values()),'requires_edges':sum(len(n['requires']) for n in nodes.values()),'dag_valid':True,'outputs':['2026-11-16_AIInfra_文档级学习知识图谱.html','2026-11-16_AIInfra_逐日文档与概念回补索引.md']},ensure_ascii=False))
