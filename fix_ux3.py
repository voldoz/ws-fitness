#!/usr/bin/env python3
"""
Fix:
1. Overview page: add Notes & Chat as icon buttons (same row as Workouts/Weight/Calc...)
2. Chat: coach messages = blue gradient, subscriber messages = green gradient
3. Notes: ONLY coach can write, subscriber reads only (no subscriber note textarea)
"""

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

original_len = len(html)
changes = []

# ══════════════════════════════════════════════════════════════════
# 1. Add Notes & Chat to quick-action buttons in cpDrawerOverview
# ══════════════════════════════════════════════════════════════════

OLD_QUICKBTNS = """  const quickBtns=[\n    {tab:\"work\",  icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><path d=\"M6 4v16M18 4v16M3 9h18M3 15h18\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`, label:\"Workouts\", color:\"#38bdf8\"},\n    {tab:\"weight\",icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><path d=\"M3 6h18M3 12h18M3 18h18\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`, label:\"Weight\", color:\"#34d399\"},\n    {tab:\"calc\",  icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><rect x=\"4\" y=\"2\" width=\"16\" height=\"20\" rx=\"2\" stroke=\"currentColor\" stroke-width=\"2\"/><path d=\"M8 7h8M8 12h4\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`, label:\"Calc\", color:\"#a78bfa\"},\n    {tab:\"week\",  icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><rect x=\"3\" y=\"4\" width=\"18\" height=\"18\" rx=\"2\" stroke=\"currentColor\" stroke-width=\"2\"/><path d=\"M16 2v4M8 2v4M3 10h18\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`, label:\"Weekly\", color:\"#fb923c\"},\n    {tab:\"macros\",icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><circle cx=\"12\" cy=\"12\" r=\"9\" stroke=\"currentColor\" stroke-width=\"2\"/><path d=\"M12 8v8M8 12h8\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`, label:\"Macros\", color:\"#f472b6\"},\n    {tab:\"manage\",icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><circle cx=\"12\" cy=\"12\" r=\"3\" stroke=\"currentColor\" stroke-width=\"2\"/><path d=\"M12 2v3M12 19v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`, label:\"Manage\", color:\"#94a3b8\"},\n  ].map(b=>`<button onclick=\"cpDrawerTab('${b.tab}')\" style=\"background:linear-gradient(145deg,#09162a,#0d1e34);border:1.5px solid rgba(255,255,255,.07);border-radius:16px;padding:14px 8px;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:8px;transition:all .22s;-webkit-tap-highlight-color:transparent;color:${b.color}\" onmouseover=\"this.style.transform='translateY(-2px) scale(1.04)';this.style.borderColor='${b.color}40'\" onmouseout=\"this.style.transform='';this.style.borderColor='rgba(255,255,255,.07)'\">`\n    +`<span style=\"width:40px;height:40px;border-radius:12px;background:${b.color}18;display:flex;align-items:center;justify-content:center;border:1px solid ${b.color}30\">${b.icon}</span>`\n    +`<span style=\"font-size:10px;font-weight:800;color:#94a3b8;letter-spacing:.02em\">${b.label}</span>`\n    +`</button>`).join(\"\");"""

NEW_QUICKBTNS = """  const quickBtns=[\n    {tab:\"work\",  icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><path d=\"M6 4v16M18 4v16M3 9h18M3 15h18\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`, label:\"Workouts\", color:\"#38bdf8\"},\n    {tab:\"weight\",icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><path d=\"M3 6h18M3 12h18M3 18h18\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`, label:\"Weight\", color:\"#34d399\"},\n    {tab:\"calc\",  icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><rect x=\"4\" y=\"2\" width=\"16\" height=\"20\" rx=\"2\" stroke=\"currentColor\" stroke-width=\"2\"/><path d=\"M8 7h8M8 12h4\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`, label:\"Calc\", color:\"#a78bfa\"},\n    {tab:\"week\",  icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><rect x=\"3\" y=\"4\" width=\"18\" height=\"18\" rx=\"2\" stroke=\"currentColor\" stroke-width=\"2\"/><path d=\"M16 2v4M8 2v4M3 10h18\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`, label:\"Weekly\", color:\"#fb923c\"},\n    {tab:\"macros\",icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><circle cx=\"12\" cy=\"12\" r=\"9\" stroke=\"currentColor\" stroke-width=\"2\"/><path d=\"M12 8v8M8 12h8\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`, label:\"Macros\", color:\"#f472b6\"},\n    {tab:\"notes\", icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><path d=\"M9 5H7a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-2\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/><rect x=\"9\" y=\"3\" width=\"6\" height=\"4\" rx=\"1\" stroke=\"currentColor\" stroke-width=\"2\"/><line x1=\"9\" y1=\"12\" x2=\"15\" y2=\"12\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/><line x1=\"9\" y1=\"16\" x2=\"13\" y2=\"16\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`, label:\"Notes\", color:\"#fbbf24\"},\n    {tab:\"chat\",  icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><path d=\"M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\"/><line x1=\"9\" y1=\"10\" x2=\"15\" y2=\"10\" stroke=\"currentColor\" stroke-width=\"1.5\" stroke-linecap=\"round\"/><line x1=\"9\" y1=\"14\" x2=\"12\" y2=\"14\" stroke=\"currentColor\" stroke-width=\"1.5\" stroke-linecap=\"round\"/></svg>`, label:\"Chat\", color:\"#4ade80\"},\n    {tab:\"manage\",icon:`<svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"20\" height=\"20\"><circle cx=\"12\" cy=\"12\" r=\"3\" stroke=\"currentColor\" stroke-width=\"2\"/><path d=\"M12 2v3M12 19v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\"/></svg>`, label:\"Manage\", color:\"#94a3b8\"},\n  ].map(b=>`<button onclick=\"cpDrawerTab('${b.tab}')\" style=\"background:linear-gradient(145deg,#09162a,#0d1e34);border:1.5px solid rgba(255,255,255,.07);border-radius:16px;padding:14px 8px;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:8px;transition:all .22s;-webkit-tap-highlight-color:transparent;color:${b.color}\" onmouseover=\"this.style.transform='translateY(-2px) scale(1.04)';this.style.borderColor='${b.color}40'\" onmouseout=\"this.style.transform='';this.style.borderColor='rgba(255,255,255,.07)'\">`\n    +`<span style=\"width:40px;height:40px;border-radius:12px;background:${b.color}18;display:flex;align-items:center;justify-content:center;border:1px solid ${b.color}30\">${b.icon}</span>`\n    +`<span style=\"font-size:10px;font-weight:800;color:#94a3b8;letter-spacing:.02em\">${b.label}</span>`\n    +`</button>`).join(\"\");"""

if OLD_QUICKBTNS in html:
    html = html.replace(OLD_QUICKBTNS, NEW_QUICKBTNS)
    changes.append("✅ Notes & Chat icon buttons added to Overview quick-actions grid")
else:
    changes.append("❌ quickBtns array not found")

# ══════════════════════════════════════════════════════════════════
# 2. CHAT COLORS: coach = blue gradient, subscriber = green gradient
#    _renderChatMsgs (drawer) — swap colors
# ══════════════════════════════════════════════════════════════════

# Replace CSS: .cp-chat-bubble.mine and .cp-chat-bubble.theirs
OLD_BUBBLE_MINE_CSS = """  .cp-chat-bubble.mine{\n    background:linear-gradient(135deg,#1e4a6e,#1a3a5c);\n    border:1px solid rgba(56,189,248,.2);\n    border-bottom-right-radius:5px;\n    align-self:flex-end; color:#e2e8f0;\n  }\n  .cp-chat-bubble.theirs{\n    background:linear-gradient(135deg,#0f1f35,#142236);\n    border:1px solid rgba(255,255,255,.08);\n    border-bottom-left-radius:5px;\n    align-self:flex-start; color:#cbd5e1;\n  }"""

NEW_BUBBLE_CSS = """  /* coach message = blue, subscriber message = green */
  .cp-chat-bubble.coach-msg{
    background:linear-gradient(135deg,#0e3a5c,#1a4a72);
    border:1px solid rgba(56,189,248,.25);
    border-bottom-right-radius:5px;
    align-self:flex-end; color:#e2e8f0;
  }
  .cp-chat-bubble.sub-msg{
    background:linear-gradient(135deg,#0b3320,#0f4228);
    border:1px solid rgba(74,222,128,.2);
    border-bottom-left-radius:5px;
    align-self:flex-start; color:#cbd5e1;
  }
  /* fallback for mine/theirs (subscriber profile chat) */
  .cp-chat-bubble.mine{
    background:linear-gradient(135deg,#0b3320,#0f4228);
    border:1px solid rgba(74,222,128,.2);
    border-bottom-right-radius:5px;
    align-self:flex-end; color:#e2e8f0;
  }
  .cp-chat-bubble.theirs{
    background:linear-gradient(135deg,#0e3a5c,#1a4a72);
    border:1px solid rgba(56,189,248,.25);
    border-bottom-left-radius:5px;
    align-self:flex-start; color:#cbd5e1;
  }"""

if OLD_BUBBLE_MINE_CSS in html:
    html = html.replace(OLD_BUBBLE_MINE_CSS, NEW_BUBBLE_CSS)
    changes.append("✅ Chat bubble colors: coach=blue, subscriber=green")
else:
    changes.append("❌ Chat bubble CSS not found")

# ══════════════════════════════════════════════════════════════════
# 3. _renderChatMsgs: use role-based classes (coach-msg / sub-msg)
#    instead of mine/theirs — so colors depend on WHO sent it, not
#    who is viewing. The coach's messages are always blue, subscriber always green.
# ══════════════════════════════════════════════════════════════════

OLD_RENDER_CHAT_CLASS = """    const mine=m.sender===myId;\n    const bubble=document.createElement(\"div\");\n    bubble.className=\"cp-chat-bubble \"+(mine?\"mine\":\"theirs\");\n    bubble.innerHTML=`${!mine?`<div class=\"cp-chat-sender\">${_escHtml(m.senderName)}</div>`:\"\"}\n      <div>${_escHtml(m.text)}</div>\n      <div class=\"cp-chat-time\">${d.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})}</div>`;\n    wrap.appendChild(bubble);\n  });\n  /* always scroll to newest message */\n  wrap.scrollTop=wrap.scrollHeight;\n}"""

NEW_RENDER_CHAT_CLASS = """    const mine=m.sender===myId;\n    /* determine role of sender for color */\n    const senderAcc=findAccById(m.sender);\n    const senderRole=senderAcc?senderAcc.role:\"\";\n    const isCoachMsg=(senderRole===\"coach\"||senderRole===\"admin\");\n    const bubbleCls=isCoachMsg?\"coach-msg\":\"sub-msg\";\n    const bubble=document.createElement(\"div\");\n    bubble.className=\"cp-chat-bubble \"+bubbleCls+(mine?\" is-mine\":\"\");\n    bubble.style.alignSelf=mine?\"flex-end\":\"flex-start\";\n    bubble.innerHTML=`${!mine?`<div class=\"cp-chat-sender\">${_escHtml(m.senderName)}</div>`:\"\"}\n      <div>${_escHtml(m.text)}</div>\n      <div class=\"cp-chat-time\">${d.toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})}</div>`;\n    wrap.appendChild(bubble);\n  });\n  /* always scroll to newest message */\n  wrap.scrollTop=wrap.scrollHeight;\n}"""

if OLD_RENDER_CHAT_CLASS in html:
    html = html.replace(OLD_RENDER_CHAT_CLASS, NEW_RENDER_CHAT_CLASS)
    changes.append("✅ _renderChatMsgs: role-based bubble colors")
else:
    changes.append("❌ _renderChatMsgs bubble class not found")

# Same fix for _pfRenderChatMsgs (subscriber profile page chat)
OLD_PF_RENDER_CLASS = """    const mine=m.sender===myId;\n    const b=document.createElement(\"div\");\n    b.className=\"cp-chat-bubble \"+(mine?\"mine\":\"theirs\");\n    b.innerHTML=`${!mine?`<div class=\"cp-chat-sender\">${_escHtml(m.senderName)}</div>`:\"\"}\n      <div>${_escHtml(m.text)}</div>\n      <div class=\"cp-chat-time\">${new Date(m.ts).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})}</div>`;\n    wrap.appendChild(b);\n  });\n  wrap.scrollTop=wrap.scrollHeight;\n}"""

NEW_PF_RENDER_CLASS = """    const mine=m.sender===myId;\n    const senderAcc=findAccById(m.sender);\n    const senderRole=senderAcc?senderAcc.role:\"\";\n    const isCoachMsg=(senderRole===\"coach\"||senderRole===\"admin\");\n    const bubbleCls=isCoachMsg?\"coach-msg\":\"sub-msg\";\n    const b=document.createElement(\"div\");\n    b.className=\"cp-chat-bubble \"+bubbleCls+(mine?\" is-mine\":\"\");\n    b.style.alignSelf=mine?\"flex-end\":\"flex-start\";\n    b.innerHTML=`${!mine?`<div class=\"cp-chat-sender\">${_escHtml(m.senderName)}</div>`:\"\"}\n      <div>${_escHtml(m.text)}</div>\n      <div class=\"cp-chat-time\">${new Date(m.ts).toLocaleTimeString([],{hour:'2-digit',minute:'2-digit'})}</div>`;\n    wrap.appendChild(b);\n  });\n  wrap.scrollTop=wrap.scrollHeight;\n}"""

if OLD_PF_RENDER_CLASS in html:
    html = html.replace(OLD_PF_RENDER_CLASS, NEW_PF_RENDER_CLASS)
    changes.append("✅ _pfRenderChatMsgs: role-based bubble colors")
else:
    changes.append("❌ _pfRenderChatMsgs bubble class not found")

# ══════════════════════════════════════════════════════════════════
# 4. NOTES — Coach Only Write: 
#    cpDrawerNotes: remove subscriber notes textarea for coach view too
#    (coach writes coach notes, subscriber section removed from drawer)
# ══════════════════════════════════════════════════════════════════

OLD_DRAWER_NOTES_BODY = """        <div style="font-size:10px;font-weight:800;color:#38bdf8;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px">Coach Notes</div>
        <textarea class="cp-note-textarea" id="coachNote_${w}" placeholder="Add coach notes for this week..."
          ${!isCoachUser?"readonly style='opacity:.6'":""}
        >${note.coachNote||""}</textarea>
        <div style="font-size:10px;font-weight:800;color:#4ade80;text-transform:uppercase;letter-spacing:.08em;margin:10px 0 4px">Subscriber Notes</div>
        <textarea class="cp-note-textarea" id="subNote_${w}" placeholder="Subscriber feedback / notes...">${note.subNote||""}</textarea>
        <button class="cp-note-save-btn" onclick="cpSaveNote(${w},'${coachId}','${sub.id}')">💾 Save Notes</button>
        <div class="cp-note-saved-msg" id="noteSaved_${w}"></div>"""

NEW_DRAWER_NOTES_BODY = """        <div style="font-size:10px;font-weight:800;color:#38bdf8;text-transform:uppercase;letter-spacing:.08em;margin-bottom:4px">📋 Coach Notes</div>
        <textarea class="cp-note-textarea" id="coachNote_${w}" placeholder="Add notes for this subscriber…">${note.coachNote||""}</textarea>
        <button class="cp-note-save-btn" onclick="cpSaveNote(${w},'${coachId}','${sub.id}')">💾 Save Notes</button>
        <div class="cp-note-saved-msg" id="noteSaved_${w}"></div>"""

if OLD_DRAWER_NOTES_BODY in html:
    html = html.replace(OLD_DRAWER_NOTES_BODY, NEW_DRAWER_NOTES_BODY)
    changes.append("✅ cpDrawerNotes: removed subscriber notes section (coach only)")
else:
    changes.append("❌ cpDrawerNotes body not found — checking...")
    idx = html.find("Subscriber Notes</div>")
    if idx >= 0:
        changes.append(f"   'Subscriber Notes' found at line {html[:idx].count(chr(10))+1}")
    else:
        changes.append("   'Subscriber Notes' NOT found")

# Also fix cpSaveNote to only save coachNote (no subNote)
OLD_CP_SAVE_NOTE = """function cpSaveNote(w, coachId, subId){\n  const cn=$(`coachNote_${w}`)?.value||\"\";\n  const sn=$(`subNote_${w}`)?.value||\"\";\n  _saveNote(coachId, subId, w, {coachNote:cn, subNote:sn, updatedAt:Date.now()});"""

NEW_CP_SAVE_NOTE = """function cpSaveNote(w, coachId, subId){\n  const cn=$(`coachNote_${w}`)?.value||\"\";\n  /* preserve existing subNote, only update coachNote */\n  const existing=_loadNote(coachId,subId,w)||{coachNote:\"\",subNote:\"\",updatedAt:0};\n  _saveNote(coachId, subId, w, {coachNote:cn, subNote:existing.subNote, updatedAt:Date.now()});"""

if OLD_CP_SAVE_NOTE in html:
    html = html.replace(OLD_CP_SAVE_NOTE, NEW_CP_SAVE_NOTE)
    changes.append("✅ cpSaveNote: only saves coachNote (preserves subNote)")
else:
    changes.append("❌ cpSaveNote pattern not found")

# ══════════════════════════════════════════════════════════════════
# 5. SUBSCRIBER pfBuildSubNotes: remove "Your Notes" textarea entirely
#    Subscriber only sees coach notes (read-only)
# ══════════════════════════════════════════════════════════════════

OLD_SUB_NOTES_BODY = """        ${note.coachNote?`
          <div style="font-size:10px;font-weight:800;color:#38bdf8;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px">📋 Coach Notes</div>
          <div style="background:rgba(56,189,248,.06);border:1px solid rgba(56,189,248,.15);border-radius:10px;padding:10px 12px;font-size:13px;color:#cbd5e1;line-height:1.6;margin-bottom:12px">${_escHtml(note.coachNote)}</div>`
        :''}
        <div style="font-size:10px;font-weight:800;color:#4ade80;text-transform:uppercase;letter-spacing:.08em;margin-bottom:6px">✏️ Your Notes</div>
        <textarea class="cp-note-textarea" id="pfSubNote_${w}" placeholder="Write your feedback for this week…">${note.subNote||""}</textarea>
        <button class="cp-note-save-btn" onclick="pfSaveSubNote(${w},'${coachId}','${sub.id}')">💾 Save</button>
        <div class="cp-note-saved-msg" id="pfNoteSaved_${w}"></div>"""

NEW_SUB_NOTES_BODY = """        ${note.coachNote
          ? `<div style="font-size:10px;font-weight:800;color:#38bdf8;text-transform:uppercase;letter-spacing:.08em;margin-bottom:8px">📋 Coach Notes</div>
             <div style="background:rgba(56,189,248,.07);border:1px solid rgba(56,189,248,.18);border-radius:12px;padding:12px 14px;font-size:13px;color:#cbd5e1;line-height:1.7">${_escHtml(note.coachNote)}</div>`
          : `<div style="text-align:center;padding:20px;opacity:.35;font-size:12px;font-weight:700">No notes from coach yet</div>`
        }"""

if OLD_SUB_NOTES_BODY in html:
    html = html.replace(OLD_SUB_NOTES_BODY, NEW_SUB_NOTES_BODY)
    changes.append("✅ pfBuildSubNotes: subscriber sees coach notes read-only, no textarea")
else:
    changes.append("❌ pfBuildSubNotes body not found")
    idx = html.find("Write your feedback for this week")
    if idx >= 0:
        changes.append(f"   Found 'Write your feedback' at line {html[:idx].count(chr(10))+1}")

# ══════════════════════════════════════════════════════════════════
# 6. Update overview grid to 4 cols to fit more buttons nicely
# ══════════════════════════════════════════════════════════════════

OLD_GRID_COLS = """    <!-- Quick actions grid -->\n    <div style=\"display:grid;grid-template-columns:repeat(3,1fr);gap:8px;padding:10px 12px 4px\">${quickBtns}</div>"""

NEW_GRID_COLS = """    <!-- Quick actions grid -->\n    <div style=\"display:grid;grid-template-columns:repeat(4,1fr);gap:8px;padding:10px 12px 4px\">${quickBtns}</div>"""

if OLD_GRID_COLS in html:
    html = html.replace(OLD_GRID_COLS, NEW_GRID_COLS)
    changes.append("✅ Overview grid: 3 cols → 4 cols to fit 8 buttons")
else:
    changes.append("❌ Overview grid cols not found")

# ══════════════════════════════════════════════════════════════════
# Write
# ══════════════════════════════════════════════════════════════════
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("\n".join(changes))
print(f"\n📦 {original_len} → {len(html)} chars, {html.count(chr(10))+1} lines")
