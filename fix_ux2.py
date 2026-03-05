#!/usr/bin/env python3
"""
Fix Notes & Chat UX:
1. Subscriber: Coach Notes = read-only, no Add Week btn (coach only)
2. Subscriber: Chat is a full-screen card at top that opens a chat page on tap
3. Drawer (coach side): Notes & Chat tabs become icon-tabs (same style as Workouts, Weight, etc.)
"""

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

original_len = len(html)
changes = []

# ══════════════════════════════════════════════════════════════════
# 1. SUBSCRIBER PROFILE: Replace pfRenderNotesChat to:
#    - Chat: big entry card at TOP → tapping opens full-screen chat page
#    - Notes: weekly cards, coach notes READ-ONLY, sub can write only in "Your Notes"
#    - No Add Week button for subscriber (coach controls that)
# ══════════════════════════════════════════════════════════════════

OLD_PF_NOTES_BODY = """  /* ── Render Notes ── */
  const notesBody=$(\"pfNotesBody\"); if(!notesBody) return;
  pfBuildSubNotes(notesBody, sub, coachId);

  /* ── Render Chat ── */
  const chatBody=$(\"pfChatBody\"); if(!chatBody) return;
  _chatCoachId=coachId; _chatSubId=sub.id;
  _pfLastMsgCount=-1;
  chatBody.innerHTML=`
    <div class="pf-chat-wrap">
      <div class="cp-chat-messages" id="pfChatMsgs"></div>
      <div class="cp-chat-input-row">
        <input class="cp-chat-inp" id="pfChatInp" placeholder="Message your coach…"
               onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();pfChatSend();}">
        <button class="cp-chat-send-btn" onclick="pfChatSend()">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M22 2L11 13" stroke="white" stroke-width="2.2" stroke-linecap="round"/>
            <path d="M22 2L15 22L11 13L2 9L22 2z" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>`;
  _pfRenderChatMsgs();
  _startPfChatPoll();
}"""

NEW_PF_NOTES_BODY = """  /* ── Render Chat entry card (at TOP of chat card) ── */
  const chatBody=$(\"pfChatBody\"); if(!chatBody) return;
  _chatCoachId=coachId; _chatSubId=sub.id;
  const msgs=_loadMsgs(coachId,sub.id);
  const lastMsg=msgs.length?msgs[msgs.length-1]:null;
  const unread=msgs.filter(m=>m.sender!==sub.id).length; /* rough unread count */
  chatBody.innerHTML=`
    <div class="pf-chat-entry" onclick="pfOpenChatPage('${coachId}','${sub.id}')">
      <div class="pf-chat-entry-avatar">
        <svg viewBox="0 0 24 24" fill="none" width="26" height="26">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
                stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
      <div class="pf-chat-entry-info">
        <div class="pf-chat-entry-title">Chat with Coach</div>
        <div class="pf-chat-entry-preview">${lastMsg?_escHtml(lastMsg.text.slice(0,45)):'Tap to start chatting…'}</div>
      </div>
      <div class="pf-chat-entry-arrow">
        <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
          <path d="M9 18l6-6-6-6" stroke="#38bdf8" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </div>
    </div>`;

  /* ── Render Notes ── */
  const notesBody=$(\"pfNotesBody\"); if(!notesBody) return;
  pfBuildSubNotes(notesBody, sub, coachId);
}"""

if OLD_PF_NOTES_BODY in html:
    html = html.replace(OLD_PF_NOTES_BODY, NEW_PF_NOTES_BODY)
    changes.append("✅ pfRenderNotesChat: Chat entry card at top + notes below")
else:
    changes.append("❌ pfRenderNotesChat body not found")
    idx = html.find("/* ── Render Notes ── */")
    changes.append(f"   Found '/* ── Render Notes ── */' at line {html[:idx].count(chr(10))+1 if idx>=0 else 'NOT FOUND'}")

# ══════════════════════════════════════════════════════════════════
# 2. pfBuildSubNotes: remove Add Week btn, make Coach Notes read-only
# ══════════════════════════════════════════════════════════════════

OLD_BUILD_SUB_NOTES = """function pfBuildSubNotes(notesBody, sub, coachId){
  const startMs=Number(sub.subStartAt||Date.now());
  const autoWeeks=Math.max(1,Math.ceil((Date.now()-startMs)/(7*24*3600*1000))+1);
  const extra=_cpGetExtraWeeks(sub.id);
  const showWeeks=Math.min(autoWeeks+extra,104);
  notesBody.innerHTML=`<button class="cp-note-add-week-btn" onclick="pfAddNoteWeek('${sub.id}','${coachId}')" style="margin-bottom:12px">+ Add Week</button>`;
  for(let w=showWeeks;w>=1;w--){
    const note=_loadNote(coachId,sub.id,w)||{coachNote:\"\",subNote:\"\",updatedAt:0};
    const hasNote=!!(note.coachNote||note.subNote);
    const card=document.createElement(\"div\");
    card.className=\"cp-week-card\"+(hasNote?\" has-note\":\"\");
    card.id=`pfNoteCard_${w}`;
    card.innerHTML=`
      <div class="cp-week-card-header" onclick="pfToggleNoteCard(${w})">
        <div class="cp-week-badge"><span class="cp-week-badge-n">${w}</span>W</div>
        <div class="cp-week-meta">
          <div class="cp-week-label">Week ${w}</div>
          <div class="cp-week-preview">${hasNote?(note.coachNote||note.subNote).slice(0,55):\"No notes yet\"}</div>
        </div>
        <span class="cp-week-chevron">›</span>
      </div>
      <div class="cp-week-body">
        ${note.coachNote?`<div style="font-size:10px;font-weight:800;color:#38bdf8;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px">Coach Notes</div>
        <div style="background:rgba(56,189,248,.06);border:1px solid rgba(56,189,248,.15);border-radius:10px;padding:10px 12px;font-size:13px;color:#cbd5e1;line-height:1.6;margin-bottom:10px">${_escHtml(note.coachNote)}</div>`:\"\"}
        <div style="font-size:10px;font-weight:800;color:#4ade80;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px">Your Notes</div>
        <textarea class="cp-note-textarea" id="pfSubNote_${w}" placeholder="Add your feedback for this week...">${note.subNote||\"\"}</textarea>
        <button class="cp-note-save-btn" onclick="pfSaveSubNote(${w},'${coachId}','${sub.id}')">💾 Save</button>
        <div class="cp-note-saved-msg" id="pfNoteSaved_${w}"></div>
      </div>`;
    notesBody.appendChild(card);
    if(w===showWeeks) card.classList.add(\"open\");
  }
}"""

NEW_BUILD_SUB_NOTES = """function pfBuildSubNotes(notesBody, sub, coachId){
  /* Weeks = auto-calculated from subscription start (coach controls adding weeks) */
  const startMs=Number(sub.subStartAt||Date.now());
  const autoWeeks=Math.max(1,Math.ceil((Date.now()-startMs)/(7*24*3600*1000))+1);
  const extra=_cpGetExtraWeeks(sub.id);
  const showWeeks=Math.min(autoWeeks+extra,104);
  notesBody.innerHTML=\"\"; /* no Add Week btn for subscriber */
  for(let w=showWeeks;w>=1;w--){
    const note=_loadNote(coachId,sub.id,w)||{coachNote:\"\",subNote:\"\",updatedAt:0};
    const hasNote=!!(note.coachNote||note.subNote);
    const card=document.createElement(\"div\");
    card.className=\"cp-week-card\"+(hasNote?\" has-note\":\"\");
    card.id=`pfNoteCard_${w}`;
    card.innerHTML=`
      <div class="cp-week-card-header" onclick="pfToggleNoteCard(${w})">
        <div class="cp-week-badge"><span class="cp-week-badge-n">${w}</span>W</div>
        <div class="cp-week-meta">
          <div class="cp-week-label">Week ${w}</div>
          <div class="cp-week-preview">${hasNote?(note.coachNote||note.subNote).slice(0,55):\"No notes yet\"}</div>
        </div>
        <span class="cp-week-chevron">›</span>
      </div>
      <div class="cp-week-body">
        ${note.coachNote?`
          <div style="font-size:10px;font-weight:800;color:#38bdf8;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px">📋 Coach Notes</div>
          <div style="background:rgba(56,189,248,.06);border:1px solid rgba(56,189,248,.15);border-radius:10px;padding:10px 12px;font-size:13px;color:#cbd5e1;line-height:1.6;margin-bottom:12px">${_escHtml(note.coachNote)}</div>`
        :''}
        <div style="font-size:10px;font-weight:800;color:#4ade80;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px">✏️ Your Notes</div>
        <textarea class="cp-note-textarea" id="pfSubNote_${w}" placeholder="Write your feedback for this week…">${note.subNote||\"\"}</textarea>
        <button class="cp-note-save-btn" onclick="pfSaveSubNote(${w},'${coachId}','${sub.id}')">💾 Save</button>
        <div class="cp-note-saved-msg" id="pfNoteSaved_${w}"></div>
      </div>`;
    notesBody.appendChild(card);
    if(w===showWeeks) card.classList.add(\"open\");
  }
}"""

if OLD_BUILD_SUB_NOTES in html:
    html = html.replace(OLD_BUILD_SUB_NOTES, NEW_BUILD_SUB_NOTES)
    changes.append("✅ pfBuildSubNotes: removed Add Week btn, coach notes read-only display")
else:
    changes.append("❌ pfBuildSubNotes not found")

# ══════════════════════════════════════════════════════════════════
# 3. Add pfOpenChatPage() — opens a full-screen chat overlay for subscriber
# ══════════════════════════════════════════════════════════════════

OLD_PF_CHAT_SEND_FUNC = """function pfChatSend(){
  const inp=$(\"pfChatInp\"); if(!inp) return;
  const text=inp.value.trim(); if(!text) return;
  const user=me(); if(!user) return;
  inp.value=\"\";
  const msgs=_loadMsgs(_chatCoachId,_chatSubId);
  msgs.push({id:Math.random().toString(36).slice(2),sender:user.id,senderName:user.name,text,ts:Date.now()});
  _saveMsgs(_chatCoachId,_chatSubId,msgs);
  _pfLastMsgCount=-1;
  _pfRenderChatMsgs();
  inp.focus();
}"""

NEW_PF_CHAT_SEND_FUNC = """function pfChatSend(){
  const inp=$(\"pfChatInp\")||$(\"pfChatPageInp\"); if(!inp) return;
  const text=inp.value.trim(); if(!text) return;
  const user=me(); if(!user) return;
  inp.value=\"\";
  const msgs=_loadMsgs(_chatCoachId,_chatSubId);
  msgs.push({id:Math.random().toString(36).slice(2),sender:user.id,senderName:user.name,text,ts:Date.now()});
  _saveMsgs(_chatCoachId,_chatSubId,msgs);
  _pfLastMsgCount=-1;
  _pfRenderChatMsgs();
  inp.focus();
}

/* Full-screen chat page for subscriber */
function pfOpenChatPage(coachId, subId){
  _chatCoachId=coachId; _chatSubId=subId;
  _pfLastMsgCount=-1;
  /* remove any existing overlay */
  const old=$(\"pfChatOverlay\"); if(old) old.remove();

  const overlay=document.createElement(\"div\");
  overlay.id=\"pfChatOverlay\";
  overlay.className=\"pf-chat-overlay\";
  overlay.innerHTML=`
    <div class="pf-chat-overlay-bar">
      <button class="pf-chat-overlay-back" onclick="pfCloseChatPage()">
        <svg viewBox="0 0 24 24" fill="none" width="20" height="20">
          <path d="M19 12H5M12 5l-7 7 7 7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
      <div class="pf-chat-overlay-title">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18" style="flex-shrink:0">
          <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"
                stroke="#38bdf8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        Chat with Coach
      </div>
    </div>
    <div class="cp-chat-messages" id="pfChatMsgs" style="flex:1;overflow-y:auto;padding:16px 12px 8px;"></div>
    <div class="cp-chat-input-row" style="flex-shrink:0;">
      <input class="cp-chat-inp" id="pfChatPageInp" placeholder="Message your coach…"
             onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();pfChatSend();}">
      <button class="cp-chat-send-btn" onclick="pfChatSend()">
        <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
          <path d="M22 2L11 13" stroke="white" stroke-width="2.2" stroke-linecap="round"/>
          <path d="M22 2L15 22L11 13L2 9L22 2z" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </button>
    </div>`;
  document.body.appendChild(overlay);
  /* animate in */
  requestAnimationFrame(()=>overlay.classList.add(\"open\"));
  _pfRenderChatMsgs();
  _startPfChatPoll();
  setTimeout(()=>{ const i=$(\"pfChatPageInp\"); if(i) i.focus(); },200);
}

function pfCloseChatPage(){
  const overlay=$(\"pfChatOverlay\"); if(!overlay) return;
  overlay.classList.remove(\"open\");
  overlay.addEventListener(\"transitionend\",()=>overlay.remove(),{once:true});
  if(_pfChatPoll){ clearInterval(_pfChatPoll); _pfChatPoll=null; }
  /* update entry card preview */
  pfRenderNotesChat();
}"""

if OLD_PF_CHAT_SEND_FUNC in html:
    html = html.replace(OLD_PF_CHAT_SEND_FUNC, NEW_PF_CHAT_SEND_FUNC)
    changes.append("✅ pfOpenChatPage + pfCloseChatPage added")
else:
    changes.append("❌ pfChatSend function not found")

# ══════════════════════════════════════════════════════════════════
# 4. Add CSS for chat entry card + overlay
# ══════════════════════════════════════════════════════════════════

OLD_NOTES_PAGE_CSS = """  .cp-notes-page{ padding:16px 4px 80px; display:flex; flex-direction:column; gap:12px; }"""

NEW_NOTES_PAGE_CSS = """  .cp-notes-page{ padding:16px 4px 80px; display:flex; flex-direction:column; gap:12px; }

  /* ── Subscriber Chat Entry Card ── */
  .pf-chat-entry{
    display:flex; align-items:center; gap:14px;
    background:linear-gradient(135deg,#0d1f3c,#0f2545);
    border:1.5px solid rgba(56,189,248,.2);
    border-radius:18px; padding:16px 18px;
    cursor:pointer; transition:all .2s;
    box-shadow:0 4px 20px rgba(0,0,0,.35);
  }
  .pf-chat-entry:active{ transform:scale(.98); border-color:rgba(56,189,248,.45); }
  .pf-chat-entry-avatar{
    width:46px; height:46px; border-radius:50%; flex-shrink:0;
    background:linear-gradient(135deg,rgba(56,189,248,.15),rgba(129,140,248,.15));
    border:1.5px solid rgba(56,189,248,.25);
    display:flex; align-items:center; justify-content:center;
  }
  .pf-chat-entry-info{ flex:1; min-width:0; }
  .pf-chat-entry-title{ font-size:14px; font-weight:900; color:#e2e8f0; margin-bottom:3px; }
  .pf-chat-entry-preview{
    font-size:12px; color:#475569; font-weight:600;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
  }
  .pf-chat-entry-arrow{ flex-shrink:0; opacity:.5; }

  /* ── Full-screen chat overlay ── */
  .pf-chat-overlay{
    position:fixed; inset:0; z-index:9999;
    background:#060c18;
    display:flex; flex-direction:column;
    transform:translateX(100%); transition:transform .28s cubic-bezier(.22,1,.36,1);
  }
  .pf-chat-overlay.open{ transform:translateX(0); }
  .pf-chat-overlay-bar{
    display:flex; align-items:center; gap:12px;
    padding:14px 16px 12px; flex-shrink:0;
    background:rgba(6,12,25,.98);
    border-bottom:1px solid rgba(255,255,255,.07);
  }
  .pf-chat-overlay-back{
    width:36px; height:36px; border-radius:12px; border:none;
    background:rgba(255,255,255,.06); color:#94a3b8;
    display:flex; align-items:center; justify-content:center;
    cursor:pointer; flex-shrink:0; transition:background .15s;
  }
  .pf-chat-overlay-back:active{ background:rgba(255,255,255,.12); }
  .pf-chat-overlay-title{
    font-size:15px; font-weight:900; color:#e2e8f0;
    display:flex; align-items:center; gap:8px;
  }"""

if OLD_NOTES_PAGE_CSS in html:
    html = html.replace(OLD_NOTES_PAGE_CSS, NEW_NOTES_PAGE_CSS)
    changes.append("✅ CSS for pf-chat-entry + pf-chat-overlay added")
else:
    changes.append("❌ .cp-notes-page CSS not found")

# ══════════════════════════════════════════════════════════════════
# 5. DRAWER NOTES/CHAT TABS: swap text labels with icons matching other tabs
#    Notes tab: already has icon + "Notes" text → keep same style ✓
#    Chat tab: already has icon + "Chat" text → keep same style ✓
#    The tabs ARE already icon-style. The issue is they look different
#    because the tab bar is scrollable and Notes/Chat are at the end.
#    We need to reorder: put Notes & Chat BEFORE Manage, or keep at end.
#    The real request is that coach-side drawer tabs look like icon tabs.
#    Currently they ARE icon tabs. Let's verify and fix if Notes/Chat
#    tabs look different (they use <polyline> which may look wrong).
#    Replace Notes tab SVG with a cleaner notepad icon.
#    Replace Chat tab SVG with clean speech bubble.
# ══════════════════════════════════════════════════════════════════

OLD_NOTES_TAB = """    <button class=\"cp-drawer-tab\"        id=\"cpTabNotes\"    onclick=\"cpDrawerTab('notes')\"   ><svg viewBox=\"0 0 24 24\" fill=\"none\"><path d=\"M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/><polyline points=\"14 2 14 8 20 8\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/><line x1=\"16\" y1=\"13\" x2=\"8\" y2=\"13\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/><line x1=\"16\" y1=\"17\" x2=\"8\" y2=\"17\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/><polyline points=\"10 9 9 9 8 9\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>Notes</button>
    <button class=\"cp-drawer-tab\"        id=\"cpTabChat\"     onclick=\"cpDrawerTab('chat')\"    ><svg viewBox=\"0 0 24 24\" fill=\"none\"><path d=\"M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>Chat</button>"""

NEW_NOTES_TAB = """    <button class=\"cp-drawer-tab\"        id=\"cpTabNotes\"    onclick=\"cpDrawerTab('notes')\"   ><svg viewBox=\"0 0 24 24\" fill=\"none\"><path d=\"M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/><rect x=\"9\" y=\"3\" width=\"6\" height=\"4\" rx=\"1\" stroke=\"currentColor\" stroke-width=\"2\"/><line x1=\"9\" y1=\"12\" x2=\"15\" y2=\"12\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/><line x1=\"9\" y1=\"16\" x2=\"13\" y2=\"16\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>Notes</button>
    <button class=\"cp-drawer-tab\"        id=\"cpTabChat\"     onclick=\"cpDrawerTab('chat')\"    ><svg viewBox=\"0 0 24 24\" fill=\"none\"><path d=\"M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/><line x1=\"9\" y1=\"10\" x2=\"15\" y2=\"10\" stroke=\"currentColor\" stroke-width=\"1.5\" stroke-linecap=\"round\"/><line x1=\"9\" y1=\"14\" x2=\"12\" y2=\"14\" stroke=\"currentColor\" stroke-width=\"1.5\" stroke-linecap=\"round\"/></svg>Chat</button>"""

if OLD_NOTES_TAB in html:
    html = html.replace(OLD_NOTES_TAB, NEW_NOTES_TAB)
    changes.append("✅ Notes & Chat drawer tab icons updated")
else:
    changes.append("❌ Notes/Chat tab HTML not found — checking...")
    idx = html.find("cpTabNotes")
    changes.append(f"   cpTabNotes at line {html[:idx].count(chr(10))+1 if idx>=0 else 'NOT FOUND'}")

# ══════════════════════════════════════════════════════════════════
# 6. Fix pfChatCard HTML: show the entry card (not raw chatBody)
#    Replace the pfChatCard title to say "Coach Chat" and remove padding
# ══════════════════════════════════════════════════════════════════

OLD_PF_CHAT_CARD_HTML = """  <div class=\"pf-card\" id=\"pfChatCard\" style=\"display:none\">
    <div class=\"pf-card-title\">
      <svg width=\"18\" height=\"18\" viewBox=\"0 0 24 24\" fill=\"none\"><path d=\"M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z\" stroke=\"#38bdf8\" stroke-width=\"1.8\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/></svg>
      Chat with Coach
    </div>"""

NEW_PF_CHAT_CARD_HTML = """  <div class=\"pf-card pf-card-chat\" id=\"pfChatCard\" style=\"display:none;padding:0;overflow:hidden;\">
    <div style=\"display:none\"><!-- chat entry rendered in pfChatBody --></div>"""

if OLD_PF_CHAT_CARD_HTML in html:
    html = html.replace(OLD_PF_CHAT_CARD_HTML, NEW_PF_CHAT_CARD_HTML)
    changes.append("✅ pfChatCard HTML simplified (entry card handles everything)")
else:
    changes.append("❌ pfChatCard HTML not found")
    idx = html.find('id="pfChatCard"')
    changes.append(f"   pfChatCard at line {html[:idx].count(chr(10))+1 if idx>=0 else 'NOT FOUND'}")

# ══════════════════════════════════════════════════════════════════
# 7. Fix pfChatBody margin-top (no gap since card has no title now)
# ══════════════════════════════════════════════════════════════════

OLD_CHAT_BODY_HTML = """    <div id=\"pfChatBody\" style=\"margin-top:8px\"></div>"""
NEW_CHAT_BODY_HTML = """    <div id=\"pfChatBody\"></div>"""

if OLD_CHAT_BODY_HTML in html:
    html = html.replace(OLD_CHAT_BODY_HTML, NEW_CHAT_BODY_HTML)
    changes.append("✅ pfChatBody margin removed")
else:
    changes.append("❌ pfChatBody margin not found")

# ══════════════════════════════════════════════════════════════════
# 8. Fix _pfRenderChatMsgs to work with pfChatMsgs in overlay
# ══════════════════════════════════════════════════════════════════
# Already uses $(\"pfChatMsgs\") — the overlay also has id="pfChatMsgs" so it will work ✓

# ══════════════════════════════════════════════════════════════════
# Write result
# ══════════════════════════════════════════════════════════════════
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("\n".join(changes))
print(f"\n📦 {original_len} → {len(html)} chars, {html.count(chr(10))+1} lines")
