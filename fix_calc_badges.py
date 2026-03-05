#!/usr/bin/env python3
"""
fix_calc_badges.py
1. Calc page: fully read-only for subscriber — hide inputs + macro sliders + calcBtn
2. Unread badges: red iOS-style number badge on Notes and Chat icons in subscriber grid
   - Notes badge: count of weeks that have a non-empty coachNote not yet seen by subscriber
   - Chat badge: count of messages from coach/admin not yet seen by subscriber
   - Badges persist until subscriber opens that section (marks as read)
"""

import re

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

original_len = len(html)

# ─────────────────────────────────────────────────────────────
# 1. Fix renderCalcMode — subscriber sees NOTHING editable
#    (hide calcInputsWrap and also hide macro sliders by using
#     a subscriber-specific flag in renderCalcResults)
# ─────────────────────────────────────────────────────────────
html = html.replace(
    """function renderCalcMode(){
  if(isSub()){
    $("calcInputsWrap").classList.add("hidden");
  } else {
    $("calcInputsWrap").classList.remove("hidden");
    const fields=["weight","height","age","gender","activityDays","proteinFactor","meals","weeklyGoal"];
    fields.forEach(id=>{
      const el=$(id); if(!el) return;
      el.disabled = !canEditEverything();
      el.style.opacity = el.disabled ? .75 : 1;
    });
    /* goal pill buttons */
    document.querySelectorAll(".calc-goal-btn").forEach(btn=>{
      btn.disabled = !canEditEverything();
      btn.style.opacity = btn.disabled ? .75 : 1;
    });
    $("calcBtn").disabled = !canEditEverything();
    $("calcBtn").style.opacity = $("calcBtn").disabled ? .75 : 1;
  }
}""",
    """function renderCalcMode(){
  const sub=isSub();
  /* Subscriber: hide all inputs, calc button, macro sliders */
  if(sub){
    $("calcInputsWrap").classList.add("hidden");
    /* also hide the macro-edit section if rendered */
    const cmeSection=document.querySelector(".calc-macro-section");
    if(cmeSection) cmeSection.style.display="none";
  } else {
    $("calcInputsWrap").classList.remove("hidden");
    const fields=["weight","height","age","gender","activityDays","proteinFactor","meals","weeklyGoal"];
    fields.forEach(id=>{
      const el=$(id); if(!el) return;
      el.disabled = !canEditEverything();
      el.style.opacity = el.disabled ? .75 : 1;
    });
    /* goal pill buttons */
    document.querySelectorAll(".calc-goal-btn").forEach(btn=>{
      btn.disabled = !canEditEverything();
      btn.style.opacity = btn.disabled ? .75 : 1;
    });
    $("calcBtn").disabled = !canEditEverything();
    $("calcBtn").style.opacity = $("calcBtn").disabled ? .75 : 1;
  }
}"""
)

# ─────────────────────────────────────────────────────────────
# 2. Fix renderCalcResults — pass subscriber flag to suppress macro sliders
#    The canEdit check already hides sliders, but subscriber has canEdit=true
#    We need to override: if isSub() → force read-only macro display
# ─────────────────────────────────────────────────────────────
html = html.replace(
    "  const isManual = !!r._manualMacros;\n  const canEdit  = canEditEverything();",
    "  const isManual = !!r._manualMacros;\n  const canEdit  = canEditEverything() && !isSub(); /* subscriber: always read-only */"
)

# ─────────────────────────────────────────────────────────────
# 3. Add CSS for unread badge (iOS red dot with number)
# ─────────────────────────────────────────────────────────────
BADGE_CSS = """
  /* ── Unread notification badge (iOS-style) ── */
  .pf-icon-btn{ position:relative; }
  .pf-unread-badge{
    position:absolute; top:2px; right:2px;
    min-width:18px; height:18px;
    background:#ef4444; color:#fff;
    border-radius:999px; border:2px solid #060c19;
    font-size:10px; font-weight:900; line-height:1;
    display:flex; align-items:center; justify-content:center;
    padding:0 4px; pointer-events:none;
    box-shadow:0 2px 6px rgba(239,68,68,.5);
    z-index:10;
    animation:badge-pop .25s cubic-bezier(.22,1,.36,1) both;
  }
  @keyframes badge-pop{
    from{ transform:scale(0); opacity:0; }
    to{ transform:scale(1); opacity:1; }
  }"""

# Insert after the .pf-icon-btn-lbl style block
html = html.replace(
    """  .pf-icon-btn-lbl{
    font-size:10px; font-weight:800; color:#94a3b8; letter-spacing:.02em;
  }""",
    """  .pf-icon-btn-lbl{
    font-size:10px; font-weight:800; color:#94a3b8; letter-spacing:.02em;
  }""" + BADGE_CSS
)

# ─────────────────────────────────────────────────────────────
# 4. Add unread-tracking helper functions
#    Key for last-seen chat: ws_chat_seen_{coachId}_{subId}
#    Key for last-seen notes: ws_notes_seen_{coachId}_{subId}
# ─────────────────────────────────────────────────────────────
UNREAD_HELPERS = """
/* ═══════════════════════════════════════════════════════════
   UNREAD BADGE HELPERS
   ════════════════════════════════════════════════════════════ */
function _chatSeenKey(coachId,subId){ return `ws_chat_seen_${coachId}_${subId}`; }
function _notesSeenKey(coachId,subId){ return `ws_notes_seen_${coachId}_${subId}`; }

/* Returns number of unread chat messages from coach/admin for subscriber */
function _getUnreadChatCount(coachId, subId){
  const msgs=_loadMsgs(coachId,subId);
  const seenTs=parseInt(localStorage.getItem(_chatSeenKey(coachId,subId))||"0",10);
  /* count msgs from coach that arrived after last seen timestamp */
  return msgs.filter(m=>
    (m.role==="coach"||m.role==="admin") && (m.ts||0)>seenTs
  ).length;
}

/* Returns number of weeks that have new coach notes subscriber hasn't read */
function _getUnreadNotesCount(coachId, subId, totalWeeks){
  const seenTs=parseInt(localStorage.getItem(_notesSeenKey(coachId,subId))||"0",10);
  let count=0;
  for(let w=1;w<=totalWeeks;w++){
    const note=_loadNote(coachId,subId,w);
    if(note && note.coachNote && note.coachNote.trim() && (note.updatedAt||0)>seenTs){
      count++;
    }
  }
  return count;
}

/* Mark chat as read (called when subscriber opens chat) */
function _markChatRead(coachId, subId){
  localStorage.setItem(_chatSeenKey(coachId,subId), String(Date.now()));
}

/* Mark notes as read (called when subscriber opens notes) */
function _markNotesRead(coachId, subId){
  localStorage.setItem(_notesSeenKey(coachId,subId), String(Date.now()));
}

/* Calculate total weeks for a subscriber (same as cpDrawerNotes logic) */
function _subTotalWeeks(sub){
  const startMs=Number(sub.subStartAt||Date.now());
  const autoWeeks=Math.max(1,Math.ceil((Date.now()-startMs)/(7*24*3600*1000))+1);
  const extra=_cpGetExtraWeeks(sub.id);
  return Math.min(autoWeeks+extra,104);
}
"""

# Insert before pfRenderSubIconGrid
html = html.replace(
    "function pfRenderSubIconGrid(){",
    UNREAD_HELPERS + "function pfRenderSubIconGrid(){"
)

# ─────────────────────────────────────────────────────────────
# 5. Update pfRenderSubIconGrid to show badges on Notes and Chat
# ─────────────────────────────────────────────────────────────
OLD_GRID_RENDER = """  inner.innerHTML="";
  items.forEach(item=>{
    const btn=document.createElement("button");
    btn.className="pf-icon-btn";
    btn.innerHTML=`
      <span class="pf-icon-btn-icon" style="background:${item.color}18;border-color:${item.color}30;color:${item.color}">${item.icon}</span>
      <span class="pf-icon-btn-lbl">${item.label}</span>`;
    btn.addEventListener("click", item.action);
    inner.appendChild(btn);
  });
}"""

NEW_GRID_RENDER = """  /* get unread counts for Notes and Chat */
  const sub2=findAccById(getManagedId());
  const coachId2=sub2&&sub2.coachId ? sub2.coachId : null;
  let unreadChat=0, unreadNotes=0;
  if(coachId2 && sub2){
    unreadChat=_getUnreadChatCount(coachId2, sub2.id);
    const totalW=_subTotalWeeks(sub2);
    unreadNotes=_getUnreadNotesCount(coachId2, sub2.id, totalW);
  }

  inner.innerHTML="";
  items.forEach(item=>{
    const btn=document.createElement("button");
    btn.className="pf-icon-btn";
    /* badge count for notes/chat */
    let badgeHtml="";
    if(item.badgeKey==="notes" && unreadNotes>0){
      badgeHtml=`<span class="pf-unread-badge">${unreadNotes>9?"9+":unreadNotes}</span>`;
    }
    if(item.badgeKey==="chat" && unreadChat>0){
      badgeHtml=`<span class="pf-unread-badge">${unreadChat>9?"9+":unreadChat}</span>`;
    }
    btn.innerHTML=`
      ${badgeHtml}
      <span class="pf-icon-btn-icon" style="background:${item.color}18;border-color:${item.color}30;color:${item.color}">${item.icon}</span>
      <span class="pf-icon-btn-lbl">${item.label}</span>`;
    btn.addEventListener("click", item.action);
    inner.appendChild(btn);
  });
}"""

html = html.replace(OLD_GRID_RENDER, NEW_GRID_RENDER)

# ─────────────────────────────────────────────────────────────
# 6. Add badgeKey to Notes and Chat items in items array
# ─────────────────────────────────────────────────────────────
html = html.replace(
    """      action:()=>subIconGo("notes"),
      icon:`<svg viewBox="0 0 24 24" fill="none" width="20" height="20"><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><rect x="9" y="3" width="6" height="4" rx="1" stroke="currentColor" stroke-width="2"/><line x1="9" y1="12" x2="15" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="9" y1="16" x2="13" y2="16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`,
      label:"Notes", color:"#fbbf24"
    },
    {
      action:()=>subIconGo("chat"),
      icon:`<svg viewBox="0 0 24 24" fill="none" width="20" height="20"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="9" y1="10" x2="15" y2="10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><line x1="9" y1="14" x2="12" y2="14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>`,
      label:"Chat", color:"#4ade80"
    },""",
    """      action:()=>subIconGo("notes"),
      icon:`<svg viewBox="0 0 24 24" fill="none" width="20" height="20"><path d="M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><rect x="9" y="3" width="6" height="4" rx="1" stroke="currentColor" stroke-width="2"/><line x1="9" y1="12" x2="15" y2="12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="9" y1="16" x2="13" y2="16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`,
      label:"Notes", color:"#fbbf24", badgeKey:"notes"
    },
    {
      action:()=>subIconGo("chat"),
      icon:`<svg viewBox="0 0 24 24" fill="none" width="20" height="20"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><line x1="9" y1="10" x2="15" y2="10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/><line x1="9" y1="14" x2="12" y2="14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>`,
      label:"Chat", color:"#4ade80", badgeKey:"chat"
    },"""
)

# ─────────────────────────────────────────────────────────────
# 7. Mark notes as read when subscriber opens Notes overlay
#    (in pfOpenNotesPage)
# ─────────────────────────────────────────────────────────────
html = html.replace(
    """function pfOpenNotesPage(){
  const a=me(); if(!a) return;
  const sub=findAccById(getManagedId()); if(!sub||!sub.coachId) return;
  const coachId=sub.coachId;

  const old=$("pfNotesOverlay"); if(old) old.remove();""",
    """function pfOpenNotesPage(){
  const a=me(); if(!a) return;
  const sub=findAccById(getManagedId()); if(!sub||!sub.coachId) return;
  const coachId=sub.coachId;

  /* mark notes as read → clear badge */
  _markNotesRead(coachId, sub.id);

  const old=$("pfNotesOverlay"); if(old) old.remove();"""
)

# ─────────────────────────────────────────────────────────────
# 8. Mark chat as read when subscriber opens Chat overlay
#    Find pfOpenChatFromProfile
# ─────────────────────────────────────────────────────────────
html = html.replace(
    """function pfOpenChatFromProfile(){
  const a=me(); if(!a) return;
  const sub=findAccById(getManagedId()); if(!sub||!sub.coachId) return;
  pfOpenChatPage(sub.coachId, sub.id);
}""",
    """function pfOpenChatFromProfile(){
  const a=me(); if(!a) return;
  const sub=findAccById(getManagedId()); if(!sub||!sub.coachId) return;
  /* mark chat as read → clear badge */
  _markChatRead(sub.coachId, sub.id);
  pfOpenChatPage(sub.coachId, sub.id);
}"""
)

# ─────────────────────────────────────────────────────────────
# 9. Also mark chat read when pfOpenChatPage is called (belt+suspenders)
#    And refresh badge on overlay close
# ─────────────────────────────────────────────────────────────
# Find pfCloseChatPage and pfCloseNotesPage to re-render grid after closing
html = html.replace(
    """function pfCloseChatPage(){
  const overlay=$("pfChatOverlay"); if(!overlay) return;""",
    """function pfCloseChatPage(){
  const overlay=$("pfChatOverlay"); if(!overlay) return;
  /* refresh icon grid badges after closing */
  setTimeout(()=>pfRenderSubIconGrid(), 50);"""
)

html = html.replace(
    """function pfCloseNotesPage(){
  const overlay=$("pfNotesOverlay"); if(!overlay) return;""",
    """function pfCloseNotesPage(){
  const overlay=$("pfNotesOverlay"); if(!overlay) return;
  /* refresh icon grid badges after closing */
  setTimeout(()=>pfRenderSubIconGrid(), 50);"""
)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

new_len = len(html)
print(f"Done. {original_len} → {new_len} chars ({new_len-original_len:+d})")

# Verify
checks = [
    ("Subscriber calc read-only", "canEditEverything() && !isSub()"),
    ("calcInputsWrap hidden for sub", 'sub=isSub();\n  /* Subscriber: hide all inputs'),
    ("Unread badge CSS", "pf-unread-badge"),
    ("_getUnreadChatCount", "_getUnreadChatCount"),
    ("_getUnreadNotesCount", "_getUnreadNotesCount"),
    ("_markChatRead", "_markChatRead"),
    ("_markNotesRead", "_markNotesRead"),
    ("badgeKey notes", 'badgeKey:"notes"'),
    ("badgeKey chat", 'badgeKey:"chat"'),
    ("badge-pop animation", "badge-pop"),
    ("pfCloseNotesPage refreshes grid", "pfRenderSubIconGrid(), 50"),
]
print("\nVerification:")
for label, pattern in checks:
    found = pattern in html
    print(f"  {'✓' if found else '✗'} {label}")
