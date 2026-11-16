"""Export presentation and manuscript versions of the frozen protocol. No API calls."""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

OUT = Path(__file__).resolve().parents[1] / 'figures'
OUT.mkdir(exist_ok=True)
for font_path in (OUT / 'fonts').glob('Montserrat-*.ttf'):
    if 'Variable' not in font_path.name:
        font_manager.fontManager.addfont(font_path)
plt.rcParams.update({'font.family':'Montserrat', 'pdf.fonttype':42, 'svg.fonttype':'path'})
INK='#182434'; BLUE='#EAF1FA'; GOLD='#FFF2D7'; PURPLE='#F0EBF9'; TEAL='#E8F4F1'

def setup(w,h):
    fig,ax=plt.subplots(figsize=(w,h)); fig.patch.set_facecolor('white')
    fig.subplots_adjust(0,0,1,1); ax.set_xlim(0,100); ax.set_ylim(0,100); ax.axis('off')
    return fig,ax

def box(ax,x,y,w,h,title,body,fill=BLUE,size=11):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.0,rounding_size=1',facecolor=fill,edgecolor='#9AA9BA',linewidth=.85))
    ax.text(x+1.6,y+h-2,title,va='top',fontsize=size+1,fontweight='bold',color=INK)
    ax.text(x+1.6,y+h-6,body,va='top',fontsize=size,linespacing=1.5,color=INK)

def arrow(ax,a,b,label=None):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=13,linewidth=1.1,color='#52647B',connectionstyle='arc3'))
    if label: ax.text((a[0]+b[0])/2,(a[1]+b[1])/2+.8,label,fontsize=9,ha='center',color=INK)

def save(fig,name):
    for ext in ['png','pdf','svg']: fig.savefig(OUT/f'{name}.{ext}',dpi=300,facecolor='white')
    plt.close(fig)

fig,ax=setup(16,11)
ax.text(4,96,'Balanced but Misleading',fontsize=28,fontweight='bold',color=INK,va='top')
ax.text(4,90.8,'Can epistemic scores miss decision-changing omissions?',fontsize=16,color='#52647B',va='top')
ax.text(4,85.6,'FROZEN DEVELOPMENT PROTOCOL  |  Six families  |  Independent validation remains outstanding',fontsize=11,color='#8A5E14',va='top')
box(ax,4,62,28,19,'01  Prepare the cases','6 fictional lease / job-offer cases\nFact IDs, two contexts, explicit rules\nFinite domains and derived objectives\n26 software tests passed',BLUE)
box(ax,36,62,28,19,'02  Freeze the configuration','Verify routes and request caps\nRecord launch authorization\nFreeze source, data and job hashes\nRetain prior failed screen versions',GOLD)
box(ax,68,62,28,19,'03  Competence screen','42 full-evidence calls: 3 models\n14 items each, including neither / ties\nRequire valid, correct initial answers\nFailure → stop; pass → separate go',GOLD)
arrow(ax,(32,71.5),(36,71.5)); arrow(ax,(64,71.5),(68,71.5))
arrow(ax,(82,62),(82,56),'Approved')
box(ax,68,35,28,21,'04  Generate briefings','DeepSeek writer (Flash 1017)\nNeutral / promotional / balance arms\n3 draws per case and condition\nSelect n−2 facts; fixed source order\nAdd matched random + full controls',PURPLE)
box(ax,36,35,28,21,'05  Paired evaluation','Same briefing in both contexts\nOnly one requirement / parameter differs\n3 receiver models; 2 repetitions\nNemotron 3.5 Super VL detector\nCoverage / checklist / topic baselines',PURPLE)
box(ax,4,35,28,21,'06  Score outcomes','Primary: incorrect commitment\nSecondary: constraint violation\nSeparate clarify, defer and neither\nAccept any tied optimum\nOmitted-only detector false alarms',TEAL)
arrow(ax,(68,45.5),(64,45.5)); arrow(ax,(36,45.5),(32,45.5)); arrow(ax,(18,35),(18,29))
box(ax,4,9,44,20,'07  Analyse and report','Per-context descriptive contrasts across six families\nRetain failures, unresolved outputs and all attempts\nVerified tables / figures → paper + GitHub supplement\nDevelopment evidence only; no generalization claim',TEAL)
box(ax,52,9,44,20,'Frozen run and model roles','54 writer jobs + 936 receiver + 312 detector jobs\nReceivers: DeepSeek V4.1 Flash 1017,\nGLM-5.3-Flash and Nemotron 3.5 Super VL\nOne writer retry; interrupted requests retained.',BLUE)
ax.text(4,4,'Repeated outputs are not independent scenarios. Consult the report for completion and failure counts.',fontsize=10,color='#52647B')
save(fig,'pipeline-share')

fig,ax=setup(11.8,7.1)
ax.text(3,97,'Experimental pipeline',fontsize=17,fontweight='bold',color=INK,va='top')
ax.text(3,91,'Six fictional development cases; paired contexts differ in one requirement or parameter.',fontsize=10,color='#52647B',va='top')
box(ax,3,65,28,20,'1. Formal specification','Source facts + formal decision rules\nFinite domains + derived objectives\nIndependent validation outstanding',BLUE,9)
box(ax,36,65,28,20,'2. Full-evidence screen','3 models × 14 items = 42 calls\nValid / correct initial responses\nSeparate approval before collection',GOLD,9)
box(ax,69,65,28,20,'3. Fact selection','Recipient-blind writer; n−2 facts\nNeutral / promotional / balance arms\n3 draws per case and condition',PURPLE,9)
arrow(ax,(31,75),(36,75)); arrow(ax,(64,75),(69,75)); arrow(ax,(83,65),(83,57))
box(ax,69,35,28,22,'4. Briefing controls','Verbatim facts in source order\nValence-count-matched random\nand full-evidence controls\nIdentical briefing in both contexts',PURPLE,9)
box(ax,36,35,28,22,'5. Evaluate and score','3 receivers × 2 repetitions\nScoped detector + simple baselines\nPrimary: incorrect commitment\nClarify / defer / neither kept separate',TEAL,9)
box(ax,3,35,28,22,'6. Descriptive analysis','Report each context separately\nRetain failures and all attempts\nDetector false alarms: harmless\nomitted facts only',TEAL,9)
arrow(ax,(69,46),(64,46)); arrow(ax,(36,46),(31,46))
ax.text(3,27,'INFORMATION BOUNDARY',fontsize=9,fontweight='bold',color=INK)
ax.text(3,22,'Receivers: briefing, shared premises and rule. Detector: full source facts and declared domains.\nNeither receives answer labels; the writer receives no recipient context.',fontsize=9.5,linespacing=1.5,color=INK)
ax.text(3,10,'54 writer jobs + 936 receiver jobs + 312 detector jobs. One writer retry is preserved in the evidence.',fontsize=9,color='#52647B')
ax.text(3,5,'Six development families; the diagram describes the method. Outcomes and unresolved requests are reported separately.',fontsize=9,color='#52647B')
save(fig,'pipeline-paper')
print('Created pipeline-share and pipeline-paper in PNG, PDF and SVG.')
