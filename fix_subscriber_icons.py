#!/usr/bin/env python3
"""
fix_subscriber_icons.py
- Remove subTopNav bar + subBackBar (CSS + HTML + JS)
- Add icon grid directly inside Profile page HTML (subscriber-only)
- Restore original tabs for coach/admin (show all normal tabs)
- Back button: inject a sticky back-bar inside each sub-page 
  (only visible when subscriber navigates from icon grid)
"""

import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

original_len = len(html)

# ─────────────────────────────────────────────────────────────
# 1. Remove old #subTopNav CSS block
# ─────────────────────────────────────────────────────────────
html = html.replace(
    """  #subTopNav{
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
  }""",
    """  /* ── Subscriber page back bar (inside pages) ── */
  #subPageBackBar{
    display:none;
    align-items:center; gap:10px;
    padding:10px 14px 8px;
    background:rgba(6,12,25,.97);
    border-bottom:1px solid rgba(255,255,255,.06);
    position:sticky; top:0; z-index:199;
    backdrop-filter:blur(14px);
    margin-bottom:4px;
  }
  #subPageBackBar.visible{ display:flex; }
  .sub-back-btn{
    width:34px; height:34px; border-radius:11px; border:none;
    background:rgba(255,255,255,.06); color:#94a3b8;
    display:flex; align-items:center; justify-content:center;
    cursor:pointer; flex-shrink:0; transition:background .15s;
  }
  .sub-back-btn:active{ background:rgba(255,255,255,.12); }
  #subPageBackTitle{
    font-size:14px; font-weight:900; color:#e2e8f0;
    display:flex; align-items:center; gap:7px;
  }"""
)

# ─────────────────────────────────────────────────────────────
# 2. Remove subTopNav HTML block + subBackBar HTML block
# ─────────────────────────────────────────────────────────────
# Find and remove the subTopNav div
idx_start = html.find('<!-- Subscriber Top Navigation Bar -->')
idx_end   = html.find('<!-- Back bar (shown when subscriber is inside a page) -->')
if idx_start != -1 and idx_end != -1:
    html = html[:idx_start] + html[idx_end:]

# Now remove the Back bar div
old_back_bar = """<!-- Back bar (shown when subscriber is inside a page) -->
<div id="subBackBar">
  <button class="sub-back-btn" onclick="subNavBack()">
    <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
      <path d="M19 12H5M12 5l-7 7 7 7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </button>
  <div id="subBackTitle">—</div>
</div>

"""
html = html.replace(old_back_bar, "")

# ─────────────────────────────────────────────────────────────
# 3. Add #subPageBackBar + icon grid div inside profile HTML
#    Insert right before the Notes & Chat cards section
# ─────────────────────────────────────────────────────────────
ICON_GRID_HTML = """
  <!-- Subscriber Icon Grid (shown only for subscribers) -->
  <div id="pfSubIconGrid" style="display:none">
    <div class="pf-card-title" style="margin-bottom:14px;padding-bottom:0;border-bottom:none;font-size:11px">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="#38bdf8" stroke-width="2"/><path d="M8 12h8M12 8v8" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/></svg>
      Quick Access
    </div>
    <div class="pf-icon-grid" id="pfIconGridInner"></div>
  </div>

"""

html = html.replace(
    """  <!-- Notes & Chat cards (visible to subscribers + coaches on their own profile) -->""",
    ICON_GRID_HTML + """  <!-- Notes & Chat cards (visible to subscribers + coaches on their own profile) -->"""
)

# ─────────────────────────────────────────────────────────────
# 4. Add #subPageBackBar before the tabs div (shared for all pages)
# ─────────────────────────────────────────────────────────────
html = html.replace(
    '<div class="tabs" id="tabs" style="display:none;">',
    """<!-- Subscriber back bar shown when inside a page -->
<div id="subPageBackBar">
  <button class="sub-back-btn" onclick="subPageBack()">
    <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
      <path d="M19 12H5M12 5l-7 7 7 7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </button>
  <div id="subPageBackTitle">—</div>
</div>

<div class="tabs" id="tabs" style="display:none;">"""
)

# ─────────────────────────────────────────────────────────────
# 5. Update showApp() — restore tabs for coach/admin, 
#    hide tabs for subscriber (no top bar, profile page shows icons)
# ─────────────────────────────────────────────────────────────
html = html.replace(
    """function showApp(){
  $("pLogin").classList.remove("active");
  const isMember=isSub()||isUser();
  if(isMember){
    /* Subscriber: show top icon nav, hide old text tabs */
    $("tabs").style.display="none";
    $("subTopNav").style.display="flex";
  } else {
    /* Coach/Admin: show old tabs, hide subscriber nav */
    $("tabs").style.display="flex";
    $("subTopNav").style.display="none";
    $("subBackBar").classList.remove("visible");
  }
  $("tAdmin").classList.toggle("hidden", !isAdmin());
  $("tCoachPanel").classList.toggle("hidden", !(isCoach() || isAdmin()));
  hydrateHeader();
  go("profile");
}""",
    """function showApp(){
  $("pLogin").classList.remove("active");
  const isMember=isSub()||isUser();
  if(isMember){
    /* Subscriber: hide old text tabs, show icon grid on profile */
    $("tabs").style.display="none";
    const spb=$("subPageBackBar"); if(spb) spb.classList.remove("visible");
  } else {
    /* Coach/Admin: show normal tabs */
    $("tabs").style.display="flex";
    const spb=$("subPageBackBar"); if(spb) spb.classList.remove("visible");
    /* Make sure all page tabs visible for coach/admin */
    ["tCalc","tWork","tWeek","tWeight","tMacros"].forEach(id=>{
      const el=$(id); if(el){ el.classList.remove("hidden"); el.style.display=""; }
    });
  }
  $("tAdmin").classList.toggle("hidden", !isAdmin());
  $("tCoachPanel").classList.toggle("hidden", !(isCoach() || isAdmin()));
  hydrateHeader();
  go("profile");
}"""
)

# ─────────────────────────────────────────────────────────────
# 6. Replace old subNavGo / _subNavSetBack / subNavBack + 
#    _subNavLabels / _subNavIcons with new clean functions
# ─────────────────────────────────────────────────────────────
OLD_SUB_NAV = """/* ── Subscriber nav ── */
const _subNavLabels={
  profile:"Profile",
  calc:"Calculator",
  work:"Workouts",
  week:"Daily Burn",
  weight:"Weight Tracker",
  macros:"Macros",
  notes:"Weekly Notes",
  chat:"Chat with Coach"
};
const _subNavIcons={
  calc:`<svg viewBox="0 0 24 24" fill="none" width="16" height="16"><rect x="4" y="2" width="16" height="20" rx="2" stroke="#a78bfa" stroke-width="2"/><path d="M8 7h8M8 12h4" stroke="#a78bfa" stroke-width="2" stroke-linecap="round"/></svg>`,
  work:`<svg viewBox="0 0 24 24" fill="none" width="16" height="16"><path d="M6 4v16M18 4v16M3 9h18M3 15h18" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/></svg>`,
  week:`<svg viewBox="0 0 24 24" fill="none" width="16" height="16"><rect x="3" y="4" width="18" height="18" rx="2" stroke="#fb923c" stroke-width="2"/><path d="M16 2v4M8 2v4M3 10h18" stroke="#fb923c" stroke-width="2" stroke-linecap="round"/></svg>`,
  weight:`<svg viewBox="0 0 24 24" fill="none" width="16" height="16"><path d="M3 6h18M3 12h18M3 18h18" stroke="#34d399" stroke-width="2" stroke-linecap="round"/></svg>`,
  macros:`<svg viewBox="0 0 24 24" fill="none" width="16" height="16"><circle cx="12" cy="12" r="9" stroke="#f472b6" stroke-width="2"/><path d="M12 8v8M8 12h8" stroke="#f472b6" stroke-width="2" stroke-linecap="round"/></svg>`,
  notes:`<svg viewBox="0 0 24 24" fill="none" width="16" height="16"><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2" stroke="#fbbf24" stroke-width="2" stroke-linecap="round"/><rect x="9" y="3" width="6" height="4" rx="1" stroke="#fbbf24" stroke-width="2"/><line x1="9" y1="12" x2="15" y2="12" stroke="#fbbf24" stroke-width="2" stroke-linecap="round"/><line x1="9" y1="16" x2="13" y2="16" stroke="#fbbf24" stroke-width="2" stroke-linecap="round"/></svg>`,
  chat:`<svg viewBox="0 0 24 24" fill="none" width="16" height="16"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="#4ade80" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`
};

function subNavGo(which){
  /* update active state on top nav */
  document.querySelectorAll(".sub-nav-btn").forEach(b=>b.classList.remove("active"));
  const btnId={profile:"snProfile",calc:"snCalc",work:"snWork",week:"snWeek",weight:"snWeight",macros:"snMacros",notes:"snNotes",chat:"snChat"};
  const activeBtn=$(btnId[which]); if(activeBtn) activeBtn.classList.add("active");

  if(which==="profile"){
    /* back to profile — hide back bar */
    $("subBackBar").classList.remove("visible");
    go("profile");
    return;
  }

  /* Notes and Chat: open full-screen overlays */
  if(which==="notes"){ pfOpenNotesPage(); _subNavSetBack(which); return; }
  if(which==="chat"){  pfOpenChatFromProfile(); _subNavSetBack(which); return; }

  /* Regular pages: navigate + show back bar */
  _subNavSetBack(which);
  go(which);
}

function _subNavSetBack(which){
  const bar=$("subBackBar"); if(!bar) return;
  bar.classList.add("visible");
  const title=$("subBackTitle"); if(!title) return;
  const icon=_subNavIcons[which]||"";
  title.innerHTML=icon+" "+(_subNavLabels[which]||"");
}

function subNavBack(){
  /* close any overlay first */
  const notesOv=$("pfNotesOverlay"); if(notesOv){ pfCloseNotesPage(); }
  const chatOv=$("pfChatOverlay");   if(chatOv){ pfCloseChatPage(); }
  /* reset active to profile */
  document.querySelectorAll(".sub-nav-btn").forEach(b=>b.classList.remove("active"));
  const snP=$("snProfile"); if(snP) snP.classList.add("active");
  $("subBackBar").classList.remove("visible");
  go("profile");
}"""

NEW_SUB_NAV = """/* ── Subscriber page navigation ── */
const _subPageLabels={
  calc:"Calculator",
  work:"Workouts",
  week:"Daily Burn",
  weight:"Weight Tracker",
  macros:"Macros",
  notes:"Weekly Notes",
  chat:"Chat with Coach"
};
const _subPageIconsSvg={
  calc:`<svg viewBox="0 0 24 24" fill="none" width="16" height="16"><rect x="4" y="2" width="16" height="20" rx="2" stroke="#a78bfa" stroke-width="2"/><path d="M8 7h8M8 12h4" stroke="#a78bfa" stroke-width="2" stroke-linecap="round"/></svg>`,
  work:`<svg viewBox="0 0 24 24" fill="none" width="16" height="16"><path d="M6 4v16M18 4v16M3 9h18M3 15h18" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/></svg>`,
  week:`<svg viewBox="0 0 24 24" fill="none" width="16" height="16"><rect x="3" y="4" width="18" height="18" rx="2" stroke="#fb923c" stroke-width="2"/><path d="M16 2v4M8 2v4M3 10h18" stroke="#fb923c" stroke-width="2" stroke-linecap="round"/></svg>`,
  weight:`<svg viewBox="0 0 24 24" fill="none" width="16" height="16"><path d="M3 6h18M3 12h18M3 18h18" stroke="#34d399" stroke-width="2" stroke-linecap="round"/></svg>`,
  macros:`<svg viewBox="0 0 24 24" fill="none" width="16" height="16"><circle cx="12" cy="12" r="9" stroke="#f472b6" stroke-width="2"/><path d="M12 8v8M8 12h8" stroke="#f472b6" stroke-width="2" stroke-linecap="round"/></svg>`,
  notes:`<svg viewBox="0 0 24 24" fill="none" width="16" height="16"><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2" stroke="#fbbf24" stroke-width="2" stroke-linecap="round"/><rect x="9" y="3" width="6" height="4" rx="1" stroke="#fbbf24" stroke-width="2"/></svg>`,
  chat:`<svg viewBox="0 0 24 24" fill="none" width="16" height="16"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="#4ade80" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`
};

/* Called from subscriber icon grid */
function subIconGo(which){
  if(which==="notes"){ pfOpenNotesPage(); return; }
  if(which==="chat"){  pfOpenChatFromProfile(); return; }
  _showSubPageBack(which);
  go(which);
}

function _showSubPageBack(which){
  const bar=$("subPageBackBar"); if(!bar) return;
  bar.classList.add("visible");
  const title=$("subPageBackTitle"); if(!title) return;
  const icon=_subPageIconsSvg[which]||"";
  title.innerHTML=icon+" "+(_subPageLabels[which]||"");
}

function subPageBack(){
  const notesOv=$("pfNotesOverlay"); if(notesOv) pfCloseNotesPage();
  const chatOv=$("pfChatOverlay");   if(chatOv)  pfCloseChatPage();
  const bar=$("subPageBackBar"); if(bar) bar.classList.remove("visible");
  go("profile");
}

/* keep old names as aliases in case called elsewhere */
function subNavBack(){ subPageBack(); }"""

html = html.replace(OLD_SUB_NAV, NEW_SUB_NAV)

# ─────────────────────────────────────────────────────────────
# 7. Update pfRenderSubIconGrid — change action calls to subIconGo
#    Also show for subscriber and hide subTopNav references
# ─────────────────────────────────────────────────────────────
html = html.replace(
    "      action:()=>go(\"calc\"),",
    "      action:()=>subIconGo(\"calc\"),"
)
html = html.replace(
    "      action:()=>go(\"work\"),",
    "      action:()=>subIconGo(\"work\"),"
)
html = html.replace(
    "      action:()=>go(\"week\"),",
    "      action:()=>subIconGo(\"week\"),"
)
html = html.replace(
    "      action:()=>go(\"weight\"),",
    "      action:()=>subIconGo(\"weight\"),"
)
html = html.replace(
    "      action:()=>go(\"macros\"),",
    "      action:()=>subIconGo(\"macros\"),"
)
html = html.replace(
    "      action:()=>pfOpenNotesPage(),",
    "      action:()=>subIconGo(\"notes\"),"
)
html = html.replace(
    "      action:()=>pfOpenChatFromProfile(),",
    "      action:()=>subIconGo(\"chat\"),"
)

# ─────────────────────────────────────────────────────────────
# 8. Fix pfRenderSubIconGrid — show grid properly, remove old subTopNav ref
# ─────────────────────────────────────────────────────────────
html = html.replace(
    """function pfRenderSubIconGrid(){
  const grid=$("pfSubIconGrid");
  if(!grid) return;
  const a=me(); if(!a) return;

  /* only show for subscribers */
  if(a.role!=="subscriber" && a.role!=="user"){
    grid.style.display="none"; return;
  }
  grid.style.display="";""",
    """function pfRenderSubIconGrid(){
  const grid=$("pfSubIconGrid");
  if(!grid) return;
  const a=me(); if(!a) return;

  /* only show for subscribers/users */
  if(a.role!=="subscriber" && a.role!=="user"){
    grid.style.display="none"; return;
  }
  grid.style.display="block";"""
)

# ─────────────────────────────────────────────────────────────
# 9. Fix pfCloseNotesPage — remove subBackBar reference, use subPageBackBar
# ─────────────────────────────────────────────────────────────
html = html.replace(
    '  document.querySelectorAll(".sub-nav-btn").forEach(b=>b.classList.remove("active"));\n  const snP=$("snProfile"); if(snP) snP.classList.add("active");\n  const bar2=$("subBackBar"); if(bar2) bar2.classList.remove("visible");',
    '  const bar2=$("subPageBackBar"); if(bar2) bar2.classList.remove("visible");'
)

# Fix all remaining subBackBar references in pfCloseNotesPage and pfCloseChatPage
html = html.replace(
    '  const bar=$("subBackBar"); if(bar) bar.classList.remove("visible");\n  go("profile");',
    '  const spb=$("subPageBackBar"); if(spb) spb.classList.remove("visible");\n  go("profile");'
)

# Generic cleanup of any remaining subBackBar references
html = html.replace('$("subBackBar")', '$("subPageBackBar")')
html = html.replace('"subBackBar"', '"subPageBackBar"')
html = html.replace('subBackBar', 'subPageBackBar')

# Fix subBackTitle references
html = html.replace('$("subBackTitle")', '$("subPageBackTitle")')
html = html.replace('"subBackTitle"', '"subPageBackTitle"')
html = html.replace('id="subBackTitle"', 'id="subPageBackTitle"')

# ─────────────────────────────────────────────────────────────
# 10. Fix tabs — make Calc, Work, Week, Weight, Macros visible 
#     by default (remove hidden class from them)
# ─────────────────────────────────────────────────────────────
# These tabs should be visible for coach/admin
html = html.replace(
    '  <button class="tab hidden" id="tCalc" onclick="go(\'calc\')">Calculator</button>',
    '  <button class="tab" id="tCalc" onclick="go(\'calc\')">Calculator</button>'
)
html = html.replace(
    '  <button class="tab hidden" id="tWork" onclick="go(\'work\')">Workouts</button>',
    '  <button class="tab" id="tWork" onclick="go(\'work\')">Workouts</button>'
)
html = html.replace(
    '  <button class="tab hidden" id="tWeek" onclick="go(\'week\')">Daily Burn</button>',
    '  <button class="tab" id="tWeek" onclick="go(\'week\')">Daily Burn</button>'
)
html = html.replace(
    '  <button class="tab hidden" id="tWeight" onclick="go(\'weight\')">Weight</button>',
    '  <button class="tab" id="tWeight" onclick="go(\'weight\')">Weight</button>'
)
html = html.replace(
    '  <button class="tab hidden" id="tMacros" onclick="go(\'macros\')">Macros</button>',
    '  <button class="tab" id="tMacros" onclick="go(\'macros\')">Macros</button>'
)

# ─────────────────────────────────────────────────────────────
# 11. Fix pfCloseChatPage / pfCloseNotesPage remaining subNavBtn refs
# ─────────────────────────────────────────────────────────────
# Remove any remaining .sub-nav-btn references in close functions
html = re.sub(
    r"  document\.querySelectorAll\(\"\.sub-nav-btn\"\)\.forEach\(b=>b\.classList\.remove\(\"active\"\)\);\s*",
    "",
    html
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

new_len = len(html)
print(f"Done. {original_len} → {new_len} chars ({new_len - original_len:+d})")

# Verify key elements
checks = [
    ("subPageBackBar in HTML", 'id="subPageBackBar"'),
    ("pfSubIconGrid in HTML", 'id="pfSubIconGrid"'),
    ("subIconGo function", 'function subIconGo('),
    ("subPageBack function", 'function subPageBack('),
    ("subTopNav removed", 'id="subTopNav"'),  # should be gone
    ("tabs restored", 'id="tCalc"'),
    ("pfRenderSubIconGrid", 'function pfRenderSubIconGrid('),
    ("No old subNavGo", 'function subNavGo('),  # should be gone
]
print("\nVerification:")
for label, pattern in checks:
    found = pattern in html
    if "removed" in label or "No old" in label:
        status = "✓ REMOVED" if not found else "✗ STILL PRESENT"
    else:
        status = "✓ FOUND" if found else "✗ MISSING"
    print(f"  {status}: {label}")
