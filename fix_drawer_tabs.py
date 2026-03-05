#!/usr/bin/env python3
# fix_drawer_tabs.py
# الحل: الـ drawer يستدعي go() للصفحات الحقيقية مع شريط "عودة للـ drawer"

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# ─────────────────────────────────────────────────────────────
# 1. Replace cpDrawerTab – استخدام الصفحات الحقيقية
# ─────────────────────────────────────────────────────────────
OLD_TAB_FN = '''/* tab id map: key used in cpDrawerTab -> actual element id */
const _cpTabIdMap = {
  overview:"cpTabOverview", work:"cpTabWorkouts", weight:"cpTabWeight",
  calc:"cpTabCalc", week:"cpTabWeek", macros:"cpTabMacros", manage:"cpTabManage"
};
function cpDrawerTab(tab){
  Object.keys(_cpTabIdMap).forEach(t=>{
    const el=$(_cpTabIdMap[t]);
    if(el) el.classList.toggle("active", t===tab);
  });
  const body=$("cpDrawerBody"); if(!body) return;
  body.scrollTop=0;
  if(tab==="overview")  { cpDrawerOverview(); return; }
  if(tab==="manage")    { cpDrawerManage();   return; }
  /* render real page content inside drawer */
  body.innerHTML=`<div class="cp-tab-inner" id="cpDrawerInner"></div>`;
  const inner=$("cpDrawerInner");
  if(tab==="work"){
    inner.innerHTML=`<div class="wo-page" id="workContainer"></div><div style="padding:0 12px 8px"><button class="wo-reset-btn hidden" id="workResetBtn" onclick="resetWorkouts()">Reset Workouts</button></div>`;
    renderWorkouts(); applyWorkButtons();
  }
  if(tab==="weight"){
    inner.innerHTML=`<div style="padding:12px" id="weightRows"></div><div style="padding:0 12px 8px"><button class="mini hidden" id="weightResetBtn" onclick="resetWeightData()">Reset</button></div>`;
    loadWeightTracker(); applyWeightButtons();
  }
  if(tab==="calc"){
    inner.innerHTML=`<div class="calc-page" id="calcInputsWrap" style="display:none"></div><div id="cpCalcResults"></div>`;
    loadCalcInputs(); renderCalcMode(); renderCalcResults(); renderSubscriberCalcView();
  }
  if(tab==="week"){
    inner.innerHTML=`<div style="padding:12px" id="weekRows"></div>`;
    buildWeekInputs(); loadWeekInputs(); syncWeeklyTarget(); recalcWeek(); applyWeekButtons();
  }
  if(tab==="macros"){
    inner.innerHTML=`<div id="macrosInner"></div>`;
    renderMacrosPage();
  }
}'''

NEW_TAB_FN = '''/* tab id map: key used in cpDrawerTab -> actual element id */
const _cpTabIdMap = {
  overview:"cpTabOverview", work:"cpTabWorkouts", weight:"cpTabWeight",
  calc:"cpTabCalc", week:"cpTabWeek", macros:"cpTabMacros", manage:"cpTabManage"
};

/* ── navigate to a real page while keeping subscriber context ── */
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
}

function cpDrawerTab(tab){
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

if OLD_TAB_FN in html:
    html = html.replace(OLD_TAB_FN, NEW_TAB_FN, 1)
    print('cpDrawerTab replaced with real-page navigation OK')
else:
    print('ERROR: OLD_TAB_FN not found')

# ─────────────────────────────────────────────────────────────
# 2. Also update cpOpenSubscriber to set initial tab properly
# ─────────────────────────────────────────────────────────────
# Make cpOpenSubscriber reset any back bar
OLD_OPEN_SUB_END = '''  /* open drawer */
  $("cpDrawer").classList.add("open");
  document.body.style.overflow="hidden";
  cpDrawerTab("overview");
}'''

NEW_OPEN_SUB_END = '''  /* hide back bar if visible */
  const _bb=$("cpBackBar"); if(_bb) _bb.classList.remove("show");
  /* open drawer */
  $("cpDrawer").classList.add("open");
  document.body.style.overflow="hidden";
  cpDrawerTab("overview");
}'''

if OLD_OPEN_SUB_END in html:
    html = html.replace(OLD_OPEN_SUB_END, NEW_OPEN_SUB_END, 1)
    print('cpOpenSubscriber back-bar reset OK')
else:
    print('WARNING: cpOpenSubscriber end not found')

# ─────────────────────────────────────────────────────────────
# 3. Add CSS for the back bar
# ─────────────────────────────────────────────────────────────
BACK_BAR_CSS = '''
  /* ── Coach back-bar (shown when viewing a page in subscriber context) ── */
  .cp-back-bar{
    position:fixed; top:0; left:0; right:0; z-index:7999;
    background:linear-gradient(90deg,#050d1e,#081428);
    border-bottom:1.5px solid rgba(56,189,248,.25);
    padding:10px 16px;
    display:flex; align-items:center; gap:12px;
    transform:translateY(-100%);
    transition:transform .28s cubic-bezier(.22,1,.36,1);
    box-shadow:0 4px 20px rgba(0,0,0,.6);
  }
  .cp-back-bar.show{ transform:translateY(0); }
  .cp-back-bar-btn{
    display:flex; align-items:center; gap:8px;
    background:rgba(56,189,248,.1); border:1.5px solid rgba(56,189,248,.3);
    color:#38bdf8; border-radius:12px; padding:8px 14px;
    font-size:13px; font-weight:800; cursor:pointer; transition:all .18s;
    white-space:nowrap;
  }
  .cp-back-bar-btn:hover{ background:rgba(56,189,248,.2); }
  .cp-back-bar-btn:active{ transform:scale(.95); }
  .cp-back-bar-label{
    font-size:12px; font-weight:700; color:#64748b;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
  }
'''

if '.cp-back-bar' not in html:
    # Insert before the workout CSS
    marker = '  /* ===== Workout Page ====='
    if marker in html:
        html = html.replace(marker, BACK_BAR_CSS + '  /* ===== Workout Page =====', 1)
        print('Back-bar CSS added OK')
    else:
        print('WARNING: workout CSS marker not found')
else:
    print('Back-bar CSS already present')

# ─────────────────────────────────────────────────────────────
# 4. Fix cpCloseDrawer to also clean up back bar
# ─────────────────────────────────────────────────────────────
OLD_CLOSE_DRAWER = '''function cpCloseDrawer(){
  $("cpDrawer").classList.remove("open");
  document.body.style.overflow="";
  _cpOpenSubId=null;
  /* restore coach's own managed id */
  const a=me(); if(a) setManagedId(a.id);
  hydrateHeader();
  cpBuildGrid();
}'''

NEW_CLOSE_DRAWER = '''function cpCloseDrawer(){
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

if OLD_CLOSE_DRAWER in html:
    html = html.replace(OLD_CLOSE_DRAWER, NEW_CLOSE_DRAWER, 1)
    print('cpCloseDrawer updated OK')
else:
    print('WARNING: cpCloseDrawer not found')

# ─────────────────────────────────────────────────────────────
# Write
# ─────────────────────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Done. {len(lines)} lines')
