from pathlib import Path
import json,hashlib,re
from html import escape as esc
ROOT=Path(__file__).resolve().parents[2];R=ROOT/'records/runs/attention-v3-001'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
s=json.loads((R/'state.json').read_text());assert s.get('gate2_approval',{}).get('sample_sha256')==h(ROOT/'attention-v3-sample.html')
M=ROOT/'content/v3/manuscript.json'
assert not s.get('independent_reviews_pending',False), 'New manuscript reviews are pending'
review_files=s['independent_reviews'];assert len(review_files)==2
for name in review_files:
 r=json.loads((R/name).read_text());assert r['result']=='pass' and all(i.get('blocking',True) is False for i in r.get('issues',[])) and r['input_sha256']==h(M)
assert all(h(ROOT/p)==v for p,v in json.loads((R/'sample-inputs.json').read_text())['wiki_hashes'].items())
data=json.loads(M.read_text());pages=data['pages']
def e(t):return esc(str(t))
def refs(p):return '<p class="sources">來源：'+''.join(f'<a href="#ref-{n}" data-source="{n}">[{n}]</a>' for n in p['references'])+'</p>' if p['references'] else ''
def block(b,cls='text-block'):return '<article class="'+cls+'"><h2>'+e(b['label'])+'</h2><p>'+e(b['text'])+'</p></article>'
def route(stage):
 stages=['選擇','分配','處理','回到生活'];active=stages.index(stage) if stage in stages else None
 return '<ol class="route" aria-label="課程主線">'+''.join('<li'+(' class="current" aria-current="step"' if i==active else ' class="read"' if (active is not None and i<active) or stage=='全程回顧' else '')+'>'+n+'</li>' for i,n in enumerate(stages))+'</ol>'
def head(p):return route(p['stage'])+'<p class="eyebrow">'+('注意力的極限' if p['id']==0 else '資料與查證' if p['id']==15 else e(p['stage']))+'</p><h1>'+e(p['title'])+'</h1><p class="lead">'+e(p['main_message'])+'</p><p class="content-p">'+e(p['explanation'])+'</p>'
def example(p):
 x=p.get('example');return '<aside class="reader-example"><h2>'+e(x['label'])+'</h2><p>'+e(x['text'])+'</p></aside>' if x else ''
def closing(p):return '<p class="closing">'+e(p['closing'])+'</p>'+refs(p)
def resultsection(kind):
 if kind=='switch':return '<section id="results" class="results" aria-live="polite"><h2>這次作答告訴你什麼？</h2><div id="result-grid" class="result-grid"><p class="stat-empty">尚未完成兩輪，可以回到上一頁體驗，或先讀這頁的解讀原則。</p></div><p id="interpret" class="interpret" hidden></p></section>'
 return '<section id="st-results" class="results" aria-live="polite"><h2>你這一輪的結果</h2><div id="st-result-grid" class="result-grid"><p class="stat-empty">尚未完成Stroop體驗；仍可先讀如何理解差值。</p></div><p id="st-interpret" class="interpret" hidden></p></section>'
# Reuse the approved sample's actual two page layouts, not a reconstruction.
sample=(ROOT/'attention-v3-sample.html').read_text();samplemain=sample.split('<main>',1)[1].split('</main>',1)[0]
p6,p8=samplemain.split('<section class="slide" id="sample8"',1)
p6=p6.replace('id="sample6"','id="p06"')
p8='<section class="slide" id="sample8"'+p8
p8=p8.replace('id="sample8"','id="p08"')
p8=re.sub(r'<section id="results".*?</section>','',p8,flags=re.S)
p8=p8.replace('<button id="skip">先跳過，看解讀</button>','<button id="skip">先跳過，看解讀</button><button id="sw-view-result" class="result-link" hidden>查看本輪結果</button>')
p8=p8.replace('先練習；說明與題間停頓不計入作答時間。','先練習；說明與題間停頓不計入作答時間。完成後到下一頁讀結果。')
sections=[]
for p in pages:
 i=p['id'];bs=p['blocks'];pid='cover' if i==0 else 'sources' if i==15 else f'p{i:02}'
 if i==6:sections.append(p6.replace('id="p06"','data-layout="dual-timeline" id="p06"'));continue
 if i==8:sections.append(p8.replace('id="p08"','data-layout="interactive-switch" id="p08"'));continue
 top=head(p);mid=''
 if i==0:mid='<div class="hero"><p class="spotlight">'+e(p['closing'])+'</p><div class="chapter-map">'+''.join('<div class="chapter-node"><h2>'+t+'</h2><p>'+txt+'</p></div>' for t,txt in [('選擇','資訊太多，先優先理解其中一部分。'),('分配','多項任務是同時做，還是來回切換？'),('處理','選好目標後，無關資訊仍可能干擾反應。')])+'</div><button class="primary" data-go="1">開始閱讀</button></div>'
 elif i==1:
  mid='<div class="prediction">'+block(bs[0])+'<div class="choice-buttons"><button data-reveal="prediction-reveal">我覺得會</button><button data-reveal="prediction-reveal">不一定</button></div><div id="prediction-reveal" class="reveal" hidden>'+block(bs[1])+'</div></div>'
 elif i in [2,13]:mid='<div class="chapter-map '+('integration' if i==13 else '')+'">'+''.join(block(b,'chapter-node') for b in bs)+'</div>'
 elif i==3:mid='<div class="listening">'+block(bs[0])+'<div class="block-stack">'+''.join(block(b) for b in bs[1:])+'</div></div>'
 elif i==4:
  mid='<div class="key-stat"><strong>46%</strong><span>192人、跨16個條件，未察覺意外事件的比例；不是所有版本的固定比例。</span></div><div class="study-grid">'+''.join(block(b,'study-step') for b in bs)+'</div>'
 elif i==5:mid='<div class="misconceptions">'+''.join(block(b) for b in bs)+'</div>'
 elif i==7:mid='<div class="research-story"><aside class="research-sidebar"><strong>2001</strong><span>依APA研究解說轉述</span></aside><div class="block-stack">'+''.join(block(b) for b in bs)+'</div></div>'
 elif i==9:mid='<div class="result-layout">'+resultsection('switch')+'<div class="block-stack">'+''.join(block(b) for b in bs)+'</div></div><details><summary>想知道切換體驗的計分細節？</summary><p>兩輪各12題；完整完成、無逾時、正確題數相同且各至少10題才比較。每題等待作答時間加總，不含說明及題間停頓。這是活動門檻，不是研究常模。</p></details><button data-go="8">返回切換體驗</button>'
 elif i==10:mid='<div class="origin-pair"><aside class="color-demonstration"><span class="word">紅</span><p>墨色是藍，字義是紅。<br>若規則要求墨色，應回答「藍」。</p><p class="fine">中文教學改編示意</p></aside><div class="block-stack">'+''.join(block(b) for b in bs)+'</div></div>'
 elif i==11:
  mid='<div class="game-view"><div class="intro-grid">'+''.join(block(b) for b in bs)+'</div><div class="experiment stroop-board"><div class="exp-top"><span id="st-count">4題練習，24題正式題</span><span class="rule">回答墨色</span></div><div class="stimulus" id="st-stimulus" aria-live="polite">—</div><div class="answers">'+''.join(f'<button data-st-answer="{j}" disabled>{color}<kbd>{j+1}</kbd></button>' for j,color in enumerate(['紅','藍','綠','紫']))+'</div><p id="st-status" class="status" aria-live="polite">先看操作說明，再開始練習。</p><div class="actions"><button id="st-start" class="primary">開始練習</button><button id="st-skip">跳過，看解讀</button><button id="st-view-result" hidden>查看本輪結果</button></div></div><details><summary>想知道題目與計分細節？</summary><p>一致與不一致各12題、各墨色平衡，每題最多5秒。僅正確且未逾時的正式題納入條件平均；任一條件不足6題不解讀差值。練習不納入。可跳過／重來；離開或切至背景會中止未完成活動，資料不上傳。</p></details></div>'
 elif i==12:mid='<div class="reading-results">'+resultsection('stroop')+'<div class="block-stack">'+''.join(block(b) for b in bs)+'</div></div><button data-go="11">返回Stroop體驗</button>'
 elif i==14:mid='<div class="applications">'+''.join(block(b,'application-case') for b in bs)+'</div>'
 elif i==15:
  def md(t):
   return re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',lambda m:'<a href="'+m.group(2)+'" target="_blank" rel="noopener noreferrer">'+m.group(1)+'</a>',e(t))
  mid='<button id="return-source" class="source-return" disabled>返回引用處</button><ol class="source-list">'+''.join('<li id="ref-'+str(n)+'" tabindex="-1"><h2>'+e(b['label'])+'</h2><p>'+md(b['text'])+'</p></li>' for n,b in enumerate(bs,1))+'</ol>'
 else:raise ValueError(i)
 content=top+mid+example(p)+(closing(p) if i!=0 else '')
 sections.append('<section class="slide" data-layout="'+e(p['layout'])+'" id="'+pid+'" hidden>'+content+'</section>')
options=''.join('<option value="'+str(p['id'])+'">'+e('封面' if p['id']==0 else '來源' if p['id']==15 else str(p['id'])+' · '+p['title'])+'</option>' for p in pages)
css=(ROOT/'presentation/v3/deck.css').read_text();js="'use strict';\nconst resultFeedback="+json.dumps(data['result_feedback'],ensure_ascii=False).replace('</','<\\/')+';\n'+(ROOT/'presentation/v3/deck.js').read_text()
html='<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="以選擇、分配與處理理解注意力的極限，含任務切換與Stroop兩個離線體驗。"><title>'+e(data['title'])+'</title><style>'+css+'</style></head><body><header><div class="brand">注意力的極限<span class="sample-tag">選擇 · 分配 · 處理</span></div><label><select id="jump" aria-label="跳到投影片">'+options+'</select></label></header><main>'+''.join(sections)+'</main><footer><span id="page-label" class="page-label main-label"></span><span class="keyboard-hint">左右鍵切換 · 長內容可上下捲動</span><div class="nav"><button id="prev">上一頁</button><button id="next">下一頁</button></div></footer><noscript>請允許本機檔案執行JavaScript，才能使用逐頁導覽與活動。</noscript><script>'+js+'</script></body></html>'
out=ROOT/'attention-v3.html';out.write_text(html);print(out)
