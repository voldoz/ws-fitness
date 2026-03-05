#!/usr/bin/env python3
"""
add_notes_chat.py  —  adds two new tabs to the subscriber drawer:
  1. Notes  — weekly coach↔subscriber notes (each week is a separate card)
  2. Chat   — real-time-style direct messaging between coach and subscriber
               (stored in localStorage, polled every 2 s while chat is open)
"""
PATH = "index.html"
txt  = open(PATH, encoding="utf-8").read()
orig = txt

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 1. HTML — add two tab buttons to the drawer tab bar
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OLD_TABS_END = '''    <button class="cp-drawer-tab"        id="cpTabManage"    onclick="cpDrawerTab('manage')"   ><svg viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/><path d="M12 2v3M12 19v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M2 12h3M19 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Manage</button>'''

NEW_TABS_END = OLD_TABS_END + '''
    <button class="cp-drawer-tab"        id="cpTabNotes"    onclick="cpDrawerTab('notes')"   ><svg viewBox="0 0 24 24" fill="none"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><polyline points="14 2 14 8 20 8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="16" y1="13" x2="8" y2="13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><line x1="16" y1="17" x2="8" y2="17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><polyline points="10 9 9 9 8 9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>Notes</button>
    <button class="cp-drawer-tab"        id="cpTabChat"     onclick="cpDrawerTab('chat')"    ><svg viewBox="0 0 24 24" fill="none"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>Chat</button>'''

if OLD_TABS_END in txt:
    txt = txt.replace(OLD_TABS_END, NEW_TABS_END)
    print("✅ Tab buttons added")
else:
    print("⚠️  Tab buttons anchor not found")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 2. JS — add notes+chat to _cpTabIdMap
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OLD_MAP = '  calc:"cpTabCalc", week:"cpTabWeek", macros:"cpTabMacros", manage:"cpTabManage"'
NEW_MAP = '  calc:"cpTabCalc", week:"cpTabWeek", macros:"cpTabMacros", manage:"cpTabManage",\n  notes:"cpTabNotes", chat:"cpTabChat"'
if OLD_MAP in txt:
    txt = txt.replace(OLD_MAP, NEW_MAP)
    print("✅ Tab map updated")
else:
    print("⚠️  Tab map not found")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 3. JS — add notes/chat cases to cpDrawerTab()
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OLD_DRAWER_TAB_RESTORE = '  if(tab==="overview"||tab==="manage") cpRestoreTransplant();'
NEW_DRAWER_TAB_RESTORE = '  if(tab==="overview"||tab==="manage"||tab==="notes"||tab==="chat") cpRestoreTransplant();'
txt = txt.replace(OLD_DRAWER_TAB_RESTORE, NEW_DRAWER_TAB_RESTORE)

OLD_MACROS_CASE = '  if(tab==="macros")  { cpGoPage("macros");  return; }\n}'
NEW_MACROS_CASE = '  if(tab==="macros")  { cpGoPage("macros");  return; }\n  if(tab==="notes")   { cpDrawerNotes();    return; }\n  if(tab==="chat")    { cpDrawerChat();     return; }\n}'
if OLD_MACROS_CASE in txt:
    txt = txt.replace(OLD_MACROS_CASE, NEW_MACROS_CASE)
    print("✅ cpDrawerTab cases added")
else:
    print("⚠️  cpDrawerTab macros case not found")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 4. CSS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CSS = r"""
  /* ═══════════ Notes Tab ═══════════ */
  .cp-notes-page{ padding:16px 4px 80px; display:flex; flex-direction:column; gap:12px; }
  .cp-notes-header{
    display:flex; align-items:center; justify-content:space-between;
    margin-bottom:4px;
  }
  .cp-notes-title{
    font-size:15px; font-weight:900;
    background:linear-gradient(90deg,#38bdf8,#818cf8);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text;
  }
  .cp-week-card{
    background:linear-gradient(145deg,#09162a,#0d1e38);
    border:1.5px solid rgba(255,255,255,.07);
    border-radius:18px; overflow:hidden;
    transition:border-color .2s;
  }
  .cp-week-card.has-note{ border-color:rgba(56,189,248,.25); }
  .cp-week-card-header{
    display:flex; align-items:center; gap:10px;
    padding:12px 16px; cursor:pointer;
    user-select:none; -webkit-tap-highlight-color:transparent;
  }
  .cp-week-card-header:active{ background:rgba(255,255,255,.03); }
  .cp-week-badge{
    width:36px; height:36px; border-radius:12px; flex-shrink:0;
    background:rgba(56,189,248,.1); border:1px solid rgba(56,189,248,.2);
    display:flex; flex-direction:column; align-items:center; justify-content:center;
    font-size:9px; font-weight:800; color:#38bdf8; line-height:1.1;
  }
  .cp-week-badge-n{ font-size:16px; font-weight:900; }
  .cp-week-meta{ flex:1; min-width:0; }
  .cp-week-label{ font-size:13px; font-weight:800; color:#e2e8f0; }
  .cp-week-preview{
    font-size:11px; color:#475569; font-weight:600;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
    max-width:180px; margin-top:2px;
  }
  .cp-week-chevron{
    color:#334155; font-size:16px;
    transition:transform .22s; flex-shrink:0;
  }
  .cp-week-card.open .cp-week-chevron{ transform:rotate(90deg); }
  .cp-week-body{
    display:none; padding:0 16px 14px;
  }
  .cp-week-card.open .cp-week-body{ display:block; }
  .cp-note-date-row{
    display:flex; justify-content:space-between; align-items:center;
    font-size:10px; color:#334155; font-weight:700; margin-bottom:8px;
  }
  .cp-note-textarea{
    width:100%; min-height:110px; resize:vertical;
    background:rgba(6,12,24,.6);
    border:1.5px solid rgba(255,255,255,.08);
    border-radius:12px; padding:10px 12px;
    font-size:13px; font-weight:600; color:#cbd5e1;
    font-family:inherit; line-height:1.6; outline:none;
    transition:border-color .18s; box-sizing:border-box;
  }
  .cp-note-textarea:focus{ border-color:rgba(56,189,248,.4); }
  .cp-note-save-btn{
    margin-top:8px; width:100%; padding:10px;
    border-radius:12px; border:none;
    background:linear-gradient(135deg,#38bdf8,#818cf8);
    color:#071224; font-size:13px; font-weight:900;
    cursor:pointer; transition:opacity .15s;
  }
  .cp-note-save-btn:active{ opacity:.8; }
  .cp-note-saved-msg{
    text-align:center; font-size:11px; font-weight:700;
    color:#4ade80; margin-top:6px; min-height:16px;
  }
  .cp-note-add-btn{
    display:flex; align-items:center; justify-content:center; gap:8px;
    padding:12px; border-radius:14px; cursor:pointer;
    border:1.5px dashed rgba(56,189,248,.25);
    color:#38bdf8; font-size:13px; font-weight:800;
    background:rgba(56,189,248,.04);
    transition:background .18s;
  }
  .cp-note-add-btn:active{ background:rgba(56,189,248,.1); }

  /* ═══════════ Chat Tab ═══════════ */
  .cp-chat-page{
    display:flex; flex-direction:column; height:100%;
    padding:0; box-sizing:border-box;
  }
  .cp-chat-messages{
    flex:1; overflow-y:auto; padding:14px 12px 8px;
    display:flex; flex-direction:column; gap:8px;
    scroll-behavior:smooth;
  }
  .cp-chat-messages::-webkit-scrollbar{ width:3px; }
  .cp-chat-messages::-webkit-scrollbar-thumb{ background:rgba(56,189,248,.2); border-radius:3px; }
  .cp-chat-bubble{
    max-width:80%; padding:9px 13px;
    border-radius:18px; font-size:13px;
    font-weight:600; line-height:1.55;
    word-break:break-word; position:relative;
    animation:chat-pop .18s cubic-bezier(.34,1.56,.64,1) both;
  }
  @keyframes chat-pop{
    from{ opacity:0; transform:scale(.88) translateY(6px); }
    to{   opacity:1; transform:scale(1) translateY(0); }
  }
  .cp-chat-bubble.mine{
    background:linear-gradient(135deg,#1e4a6e,#1a3a5c);
    border:1px solid rgba(56,189,248,.2);
    border-bottom-right-radius:5px;
    align-self:flex-end; color:#e2e8f0;
  }
  .cp-chat-bubble.theirs{
    background:linear-gradient(135deg,#0f1f35,#142236);
    border:1px solid rgba(255,255,255,.08);
    border-bottom-left-radius:5px;
    align-self:flex-start; color:#cbd5e1;
  }
  .cp-chat-sender{
    font-size:9px; font-weight:800; text-transform:uppercase;
    letter-spacing:.08em; opacity:.5; margin-bottom:3px;
  }
  .cp-chat-time{
    font-size:9px; opacity:.35; margin-top:3px;
    text-align:right; font-weight:600;
  }
  .cp-chat-empty{
    flex:1; display:flex; flex-direction:column; align-items:center;
    justify-content:center; gap:8px; opacity:.3; padding:24px;
  }
  .cp-chat-empty-icon{ font-size:36px; }
  .cp-chat-empty-text{ font-size:13px; font-weight:700; text-align:center; }
  .cp-chat-input-row{
    display:flex; gap:8px; padding:10px 12px 14px;
    border-top:1px solid rgba(255,255,255,.06);
    background:rgba(6,12,24,.9); flex-shrink:0;
  }
  .cp-chat-inp{
    flex:1; background:rgba(255,255,255,.06);
    border:1.5px solid rgba(255,255,255,.1);
    border-radius:22px; padding:10px 16px;
    font-size:13px; font-weight:600; color:#e2e8f0;
    outline:none; font-family:inherit;
    transition:border-color .18s;
  }
  .cp-chat-inp:focus{ border-color:rgba(56,189,248,.45); }
  .cp-chat-inp::placeholder{ color:#334155; }
  .cp-chat-send-btn{
    width:42px; height:42px; flex-shrink:0;
    border-radius:50%; border:none;
    background:linear-gradient(135deg,#38bdf8,#818cf8);
    display:flex; align-items:center; justify-content:center;
    cursor:pointer; transition:transform .12s, opacity .15s;
  }
  .cp-chat-send-btn:active{ transform:scale(.92); opacity:.85; }
  .cp-chat-date-sep{
    text-align:center; font-size:10px; color:#334155; font-weight:700;
    position:relative; margin:4px 0;
  }
  .cp-chat-date-sep::before,.cp-chat-date-sep::after{
    content:''; position:absolute; top:50%;
    width:28%; height:1px; background:rgba(255,255,255,.06);
  }
  .cp-chat-date-sep::before{ left:0; }
  .cp-chat-date-sep::after{ right:0; }
"""

CSS_ANCHOR = "  /* ===== Macros Page ====="
if CSS_ANCHOR in txt:
    txt = txt.replace(CSS_ANCHOR, CSS + "\n  " + CSS_ANCHOR.strip())
    print("✅ CSS injected")
else:
    print("⚠️  CSS anchor not found")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 5. JS — Notes + Chat functions (append before closing </script>)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
JS = r"""
/* ════════════════════════════════════════════════════
   NOTES TAB
   Storage key: ws_notes_{coachId}_{subId}_{weekNum}
   Each value: { coachNote, subNote, updatedAt }
   ════════════════════════════════════════════════════ */
function _notesKey(coachId, subId, week){ return `ws_notes_${coachId}_${subId}_w${week}`; }
function _loadNote(coachId, subId, week){
  try{ return JSON.parse(localStorage.getItem(_notesKey(coachId,subId,week))||"null"); }catch{ return null; }
}
function _saveNote(coachId, subId, week, obj){
  localStorage.setItem(_notesKey(coachId,subId,week), JSON.stringify(obj));
}

function cpDrawerNotes(){
  const body=$("cpDrawerBody"); if(!body) return;
  const sub=findAccById(_cpOpenSubId); if(!sub) return;
  const coach=me(); if(!coach) return;
  const coachId=coach.role==="coach"||coach.role==="admin" ? coach.id : sub.coachId;

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

  const container=$("cpNotesCards");
  for(let w=displayWeeks; w>=1; w--){
    const note=_loadNote(coachId, sub.id, w)||{coachNote:"",subNote:"",updatedAt:0};
    const hasNote=!!(note.coachNote||note.subNote);
    const weekStart=new Date(startMs+(w-1)*7*24*3600*1000).toLocaleDateString();
    const updLabel=note.updatedAt?new Date(note.updatedAt).toLocaleString():"No notes yet";

    const card=document.createElement("div");
    card.className="cp-week-card"+(hasNote?" has-note":"");
    card.id=`noteCard_${w}`;

    card.innerHTML=`
      <div class="cp-week-card-header" onclick="cpToggleNoteCard(${w})">
        <div class="cp-week-badge"><span class="cp-week-badge-n">${w}</span>W</div>
        <div class="cp-week-meta">
          <div class="cp-week-label">Week ${w}</div>
          <div class="cp-week-preview">${hasNote?(note.coachNote||note.subNote).slice(0,50):"Tap to add notes..."}</div>
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
          ${coach.role==="subscriber"?"readonly style='opacity:.6'":""}
        >${note.coachNote||""}</textarea>
        <div style="font-size:10px;font-weight:800;color:#4ade80;text-transform:uppercase;letter-spacing:.08em;margin:10px 0 4px">Subscriber Notes</div>
        <textarea class="cp-note-textarea" id="subNote_${w}" placeholder="Subscriber's feedback / notes..."
          ${(coach.role!=="subscriber")?"":""}
        >${note.subNote||""}</textarea>
        <button class="cp-note-save-btn" onclick="cpSaveNote(${w},'${coachId}','${sub.id}')">💾 Save Notes</button>
        <div class="cp-note-saved-msg" id="noteSaved_${w}"></div>
      </div>`;
    container.appendChild(card);

    /* auto-open latest week with content or week 1 if all empty */
    if(w===displayWeeks && displayWeeks===1) card.classList.add("open");
    if(hasNote && w===displayWeeks) card.classList.add("open");
  }
}

function cpToggleNoteCard(w){
  const card=$(`noteCard_${w}`); if(!card) return;
  card.classList.toggle("open");
}

function cpSaveNote(w, coachId, subId){
  const cn=$(`coachNote_${w}`)?.value||"";
  const sn=$(`subNote_${w}`)?.value||"";
  _saveNote(coachId, subId, w, {coachNote:cn, subNote:sn, updatedAt:Date.now()});
  /* update preview */
  const preview=document.querySelector(`#noteCard_${w} .cp-week-preview`);
  if(preview) preview.textContent=(cn||sn).slice(0,50)||"Tap to add notes...";
  const card=$(`noteCard_${w}`);
  if(card) card.classList.toggle("has-note", !!(cn||sn));
  const upd=$(`noteUpd_${w}`);
  if(upd) upd.textContent=new Date().toLocaleString();
  const msg=$(`noteSaved_${w}`);
  if(msg){ msg.textContent="✅ Saved!"; setTimeout(()=>{msg.textContent="";},2000); }
}

/* ════════════════════════════════════════════════════
   CHAT TAB
   Storage key: ws_chat_{coachId}_{subId}
   Value: array of {id, sender, senderName, text, ts}
   Polling every 2s while chat is open
   ════════════════════════════════════════════════════ */
let _chatPollTimer=null;
let _chatSubId=null;
let _chatCoachId=null;
let _lastMsgCount=0;

function _chatKey(coachId,subId){ return `ws_chat_${coachId}_${subId}`; }
function _loadMsgs(coachId,subId){ try{ return JSON.parse(localStorage.getItem(_chatKey(coachId,subId))||"[]"); }catch{ return []; } }
function _saveMsgs(coachId,subId,arr){ localStorage.setItem(_chatKey(coachId,subId),JSON.stringify(arr)); }

function cpDrawerChat(){
  const body=$("cpDrawerBody"); if(!body) return;
  const sub=findAccById(_cpOpenSubId); if(!sub) return;
  const user=me(); if(!user) return;
  const coachId=user.role==="coach"||user.role==="admin" ? user.id : sub.coachId;
  _chatSubId=sub.id; _chatCoachId=coachId;

  body.innerHTML=`
    <div class="cp-chat-page" id="cpChatPage" style="height:calc(100vh - 130px)">
      <div class="cp-chat-messages" id="cpChatMsgs"></div>
      <div class="cp-chat-input-row">
        <input class="cp-chat-inp" id="cpChatInp" placeholder="Message ${sub.name}…"
               onkeydown="if(event.key==='Enter'&&!event.shiftKey){event.preventDefault();cpChatSend();}">
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
  setTimeout(()=>{ const inp=$("cpChatInp"); if(inp) inp.focus(); }, 200);
}

function _renderChatMsgs(){
  const wrap=$("cpChatMsgs"); if(!wrap) return;
  const msgs=_loadMsgs(_chatCoachId,_chatSubId);
  if(msgs.length===_lastMsgCount) return; /* no change */
  _lastMsgCount=msgs.length;

  const user=me();
  const myId=user?user.id:"";
  wrap.innerHTML="";

  if(!msgs.length){
    wrap.innerHTML=`<div class="cp-chat-empty">
      <div class="cp-chat-empty-icon">💬</div>
      <div class="cp-chat-empty-text">No messages yet.<br>Start the conversation!</div>
    </div>`;
    return;
  }

  let lastDate="";
  msgs.forEach(m=>{
    const d=new Date(m.ts);
    const dateStr=d.toLocaleDateString();
    if(dateStr!==lastDate){
      lastDate=dateStr;
      const sep=document.createElement("div");
      sep.className="cp-chat-date-sep";
      sep.textContent=dateStr;
      wrap.appendChild(sep);
    }
    const mine=m.sender===myId;
    const bubble=document.createElement("div");
    bubble.className="cp-chat-bubble "+(mine?"mine":"theirs");
    bubble.innerHTML=`
      ${!mine?`<div class="cp-chat-sender">${m.senderName}</div>`:""}
      <div>${_escHtml(m.text)}</div>
      <div class="cp-chat-time">${d.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})}</div>`;
    wrap.appendChild(bubble);
  });
  /* scroll to bottom */
  setTimeout(()=>{ wrap.scrollTop=wrap.scrollHeight; },40);
}

function _escHtml(s){
  return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/\n/g,"<br>");
}

function cpChatSend(){
  const inp=$("cpChatInp"); if(!inp) return;
  const text=inp.value.trim(); if(!text) return;
  const user=me(); if(!user) return;
  inp.value="";
  const msgs=_loadMsgs(_chatCoachId,_chatSubId);
  msgs.push({
    id:Math.random().toString(36).slice(2),
    sender:user.id, senderName:user.name,
    text, ts:Date.now()
  });
  _saveMsgs(_chatCoachId,_chatSubId,msgs);
  _lastMsgCount=0; /* force re-render */
  _renderChatMsgs();
}

function _startChatPoll(){
  _stopChatPoll();
  _chatPollTimer=setInterval(()=>{
    if(!$("cpChatMsgs")) { _stopChatPoll(); return; }
    _renderChatMsgs();
  }, 2000);
}
function _stopChatPoll(){
  if(_chatPollTimer){ clearInterval(_chatPollTimer); _chatPollTimer=null; }
}
"""

# Insert JS just before </script>
SCRIPT_END = "</script>"
if SCRIPT_END in txt:
    txt = txt.replace(SCRIPT_END, JS + "\n" + SCRIPT_END, 1)
    print("✅ JS functions added")
else:
    print("⚠️  </script> not found")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 6. Stop chat poll when drawer closes
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
OLD_CLOSE = 'function cpCloseDrawer(){\n  /* restore any transplanted page BEFORE clearing drawer */\n  cpRestoreTransplant();'
NEW_CLOSE = 'function cpCloseDrawer(){\n  _stopChatPoll();\n  /* restore any transplanted page BEFORE clearing drawer */\n  cpRestoreTransplant();'
if OLD_CLOSE in txt:
    txt = txt.replace(OLD_CLOSE, NEW_CLOSE)
    print("✅ chat poll stop on drawer close")
else:
    print("⚠️  cpCloseDrawer anchor not found")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 7. Also allow subscriber to access notes+chat from their own profile
#    Add a "Notes" and "Chat" section to pCalc or as standalone nav
#    (simplest: add nav buttons on their profile page that open the drawer-style panels)
#    Skip for now — coach controls the drawer, subscriber sees the tabs when coach opens their profile
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

open(PATH, "w", encoding="utf-8").write(txt)
print(f"\n✅ Done — {len(orig)} → {len(txt)} chars, {txt.count(chr(10))+1} lines")
