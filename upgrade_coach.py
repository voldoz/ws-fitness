#!/usr/bin/env python3
# upgrade_coach.py – Complete Coach Panel Upgrade
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

original_len = len(html)

# ─────────────────────────────────────────────
# 1. REPLACE the coach panel CSS (animations + all .cp-* classes)
# ─────────────────────────────────────────────
OLD_CSS = '''  @keyframes cp-rise  { from{opacity:0;transform:translateY(16px)} to{opacity:1;transform:none} }
  @keyframes cp-pop   { 0%{transform:scale(.9)} 60%{transform:scale(1.04)} 100%{transform:scale(1)} }
  @keyframes cp-slide { from{opacity:0;transform:translateX(100%)} to{opacity:1;transform:none} }
  @keyframes cp-shine {
    0%   { background-position:200% center; }
    100% { background-position:-200% center; }
  }'''

NEW_CSS = '''  /* ═══════════════════════════════════════════════
     COACH PANEL – PREMIUM REDESIGN
     ═══════════════════════════════════════════════ */
  @keyframes cp-rise  { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:none} }
  @keyframes cp-pop   { 0%{transform:scale(.88)} 55%{transform:scale(1.06)} 100%{transform:scale(1)} }
  @keyframes cp-slide { from{opacity:0;transform:translateX(100%)} to{opacity:1;transform:translateX(0)} }
  @keyframes cp-shine {
    0%   { background-position:200% center; }
    100% { background-position:-200% center; }
  }
  @keyframes cp-pulse { 0%,100%{opacity:1} 50%{opacity:.5} }
  @keyframes cp-glow  { 0%,100%{box-shadow:0 0 0 0 rgba(56,189,248,.4)} 50%{box-shadow:0 0 0 8px rgba(56,189,248,0)} }'''

if OLD_CSS in html:
    html = html.replace(OLD_CSS, NEW_CSS, 1)
    print('CSS animations replaced OK')
else:
    print('WARNING: CSS animations block not found')

# ─────────────────────────────────────────────
# 2. REPLACE .cp-page through .cp-add-card-lbl (grid + cards CSS)
# ─────────────────────────────────────────────
OLD_GRID_CSS = '''  .cp-page{ animation:cp-rise .35s cubic-bezier(.22,1,.36,1) both; }

  /* ── Top header ── */
  .cp-header{
    background:linear-gradient(145deg,#0a1628,#0e1e38);
    border-radius:22px; padding:18px 20px; margin-bottom:16px;
    border:1.5px solid rgba(56,189,248,.12);
    box-shadow:0 8px 32px rgba(0,0,0,.4), inset 0 1px 0 rgba(255,255,255,.05);
    display:flex; align-items:center; justify-content:space-between; gap:12px;
  }
  .cp-header-left{ display:flex; flex-direction:column; gap:3px; }
  .cp-header-title{
    font-size:18px; font-weight:900;
    background:linear-gradient(90deg,#38bdf8,#818cf8);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
  }
  .cp-header-sub{ font-size:11px; color:#64748b; font-weight:600; }
  .cp-header-icon{ font-size:30px; flex-shrink:0; }
  /* ── Stats row under header ── */
  .cp-stats{
    display:flex; gap:8px; margin-bottom:16px; overflow-x:auto; scrollbar-width:none;
  }
  .cp-stats::-webkit-scrollbar{ display:none; }
  .cp-stat{
    flex-shrink:0; min-width:90px;
    background:linear-gradient(145deg,#0d1829,#111e30);
    border-radius:16px; padding:12px 14px; text-align:center;
    border:1.5px solid rgba(255,255,255,.07);
    animation:cp-rise .35s both;
  }
  .cp-stat-val{ font-size:22px; font-weight:900; color:#e2e8f0; line-height:1; }
  .cp-stat-val.green{ color:#4ade80; }
  .cp-stat-val.yellow{ color:#fbbf24; }
  .cp-stat-val.red{ color:#f87171; }
  .cp-stat-lbl{ font-size:9px; font-weight:700; opacity:.4; text-transform:uppercase; letter-spacing:.05em; margin-top:3px; }

  /* ── Search / filter bar ── */
  .cp-search-row{
    display:flex; gap:8px; margin-bottom:14px; align-items:center;
  }
  .cp-search{
    flex:1; background:#0f172a; color:#e2e8f0;
    border:1.5px solid rgba(255,255,255,.08); border-radius:14px;
    padding:10px 14px; font-size:14px; outline:none; transition:border-color .18s;
  }
  .cp-search:focus{ border-color:rgba(56,189,248,.5); }
  .cp-search::placeholder{ color:#334155; }
  .cp-filter-btn{
    padding:10px 14px; border-radius:14px; border:none; cursor:pointer;
    font-size:12px; font-weight:800; transition:all .18s;
    background:rgba(255,255,255,.05); color:#64748b;
    border:1.5px solid rgba(255,255,255,.07); white-space:nowrap;
  }
  .cp-filter-btn.active{
    background:rgba(56,189,248,.12); color:#38bdf8;
    border-color:rgba(56,189,248,.3);
  }

  /* ── Subscriber grid ── */
  .cp-grid{
    display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:16px;
  }
  @media(min-width:500px){ .cp-grid{ grid-template-columns:1fr 1fr 1fr; } }
  .cp-sub-card{
    background:linear-gradient(145deg,#0d1829,#111e30);
    border-radius:20px; padding:16px 14px 14px; cursor:pointer;
    border:1.5px solid rgba(255,255,255,.06);
    transition:all .22s cubic-bezier(.34,1.56,.64,1);
    position:relative; overflow:hidden;
    animation:cp-rise .35s cubic-bezier(.22,1,.36,1) both;
    -webkit-tap-highlight-color:transparent;
  }
  .cp-sub-card::before{
    content:''; position:absolute; inset:0; border-radius:19px;
    background:linear-gradient(135deg,rgba(56,189,248,.07),rgba(129,140,248,.05));
    opacity:0; transition:opacity .22s;
  }
  .cp-sub-card:hover{ transform:translateY(-3px) scale(1.02); border-color:rgba(56,189,248,.3); }
  .cp-sub-card:hover::before{ opacity:1; }
  .cp-sub-card:active{ transform:scale(.96); }
  .cp-sub-card.expired{ border-color:rgba(239,68,68,.18); }
  .cp-sub-card.expiring{ border-color:rgba(251,191,36,.22); }

  /* avatar */
  .cp-card-avatar{
    width:56px; height:56px; border-radius:16px; margin:0 auto 10px;
    display:flex; align-items:center; justify-content:center;
    font-size:20px; font-weight:900; letter-spacing:-.5px;
    background:linear-gradient(135deg,#0f2744,#1a3a5c);
    border:2px solid rgba(56,189,248,.25);
    overflow:hidden; position:relative;
  }
  .cp-card-avatar img{ width:100%; height:100%; object-fit:cover; border-radius:14px; }
  .cp-card-avatar-txt{
    background:linear-gradient(135deg,#38bdf8,#818cf8);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
  }
  /* status dot on avatar */
  .cp-card-dot{
    position:absolute; bottom:-2px; right:-2px;
    width:14px; height:14px; border-radius:50%;
    border:2px solid #0d1829;
  }
  .cp-card-dot.active{ background:#22c55e; }
  .cp-card-dot.expiring{ background:#fbbf24; }
  .cp-card-dot.expired{ background:#ef4444; }

  .cp-card-name{
    font-size:13px; font-weight:800; color:#e2e8f0; text-align:center;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
    margin-bottom:4px;
  }
  .cp-card-days{
    text-align:center; font-size:10px; font-weight:700;
    padding:3px 8px; border-radius:20px; display:inline-block;
    width:100%; box-sizing:border-box;
  }
  .cp-card-days.active{ color:#4ade80; background:rgba(34,197,94,.1); }
  .cp-card-days.expiring{ color:#fbbf24; background:rgba(251,191,36,.1); }
  .cp-card-days.expired{ color:#f87171; background:rgba(239,68,68,.1); }

  /* ── Add subscriber card ── */
  .cp-add-card{
    background:linear-gradient(145deg,#0d1829,#111e30);
    border-radius:20px; padding:16px 14px 14px; cursor:pointer;
    border:1.5px dashed rgba(56,189,248,.2);
    display:flex; flex-direction:column; align-items:center; justify-content:center; gap:6px;
    min-height:120px; transition:all .22s; color:#38bdf8;
    animation:cp-rise .35s .1s cubic-bezier(.22,1,.36,1) both;
  }
  .cp-add-card:hover{ background:rgba(56,189,248,.06); border-color:rgba(56,189,248,.45); transform:scale(1.02); }
  .cp-add-card-icon{ font-size:24px; }
  .cp-add-card-lbl{ font-size:11px; font-weight:800; opacity:.7; }'''

NEW_GRID_CSS = '''  /* ── Page wrapper ── */
  .cp-page{ animation:cp-rise .38s cubic-bezier(.22,1,.36,1) both; padding-bottom:24px; }

  /* ── Hero Header ── */
  .cp-header{
    background:linear-gradient(145deg,#070e1c,#0c1830,#0e2040);
    border-radius:24px; padding:20px; margin-bottom:14px;
    border:1.5px solid rgba(56,189,248,.15);
    box-shadow:0 12px 40px rgba(0,0,0,.5), inset 0 1px 0 rgba(255,255,255,.06);
    display:flex; align-items:center; justify-content:space-between; gap:12px;
    position:relative; overflow:hidden;
  }
  .cp-header::after{
    content:''; position:absolute; top:-40px; right:-40px;
    width:160px; height:160px; border-radius:50%;
    background:radial-gradient(circle,rgba(56,189,248,.1) 0%,transparent 70%);
    pointer-events:none;
  }
  .cp-header-left{ display:flex; flex-direction:column; gap:4px; }
  .cp-header-title{
    font-size:20px; font-weight:900; letter-spacing:-.3px;
    background:linear-gradient(90deg,#38bdf8,#818cf8,#a78bfa);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
  }
  .cp-header-sub{ font-size:12px; color:#475569; font-weight:700; }
  .cp-header-icon{
    font-size:32px; flex-shrink:0; width:52px; height:52px;
    background:linear-gradient(135deg,rgba(56,189,248,.1),rgba(129,140,248,.1));
    border-radius:16px; display:flex; align-items:center; justify-content:center;
    border:1.5px solid rgba(56,189,248,.15);
  }

  /* ── Stats pills ── */
  .cp-stats{
    display:grid; grid-template-columns:repeat(4,1fr); gap:8px; margin-bottom:14px;
  }
  .cp-stat{
    background:linear-gradient(145deg,#0a1525,#0e1e35);
    border-radius:16px; padding:12px 8px; text-align:center;
    border:1.5px solid rgba(255,255,255,.06);
    animation:cp-rise .35s both; cursor:default;
    transition:transform .18s; position:relative; overflow:hidden;
  }
  .cp-stat::before{
    content:''; position:absolute; bottom:0; left:0; right:0; height:2px;
    background:linear-gradient(90deg,transparent,rgba(56,189,248,.3),transparent);
    opacity:0; transition:opacity .2s;
  }
  .cp-stat:hover{ transform:translateY(-2px); }
  .cp-stat:hover::before{ opacity:1; }
  .cp-stat-val{ font-size:22px; font-weight:900; color:#e2e8f0; line-height:1; }
  .cp-stat-val.green{ color:#4ade80; }
  .cp-stat-val.yellow{ color:#fbbf24; }
  .cp-stat-val.red{ color:#f87171; }
  .cp-stat-lbl{ font-size:9px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:.06em; margin-top:4px; }

  /* ── Search / filter bar ── */
  .cp-search-row{
    display:flex; gap:8px; margin-bottom:14px; align-items:center;
  }
  .cp-search{
    flex:1; background:rgba(15,23,42,.9); color:#e2e8f0;
    border:1.5px solid rgba(255,255,255,.07); border-radius:14px;
    padding:11px 14px; font-size:14px; outline:none; transition:all .2s;
  }
  .cp-search:focus{ border-color:rgba(56,189,248,.5); background:#0a1525; box-shadow:0 0 0 3px rgba(56,189,248,.08); }
  .cp-search::placeholder{ color:#2d3f5a; }
  .cp-filter-btn{
    padding:11px 14px; border-radius:14px; border:none; cursor:pointer;
    font-size:12px; font-weight:800; transition:all .2s;
    background:rgba(255,255,255,.04); color:#475569;
    border:1.5px solid rgba(255,255,255,.06); white-space:nowrap;
  }
  .cp-filter-btn.active{
    background:rgba(56,189,248,.12); color:#38bdf8;
    border-color:rgba(56,189,248,.35); box-shadow:0 2px 12px rgba(56,189,248,.15);
  }

  /* ── Subscriber grid ── */
  .cp-grid{
    display:grid; grid-template-columns:1fr 1fr; gap:10px; margin-bottom:16px;
  }
  @media(min-width:480px){ .cp-grid{ grid-template-columns:1fr 1fr 1fr; } }

  .cp-sub-card{
    background:linear-gradient(160deg,#0b1726,#0f1f35);
    border-radius:22px; padding:18px 14px 14px; cursor:pointer;
    border:1.5px solid rgba(255,255,255,.06);
    transition:all .25s cubic-bezier(.34,1.56,.64,1);
    position:relative; overflow:hidden; display:flex; flex-direction:column; align-items:center;
    animation:cp-rise .38s cubic-bezier(.22,1,.36,1) both;
    -webkit-tap-highlight-color:transparent;
    box-shadow:0 4px 16px rgba(0,0,0,.3);
  }
  .cp-sub-card::before{
    content:''; position:absolute; top:0; left:0; right:0; height:50%;
    background:linear-gradient(180deg,rgba(56,189,248,.05),transparent);
    opacity:0; transition:opacity .25s; border-radius:22px 22px 0 0;
  }
  .cp-sub-card::after{
    content:''; position:absolute; inset:0;
    background:linear-gradient(135deg,rgba(56,189,248,.06),rgba(129,140,248,.04));
    opacity:0; transition:opacity .22s; border-radius:21px;
  }
  .cp-sub-card:hover{ transform:translateY(-4px) scale(1.03); border-color:rgba(56,189,248,.35); box-shadow:0 12px 32px rgba(0,0,0,.5); }
  .cp-sub-card:hover::before, .cp-sub-card:hover::after{ opacity:1; }
  .cp-sub-card:active{ transform:scale(.95); }
  .cp-sub-card.expired{ border-color:rgba(239,68,68,.2); background:linear-gradient(160deg,#170b0b,#1e1020); }
  .cp-sub-card.expiring{ border-color:rgba(251,191,36,.25); background:linear-gradient(160deg,#16120a,#1c1830); }

  /* avatar circle */
  .cp-card-avatar{
    width:60px; height:60px; border-radius:18px; margin-bottom:10px;
    display:flex; align-items:center; justify-content:center;
    font-size:22px; font-weight:900; letter-spacing:-.5px;
    background:linear-gradient(135deg,#0f2744,#1a3a5c);
    border:2.5px solid rgba(56,189,248,.3);
    overflow:hidden; position:relative; flex-shrink:0;
    box-shadow:0 4px 16px rgba(0,0,0,.4);
  }
  .cp-card-avatar img{ width:100%; height:100%; object-fit:cover; }
  .cp-card-avatar-txt{
    background:linear-gradient(135deg,#38bdf8,#818cf8);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
  }
  .cp-card-dot{
    position:absolute; bottom:-1px; right:-1px;
    width:16px; height:16px; border-radius:50%;
    border:2.5px solid #0b1726;
  }
  .cp-card-dot.active{ background:#22c55e; animation:cp-glow 2s infinite; }
  .cp-card-dot.expiring{ background:#fbbf24; }
  .cp-card-dot.expired{ background:#ef4444; }

  .cp-card-name{
    font-size:13px; font-weight:900; color:#e2e8f0; text-align:center;
    white-space:nowrap; overflow:hidden; text-overflow:ellipsis;
    width:100%; margin-bottom:6px; letter-spacing:-.1px;
  }
  .cp-card-days{
    text-align:center; font-size:10px; font-weight:800;
    padding:4px 10px; border-radius:20px; display:inline-block;
    width:100%; box-sizing:border-box; letter-spacing:.01em;
  }
  .cp-card-days.active{ color:#4ade80; background:rgba(34,197,94,.12); border:1px solid rgba(34,197,94,.2); }
  .cp-card-days.expiring{ color:#fbbf24; background:rgba(251,191,36,.12); border:1px solid rgba(251,191,36,.2); }
  .cp-card-days.expired{ color:#f87171; background:rgba(239,68,68,.12); border:1px solid rgba(239,68,68,.2); }

  /* ── Add subscriber card ── */
  .cp-add-card{
    background:transparent;
    border-radius:22px; padding:18px 14px 14px; cursor:pointer;
    border:2px dashed rgba(56,189,248,.25);
    display:flex; flex-direction:column; align-items:center; justify-content:center; gap:8px;
    min-height:130px; transition:all .25s; color:#38bdf8;
    animation:cp-rise .38s .12s cubic-bezier(.22,1,.36,1) both;
    -webkit-tap-highlight-color:transparent;
  }
  .cp-add-card:hover{ background:rgba(56,189,248,.05); border-color:rgba(56,189,248,.5); transform:scale(1.03); box-shadow:0 8px 24px rgba(56,189,248,.1); }
  .cp-add-card:active{ transform:scale(.95); }
  .cp-add-card-icon{ font-size:28px; width:44px; height:44px; border-radius:14px; display:flex; align-items:center; justify-content:center; background:rgba(56,189,248,.1); border:1px solid rgba(56,189,248,.2); }
  .cp-add-card-lbl{ font-size:11px; font-weight:800; opacity:.8; }'''

if OLD_GRID_CSS in html:
    html = html.replace(OLD_GRID_CSS, NEW_GRID_CSS, 1)
    print('Grid CSS replaced OK')
else:
    print('WARNING: Grid CSS block not found — trying partial replace')
    # Try replacing just the header part
    if '.cp-page{ animation:cp-rise .35s cubic-bezier(.22,1,.36,1) both; }' in html:
        print('  Found .cp-page selector')

# ─────────────────────────────────────────────
# 3. REPLACE drawer CSS
# ─────────────────────────────────────────────
OLD_DRAWER_CSS = '''  /* ══════════════════════════════════════════════
     SUBSCRIBER DRAWER (full-screen slide-in)
     ══════════════════════════════════════════════ */
  .cp-drawer{
    position:fixed; inset:0; z-index:8000;
    background:#060d1a;
    transform:translateX(100%);
    transition:transform .32s cubic-bezier(.22,1,.36,1);
    display:flex; flex-direction:column; overflow:hidden;
  }
  .cp-drawer.open{ transform:none; }

  /* drawer top bar */
  .cp-drawer-bar{
    display:flex; align-items:center; gap:12px;
    padding:14px 16px; flex-shrink:0;
    background:linear-gradient(145deg,#080f20,#0c1830);
    border-bottom:1px solid rgba(255,255,255,.06);
  }
  .cp-drawer-back{
    width:38px; height:38px; border-radius:12px; border:none; cursor:pointer;
    background:rgba(255,255,255,.07); color:#e2e8f0; font-size:18px;
    display:flex; align-items:center; justify-content:center; flex-shrink:0;
    transition:all .18s;
  }
  .cp-drawer-back:active{ transform:scale(.92); background:rgba(56,189,248,.15); }
  .cp-drawer-bar-avatar{
    width:36px; height:36px; border-radius:10px;
    background:linear-gradient(135deg,#0f2744,#1a3a5c);
    border:1.5px solid rgba(56,189,248,.3);
    display:flex; align-items:center; justify-content:center;
    font-size:13px; font-weight:900; overflow:hidden; flex-shrink:0;
  }
  .cp-drawer-bar-avatar img{ width:100%; height:100%; object-fit:cover; }
  .cp-drawer-bar-info{ flex:1; min-width:0; }
  .cp-drawer-bar-name{ font-size:15px; font-weight:900; color:#e2e8f0; }
  .cp-drawer-bar-status{ font-size:10px; font-weight:700; margin-top:1px; }
  .cp-drawer-bar-status.active{ color:#4ade80; }
  .cp-drawer-bar-status.expired{ color:#f87171; }
  .cp-drawer-bar-status.expiring{ color:#fbbf24; }

  /* drawer quick-nav tabs */
  .cp-drawer-tabs{
    display:flex; gap:0; overflow-x:auto; scrollbar-width:none;
    background:rgba(0,0,0,.3); border-bottom:1px solid rgba(255,255,255,.06);
    flex-shrink:0;
  }
  .cp-drawer-tabs::-webkit-scrollbar{ display:none; }
  .cp-drawer-tab{
    padding:10px 16px; border:none; cursor:pointer; white-space:nowrap;
    background:transparent; color:#475569; font-size:12px; font-weight:800;
    border-bottom:2.5px solid transparent; transition:all .18s; flex-shrink:0;
    display:flex; align-items:center; gap:6px;
  }
  .cp-drawer-tab.active{
    color:#38bdf8; border-bottom-color:#38bdf8;
    background:rgba(56,189,248,.06);
  }
  .cp-drawer-tab svg{ width:14px; height:14px; }

  /* drawer content area */
  .cp-drawer-body{
    flex:1; overflow-y:auto; padding:0; -webkit-overflow-scrolling:touch;
  }
  .cp-drawer-body .page{ display:block !important; padding-bottom:20px; }

  /* subscriber info card at top of drawer */
  .cp-sub-info-card{
    margin:12px; border-radius:18px; padding:16px;
    background:linear-gradient(145deg,#0d1829,#111e30);
    border:1.5px solid rgba(56,189,248,.12);
    display:flex; gap:14px; align-items:center;
  }
  .cp-sub-info-avatar{
    width:52px; height:52px; border-radius:14px; flex-shrink:0;
    background:linear-gradient(135deg,#0f2744,#1a3a5c);
    border:2px solid rgba(56,189,248,.3);
    display:flex; align-items:center; justify-content:center;
    font-size:18px; font-weight:900; overflow:hidden;
  }
  .cp-sub-info-avatar img{ width:100%; height:100%; object-fit:cover; }
  .cp-sub-info-avatar-txt{
    background:linear-gradient(135deg,#38bdf8,#818cf8);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
  }
  .cp-sub-info-details{ flex:1; min-width:0; }
  .cp-sub-info-name{ font-size:16px; font-weight:900; color:#e2e8f0; margin-bottom:4px; }
  .cp-sub-info-pills{ display:flex; gap:6px; flex-wrap:wrap; }
  .cp-sub-info-pill{
    padding:3px 10px; border-radius:20px; font-size:10px; font-weight:800;
  }
  .cp-sub-info-pill.green{ background:rgba(34,197,94,.12); color:#4ade80; }
  .cp-sub-info-pill.red  { background:rgba(239,68,68,.12);  color:#f87171; }
  .cp-sub-info-pill.yellow{ background:rgba(251,191,36,.12); color:#fbbf24; }
  .cp-sub-info-pill.blue { background:rgba(56,189,248,.12); color:#38bdf8; }'''

NEW_DRAWER_CSS = '''  /* ══════════════════════════════════════════════
     SUBSCRIBER DRAWER (full-screen slide-in)
     ══════════════════════════════════════════════ */
  .cp-drawer{
    position:fixed; inset:0; z-index:8000;
    background:#060c19;
    transform:translateX(100%);
    transition:transform .35s cubic-bezier(.22,1,.36,1);
    display:flex; flex-direction:column; overflow:hidden;
  }
  .cp-drawer.open{ transform:translateX(0); }

  /* drawer top bar — hero style */
  .cp-drawer-bar{
    display:flex; align-items:center; gap:12px;
    padding:14px 16px 12px; flex-shrink:0;
    background:linear-gradient(180deg,#070e20 0%,#0a1628 100%);
    border-bottom:1px solid rgba(255,255,255,.07);
    position:relative;
  }
  .cp-drawer-bar::after{
    content:''; position:absolute; bottom:-1px; left:0; right:0; height:1px;
    background:linear-gradient(90deg,transparent,rgba(56,189,248,.4),transparent);
  }
  .cp-drawer-back{
    width:40px; height:40px; border-radius:13px; border:none; cursor:pointer;
    background:rgba(255,255,255,.07); color:#94a3b8; font-size:18px;
    display:flex; align-items:center; justify-content:center; flex-shrink:0;
    transition:all .2s; border:1.5px solid rgba(255,255,255,.07);
  }
  .cp-drawer-back:hover{ background:rgba(56,189,248,.12); color:#38bdf8; border-color:rgba(56,189,248,.3); }
  .cp-drawer-back:active{ transform:scale(.9); }
  .cp-drawer-bar-avatar{
    width:40px; height:40px; border-radius:13px;
    background:linear-gradient(135deg,#0f2744,#1a3a5c);
    border:2px solid rgba(56,189,248,.35);
    display:flex; align-items:center; justify-content:center;
    font-size:14px; font-weight:900; overflow:hidden; flex-shrink:0;
    box-shadow:0 4px 12px rgba(0,0,0,.4);
  }
  .cp-drawer-bar-avatar img{ width:100%; height:100%; object-fit:cover; }
  .cp-drawer-bar-info{ flex:1; min-width:0; }
  .cp-drawer-bar-name{ font-size:15px; font-weight:900; color:#e2e8f0; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
  .cp-drawer-bar-status{ font-size:10px; font-weight:700; margin-top:2px; }
  .cp-drawer-bar-status.active{ color:#4ade80; }
  .cp-drawer-bar-status.expired{ color:#f87171; }
  .cp-drawer-bar-status.expiring{ color:#fbbf24; }

  /* drawer quick-nav tabs */
  .cp-drawer-tabs{
    display:flex; gap:0; overflow-x:auto; scrollbar-width:none;
    background:rgba(6,12,25,.95); border-bottom:1px solid rgba(255,255,255,.06);
    flex-shrink:0; padding:0 2px;
  }
  .cp-drawer-tabs::-webkit-scrollbar{ display:none; }
  .cp-drawer-tab{
    padding:11px 14px 10px; border:none; cursor:pointer; white-space:nowrap;
    background:transparent; color:#3d5068; font-size:11px; font-weight:800;
    border-bottom:2.5px solid transparent; transition:all .2s; flex-shrink:0;
    display:flex; align-items:center; gap:5px; letter-spacing:.01em;
  }
  .cp-drawer-tab:hover{ color:#64748b; }
  .cp-drawer-tab.active{
    color:#38bdf8; border-bottom-color:#38bdf8;
    background:linear-gradient(180deg,rgba(56,189,248,.07),transparent);
  }
  .cp-drawer-tab svg{ width:13px; height:13px; }

  /* drawer content area */
  .cp-drawer-body{
    flex:1; overflow-y:auto; padding:0; -webkit-overflow-scrolling:touch;
    scroll-behavior:smooth;
  }
  .cp-drawer-body .page{ display:block !important; padding-bottom:24px; }

  /* subscriber info card at top of overview */
  .cp-sub-info-card{
    margin:12px 12px 0; border-radius:20px; padding:18px;
    background:linear-gradient(145deg,#08142a,#0c1e3a);
    border:1.5px solid rgba(56,189,248,.15);
    display:flex; gap:16px; align-items:center;
    box-shadow:0 8px 24px rgba(0,0,0,.4);
    position:relative; overflow:hidden;
  }
  .cp-sub-info-card::before{
    content:''; position:absolute; top:-30px; right:-30px;
    width:120px; height:120px; border-radius:50%;
    background:radial-gradient(circle,rgba(56,189,248,.08) 0%,transparent 70%);
    pointer-events:none;
  }
  .cp-sub-info-avatar{
    width:64px; height:64px; border-radius:18px; flex-shrink:0;
    background:linear-gradient(135deg,#0f2744,#1a3a5c);
    border:2.5px solid rgba(56,189,248,.35);
    display:flex; align-items:center; justify-content:center;
    font-size:22px; font-weight:900; overflow:hidden;
    box-shadow:0 6px 20px rgba(0,0,0,.5);
  }
  .cp-sub-info-avatar img{ width:100%; height:100%; object-fit:cover; }
  .cp-sub-info-avatar-txt{
    background:linear-gradient(135deg,#38bdf8,#818cf8);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text;
  }
  .cp-sub-info-details{ flex:1; min-width:0; }
  .cp-sub-info-name{ font-size:18px; font-weight:900; color:#e2e8f0; margin-bottom:6px; letter-spacing:-.2px; }
  .cp-sub-info-pills{ display:flex; gap:6px; flex-wrap:wrap; }
  .cp-sub-info-pill{
    padding:4px 10px; border-radius:20px; font-size:10px; font-weight:800; letter-spacing:.02em;
  }
  .cp-sub-info-pill.green{ background:rgba(34,197,94,.12); color:#4ade80; border:1px solid rgba(34,197,94,.2); }
  .cp-sub-info-pill.red  { background:rgba(239,68,68,.12);  color:#f87171; border:1px solid rgba(239,68,68,.2); }
  .cp-sub-info-pill.yellow{ background:rgba(251,191,36,.12); color:#fbbf24; border:1px solid rgba(251,191,36,.2); }
  .cp-sub-info-pill.blue { background:rgba(56,189,248,.12); color:#38bdf8; border:1px solid rgba(56,189,248,.2); }'''

if OLD_DRAWER_CSS in html:
    html = html.replace(OLD_DRAWER_CSS, NEW_DRAWER_CSS, 1)
    print('Drawer CSS replaced OK')
else:
    print('WARNING: Drawer CSS not found')

# ─────────────────────────────────────────────
# 4. FIX cpDrawerTab – the "work" tab key vs "cpTabWorkouts" mismatch
#    and improve the inner content rendering
# ─────────────────────────────────────────────
OLD_DRAWER_TAB_FN = '''function cpDrawerTab(tab){
  ["overview","work","weight","calc","week","macros","manage"].forEach(t=>{
    const el=$("cpTab"+t.charAt(0).toUpperCase()+t.slice(1));
    if(el) el.classList.toggle("active", t===tab);
  });
  const body=$("cpDrawerBody"); if(!body) return;
  body.scrollTop=0;
  if(tab==="overview")  { cpDrawerOverview(); return; }
  if(tab==="manage")    { cpDrawerManage();   return; }
  /* render real page content inside drawer */
  body.innerHTML=`<div style="padding:8px 0" id="cpDrawerInner"></div>`;
  const inner=$("cpDrawerInner");
  if(tab==="work"){
    inner.innerHTML=`<div class="wo-page" id="workContainer"></div><div style="padding:0 12px 8px"><button class="wo-reset-btn hidden" id="workResetBtn" onclick="resetWorkouts()">Reset Workouts</button></div>`;
    renderWorkouts(); applyWorkButtons();
  }
  if(tab==="weight"){
    inner.innerHTML=`<div style="padding:12px" id="weightRows"></div><div style="padding:0 12px 8px"><button class="mini hidden" id="weightResetBtn" onclick="resetWeightData()">Reset</button></div>`;
    loadWeightTracker(); applyWeightButtons();
  }
  if(tab==="calc"){
    inner.innerHTML=`<div class="calc-page" id="calcInputsWrap" style="display:none"></div><div id="cpCalcResults"></div>`;
    loadCalcInputs(); renderCalcMode(); renderCalcResults(); renderSubscriberCalcView();
  }
  if(tab==="week"){
    inner.innerHTML=`<div style="padding:12px" id="weekRows"></div>`;
    buildWeekInputs(); loadWeekInputs(); syncWeeklyTarget(); recalcWeek(); applyWeekButtons();
  }
  if(tab==="macros"){
    inner.innerHTML=`<div id="macrosInner"></div>`;
    renderMacrosPage();
  }
}'''

NEW_DRAWER_TAB_FN = '''/* tab id map: key used in cpDrawerTab -> actual element id */
const _cpTabIdMap = {
  overview:"cpTabOverview", work:"cpTabWorkouts", weight:"cpTabWeight",
  calc:"cpTabCalc", week:"cpTabWeek", macros:"cpTabMacros", manage:"cpTabManage"
};
function cpDrawerTab(tab){
  Object.keys(_cpTabIdMap).forEach(t=>{
    const el=$(_cpTabIdMap[t]);
    if(el) el.classList.toggle("active", t===tab);
  });
  const body=$("cpDrawerBody"); if(!body) return;
  body.scrollTop=0;
  if(tab==="overview")  { cpDrawerOverview(); return; }
  if(tab==="manage")    { cpDrawerManage();   return; }
  /* render real page content inside drawer */
  body.innerHTML=`<div class="cp-tab-inner" id="cpDrawerInner"></div>`;
  const inner=$("cpDrawerInner");
  if(tab==="work"){
    inner.innerHTML=`<div class="wo-page" id="workContainer"></div><div style="padding:0 12px 8px"><button class="wo-reset-btn hidden" id="workResetBtn" onclick="resetWorkouts()">Reset Workouts</button></div>`;
    renderWorkouts(); applyWorkButtons();
  }
  if(tab==="weight"){
    inner.innerHTML=`<div style="padding:12px" id="weightRows"></div><div style="padding:0 12px 8px"><button class="mini hidden" id="weightResetBtn" onclick="resetWeightData()">Reset</button></div>`;
    loadWeightTracker(); applyWeightButtons();
  }
  if(tab==="calc"){
    inner.innerHTML=`<div class="calc-page" id="calcInputsWrap" style="display:none"></div><div id="cpCalcResults"></div>`;
    loadCalcInputs(); renderCalcMode(); renderCalcResults(); renderSubscriberCalcView();
  }
  if(tab==="week"){
    inner.innerHTML=`<div style="padding:12px" id="weekRows"></div>`;
    buildWeekInputs(); loadWeekInputs(); syncWeeklyTarget(); recalcWeek(); applyWeekButtons();
  }
  if(tab==="macros"){
    inner.innerHTML=`<div id="macrosInner"></div>`;
    renderMacrosPage();
  }
}'''

if OLD_DRAWER_TAB_FN in html:
    html = html.replace(OLD_DRAWER_TAB_FN, NEW_DRAWER_TAB_FN, 1)
    print('cpDrawerTab function replaced OK (tab ID fix applied)')
else:
    print('WARNING: cpDrawerTab function not found')

# ─────────────────────────────────────────────
# 5. IMPROVE cpDrawerOverview – add more stats and better layout
# ─────────────────────────────────────────────
OLD_OVERVIEW = '''function cpDrawerOverview(){
  const body=$("cpDrawerBody"); if(!body) return;
  const sub=findAccById(_cpOpenSubId); if(!sub) return;
  const st=cpSubStatus(sub);
  const now=nowMs();
  const expMs=Number(sub.subExpiresAt||0);
  const startMs=Number(sub.subStartAt||0);
  const daysLeft=expMs?Math.max(0,Math.ceil((expMs-now)/DAY_MS)):0;
  const daysAgo =expMs?Math.max(0,Math.ceil((now-expMs)/DAY_MS)):0;
  const saved=localStorage.getItem("pf_avatar:"+sub.id)||"";
  const statusLabel={active:"Active",expiring:"Expiring",expired:"Expired"};
  const pillCls={active:"green",expiring:"yellow",expired:"red"};
  const avatarHtml=saved
    ? `<div class="cp-sub-info-avatar"><img src="${saved}" alt=""></div>`
    : `<div class="cp-sub-info-avatar"><span class="cp-sub-info-avatar-txt">${cpInitials(sub.name)}</span></div>`;
  /* workouts summary */
  const wo=loadWorkouts?loadWorkouts():{};
  let totalEx=0; Object.values(wo).forEach(exs=>{ if(Array.isArray(exs)) totalEx+=exs.length; });
  /* macros summary */
  let macroInfo="—";
  try{
    const cr=JSON.parse(pget("calc_results")||"null");
    if(cr && cr.tdee) macroInfo=`TDEE: ${cr.tdee} kcal`;
  }catch(e){}
  body.innerHTML=`
    <div class="cp-sub-info-card">
      ${avatarHtml}
      <div class="cp-sub-info-details">
        <div class="cp-sub-info-name">${sub.name}</div>
        <div class="cp-sub-info-pills">
          <span class="cp-sub-info-pill ${pillCls[st]}">${statusLabel[st]}</span>
          <span class="cp-sub-info-pill blue">Subscriber</span>
        </div>
      </div>
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;padding:0 12px 8px">
      <div class="cp-stat" style="min-width:0">
        <div class="cp-stat-val ${pillCls[st]}">${st==="expired"?("-"+daysAgo):daysLeft}</div>
        <div class="cp-stat-lbl">${st==="expired"?"Days Ago":"Days Left"}</div>
      </div>
      <div class="cp-stat" style="min-width:0">
        <div class="cp-stat-val">${totalEx}</div>
        <div class="cp-stat-lbl">Exercises</div>
      </div>
      <div class="cp-stat" style="min-width:0;grid-column:1/-1">
        <div class="cp-stat-val" style="font-size:14px">${macroInfo}</div>
        <div class="cp-stat-lbl">Nutrition</div>
      </div>
    </div>
    <div style="padding:0 12px 12px;display:flex;flex-direction:column;gap:8px">
      <div style="background:linear-gradient(145deg,#0d1829,#111e30);border-radius:16px;padding:14px;border:1px solid rgba(255,255,255,.06)">
        <div style="font-size:10px;font-weight:800;color:#64748b;text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px">Subscription</div>
        <div style="display:flex;justify-content:space-between;font-size:12px;color:#94a3b8;padding:5px 0;border-bottom:1px solid rgba(255,255,255,.05)">
          <span>Start Date</span><span style="color:#e2e8f0;font-weight:700">${fmtDate(startMs)}</span></div>
        <div style="display:flex;justify-content:space-between;font-size:12px;color:#94a3b8;padding:5px 0">
          <span>Expiry Date</span><span style="color:#e2e8f0;font-weight:700">${fmtDate(expMs)}</span></div>
      </div>
    </div>
  `;
}'''

NEW_OVERVIEW = '''function cpDrawerOverview(){
  const body=$("cpDrawerBody"); if(!body) return;
  const sub=findAccById(_cpOpenSubId); if(!sub) return;
  const st=cpSubStatus(sub);
  const now=nowMs();
  const expMs=Number(sub.subExpiresAt||0);
  const startMs=Number(sub.subStartAt||0);
  const daysLeft=expMs?Math.max(0,Math.ceil((expMs-now)/DAY_MS)):0;
  const daysAgo =expMs?Math.max(0,Math.ceil((now-expMs)/DAY_MS)):0;
  const saved=localStorage.getItem("pf_avatar:"+sub.id)||"";
  const statusLabel={active:"Active",expiring:"Expiring",expired:"Expired"};
  const pillCls={active:"green",expiring:"yellow",expired:"red"};
  const pillColors={active:"#22c55e",expiring:"#fbbf24",expired:"#ef4444"};
  const avatarHtml=saved
    ? `<div class="cp-sub-info-avatar"><img src="${saved}" alt=""></div>`
    : `<div class="cp-sub-info-avatar"><span class="cp-sub-info-avatar-txt">${cpInitials(sub.name)}</span></div>`;
  /* workouts summary */
  const wo=loadWorkouts?loadWorkouts():{};
  let totalEx=0, activeDays=0;
  Object.entries(wo).forEach(([k,v])=>{
    if(Array.isArray(v) && v.length){ totalEx+=v.length; activeDays++; }
  });
  /* weight summary */
  let latestWeight="—", weightWeeks=0;
  try{
    for(let i=1;i<=52;i++){
      const w=parseFloat(pget("week_"+i)||"");
      if(!isNaN(w)){ latestWeight=w+"kg"; weightWeeks++; }
    }
  }catch(e){}
  /* macros summary */
  let tdeeVal="—", proteinVal="—";
  try{
    const cr=JSON.parse(pget("calc_results")||"null");
    if(cr && cr.tdee){ tdeeVal=cr.tdee+" kcal"; }
    if(cr && cr.protein){ proteinVal=cr.protein+"g"; }
  }catch(e){}

  /* quick-action buttons */
  const quickBtns=[
    {tab:"work",  icon:`<svg viewBox="0 0 24 24" fill="none" width="20" height="20"><path d="M6 4v16M18 4v16M3 9h18M3 15h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`, label:"Workouts", color:"#38bdf8"},
    {tab:"weight",icon:`<svg viewBox="0 0 24 24" fill="none" width="20" height="20"><path d="M3 6h18M3 12h18M3 18h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`, label:"Weight", color:"#34d399"},
    {tab:"calc",  icon:`<svg viewBox="0 0 24 24" fill="none" width="20" height="20"><rect x="4" y="2" width="16" height="20" rx="2" stroke="currentColor" stroke-width="2"/><path d="M8 7h8M8 12h4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`, label:"Calc", color:"#a78bfa"},
    {tab:"week",  icon:`<svg viewBox="0 0 24 24" fill="none" width="20" height="20"><rect x="3" y="4" width="18" height="18" rx="2" stroke="currentColor" stroke-width="2"/><path d="M16 2v4M8 2v4M3 10h18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`, label:"Weekly", color:"#fb923c"},
    {tab:"macros",icon:`<svg viewBox="0 0 24 24" fill="none" width="20" height="20"><circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2"/><path d="M12 8v8M8 12h8" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`, label:"Macros", color:"#f472b6"},
    {tab:"manage",icon:`<svg viewBox="0 0 24 24" fill="none" width="20" height="20"><circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/><path d="M12 2v3M12 19v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>`, label:"Manage", color:"#94a3b8"},
  ].map(b=>`<button onclick="cpDrawerTab('${b.tab}')" style="background:linear-gradient(145deg,#09162a,#0d1e34);border:1.5px solid rgba(255,255,255,.07);border-radius:16px;padding:14px 8px;cursor:pointer;display:flex;flex-direction:column;align-items:center;gap:8px;transition:all .22s;-webkit-tap-highlight-color:transparent;color:${b.color}" onmouseover="this.style.transform='translateY(-2px) scale(1.04)';this.style.borderColor='${b.color}40'" onmouseout="this.style.transform='';this.style.borderColor='rgba(255,255,255,.07)'">`
    +`<span style="width:40px;height:40px;border-radius:12px;background:${b.color}18;display:flex;align-items:center;justify-content:center;border:1px solid ${b.color}30">${b.icon}</span>`
    +`<span style="font-size:10px;font-weight:800;color:#94a3b8;letter-spacing:.02em">${b.label}</span>`
    +`</button>`).join("");

  body.innerHTML=`
    <div class="cp-sub-info-card">
      ${avatarHtml}
      <div class="cp-sub-info-details">
        <div class="cp-sub-info-name">${sub.name}</div>
        <div class="cp-sub-info-pills">
          <span class="cp-sub-info-pill ${pillCls[st]}">${statusLabel[st]}</span>
          <span class="cp-sub-info-pill blue">Subscriber</span>
        </div>
      </div>
    </div>

    <!-- Quick actions grid -->
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;padding:10px 12px 4px">${quickBtns}</div>

    <!-- Stats row -->
    <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:8px;padding:8px 12px 4px">
      <div class="cp-stat" style="min-width:0">
        <div class="cp-stat-val ${pillCls[st]}">${st==="expired"?daysAgo:daysLeft}</div>
        <div class="cp-stat-lbl">${st==="expired"?"Days Ago":"Days Left"}</div>
      </div>
      <div class="cp-stat" style="min-width:0">
        <div class="cp-stat-val">${totalEx}</div>
        <div class="cp-stat-lbl">Exercises</div>
      </div>
      <div class="cp-stat" style="min-width:0">
        <div class="cp-stat-val" style="font-size:16px">${latestWeight}</div>
        <div class="cp-stat-lbl">Weight</div>
      </div>
    </div>

    <!-- Info cards -->
    <div style="padding:4px 12px 12px;display:flex;flex-direction:column;gap:8px">
      <!-- Subscription card -->
      <div style="background:linear-gradient(145deg,#08142a,#0c1e38);border-radius:18px;padding:16px;border:1.5px solid rgba(255,255,255,.07)">
        <div style="font-size:10px;font-weight:800;color:#3d5068;text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px">📅 Subscription</div>
        <div style="display:flex;justify-content:space-between;align-items:center;font-size:12px;color:#64748b;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05)">
          <span>Status</span>
          <span style="color:${pillColors[st]};font-weight:800;background:${pillColors[st]}18;padding:3px 10px;border-radius:12px">${statusLabel[st]}</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05)">
          <span>Start</span><span style="color:#e2e8f0;font-weight:700">${fmtDate(startMs)}</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;padding:6px 0">
          <span>Expires</span><span style="color:#e2e8f0;font-weight:700">${fmtDate(expMs)}</span>
        </div>
      </div>
      <!-- Nutrition card -->
      <div style="background:linear-gradient(145deg,#08142a,#0c1e38);border-radius:18px;padding:16px;border:1.5px solid rgba(255,255,255,.07)">
        <div style="font-size:10px;font-weight:800;color:#3d5068;text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px">🥗 Nutrition</div>
        <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05)">
          <span>TDEE</span><span style="color:#e2e8f0;font-weight:700">${tdeeVal}</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;padding:6px 0">
          <span>Protein target</span><span style="color:#e2e8f0;font-weight:700">${proteinVal}</span>
        </div>
      </div>
      <!-- Training card -->
      <div style="background:linear-gradient(145deg,#08142a,#0c1e38);border-radius:18px;padding:16px;border:1.5px solid rgba(255,255,255,.07)">
        <div style="font-size:10px;font-weight:800;color:#3d5068;text-transform:uppercase;letter-spacing:.06em;margin-bottom:10px">💪 Training</div>
        <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05)">
          <span>Total exercises</span><span style="color:#e2e8f0;font-weight:700">${totalEx}</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;padding:6px 0;border-bottom:1px solid rgba(255,255,255,.05)">
          <span>Active training days</span><span style="color:#e2e8f0;font-weight:700">${activeDays}</span>
        </div>
        <div style="display:flex;justify-content:space-between;font-size:12px;color:#64748b;padding:6px 0">
          <span>Weight entries</span><span style="color:#e2e8f0;font-weight:700">${weightWeeks} weeks</span>
        </div>
      </div>
    </div>
  `;
}'''

if OLD_OVERVIEW in html:
    html = html.replace(OLD_OVERVIEW, NEW_OVERVIEW, 1)
    print('cpDrawerOverview replaced OK')
else:
    print('WARNING: cpDrawerOverview not found')

# ─────────────────────────────────────────────
# 6. Add .cp-tab-inner CSS (needed for the new tab wrapper)
# ─────────────────────────────────────────────
TAB_INNER_CSS = '''
  .cp-tab-inner{ animation:cp-rise .3s cubic-bezier(.22,1,.36,1) both; }
'''
if '.cp-tab-inner' not in html:
    # Insert after .cp-drawer-body .page style
    marker = '  .cp-drawer-body .page{ display:block !important; padding-bottom:24px; }'
    if marker in html:
        html = html.replace(marker, marker + TAB_INNER_CSS, 1)
        print('cp-tab-inner CSS added OK')
    else:
        print('WARNING: could not find cp-drawer-body marker for tab-inner CSS')

# ─────────────────────────────────────────────
# 7. Improve the subscriber card HTML: add last activity line
# ─────────────────────────────────────────────
OLD_CARD_HTML = '''    card.innerHTML=`
      ${avatarHtml}
      <div class="cp-card-name">${sub.name}</div>
      <div class="cp-card-days ${st}">${daysLabel}</div>
    `;'''

NEW_CARD_HTML = '''    card.innerHTML=`
      ${avatarHtml}
      <div class="cp-card-name">${sub.name}</div>
      <div class="cp-card-days ${st}">${daysLabel}</div>
    `;'''

# (Keep card HTML the same but improve the card with extra info in JS)
# Instead, enhance the card render to add an exercise count badge
OLD_CARD_BUILD = '''    const daysLabel=cpSubDaysLabel(sub);
    card.innerHTML=`
      ${avatarHtml}
      <div class="cp-card-name">${sub.name}</div>
      <div class="cp-card-days ${st}">${daysLabel}</div>
    `;
    card.onclick=()=>cpOpenSubscriber(sub.id);'''

NEW_CARD_BUILD = '''    const daysLabel=cpSubDaysLabel(sub);
    /* get subscriber exercise count */
    const _prevManaged=getManagedId();
    setManagedId(sub.id);
    let subExCount=0;
    try{
      const wo=loadWorkouts?loadWorkouts():{};
      Object.values(wo).forEach(v=>{ if(Array.isArray(v)) subExCount+=v.length; });
    }catch(e){}
    setManagedId(_prevManaged);
    const exBadge=subExCount>0?`<div style="position:absolute;top:8px;right:8px;background:rgba(56,189,248,.15);border:1px solid rgba(56,189,248,.25);border-radius:8px;padding:2px 6px;font-size:9px;font-weight:800;color:#38bdf8">${subExCount}</div>`:"";
    card.innerHTML=`
      ${exBadge}
      ${avatarHtml}
      <div class="cp-card-name">${sub.name}</div>
      <div class="cp-card-days ${st}">${daysLabel}</div>
    `;
    card.onclick=()=>cpOpenSubscriber(sub.id);'''

if OLD_CARD_BUILD in html:
    html = html.replace(OLD_CARD_BUILD, NEW_CARD_BUILD, 1)
    print('Card build enhanced with exercise count OK')
else:
    print('WARNING: card build block not found')

# ─────────────────────────────────────────────
# 8. Improve the coach panel HTML header with better icon
# ─────────────────────────────────────────────
OLD_CP_HTML_HEADER = '''  <!-- Header -->
  <div class="cp-header">
    <div class="cp-header-left">
      <div class="cp-header-title">My Subscribers</div>
      <div class="cp-header-sub" id="cpHeaderSub">Loading...</div>
    </div>
    <div class="cp-header-icon">&#x1F3CB;&#xFE0F;</div>
  </div>'''

NEW_CP_HTML_HEADER = '''  <!-- Header -->
  <div class="cp-header">
    <div class="cp-header-left">
      <div class="cp-header-title">My Subscribers</div>
      <div class="cp-header-sub" id="cpHeaderSub">Loading...</div>
    </div>
    <div class="cp-header-icon">
      <svg viewBox="0 0 24 24" fill="none" width="28" height="28">
        <circle cx="9" cy="7" r="3" stroke="#38bdf8" stroke-width="2"/>
        <path d="M3 20c0-3.3 2.7-6 6-6" stroke="#38bdf8" stroke-width="2" stroke-linecap="round"/>
        <circle cx="17" cy="9" r="2.5" stroke="#818cf8" stroke-width="2"/>
        <path d="M14 20c0-2.8 2-5 5-5" stroke="#818cf8" stroke-width="2" stroke-linecap="round"/>
        <path d="M21 20h-4" stroke="#818cf8" stroke-width="2" stroke-linecap="round"/>
      </svg>
    </div>
  </div>'''

if OLD_CP_HTML_HEADER in html:
    html = html.replace(OLD_CP_HTML_HEADER, NEW_CP_HTML_HEADER, 1)
    print('Coach panel header HTML updated OK')
else:
    print('WARNING: coach panel header HTML not found')

# ─────────────────────────────────────────────
# 9. Improve the "New Subscriber" add card icon
# ─────────────────────────────────────────────
OLD_ADD_CARD_INNER = '''    addCard.innerHTML=`<div class="cp-add-card-icon">+</div><div class="cp-add-card-lbl">New Subscriber</div>`;'''

NEW_ADD_CARD_INNER = '''    addCard.innerHTML=`<div class="cp-add-card-icon"><svg viewBox="0 0 24 24" fill="none" width="20" height="20"><circle cx="12" cy="8" r="3.5" stroke="currentColor" stroke-width="2"/><path d="M5 20c0-3.9 3.1-7 7-7s7 3.1 7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><path d="M19 3v6M16 6h6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg></div><div class="cp-add-card-lbl">New Subscriber</div>`;'''

if OLD_ADD_CARD_INNER in html:
    html = html.replace(OLD_ADD_CARD_INNER, NEW_ADD_CARD_INNER, 1)
    print('Add card icon updated OK')
else:
    print('WARNING: add card icon not found')

# ─────────────────────────────────────────────
# Write output
# ─────────────────────────────────────────────
with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

new_len = len(html)
with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()
print(f'Done. {original_len} chars -> {new_len} chars, {len(lines)} lines')
