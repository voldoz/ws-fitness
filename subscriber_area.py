#!/usr/bin/env python3
"""
subscriber_area.py
──────────────────
1. Rename "Coach Panel" → "Subscriber Area" (header title, page title, JS comment)
2. Replace "New Subscriber" add-card in grid with "Generate Code" card
3. Add "Generate Code" button & active-codes list in the header area
4. Replace createUserAccount() with createSubscriber() that requires a coach invite code
5. Add "Create Subscriber" tab to login page (replaces Create Account label)
6. Store invite codes in localStorage; link subscriber to coachId on signup
"""
import re, sys

PATH = "index.html"
txt  = open(PATH, encoding="utf-8").read()
orig = txt

# ──────────────────────────────────────────────────────────────────────────────
# 1. Header title: "My Subscribers" → "Subscriber Area"
# ──────────────────────────────────────────────────────────────────────────────
txt = txt.replace(
    '<div class="cp-header-title">My Subscribers</div>',
    '<div class="cp-header-title">Subscriber Area</div>'
)

# ──────────────────────────────────────────────────────────────────────────────
# 2. JS comment block
# ──────────────────────────────────────────────────────────────────────────────
txt = txt.replace(
    "/* ========= Coach Panel =========",
    "/* ========= Subscriber Area ====="
)

# ──────────────────────────────────────────────────────────────────────────────
# 3. Replace "New Subscriber" add-card with "Generate Code" card in cpFilterGrid
# ──────────────────────────────────────────────────────────────────────────────
old_add_card = (
    '  /* add card */\n'
    '  const addCard=document.createElement("div");\n'
    '  addCard.className="cp-add-card";\n'
    '  addCard.innerHTML=`<div class="cp-add-card-icon"><svg viewBox="0 0 24 24" fill="none" width="20" height="20">'
    '<circle cx="12" cy="8" r="3.5" stroke="currentColor" stroke-width="2"/>'
    '<path d="M5 20c0-3.9 3.1-7 7-7s7 3.1 7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>'
    '<path d="M19 3v6M16 6h6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></div>'
    '<div class="cp-add-card-lbl">New Subscriber</div>`;\n'
    '  addCard.onclick=cpOpenCreate;\n'
    '  grid.appendChild(addCard);'
)
new_add_card = (
    '  /* generate-code card */\n'
    '  const addCard=document.createElement("div");\n'
    '  addCard.className="cp-add-card";\n'
    '  addCard.innerHTML=`<div class="cp-add-card-icon">'
    '<svg viewBox="0 0 24 24" fill="none" width="22" height="22">'
    '<rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" stroke-width="2"/>'
    '<path d="M7 7h4v4H7zM13 7h4v4h-4zM7 13h4v4H7zM13 15h2M15 13v2M13 13h2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
    '</svg></div>'
    '<div class="cp-add-card-lbl">Generate Code</div>`;\n'
    '  addCard.onclick=cpOpenGenerateCode;\n'
    '  grid.appendChild(addCard);'
)
if old_add_card in txt:
    txt = txt.replace(old_add_card, new_add_card)
    print("✅ add-card replaced with generate-code card")
else:
    print("⚠️  add-card pattern not found — trying partial match")
    # Fallback: just replace the innerHTML and onclick
    txt = txt.replace(
        'addCard.innerHTML=`<div class="cp-add-card-icon"><svg viewBox="0 0 24 24" fill="none" width="20" height="20"><circle cx="12" cy="8" r="3.5" stroke="currentColor" stroke-width="2"/><path d="M5 20c0-3.9 3.1-7 7-7s7 3.1 7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M19 3v6M16 6h6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></div><div class="cp-add-card-lbl">New Subscriber</div>`;',
        'addCard.innerHTML=`<div class="cp-add-card-icon"><svg viewBox="0 0 24 24" fill="none" width="22" height="22"><rect x="3" y="3" width="18" height="18" rx="3" stroke="currentColor" stroke-width="2"/><path d="M7 7h4v4H7zM13 7h4v4h-4zM7 13h4v4H7zM13 15h2M15 13v2M13 13h2" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg></div><div class="cp-add-card-lbl">Generate Code</div>`;'
    )
    txt = txt.replace('addCard.onclick=cpOpenCreate;', 'addCard.onclick=cpOpenGenerateCode;')
    print("✅ add-card replaced via fallback")

# ──────────────────────────────────────────────────────────────────────────────
# 4. Remove old Create Subscriber Modal + add Generate Code Modal
#    after the cp-create-modal block
# ──────────────────────────────────────────────────────────────────────────────
old_modal = '''<!-- ══ CREATE SUBSCRIBER MODAL ══ -->
<div class="cp-create-modal" id="cpCreateModal" style="display:none" onclick="if(event.target===this)cpCloseCreate()">
  <div class="cp-create-sheet">
    <div class="cp-sheet-title">&#x2795; New Subscriber</div>
    <div class="cp-sheet-field">
      <div class="cp-sheet-label">USERNAME</div>
      <input class="cp-sheet-inp" id="cSubName" placeholder="e.g. john123" autocapitalize="none">
    </div>
    <div class="cp-sheet-field">
      <div class="cp-sheet-label">PIN (6 digits)</div>
      <input class="cp-sheet-inp" id="cSubPin" type="password" inputmode="numeric" maxlength="6" placeholder="&#x2022; &#x2022; &#x2022; &#x2022; &#x2022; &#x2022;">
    </div>
    <div class="cp-sheet-field">
      <div class="cp-sheet-label">SUBSCRIPTION DURATION</div>
      <select class="cp-sheet-select" id="cSubMonths">
        <option value="1">1 month</option><option value="2">2 months</option>
        <option value="3">3 months</option><option value="4">4 months</option>
        <option value="5">5 months</option><option value="6">6 months</option>
      </select>
    </div>
    <div class="cp-create-msg" id="cSubMsg"></div>
    <div class="cp-sheet-actions">
      <button class="cp-sheet-btn ghost" onclick="cpCloseCreate()">Cancel</button>
      <button class="cp-sheet-btn primary" onclick="coachAddSubscriber()">Create</button>
    </div>
  </div>
</div>'''

new_modal = '''<!-- ══ GENERATE CODE MODAL ══ -->
<div class="cp-create-modal" id="cpGenCodeModal" style="display:none" onclick="if(event.target===this)cpCloseGenCode()">
  <div class="cp-create-sheet">
    <div class="cp-sheet-title">🔑 Generate Invite Code</div>
    <div class="cp-sheet-field">
      <div class="cp-sheet-label">SUBSCRIPTION DURATION</div>
      <select class="cp-sheet-select" id="gcMonths">
        <option value="1">1 month</option><option value="2">2 months</option>
        <option value="3">3 months</option><option value="4">4 months</option>
        <option value="5">5 months</option><option value="6">6 months</option>
        <option value="12">12 months</option>
      </select>
    </div>
    <div class="cp-create-msg" id="gcMsg"></div>
    <!-- Generated code display -->
    <div id="gcResult" style="display:none;margin:14px 0 0">
      <div style="background:rgba(56,189,248,.08);border:1.5px dashed rgba(56,189,248,.4);border-radius:14px;padding:18px;text-align:center">
        <div style="font-size:11px;color:#64748b;font-weight:700;letter-spacing:1px;margin-bottom:8px">INVITE CODE</div>
        <div id="gcCodeDisplay" style="font-size:26px;font-weight:900;letter-spacing:6px;color:#38bdf8;font-family:monospace"></div>
        <div style="font-size:11px;color:#475569;margin-top:6px" id="gcExpLabel"></div>
      </div>
      <button class="cp-sheet-btn primary" style="width:100%;margin-top:10px" onclick="cpCopyCode()">
        <svg viewBox="0 0 24 24" fill="none" width="14" height="14"><rect x="9" y="9" width="13" height="13" rx="2" stroke="currentColor" stroke-width="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
        Copy Code
      </button>
    </div>
    <!-- Active codes list -->
    <div style="margin-top:18px">
      <div style="font-size:11px;font-weight:800;color:#64748b;letter-spacing:1px;margin-bottom:8px">ACTIVE CODES</div>
      <div id="gcActiveList" style="max-height:160px;overflow-y:auto"></div>
    </div>
    <div class="cp-sheet-actions" style="margin-top:10px">
      <button class="cp-sheet-btn ghost" onclick="cpCloseGenCode()">Close</button>
      <button class="cp-sheet-btn primary" onclick="cpDoGenCode()">
        <svg viewBox="0 0 24 24" fill="none" width="14" height="14"><path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"/></svg>
        Generate
      </button>
    </div>
  </div>
</div>

<!-- ══ OLD CREATE MODAL (kept hidden for JS compat) ══ -->
<div id="cpCreateModal" style="display:none">
  <select id="cSubMonths"><option value="1">1</option></select>
  <input id="cSubName"><input id="cSubPin"><div id="cSubMsg"></div>
</div>'''

if old_modal in txt:
    txt = txt.replace(old_modal, new_modal)
    print("✅ Modal replaced with Generate Code modal")
else:
    print("⚠️  Modal block not found exactly — check whitespace")

# ──────────────────────────────────────────────────────────────────────────────
# 5. Login page: rename "Create Account" → "Create Subscriber" tab
#    and update the authAccount section to include code field
# ──────────────────────────────────────────────────────────────────────────────
txt = txt.replace(
    '<button id="segCreateAccount" onclick="switchAuth(\'account\')">Create Account</button>',
    '<button id="segCreateAccount" onclick="switchAuth(\'account\')">Create Subscriber</button>'
)

old_auth_account = '''  <div id="authAccount" class="hidden">
    <div class="box">
      <div style="font-weight:900;color:#38bdf8">Create Account</div>
    </div>

    <label>Name</label>
    <input id="accName" placeholder="name" autocapitalize="none"/>

    <label>PIN (6 digits)</label>
    <input id="accPin" type="password" inputmode="numeric" maxlength="6" placeholder="******" />

    <button class="primary" onclick="createUserAccount()">Create Account</button>
    <div class="small danger" id="accMsg"></div>
  </div>'''

new_auth_account = '''  <div id="authAccount" class="hidden">
    <div class="box">
      <div style="font-weight:900;color:#38bdf8">Create Subscriber</div>
    </div>

    <label>Name</label>
    <input id="accName" placeholder="name" autocapitalize="none"/>

    <label>PIN (6 digits)</label>
    <input id="accPin" type="password" inputmode="numeric" maxlength="6" placeholder="******" />

    <label>Coach Invite Code</label>
    <div style="position:relative">
      <input id="accCode" placeholder="6-character code from your coach" autocapitalize="none" autocomplete="off"
             style="letter-spacing:3px;text-transform:uppercase" maxlength="6"
             oninput="this.value=this.value.toUpperCase()"/>
      <div id="accCodeStatus" style="position:absolute;right:12px;top:50%;transform:translateY(-50%);font-size:12px;font-weight:800"></div>
    </div>
    <div style="font-size:11px;color:#64748b;margin-top:-6px;margin-bottom:4px">
      Ask your coach for an invite code to link your account automatically.
    </div>

    <button class="primary" onclick="createSubscriberAccount()">Join & Create Account</button>
    <div class="small danger" id="accMsg"></div>
  </div>'''

if old_auth_account in txt:
    txt = txt.replace(old_auth_account, new_auth_account)
    print("✅ authAccount section updated with code field")
else:
    print("⚠️  authAccount section not found exactly")

# ──────────────────────────────────────────────────────────────────────────────
# 6. Replace createUserAccount() JS with createSubscriberAccount()
#    and add Generate Code JS functions
# ──────────────────────────────────────────────────────────────────────────────
old_create_user_js = '''function createUserAccount(){
  $("accMsg").textContent="";
  const name=($("accName").value||"").trim().toLowerCase();
  const pin=($("accPin").value||"").trim();

  if(!NAME_RE.test(name) || name.includes(" ")){ $("accMsg").textContent="Invalid name (3-20 letters/numbers/_)."; return; }
  if(name==="admin"){ $("accMsg").textContent="Name reserved."; return; }
  if(findAccByName(name)){ $("accMsg").textContent="Name already used."; return; }
  if(!PIN_RE.test(pin)){ $("accMsg").textContent="PIN must be 6 digits."; return; }

  const acc=loadAccounts();
  acc.push({id:uid(), role:"user", name, pinHash: hashPin(pin)});
  saveAccounts(acc);

  $("accName").value=""; $("accPin").value="";
  $("accMsg").innerHTML=`<span class="ok">✅ Account created. Login now.</span>`;
  refreshAdminUsersList();
  switchAuth("login");
}'''

new_create_user_js = '''/* ─── Invite Codes helpers ─── */
function _codesKey(coachId){ return "ws_invite_codes:"+coachId; }
function loadCodes(coachId){ try{ return JSON.parse(localStorage.getItem(_codesKey(coachId))||"[]"); }catch(e){ return []; } }
function saveCodes(coachId,arr){ localStorage.setItem(_codesKey(coachId),JSON.stringify(arr)); }
function _genRandCode(){ return Math.random().toString(36).substring(2,8).toUpperCase(); }
function cpOpenGenerateCode(){
  $("gcMsg").textContent=""; $("gcResult").style.display="none";
  cpRenderActiveCodesList();
  $("cpGenCodeModal").style.display="flex";
}
function cpCloseGenCode(){ $("cpGenCodeModal").style.display="none"; }
function cpDoGenCode(){
  const a=me(); if(!a) return;
  const months=parseInt($("gcMonths").value||"1",10);
  /* generate unique code */
  let code; const existing=loadCodes(a.id).map(c=>c.code);
  do{ code=_genRandCode(); }while(existing.includes(code));
  const expMs=Date.now()+months*30*24*60*60*1000;
  const arr=loadCodes(a.id);
  arr.push({code, months, createdAt:Date.now(), expiresAt:expMs, used:false});
  saveCodes(a.id,arr);
  /* show result */
  $("gcCodeDisplay").textContent=code;
  $("gcExpLabel").textContent="Valid for "+months+" month"+(months!==1?"s":"")+" · expires "+new Date(expMs).toLocaleDateString();
  $("gcResult").style.display="block";
  _lastGeneratedCode=code;
  cpRenderActiveCodesList();
  $("gcMsg").innerHTML="<span style='color:#4ade80'>✅ Code generated!</span>";
}
let _lastGeneratedCode="";
function cpCopyCode(){
  const c=$("gcCodeDisplay")?.textContent||"";
  if(!c) return;
  navigator.clipboard?.writeText(c).then(()=>{
    $("gcMsg").innerHTML="<span style='color:#4ade80'>✅ Copied!</span>";
  }).catch(()=>{
    $("gcMsg").innerHTML="<span style='color:#f87171'>Copy: "+c+"</span>";
  });
}
function cpRenderActiveCodesList(){
  const a=me(); if(!a) return;
  const list=$("gcActiveList"); if(!list) return;
  const arr=loadCodes(a.id).filter(c=>!c.used && Date.now()<c.expiresAt);
  if(!arr.length){ list.innerHTML='<div style="font-size:12px;color:#475569;text-align:center;padding:10px">No active codes</div>'; return; }
  list.innerHTML=arr.map(c=>`
    <div style="display:flex;align-items:center;justify-content:space-between;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.08);border-radius:10px;padding:8px 12px;margin-bottom:6px">
      <div>
        <span style="font-family:monospace;font-size:16px;font-weight:900;letter-spacing:4px;color:#38bdf8">${c.code}</span>
        <div style="font-size:10px;color:#64748b;margin-top:2px">${c.months} month${c.months!==1?"s":""}  ·  expires ${new Date(c.expiresAt).toLocaleDateString()}</div>
      </div>
      <button onclick="cpRevokeCode('${c.code}')" style="background:rgba(248,113,113,.12);border:1px solid rgba(248,113,113,.25);border-radius:8px;padding:4px 10px;color:#f87171;font-size:11px;font-weight:700;cursor:pointer">Revoke</button>
    </div>`).join("");
}
function cpRevokeCode(code){
  const a=me(); if(!a) return;
  let arr=loadCodes(a.id).filter(c=>c.code!==code);
  saveCodes(a.id,arr);
  cpRenderActiveCodesList();
}

/* validate a code from subscriber perspective */
function validateInviteCode(code){
  const codeUC=(code||"").toUpperCase().trim();
  if(!codeUC || codeUC.length!==6) return null;
  const acc=loadAccounts();
  const coaches=acc.filter(x=>x.role==="coach");
  for(const coach of coaches){
    const arr=loadCodes(coach.id);
    const idx=arr.findIndex(c=>c.code===codeUC && !c.used && Date.now()<c.expiresAt);
    if(idx>=0) return {coach, codeObj:arr[idx], idx, allCodes:arr, coachId:coach.id};
  }
  return null;
}

function createUserAccount(){
  /* legacy stub — redirect to createSubscriberAccount */
  createSubscriberAccount();
}
function createSubscriberAccount(){
  $("accMsg").textContent="";
  const name=($("accName").value||"").trim().toLowerCase();
  const pin=($("accPin").value||"").trim();
  const code=($("accCode")?.value||"").trim().toUpperCase();

  if(!NAME_RE.test(name) || name.includes(" ")){ $("accMsg").textContent="Invalid name (3-20 letters/numbers/_)."; return; }
  if(name==="admin"){ $("accMsg").textContent="Name reserved."; return; }
  if(findAccByName(name)){ $("accMsg").textContent="Name already used."; return; }
  if(!PIN_RE.test(pin)){ $("accMsg").textContent="PIN must be 6 digits."; return; }
  if(!code){ $("accMsg").textContent="Enter the invite code from your coach."; return; }
  if(code.length!==6){ $("accMsg").textContent="Code must be 6 characters."; return; }

  const validated=validateInviteCode(code);
  if(!validated){ $("accMsg").textContent="Invalid or expired code."; return; }

  /* mark code as used */
  const {coachId, codeObj, idx, allCodes}=validated;
  allCodes[idx].used=true;
  allCodes[idx].usedBy=name;
  allCodes[idx].usedAt=Date.now();
  saveCodes(coachId, allCodes);

  /* create subscriber account linked to coach */
  const start=Date.now();
  const expMs=start+codeObj.months*30*24*60*60*1000;
  const acc=loadAccounts();
  acc.push({id:uid(), role:"subscriber", name, coachId, pinHash: hashPin(pin),
            subStartAt:start, subExpiresAt:expMs});
  saveAccounts(acc);

  $("accName").value=""; $("accPin").value=""; if($("accCode")) $("accCode").value="";
  $("accMsg").innerHTML=`<span class="ok">✅ Account created & linked to coach <b>${validated.coach.name}</b>. Login now.</span>`;
  switchAuth("login");
}'''

if old_create_user_js in txt:
    txt = txt.replace(old_create_user_js, new_create_user_js)
    print("✅ createUserAccount replaced with createSubscriberAccount + generate code logic")
else:
    print("⚠️  createUserAccount JS not found exactly — trying to append")
    # Insert before createCoach
    insert_before = "function createCoach(){"
    if insert_before in txt:
        txt = txt.replace(insert_before, new_create_user_js + "\n" + insert_before)
        print("✅ Appended new functions before createCoach")

# ──────────────────────────────────────────────────────────────────────────────
# 7. Add CSS for generate-code modal (append to existing .cp-create-msg styles)
# ──────────────────────────────────────────────────────────────────────────────
css_inject = '''
  /* Generate-code modal extra */
  #gcActiveList::-webkit-scrollbar{ width:4px; }
  #gcActiveList::-webkit-scrollbar-track{ background:transparent; }
  #gcActiveList::-webkit-scrollbar-thumb{ background:rgba(56,189,248,.3); border-radius:4px; }
  #accCode{ text-transform:uppercase; letter-spacing:3px; font-weight:700; }
'''
marker = '.cp-create-msg.err{ color:#f87171; }'
if marker in txt:
    txt = txt.replace(marker, marker + "\n" + css_inject)
    print("✅ CSS injected")

# ──────────────────────────────────────────────────────────────────────────────
# 8. Update cpOpenCreate reference in renderCoachPanel (if any)
# ──────────────────────────────────────────────────────────────────────────────
txt = txt.replace('onclick="cpOpenCreate()"', 'onclick="cpOpenGenerateCode()"')
txt = txt.replace("onclick='cpOpenCreate()'", "onclick='cpOpenGenerateCode()'")

# also stub old functions
old_open_create = 'function cpOpenCreate(){\n  const m=$("cpCreateModal"); if(m){ m.style.display="flex"; }\n  $("cSubName").value=""; $("cSubPin").value=""; $("cSubMsg").textContent="";\n}'
new_open_create = 'function cpOpenCreate(){ cpOpenGenerateCode(); }\n'
if old_open_create in txt:
    txt = txt.replace(old_open_create, new_open_create)
    print("✅ cpOpenCreate stubbed to cpOpenGenerateCode")

old_close_create = 'function cpCloseCreate(){\n  const m=$("cpCreateModal"); if(m) m.style.display="none";\n}'
new_close_create = 'function cpCloseCreate(){ cpCloseGenCode(); }\n'
if old_close_create in txt:
    txt = txt.replace(old_close_create, new_close_create)
    print("✅ cpCloseCreate stubbed")

# ──────────────────────────────────────────────────────────────────────────────
# Write output
# ──────────────────────────────────────────────────────────────────────────────
open(PATH, "w", encoding="utf-8").write(txt)
print(f"\n✅ Done — {len(orig)} → {len(txt)} chars, {txt.count(chr(10))} lines")
