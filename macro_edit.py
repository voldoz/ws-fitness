#!/usr/bin/env python3
"""
macro_edit.py
─────────────
Adds an "Edit Macros" panel inside the Calculator results card.
- A pencil button appears in the results title bar (coach/admin/user only)
- Clicking it opens an inline edit panel with 3 sliders + number inputs
  for Protein %, Carbs %, Fat %
- The three sliders are linked (always sum to 100%)
- "Apply" recalculates grams & calories and saves back to calc_results
- "Reset" restores the auto-calculated values
- Total calories (and per-meal chips) update live
"""

import re

PATH = "index.html"
txt  = open(PATH, encoding="utf-8").read()
orig = txt

# ─────────────────────────────────────────────────
# 1.  CSS — append to existing calc-results CSS block
# ─────────────────────────────────────────────────
CSS = r"""
  /* ── Macro manual-edit panel ── */
  .calc-edit-btn{
    margin-left:auto; background:rgba(56,189,248,.12);
    border:1px solid rgba(56,189,248,.25); border-radius:10px;
    padding:4px 10px; font-size:11px; font-weight:800; color:#38bdf8;
    cursor:pointer; display:flex; align-items:center; gap:5px;
    transition:background .18s;
  }
  .calc-edit-btn:hover{ background:rgba(56,189,248,.22); }
  .calc-edit-panel{
    background:rgba(6,12,24,.7);
    border:1.5px solid rgba(56,189,248,.18);
    border-radius:18px; padding:16px;
    margin-top:14px; display:none;
    flex-direction:column; gap:12px;
    animation:calc-fadeIn .25s ease;
  }
  .calc-edit-panel.open{ display:flex; }
  .calc-edit-panel-title{
    font-size:12px; font-weight:800; color:#64748b;
    text-transform:uppercase; letter-spacing:.08em;
    display:flex; align-items:center; gap:6px; margin-bottom:4px;
  }
  .calc-edit-row{
    display:flex; flex-direction:column; gap:4px;
  }
  .calc-edit-label{
    display:flex; justify-content:space-between; align-items:center;
    font-size:12px; font-weight:700;
  }
  .calc-edit-label span.pct{
    font-size:14px; font-weight:900;
  }
  .calc-edit-label span.grams{
    font-size:11px; color:#64748b; font-weight:700;
  }
  .calc-edit-slider{
    -webkit-appearance:none; appearance:none;
    width:100%; height:6px; border-radius:6px;
    outline:none; cursor:pointer;
    background:rgba(255,255,255,.08);
    transition:background .2s;
  }
  .calc-edit-slider::-webkit-slider-thumb{
    -webkit-appearance:none; width:20px; height:20px;
    border-radius:50%; cursor:pointer; border:2px solid #0b1628;
    box-shadow:0 2px 6px rgba(0,0,0,.4);
  }
  .calc-edit-slider.p{ accent-color:#38bdf8; }
  .calc-edit-slider.p::-webkit-slider-thumb{ background:#38bdf8; }
  .calc-edit-slider.c{ accent-color:#f97316; }
  .calc-edit-slider.c::-webkit-slider-thumb{ background:#f97316; }
  .calc-edit-slider.f{ accent-color:#a78bfa; }
  .calc-edit-slider.f::-webkit-slider-thumb{ background:#a78bfa; }

  .calc-edit-sum{
    display:flex; justify-content:center; align-items:center;
    font-size:13px; font-weight:800; gap:6px; padding:6px 0;
  }
  .calc-edit-sum .ok{ color:#4ade80; }
  .calc-edit-sum .warn{ color:#f87171; }

  .calc-edit-actions{
    display:flex; gap:8px;
  }
  .calc-edit-apply{
    flex:1; padding:10px; border-radius:12px; font-size:13px;
    font-weight:800; cursor:pointer; border:none;
    background:linear-gradient(135deg,#38bdf8,#818cf8);
    color:#0b1628; transition:opacity .18s;
  }
  .calc-edit-apply:hover{ opacity:.88; }
  .calc-edit-reset{
    padding:10px 16px; border-radius:12px; font-size:13px;
    font-weight:800; cursor:pointer;
    background:rgba(255,255,255,.06);
    border:1px solid rgba(255,255,255,.1); color:#94a3b8;
    transition:background .18s;
  }
  .calc-edit-reset:hover{ background:rgba(255,255,255,.1); }
  .calc-edit-note{
    font-size:10px; color:#475569; text-align:center; font-weight:600;
  }
"""

# Insert after the last calc CSS rule
anchor = "  .calc-results-empty{\n    text-align:center; padding:24px 16px;\n    opacity:.35; font-size:13px;\n    background:rgba(15,23,42,.5); border-radius:18px; margin-top:14px;\n  }"
if anchor in txt:
    txt = txt.replace(anchor, anchor + "\n" + CSS)
    print("✅ CSS injected")
else:
    print("⚠️  CSS anchor not found")

# ─────────────────────────────────────────────────
# 2.  HTML — modify renderCalcResults() to add edit button + panel
# ─────────────────────────────────────────────────
old_results_title = "      <div class=\"calc-results-title\">✅ Your Results</div>"
new_results_title = """      <div class=\"calc-results-title\" style=\"display:flex;align-items:center\">
        ✅ Your Results
        ${canEditEverything()?`<button class=\"calc-edit-btn\" onclick=\"toggleMacroEdit()\" id=\"macroEditBtn\">
          <svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"12\" height=\"12\"><path d=\"M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7\" stroke=\"currentColor\" stroke-width=\"2.2\" stroke-linecap=\"round\"/><path d=\"M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z\" stroke=\"currentColor\" stroke-width=\"2.2\" stroke-linecap=\"round\"/></svg>
          Edit Macros
        </button>`:\"\"}
      </div>"""

if old_results_title in txt:
    txt = txt.replace(old_results_title, new_results_title)
    print("✅ Edit button added to results title")
else:
    print("⚠️  results title not found")

# Add the edit panel right after the burn strip closing tag
old_burn_end = """      <!-- Daily burn -->
      <div class=\"calc-burn-strip\">
        <div class=\"calc-burn-icon\">🔥</div>
        <div class=\"calc-burn-info\">
          <div class=\"calc-burn-label\">Daily Burn Target</div>
          <div class=\"calc-burn-val\" id=\"outBurn\">${r.dailyBurn} kcal</div>
        </div>
      </div>

    </div>\`;"""

new_burn_end = """      <!-- Daily burn -->
      <div class=\"calc-burn-strip\">
        <div class=\"calc-burn-icon\">🔥</div>
        <div class=\"calc-burn-info\">
          <div class=\"calc-burn-label\">Daily Burn Target</div>
          <div class=\"calc-burn-val\" id=\"outBurn\">${r.dailyBurn} kcal</div>
        </div>
      </div>

      <!-- Macro edit panel (coach/admin only) -->
      ${canEditEverything()?`
      <div class=\"calc-edit-panel\" id=\"macroEditPanel\">
        <div class=\"calc-edit-panel-title\">
          <svg viewBox=\"0 0 24 24\" fill=\"none\" width=\"13\" height=\"13\"><path d=\"M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7\" stroke=\"currentColor\" stroke-width=\"2.2\" stroke-linecap=\"round\"/><path d=\"M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z\" stroke=\"currentColor\" stroke-width=\"2.2\" stroke-linecap=\"round\"/></svg>
          Manual Macro Override
        </div>

        <!-- Protein -->
        <div class=\"calc-edit-row\">
          <div class=\"calc-edit-label\">
            <span style=\"color:#38bdf8\">🥩 Protein</span>
            <span class=\"pct\" style=\"color:#38bdf8\" id=\"meP_pct\">${_pPct(r)}%</span>
            <span class=\"grams\" id=\"meP_g\">${r.protein}g · ${Math.round(r.protein*4)} kcal</span>
          </div>
          <input type=\"range\" class=\"calc-edit-slider p\" id=\"meP\" min=\"10\" max=\"60\" step=\"1\" value=\"${_pPct(r)}\"
                 oninput=\"meSlidersInput('p',this.value)\">
        </div>

        <!-- Carbs -->
        <div class=\"calc-edit-row\">
          <div class=\"calc-edit-label\">
            <span style=\"color:#f97316\">🍚 Carbs</span>
            <span class=\"pct\" style=\"color:#f97316\" id=\"meC_pct\">${_cPct(r)}%</span>
            <span class=\"grams\" id=\"meC_g\">${r.carbs}g · ${Math.round(r.carbs*4)} kcal</span>
          </div>
          <input type=\"range\" class=\"calc-edit-slider c\" id=\"meC\" min=\"5\" max=\"70\" step=\"1\" value=\"${_cPct(r)}\"
                 oninput=\"meSlidersInput('c',this.value)\">
        </div>

        <!-- Fat -->
        <div class=\"calc-edit-row\">
          <div class=\"calc-edit-label\">
            <span style=\"color:#a78bfa\">🫒 Fat</span>
            <span class=\"pct\" style=\"color:#a78bfa\" id=\"meF_pct\">${_fPct(r)}%</span>
            <span class=\"grams\" id=\"meF_g\">${r.fat}g · ${Math.round(r.fat*9)} kcal</span>
          </div>
          <input type=\"range\" class=\"calc-edit-slider f\" id=\"meF\" min=\"5\" max=\"50\" step=\"1\" value=\"${_fPct(r)}\"
                 oninput=\"meSlidersInput('f',this.value)\">
        </div>

        <!-- Sum check -->
        <div class=\"calc-edit-sum\" id=\"meSum\">
          <span>Total: <b id=\"meSumVal\">${_pPct(r)+_cPct(r)+_fPct(r)}</b>%</span>
          <span id=\"meSumStatus\" class=\"ok\">✓</span>
        </div>

        <div class=\"calc-edit-note\">Calories will be recalculated from the new macro split.</div>

        <div class=\"calc-edit-actions\">
          <button class=\"calc-edit-reset\" onclick=\"meReset()\">↺ Auto</button>
          <button class=\"calc-edit-apply\" onclick=\"meApply()\">✓ Apply & Save</button>
        </div>
      </div>
      `:\"\"}

    </div>\`;"""

if old_burn_end in txt:
    txt = txt.replace(old_burn_end, new_burn_end)
    print("✅ Edit panel HTML added to results card")
else:
    print("⚠️  burn end pattern not found — trying alternate")
    # try without the trailing backtick-semicolon alignment issue
    check = "    </div>`;"
    count = txt.count(check)
    print(f"   Found {count} occurrences of closing backtick pattern")

# ─────────────────────────────────────────────────
# 3.  Helper: % calculators used inside template literals
#     Add before renderCalcResults()
# ─────────────────────────────────────────────────
insert_before = "function renderCalcResults(){"
helpers = """/* ── macro edit helpers ── */
function _totKcal(r){ return Number(r.calories)||1; }
function _pPct(r){ return Math.round((Number(r.protein||0)*4)/_totKcal(r)*100); }
function _cPct(r){ return Math.round((Number(r.carbs||0)*4)/_totKcal(r)*100); }
function _fPct(r){ return Math.round((Number(r.fat||0)*9)/_totKcal(r)*100); }

function toggleMacroEdit(){
  const p=$("macroEditPanel"); if(!p) return;
  p.classList.toggle("open");
  const btn=$("macroEditBtn"); if(btn) btn.textContent=p.classList.contains("open")?"✕ Close":"✏ Edit Macros";
}

/* called when a slider moves — clamp the other two proportionally */
function meSlidersInput(changed, val){
  val=parseInt(val);
  const pSlider=$("meP"), cSlider=$("meC"), fSlider=$("meF");
  if(!pSlider||!cSlider||!fSlider) return;
  let p=parseInt(pSlider.value), c=parseInt(cSlider.value), f=parseInt(fSlider.value);
  if(changed==="p") p=val;
  else if(changed==="c") c=val;
  else f=val;

  /* keep min 5 for unchanged, redistribute remainder */
  const MIN=5;
  if(changed!=="p"){ p=Math.max(MIN,p); }
  if(changed!=="c"){ c=Math.max(MIN,c); }
  if(changed!=="f"){ f=Math.max(MIN,f); }

  /* update display labels */
  pSlider.value=p; cSlider.value=c; fSlider.value=f;
  const total=p+c+f;
  const sumEl=$("meSumVal"); if(sumEl) sumEl.textContent=total;
  const st=$("meSumStatus");
  if(st){ st.className=Math.abs(total-100)<=2?"ok":"warn"; st.textContent=Math.abs(total-100)<=2?"✓":"⚠"; }

  /* live gram preview */
  const r=loadCalcResults(); if(!r) return;
  const kcal=Number(r.calories)||2000;
  const pg=Math.round(kcal*(p/100)/4);
  const cg=Math.round(kcal*(c/100)/4);
  const fg=Math.round(kcal*(f/100)/9);
  const pEl=$("meP_pct"); if(pEl) pEl.textContent=p+"%";
  const cEl=$("meC_pct"); if(cEl) cEl.textContent=c+"%";
  const fEl=$("meF_pct"); if(fEl) fEl.textContent=f+"%";
  const pgEl=$("meP_g");  if(pgEl) pgEl.textContent=pg+"g · "+Math.round(pg*4)+" kcal";
  const cgEl=$("meC_g");  if(cgEl) cgEl.textContent=cg+"g · "+Math.round(cg*4)+" kcal";
  const fgEl=$("meF_g");  if(fgEl) fgEl.textContent=fg+"g · "+Math.round(fg*9)+" kcal";
}

function meApply(){
  if(!canEditEverything()) return;
  const r=loadCalcResults(); if(!r){ alert("Run the calculator first."); return; }
  const p=parseInt($("meP")?.value||"0");
  const c=parseInt($("meC")?.value||"0");
  const f=parseInt($("meF")?.value||"0");
  const total=p+c+f;
  if(Math.abs(total-100)>3){ alert("Percentages must sum to ~100%. Current total: "+total+"%"); return; }

  /* keep same total calories, redistribute macros */
  const kcal=Number(r.calories)||2000;
  const protein=Math.round(kcal*(p/100)/4);
  const carbs  =Math.round(kcal*(c/100)/4);
  const fat    =Math.round(kcal*(f/100)/9);
  const meals  =Number(r.meals||1);

  const updated={
    ...r,
    protein, carbs, fat,
    proteinMeal:Math.round(protein/meals),
    carbsMeal:  Math.round(carbs/meals),
    fatMeal:    Math.round(fat/meals),
    _manualMacros:{p,c,f}   /* flag that macros were manually overridden */
  };
  storeCalcResults(updated);
  renderCalcResults();
  /* re-open edit panel after re-render */
  setTimeout(()=>{
    const panel=$("macroEditPanel");
    if(panel) panel.classList.add("open");
    const btn=$("macroEditBtn");
    if(btn) btn.innerHTML=`<svg viewBox="0 0 24 24" fill="none" width="12" height="12"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg> Edit Macros`;
  }, 80);
}

function meReset(){
  if(!canEditEverything()) return;
  const r=loadCalcResults(); if(!r) return;
  /* strip manual override and re-run formula */
  delete r._manualMacros;
  storeCalcResults(r);
  /* re-trigger full calc using stored inputs */
  const inp=pget("calc_inputs"); if(!inp) return;
  const d=JSON.parse(inp);
  /* temporarily load inputs back and run calcAndSave */
  $("weight").value=d.weight||""; $("height").value=d.height||"";
  $("age").value=d.age||""; $("gender").value=d.gender||"male";
  $("activityDays").value=d.activityDays||"3"; $("goal").value=d.goal||"cut";
  $("proteinFactor").value=d.proteinFactor||"2.2";
  $("meals").value=d.meals||"3"; $("weeklyGoal").value=d.weeklyGoal||"0.5";
  calcAndSave();
}

"""

if insert_before in txt:
    txt = txt.replace(insert_before, helpers + insert_before, 1)
    print("✅ Helper functions injected before renderCalcResults")
else:
    print("⚠️  renderCalcResults anchor not found")

# ─────────────────────────────────────────────────
# 4. Write
# ─────────────────────────────────────────────────
open(PATH, "w", encoding="utf-8").write(txt)
print(f"\n✅ Done — {len(orig)} → {len(txt)} chars, {txt.count(chr(10))+1} lines")
