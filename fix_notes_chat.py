#!/usr/bin/env python3
"""
Fix Notes & Chat:
1. Notes & Chat drawer tabs work like Calc/Weight/Macros — direct render inside drawer body
2. Notes: Add "Add Week" button to manually add more weeks beyond auto-calculated
3. Chat: Full rework — proper flex layout, auto-scroll, no polling bugs
4. Subscriber profile page: same style cards for Notes & Chat
"""

import re

with open("index.html","r",encoding="utf-8") as f:
    html = f.read()

original_len = len(html)

# ─────────────────────────────────────────────────────────────────
# 1. Replace cpDrawerNotes() with improved version that:
#    - Shows all weeks dynamically
#    - Has "Add Week" button
#    - Uses a dedicated extra-weeks counter stored per sub
# ─────────────────────────────────────────────────────────────────
OLD_DRAWER_NOTES = '''function cpDrawerNotes(){
  const body=$(\"cpDrawerBody\"); if(!body) return;
  const sub=findAccById(_cpOpenSubId); if(!sub) return;
  const coach=me(); if(!coach) return;
  const coachId=coach.role===\"coach\"||coach.role===\"admin\" ? coach.id : sub.coachId;

  /* calculate how many weeks since subscription start */
  const startMs=Number(sub.subStartAt||Date.now());
  const totalWeeks=Math.max(1, Math.ceil((Date.now()-startMs)/(7*24*3600*1000))+1);
  const displayWeeks=Math.min(totalWeeks+1, 52); /* show up to 52 weeks */

  body.innerHTML=`
    <div class="cp-notes-page">
      <div class="cp-notes-header">
        <div class="cp-notes-title">📋 Weekly Notes</div>
        <div style="font-size:11px;color:#475569;font-weight:700">${displayWeeks} weeks</div>
      </div>
      <div id="cpNotesCards"></div>
    </div>`;

  const container=$(\"cpNotesCards\");
  for(let w=displayWeeks; w>=1; w--){
    const note=_loadNote(coachId, sub.id, w)||{coachNote:\"\",subNote:\"\",updatedAt:0};
    const hasNote=!!(note.coachNote||note.subNote);
    const weekStart=new Date(startMs+(w-1)*7*24*3600*1000).toLocaleDateString();
    const updLabel=note.updatedAt?new Date(note.updatedAt).toLocaleString():\"No notes yet\";

    const card=document.createElement(\"div\");
    card.className=\"cp-week-card\"+(hasNote?\" has-note\":\"\");
    card.id=`noteCard_${w}`;

    card.innerHTML=`
      <div class="cp-week-card-header" onclick="cpToggleNoteCard(${w})">
        <div class="cp-week-badge"><span class="cp-week-badge-n">${w}</span>W</div>
        <div class="cp-week-meta">
          <div class="cp-week-label">Week ${w}</div>
          <div class="cp-week-preview">${hasNote?(note.coachNote||note.subNote).slice(0,50):\"Tap to add notes...\"}</div>
        </div>
        <span class="cp-week-chevron">›</span>
      </div>
      <div class="cp-week-body">
        <div class="cp-note-date-row">
          <span>Week of ${weekStart}</span>
          <span id="noteUpd_${w}">${updLabel}</span>
        </div>
        <div style="font-size:10px;font-weight:800;color:#38bdf8;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px">Coach Notes</div>
        <textarea class="cp-note-textarea" id="coachNote_${w}" placeholder="Add coach notes for this week..."
          ${coach.role===\"subscriber\"?\"readonly style='opacity:.6'\":\"\"}
        >${note.coachNote||\"\"}</textarea>
        <div style="font-size:10px;font-weight:800;color:#4ade80;text-transform:uppercase;letter-spacing:.08em;margin:10px 0 4px">Subscriber Notes</div>
        <textarea class="cp-note-textarea" id="subNote_${w}" placeholder="Subscriber\'s feedback / notes..."
          ${(coach.role!==\"subscriber\")?\"\":\"\"}
        >${note.subNote||\"\"}</textarea>
        <button class="cp-note-save-btn" onclick="cpSaveNote(${w},'${coachId}','${sub.id}')">💾 Save Notes</button>
        <div class="cp-note-saved-msg" id="noteSaved_${w}"></div>
      </div>`;
    container.appendChild(card);

    /* auto-open latest week with content or week 1 if all empty */
    if(w===displayWeeks && displayWeeks===1) card.classList.add(\"open\");
    if(hasNote && w===displayWeeks) card.classList.add(\"open\");
  }
}'''

NEW_DRAWER_NOTES = '''function _cpNotesExtraKey(subId){ return `ws_notes_extra_${subId}`; }
function _cpGetExtraWeeks(subId){ return parseInt(localStorage.getItem(_cpNotesExtraKey(subId))||\"0\",10)||0; }
function _cpSetExtraWeeks(subId,n){ localStorage.setItem(_cpNotesExtraKey(subId),String(n)); }

function cpDrawerNotes(){
  const body=$(\"cpDrawerBody\"); if(!body) return;
  const sub=findAccById(_cpOpenSubId); if(!sub) return;
  const coach=me(); if(!coach) return;
  const coachId=(coach.role===\"coach\"||coach.role===\"admin\") ? coach.id : sub.coachId;
  _cpBuildNotesUI(body, sub, coachId);
}

function _cpBuildNotesUI(body, sub, coachId){
  const startMs=Number(sub.subStartAt||Date.now());
  const autoWeeks=Math.max(1, Math.ceil((Date.now()-startMs)/(7*24*3600*1000))+1);
  const extra=_cpGetExtraWeeks(sub.id);
  const displayWeeks=Math.min(autoWeeks+extra, 104); /* max 2 years */

  body.innerHTML=`
    <div class="cp-notes-page" id="cpNotesPage">
      <div class="cp-notes-header">
        <div class="cp-notes-title">📋 Weekly Notes</div>
        <button class="cp-note-add-week-btn" onclick="cpAddNoteWeek('${sub.id}','${coachId}')">+ Add Week</button>
      </div>
      <div id="cpNotesCards"></div>
    </div>`;

  const container=$(\"cpNotesCards\");
  const isCoachUser=(me()?.role===\"coach\"||me()?.role===\"admin\");

  for(let w=displayWeeks; w>=1; w--){
    const note=_loadNote(coachId, sub.id, w)||{coachNote:\"\",subNote:\"\",updatedAt:0};
    const hasNote=!!(note.coachNote||note.subNote);
    const weekStart=new Date(startMs+(w-1)*7*24*3600*1000).toLocaleDateString();
    const updLabel=note.updatedAt?new Date(note.updatedAt).toLocaleString():\"No notes yet\";

    const card=document.createElement(\"div\");
    card.className=\"cp-week-card\"+(hasNote?\" has-note\":\"\");
    card.id=`noteCard_${w}`;
    card.innerHTML=`
      <div class="cp-week-card-header" onclick="cpToggleNoteCard(${w})">
        <div class="cp-week-badge"><span class="cp-week-badge-n">${w}</span>W</div>
        <div class="cp-week-meta">
          <div class="cp-week-label">Week ${w}</div>
          <div class="cp-week-preview">${hasNote?(note.coachNote||note.subNote).slice(0,50):\"Tap to add notes...\"}</div>
        </div>
        <span class="cp-week-chevron">›</span>
      </div>
      <div class="cp-week-body">
        <div class="cp-note-date-row">
          <span>Week of ${weekStart}</span>
          <span id="noteUpd_${w}">${updLabel}</span>
        </div>
        <div style="font-size:10px;font-weight:800;color:#38bdf8;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px">Coach Notes</div>
        <textarea class="cp-note-textarea" id="coachNote_${w}" placeholder="Add coach notes for this week..."
          ${!isCoachUser?\"readonly style='opacity:.6'\":\"\"}
        >${note.coachNote||\"\"}</textarea>
        <div style="font-size:10px;font-weight:800;color:#4ade80;text-transform:uppercase;letter-spacing:.08em;margin:10px 0 4px">Subscriber Notes</div>
        <textarea class="cp-note-textarea" id="subNote_${w}" placeholder="Subscriber feedback / notes...">${note.subNote||\"\"}</textarea>
        <button class="cp-note-save-btn" onclick="cpSaveNote(${w},'${coachId}','${sub.id}')">💾 Save Notes</button>
        <div class="cp-note-saved-msg" id="noteSaved_${w}"></div>
      </div>`;
    container.appendChild(card);

    /* auto-open the latest week that has content, or last week if all empty */
    if(w===displayWeeks) card.classList.add(\"open\");
  }
}

function cpAddNoteWeek(subId, coachId){
  const extra=_cpGetExtraWeeks(subId);
  _cpSetExtraWeeks(subId, extra+1);
  /* re-render */
  const sub=findAccById(_cpOpenSubId); if(!sub) return;
  const body=$(\"cpDrawerBody\"); if(!body) return;
  _cpBuildNotesUI(body, sub, coachId);
}'''

if OLD_DRAWER_NOTES in html:
    html = html.replace(OLD_DRAWER_NOTES, NEW_DRAWER_NOTES)
    print("✅ cpDrawerNotes replaced with improved version")
else:
    print("❌ cpDrawerNotes pattern not found — checking partial...")
    idx = html.find("function cpDrawerNotes()")
    print(f"   cpDrawerNotes at line: {html[:idx].count(chr(10))+1 if idx>=0 else 'NOT FOUND'}")

# ─────────────────────────────────────────────────────────────────
# 2. Replace cpDrawerChat() with a proper flex-layout chat
#    - Full height, messages scrollable, input pinned to bottom
#    - Reliable send + scroll-to-bottom
# ─────────────────────────────────────────────────────────────────
OLD_DRAWER_CHAT = '''function cpDrawerChat(){
  const body=$(\"cpDrawerBody\"); if(!body) return;
  const sub=findAccById(_cpOpenSubId); if(!sub) return;
  const user=me(); if(!user) return;
  const coachId=user.role===\"coach\"||user.role===\"admin\" ? user.id : sub.coachId;
  _chatSubId=sub.id; _chatCoachId=coachId;

  body.innerHTML=`
    <div class="cp-chat-page" id="cpChatPage" style="height:calc(100vh - 130px)">
      <div class="cp-chat-messages" id="cpChatMsgs"></div>
      <div class="cp-chat-input-row">
        <input class="cp-chat-inp" id="cpChatInp" placeholder="Message ${sub.name}…"
               onkeydown="if(event.key===\'Enter\'&&!event.shiftKey){event.preventDefault();cpChatSend();}">
        <button class="cp-chat-send-btn" onclick="cpChatSend()">
          <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
            <path d="M22 2L11 13" stroke="white" stroke-width="2.2" stroke-linecap="round"/>
            <path d="M22 2L15 22L11 13L2 9L22 2z" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>`;

  _renderChatMsgs();
  _startChatPoll();
  setTimeout(()=>{ const inp=$(\"cpChatInp\"); if(inp) inp.focus(); }, 200);
}'''

NEW_DRAWER_CHAT = '''function cpDrawerChat(){
  const body=$(\"cpDrawerBody\"); if(!body) return;
  const sub=findAccById(_cpOpenSubId); if(!sub) return;
  const user=me(); if(!user) return;
  const coachId=(user.role===\"coach\"||user.role===\"admin\") ? user.id : sub.coachId;
  _chatSubId=sub.id; _chatCoachId=coachId;
  _lastMsgCount=-1; /* force full render */

  body.style.padding=\"0\";
  body.style.display=\"flex\";
  body.style.flexDirection=\"column\";
  body.style.height=\"calc(100vh - 128px)\";
  body.innerHTML=`
    <div class="cp-chat-page" id="cpChatPage">
      <div class="cp-chat-messages" id="cpChatMsgs"></div>
      <div class="cp-chat-input-row">
        <input class="cp-chat-inp" id="cpChatInp" placeholder="Message ${sub.name}…"
               onkeydown="if(event.key===\'Enter\'&&!event.shiftKey){event.preventDefault();cpChatSend();}">
        <button class="cp-chat-send-btn" onclick="cpChatSend()">
          <svg viewBox="0 0 24 24" fill="none" width="18" height="18">
            <path d="M22 2L11 13" stroke="white" stroke-width="2.2" stroke-linecap="round"/>
            <path d="M22 2L15 22L11 13L2 9L22 2z" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>`;

  _renderChatMsgs();
  _startChatPoll();
  setTimeout(()=>{ const inp=$(\"cpChatInp\"); if(inp){ inp.focus(); } }, 150);
}'''

if OLD_DRAWER_CHAT in html:
    html = html.replace(OLD_DRAWER_CHAT, NEW_DRAWER_CHAT)
    print("✅ cpDrawerChat replaced with improved version")
else:
    print("❌ cpDrawerChat pattern not found")

# ─────────────────────────────────────────────────────────────────
# 3. Fix _renderChatMsgs to always force-scroll and render properly
# ─────────────────────────────────────────────────────────────────
OLD_RENDER_CHAT = '''function _renderChatMsgs(){
  const wrap=$(\"cpChatMsgs\"); if(!wrap) return;
  const msgs=_loadMsgs(_chatCoachId,_chatSubId);
  if(msgs.length===_lastMsgCount) return; /* no change */
  _lastMsgCount=msgs.length;

  const user=me();
  const myId=user?user.id:\"\";
  wrap.innerHTML=\"\";

  if(!msgs.length){
    wrap.innerHTML=`<div class="cp-chat-empty">
      <div class="cp-chat-empty-icon">💬</div>
      <div class="cp-chat-empty-text">No messages yet.<br>Start the conversation!</div>
    </div>`;
    return;
  }

  let lastDate=\"\";
  msgs.forEach(m=>{
    const d=new Date(m.ts);
    const dateStr=d.toLocaleDateString();
    if(dateStr!==lastDate){
      lastDate=dateStr;
      const sep=document.createElement(\"div\");
      sep.className=\"cp-chat-date-sep\";
      sep.textContent=dateStr;
      wrap.appendChild(sep);
    }
    const mine=m.sender===myId;
    const bubble=document.createElement(\"div\");
    bubble.className=\"cp-chat-bubble \"+(mine?\"mine\":\"theirs\");
    bubble.innerHTML=`
      ${!mine?`<div class="cp-chat-sender">${m.senderName}</div>`:\"\"}
      <div>${_escHtml(m.text)}</div>
      <div class="cp-chat-time">${d.toLocaleTimeString([],{hour:\'2-digit\',minute:\'2-digit\'})}</div>`;
    wrap.appendChild(bubble);
  });
  /* scroll to bottom */
  setTimeout(()=>{ wrap.scrollTop=wrap.scrollHeight; },40);
}'''

NEW_RENDER_CHAT = '''function _renderChatMsgs(){
  const wrap=$(\"cpChatMsgs\"); if(!wrap) return;
  const msgs=_loadMsgs(_chatCoachId,_chatSubId);
  if(msgs.length===_lastMsgCount) return; /* no change */
  _lastMsgCount=msgs.length;

  const user=me();
  const myId=user?user.id:\"\";
  wrap.innerHTML=\"\";

  if(!msgs.length){
    const empty=document.createElement(\"div\");
    empty.className=\"cp-chat-empty\";
    empty.innerHTML=`<div class="cp-chat-empty-icon">💬</div><div class="cp-chat-empty-text">No messages yet.<br>Start the conversation!</div>`;
    wrap.appendChild(empty);
    return;
  }

  let lastDate=\"\";
  msgs.forEach(m=>{
    const d=new Date(m.ts);
    const dateStr=d.toLocaleDateString();
    if(dateStr!==lastDate){
      lastDate=dateStr;
      const sep=document.createElement(\"div\");
      sep.className=\"cp-chat-date-sep\";
      sep.textContent=dateStr;
      wrap.appendChild(sep);
    }
    const mine=m.sender===myId;
    const bubble=document.createElement(\"div\");
    bubble.className=\"cp-chat-bubble \"+(mine?\"mine\":\"theirs\");
    bubble.innerHTML=`${!mine?`<div class="cp-chat-sender">${_escHtml(m.senderName)}</div>`:\"\"}
      <div>${_escHtml(m.text)}</div>
      <div class="cp-chat-time">${d.toLocaleTimeString([],{hour:\'2-digit\',minute:\'2-digit\'})}</div>`;
    wrap.appendChild(bubble);
  });
  /* always scroll to newest message */
  wrap.scrollTop=wrap.scrollHeight;
}'''

if OLD_RENDER_CHAT in html:
    html = html.replace(OLD_RENDER_CHAT, NEW_RENDER_CHAT)
    print("✅ _renderChatMsgs fixed")
else:
    print("❌ _renderChatMsgs pattern not found")

# ─────────────────────────────────────────────────────────────────
# 4. Fix cpChatSend to also scroll after send and reset body styles
# ─────────────────────────────────────────────────────────────────
OLD_CP_CHAT_SEND = '''function cpChatSend(){
  const inp=$(\"cpChatInp\"); if(!inp) return;
  const text=inp.value.trim(); if(!text) return;
  const user=me(); if(!user) return;
  inp.value=\"\";
  const msgs=_loadMsgs(_chatCoachId,_chatSubId);
  msgs.push({
    id:Math.random().toString(36).slice(2),
    sender:user.id, senderName:user.name,
    text, ts:Date.now()
  });
  _saveMsgs(_chatCoachId,_chatSubId,msgs);
  _lastMsgCount=0; /* force re-render */
  _renderChatMsgs();
}'''

NEW_CP_CHAT_SEND = '''function cpChatSend(){
  const inp=$(\"cpChatInp\"); if(!inp) return;
  const text=inp.value.trim(); if(!text) return;
  const user=me(); if(!user) return;
  inp.value=\"\";
  const msgs=_loadMsgs(_chatCoachId,_chatSubId);
  msgs.push({id:Math.random().toString(36).slice(2),sender:user.id,senderName:user.name,text,ts:Date.now()});
  _saveMsgs(_chatCoachId,_chatSubId,msgs);
  _lastMsgCount=-1; /* force re-render */
  _renderChatMsgs();
  inp.focus();
}'''

if OLD_CP_CHAT_SEND in html:
    html = html.replace(OLD_CP_CHAT_SEND, NEW_CP_CHAT_SEND)
    print("✅ cpChatSend fixed")
else:
    print("❌ cpChatSend pattern not found")

# ─────────────────────────────────────────────────────────────────
# 5. Fix drawer body styles reset when switching tabs away from chat
# ─────────────────────────────────────────────────────────────────
OLD_CP_DRAWER_TAB = '''  if(tab===\"overview\"||tab===\"manage\"||tab===\"notes\"||tab===\"chat\") cpRestoreTransplant();'''

NEW_CP_DRAWER_TAB = '''  if(tab===\"overview\"||tab===\"manage\"||tab===\"notes\"||tab===\"chat\") cpRestoreTransplant();
  /* reset body inline styles set by chat tab */
  const _b=$(\"cpDrawerBody\"); if(_b){ _b.style.padding=\"\"; _b.style.display=\"\"; _b.style.flexDirection=\"\"; _b.style.height=\"\"; }'''

if OLD_CP_DRAWER_TAB in html:
    html = html.replace(OLD_CP_DRAWER_TAB, NEW_CP_DRAWER_TAB)
    print("✅ cpDrawerTab: body style reset added")
else:
    print("❌ cpDrawerTab reset pattern not found")

# ─────────────────────────────────────────────────────────────────
# 6. Fix subscriber profile pfRenderNotesChat — show all weeks with Add Week btn
# ─────────────────────────────────────────────────────────────────
OLD_PF_RENDER_NOTES = '''  /* ── Render Notes (latest 4 weeks collapsed) ── */
  const notesBody=$(\"pfNotesBody\"); if(!notesBody) return;
  const startMs=Number(sub.subStartAt||Date.now());
  const totalWeeks=Math.max(1,Math.ceil((Date.now()-startMs)/(7*24*3600*1000))+1);
  const showWeeks=Math.min(totalWeeks,8);
  notesBody.innerHTML=\"\";
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
        <div style="font-size:10px;font-weight:800;color:#38bdf8;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px">Coach Notes</div>
        <div style="background:rgba(56,189,248,.06);border:1px solid rgba(56,189,248,.15);border-radius:10px;padding:10px 12px;font-size:13px;color:#cbd5e1;line-height:1.6;margin-bottom:10px">${_escHtml(note.coachNote)}</div>`:\"\"}
        <div style="font-size:10px;font-weight:800;color:#4ade80;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px">Your Notes</div>
        <textarea class="cp-note-textarea" id="pfSubNote_${w}" placeholder="Add your feedback for this week...">${note.subNote||\"\"}</textarea>
        <button class="cp-note-save-btn" onclick="pfSaveSubNote(${w},\'${coachId}\',\'${sub.id}\')">💾 Save</button>
        <div class="cp-note-saved-msg" id="pfNoteSaved_${w}"></div>
      </div>`;
    notesBody.appendChild(card);
    if(w===showWeeks) card.classList.add(\"open\");
  }'''

NEW_PF_RENDER_NOTES = '''  /* ── Render Notes ── */
  const notesBody=$(\"pfNotesBody\"); if(!notesBody) return;
  pfBuildSubNotes(notesBody, sub, coachId);'''

if OLD_PF_RENDER_NOTES in html:
    html = html.replace(OLD_PF_RENDER_NOTES, NEW_PF_RENDER_NOTES)
    print("✅ pfRenderNotesChat notes section simplified")
else:
    print("❌ pfRenderNotesChat notes section not found — trying partial search")
    idx = html.find("/* ── Render Notes (latest 4 weeks collapsed) ── */")
    print(f"   Found at idx {idx}, line {html[:idx].count(chr(10))+1 if idx>=0 else 'NOT FOUND'}")

# ─────────────────────────────────────────────────────────────────
# 7. Fix subscriber profile chat — proper auto-scroll and layout
# ─────────────────────────────────────────────────────────────────
OLD_PF_CHAT_HTML = '''  /* ── Render Chat ── */
  const chatBody=$(\"pfChatBody\"); if(!chatBody) return;
  _chatCoachId=coachId; _chatSubId=sub.id;
  chatBody.innerHTML=`
    <div style="border:1px solid rgba(255,255,255,.08);border-radius:16px;overflow:hidden">
      <div class="cp-chat-messages" id="pfChatMsgs" style="max-height:300px;padding:12px;"></div>
      <div class="cp-chat-input-row" style="border-radius:0 0 16px 16px">
        <input class="cp-chat-inp" id="pfChatInp" placeholder="Message your coach…"
               onkeydown="if(event.key===\'Enter\'){event.preventDefault();pfChatSend();}">
        <button class="cp-chat-send-btn" onclick="pfChatSend()">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M22 2L11 13" stroke="white" stroke-width="2.2" stroke-linecap="round"/>
            <path d="M22 2L15 22L11 13L2 9L22 2z" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>`;
  _pfRenderChatMsgs();
  _startPfChatPoll();'''

NEW_PF_CHAT_HTML = '''  /* ── Render Chat ── */
  const chatBody=$(\"pfChatBody\"); if(!chatBody) return;
  _chatCoachId=coachId; _chatSubId=sub.id;
  _pfLastMsgCount=-1;
  chatBody.innerHTML=`
    <div class="pf-chat-wrap">
      <div class="cp-chat-messages" id="pfChatMsgs"></div>
      <div class="cp-chat-input-row">
        <input class="cp-chat-inp" id="pfChatInp" placeholder="Message your coach…"
               onkeydown="if(event.key===\'Enter\'&&!event.shiftKey){event.preventDefault();pfChatSend();}">
        <button class="cp-chat-send-btn" onclick="pfChatSend()">
          <svg viewBox="0 0 24 24" fill="none" width="16" height="16">
            <path d="M22 2L11 13" stroke="white" stroke-width="2.2" stroke-linecap="round"/>
            <path d="M22 2L15 22L11 13L2 9L22 2z" stroke="white" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
          </svg>
        </button>
      </div>
    </div>`;
  _pfRenderChatMsgs();
  _startPfChatPoll();'''

if OLD_PF_CHAT_HTML in html:
    html = html.replace(OLD_PF_CHAT_HTML, NEW_PF_CHAT_HTML)
    print("✅ pfRenderNotesChat chat section improved")
else:
    print("❌ pfRenderNotesChat chat HTML not found")

# ─────────────────────────────────────────────────────────────────
# 8. Fix _pfRenderChatMsgs to force-scroll and always re-render
# ─────────────────────────────────────────────────────────────────
OLD_PF_RENDER_MSGS = '''function _pfRenderChatMsgs(){
  const wrap=$(\"pfChatMsgs\"); if(!wrap) return;
  const msgs=_loadMsgs(_chatCoachId,_chatSubId);
  if(msgs.length===_pfLastMsgCount) return;
  _pfLastMsgCount=msgs.length;
  const user=me(); const myId=user?user.id:\"\";
  wrap.innerHTML=\"\";
  if(!msgs.length){
    wrap.innerHTML=`<div style="text-align:center;padding:20px;opacity:.3;font-size:12px;font-weight:700">No messages yet</div>`;
    return;
  }
  msgs.slice(-30).forEach(m=>{
    const mine=m.sender===myId;
    const b=document.createElement(\"div\");
    b.className=\"cp-chat-bubble \"+(mine?\"mine\":\"theirs\");
    b.style.marginBottom=\"6px\";
    b.innerHTML=`${!mine?`<div class="cp-chat-sender">${m.senderName}</div>`:\"\"}
      <div>${_escHtml(m.text)}</div>
      <div class="cp-chat-time">${new Date(m.ts).toLocaleTimeString([],{hour:\'2-digit\',minute:\'2-digit\'})}</div>`;
    wrap.appendChild(b);
  });
  setTimeout(()=>{wrap.scrollTop=wrap.scrollHeight;},40);
}'''

NEW_PF_RENDER_MSGS = '''function _pfRenderChatMsgs(){
  const wrap=$(\"pfChatMsgs\"); if(!wrap) return;
  const msgs=_loadMsgs(_chatCoachId,_chatSubId);
  if(msgs.length===_pfLastMsgCount) return;
  _pfLastMsgCount=msgs.length;
  const user=me(); const myId=user?user.id:\"\";
  wrap.innerHTML=\"\";
  if(!msgs.length){
    const empty=document.createElement(\"div\");
    empty.className=\"cp-chat-empty\";
    empty.innerHTML=`<div class="cp-chat-empty-icon">💬</div><div class="cp-chat-empty-text">No messages yet.<br>Start the conversation!</div>`;
    wrap.appendChild(empty);
    return;
  }
  let lastDate=\"\";
  msgs.forEach(m=>{
    const d=new Date(m.ts);
    const dateStr=d.toLocaleDateString();
    if(dateStr!==lastDate){
      lastDate=dateStr;
      const sep=document.createElement(\"div\");
      sep.className=\"cp-chat-date-sep\";
      sep.textContent=dateStr;
      wrap.appendChild(sep);
    }
    const mine=m.sender===myId;
    const b=document.createElement(\"div\");
    b.className=\"cp-chat-bubble \"+(mine?\"mine\":\"theirs\");
    b.innerHTML=`${!mine?`<div class="cp-chat-sender">${_escHtml(m.senderName)}</div>`:\"\"}
      <div>${_escHtml(m.text)}</div>
      <div class="cp-chat-time">${d.toLocaleTimeString([],{hour:\'2-digit\',minute:\'2-digit\'})}</div>`;
    wrap.appendChild(b);
  });
  wrap.scrollTop=wrap.scrollHeight;
}'''

if OLD_PF_RENDER_MSGS in html:
    html = html.replace(OLD_PF_RENDER_MSGS, NEW_PF_RENDER_MSGS)
    print("✅ _pfRenderChatMsgs fixed")
else:
    print("❌ _pfRenderChatMsgs not found")

# ─────────────────────────────────────────────────────────────────
# 9. Fix pfChatSend to force re-render and re-focus
# ─────────────────────────────────────────────────────────────────
OLD_PF_CHAT_SEND = '''function pfChatSend(){
  const inp=$(\"pfChatInp\"); if(!inp) return;
  const text=inp.value.trim(); if(!text) return;
  const user=me(); if(!user) return;
  inp.value=\"\";
  const msgs=_loadMsgs(_chatCoachId,_chatSubId);
  msgs.push({id:Math.random().toString(36).slice(2),sender:user.id,senderName:user.name,text,ts:Date.now()});
  _saveMsgs(_chatCoachId,_chatSubId,msgs);
  _pfLastMsgCount=-1;
  _pfRenderChatMsgs();
}'''

NEW_PF_CHAT_SEND = '''function pfChatSend(){
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
}'''

if OLD_PF_CHAT_SEND in html:
    html = html.replace(OLD_PF_CHAT_SEND, NEW_PF_CHAT_SEND)
    print("✅ pfChatSend fixed")
else:
    print("❌ pfChatSend not found")

# ─────────────────────────────────────────────────────────────────
# 10. Add pfBuildSubNotes function (subscriber side notes, after pfSaveSubNote)
# ─────────────────────────────────────────────────────────────────
OLD_AFTER_PF_SAVE = '''function pfToggleNoteCard(w){
  const c=$(`pfNoteCard_${w}`); if(c) c.classList.toggle(\"open\");
}
function pfSaveSubNote(w,coachId,subId){
  const ta=$(`pfSubNote_${w}`); if(!ta) return;
  const existing=_loadNote(coachId,subId,w)||{coachNote:\"\",subNote:\"\",updatedAt:0};
  existing.subNote=ta.value; existing.updatedAt=Date.now();
  _saveNote(coachId,subId,w,existing);
  const msg=$(`pfNoteSaved_${w}`);
  if(msg){msg.textContent=\"✅ Saved!\";setTimeout(()=>{msg.textContent=\"\";},2000);}
  const prev=document.querySelector(`#pfNoteCard_${w} .cp-week-preview`);
  if(prev) prev.textContent=(existing.coachNote||ta.value).slice(0,55)||\"No notes yet\";
}'''

NEW_AFTER_PF_SAVE = '''function pfToggleNoteCard(w){
  const c=$(`pfNoteCard_${w}`); if(c) c.classList.toggle(\"open\");
}
function pfSaveSubNote(w,coachId,subId){
  const ta=$(`pfSubNote_${w}`); if(!ta) return;
  const existing=_loadNote(coachId,subId,w)||{coachNote:\"\",subNote:\"\",updatedAt:0};
  existing.subNote=ta.value; existing.updatedAt=Date.now();
  _saveNote(coachId,subId,w,existing);
  const msg=$(`pfNoteSaved_${w}`);
  if(msg){msg.textContent=\"✅ Saved!\";setTimeout(()=>{msg.textContent=\"\";},2000);}
  const prev=document.querySelector(`#pfNoteCard_${w} .cp-week-preview`);
  if(prev) prev.textContent=(existing.coachNote||ta.value).slice(0,55)||\"No notes yet\";
}

function pfAddNoteWeek(subId,coachId){
  const extra=_cpGetExtraWeeks(subId);
  _cpSetExtraWeeks(subId,extra+1);
  const sub=findAccById(getManagedId()); if(!sub) return;
  const body=$(\"pfNotesBody\"); if(!body) return;
  pfBuildSubNotes(body,sub,coachId);
}

function pfBuildSubNotes(notesBody, sub, coachId){
  const startMs=Number(sub.subStartAt||Date.now());
  const autoWeeks=Math.max(1,Math.ceil((Date.now()-startMs)/(7*24*3600*1000))+1);
  const extra=_cpGetExtraWeeks(sub.id);
  const showWeeks=Math.min(autoWeeks+extra,104);
  notesBody.innerHTML=`<button class="cp-note-add-week-btn" onclick="pfAddNoteWeek(\'${sub.id}\',\'${coachId}\')" style="margin-bottom:12px">+ Add Week</button>`;
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
        <button class="cp-note-save-btn" onclick="pfSaveSubNote(${w},\'${coachId}\',\'${sub.id}\')">💾 Save</button>
        <div class="cp-note-saved-msg" id="pfNoteSaved_${w}"></div>
      </div>`;
    notesBody.appendChild(card);
    if(w===showWeeks) card.classList.add(\"open\");
  }
}'''

if OLD_AFTER_PF_SAVE in html:
    html = html.replace(OLD_AFTER_PF_SAVE, NEW_AFTER_PF_SAVE)
    print("✅ pfBuildSubNotes and pfAddNoteWeek added")
else:
    print("❌ pfSaveSubNote area not found")

# ─────────────────────────────────────────────────────────────────
# 11. Add CSS for .cp-note-add-week-btn and .pf-chat-wrap
# ─────────────────────────────────────────────────────────────────
OLD_CHAT_PAGE_CSS = '''  .cp-chat-page{
    display:flex; flex-direction:column; height:100%;
    padding:0; box-sizing:border-box;
  }'''

NEW_CHAT_PAGE_CSS = '''  .cp-chat-page{
    display:flex; flex-direction:column; height:100%;
    padding:0; box-sizing:border-box;
  }
  .pf-chat-wrap{
    display:flex; flex-direction:column;
    border:1px solid rgba(255,255,255,.08); border-radius:16px; overflow:hidden;
    min-height:320px;
  }
  .pf-chat-wrap .cp-chat-messages{ max-height:280px; padding:12px; }
  .cp-note-add-week-btn{
    display:flex; align-items:center; justify-content:center; gap:6px;
    width:100%; padding:11px; border-radius:12px; cursor:pointer;
    border:1.5px dashed rgba(56,189,248,.3);
    color:#38bdf8; font-size:13px; font-weight:800;
    background:rgba(56,189,248,.05);
    transition:background .18s; margin-bottom:4px;
  }
  .cp-note-add-week-btn:active{ background:rgba(56,189,248,.12); }'''

if OLD_CHAT_PAGE_CSS in html:
    html = html.replace(OLD_CHAT_PAGE_CSS, NEW_CHAT_PAGE_CSS)
    print("✅ CSS for add-week btn and pf-chat-wrap added")
else:
    print("❌ .cp-chat-page CSS not found")

# ─────────────────────────────────────────────────────────────────
# 12. Also fix cp-drawer-body to use flex when chat tab is active
#     by updating the CSS for .cp-drawer-body
# ─────────────────────────────────────────────────────────────────
# Check what the current cp-drawer-body CSS looks like
cp_drawer_body_idx = html.find(".cp-drawer-body{")
print(f"\ncp-drawer-body CSS at idx {cp_drawer_body_idx}, line {html[:cp_drawer_body_idx].count(chr(10))+1 if cp_drawer_body_idx>=0 else 'NOT FOUND'}")

# ─────────────────────────────────────────────────────────────────
# Write result
# ─────────────────────────────────────────────────────────────────
with open("index.html","w",encoding="utf-8") as f:
    f.write(html)

print(f"\n📦 File: {original_len} → {len(html)} chars, {html.count(chr(10))+1} lines")
print("✅ Done!")
