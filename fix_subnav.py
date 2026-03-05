#!/usr/bin/env python3
"""
Subscriber UX redesign:
1. Fixed top icon bar (replaces text tabs) for subscribers
2. Back button when inside any page (Calc, Work, etc.)
3. Icon grid removed from profile (replaced by top bar)
"""

with open("index.html","r",encoding="utf-8") as f:
    html = f.read()

original_len = len(html)
ok = []
fail = []

# ══════════════════════════════════════════════════════════════════
# 1. Add CSS for the new subscriber top nav bar + back button
# ══════════════════════════════════════════════════════════════════

TARGET_CSS = "  .pf-page{ animation:pf-rise .38s cubic-bezier(.22,1,.36,1) both; }"

SUB_NAV_CSS = """  /* ── Subscriber top nav bar ── */
  #subTopNav{
    display:none; /* shown only for subscribers */
    position:sticky; top:0; z-index:200;
    background:rgba(6,12,25,.97);
    border-bottom:1px solid rgba(255,255,255,.07);
    padding:0 4px; overflow-x:auto; scrollbar-width:none;
    flex-shrink:0; gap:0;
    -webkit-overflow-scrolling:touch;
    backdrop-filter:blur(14px);
    flex-direction:row; align-items:stretch;
  }
  #subTopNav::-webkit-scrollbar{ display:none; }
  .sub-nav-btn{
    padding:11px 14px 10px; border:none; cursor:pointer;
    background:transparent; color:#3d5068;
    font-size:11px; font-weight:800;
    border-bottom:2.5px solid transparent;
    transition:all .2s; flex-shrink:0;
    display:flex; align-items:center; gap:5px;
    letter-spacing:.01em; white-space:nowrap;
    -webkit-tap-highlight-color:transparent;
  }
  .sub-nav-btn svg{ width:14px; height:14px; }
  .sub-nav-btn.active{
    color:#38bdf8; border-bottom-color:#38bdf8;
    background:linear-gradient(180deg,rgba(56,189,248,.07),transparent);
  }
  .sub-nav-btn:active{ opacity:.7; }

  /* ── Back bar shown inside pages ── */
  #subBackBar{
    display:none;
    align-items:center; gap:10px;
    padding:10px 14px 8px;
    background:rgba(6,12,25,.97);
    border-bottom:1px solid rgba(255,255,255,.06);
    position:sticky; top:0; z-index:199;
    backdrop-filter:blur(14px);
  }
  #subBackBar.visible{ display:flex; }
  .sub-back-btn{
    width:34px; height:34px; border-radius:11px; border:none;
    background:rgba(255,255,255,.06); color:#94a3b8;
    display:flex; align-items:center; justify-content:center;
    cursor:pointer; flex-shrink:0; transition:background .15s;
  }
  .sub-back-btn:active{ background:rgba(255,255,255,.12); }
  #subBackTitle{
    font-size:14px; font-weight:900; color:#e2e8f0;
    display:flex; align-items:center; gap:7px;
  }

"""

TARGET_CSS_FULL = "  .pf-page{ animation:pf-rise .38s cubic-bezier(.22,1,.36,1) both; }"

if TARGET_CSS_FULL in html:
    html = html.replace(TARGET_CSS_FULL, SUB_NAV_CSS + TARGET_CSS_FULL)
    ok.append("✅ Subscriber top nav bar CSS added")
else:
    fail.append("❌ .pf-page CSS anchor not found")

# ══════════════════════════════════════════════════════════════════
# 2. Add the HTML for subTopNav and subBackBar 
#    Insert BEFORE <div class="tabs" id="tabs"
# ══════════════════════════════════════════════════════════════════

OLD_TABS_HTML = """<div class="tabs" id="tabs" style="display:none;">
  <button class="tab active" id="tProfile" onclick="go('profile')">Profile</button>
  <button class="tab hidden" id="tAdmin" onclick="go('admin')">Admin</button>
  <button class="tab hidden" id="tCoachPanel" onclick="go('coachpanel')">Subscribers</button>
  <button class="tab" id="tCalc" onclick="go('calc')">Calculator</button>
  <button class="tab" id="tWork" onclick="go('work')">Workouts</button>
  <button class="tab" id="tWeek" onclick="go('week')">Daily Burn</button>
  <button class="tab" id="tWeight" onclick="go('weight')">Weight</button>
  <button class="tab" id="tMacros" onclick="go('macros')">Macros</button>
</div>"""

NEW_TABS_HTML = """<!-- Subscriber Top Navigation Bar -->
<div id="subTopNav" style="display:none">
  <button class="sub-nav-btn active" id="snProfile" onclick="subNavGo('profile')">
    <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="8" r="4" stroke="currentColor" stroke-width="2"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Profile
  </button>
  <button class="sub-nav-btn" id="snCalc" onclick="subNavGo('calc')">
    <svg viewBox="0 0 24 24" fill="none"><rect x="4" y="2" width="16" height="20" rx="2" stroke="currentColor" stroke-width="2"/><path d="M8 7h8M8 12h4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Calc
  </button>
  <button class="sub-nav-btn" id="snWork" onclick="subNavGo('work')">
    <svg viewBox="0 0 24 24" fill="none"><path d="M6 4v16M18 4v16M3 9h18M3 15h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Workouts
  </button>
  <button class="sub-nav-btn" id="snWeek" onclick="subNavGo('week')">
    <svg viewBox="0 0 24 24" fill="none"><rect x="3" y="4" width="18" height="18" rx="2" stroke="currentColor" stroke-width="2"/><path d="M16 2v4M8 2v4M3 10h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Daily Burn
  </button>
  <button class="sub-nav-btn" id="snWeight" onclick="subNavGo('weight')">
    <svg viewBox="0 0 24 24" fill="none"><path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Weight
  </button>
  <button class="sub-nav-btn" id="snMacros" onclick="subNavGo('macros')">
    <svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/><path d="M12 8v8M8 12h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Macros
  </button>
  <button class="sub-nav-btn" id="snNotes" onclick="subNavGo('notes')">
    <svg viewBox="0 0 24 24" fill="none"><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><rect x="9" y="3" width="6" height="4" rx="1" stroke="currentColor" stroke-width="2"/><line x1="9" y1="12" x2="15" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="9" y1="16" x2="13" y2="16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Notes
  </button>
  <button class="sub-nav-btn" id="snChat" onclick="subNavGo('chat')">
    <svg viewBox="0 0 24 24" fill="none"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="9" y1="10" x2="15" y2="10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><line x1="9" y1="14" x2="12" y2="14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>Chat
  </button>
</div>

<!-- Back bar (shown when subscriber is inside a page) -->
<div id="subBackBar">
  <button class="sub-back-btn" onclick="subNavBack()">
    <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
      <path d="M19 12H5M12 5l-7 7 7 7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </button>
  <div id="subBackTitle">—</div>
</div>

<div class="tabs" id="tabs" style="display:none;">
  <button class="tab active" id="tProfile" onclick="go('profile')">Profile</button>
  <button class="tab hidden" id="tAdmin" onclick="go('admin')">Admin</button>
  <button class="tab hidden" id="tCoachPanel" onclick="go('coachpanel')">Subscribers</button>
  <button class="tab hidden" id="tCalc" onclick="go('calc')">Calculator</button>
  <button class="tab hidden" id="tWork" onclick="go('work')">Workouts</button>
  <button class="tab hidden" id="tWeek" onclick="go('week')">Daily Burn</button>
  <button class="tab hidden" id="tWeight" onclick="go('weight')">Weight</button>
  <button class="tab hidden" id="tMacros" onclick="go('macros')">Macros</button>
</div>"""

if OLD_TABS_HTML in html:
    html = html.replace(OLD_TABS_HTML, NEW_TABS_HTML)
    ok.append("✅ subTopNav + subBackBar HTML inserted")
else:
    fail.append("❌ tabs HTML not found")

# ══════════════════════════════════════════════════════════════════
# 3. Update showApp() to show subTopNav for subscribers and hide old tabs
# ══════════════════════════════════════════════════════════════════

OLD_SHOW_APP = """function showApp(){
  $(\"pLogin\").classList.remove(\"active\");
  $(\"tabs\").style.display=\"flex\";
  $(\"tAdmin\").classList.toggle(\"hidden\", !isAdmin());
  $(\"tCoachPanel\").classList.toggle(\"hidden\", !(isCoach() || isAdmin()));
  /* For subscribers/users: hide the page tabs (they use icon grid in Profile) */
  const isMember=isSub()||isUser();
  [\"tCalc\",\"tWork\",\"tWeek\",\"tWeight\",\"tMacros\"].forEach(id=>{
    const el=$(id); if(el) el.classList.toggle(\"hidden\", isMember);
  });
  hydrateHeader();
  go(\"profile\");
}"""

NEW_SHOW_APP = """function showApp(){
  $(\"pLogin\").classList.remove(\"active\");
  const isMember=isSub()||isUser();
  if(isMember){
    /* Subscriber: show top icon nav, hide old text tabs */
    $(\"tabs\").style.display=\"none\";
    $(\"subTopNav\").style.display=\"flex\";
  } else {
    /* Coach/Admin: show old tabs, hide subscriber nav */
    $(\"tabs\").style.display=\"flex\";
    $(\"subTopNav\").style.display=\"none\";
    $(\"subBackBar\").classList.remove(\"visible\");
  }
  $(\"tAdmin\").classList.toggle(\"hidden\", !isAdmin());
  $(\"tCoachPanel\").classList.toggle(\"hidden\", !(isCoach() || isAdmin()));
  hydrateHeader();
  go(\"profile\");
}"""

if OLD_SHOW_APP in html:
    html = html.replace(OLD_SHOW_APP, NEW_SHOW_APP)
    ok.append("✅ showApp updated for subscriber nav")
else:
    fail.append("❌ showApp not found")

# ══════════════════════════════════════════════════════════════════
# 4. Add subNavGo() and subNavBack() functions, and update snActive
# ══════════════════════════════════════════════════════════════════

OLD_GO_FUNC = """function go(which){
  [\"Profile\",\"Admin\",\"CoachPanel\",\"Calc\",\"Work\",\"Week\",\"Weight\",\"Macros\"].forEach(p=> $(\"p\"+p).classList.remove(\"active\"));
  [\"Profile\",\"Admin\",\"CoachPanel\",\"Calc\",\"Work\",\"Week\",\"Weight\",\"Macros\"].forEach(t=> $(\"t\"+t)?.classList.remove(\"active\"));
  const map={profile:\"Profile\",admin:\"Admin\",coachpanel:\"CoachPanel\",calc:\"Calc\",work:\"Work\",week:\"Week\",weight:\"Weight\",macros:\"Macros\"};
  const P=\"p\"+map[which], T=\"t\"+map[which];
  $(P).classList.add(\"active\");
  $(T).classList.add(\"active\");

  if(which===\"profile\") renderProfile();
  if(which===\"admin\") renderAdminPanel();
  if(which===\"coachpanel\") renderCoachPanel();
  if(which===\"calc\") { loadCalcInputs(); renderCalcMode(); renderCalcResults(); renderSubscriberCalcView(); }
  if(which===\"work\") { renderWorkouts(); applyWorkButtons(); }
  if(which===\"week\") { buildWeekInputs(); loadWeekInputs(); syncWeeklyTarget(); recalcWeek(); applyWeekButtons(); }
  if(which===\"weight\"){ loadWeightTracker(); applyWeightButtons(); }
  if(which===\"macros\"){ renderMacrosPage(); }
  hydrateHeader();
}"""

NEW_GO_FUNC = """function go(which){
  [\"Profile\",\"Admin\",\"CoachPanel\",\"Calc\",\"Work\",\"Week\",\"Weight\",\"Macros\"].forEach(p=> $(\"p\"+p).classList.remove(\"active\"));
  [\"Profile\",\"Admin\",\"CoachPanel\",\"Calc\",\"Work\",\"Week\",\"Weight\",\"Macros\"].forEach(t=> $(\"t\"+t)?.classList.remove(\"active\"));
  const map={profile:\"Profile\",admin:\"Admin\",coachpanel:\"CoachPanel\",calc:\"Calc\",work:\"Work\",week:\"Week\",weight:\"Weight\",macros:\"Macros\"};
  const P=\"p\"+map[which], T=\"t\"+map[which];
  $(P).classList.add(\"active\");
  $(T)?.classList.add(\"active\");

  if(which===\"profile\") renderProfile();
  if(which===\"admin\") renderAdminPanel();
  if(which===\"coachpanel\") renderCoachPanel();
  if(which===\"calc\") { loadCalcInputs(); renderCalcMode(); renderCalcResults(); renderSubscriberCalcView(); }
  if(which===\"work\") { renderWorkouts(); applyWorkButtons(); }
  if(which===\"week\") { buildWeekInputs(); loadWeekInputs(); syncWeeklyTarget(); recalcWeek(); applyWeekButtons(); }
  if(which===\"weight\"){ loadWeightTracker(); applyWeightButtons(); }
  if(which===\"macros\"){ renderMacrosPage(); }
  hydrateHeader();
}

/* ── Subscriber nav ── */
const _subNavLabels={
  profile:\"Profile\",
  calc:\"Calculator\",
  work:\"Workouts\",
  week:\"Daily Burn\",
  weight:\"Weight Tracker\",
  macros:\"Macros\",
  notes:\"Weekly Notes\",
  chat:\"Chat with Coach\"
};
const _subNavIcons={
  calc:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"16\" height=\"16\"><rect x=\"4\" y=\"2\" width=\"16\" height=\"20\" rx=\"2\" stroke=\"#a78bfa\" stroke-width=\"2\"/><path d=\"M8 7h8M8 12h4\" stroke=\"#a78bfa\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`,
  work:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"16\" height=\"16\"><path d=\"M6 4v16M18 4v16M3 9h18M3 15h18\" stroke=\"#38bdf8\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`,
  week:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"16\" height=\"16\"><rect x=\"3\" y=\"4\" width=\"18\" height=\"18\" rx=\"2\" stroke=\"#fb923c\" stroke-width=\"2\"/><path d=\"M16 2v4M8 2v4M3 10h18\" stroke=\"#fb923c\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`,
  weight:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"16\" height=\"16\"><path d=\"M3 6h18M3 12h18M3 18h18\" stroke=\"#34d399\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`,
  macros:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"16\" height=\"16\"><circle cx=\"12\" cy=\"12\" r=\"9\" stroke=\"#f472b6\" stroke-width=\"2\"/><path d=\"M12 8v8M8 12h8\" stroke=\"#f472b6\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`,
  notes:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"16\" height=\"16\"><path d=\"M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2\" stroke=\"#fbbf24\" stroke-width=\"2\" stroke-linecap=\"round\"/><rect x=\"9\" y=\"3\" width=\"6\" height=\"4\" rx=\"1\" stroke=\"#fbbf24\" stroke-width=\"2\"/><line x1=\"9\" y1=\"12\" x2=\"15\" y2=\"12\" stroke=\"#fbbf24\" stroke-width=\"2\" stroke-linecap=\"round\"/><line x1=\"9\" y1=\"16\" x2=\"13\" y2=\"16\" stroke=\"#fbbf24\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`,
  chat:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"16\" height=\"16\"><path d=\"M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z\" stroke=\"#4ade80\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>`
};

function subNavGo(which){
  /* update active state on top nav */
  document.querySelectorAll(\".sub-nav-btn\").forEach(b=>b.classList.remove(\"active\"));
  const btnId={profile:\"snProfile\",calc:\"snCalc\",work:\"snWork\",week:\"snWeek\",weight:\"snWeight\",macros:\"snMacros\",notes:\"snNotes\",chat:\"snChat\"};
  const activeBtn=$(btnId[which]); if(activeBtn) activeBtn.classList.add(\"active\");

  if(which===\"profile\"){
    /* back to profile — hide back bar */
    $(\"subBackBar\").classList.remove(\"visible\");
    go(\"profile\");
    return;
  }

  /* Notes and Chat: open full-screen overlays */
  if(which===\"notes\"){ pfOpenNotesPage(); _subNavSetBack(which); return; }
  if(which===\"chat\"){  pfOpenChatFromProfile(); _subNavSetBack(which); return; }

  /* Regular pages: navigate + show back bar */
  _subNavSetBack(which);
  go(which);
}

function _subNavSetBack(which){
  const bar=$(\"subBackBar\"); if(!bar) return;
  bar.classList.add(\"visible\");
  const title=$(\"subBackTitle\"); if(!title) return;
  const icon=_subNavIcons[which]||\"\";
  title.innerHTML=icon+\" \"+(_subNavLabels[which]||\"\");
}

function subNavBack(){
  /* close any overlay first */
  const notesOv=$(\"pfNotesOverlay\"); if(notesOv){ pfCloseNotesPage(); }
  const chatOv=$(\"pfChatOverlay\");   if(chatOv){ pfCloseChatPage(); }
  /* reset active to profile */
  document.querySelectorAll(\".sub-nav-btn\").forEach(b=>b.classList.remove(\"active\"));
  const snP=$(\"snProfile\"); if(snP) snP.classList.add(\"active\");
  $(\"subBackBar\").classList.remove(\"visible\");
  go(\"profile\");
}"""

if OLD_GO_FUNC in html:
    html = html.replace(OLD_GO_FUNC, NEW_GO_FUNC)
    ok.append("✅ subNavGo + subNavBack + _subNavSetBack added")
else:
    fail.append("❌ go() function not found")

# ══════════════════════════════════════════════════════════════════
# 5. Update pfOpenNotesPage + pfOpenChatPage to call subNavBack on close
#    (so back bar resets when overlay is closed)
# ══════════════════════════════════════════════════════════════════

OLD_CLOSE_NOTES = """function pfCloseNotesPage(){
  const overlay=$(\"pfNotesOverlay\"); if(!overlay) return;
  overlay.classList.remove(\"open\");
  overlay.addEventListener(\"transitionend\",()=>overlay.remove(),{once:true});
}"""

NEW_CLOSE_NOTES = """function pfCloseNotesPage(){
  const overlay=$(\"pfNotesOverlay\"); if(!overlay) return;
  overlay.classList.remove(\"open\");
  overlay.addEventListener(\"transitionend\",()=>overlay.remove(),{once:true});
  /* reset back bar */
  document.querySelectorAll(\".sub-nav-btn\").forEach(b=>b.classList.remove(\"active\"));
  const snP=$(\"snProfile\"); if(snP) snP.classList.add(\"active\");
  const bar=$(\"subBackBar\"); if(bar) bar.classList.remove(\"visible\");
}"""

if OLD_CLOSE_NOTES in html:
    html = html.replace(OLD_CLOSE_NOTES, NEW_CLOSE_NOTES)
    ok.append("✅ pfCloseNotesPage resets back bar")
else:
    fail.append("❌ pfCloseNotesPage not found")

OLD_CLOSE_CHAT_PF = """function pfCloseChatPage(){
  const overlay=$(\"pfChatOverlay\"); if(!overlay) return;
  overlay.classList.remove(\"open\");
  overlay.addEventListener(\"transitionend\",()=>overlay.remove(),{once:true});
  if(_pfChatPoll){ clearInterval(_pfChatPoll); _pfChatPoll=null; }
  /* update entry card preview */
  pfRenderNotesChat();
}"""

NEW_CLOSE_CHAT_PF = """function pfCloseChatPage(){
  const overlay=$(\"pfChatOverlay\"); if(!overlay) return;
  overlay.classList.remove(\"open\");
  overlay.addEventListener(\"transitionend\",()=>overlay.remove(),{once:true});
  if(_pfChatPoll){ clearInterval(_pfChatPoll); _pfChatPoll=null; }
  /* reset back bar */
  document.querySelectorAll(\".sub-nav-btn\").forEach(b=>b.classList.remove(\"active\"));
  const snP=$(\"snProfile\"); if(snP) snP.classList.add(\"active\");
  const bar=$(\"subBackBar\"); if(bar) bar.classList.remove(\"visible\");
  /* update entry card preview */
  pfRenderNotesChat();
}"""

if OLD_CLOSE_CHAT_PF in html:
    html = html.replace(OLD_CLOSE_CHAT_PF, NEW_CLOSE_CHAT_PF)
    ok.append("✅ pfCloseChatPage resets back bar")
else:
    fail.append("❌ pfCloseChatPage not found")

# ══════════════════════════════════════════════════════════════════
# 6. Remove the old icon grid from profile (pfSubIconGrid HTML)
#    since top nav replaces it
# ══════════════════════════════════════════════════════════════════

OLD_ICON_GRID_HTML = """  <!-- Subscriber Quick-Access Icon Grid (only shown for subscribers) -->
  <div id="pfSubIconGrid" style="display:none">
    <div class="pf-icon-grid-title">Quick Access</div>
    <div class="pf-icon-grid" id="pfIconGridInner"></div>
  </div>

  <!-- Notes & Chat cards (visible to subscribers + coaches on their own profile) -->"""

NEW_ICON_GRID_HTML = """  <!-- Notes & Chat cards (visible to subscribers + coaches on their own profile) -->"""

if OLD_ICON_GRID_HTML in html:
    html = html.replace(OLD_ICON_GRID_HTML, NEW_ICON_GRID_HTML)
    ok.append("✅ Old icon grid div removed from HTML")
else:
    fail.append("❌ pfSubIconGrid HTML not found in profile")

# ══════════════════════════════════════════════════════════════════
# Write
# ══════════════════════════════════════════════════════════════════
with open("index.html","w",encoding="utf-8") as f:
    f.write(html)

for m in ok:   print(m)
for m in fail: print(m)
print(f"\n📦 {original_len} → {len(html)} chars, {html.count(chr(10))+1} lines")
