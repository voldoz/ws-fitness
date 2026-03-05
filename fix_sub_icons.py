#!/usr/bin/env python3
"""
Add icon grid to subscriber profile page — same design as coach's Overview.
All pages (Calc, Workouts, Daily Burn, Weight, Macros, Notes, Chat) shown as icon buttons.
"""

with open("index.html","r",encoding="utf-8") as f:
    html = f.read()

original_len = len(html)

# ══════════════════════════════════════════════════════════════════
# 1. Add subscriber icon grid HTML inside pProfile page
#    Insert AFTER pfSubCard and BEFORE pfNotesCard
# ══════════════════════════════════════════════════════════════════

OLD_NOTES_CARD_HTML = """  <!-- Notes & Chat cards (visible to subscribers + coaches on their own profile) -->
  <div class="pf-card" id="pfNotesCard" style="display:none">"""

NEW_NOTES_CARD_HTML = """  <!-- Subscriber Quick-Access Icon Grid (only shown for subscribers) -->
  <div id="pfSubIconGrid" style="display:none">
    <div class="pf-icon-grid-title">Quick Access</div>
    <div class="pf-icon-grid" id="pfIconGridInner"></div>
  </div>

  <!-- Notes & Chat cards (visible to subscribers + coaches on their own profile) -->
  <div class="pf-card" id="pfNotesCard" style="display:none">"""

if OLD_NOTES_CARD_HTML in html:
    html = html.replace(OLD_NOTES_CARD_HTML, NEW_NOTES_CARD_HTML)
    print("✅ pfSubIconGrid HTML inserted before pfNotesCard")
else:
    print("❌ pfNotesCard HTML not found")

# ══════════════════════════════════════════════════════════════════
# 2. Add CSS for the icon grid
# ══════════════════════════════════════════════════════════════════

OLD_PF_CARD_CSS = """  .pf-card{
    background:linear-gradient(145deg,#0d1829,#111e30);
    border-radius:20px; padding:18px; margin-bottom:12px;
    border:1.5px solid rgba(255,255,255,.06);
    animation:pf-rise .38s cubic-bezier(.22,1,.36,1) both;
  }"""

NEW_PF_CARD_CSS = """  .pf-card{
    background:linear-gradient(145deg,#0d1829,#111e30);
    border-radius:20px; padding:18px; margin-bottom:12px;
    border:1.5px solid rgba(255,255,255,.06);
    animation:pf-rise .38s cubic-bezier(.22,1,.36,1) both;
  }

  /* ── Subscriber icon grid ── */
  #pfSubIconGrid{ padding:0 0 4px; }
  .pf-icon-grid-title{
    font-size:10px; font-weight:800; color:#3d5068;
    text-transform:uppercase; letter-spacing:.08em;
    padding:0 4px 10px;
  }
  .pf-icon-grid{
    display:grid; grid-template-columns:repeat(4,1fr); gap:8px;
    margin-bottom:12px;
  }
  .pf-icon-btn{
    background:linear-gradient(145deg,#09162a,#0d1e34);
    border:1.5px solid rgba(255,255,255,.07);
    border-radius:16px; padding:14px 6px;
    cursor:pointer; display:flex; flex-direction:column;
    align-items:center; gap:8px;
    transition:all .22s; -webkit-tap-highlight-color:transparent;
  }
  .pf-icon-btn:active{ transform:scale(.93); }
  .pf-icon-btn-icon{
    width:40px; height:40px; border-radius:12px;
    display:flex; align-items:center; justify-content:center;
    border-width:1px; border-style:solid;
  }
  .pf-icon-btn-lbl{
    font-size:10px; font-weight:800; color:#94a3b8; letter-spacing:.02em;
  }"""

if OLD_PF_CARD_CSS in html:
    html = html.replace(OLD_PF_CARD_CSS, NEW_PF_CARD_CSS)
    print("✅ Subscriber icon grid CSS added")
else:
    print("❌ .pf-card CSS not found")

# ══════════════════════════════════════════════════════════════════
# 3. In renderProfile(), build the icon grid for subscribers
#    Insert after pfRenderNotesChat() call
# ══════════════════════════════════════════════════════════════════

OLD_RENDER_PROFILE_END = """  /* ── notes & chat for subscribers ── */
  pfRenderNotesChat();

  /* ── clear msgs ── */
  $(\"pfNameMsg\").textContent=''; $(\"pfPinMsg\").textContent='';
  if($(\"pfNewPin\")) $(\"pfNewPin\").value='';
}"""

NEW_RENDER_PROFILE_END = """  /* ── notes & chat for subscribers ── */
  pfRenderNotesChat();

  /* ── subscriber icon grid ── */
  pfRenderSubIconGrid();

  /* ── clear msgs ── */
  $(\"pfNameMsg\").textContent=''; $(\"pfPinMsg\").textContent='';
  if($(\"pfNewPin\")) $(\"pfNewPin\").value='';
}

function pfRenderSubIconGrid(){
  const grid=$(\"pfSubIconGrid\");
  if(!grid) return;
  const a=me(); if(!a) return;

  /* only show for subscribers */
  if(a.role!==\"subscriber\" && a.role!==\"user\"){
    grid.style.display=\"none\"; return;
  }
  grid.style.display=\"\";

  const inner=$(\"pfIconGridInner\"); if(!inner) return;

  const items=[
    {
      action:()=>go(\"calc\"),
      icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><rect x=\"4\" y=\"2\" width=\"16\" height=\"20\" rx=\"2\" stroke=\"currentColor\" stroke-width=\"2\"/><path d=\"M8 7h8M8 12h4M8 17h4M16 17l2 2 4-4\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`,
      label:\"Calculator\", color:\"#a78bfa\"
    },
    {
      action:()=>go(\"work\"),
      icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><path d=\"M6 4v16M18 4v16M3 9h18M3 15h18\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`,
      label:\"Workouts\", color:\"#38bdf8\"
    },
    {
      action:()=>go(\"week\"),
      icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><rect x=\"3\" y=\"4\" width=\"18\" height=\"18\" rx=\"2\" stroke=\"currentColor\" stroke-width=\"2\"/><path d=\"M16 2v4M8 2v4M3 10h18\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`,
      label:\"Daily Burn\", color:\"#fb923c\"
    },
    {
      action:()=>go(\"weight\"),
      icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><path d=\"M3 6h18M3 12h18M3 18h18\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`,
      label:\"Weight\", color:\"#34d399\"
    },
    {
      action:()=>go(\"macros\"),
      icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><circle cx=\"12\" cy=\"12\" r=\"9\" stroke=\"currentColor\" stroke-width=\"2\"/><path d=\"M12 8v8M8 12h8\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`,
      label:\"Macros\", color:\"#f472b6\"
    },
    {
      action:()=>pfOpenNotesPage(),
      icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><path d=\"M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/><rect x=\"9\" y=\"3\" width=\"6\" height=\"4\" rx=\"1\" stroke=\"currentColor\" stroke-width=\"2\"/><line x1=\"9\" y1=\"12\" x2=\"15\" y2=\"12\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/><line x1=\"9\" y1=\"16\" x2=\"13\" y2=\"16\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`,
      label:\"Notes\", color:\"#fbbf24\"
    },
    {
      action:()=>pfOpenChatFromProfile(),
      icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><path d=\"M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/><line x1=\"9\" y1=\"10\" x2=\"15\" y2=\"10\" stroke=\"currentColor\" stroke-width=\"1.5\" stroke-linecap=\"round\"/><line x1=\"9\" y1=\"14\" x2=\"12\" y2=\"14\" stroke=\"currentColor\" stroke-width=\"1.5\" stroke-linecap=\"round\"/></svg>`,
      label:\"Chat\", color:\"#4ade80\"
    },
  ];

  inner.innerHTML=\"\";
  items.forEach(item=>{
    const btn=document.createElement(\"button\");
    btn.className=\"pf-icon-btn\";
    btn.innerHTML=`
      <span class=\"pf-icon-btn-icon\" style=\"background:${item.color}18;border-color:${item.color}30;color:${item.color}\">${item.icon}</span>
      <span class=\"pf-icon-btn-lbl\">${item.label}</span>`;
    btn.addEventListener(\"click\", item.action);
    inner.appendChild(btn);
  });
}

/* open Notes as full-screen overlay for subscriber */
function pfOpenNotesPage(){
  const a=me(); if(!a) return;
  const sub=findAccById(getManagedId()); if(!sub||!sub.coachId) return;
  const coachId=sub.coachId;

  const old=$(\"pfNotesOverlay\"); if(old) old.remove();
  const overlay=document.createElement(\"div\");
  overlay.id=\"pfNotesOverlay\";
  overlay.className=\"pf-chat-overlay\"; /* reuse same slide-in style */
  overlay.innerHTML=`
    <div class=\"pf-chat-overlay-bar\">
      <button class=\"pf-chat-overlay-back\" onclick=\"pfCloseNotesPage()\">
        <svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\">
          <path d=\"M19 12H5M12 5l-7 7 7 7\" stroke=\"currentColor\" stroke-width=\"2.2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/>
        </svg>
      </button>
      <div class=\"pf-chat-overlay-title\">
        <svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"18\" height=\"18\" style=\"flex-shrink:0\">
          <path d=\"M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2\" stroke=\"#fbbf24\" stroke-width=\"2\" stroke-linecap=\"round\"/>
          <rect x=\"9\" y=\"3\" width=\"6\" height=\"4\" rx=\"1\" stroke=\"#fbbf24\" stroke-width=\"2\"/>
          <line x1=\"9\" y1=\"12\" x2=\"15\" y2=\"12\" stroke=\"#fbbf24\" stroke-width=\"2\" stroke-linecap=\"round\"/>
          <line x1=\"9\" y1=\"16\" x2=\"13\" y2=\"16\" stroke=\"#fbbf24\" stroke-width=\"2\" stroke-linecap=\"round\"/>
        </svg>
        Weekly Notes
      </div>
    </div>
    <div style=\"flex:1;overflow-y:auto;padding:16px 12px 24px\" id=\"pfNotesOverlayBody\"></div>`;
  document.body.appendChild(overlay);
  requestAnimationFrame(()=>overlay.classList.add(\"open\"));

  /* build notes content */
  const body=$(\"pfNotesOverlayBody\");
  pfBuildSubNotes(body, sub, coachId);
}
function pfCloseNotesPage(){
  const overlay=$(\"pfNotesOverlay\"); if(!overlay) return;
  overlay.classList.remove(\"open\");
  overlay.addEventListener(\"transitionend\",()=>overlay.remove(),{once:true});
}

/* open Chat from profile icon grid */
function pfOpenChatFromProfile(){
  const a=me(); if(!a) return;
  const sub=findAccById(getManagedId()); if(!sub||!sub.coachId) return;
  pfOpenChatPage(sub.coachId, sub.id);
}"""

if OLD_RENDER_PROFILE_END in html:
    html = html.replace(OLD_RENDER_PROFILE_END, NEW_RENDER_PROFILE_END)
    print("✅ pfRenderSubIconGrid + pfOpenNotesPage + pfOpenChatFromProfile added")
else:
    print("❌ renderProfile end not found")
    idx = html.find("/* ── clear msgs ── */")
    print(f"   '/* ── clear msgs ── */' at line {html[:idx].count(chr(10))+1 if idx>=0 else 'NOT FOUND'}")

# ══════════════════════════════════════════════════════════════════
# 4. Hide the top tab bar (Calculator, Workouts, etc.) for subscribers
#    since they now use the icon grid inside Profile
#    We hide all tabs EXCEPT Profile, Admin, Subscribers for subscribers
# ══════════════════════════════════════════════════════════════════

OLD_SHOW_APP = """function showApp(){
  $(\"pLogin\").classList.remove(\"active\");
  $(\"tabs\").style.display=\"flex\";
  $(\"tAdmin\").classList.toggle(\"hidden\", !isAdmin());
  $(\"tCoachPanel\").classList.toggle(\"hidden\", !(isCoach() || isAdmin()));
  hydrateHeader();
  go(\"profile\");
}"""

NEW_SHOW_APP = """function showApp(){
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

if OLD_SHOW_APP in html:
    html = html.replace(OLD_SHOW_APP, NEW_SHOW_APP)
    print("✅ showApp: tab bar hidden for subscribers")
else:
    print("❌ showApp not found")

# ══════════════════════════════════════════════════════════════════
# Write
# ══════════════════════════════════════════════════════════════════
with open("index.html","w",encoding="utf-8") as f:
    f.write(html)

print(f"\n📦 {original_len} → {len(html)} chars, {html.count(chr(10))+1} lines")
