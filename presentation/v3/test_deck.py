from pathlib import Path
import json,re,hashlib,datetime,zoneinfo,argparse
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[2];R=ROOT/'records/runs/attention-v3-001';HTML=ROOT/'attention-v3.html';M=json.loads((ROOT/'content/v3/manuscript.json').read_text());a=argparse.ArgumentParser();a.add_argument('--report',default='full-browser-01.json');args=a.parse_args();checks=[];issues=[];screens=[];errors=[];requests=[];direct_error=None;mode='file'
state=json.loads((R/'state.json').read_text());assert not state.get('independent_reviews_pending',False), 'Cannot test stale HTML while new manuscript reviews are pending'
assert hashlib.sha256(HTML.read_bytes()).hexdigest()==state['html_sha256'], 'HTML does not match the recorded generated version'
assert not (R/args.report).exists(), 'Use a new report filename to preserve previous test evidence'
def check(n,ok,detail=None):
 checks.append(dict(name=n,result='pass' if ok else 'fail',detail=detail))
 if not ok:issues.append(dict(node=6,check=n,detail=detail))
with sync_playwright() as p:
 b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox']);c=b.new_context(offline=True,viewport={'width':1440,'height':900});probe=c.new_page()
 try:probe.goto(HTML.as_uri(),timeout=15000)
 except Exception as ex:mode='memory-http';direct_error=str(ex)
 probe.close();c.route('http://**/*',lambda r:r.abort());c.route('https://**/*',lambda r:r.abort());c.route('http://localhost:31460/deck',lambda r:r.fulfill(content_type='text/html; charset=utf-8',body=HTML.read_bytes()));page=c.new_page();page.on('pageerror',lambda ex:errors.append(str(ex)));page.on('request',lambda req:requests.append(req.url) if req.url.startswith(('http://','https://')) and req.url!='http://localhost:31460/deck' else None)
 try:
  page.goto(HTML.as_uri() if mode=='file' else 'http://localhost:31460/deck');check('16_total_14_body',page.locator('.slide').count()==16 and page.locator('.slide[id^=p]').count()==14)
  check('cover_boundary',page.locator('#prev').is_disabled());page.keyboard.press('ArrowLeft');check('cover_stays',page.locator('#cover').is_visible())
  for i in range(15):page.locator('#next').click()
  check('all_next_pages',page.locator('#sources').is_visible() and page.locator('#next').is_disabled());page.keyboard.press('ArrowRight');check('source_boundary',page.locator('#sources').is_visible());page.keyboard.press('ArrowLeft');check('keyboard_previous',page.locator('#p14').is_visible())
  layouts=page.locator('.slide').evaluate_all('(els)=>els.map(e=>e.dataset.layout)');check('varied_adjacent_layouts',len(set(layouts))>=4 and all(x!=y for x,y in zip(layouts,layouts[1:])),layouts)
  for w,h in [(1440,900),(1366,600),(390,844),(960,540),(1280,720)]:
   page.set_viewport_size(dict(width=w,height=h));style=page.add_style_tag(content='h1{font-size:3.5rem!important}p{font-size:1.4rem!important}body{font-family:serif!important}') if w==1280 else None
   for i in range(16):
    page.select_option('#jump',str(i));id='cover' if i==0 else 'sources' if i==15 else f'p{i:02}'
    check(f'title_{w}_{i}',page.locator('#'+id+' h1').inner_text()==M['pages'][i]['title'])
    if 1<=i<=14:check(f'storyline_{w}_{i}',page.locator('#'+id+' .current').inner_text()==M['pages'][i]['stage'])
    bad=page.evaluate('''()=>[...document.querySelectorAll('.slide:not([hidden]) *')].filter(e=>{const r=e.getBoundingClientRect();return r.width>0&&(r.left < -1||r.right>innerWidth+1)}).map(e=>({cls:e.className,text:e.textContent.slice(0,60)}))''');check(f'horizontal_bounds_{w}_{i}',not bad,bad)
    overlaps=page.evaluate('''()=>{let bad=[];const root=document.querySelector('.slide:not([hidden])');const groups=[root,...root.querySelectorAll('.text-block,.study-step,.arrangement-content,.experiment,.source-list li,.application-case,.chapter-node')];for(const g of groups){let a=[...g.children].filter(e=>e.getBoundingClientRect().height>0);for(let i=1;i<a.length;i++){let x=a[i-1].getBoundingClientRect(),y=a[i].getBoundingClientRect();if(x.bottom>y.top+1)bad.push([a[i-1].className,a[i].className])}}return bad}''');check(f'no_overlap_{w}_{i}',not overlaps,overlaps)
    check(f'footer_{w}_{i}',page.locator('footer').bounding_box()['y']+page.locator('footer').bounding_box()['height']<=h+1)
    check(f'no_truncation_{w}_{i}',page.evaluate('''()=>[...document.querySelectorAll('.slide:not([hidden]) h1,.slide:not([hidden]) h2,.slide:not([hidden]) p')].every(e=>e.scrollWidth<=e.clientWidth+1&&e.scrollHeight<=e.clientHeight+1)'''))
    shot=R/f'screens/{Path(args.report).stem}/{w}-{id}.png';shot.parent.mkdir(parents=True,exist_ok=True);page.screenshot(path=str(shot));screens.append(str(shot.relative_to(ROOT)))
    page.evaluate('document.querySelector("main").scrollTop=document.querySelector("main").scrollHeight');check(f'bottom_reachable_{w}_{i}',page.locator('#'+id).evaluate('e=>{const m=document.querySelector("main").getBoundingClientRect(),target=e.id==="cover"?e.querySelector(".hero button"):e.lastElementChild,r=target.getBoundingClientRect();return r.bottom<=m.bottom+1&&r.top>=m.top-1}'))
   if style:style.evaluate('(e)=>e.remove()')
  page.set_viewport_size(dict(width=1440,height=900));page.select_option('#jump','1');page.locator('[data-reveal="prediction-reveal"]').first.click();check('prediction_reveal',page.locator('#prediction-reveal').is_visible())
  # All reviewed knowledge retained; sample8 uses equivalent split round cards.
  missing=[]
  for p in M['pages']:
   i=p['id'];id='cover' if i==0 else 'sources' if i==15 else f'p{i:02}';text=page.locator('#'+id).inner_text()
   if p['main_message'] not in text or p['explanation'] not in text:missing.append((i,'main'))
   if i not in [6,8,15]:
    for block in p['blocks']:
     if block['text'] not in text:missing.append((i,block['label']))
  check('reviewed_knowledge_retained',not missing,missing)
  for game_name in ['switch','stroop']:
   for branch,delta,eligible in [('positive',100,True),('zero',0,True),('negative',-100,True),('insufficient',None,False)]:
    actual=page.evaluate('([kind,delta,eligible])=>__deck.feedbackFor(kind,{delta,eligible})',[game_name,delta,eligible])
    check(f'{game_name}_reviewed_feedback_{branch}',actual==M['result_feedback'][game_name][branch],actual)
  check('no_reader_internal_codes',not re.search(r'\b[KC]\d{2}\b',page.locator('main').text_content()))
  page.select_option('#jump','4');page.locator('#p04 [data-source="5"]').click();check('source_focus',page.locator('#sources').is_visible() and page.locator('#ref-5').evaluate('e=>e===document.activeElement'));page.locator('#return-source').click();check('source_return',page.locator('#p04').is_visible() and page.locator('#p04 [data-source="5"]').evaluate('e=>e===document.activeElement'))
  check('seven_source_entries',page.locator('#sources .source-list li').count()==7);check('all_anchor_targets',page.evaluate('''()=>[...document.querySelectorAll('a[href^="#"]')].every(a=>document.getElementById(a.getAttribute('href').slice(1)))'''));check('no_external_assets',page.locator('script[src],link[rel=stylesheet],iframe,img,video,audio').count()==0);check('offline_no_extra_requests',not requests,requests)
  pure=page.evaluate('''()=>{let api=__deck.switch,a=api.makeRound('blocked',()=>.3),b=api.makeRound('mixed',()=>.3);let same=['parity','magnitude'].every(r=>JSON.stringify(a.filter(t=>t.rule===r).map(t=>t.n).sort())===JSON.stringify(b.filter(t=>t.rule===r).map(t=>t.n).sort()));let rows=[];for(let kind of ['blocked','mixed'])for(let i=0;i<12;i++)rows.push({kind,status:'correct',rt:kind==='blocked'?300:200});const neg=api.summarize(rows);rows[0].status='wrong';return {same,negative:neg.delta,unequal:api.summarize(rows).eligible}}''');check('switch_matching_scoring',pure['same'] and pure['negative']==-1200 and not pure['unequal'],pure)
  page.clock.install();page.select_option('#jump','8');page.locator('#start').click()
  def check_result_view(kind,branch):
   locator=page.locator('#interpret' if kind=='switch' else '#st-interpret')
   check(f'{kind}_{branch}_rendered_reviewed_message',M['result_feedback'][kind][branch] in locator.inner_text())
   for width,height in [(1440,900),(390,844)]:
    page.set_viewport_size(dict(width=width,height=height));locator.scroll_into_view_if_needed()
    check(f'{kind}_{branch}_feedback_bounds_{width}',locator.evaluate('e=>{const r=e.getBoundingClientRect();return r.left>=-1&&r.right<=innerWidth+1&&e.scrollWidth<=e.clientWidth+1&&e.scrollHeight<=e.clientHeight+1}'))
    path=R/f'screens/{Path(args.report).stem}/{width}-{kind}-{branch}.png';page.screenshot(path=str(path));screens.append(str(path.relative_to(ROOT)))
   page.set_viewport_size(dict(width=1440,height=900))
  def swAnswer(i,wrong=False,delay=0):
   if delay:page.clock.run_for(delay)
   t=page.evaluate('__deck.switch.getState().trial');v=(0 if t['n']%2 else 1) if t['rule']=='parity' else (0 if t['n']<5 else 1);v=1-v if wrong else v
   if i%2:page.keyboard.press('f' if v==0 else 'j')
   else:page.locator('#answer-left' if v==0 else '#answer-right').click()
   page.clock.run_for(310)
  for i in range(6):swAnswer(i)
  check('switch_practice_excluded',page.evaluate('__deck.switch.getState().rows')==0)
  for rr in range(2):
   page.locator('#continue').click()
   for i in range(12):swAnswer(i,delay=200 if page.evaluate('__deck.switch.getState().order[__deck.switch.getState().round]')=='blocked' else 500)
  st=page.evaluate('__deck.switch.getState()');check('switch_complete_24',st['rows']==24 and st['result']['eligible'],st);page.locator('#sw-view-result').click();check('switch_goes_result_page9',page.locator('#p09').is_visible() and page.locator('#results .result-item').count()==2)
  check('switch_positive_theory_feedback',st['result']['delta']>0 and M['result_feedback']['switch']['positive'] in page.locator('#interpret').inner_text())
  check_result_view('switch','positive')
  page.screenshot(path=str(R/f'screens/{Path(args.report).stem}/switch-results.png'))
  page.select_option('#jump','8');page.locator('#start').click();check('switch_restart_clears',page.evaluate('__deck.switch.getState().rows')==0)
  for i in range(6):swAnswer(i)
  for rr in range(2):
   page.locator('#continue').click()
   for i in range(12):
    if rr==0 and i==0:page.clock.run_for(5310)
    else:swAnswer(i,wrong=rr==0 and i==1)
  st=page.evaluate('__deck.switch.getState()');check('switch_bad_data_suppressed',not st['result']['eligible'] and sum(r['timeout'] for r in st['result']['rounds'])==1);page.locator('#sw-view-result').click();check('switch_plain_insufficient','先不比較快慢' in page.locator('#interpret').inner_text())
  check_result_view('switch','insufficient')
  page.select_option('#jump','8');page.locator('#start').click();page.locator('#skip').click();check('switch_skip_no_fake',page.locator('#p09').is_visible() and '尚未完成' in page.locator('#result-grid').inner_text());page.select_option('#jump','8');page.locator('#start').click();page.keyboard.press('f');page.keyboard.press('j');check('switch_duplicate_input',page.evaluate('__deck.switch.getState().index')==1);page.keyboard.press('ArrowLeft');check('switch_leave_aborts',page.evaluate('__deck.switch.getState().phase')=='aborted')
  stpure=page.evaluate('''()=>{const a=__deck.stroop.makeTrials(()=>.37),ok=[true,false].every(c=>[0,1,2,3].every(ink=>a.filter(x=>x.compatible===c&&x.ink===ink).length===3)),rows=[];for(let c of [true,false])for(let i=0;i<12;i++)rows.push({compatible:c,status:'correct',rt:c?500:400});return {balanced:ok&&a.length===24&&a.every(x=>x.compatible?(x.word===x.ink):(x.word!==x.ink)),negative:__deck.stroop.summarize(rows).delta,insufficient:__deck.stroop.summarize(rows.slice(0,12)).eligible}}''');check('stroop_balance_and_scoring',stpure['balanced'] and stpure['negative']==-100 and not stpure['insufficient'],stpure)
  page.select_option('#jump','11');page.locator('#st-start').click()
  def stAnswer(i,wrong=False,delay=0):
   if delay:page.clock.run_for(delay)
   t=page.evaluate('__deck.stroop.getState().trial');v=(t['ink']+1)%4 if wrong else t['ink']
   if i%2:page.keyboard.press(str(v+1))
   else:page.locator(f'[data-st-answer="{v}"]').click()
   page.clock.run_for(310)
  for i in range(28):stAnswer(i,delay=200 if page.evaluate('__deck.stroop.getState().trial.compatible') else 500)
  st=page.evaluate('__deck.stroop.getState()');check('stroop_complete_practice_excluded',st['rows']==24 and st['phase']=='results' and all(g['valid']==12 for g in st['result']['groups']),st);page.locator('#st-view-result').click();check('stroop_goes_results_page12',page.locator('#p12').is_visible() and page.locator('#st-results .result-item').count()==2)
  check('stroop_positive_theory_feedback',st['result']['delta']>0 and M['result_feedback']['stroop']['positive'] in page.locator('#st-interpret').inner_text())
  check_result_view('stroop','positive')
  page.screenshot(path=str(R/f'screens/{Path(args.report).stem}/stroop-results.png'))
  page.select_option('#jump','11');page.locator('#st-start').click();check('stroop_restart_clears',page.evaluate('__deck.stroop.getState().rows')==0)
  for i in range(28):
   if i==4:page.clock.run_for(5310)
   else:stAnswer(i,wrong=i>=5)
  st=page.evaluate('__deck.stroop.getState()');check('stroop_timeout_wrong_insufficient',not st['result']['eligible'] and sum(x['timeout'] for x in st['result']['groups'])==1);page.locator('#st-view-result').click();check('stroop_plain_insufficient','資料不足' in page.locator('#st-interpret').inner_text())
  check_result_view('stroop','insufficient')
  page.select_option('#jump','11');page.locator('#st-start').click();page.locator('#st-skip').click();check('stroop_skip_no_fake',page.locator('#p12').is_visible() and not page.evaluate('__deck.stroop.getState().result'))
  page.select_option('#jump','11');page.locator('#st-start').click();page.keyboard.press('1');page.keyboard.press('2');check('stroop_duplicate_input',page.evaluate('__deck.stroop.getState().index')==1);page.keyboard.press('ArrowRight');check('stroop_leave_aborts',page.evaluate('__deck.stroop.getState().phase')=='aborted')
  # End-to-end opposite-direction outcomes use synthetic timing, not human data.
  page.select_option('#jump','8');page.locator('#start').click()
  for i in range(6):swAnswer(i)
  for rr in range(2):
   page.locator('#continue').click()
   for i in range(12):swAnswer(i,delay=500 if page.evaluate('__deck.switch.getState().order[__deck.switch.getState().round]')=='blocked' else 200)
  check('switch_negative_result_direction',page.evaluate('__deck.switch.getState().result.delta')<0);page.locator('#sw-view-result').click();check_result_view('switch','negative')
  page.select_option('#jump','11');page.locator('#st-start').click()
  for i in range(28):stAnswer(i,delay=500 if page.evaluate('__deck.stroop.getState().trial.compatible') else 200)
  check('stroop_negative_result_direction',page.evaluate('__deck.stroop.getState().result.delta')<0);page.locator('#st-view-result').click();check_result_view('stroop','negative')
  page.select_option('#jump','0');page.emulate_media(media='print');check('print_shows_all16',page.locator('.slide:visible').count()==16);page.emulate_media(media='screen');check('no_js_errors',not errors,errors)
 except Exception as ex:check('test_completed',False,str(ex))
 b.close()
report={'time':datetime.datetime.now(zoneinfo.ZoneInfo('Asia/Taipei')).isoformat(),'result':'pass' if not issues else 'fail','mode':mode,'browser_executed':True,'html_sha256':hashlib.sha256(HTML.read_bytes()).hexdigest(),'checks':checks,'issues':issues,'screenshots':screens,'direct_file_probe_error':direct_error,'unverified':[] if mode=='file' else ['Direct file:// launch blocked by managed browser policy; full tests used exact bytes at permitted localhost in offline context.'],'scope':'16 slides, 5 viewport/font conditions, both games, citations, offline and print; game inputs synthetic, not participant data.','external_link_scope':'URLs and local targets validated; live external availability not verified offline.'};(R/args.report).write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({'result':report['result'],'checks':len(checks),'issues':issues,'mode':mode},ensure_ascii=False,indent=2));raise SystemExit(bool(issues))
