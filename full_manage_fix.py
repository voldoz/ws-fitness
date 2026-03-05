#!/usr/bin/env python3
# full_manage_fix.py

with open('index.html','r',encoding='utf-8') as f:
    html = f.read()

# ══════════════════════════════════════════════
# 1. إخفاء pfManagedCard من صفحة Profile نهائياً
#    نغير renderProfile() لإخفائه دائماً
# ══════════════════════════════════════════════
OLD_MANAGED_BLOCK = '''  /* ── managed ── */
  const allowManaged=isAdmin()||isCoach();
  const mc=$(\"pfManagedCard\");
  if(mc) mc.style.display=allowManaged?'':'none';
  if(allowManaged) fillManagedSelect();
  if(isSub()||isUser()){ if(getManagedId()!==a.id) setManagedId(a.id); }'''

NEW_MANAGED_BLOCK = '''  /* ── managed card: hidden for coach (managed from Coach Panel) ── */
  const mc=$(\"pfManagedCard\");
  if(mc) mc.style.display='none';
  /* admin still uses fillManagedSelect for their own context management */
  if(isAdmin()) fillManagedSelect();
  if(isSub()||isUser()){ if(getManagedId()!==a.id) setManagedId(a.id); }'''

if OLD_MANAGED_BLOCK in html:
    html = html.replace(OLD_MANAGED_BLOCK, NEW_MANAGED_BLOCK, 1)
    print('renderProfile managed block hidden OK')
else:
    print('WARNING: managed block not found')

# ══════════════════════════════════════════════
# 2. توسيع cpDrawerManage بالكامل
# ══════════════════════════════════════════════
OLD_MANAGE_FN = '''function cpDrawerManage(){
  const body=$("cpDrawerBody"); if(!body) return;
  const sub=findAccById(_cpOpenSubId); if(!sub) return;
  body.innerHTML=`
    <div style="padding:12px;display:flex;flex-direction:column;gap:12px">
      <div style="background:linear-gradient(145deg,#0d1829,#111e30);border-radius:18px;padding:16px;border:1px solid rgba(255,255,255,.06)">
        <div style="font-size:11px;font-weight:800;color:#64748b;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px">Reset PIN</div>
        <input class="cp-sheet-inp" id="cpResetPinInp" type="password" inputmode="numeric" maxlength="6" placeholder="New 6-digit PIN">
        <button class="pf-pin-btn" style="margin-top:10px" onclick="cpDoResetPin()">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none"><path d="M12 2l3 9h9l-7 5 3 9-8-6-8 6 3-9-7-5h9z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>
          Reset PIN
        </button>
        <div class="cp-create-msg" id="cpResetPinMsg"></div>
      </div>
      <div style="background:linear-gradient(145deg,#0d1829,#111e30);border-radius:18px;padding:16px;border:1px solid rgba(255,255,255,.06)">
        <div style="font-size:11px;font-weight:800;color:#64748b;text-transform:uppercase;letter-spacing:.06em;margin-bottom:12px">Extend Subscription</div>
        <select class="cp-sheet-select" id="cpExtendSel">
          <option value="1">+1 month</option><option value="2">+2 months</option>
          <option value="3">+3 months</option><option value="6">+6 months</option>
        </select>
        <button class="pf-pin-btn" style="margin-top:10px;background:linear-gradient(135deg,#22c55e,#16a34a)" onclick="cpDoExtend()">
          Extend Subscription
        </button>
        <div class="cp-create-msg" id="cpExtendMsg"></div>
      </div>
      <button style="width:100%;padding:13px;border-radius:14px;border:none;cursor:pointer;background:rgba(239,68,68,.1);color:#f87171;border:1.5px solid rgba(239,68,68,.2);font-size:14px;font-weight:900" onclick="cpDoDelete()">
        Delete Subscriber
      </button>
    </div>
  `;
}'''

NEW_MANAGE_FN = '''function cpDrawerManage(){
  const body=$("cpDrawerBody"); if(!body) return;
  const sub=findAccById(_cpOpenSubId); if(!sub) return;
  const saved=localStorage.getItem("pf_avatar:"+sub.id)||"";
  const ini=cpInitials(sub.name);
  const st=cpSubStatus(sub);
  const expMs=Number(sub.subExpiresAt||0);
  const startMs=Number(sub.subStartAt||0);
  const daysLeft=expMs?Math.max(0,Math.ceil((expMs-nowMs())/DAY_MS)):0;
  const pillCls={active:"green",expiring:"yellow",expired:"red"};
  const statusLabel={active:"Active",expiring:"Expiring soon",expired:"Expired"};

  body.innerHTML=`
    <div style="padding:12px;display:flex;flex-direction:column;gap:12px">

      <!-- ── Profile Photo ── -->
      <div class="cp-manage-card">
        <div class="cp-manage-card-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="8" r="4" stroke="#38bdf8" stroke-width="2"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/></svg>
          Profile Photo
        </div>
        <div style="display:flex;align-items:center;gap:14px;margin-top:4px">
          <div id="cpManageAvatar" style="width:64px;height:64px;border-radius:18px;overflow:hidden;background:linear-gradient(135deg,#0f2744,#1a3a5c);border:2px solid rgba(56,189,248,.3);display:flex;align-items:center;justify-content:center;flex-shrink:0;cursor:pointer" onclick="$('cpManageAvatarInput').click()">
            ${saved
              ? `<img src="${saved}" style="width:100%;height:100%;object-fit:cover" alt="">`
              : `<span style="font-size:20px;font-weight:900;background:linear-gradient(135deg,#38bdf8,#818cf8);-webkit-background-clip:text;-webkit-text-fill-color:transparent">${ini}</span>`}
          </div>
          <div style="flex:1;display:flex;flex-direction:column;gap:8px">
            <button class="cp-manage-btn primary" onclick="$('cpManageAvatarInput').click()">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4M17 8l-5-5-5 5M12 3v12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
              Upload Photo
            </button>
            ${saved ? `<button class="cp-manage-btn ghost" onclick="cpDoDeleteAvatar()">
              <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><polyline points="3 6 5 6 21 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M19 6l-1 14H6L5 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M10 11v6M14 11v6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
              Remove Photo
            </button>` : ""}
          </div>
        </div>
        <input type="file" id="cpManageAvatarInput" accept="image/*" style="display:none" onchange="cpDoUploadAvatar(this)">
        <div class="cp-create-msg" id="cpAvatarMsg"></div>
      </div>

      <!-- ── Display Name ── -->
      <div class="cp-manage-card">
        <div class="cp-manage-card-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/></svg>
          Display Name
        </div>
        <input class="cp-sheet-inp" id="cpNameInp" value="${sub.name}" placeholder="Subscriber name" style="margin-top:8px">
        <button class="cp-manage-btn primary" style="margin-top:8px" onclick="cpDoSaveName()">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z" stroke="currentColor" stroke-width="2"/><polyline points="17 21 17 13 7 13 7 21" stroke="currentColor" stroke-width="2"/></svg>
          Save Name
        </button>
        <div class="cp-create-msg" id="cpNameMsg"></div>
      </div>

      <!-- ── Reset PIN ── -->
      <div class="cp-manage-card">
        <div class="cp-manage-card-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="3" y="11" width="18" height="11" rx="2" stroke="#38bdf8" stroke-width="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/></svg>
          Reset PIN
        </div>
        <input class="cp-sheet-inp" id="cpResetPinInp" type="password" inputmode="numeric" maxlength="6" placeholder="New 6-digit PIN" style="margin-top:8px">
        <button class="cp-manage-btn primary" style="margin-top:8px" onclick="cpDoResetPin()">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><polyline points="23 4 23 10 17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M20.49 15a9 9 0 1 1-2.12-9.36L23 10" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          Reset PIN
        </button>
        <div class="cp-create-msg" id="cpResetPinMsg"></div>
      </div>

      <!-- ── Subscription ── -->
      <div class="cp-manage-card">
        <div class="cp-manage-card-title">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><rect x="3" y="4" width="18" height="18" rx="2" stroke="#38bdf8" stroke-width="2"/><path d="M16 2v4M8 2v4M3 10h18" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/></svg>
          Subscription
        </div>
        <!-- current status -->
        <div style="display:flex;justify-content:space-between;align-items:center;margin-top:10px;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.05)">
          <span style="font-size:12px;color:#64748b">Status</span>
          <span style="font-size:12px;font-weight:800;padding:3px 10px;border-radius:10px" class="cp-sub-info-pill ${pillCls[st]}">${statusLabel[st]}</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.05)">
          <span>Start</span><span style="color:#e2e8f0;font-weight:700">${fmtDate(startMs)}</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;padding:8px 0;border-bottom:1px solid rgba(255,255,255,.05)">
          <span>Expires</span><span style="color:#e2e8f0;font-weight:700">${fmtDate(expMs)}</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;padding:8px 0">
          <span>Days left</span><span style="font-weight:800" class="${pillCls[st]}-text">${daysLeft > 0 ? daysLeft+" days" : "Expired"}</span>
        </div>
        <!-- extend -->
        <div style="margin-top:12px">
          <div style="font-size:11px;font-weight:700;color:#64748b;margin-bottom:6px">EXTEND SUBSCRIPTION</div>
          <div style="display:flex;gap:8px;align-items:center">
            <select class="cp-sheet-select" id="cpExtendSel" style="flex:1">
              <option value="1">+1 month</option><option value="2">+2 months</option>
              <option value="3">+3 months</option><option value="6">+6 months</option>
              <option value="12">+12 months</option>
            </select>
            <button class="cp-manage-btn success" onclick="cpDoExtend()">Extend</button>
          </div>
          <div class="cp-create-msg" id="cpExtendMsg"></div>
        </div>
      </div>

      <!-- ── Danger Zone ── -->
      <div class="cp-manage-card danger">
        <div class="cp-manage-card-title" style="color:#f87171">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none"><path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z" stroke="#f87171" stroke-width="2"/><line x1="12" y1="9" x2="12" y2="13" stroke="#f87171" stroke-width="2" stroke-linecap="round"/><line x1="12" y1="17" x2="12.01" y2="17" stroke="#f87171" stroke-width="2" stroke-linecap="round"/></svg>
          Danger Zone
        </div>
        <button class="cp-manage-btn danger" style="margin-top:10px;width:100%" onclick="cpDoDelete()">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none"><polyline points="3 6 5 6 21 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M19 6l-1 14H6L5 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M10 11v6M14 11v6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>
          Delete Subscriber
        </button>
      </div>

    </div>
  `;
}
/* ── upload avatar for subscriber ── */
function cpDoUploadAvatar(input){
  const file=input.files&&input.files[0]; if(!file) return;
  const reader=new FileReader();
  reader.onload=function(e){
    const sub=findAccById(_cpOpenSubId); if(!sub) return;
    /* compress */
    const img2=new Image();
    img2.onload=function(){
      const canvas=document.createElement("canvas");
      const MAX=320; let w=img2.width,h=img2.height;
      if(w>h){ if(w>MAX){h=Math.round(h*MAX/w);w=MAX;} }
      else { if(h>MAX){w=Math.round(w*MAX/h);h=MAX;} }
      canvas.width=w; canvas.height=h;
      canvas.getContext("2d").drawImage(img2,0,0,w,h);
      const data=canvas.toDataURL("image/jpeg",0.82);
      localStorage.setItem("pf_avatar:"+sub.id, data);
      cpMsg("cpAvatarMsg","Photo updated","ok");
      /* refresh avatar preview */
      const av=$("cpManageAvatar");
      if(av) av.innerHTML=`<img src="${data}" style="width:100%;height:100%;object-fit:cover" alt="">`;
      /* update drawer bar */
      const barAv=$("cpDrBarAvatar");
      if(barAv) barAv.innerHTML=`<img src="${data}" alt="">`;
    };
    img2.src=e.target.result;
  };
  reader.readAsDataURL(file);
}
/* ── delete avatar ── */
function cpDoDeleteAvatar(){
  const sub=findAccById(_cpOpenSubId); if(!sub) return;
  localStorage.removeItem("pf_avatar:"+sub.id);
  cpMsg("cpAvatarMsg","Photo removed","ok");
  setTimeout(()=>cpDrawerManage(),300);
}
/* ── save display name ── */
function cpDoSaveName(){
  const sub=findAccById(_cpOpenSubId); if(!sub) return;
  const name=($("cpNameInp")?.value||"").trim();
  if(!name){ cpMsg("cpNameMsg","Name cannot be empty","err"); return; }
  const acc=loadAccounts(); const i=acc.findIndex(x=>x.id===sub.id);
  if(i===-1) return;
  acc[i].name=name; saveAccounts(acc);
  /* update drawer bar */
  const barName=$("cpDrBarName"); if(barName) barName.textContent=name;
  cpMsg("cpNameMsg","Name saved","ok");
}'''

if OLD_MANAGE_FN in html:
    html = html.replace(OLD_MANAGE_FN, NEW_MANAGE_FN, 1)
    print('cpDrawerManage expanded OK')
else:
    print('ERROR: cpDrawerManage not found — trying partial match')
    if 'function cpDrawerManage()' in html:
        print('  function exists but body differs')

# ══════════════════════════════════════════════
# 3. إضافة CSS لبطاقات الـ Manage
# ══════════════════════════════════════════════
MANAGE_CSS = '''
  /* ── Manage drawer cards ── */
  .cp-manage-card{
    background:linear-gradient(145deg,#08142a,#0d1e38);
    border-radius:20px; padding:16px;
    border:1.5px solid rgba(255,255,255,.07);
    display:flex; flex-direction:column; gap:2px;
  }
  .cp-manage-card.danger{ border-color:rgba(239,68,68,.2); background:linear-gradient(145deg,#180a0a,#1e1015); }
  .cp-manage-card-title{
    font-size:11px; font-weight:800; color:#64748b;
    text-transform:uppercase; letter-spacing:.06em;
    display:flex; align-items:center; gap:7px;
  }
  .cp-manage-btn{
    display:flex; align-items:center; justify-content:center; gap:7px;
    padding:10px 16px; border-radius:13px; border:none; cursor:pointer;
    font-size:13px; font-weight:800; transition:all .18s;
    -webkit-tap-highlight-color:transparent;
  }
  .cp-manage-btn.primary{
    background:linear-gradient(135deg,#38bdf8,#818cf8); color:#fff;
    box-shadow:0 4px 14px rgba(56,189,248,.25);
  }
  .cp-manage-btn.primary:active{ transform:scale(.95); }
  .cp-manage-btn.success{
    background:linear-gradient(135deg,#22c55e,#16a34a); color:#fff;
    padding:10px 18px; white-space:nowrap;
  }
  .cp-manage-btn.ghost{
    background:rgba(255,255,255,.06); color:#94a3b8;
    border:1.5px solid rgba(255,255,255,.09);
  }
  .cp-manage-btn.danger{
    background:rgba(239,68,68,.1); color:#f87171;
    border:1.5px solid rgba(239,68,68,.25);
  }
  .cp-manage-btn.danger:active{ transform:scale(.95); background:rgba(239,68,68,.2); }
  .green-text{ color:#4ade80; }
  .yellow-text{ color:#fbbf24; }
  .red-text{ color:#f87171; }
'''

if '.cp-manage-card' not in html:
    marker = '  /* ── Coach back-bar'
    if marker in html:
        html = html.replace(marker, MANAGE_CSS + '  /* ── Coach back-bar', 1)
        print('Manage card CSS added OK')
    else:
        print('WARNING: CSS marker not found')
else:
    print('Manage card CSS already present')

# ══════════════════════════════════════════════
# Write
# ══════════════════════════════════════════════
with open('index.html','w',encoding='utf-8') as f:
    f.write(html)

with open('index.html','r',encoding='utf-8') as f:
    lines = f.readlines()
print(f'Done. {len(lines)} lines')
