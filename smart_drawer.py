#!/usr/bin/env python3
# smart_drawer.py – كل شيء داخل الـ drawer بدون زر رجوع

with open('index.html','r',encoding='utf-8') as f:
    html = f.read()

# ══════════════════════════════════════════════════════
# 1. استبدال cpGoPage + cpShowBackBar + cpReturnToDrawer
#    بمنطق DOM-transplant جديد
# ══════════════════════════════════════════════════════
OLD_NAV = '''/* ── navigate to a real page while keeping subscriber context ── */
function cpGoPage(which){
  /* close drawer, navigate to real page, show back-bar */
  $("cpDrawer").classList.remove("open");
  document.body.style.overflow="";
  go(which);
  cpShowBackBar(which);
}
function cpShowBackBar(which){
  let bar=$("cpBackBar");
  if(!bar){
    bar=document.createElement("div");
    bar.id="cpBackBar";
    bar.className="cp-back-bar";
    document.body.appendChild(bar);
  }
  const sub=findAccById(_cpOpenSubId);
  const name=sub?sub.name:"Subscriber";
  bar.innerHTML=`
    <button class="cp-back-bar-btn" onclick="cpReturnToDrawer()">
      <svg viewBox="0 0 24 24" fill="none" width="16" height="16"><path d="M19 12H5M12 5l-7 7 7 7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      Back to ${name}
    </button>
    <span class="cp-back-bar-label">${name}</span>
  `;
  bar.classList.add("show");
}
function cpReturnToDrawer(){
  const bar=$("cpBackBar");
  if(bar) bar.classList.remove("show");
  go("coachpanel");
  if(_cpOpenSubId){
    /* reopen drawer */
    setTimeout(()=>cpOpenSubscriber(_cpOpenSubId), 80);
  }
}'''

NEW_NAV = '''/* ═══════════════════════════════════════════════════
   DOM-TRANSPLANT: نقل الصفحة الحقيقية داخل الـ drawer
   ═══════════════════════════════════════════════════ */
let _cpTransplanted=null; /* {pageId, placeholder} */

function cpGoPage(which){
  const pageMap={work:"pWork",weight:"pWeight",calc:"pCalc",week:"pWeek",macros:"pMacros"};
  const pageId=pageMap[which]; if(!pageId) return;
  const page=$(pageId); if(!page) return;
  const body=$("cpDrawerBody"); if(!body) return;

  /* ── restore any previous transplant first ── */
  cpRestoreTransplant();

  /* ── create placeholder in original position ── */
  const placeholder=document.createElement("div");
  placeholder.id="cpTransplantHolder";
  placeholder.style.display="none";
  page.parentNode.insertBefore(placeholder, page);

  /* ── move page into drawer body ── */
  body.innerHTML="";
  page.classList.add("active","cp-transplanted");
  body.appendChild(page);
  body.scrollTop=0;

  _cpTransplanted={pageId, placeholder};

  /* ── call init functions with subscriber context ── */
  if(which==="work")   { renderWorkouts(); applyWorkButtons(); }
  if(which==="weight") { loadWeightTracker(); applyWeightButtons(); }
  if(which==="calc")   { loadCalcInputs(); renderCalcMode(); renderCalcResults(); renderSubscriberCalcView(); }
  if(which==="week")   { buildWeekInputs(); loadWeekInputs(); syncWeeklyTarget(); recalcWeek(); applyWeekButtons(); }
  if(which==="macros") { renderMacrosPage(); }
}

function cpRestoreTransplant(){
  if(!_cpTransplanted) return;
  const {pageId, placeholder}=_cpTransplanted;
  const page=$(pageId); if(!page) { _cpTransplanted=null; return; }
  /* put page back where placeholder is */
  page.classList.remove("active","cp-transplanted");
  placeholder.parentNode.insertBefore(page, placeholder);
  placeholder.remove();
  _cpTransplanted=null;
}

/* kept as no-op – back-bar no longer used */
function cpShowBackBar(){ }
function cpReturnToDrawer(){ }'''

if OLD_NAV in html:
    html = html.replace(OLD_NAV, NEW_NAV, 1)
    print('cpGoPage DOM-transplant replaced OK')
else:
    print('ERROR: OLD_NAV not found')

# ══════════════════════════════════════════════════════
# 2. cpCloseDrawer: استعادة الـ transplant عند الإغلاق
# ══════════════════════════════════════════════════════
OLD_CLOSE = '''function cpCloseDrawer(){
  $("cpDrawer").classList.remove("open");
  document.body.style.overflow="";
  _cpOpenSubId=null;
  /* restore coach's own managed id */
  const a=me(); if(a) setManagedId(a.id);
  hydrateHeader();
  cpBuildGrid();
  /* hide back bar */
  const bb=$("cpBackBar"); if(bb) bb.classList.remove("show");
}'''

NEW_CLOSE = '''function cpCloseDrawer(){
  /* restore any transplanted page BEFORE clearing drawer */
  cpRestoreTransplant();
  $("cpDrawer").classList.remove("open");
  document.body.style.overflow="";
  _cpOpenSubId=null;
  /* restore coach's own managed id */
  const a=me(); if(a) setManagedId(a.id);
  hydrateHeader();
  cpBuildGrid();
}'''

if OLD_CLOSE in html:
    html = html.replace(OLD_CLOSE, NEW_CLOSE, 1)
    print('cpCloseDrawer updated OK')
else:
    print('ERROR: cpCloseDrawer not found')

# ══════════════════════════════════════════════════════
# 3. cpOpenSubscriber: استعادة أي transplant سابق
# ══════════════════════════════════════════════════════
OLD_OPEN_BAR = '''  /* hide back bar if visible */
  const _bb=$("cpBackBar"); if(_bb) _bb.classList.remove("show");
  /* open drawer */'''

NEW_OPEN_BAR = '''  /* restore any transplanted page first */
  cpRestoreTransplant();
  /* open drawer */'''

if OLD_OPEN_BAR in html:
    html = html.replace(OLD_OPEN_BAR, NEW_OPEN_BAR, 1)
    print('cpOpenSubscriber updated OK')
else:
    print('ERROR: cpOpenSubscriber header not found')

# ══════════════════════════════════════════════════════
# 4. CSS: تحديث .cp-transplanted + إزالة .cp-back-bar
# ══════════════════════════════════════════════════════
OLD_BACK_CSS = '''  /* ── Coach back-bar: floating pill at top when viewing subscriber's pages ── */
  .cp-back-bar{
    position:fixed; top:12px; left:50%; transform:translateX(-50%) translateY(-80px);
    z-index:7999; width:calc(100% - 32px); max-width:420px;
    background:linear-gradient(135deg,#060e22,#0a1830);
    border:1.5px solid rgba(56,189,248,.35);
    border-radius:18px;
    padding:10px 14px;
    display:flex; align-items:center; gap:10px;
    transition:transform .32s cubic-bezier(.22,1,.36,1);
    box-shadow:0 8px 32px rgba(0,0,0,.7), 0 0 0 1px rgba(56,189,248,.1);
  }
  .cp-back-bar.show{ transform:translateX(-50%) translateY(0); }
  .cp-back-bar-btn{
    display:flex; align-items:center; gap:7px; flex-shrink:0;
    background:rgba(56,189,248,.12); border:1.5px solid rgba(56,189,248,.3);
    color:#38bdf8; border-radius:12px; padding:7px 13px;
    font-size:12px; font-weight:800; cursor:pointer; transition:all .18s;
    white-space:nowrap;
  }
  .cp-back-bar-btn:hover{ background:rgba(56,189,248,.22); }
  .cp-back-bar-btn:active{ transform:scale(.94); }
  .cp-back-bar-label{
    font-size:12px; font-weight:700;
    background:linear-gradient(90deg,#38bdf8,#818cf8);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis; flex:1;
  }'''

NEW_TRANS_CSS = '''  /* ── Transplanted page inside drawer ── */
  .cp-transplanted{
    display:block !important;
    animation:cp-rise .28s cubic-bezier(.22,1,.36,1) both;
  }
  .cp-transplanted .wo-page,
  .cp-transplanted .calc-page,
  .cp-transplanted .wt-page,
  .cp-transplanted .burn-page,
  .cp-transplanted .mac-page{
    padding-bottom:32px;
  }'''

if OLD_BACK_CSS in html:
    html = html.replace(OLD_BACK_CSS, NEW_TRANS_CSS, 1)
    print('Back-bar CSS replaced with transplant CSS OK')
else:
    print('ERROR: back-bar CSS not found')

# ══════════════════════════════════════════════════════
# 5. تحديث cpDrawerTab لعدم استخدام cpGoPage مع الـ overview في tabs
#    (الـ tabs تبقى كما هي فقط نتأكد من restore)
# ══════════════════════════════════════════════════════
OLD_TAB_BODY = '''function cpDrawerTab(tab){
  Object.keys(_cpTabIdMap).forEach(t=>{
    const el=$(_cpTabIdMap[t]);
    if(el) el.classList.toggle("active", t===tab);
  });
  const body=$("cpDrawerBody"); if(!body) return;
  body.scrollTop=0;
  if(tab==="overview")  { cpDrawerOverview(); return; }
  if(tab==="manage")    { cpDrawerManage();   return; }
  /* For content-heavy tabs: navigate to real page with subscriber context */
  if(tab==="work")    { cpGoPage("work");    return; }
  if(tab==="weight")  { cpGoPage("weight");  return; }
  if(tab==="calc")    { cpGoPage("calc");    return; }
  if(tab==="week")    { cpGoPage("week");    return; }
  if(tab==="macros")  { cpGoPage("macros");  return; }
}'''

NEW_TAB_BODY = '''function cpDrawerTab(tab){
  Object.keys(_cpTabIdMap).forEach(t=>{
    const el=$(_cpTabIdMap[t]);
    if(el) el.classList.toggle("active", t===tab);
  });
  const body=$("cpDrawerBody"); if(!body) return;
  body.scrollTop=0;
  /* restore any transplanted page before switching tabs */
  if(tab==="overview"||tab==="manage") cpRestoreTransplant();
  if(tab==="overview")  { cpDrawerOverview(); return; }
  if(tab==="manage")    { cpDrawerManage();   return; }
  /* content tabs: transplant real page directly into drawer */
  if(tab==="work")    { cpGoPage("work");    return; }
  if(tab==="weight")  { cpGoPage("weight");  return; }
  if(tab==="calc")    { cpGoPage("calc");    return; }
  if(tab==="week")    { cpGoPage("week");    return; }
  if(tab==="macros")  { cpGoPage("macros");  return; }
}'''

if OLD_TAB_BODY in html:
    html = html.replace(OLD_TAB_BODY, NEW_TAB_BODY, 1)
    print('cpDrawerTab updated with restore OK')
else:
    print('ERROR: cpDrawerTab not found')

# ══════════════════════════════════════════════════════
# Write
# ══════════════════════════════════════════════════════
with open('index.html','w',encoding='utf-8') as f:
    f.write(html)

with open('index.html','r',encoding='utf-8') as f:
    lines = f.readlines()
print(f'Done. {len(lines)} lines')
