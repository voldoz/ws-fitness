#!/usr/bin/env python3
"""
fix_three.py
────────────
1. Rename nav tab "Coach" → "Subscribers" (bottom nav button tCoachPanel)
2. Add "Create Account" (independent user) tab in login page — separate from "Create Subscriber"
3. Fix weight tracker photos for subscribers: canEditEverything() must return true for subscriber managing their OWN profile
"""

PATH = "index.html"
txt  = open(PATH, encoding="utf-8").read()
orig = txt

# ══════════════════════════════════════════════════════════════════
# 1. Rename nav tab label "Coach" → "Subscribers"
# ══════════════════════════════════════════════════════════════════
old_nav = '<button class="tab hidden" id="tCoachPanel" onclick="go(\'coachpanel\')">Coach</button>'
new_nav = '<button class="tab hidden" id="tCoachPanel" onclick="go(\'coachpanel\')">Subscribers</button>'
if old_nav in txt:
    txt = txt.replace(old_nav, new_nav)
    print("✅ Nav tab renamed to Subscribers")
else:
    print("⚠️  Nav tab not found exactly")

# ══════════════════════════════════════════════════════════════════
# 2. Add "Create Account" tab (independent user) alongside existing tabs
#    The login page currently has: Login | Create Subscriber | Create Coach
#    We add: Login | Create Account | Create Subscriber | Create Coach
# ══════════════════════════════════════════════════════════════════

# 2a. Add new segment button
old_seg_row = '''  <div class="seg">
    <button id="segLogin" class="active" onclick="switchAuth(\'login\')">Login</button>
    <button id="segCreateAccount" onclick="switchAuth(\'account\')">Create Subscriber</button>
    <button id="segCreateCoach" onclick="switchAuth(\'coach\')">Create Coach</button>
  </div>'''

new_seg_row = '''  <div class="seg">
    <button id="segLogin" class="active" onclick="switchAuth(\'login\')">Login</button>
    <button id="segCreateIndependent" onclick="switchAuth(\'independent\')">Create Account</button>
    <button id="segCreateAccount" onclick="switchAuth(\'account\')">Create Subscriber</button>
    <button id="segCreateCoach" onclick="switchAuth(\'coach\')">Create Coach</button>
  </div>'''

if old_seg_row in txt:
    txt = txt.replace(old_seg_row, new_seg_row)
    print("✅ Added Create Account segment button")
else:
    print("⚠️  Segment row not found")

# 2b. Add independent account HTML form (insert before authAccount div)
old_auth_account_start = '  <div id="authAccount" class="hidden">'
new_independent_block = '''  <div id="authIndependent" class="hidden">
    <div class="box">
      <div style="font-weight:900;color:#38bdf8">Create Account</div>
    </div>
    <div style="font-size:12px;color:#64748b;margin-bottom:10px;background:rgba(56,189,248,.06);border:1px solid rgba(56,189,248,.15);border-radius:10px;padding:10px 12px">
      Independent account — full control over your own data. No coach required.
    </div>
    <label>Name</label>
    <input id="indName" placeholder="name" autocapitalize="none"/>

    <label>PIN (6 digits)</label>
    <input id="indPin" type="password" inputmode="numeric" maxlength="6" placeholder="******" />

    <button class="primary" onclick="createIndependentAccount()">Create Account</button>
    <div class="small danger" id="indMsg"></div>
  </div>

  <div id="authAccount" class="hidden">'''

if old_auth_account_start in txt:
    txt = txt.replace(old_auth_account_start, new_independent_block, 1)
    print("✅ Added independent account form")
else:
    print("⚠️  authAccount start not found")

# 2c. Update switchAuth() to handle 'independent' mode
old_switch_auth = '''function switchAuth(mode){
  $("segLogin").classList.toggle("active", mode==="login");
  $("segCreateAccount").classList.toggle("active", mode==="account");
  $("segCreateCoach").classList.toggle("active", mode==="coach");

  $("authLogin").classList.toggle("hidden", mode!=="login");
  $("authAccount").classList.toggle("hidden", mode!=="account");
  $("authCoach").classList.toggle("hidden", mode!=="coach");

  $("loginMsg").textContent="";
  $("accMsg").textContent="";
  $("coachMsg").textContent="";'''

new_switch_auth = '''function switchAuth(mode){
  $("segLogin").classList.toggle("active", mode==="login");
  if($("segCreateIndependent")) $("segCreateIndependent").classList.toggle("active", mode==="independent");
  $("segCreateAccount").classList.toggle("active", mode==="account");
  $("segCreateCoach").classList.toggle("active", mode==="coach");

  $("authLogin").classList.toggle("hidden", mode!=="login");
  if($("authIndependent")) $("authIndependent").classList.toggle("hidden", mode!=="independent");
  $("authAccount").classList.toggle("hidden", mode!=="account");
  $("authCoach").classList.toggle("hidden", mode!=="coach");

  $("loginMsg").textContent="";
  $("accMsg").textContent="";
  $("coachMsg").textContent="";
  if($("indMsg")) $("indMsg").textContent="";'''

if old_switch_auth in txt:
    txt = txt.replace(old_switch_auth, new_switch_auth)
    print("✅ switchAuth updated for independent mode")
else:
    print("⚠️  switchAuth not found exactly")

# 2d. Add createIndependentAccount() function — insert before createSubscriberAccount
insert_before_sub = "function createUserAccount(){"
new_independent_fn = '''function createIndependentAccount(){
  if($("indMsg")) $("indMsg").textContent="";
  const name=($("indName")?.value||"").trim().toLowerCase();
  const pin=($("indPin")?.value||"").trim();

  if(!NAME_RE.test(name)||name.includes(" ")){ if($("indMsg")) $("indMsg").textContent="Invalid name (3-20 letters/numbers/_)."; return; }
  if(name==="admin"){ if($("indMsg")) $("indMsg").textContent="Name reserved."; return; }
  if(findAccByName(name)){ if($("indMsg")) $("indMsg").textContent="Name already used."; return; }
  if(!PIN_RE.test(pin)){ if($("indMsg")) $("indMsg").textContent="PIN must be 6 digits."; return; }

  const acc=loadAccounts();
  acc.push({id:uid(), role:"user", name, pinHash:hashPin(pin)});
  saveAccounts(acc);

  if($("indName")) $("indName").value="";
  if($("indPin"))  $("indPin").value="";
  if($("indMsg"))  $("indMsg").innerHTML=`<span class="ok">✅ Account created. Login now.</span>`;
  setTimeout(()=>switchAuth("login"), 1400);
}

'''

if insert_before_sub in txt:
    txt = txt.replace(insert_before_sub, new_independent_fn + insert_before_sub, 1)
    print("✅ createIndependentAccount() function added")
else:
    print("⚠️  insert point for createIndependentAccount not found")

# ══════════════════════════════════════════════════════════════════
# 3. Fix canEditEverything() so subscribers can edit their OWN data
#    (including uploading progress photos)
# ══════════════════════════════════════════════════════════════════
old_can_edit = '''function canEditEverything(){
  if(isAdmin()) return true;

  const a=me();
  const managed=findAccById(getManagedId());
  if(!a || !managed) return false;

  if(a.role==="user") return managed.id===a.id;

  if(a.role==="coach"){
    if(managed.id===a.id) return true;
    return managed.role==="subscriber" && managed.coachId===a.id;
  }

  return false;
}'''

new_can_edit = '''function canEditEverything(){
  if(isAdmin()) return true;

  const a=me();
  const managed=findAccById(getManagedId());
  if(!a || !managed) return false;

  /* independent user manages themselves */
  if(a.role==="user") return managed.id===a.id;

  /* subscriber manages their own profile */
  if(a.role==="subscriber") return managed.id===a.id;

  if(a.role==="coach"){
    if(managed.id===a.id) return true;
    return managed.role==="subscriber" && managed.coachId===a.id;
  }

  return false;
}'''

if old_can_edit in txt:
    txt = txt.replace(old_can_edit, new_can_edit)
    print("✅ canEditEverything fixed — subscribers can now edit own data & upload photos")
else:
    print("⚠️  canEditEverything not found exactly")

# ══════════════════════════════════════════════════════════════════
# Write
# ══════════════════════════════════════════════════════════════════
open(PATH, "w", encoding="utf-8").write(txt)
print(f"\n✅ Done — {len(orig)} → {len(txt)} chars, {txt.count(chr(10))+1} lines")
