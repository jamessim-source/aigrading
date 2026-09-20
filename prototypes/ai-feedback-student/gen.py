# Generates the AI Feedback student prototype: 8 PC + 8 mobile screens × 2 languages (JA / EN).
# Two outputs from the same builders:
#   project/   — .dc.html artboards + canvas.json for the Claude Design canvas
#   deploy/public/ — standalone pages for the Railway static site (see deploy/README.md)
# Design language: Manabie "(Final) Learner app" Figma — Noto Sans JP, #f2f2f4 ground, white paper,
# primary #395ad2 / light #eef1ff, text rgba(28,30,44,.87/.6), border rgba(28,30,44,.12),
# 8px cards with 0 8px 16px rgba(0,0,0,.1), pill buttons, 72px header with 40px bordered icon button.
import json, os, re, datetime

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "project")
SITE = os.path.join(HERE, "deploy", "public")
os.makedirs(ROOT, exist_ok=True)
os.makedirs(SITE, exist_ok=True)
W, H, GAP = 1280, 800, 80

# ---------- icons (inline stroke SVG, 24 viewBox) ----------
def ic(name, size=20, color="currentColor", sw=2):
    paths = {
        "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
        "bell": '<path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/><path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>',
        "down": '<path d="m6 9 6 6 6-6"/>',
        "right": '<path d="m9 6 6 6-6 6"/>',
        "back": '<path d="M19 12H5m7-7-7 7 7 7"/>',
        "book": '<path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/>',
        "sparkle": '<path d="M12 3l1.9 5.1L19 10l-5.1 1.9L12 17l-1.9-5.1L5 10l5.1-1.9L12 3z"/><path d="M19 17l.7 1.8 1.8.7-1.8.7L19 22l-.7-1.8-1.8-.7 1.8-.7L19 17z"/>',
        "upload": '<path d="M12 16V4m0 0-4 4m4-4 4 4"/><path d="M4 16v3a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-3"/>',
        "download": '<path d="M12 4v12m0 0-4-4m4 4 4-4"/><path d="M4 16v3a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-3"/>',
        "file": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/>',
        "filetext": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M8 13h8M8 17h8"/>',
        "table": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 10h18M3 15h18M9 4v16M15 4v16"/>',
        "play": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="m10 9 5 3-5 3z"/>',
        "check": '<path d="m5 12 5 5L20 7"/>',
        "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
        "message": '<path d="M21 12a8 8 0 0 1-8 8H5l-2 2V12a8 8 0 0 1 8-8h2a8 8 0 0 1 8 8z"/>',
        "scan": '<path d="M4 8V6a2 2 0 0 1 2-2h2M16 4h2a2 2 0 0 1 2 2v2M20 16v2a2 2 0 0 1-2 2h-2M8 20H6a2 2 0 0 1-2-2v-2"/><circle cx="12" cy="12" r="3"/>',
        "x": '<path d="M18 6 6 18M6 6l12 12"/>',
        "person": '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
        "lock": '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
        "eye": '<path d="M2 12s4-7 10-7 10 7 10 7-4 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/>',
        "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3a14 14 0 0 1 0 18M12 3a14 14 0 0 0 0 18"/>',
        "alert": '<path d="M12 9v4m0 4h.01"/><path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/>',
        "minus": '<path d="M5 12h14"/>',
        "refresh": '<path d="M21 12a9 9 0 1 1-2.6-6.4"/><path d="M21 3v6h-6"/>',
        "camera": '<path d="M3 8a2 2 0 0 1 2-2h2l2-3h6l2 3h2a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"/><circle cx="12" cy="13" r="4"/>',
        "monitor": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
        "phone": '<rect x="7" y="2" width="10" height="20" rx="2"/><path d="M11 18h2"/>',
        "left": '<path d="m15 6-6 6 6 6"/>',
        "plus": '<path d="M12 5v14M5 12h14"/>',
        "flash": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
        "rotate": '<path d="M3 12a9 9 0 1 0 2.6-6.4"/><path d="M3 3v6h6"/>',
        "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
        "grip": '<circle cx="9" cy="6" r="1.2"/><circle cx="15" cy="6" r="1.2"/><circle cx="9" cy="12" r="1.2"/><circle cx="15" cy="12" r="1.2"/><circle cx="9" cy="18" r="1.2"/><circle cx="15" cy="18" r="1.2"/>',
        "image": '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="8.5" cy="9.5" r="1.5"/><path d="m21 16-5-5-9 9"/>',
        "grid": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
        "trash": '<path d="M4 7h16M10 11v6M14 11v6"/><path d="M6 7l1 13a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1l1-13M9 7V4h6v3"/>',
        "pencil": '<path d="M4 20h4L20 8a2.8 2.8 0 0 0-4-4L4 16z"/><path d="M14 6l4 4"/>',
    }[name]
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
            f'style="flex-shrink:0;display:block">{paths}</svg>')

# ---------- shared CSS ----------
CSS = """
body{margin:0;background:#f2f2f4;font-family:'Noto Sans JP',system-ui,sans-serif;color:rgba(28,30,44,.87);-webkit-font-smoothing:antialiased}
a{color:#395ad2;text-decoration:none}a:hover{color:#2c48ae}
*{box-sizing:border-box}
.root{width:1280px;height:800px;display:flex;flex-direction:column;overflow:hidden;background:#f2f2f4;position:relative}
.hdr{height:72px;flex:0 0 72px;background:#fff;border-bottom:1px solid rgba(28,30,44,.12);display:flex;align-items:center;justify-content:space-between;padding:16px 24px;gap:16px}
.hdr-l{display:flex;align-items:center;gap:20px;min-width:0;flex:1 1 auto}
.ibtn{width:40px;height:40px;border:1px solid rgba(28,30,44,.12);border-radius:4px;background:#fff;display:flex;align-items:center;justify-content:center;color:#404564;cursor:pointer;padding:0;flex:0 0 40px}
.ibtn:hover{background:#f2f2f4;color:#404564}
.h4{font-size:18px;line-height:24px;font-weight:500;margin:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.crumb{font-size:12px;line-height:16px;color:rgba(28,30,44,.6);margin:0 0 2px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.hdr-r{display:flex;align-items:center;gap:20px;flex:0 0 auto}
.seg{display:inline-flex;align-items:center;border:1px solid rgba(28,30,44,.12);border-radius:1000px;padding:3px;background:#fff;height:34px;gap:2px}
.seg-i{display:inline-flex;align-items:center;gap:6px;height:26px;padding:0 12px;border-radius:1000px;font-size:12px;line-height:16px;font-weight:700;color:rgba(28,30,44,.6);white-space:nowrap}
a.seg-i:hover{color:#395ad2;background:#f2f2f4}
.seg-i.on{background:#eef1ff;color:#395ad2}
button.seg-i{border:0;background:none;cursor:pointer;font-family:inherit;height:28px;padding:0 14px;font-size:13px}
button.seg-i:hover{color:#395ad2;background:#f2f2f4}
button.seg-i.on{background:#eef1ff;color:#395ad2}
.ta{width:100%;min-height:180px;resize:vertical;border:1px solid rgba(28,30,44,.2);border-radius:8px;padding:12px 14px;font:inherit;font-size:14px;line-height:22px;color:rgba(28,30,44,.87);background:#fff;outline:none}
.ta:focus{border-color:#395ad2;box-shadow:0 0 0 3px rgba(57,90,210,.15)}
.ta::placeholder{color:rgba(28,30,44,.38)}
.bell{position:relative;width:40px;height:40px;display:flex;align-items:center;justify-content:center;color:#404564;background:none;border:0;padding:0;cursor:pointer}
.bell .n{position:absolute;top:4px;left:20px;background:#d13842;color:#fff;border:1px solid #fff;border-radius:4px;font-size:10px;line-height:14px;padding:0 5px;font-weight:500}
.acct{display:flex;align-items:center;gap:8px;font-size:14px;line-height:18px;background:none;border:0;padding:0;cursor:pointer;color:rgba(28,30,44,.87);font-family:inherit;white-space:nowrap}
.av{width:36px;height:36px;border-radius:50%;background:#e4e8ff;border:1px solid rgba(28,30,44,.12);display:flex;align-items:center;justify-content:center;color:#395ad2}
.body{flex:1 1 auto;overflow:auto;padding:24px}
.col{width:880px;margin:0 auto;display:flex;flex-direction:column;gap:16px}
.card{background:#fff;border-radius:8px;box-shadow:0 8px 16px rgba(0,0,0,.1);padding:16px}
.h3{font-size:24px;line-height:36px;font-weight:700;margin:0}
.sub1{font-size:16px;line-height:24px;font-weight:700;margin:0}
.b1{font-size:16px;line-height:24px;margin:0}
.b2{font-size:14px;line-height:18px;margin:0}
.cap{font-size:12px;line-height:16px;margin:0;color:rgba(28,30,44,.6)}
.muted{color:rgba(28,30,44,.6)}
.row{display:flex;align-items:center;gap:16px}
.tile{width:56px;height:56px;border-radius:50%;background:#eef1ff;display:flex;align-items:center;justify-content:center;color:#395ad2;flex:0 0 56px;position:relative}
.tile.done{background:#f0f0f3;color:#8e939b}
.tile .sp{position:absolute;right:-2px;top:-2px;width:22px;height:22px;border-radius:50%;background:#ffc20a;display:flex;align-items:center;justify-content:center;color:#1c1e2c;border:2px solid #fff}
.lo{display:flex;align-items:center;gap:16px;background:#fff;border-radius:8px;box-shadow:0 8px 16px rgba(0,0,0,.1);padding:16px;color:inherit;text-align:left;width:100%;border:0;font-family:inherit;cursor:pointer}
.lo:hover{color:inherit;background:#fafafc}
.lo.off{opacity:.55;cursor:default;box-shadow:none;border:1px solid rgba(28,30,44,.12)}
.lo .t{flex:1 1 auto;min-width:0;display:flex;flex-direction:column;gap:6px}
.lo .t b{font-size:16px;line-height:24px;font-weight:700;display:block}
.lo .t i{font-style:normal;font-size:14px;line-height:18px;color:rgba(28,30,44,.6);display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.chip{display:inline-flex;align-items:center;gap:6px;height:24px;padding:0 10px;border-radius:360px;font-size:12px;line-height:16px;font-weight:700;white-space:nowrap}
.chip.wait{background:#fff3cc;color:#7a5a00}
.chip.review{background:#eef1ff;color:#395ad2}
.chip.done{background:#e6f5ee;color:#1f7a4d}
.chip.late{background:#fbe7e9;color:#d13842}
.chip.pre{background:#ececef;color:rgba(28,30,44,.6)}
.chip.neutral{background:#f2f2f4;color:rgba(28,30,44,.87);font-weight:500}
.chip.lt{background:#f2f2f4;color:rgba(28,30,44,.6);font-weight:700;height:22px;font-size:11px}
.chip.lt.fb{background:#fff3cc;color:#1c1e2c}
.topic{display:flex;align-items:center;gap:8px;margin:4px 0 -6px 4px;font-size:14px;line-height:18px;font-weight:700;color:rgba(28,30,44,.6)}
.topic::before{content:"";width:3px;height:14px;border-radius:2px;background:#395ad2;opacity:.5}
.chip.pick{height:32px;padding:0 14px;background:#fff;border:1px solid rgba(28,30,44,.2);color:rgba(28,30,44,.87);cursor:pointer;font-family:inherit;font-weight:500}
.chip.pick:hover{background:#f2f2f4}
.chip.pick.sel{background:#eef1ff;border-color:#395ad2;color:#395ad2;font-weight:700}
.btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:44px;padding:0 24px;border-radius:1000px;font-size:14px;line-height:18px;font-weight:700;border:0;cursor:pointer;font-family:inherit;white-space:nowrap}
.btn.primary{background:#395ad2;color:#fff}.btn.primary:hover{background:#2c48ae;color:#fff}
.btn.neutral{background:#fff;color:rgba(28,30,44,.87);border:1px solid rgba(28,30,44,.12)}.btn.neutral:hover{background:#f2f2f4;color:rgba(28,30,44,.87)}
.btn.ghost{background:none;color:#395ad2;padding:0 12px}.btn.ghost:hover{background:#eef1ff}
.btn.dis{background:rgba(28,30,44,.12);color:rgba(28,30,44,.38);cursor:default}
.divider{height:1px;background:rgba(28,30,44,.12);margin:4px 0}
.steps{display:flex;align-items:flex-start;gap:0}
.step{flex:1 1 0;display:flex;flex-direction:column;align-items:center;gap:8px;position:relative;text-align:center;padding:0 8px}
.step .dot{width:32px;height:32px;border-radius:50%;background:#fff;border:2px solid rgba(28,30,44,.24);display:flex;align-items:center;justify-content:center;color:rgba(28,30,44,.6);font-weight:700;font-size:14px;z-index:1}
.step.done .dot{background:#395ad2;border-color:#395ad2;color:#fff}
.step.cur .dot{border-color:#395ad2;color:#395ad2;box-shadow:0 0 0 6px #eef1ff}
.step .l{font-size:14px;line-height:18px;font-weight:700}
.step .s{font-size:12px;line-height:16px;color:rgba(28,30,44,.6)}
.step .line{position:absolute;top:15px;left:50%;width:100%;height:2px;background:rgba(28,30,44,.16)}
.step.done .line{background:#395ad2}
.step:last-child .line{display:none}
.crit{display:flex;flex-wrap:wrap;gap:8px}
.drop{border:2px dashed rgba(57,90,210,.45);background:#fafbff;border-radius:8px;padding:28px;display:flex;flex-direction:column;align-items:center;gap:12px;text-align:center}
.filerow{display:flex;align-items:center;gap:12px;border:1px solid rgba(28,30,44,.12);border-radius:8px;padding:12px 16px;background:#fff}
.filerow .ficon{width:40px;height:40px;border-radius:8px;background:#fbe7e9;color:#d13842;display:flex;align-items:center;justify-content:center;flex:0 0 40px}
.shot{position:relative;display:block;border-radius:6px;overflow:hidden;border:1px solid rgba(28,30,44,.12);background:#f2f2f4}
/* on the phone the thumbnails keep the first line and the detail wraps under them */
.mroot .shots{flex-wrap:wrap}
.mroot .shots .shots-txt{order:3;flex:1 1 100%}
.mroot .shots .ibtn{order:2;margin-left:auto}
.shot i{position:absolute;left:2px;top:2px;z-index:1;background:#395ad2;color:#fff;font-size:10px;font-weight:700;font-style:normal;border-radius:4px;padding:0 5px;line-height:15px}
.fb-card{background:#fff;border-radius:8px;border:1px solid rgba(28,30,44,.12);padding:16px;position:relative;display:flex;flex-direction:column;gap:10px}
.fb-card.next{background:#fffbea;border-color:#f2dc8f}
.badge{display:inline-flex;align-items:center;gap:7px;height:26px;padding:0 11px;border-radius:8px;font-size:13px;font-weight:700;align-self:flex-start}
.badge.sum{background:#1c1e2c;color:#fff}
.badge.good{background:#e6f5ee;color:#1f7a4d}
.badge.ask{background:#eef1ff;color:#395ad2}
.badge.todo{background:#fbe7e9;color:#d13842}
.badge.next{background:#ffc20a;color:#1c1e2c}
.badge .n{width:18px;height:18px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-size:11px;color:#fff;font-style:normal}
.badge.good .n{background:#1f7a4d}.badge.ask .n{background:#395ad2}.badge.todo .n{background:#d13842}
.ctag{display:inline-flex;align-items:center;height:22px;padding:0 8px;border-radius:6px;background:#f2f2f4;color:rgba(28,30,44,.6);font-size:12px;font-weight:700;white-space:nowrap}
.quote{margin:0;padding:2px 0 2px 12px;border-left:3px solid #d5d7dd;font-size:14px;line-height:22px;color:rgba(28,30,44,.6)}
.quote.good{border-left-color:#9ddcbb}.quote.ask{border-left-color:#aeb9ea}.quote.todo{border-left-color:#f3b4b8}
.fbody{margin:0;font-size:15px;line-height:1.85;white-space:pre-wrap}
.ref{display:inline-flex;align-items:center;gap:6px;font-size:12px;line-height:16px;color:#395ad2;background:#eef1ff;border-radius:6px;padding:4px 8px;align-self:flex-start}
.jump{position:absolute;right:10px;top:12px;width:32px;height:32px;border-radius:8px;border:0;background:none;color:#395ad2;display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0}
.jump:hover{background:#eef1ff}
.raw{font-size:15px;line-height:2;margin:0 0 16px}
.fbm{display:inline;font:inherit;line-height:inherit;text-align:left;border:0;cursor:pointer;background:none;color:inherit;border-radius:4px;padding:1px 2px;box-shadow:inset 0 -2px 0 #9ddcbb;transition:background .2s}
.fbm:hover{background:#f2f2f4}
.fb-card.hit{border-color:#395ad2;box-shadow:0 0 0 3px #eef1ff}
.fbm.ask{box-shadow:inset 0 -2px 0 #aeb9ea}.fbm.todo{box-shadow:inset 0 -2px 0 #f3b4b8}
.fbm .n{display:inline-flex;width:18px;height:18px;border-radius:50%;background:#1f7a4d;color:#fff;font-size:11px;font-style:normal;align-items:center;justify-content:center;vertical-align:middle;margin:-2px 4px 0 0}
.fbm.ask .n{background:#395ad2}.fbm.todo .n{background:#d13842}
.fbm.hit{background:#e6f5ee}.fbm.ask.hit{background:#eef1ff}.fbm.todo.hit{background:#fbe7e9}
.pane{background:#fff;border-radius:8px;box-shadow:0 8px 16px rgba(0,0,0,.1);display:flex;flex-direction:column;min-height:0;overflow:hidden}
.pane-h{padding:12px 20px;border-bottom:1px solid rgba(28,30,44,.12);display:flex;align-items:center;justify-content:space-between;gap:12px;flex:0 0 auto}
.pane-b{padding:20px 24px;overflow:auto;flex:1 1 auto}
.demo{position:absolute;right:20px;bottom:20px;display:inline-flex;align-items:center;gap:10px;background:#1c1e2c;color:#fff;border-radius:1000px;padding:8px 8px 8px 14px;font-size:12px;font-weight:700;box-shadow:0 8px 16px rgba(0,0,0,.25);z-index:5}
.demo:hover{color:#fff;background:#2b2e42}
.demo .tag{background:#ffc20a;color:#1c1e2c;border-radius:1000px;padding:2px 8px;font-size:10px;letter-spacing:.06em}
.tav{width:40px;height:40px;border-radius:50%;background:#dfe4ff;color:#395ad2;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:14px;flex:0 0 40px}
.chk{display:flex;gap:12px;align-items:flex-start;padding:10px 0;border-bottom:1px solid rgba(28,30,44,.08);width:100%;background:none;border-left:0;border-right:0;border-top:0;text-align:left;font-family:inherit;color:inherit;cursor:pointer}
.chk:last-child{border-bottom:0}
.chk .box{width:22px;height:22px;border-radius:6px;border:2px solid rgba(28,30,44,.24);display:flex;align-items:center;justify-content:center;flex:0 0 22px;color:#fff;margin-top:1px}
.chk.on .box{background:#1f7a4d;border-color:#1f7a4d}
.chk .tt{display:flex;flex-direction:column;gap:2px;min-width:0;flex:1 1 auto}
.chk .tt b{font-size:14px;line-height:20px}
.chk.on .tt b{text-decoration:line-through;color:rgba(28,30,44,.6)}
.pc{display:flex;gap:10px;align-items:flex-start;padding:8px 0}
.pc .st{width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:0 0 22px;margin-top:1px}
.pc.ok .st{background:#e6f5ee;color:#1f7a4d}.pc.warn .st{background:#fff3cc;color:#7a5a00}.pc.pend .st{background:#ececef;color:rgba(28,30,44,.5)}
.pc .tt{font-size:14px;line-height:22px}
.pc.warn .tt b{color:#7a5a00}
.chg{display:flex;gap:10px;align-items:center;font-size:14px;line-height:22px}
.chg .st{width:22px;height:22px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:0 0 22px}
.chg.done .st{background:#e6f5ee;color:#1f7a4d}.chg.new .st{background:#fbe7e9;color:#d13842}
.kv{display:flex;align-items:center;gap:8px;font-size:13px;line-height:18px;color:rgba(28,30,44,.6);flex-wrap:wrap}
.kv b{color:rgba(28,30,44,.87);font-weight:500}
.inp{border:1px solid rgba(28,30,44,.2);border-radius:8px;padding:10px 12px;font-size:14px;line-height:20px;color:rgba(28,30,44,.45);background:#fff}
/* prototype-only PC / Mobile switch, bottom-left */
.dev{position:absolute;left:20px;bottom:20px;display:inline-flex;align-items:center;gap:2px;background:#1c1e2c;border-radius:1000px;padding:4px;z-index:60;box-shadow:0 8px 16px rgba(0,0,0,.25)}
.dev-i{display:inline-flex;align-items:center;gap:6px;height:26px;padding:0 12px;border-radius:1000px;font-size:12px;line-height:16px;font-weight:700;color:rgba(255,255,255,.72);white-space:nowrap}
a.dev-i:hover{color:#fff;background:rgba(255,255,255,.12)}
.dev-i.on{background:#fff;color:#1c1e2c}
.dev.m{left:12px;bottom:14px}
.dev.m .dev-i:not(.on) .dl{display:none}
.dev.m .dev-i:not(.on){padding:0 9px}
.dev.m.nav{bottom:70px}
/* ---------- mobile (375 x 812, Figma [Mobile-View]) ---------- */
.mroot{width:375px;height:812px;display:flex;flex-direction:column;overflow:hidden;background:#f2f2f4;position:relative}
.mroot.dark{background:#000;color:#fff}
.sb{height:44px;flex:0 0 44px;display:flex;align-items:center;justify-content:space-between;padding:0 14px 0 21px;font-size:15px;font-weight:600;letter-spacing:-.17px;position:relative;z-index:20}
.sb .si{display:flex;align-items:center;gap:5px}
.mhdr{height:64px;flex:0 0 64px;background:#fff;border-bottom:1px solid rgba(28,30,44,.12);display:flex;align-items:center;gap:8px;padding:8px 16px;position:relative;z-index:20}
.mhdr .mib{width:40px;height:40px;display:flex;align-items:center;justify-content:center;color:#404564;background:none;border:0;padding:0;flex:0 0 40px;cursor:pointer}
.mhdr .mt{flex:1 1 auto;min-width:0;font-size:20px;line-height:28px;font-weight:700;margin:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mhdr .mt.h2{font-size:28px;line-height:40px}
.mhdr .mav{width:36px;height:36px;border-radius:50%;background:#e4e8ff;border:1px solid rgba(28,30,44,.12);display:flex;align-items:center;justify-content:center;color:#395ad2;flex:0 0 36px}
.mseg{display:inline-flex;align-items:center;border:1px solid rgba(28,30,44,.12);border-radius:1000px;padding:2px;background:#fff;height:30px;gap:1px;flex:0 0 auto}
.mseg .seg-i{height:24px;padding:0 9px;font-size:11px}
.mbody{flex:1 1 auto;overflow:auto;padding:16px 16px 64px;display:flex;flex-direction:column;gap:16px}
.mbody.nav{padding-bottom:124px}
.mnav{position:absolute;left:0;right:0;bottom:0;height:58px;background:#fff;box-shadow:0 -5px 20px rgba(0,0,0,.05);display:flex;align-items:flex-start;padding-top:8px;z-index:20}
.mnav .ni{flex:1 1 0;display:flex;flex-direction:column;align-items:center;gap:2px;font-size:10px;line-height:12px;color:rgba(28,30,44,.48)}
.mnav .ni.on{color:#395ad2}
.banner{background:#395ad2;color:#fff;border-radius:8px;padding:8px 16px;display:flex;flex-direction:column;align-items:center;gap:4px;text-align:center}
.banner b{font-size:24px;line-height:36px;font-weight:700}
.banner span{font-size:12px;line-height:16px}
.mcard{background:#fff;border-radius:8px;box-shadow:0 8px 16px rgba(0,0,0,.1);padding:16px;display:flex;flex-direction:column;gap:12px}
.mh{font-size:18px;line-height:26px;font-weight:700;margin:0}
.opt{display:flex;align-items:center;gap:14px;padding:12px;border:1px solid rgba(28,30,44,.12);border-radius:8px;background:#fff;color:inherit;text-align:left;font-family:inherit;cursor:pointer;width:100%}
.opt:hover{background:#fafafc;color:inherit}
.opt.pri{border-color:#395ad2;background:#f7f8ff}
.opt .oi{width:48px;height:48px;border-radius:50%;background:#eef1ff;color:#395ad2;display:flex;align-items:center;justify-content:center;flex:0 0 48px}
.opt.pri .oi{background:#395ad2;color:#fff}
.opt .ot{flex:1 1 auto;min-width:0;display:flex;flex-direction:column;gap:2px}
.opt .ot b{font-size:15px;line-height:22px}
.opt .ot span{font-size:12px;line-height:16px;color:rgba(28,30,44,.6)}
.mbtn{display:flex;align-items:center;justify-content:center;gap:8px;height:48px;border-radius:1000px;font-size:15px;font-weight:700;border:0;cursor:pointer;font-family:inherit;width:100%;white-space:nowrap}
.mbtn.primary{background:#395ad2;color:#fff}.mbtn.primary:hover{background:#2c48ae;color:#fff}
.mbtn.neutral{background:#fff;color:rgba(28,30,44,.87);border:1px solid rgba(28,30,44,.12)}
.mbtn.dis{background:rgba(28,30,44,.12);color:rgba(28,30,44,.38);cursor:default}
.vsteps{display:flex;flex-direction:column}
.vstep{display:flex;gap:12px;align-items:flex-start;position:relative;padding-bottom:18px}
.vstep:last-child{padding-bottom:0}
.vstep .dot{width:28px;height:28px;border-radius:50%;background:#fff;border:2px solid rgba(28,30,44,.24);display:flex;align-items:center;justify-content:center;color:rgba(28,30,44,.6);font-weight:700;font-size:13px;flex:0 0 28px;z-index:1}
.vstep.done .dot{background:#395ad2;border-color:#395ad2;color:#fff}
.vstep.cur .dot{border-color:#395ad2;color:#395ad2;box-shadow:0 0 0 5px #eef1ff}
.vstep .line{position:absolute;left:13px;top:28px;bottom:0;width:2px;background:rgba(28,30,44,.16)}
.vstep.done .line{background:#395ad2}
.vstep:last-child .line{display:none}
.vstep .tt{display:flex;flex-direction:column;gap:2px;padding-top:3px}
.vstep .tt b{font-size:14px;line-height:20px}
.vstep .tt span{font-size:12px;line-height:16px;color:rgba(28,30,44,.6)}
/* camera & crop (unifiedapp snap UX, dark) */
.desk{position:absolute;inset:0;background:radial-gradient(120% 80% at 50% 32%,#4b433c 0%,#2a2521 58%,#171412 100%)}
.paper{position:absolute;box-shadow:0 12px 30px rgba(0,0,0,.55);border-radius:2px;overflow:hidden;background:#fdfdfb}
.paper svg{display:block;width:100%;height:100%}
.cam-scrim{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,.55) 0 13%,transparent 26% 60%,rgba(0,0,0,.62) 76%,rgba(0,0,0,.78));pointer-events:none}
.ctop{position:absolute;left:0;right:0;top:44px;height:56px;display:flex;align-items:center;justify-content:space-between;padding:0 12px;z-index:30;color:#fff}
.ctop.flow{position:static;flex:0 0 56px}
.ctop .t{font-size:16px;font-weight:700;flex:1 1 auto;text-align:center}
.cbtn{width:40px;height:40px;border-radius:50%;background:rgba(255,255,255,.12);border:0;display:flex;align-items:center;justify-content:center;color:#fff;cursor:pointer;padding:0;flex:0 0 40px}
.cbtn:hover{background:rgba(255,255,255,.22);color:#fff}
.cpill{height:30px;padding:0 12px;border-radius:15px;border:1px solid rgba(255,255,255,.32);background:rgba(40,40,42,.5);color:#fff;font-size:13px;font-weight:600;display:flex;align-items:center;gap:6px;white-space:nowrap}
.guide{position:absolute;z-index:25;pointer-events:none}
.guide i{position:absolute;width:28px;height:28px;border:3px solid #fff;border-radius:3px}
.guide i.tl{left:-2px;top:-2px;border-right:0;border-bottom:0}.guide i.tr{right:-2px;top:-2px;border-left:0;border-bottom:0}
.guide i.bl{left:-2px;bottom:-2px;border-right:0;border-top:0}.guide i.br{right:-2px;bottom:-2px;border-left:0;border-top:0}
.chint{position:absolute;left:0;right:0;bottom:184px;text-align:center;color:#fff;font-size:14px;font-weight:600;text-shadow:0 1px 6px rgba(0,0,0,.6);z-index:25;margin:0}
.shutter-row{position:absolute;left:0;right:0;bottom:64px;height:72px;display:flex;align-items:center;justify-content:center;z-index:30}
.shutter{width:68px;height:68px;border-radius:50%;background:#395ad2;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 22px rgba(57,90,210,.55),0 0 0 4px rgba(255,255,255,.9);color:#fff}
.shutter:hover{background:#2c48ae;color:#fff}
.gbtn{position:absolute;top:50%;transform:translateY(-50%);width:48px;height:48px;border-radius:50%;background:rgba(255,255,255,.14);border:0;color:#fff;display:flex;align-items:center;justify-content:center;cursor:pointer;padding:0}
.gbtn.l{left:64px}.gbtn.r{right:64px}
.gbtn .b{position:absolute;right:-4px;top:-4px;min-width:18px;height:18px;border-radius:9px;background:#ffc20a;color:#1c1e2c;font-size:11px;font-weight:700;display:flex;align-items:center;justify-content:center;padding:0 5px}
.photo{position:relative;flex:1 1 auto;min-height:0;margin:12px 16px 0;background:#1c1c1e;border-radius:6px;overflow:hidden}
.veil{position:absolute;background:rgba(20,20,22,.78);pointer-events:none}
.band{position:absolute;border:2px solid #395ad2;border-radius:5px;box-shadow:0 0 0 2px rgba(255,255,255,.85)}
.hd{position:absolute;width:16px;height:16px;border-radius:50%;background:#395ad2;border:2px solid #fff;z-index:4}
.hd.tl{top:-9px;left:-9px}.hd.tr{top:-9px;right:-9px}.hd.bl{bottom:-9px;left:-9px}.hd.br{bottom:-9px;right:-9px}
.cctl{flex:0 0 auto;display:flex;flex-direction:column;gap:10px;padding:14px 16px 20px}
.crop-cap{text-align:center;color:#fff;font-size:15px;font-weight:600;margin:0;text-shadow:0 1px 6px rgba(0,0,0,.6)}
.ctools{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.tool{height:36px;padding:0 14px;border-radius:18px;border:1px solid rgba(255,255,255,.3);background:rgba(255,255,255,.08);color:#fff;font-size:13px;font-weight:700;display:inline-flex;align-items:center;gap:6px;cursor:pointer;font-family:inherit;white-space:nowrap}
.tool:hover{background:rgba(255,255,255,.18);color:#fff}
.tool.on{background:#fff;color:#1c1e2c;border-color:#fff}
.cnote{color:rgba(255,255,255,.72);font-size:12px;margin:0}
.thumbs{display:flex;align-items:flex-start;gap:14px}
.thumb-w{display:flex;flex-direction:column;align-items:center;gap:6px;color:rgba(255,255,255,.9);font-size:12px}
.thumb{width:56px;height:56px;border-radius:7px;overflow:hidden;border:2px solid rgba(255,255,255,.45);background:#111;position:relative;display:flex;align-items:center;justify-content:center}
.thumb.on{border-color:#fff}
.thumb .no{position:absolute;left:2px;top:2px;background:#395ad2;color:#fff;font-size:10px;font-weight:700;border-radius:4px;padding:1px 5px}
.thumb.add{border:2px dashed rgba(255,255,255,.75);background:none;color:#fff}
.thumb.add:hover{background:rgba(255,255,255,.1);color:#fff}
.crop-next{align-self:flex-end;height:52px;padding:0 24px;border-radius:26px;border:0;background:#395ad2;color:#fff;font-size:16px;font-weight:700;display:inline-flex;align-items:center;gap:8px;box-shadow:0 6px 20px rgba(57,90,210,.45)}
.crop-next:hover{background:#2c48ae;color:#fff}
/* pages review (light) */
.pstrip{display:flex;gap:12px;align-items:flex-start;overflow-x:auto;padding:2px}
.pth{width:72px;height:92px;border-radius:8px;overflow:hidden;border:2px solid rgba(28,30,44,.12);background:#e9e9ec;position:relative;flex:0 0 72px;display:flex;align-items:center;justify-content:center;padding:0;cursor:pointer}
.pth.on{border-color:#395ad2;box-shadow:0 0 0 2px #eef1ff}
.pth .no{position:absolute;left:4px;top:4px;background:#395ad2;color:#fff;font-size:10px;font-weight:700;border-radius:4px;padding:1px 5px}
.pth.add{border:2px dashed rgba(57,90,210,.5);background:#fafbff;color:#395ad2}
.pth.add:hover{background:#eef1ff;color:#395ad2}
.preview{position:relative;height:300px;border-radius:8px;background:#e9e9ec;overflow:hidden;display:flex;align-items:center;justify-content:center}
.preview .pg{position:absolute;right:10px;bottom:10px;background:rgba(28,30,44,.75);color:#fff;font-size:12px;font-weight:700;border-radius:1000px;padding:3px 10px}
/* feedback: bottom sheet */
.scrim{position:absolute;inset:0;background:rgba(28,30,44,.38);z-index:39;border:0;padding:0;cursor:pointer}
.sheet{position:absolute;left:0;right:0;bottom:0;background:#fff;border-radius:16px 16px 0 0;box-shadow:0 -8px 24px rgba(0,0,0,.18);padding:8px 20px 56px;z-index:40;display:flex;flex-direction:column;gap:12px;max-height:74%;overflow:auto}
.grab{width:40px;height:4px;border-radius:2px;background:rgba(28,30,44,.2);margin:0 auto 4px;flex:0 0 4px}
.sheet .fbody{font-size:14px;line-height:1.8}
.sheet-nav{display:flex;align-items:center;justify-content:space-between;gap:8px;padding-top:4px;border-top:1px solid rgba(28,30,44,.12)}
.snb{height:40px;padding:0 14px;border-radius:1000px;border:1px solid rgba(28,30,44,.12);background:#fff;color:rgba(28,30,44,.87);font-size:13px;font-weight:700;display:inline-flex;align-items:center;gap:6px;cursor:pointer;font-family:inherit}
.snb:hover{background:#f2f2f4}
.sx{position:absolute;right:12px;top:12px;width:32px;height:32px;border-radius:50%;border:0;background:#f2f2f4;display:flex;align-items:center;justify-content:center;cursor:pointer;color:#404564;padding:0}
.mraw{font-size:14px;line-height:1.9;margin:0 0 12px}
.pts{display:flex;gap:8px;flex-wrap:wrap}
.pt{height:30px;padding:0 10px;border-radius:1000px;border:1px solid rgba(28,30,44,.12);background:#fff;font-size:12px;font-weight:700;display:inline-flex;align-items:center;gap:6px;cursor:pointer;font-family:inherit;color:rgba(28,30,44,.87)}
.pt:hover{background:#f2f2f4}
.pt.hit{border-color:#395ad2;background:#eef1ff}
"""
HELMET = ('<helmet><link rel="preconnect" href="https://fonts.googleapis.com">'
          '<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&amp;display=swap" rel="stylesheet">'
          f'<style>{CSS}</style></helmet>')

# ---------- strings ----------
JA = dict(
    lang="ja", student="山田 花子", back="もどる", menu="メニュー", notif="お知らせ 6件", lang_aria="言語", sep="・",
    crumb_course="コース", crumb_study="学習", todo="やること",
    course="地域環境統計学", course_meta="応用社会学部 2年 ・ 安本 正義 先生 ・ 木曜 3限",
    progress="全16回 ・ 第7回まで公開", book="教材：地域環境統計学 テキスト（2026年度）",
    t71="7-1　相関分析", t72="7-2　仮説検定", t61="6-1　相関と外れ値", t81="8-1　回帰分析", lt_video="動画", lt_doc="資料", lt_file="ファイル", lt_fb="フィードバック",
    lo_fb7_name="第7回 演習レポート", lo_fb6_name="第6回 演習レポート", lo_ref6_name="第6回 週のふりかえり", lo_fb8_name="第8回 演習レポート",
    wk7="第7回　データの分析と仮説検定", wk7_pub="11月6日 公開",
    wk6="第6回　相関と外れ値", wk6_pub="10月30日 公開",
    wk8="第8回　回帰分析の基礎", wk8_from="11月20日から",
    lo_video="第7回 講義動画", lo_video_s="42分 ・ 視聴済み",
    lo_pdf="第7回 講義資料（PDF）", lo_pdf_s="24ページ ・ 閲覧済み",
    lo_xlsx="第7回 演習ファイル（Excel）", lo_xlsx_s="都道府県別データ.xlsx ・ ダウンロード済み",
    lo_fb7="第7回 演習 のフィードバック", lo_fb_s="提出した演習レポートへのコメント",
    chip_notsub="未提出 ・ 11月13日まで",
    lo_fb6="第6回 演習 のフィードバック",
    lo_ref6="第6回 週のふりかえり のフィードバック", lo_ref_s="300字のふりかえり",
    chip_returned="返却済み",
    lo_fb8="第8回 演習 のフィードバック", lo_fb8_s="開始日になると「やること」に表示されます", chip_pre="開始前",
    a_crumb="地域環境統計学 ／ 第7回", a_h="第7回 演習：都道府県別データの相関分析",
    a_meta="安本 正義 先生 ・ 11月6日 出題", a_due="11月13日 23:59 まで",
    a_desc="総務省「社会生活統計指標」の都道府県別データから2つの変数を選び、Excel で相関係数を求めて散布図を作成してください。結果の解釈と、有意性の確認までを A4 2枚程度のレポートにまとめて提出します。",
    a_crit_h="コメントの観点",
    criteria=["Excelスキル","図表の見やすさ","統計処理","解釈","論理構成","生成AIリテラシー"],
    a_flow_h="提出してから返却まで",
    steps=[("提出する","ファイル・写真をアップロード、または直接入力"),("先生がフィードバック","期限のあとに返却"),("返却","お知らせが届きます")],
    a_upload_h="答案を提出する", a_upload_meta="PDF ・ Word ・ Excel ・ PowerPoint ・ 写真（JPG / PNG / HEIC） ・ 20MB まで",
    a_drop="ファイルや写真をここにドロップ", a_drop_s="Excel も PowerPoint もそのまま提出できます。手書きの答案は撮影した写真をまとめてアップロードできます",
    a_photo="答案の写真を選ぶ", a_photo_s="複数枚まとめて選べます。ページ順に並びます",
    a_photos_name="答案の写真 3枚", a_photos_meta="JPG ・ 合計 4.1 MB ・ ページ順 ・ いま選択", a_photos_add="写真を追加",
    a_mode_file="ファイル・写真をアップロード", a_mode_text="直接入力する",
    a_ta_ph="ここに入力してください。週次リフレクションなど短い課題はファイルなしで提出できます。",
    a_ta_target="目安 300字", a_ta_unit="文字", a_ta_note="入力内容はそのまま先生に届きます。提出後も期限までは書き直せます。",
    a_ta_confirm="回答を確定する", a_ta_confirm_note="確定すると、提出の基本条件を確認します", a_ta_confirmed="回答を確定しました", a_ta_edit="編集する",
    a_pick="ファイルを選ぶ", a_note="提出すると先生に届きます。フィードバックは期限のあとに返却されます。",
    a_submit="この答案を提出する", a_file="第7回_演習_山田花子.pdf", a_file_meta="3ページ ・ 1.2 MB ・ いま選択", a_remove="ファイルを外す",
    pc_h="提出の基本条件", pc_note="この課題で必ず含めるもの", pc_wait="",
    pc_items=[("ok","散布図が含まれている",""),("ok","相関係数が記載されている",""),("ok","有意性の検定が記載されている",""),
              ("warn","参照した講義資料の記載","見つかりませんでした。提出前に確認してください"),("ok","ページ数 3（目安は 2 枚程度）","")],
    decl_h="AI 利用の申告", decl_sub="任意",
    decl_note="申告は、安本先生が「生成AIリテラシー」の観点を見るときに参照します。AI がこれを使って不正を判定することはありません。",
    decl=["使っていない","数式・関数の確認","文章の校正","構成の相談"], decl_kept="AI の文をそのまま残した箇所があれば書いてください（任意）",
    p_chip="フィードバック待ち", p_h="提出しました", p_received="11月11日 14:32 に受け付けました",
    p_steps=[("提出","11月11日 14:32"),("先生がフィードバック","期限のあとに返却されます"),("返却","届いたらお知らせします")],
    p_teacher_h="先生からフィードバックが届きます",
    p_teacher_body="期限（{due}）のあと、先生からフィードバックが返却されます。届いたらここに表示され、お知らせでもお伝えします。",
    p_teacher_cap="",
    p_expect="フィードバックが届いたら、お知らせでお伝えします。",
    p_sub_h="提出したもの", p_file_meta="3ページ ・ 1.2 MB ・ 11月11日 14:32", p_view="提出物を見る", p_replace="ファイルを差し替える", p_replace_note="期限の 11月13日 23:59 までは差し替えできます。", p2_replace_note="期限の 11月20日 23:59 までは差し替えできます。", p_due1="11月13日 23:59", p_due2="11月20日 23:59", p_msg="先生にメッセージ",
    p_demo="先生が確認して返却する", tav="安",
    p2_chip="2回目 ・ フィードバック待ち", p2_received="11月19日 16:05 に受け付けました", p2_step1="11月19日 16:05",
    p2_file_meta="3ページ ・ 1.3 MB ・ 11月19日 16:05",
    f_chip="返却済み ・ 11月13日", f_meta="提出 11月11日 14:32 ・ 返却 11月13日 18:42",
    f_decl_echo="AI 利用の申告: 数式・関数の確認 ・ 残した文: なし",
    f_ask="先生に質問する", f_resubmit="修正して再提出する", f_resub_due="再提出は 11月20日 23:59 まで", f_pages="3ページ", f_save="コメントを PDF で保存",
    f_legend="コメントの番号は本文の下線と対応しています",
    f_raw_title="第7回 演習　都道府県別データによる相関分析", f_raw_meta="応用社会学部 2年　山田 花子　　提出: 2026年11月11日",
    raw=[
        '本演習では、総務省「社会生活統計指標」から47都道府県の人口密度と一人当たり県民所得のデータを取得し、両者の関係を分析した。Excel の CORREL 関数を用いて相関係数を算出したところ、r = 0.62 となり、正の相関が確認された。',
        '散布図を作成した結果、東京都が他の道府県から大きく離れた位置にあることが分かった。そこで東京都を除いて再計算すると r = 0.41 に低下し、東京都の値が相関係数を押し上げていることが確認できた。',
        'この結果から、人口密度が高い地域ほど所得が高くなるといえる。都市部に企業が集中し、雇用機会が多いためだと考えられる。',
        '有意性を確認するため T.TEST 関数を実行したところ、p 値は 0.03 であった。したがって帰無仮説は棄却され、2つの変数の間には統計的に有意な関係があるといえる。',
        '今後は、第三の変数として高齢化率を加えた分析を行い、地域差の背景をより多角的に捉えたい。',
    ],
    f_tnote_h="先生からのひとこと",
    f_tnote="東京都を除いて再計算したところ、よく気づきました。②の点は次回の授業でも取り上げるので、自分の考えを用意しておいてください。",
    f_sum="まとめ",
    f_sum_body="相関係数の算出から外れ値の検討、有意性の確認まで、分析の手順が一通り押さえられています。とくに東京都を除いて再計算した判断は、データを鵜呑みにしない姿勢としてすばらしいです。一方で、相関から因果へと一足で進んでいる箇所と、T.TEST の使い方には見直す余地があります。再提出では「このデータから言えること」と「言えないこと」の線引きを意識してみましょう。",
    labels={"good":"優れた点","ask":"問いかけ","todo":"改善点"},
    cards=[
        ("good","統計処理","そこで東京都を除いて再計算すると r = 0.41 に低下し、東京都の値が相関係数を押し上げていることが確認できた。",
         "外れ値の影響を疑い、除外前後の相関係数を並べて示した点がとても良いです。数値がどう変わったかを具体的に書いているので、読む側も判断の根拠を追うことができます。第6回で扱った「外れ値の扱い」がしっかり生かされています。",
         "第6回 講義資料 p.14「外れ値と相関係数」"),
        ("ask","解釈","この結果から、人口密度が高い地域ほど所得が高くなるといえる。",
         "相関係数が正だったことから「人口密度が高いほど所得が高くなる」と述べていますが、これは因果関係の主張になっています。逆に「所得が高い地域に人が集まる」という説明も、同じデータから成り立ちませんか。相関と因果のちがいを、この文の前後で一度整理してみてください。",
         "第5回 講義資料 p.8「相関と因果」"),
        ("todo","統計処理","有意性を確認するため T.TEST 関数を実行したところ、p 値は 0.03 であった。",
         "T.TEST は2つのグループの平均の差を検定する関数です。2つの変数の相関が有意かどうかを調べたい場合は、相関係数の検定（t = r√(n−2) ／ √(1−r²)）を用います。どの検定が何を調べているのかを講義資料の表で確認してから、計算式を書き直してみましょう。",
         "第7回 講義資料 p.11「検定の使い分け」"),
    ],
    next_h="次の一歩",
    next_body="③の検定を書き直し、②の文は「相関がある」までの主張にとどめてから再提出しましょう。第7回資料 p.11 の表を見て、使った検定の名前を一行で書き添えてください。",
    f_footer="",
    f_jump="本文の該当箇所を見る",
    # resubmit
    r_title="第7回 演習 のフィードバック ― 2回目の提出", r_h="2回目の提出", r_due="11月20日 23:59 まで",
    r_prev_h="前回のコメント", r_prev_sub="直したものにチェックを入れてください", r_keep="維持できているか確認",
    r_self_h="自己チェック", r_self=["自分の言葉で書き直した","AI の文をそのまま使った箇所がある"],
    r_self_note="正直に答えて大丈夫です。先生が次の指導に使います。",
    r_submit="2回目を提出する", r_file="第7回_演習_山田花子_v2.pdf", r_file_meta="3ページ ・ 1.3 MB ・ いま選択",
    r_note="提出すると先生に届きます。前回のコメントが直っているかも見てもらえます。",
    # feedback 2
    f2_chip="返却済み ・ 11月21日", f2_meta="2回目 ・ 提出 11月19日 16:05 ・ 返却 11月21日 17:10",
    f2_raw_meta="応用社会学部 2年　山田 花子　　2回目の提出: 2026年11月19日",
    f2_chg_h="前回からの変化",
    f2_chg=[("done","③ 検定の使い分け（統計処理）― 直りました"),("done","② 相関と因果（解釈）― 直りました"),("new","新しいコメント 1件（論理構成）")],
    f2_own="前回の指摘箇所は、自分の言葉で書き直されています。", f2_self_echo="自己チェック: 自分の言葉で書き直した",
    f2_tnote="検定をきちんと直せています。②も「相関がある」までにとどめた書き方になり、ぐっと良くなりました。冒頭に問いを一文置けば、レポートとして完成です。",
    f2_sum_body="前回の2つの改善点が、どちらも自分の言葉で直されています。検定は相関係数の検定に置き換わり、計算過程も示されました。解釈も「相関がある」までにとどめ、逆の説明があり得ることまで書けています。残るのは構成です。冒頭に「何を明らかにしたいのか」が書かれていないため、結論で答えている問いが読者に見えません。",
    raw2=[
        '本演習では、総務省「社会生活統計指標」から47都道府県の人口密度と一人当たり県民所得のデータを取得し、両者の関係を分析した。Excel の CORREL 関数を用いて相関係数を算出したところ、r = 0.62 となり、正の相関が確認された。',
        '散布図を作成した結果、東京都が他の道府県から大きく離れた位置にあることが分かった。そこで東京都を除いて再計算すると r = 0.41 に低下し、東京都の値が相関係数を押し上げていることが確認できた。',
        'この結果から、人口密度と所得の間には正の相関があるといえる。ただし、これは「人口密度が高いから所得が高い」ことを示すものではなく、所得の高い地域に人が集まるという逆の説明も同じデータから成り立つ。',
        '相関係数の有意性を確認するため、t = r√(n−2) ／ √(1−r²) により t 値を求めたところ t = 5.30（自由度 45）となり、p < 0.01 で有意であった。したがって、2つの変数の間の相関は偶然とは考えにくい。',
        'したがって両者には正の相関があるが、因果の方向はこのデータだけでは判断できない。今後は高齢化率を加えた分析を行い、地域差の背景を多角的に捉えたい。',
    ],
    cards2=[
        ("good","解釈","ただし、これは「人口密度が高いから所得が高い」ことを示すものではなく、所得の高い地域に人が集まるという逆の説明も同じデータから成り立つ。",
         "前回の問いかけに、そのまま答える形で書き直せています。相関を述べたうえで因果の方向は判断できないと明記し、逆の説明を自分で挙げている点が、統計を扱う姿勢として大切です。",
         "第5回 講義資料 p.8「相関と因果」"),
        ("good","統計処理","t = r√(n−2) ／ √(1−r²) により t 値を求めたところ t = 5.30（自由度 45）となり、p < 0.01 で有意であった。",
         "検定を相関係数の検定に置き換え、式・t 値・自由度・p 値の順に示せています。r = 0.62、n = 47 からの計算も合っています。何を検定したのかが一読で分かる書き方です。",
         "第7回 講義資料 p.11「検定の使い分け」"),
        ("todo","論理構成","本演習では、総務省「社会生活統計指標」から47都道府県の人口密度と一人当たり県民所得のデータを取得し、両者の関係を分析した。",
         "結論では「正の相関はあるが因果の方向は判断できない」と、はっきりした問いに答えています。ところが冒頭には「関係を分析した」とあるだけで、その問いが書かれていません。「人口密度の高い地域ほど所得が高いといえるか」のように、明らかにしたいことを一文で置くと、結論までの筋が通ります。",
         "第7回 講義資料 p.3「分析の問いを立てる」"),
    ],
    next2_body="冒頭に「何を明らかにしたいか」を一文で。第8回の回帰分析では、今回の相関を説明変数の選び方に使ってみましょう。",
    f2_footer="",
    # todo
    t_week="今週　11月10日 – 16日", t_week_cap="開始日を過ぎたものが表示されます",
    t_fb7_chip="再提出待ち ・ 11月20日まで", t_fb7_when="11月13日 返却 ・ コメントを見る",
    t_ref7="第7回 週のふりかえり のフィードバック", t_ref7_when="11月12日 提出",
    t_sim="素因数分解 の AI演習", t_sim_course="数学基礎", t_sim_chip="11月15日まで",
    t_video="第7回 講義動画 を見る", t_done="完了",
    t_late_h="期限切れ", t_late="第6回 演習 の 再提出", t_late_chip="11月6日まで ・ 期限切れ",
    t_up_h="これから　11月20日から", t_up_cap="開始日になると上に移ります", t_fb8_chip="開始前 ・ 11月27日まで",
    titles={"course":"コース — 地域環境統計学","assign":"課題 — 答案を提出する","pending":"提出済み — 先生の確認待ち","fb":"フィードバック — 返却済み",
            "resub":"2回目の提出","pending2":"2回目 提出済み — 先生の確認待ち","fb2":"フィードバック — 2回目 返却済み","todo":"やること"},
)

EN = dict(
    lang="en", student="Hanako Yamada", back="Back", menu="Menu", notif="6 notifications", lang_aria="Language", sep="·",
    crumb_course="Courses", crumb_study="Learning", todo="To-do",
    course="Regional & Environmental Statistics", course_meta="Faculty of Applied Sociology, Year 2 · Prof. Masayoshi Yasumoto · Thu, 3rd period",
    progress="16 sessions · through Session 7 published", book="Book: Regional & Environmental Statistics — Textbook (2026)",
    t71="7-1 · Correlation analysis", t72="7-2 · Hypothesis testing", t61="6-1 · Correlation and outliers", t81="8-1 · Regression", lt_video="Video", lt_doc="Document", lt_file="File", lt_fb="Feedback",
    lo_fb7_name="Session 7 exercise report", lo_fb6_name="Session 6 exercise report", lo_ref6_name="Session 6 weekly reflection", lo_fb8_name="Session 8 exercise report",
    wk7="Session 7 · Data analysis and hypothesis testing", wk7_pub="Published Nov 6",
    wk6="Session 6 · Correlation and outliers", wk6_pub="Published Oct 30",
    wk8="Session 8 · Basics of regression", wk8_from="From Nov 20",
    lo_video="Session 7 lecture video", lo_video_s="42 min · Watched",
    lo_pdf="Session 7 lecture slides (PDF)", lo_pdf_s="24 pages · Viewed",
    lo_xlsx="Session 7 exercise file (Excel)", lo_xlsx_s="prefecture_data.xlsx · Downloaded",
    lo_fb7="Feedback · Session 7 exercise", lo_fb_s="Comments on your submitted exercise report",
    chip_notsub="Not submitted · due Nov 13",
    lo_fb6="Feedback · Session 6 exercise",
    lo_ref6="Feedback · Session 6 weekly reflection", lo_ref_s="300-character reflection",
    chip_returned="Returned",
    lo_fb8="Feedback · Session 8 exercise", lo_fb8_s="Appears in To-do on its start date", chip_pre="Not started",
    a_crumb="Regional & Environmental Statistics / Session 7", a_h="Session 7 exercise: Correlation analysis of prefectural data",
    a_meta="Prof. Masayoshi Yasumoto · Set Nov 6", a_due="Due Nov 13, 23:59",
    a_desc="Choose two variables from the Statistics Bureau's prefectural social indicators, compute the correlation coefficient in Excel and draw a scatter plot. Submit a report of about two A4 pages covering your interpretation and a check of statistical significance.",
    a_crit_h="What the comments cover",
    criteria=["Excel skills","Clarity of charts","Statistical processing","Interpretation","Logical structure","Generative-AI literacy"],
    a_flow_h="From submission to return",
    steps=[("Submit","Upload a file or photos, or type your answer"),("Teacher feedback","Returned after the due date"),("Returned","You get a notification")],
    a_upload_h="Submit your work", a_upload_meta="PDF · Word · Excel · PowerPoint · Photos (JPG / PNG / HEIC) · up to 20 MB",
    a_drop="Drop a file or photos here", a_drop_s="Excel and PowerPoint can be submitted as they are. Handwritten work can be photographed and uploaded as a set of photos",
    a_photo="Choose photos of your work", a_photo_s="Pick several at once; they are kept in page order",
    a_photos_name="3 photos of your work", a_photos_meta="JPG · 4.1 MB total · in page order · just selected", a_photos_add="Add photos",
    a_mode_file="Upload a file or photos", a_mode_text="Type your answer",
    a_ta_ph="Write here. Short pieces such as weekly reflections can be submitted without a file.",
    a_ta_target="Target about 300 characters", a_ta_unit="characters", a_ta_note="Your text goes to your teacher as written. You can edit it until the due date.",
    a_ta_confirm="Confirm answer", a_ta_confirm_note="Confirming checks it against the basic requirements", a_ta_confirmed="Answer confirmed", a_ta_edit="Edit answer",
    a_pick="Choose a file", a_note="Your submission goes to your teacher. Feedback is returned after the due date.",
    a_submit="Submit this work", a_file="Session7_Exercise_HanakoYamada.pdf", a_file_meta="3 pages · 1.2 MB · just selected", a_remove="Remove file",
    pc_h="Basic requirements", pc_note="What this submission must include", pc_wait="",
    pc_items=[("ok","Scatter plot included",""),("ok","Correlation coefficient stated",""),("ok","Significance test stated",""),
              ("warn","Lecture material referenced","Not found. Check before you submit"),("ok","3 pages (guide: about 2)","")],
    decl_h="AI-use declaration", decl_sub="optional",
    decl_note="Your teacher refers to this when looking at the \"generative-AI literacy\" criterion. The AI never uses it to judge misconduct.",
    decl=["Did not use","Checking formulas","Proofreading","Planning the structure"], decl_kept="Passages kept from AI output, if any (optional)",
    p_chip="Awaiting feedback", p_h="Submitted", p_received="Received Nov 11, 14:32",
    p_steps=[("Submitted","Nov 11, 14:32"),("Teacher feedback","Returned after the due date"),("Returned","We'll notify you when it arrives")],
    p_teacher_h="Feedback from your teacher is on its way",
    p_teacher_body="After the due date ({due}), your teacher returns feedback. It will appear here and you'll get a notification.",
    p_teacher_cap="",
    p_expect="You'll get a notification when your feedback arrives.",
    p_sub_h="Your submission", p_file_meta="3 pages · 1.2 MB · Nov 11, 14:32", p_view="View submission", p_replace="Replace file", p_replace_note="You can replace it until the due date, Nov 13, 23:59.", p2_replace_note="You can replace it until the due date, Nov 20, 23:59.", p_due1="Nov 13, 23:59", p_due2="Nov 20, 23:59", p_msg="Message teacher",
    p_demo="Teacher approves and returns", tav="Y",
    p2_chip="2nd submission · Awaiting feedback", p2_received="Received Nov 19, 16:05", p2_step1="Nov 19, 16:05",
    p2_file_meta="3 pages · 1.3 MB · Nov 19, 16:05",
    f_chip="Returned · Nov 13", f_meta="Submitted Nov 11, 14:32 · Returned Nov 13, 18:42",
    f_decl_echo="AI-use declaration: checking formulas · kept passages: none",
    f_ask="Ask your teacher", f_resubmit="Revise and resubmit", f_resub_due="Resubmit by Nov 20, 23:59", f_pages="3 pages", f_save="Save comments as PDF",
    f_legend="Comment numbers match the underlined passages",
    f_raw_title="Session 7 Exercise: Correlation analysis using prefectural data", f_raw_meta="Faculty of Applied Sociology, Year 2 · Hanako Yamada · Submitted Nov 11, 2026",
    raw=[
        "In this exercise I took population density and per-capita prefectural income for the 47 prefectures from the Statistics Bureau's social indicators and analysed the relationship between them. Using Excel's CORREL function, the correlation coefficient came to r = 0.62, confirming a positive correlation.",
        "The scatter plot showed Tokyo sitting far away from the other prefectures. Recalculating without Tokyo lowered the coefficient to r = 0.41, confirming that Tokyo's values were pulling the correlation up.",
        "From this result it can be said that the denser a region's population, the higher its income. This is likely because companies concentrate in urban areas, creating more employment.",
        "To check significance I ran the T.TEST function, which gave a p-value of 0.03. The null hypothesis is therefore rejected, and there is a statistically significant relationship between the two variables.",
        "Next I would like to add the ageing rate as a third variable, to capture the background of regional differences from more angles.",
    ],
    f_tnote_h="A note from your teacher",
    f_tnote="Good catch recalculating without Tokyo. We'll pick up point ② in the next class, so have your own view ready.",
    f_sum="Summary",
    f_sum_body="You cover the full sequence of the analysis: computing the coefficient, checking for outliers, and testing significance. Recalculating without Tokyo was an excellent decision — it shows you don't take the data at face value. Two things to revisit: one place where you jump from correlation straight to causation, and how T.TEST is used. For the resubmission, keep a clear line between what this data can say and what it cannot.",
    labels={"good":"Strength","ask":"Question","todo":"To improve"},
    cards=[
        ("good","Statistical processing","Recalculating without Tokyo lowered the coefficient to r = 0.41, confirming that Tokyo's values were pulling the correlation up.",
         "Suspecting an outlier and showing the coefficient before and after removing it is very good practice. Because you state exactly how the number changed, a reader can follow the basis of your judgement. This applies what we covered in Session 6 on handling outliers.",
         "Session 6 slides, p.14 — Outliers and the correlation coefficient"),
        ("ask","Interpretation","From this result it can be said that the denser a region's population, the higher its income.",
         "Because the coefficient was positive, you conclude that higher density leads to higher income — but that is a causal claim. Could the reverse explanation, that people move to regions where income is already high, be supported by the same data? Take a moment to separate correlation from causation around this sentence.",
         "Session 5 slides, p.8 — Correlation and causation"),
        ("todo","Statistical processing","To check significance I ran the T.TEST function, which gave a p-value of 0.03.",
         "T.TEST tests the difference between the means of two groups. To test whether a correlation between two variables is significant, use the test for the correlation coefficient (t = r√(n−2) / √(1−r²)). Check which test answers which question in the table in the slides, then rewrite the calculation.",
         "Session 7 slides, p.11 — Choosing the right test"),
    ],
    next_h="Next step",
    next_body="Rewrite the test in ③ and keep the claim in ② to \"there is a correlation\", then resubmit. Look at the table on p.11 of the Session 7 slides and add one line naming the test you used.",
    f_footer="",
    f_jump="Show this passage in the text",
    r_title="Feedback · Session 7 exercise — Second submission", r_h="Second submission", r_due="Due Nov 20, 23:59",
    r_prev_h="Last time's comments", r_prev_sub="Tick what you've addressed", r_keep="Check it still holds",
    r_self_h="Self-check", r_self=["I rewrote it in my own words","Some AI sentences are used as-is"],
    r_self_note="It's fine to be honest. Your teacher uses this for the next round of guidance.",
    r_submit="Submit second draft", r_file="Session7_Exercise_HanakoYamada_v2.pdf", r_file_meta="3 pages · 1.3 MB · just selected",
    r_note="Your submission goes to your teacher, who will also see whether last time's comments were addressed.",
    f2_chip="Returned · Nov 21", f2_meta="2nd submission · Submitted Nov 19, 16:05 · Returned Nov 21, 17:10",
    f2_raw_meta="Faculty of Applied Sociology, Year 2 · Hanako Yamada · 2nd submission: Nov 19, 2026",
    f2_chg_h="Since last time",
    f2_chg=[("done","③ Choosing the right test (statistical processing) — fixed"),("done","② Correlation vs. causation (interpretation) — fixed"),("new","1 new comment (logical structure)")],
    f2_own="The passages flagged last time have been rewritten in your own words.", f2_self_echo="Self-check: rewrote in my own words",
    f2_tnote="You've fixed the test properly, and ② now stops at \"there is a correlation\" — a big improvement. One sentence stating your question at the start and this is a complete report.",
    f2_sum_body="Both of last time's points have been fixed, in your own words. The test is now the test for the correlation coefficient, with the working shown. The interpretation stops at \"there is a correlation\" and even names the reverse explanation. What remains is structure: the opening never says what you set out to find, so the reader can't see which question the conclusion answers.",
    raw2=[
        "In this exercise I took population density and per-capita prefectural income for the 47 prefectures from the Statistics Bureau's social indicators and analysed the relationship between them. Using Excel's CORREL function, the correlation coefficient came to r = 0.62, confirming a positive correlation.",
        "The scatter plot showed Tokyo sitting far away from the other prefectures. Recalculating without Tokyo lowered the coefficient to r = 0.41, confirming that Tokyo's values were pulling the correlation up.",
        "From this result it can be said that there is a positive correlation between population density and income. This does not, however, show that higher density causes higher income: the reverse explanation, that people move to regions where income is already high, is equally consistent with the data.",
        "To test the significance of the correlation coefficient I computed t = r√(n−2) / √(1−r²), giving t = 5.30 (45 degrees of freedom), significant at p < 0.01. The correlation between the two variables is therefore unlikely to be due to chance.",
        "There is thus a positive correlation between the two, but the direction of causation cannot be judged from this data alone. Next I would like to add the ageing rate to capture the background of regional differences from more angles.",
    ],
    cards2=[
        ("good","Interpretation","This does not, however, show that higher density causes higher income: the reverse explanation, that people move to regions where income is already high, is equally consistent with the data.",
         "You've rewritten this as a direct answer to last time's question. Stating the correlation, saying explicitly that the direction of causation cannot be judged, and naming the reverse explanation yourself — that is exactly the attitude statistics asks for.",
         "Session 5 slides, p.8 — Correlation and causation"),
        ("good","Statistical processing","I computed t = r√(n−2) / √(1−r²), giving t = 5.30 (45 degrees of freedom), significant at p < 0.01.",
         "The test is now the test for the correlation coefficient, shown in order: formula, t value, degrees of freedom, p value. The arithmetic from r = 0.62 and n = 47 is right. A reader sees at once what was tested.",
         "Session 7 slides, p.11 — Choosing the right test"),
        ("todo","Logical structure","In this exercise I took population density and per-capita prefectural income for the 47 prefectures from the Statistics Bureau's social indicators and analysed the relationship between them.",
         "Your conclusion answers a clear question — \"there is a positive correlation, but the direction of causation cannot be judged\". The opening, though, only says you \"analysed the relationship\"; the question itself is never stated. One sentence such as \"Can it be said that denser regions have higher incomes?\" would carry the reader straight through to the conclusion.",
         "Session 7 slides, p.3 — Framing the analytical question"),
    ],
    next2_body="One sentence at the start saying what you want to find out. In Session 8's regression, use this correlation to choose your explanatory variable.",
    f2_footer="",
    t_week="This week · Nov 10 – 16", t_week_cap="Items appear once their start date has passed",
    t_fb7_chip="Awaiting resubmission · by Nov 20", t_fb7_when="Returned Nov 13 · view comments",
    t_ref7="Feedback · Session 7 weekly reflection", t_ref7_when="Submitted Nov 12",
    t_sim="AI Practice · Prime factorisation", t_sim_course="Basic Mathematics", t_sim_chip="Due Nov 15",
    t_video="Watch Session 7 lecture video", t_done="Done",
    t_late_h="Overdue", t_late="Resubmission · Session 6 exercise", t_late_chip="Due Nov 6 · Overdue",
    t_up_h="Upcoming · from Nov 20", t_up_cap="Moves up on its start date", t_fb8_chip="Not started · due Nov 27",
    titles={"course":"Courses — Regional & Environmental Statistics","assign":"Assignment — Submit your work","pending":"Submitted — Awaiting teacher review","fb":"Feedback — Returned",
            "resub":"Second submission","pending2":"2nd submission — Awaiting teacher review","fb2":"Feedback — 2nd submission returned","todo":"To-do"},
)

MJA = dict(
    m_crumb="地域環境統計学 › 第7回 データの分析と仮説検定", m_banner_n="3 / 4", m_banner_l="完了",
    m_nav=["コース", "メッセージ", "カレンダー"],
    m_opt_cam="撮影して提出", m_opt_cam_s="手書きの答案を1ページずつ撮影します",
    m_opt_file="ファイル・写真を選ぶ", m_opt_file_s="PDF ・ Word ・ Excel ・ PowerPoint ・ 写真（複数枚まとめて）",
    m_opt_text="直接入力する", m_opt_text_s="週次リフレクションなど短い課題に",
    m_cam_title="答案を撮影", m_cam_hint="答案全体が枠に入るように", m_cam_page="1ページ目", m_cam_gallery="写真から選ぶ", m_cam_shutter="撮る", m_cam_flash="フラッシュ",
    m_close="閉じる", m_back="もどる",
    m_crop_title="範囲を切り取る", m_crop_cap="答案の端に合わせて切り取ろう", m_crop_auto="自動で合わせる", m_crop_rotate="回転", m_crop_retake="撮り直す",
    m_crop_note="角を動かして範囲を変えられます", m_add_page="ページを追加", m_next="次へ", m_page1="1", m_page2="2",
    m_pages_title="提出するページ", m_pages_hint="長押しで並べ替え ・ タップで確認", m_pages_count="1 / 2", m_pc_pages="ページ数 2（目安は 2 枚程度）",
    m_file_title="ファイル・写真を選ぶ", m_type_title="直接入力する",
    m_pending_pages="2ページ ・ 写真 ・ 11月11日 14:32", m_pending_replace="差し替える",
    m_fb_doc_h="提出した答案（読み取ったテキスト）", m_fb_points="コメント 3件 ・ 下線をタップすると開きます",
    m_prev="前へ", m_next_pt="次へ", m_lang_ja="日本語", m_lang_en="EN",
    m_dev_pc="PC", m_dev_mobile="モバイル", m_dev_teacher="先生（BO）", m_dev_aria="表示デバイス",
    m_titles={"main": "モバイル — LO一覧", "assign": "モバイル — 課題", "cam": "モバイル — 撮影", "crop": "モバイル — 切り取り", "pages": "モバイル — 提出するページ",
              "file": "モバイル — ファイル・写真を選ぶ", "type": "モバイル — 直接入力",
              "pending": "モバイル — 提出済み", "fb": "モバイル — 返却済み", "sheet": "モバイル — 返却済み（コメントを開いた状態）"},
)
MEN = dict(
    m_crumb="Regional & Environmental Statistics › Session 7 Data analysis and hypothesis testing", m_banner_n="3 / 4", m_banner_l="Completed",
    m_nav=["Courses", "Message", "Calendar"],
    m_opt_cam="Snap and submit", m_opt_cam_s="Photograph handwritten pages one at a time",
    m_opt_file="Choose a file or photos", m_opt_file_s="PDF · Word · Excel · PowerPoint · Photos (several at once)",
    m_opt_text="Type your answer", m_opt_text_s="For short pieces such as weekly reflections",
    m_cam_title="Snap your work", m_cam_hint="Fit the whole page inside the frame", m_cam_page="Page 1", m_cam_gallery="From photos", m_cam_shutter="Take photo", m_cam_flash="Flash",
    m_close="Close", m_back="Back",
    m_crop_title="Crop the page", m_crop_cap="Crop to the edges of the page", m_crop_auto="Auto-fit", m_crop_rotate="Rotate", m_crop_retake="Retake",
    m_crop_note="Drag a corner to adjust", m_add_page="Add page", m_next="Next", m_page1="1", m_page2="2",
    m_pages_title="Pages to submit", m_pages_hint="Hold to reorder · tap to preview", m_pages_count="1 / 2", m_pc_pages="2 pages (guide: about 2)",
    m_file_title="Choose a file or photos", m_type_title="Type your answer",
    m_pending_pages="2 pages · Photos · Nov 11, 14:32", m_pending_replace="Replace",
    m_fb_doc_h="Your submission (recognised text)", m_fb_points="3 comments · tap an underline to open one",
    m_prev="Previous", m_next_pt="Next", m_lang_ja="日本語", m_lang_en="EN",
    m_dev_pc="PC", m_dev_mobile="Mobile", m_dev_teacher="Teacher (BO)", m_dev_aria="Device",
    m_titles={"main": "Mobile — LO list", "assign": "Mobile — Assignment", "cam": "Mobile — Snap", "crop": "Mobile — Crop", "pages": "Mobile — Pages to submit",
              "file": "Mobile — Choose a file or photos", "type": "Mobile — Type your answer",
              "pending": "Mobile — Submitted", "fb": "Mobile — Returned", "sheet": "Mobile — Returned (comment sheet open)"},
)
JA.update(MJA); EN.update(MEN)

DECL = False  # AI-use declaration removed on PM decision (18 Sep): student self-report is not evidence
SCREENS = ["Main", "02-Assignment", "03-Pending", "04-Feedback", "06-Resubmit", "07-Pending2", "08-Feedback2", "05-Todo"]
MSCREENS = ["M-Main", "M-Assignment", "M-Camera", "M-Crop", "M-Pages", "M-File", "M-Type", "M-Pending", "M-Feedback", "M-Sheet"]
# PC <-> mobile counterparts for the bottom-left device switch
TO_MOBILE = {"Main": "M-Main", "02-Assignment": "M-Assignment", "03-Pending": "M-Pending", "04-Feedback": "M-Feedback",
             "06-Resubmit": "M-Assignment", "07-Pending2": "M-Pending", "08-Feedback2": "M-Feedback", "05-Todo": "M-Main"}
TO_PC = {"M-Main": "Main", "M-Assignment": "02-Assignment", "M-Camera": "02-Assignment", "M-Crop": "02-Assignment", "M-Pages": "02-Assignment",
         "M-File": "02-Assignment", "M-Type": "02-Assignment",
         "M-Pending": "03-Pending", "M-Feedback": "04-Feedback", "M-Sheet": "04-Feedback"}
CUR = "Main"  # screen being built (set by the write loop) so page() can place the device switch
def fn(screen, lang):
    return f"{screen}.dc.html" if lang == "ja" else f"{screen}-en.dc.html"

def device_toggle(S, screen, mobile=False, over_nav=False):
    L = S["lang"]
    if mobile:
        pc = f'<a class="dev-i" href="{fn(TO_PC[screen], L)}" aria-label="{S["m_dev_pc"]}">{ic("monitor",14)}<span class="dl">{S["m_dev_pc"]}</span></a>'
        mb = f'<span class="dev-i on">{ic("phone",14)}<span class="dl">{S["m_dev_mobile"]}</span></span>'
    else:
        pc = f'<span class="dev-i on">{ic("monitor",14)}<span class="dl">{S["m_dev_pc"]}</span></span>'
        mb = f'<a class="dev-i" href="{fn(TO_MOBILE[screen], L)}" aria-label="{S["m_dev_mobile"]}">{ic("phone",14)}<span class="dl">{S["m_dev_mobile"]}</span></a>'
    # prototype-only: the teacher's Back Office is one hop away from every student screen
    tc = f'<a class="dev-i" href="{tfn("T-Book", L)}" aria-label="{S["m_dev_teacher"]}">{mi("person", 14)}<span class="dl">{S["m_dev_teacher"]}</span></a>'
    cls = "dev" + (" m" if mobile else "") + (" nav" if over_nav else "")
    return f'<div class="{cls}" role="group" aria-label="{S["m_dev_aria"]}">{pc}{mb}{tc}</div>'

# ---------- chrome ----------
def lang_toggle(S, screen):
    ja_on = S["lang"] == "ja"
    ja = '<span class="seg-i on">日本語</span>' if ja_on else f'<a class="seg-i" href="{fn(screen,"ja")}" lang="ja">日本語</a>'
    en = '<span class="seg-i on">English</span>' if not ja_on else f'<a class="seg-i" href="{fn(screen,"en")}" lang="en">English</a>'
    return f'<div class="seg" role="group" aria-label="{S["lang_aria"]}">{ic("globe",14,"rgba(28,30,44,.6)")}{ja}{en}</div>'

def header(S, screen, title, crumb=None, back_href=None, right_extra=""):
    left_btn = (f'<a class="ibtn" href="{back_href}" aria-label="{S["back"]}">{ic("back",22)}</a>' if back_href
                else f'<button class="ibtn" aria-label="{S["menu"]}">{ic("menu",22)}</button>')
    tt = f'<div style="min-width:0"><p class="crumb">{crumb}</p><h1 class="h4">{title}</h1></div>' if crumb else f'<h1 class="h4">{title}</h1>'
    return f'''<header class="hdr">
  <div class="hdr-l">{left_btn}{tt}</div>
  <div class="hdr-r">{right_extra}{lang_toggle(S, screen)}
    <button class="bell" aria-label="{S["notif"]}">{ic("bell",24)}<span class="n">6</span></button>
    <button class="acct"><span class="av">{ic("person",20)}</span><span>{S["student"]}</span>{ic("down",16,"rgba(28,30,44,.6)")}</button>
  </div>
</header>'''

def page(S, title, body, logic="renderVals(){ return {}; }"):
    return f'''<!doctype html>
<html lang="{S["lang"]}">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
{HELMET}
<div class="root" style="width: 1280px; height: 800px;">
{body}
{device_toggle(S, CUR)}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1280,"height":800}}}}'>
class Component extends DCLogic {{
  {logic}
}}
</script>
</body>
</html>
'''

def lo_row(icon, title, sub, chip=None, href=None, sparkle=False, done=False, off=False):
    tile_cls = "tile done" if done else "tile"
    sp = f'<span class="sp">{ic("sparkle",12,"#1c1e2c",2.4)}</span>' if sparkle else ""
    inner = f'''<span class="{tile_cls}">{ic(icon,26)}{sp}</span>
    <span class="t"><b>{title}</b><i>{chip or ""}<span>{sub}</span></i></span>
    {ic("check",22,"#1f7a4d",2.4) if done else ic("right",20,"#c7c7cc",2.4)}'''
    cls = "lo off" if off else "lo"
    if href and not off:
        return f'<a class="{cls}" href="{href}">{inner}</a>'
    return f'<div class="{cls}">{inner}</div>'

def lt(label, fb=False):
    return f'<span class="chip lt{" fb" if fb else ""}">{label}</span>'

def sect(title, right="", muted=False):
    return f'''<div style="display:flex;align-items:center;justify-content:space-between;margin-top:8px">
    <p class="sub1{" muted" if muted else ""}">{title}</p>{right}</div>'''

# ---------- shared blocks ----------
def precheck_block(S, pending_hole=None):
    """Pre-submission structural checks. When pending_hole is given the block renders a waiting state under that sc-if."""
    items = ""
    for st, label, note in S["pc_items"]:
        icon = ic("check",14,"currentColor",3) if st == "ok" else ic("alert",14,"currentColor",2.4)
        items += f'<div class="pc {st}"><span class="st">{icon}</span><div class="tt"><b>{label}</b>{("<br><span class=cap>" + note + "</span>") if note else ""}</div></div>'
    waiting = "".join(f'<div class="pc pend"><span class="st">{ic("minus",14,"currentColor",3)}</span><div class="tt muted">{label}</div></div>' for _, label, _ in S["pc_items"])
    return f'''<div class="card" style="padding:20px 24px;display:flex;flex-direction:column;gap:8px">
    <div style="display:flex;align-items:center;justify-content:space-between"><p class="sub1">{S["pc_h"]}</p><span class="cap">{S["pc_note"]}</span></div>
    <sc-if value="{{{{empty}}}}" hint-placeholder-val="{{{{true}}}}">{waiting}</sc-if>
    <sc-if value="{{{{picked}}}}" hint-placeholder-val="{{{{false}}}}">{items}</sc-if>
  </div>'''

def decl_block(S):
    if not DECL:
        return ""
    chips = "".join(f'<button class="chip pick {{{{d{i}}}}}" onClick="{{{{t{i}}}}}">{lbl}</button>' for i, lbl in enumerate(S["decl"]))
    return f'''<div class="card" style="padding:20px 24px;display:flex;flex-direction:column;gap:12px">
    <div style="display:flex;align-items:center;gap:8px"><p class="sub1">{S["decl_h"]}</p><span class="chip pre" style="height:20px;font-size:11px">{S["decl_sub"]}</span></div>
    <div class="crit">{chips}</div>
    <div class="inp">{S["decl_kept"]}</div>
    <p class="cap">{S["decl_note"]}</p>
  </div>'''

DECL_LOGIC = """
      d0: this.state.d0 ? "sel" : "", d1: this.state.d1 ? "sel" : "", d2: this.state.d2 ? "sel" : "", d3: this.state.d3 ? "sel" : "",
      t0: () => this.setState({ d0: !this.state.d0, d1: false, d2: false, d3: false }),
      t1: () => this.setState({ d0: false, d1: !this.state.d1 }),
      t2: () => this.setState({ d0: false, d2: !this.state.d2 }),
      t3: () => this.setState({ d0: false, d3: !this.state.d3 }),"""

def upload_block(S, submit_label, file_name, file_meta, note, href):
    return f'''<sc-if value="{{{{empty}}}}" hint-placeholder-val="{{{{true}}}}">
      <div class="drop">
        <span style="width:56px;height:56px;border-radius:50%;background:#eef1ff;display:flex;align-items:center;justify-content:center;color:#395ad2">{ic("upload",28)}</span>
        <p class="b1" style="font-weight:700">{S["a_drop"]}</p>
        <p class="b2 muted" style="max-width:520px;text-align:center">{S["a_drop_s"]}</p>
        <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap;justify-content:center">
          <button class="btn neutral" onClick="{{{{pick}}}}">{ic("file",18)}{S["a_pick"]}</button>
          <button class="btn neutral" onClick="{{{{pickPhotos}}}}">{ic("camera",18)}{S["a_photo"]}</button>
        </div>
        <p class="cap" style="display:flex;align-items:center;gap:6px">{ic("image",14)}{S["a_photo_s"]}</p>
      </div>
    </sc-if>
    <sc-if value="{{{{pickedFile}}}}" hint-placeholder-val="{{{{false}}}}">
      <div class="filerow">
        <span class="ficon">{ic("filetext",22)}</span>
        <div style="flex:1 1 auto;min-width:0;display:flex;flex-direction:column;gap:2px">
          <p class="b2" style="font-weight:700">{file_name}</p>
          <p class="cap">{file_meta}</p>
        </div>
        <button class="ibtn" style="border:0" onClick="{{{{clear}}}}" aria-label="{S["a_remove"]}">{ic("x",20)}</button>
      </div>
    </sc-if>
    <sc-if value="{{{{pickedPhotos}}}}" hint-placeholder-val="{{{{false}}}}">
      <div class="filerow shots" style="align-items:flex-start">
        <span style="display:flex;gap:8px;flex:0 0 auto">
          <span class="shot"><i>1</i>{paper_inline(44, 58, False)}</span>
          <span class="shot"><i>2</i>{paper_inline(44, 58, False)}</span>
          <span class="shot"><i>3</i>{paper_inline(44, 58, False)}</span>
        </span>
        <div class="shots-txt" style="flex:1 1 auto;min-width:0;display:flex;flex-direction:column;gap:4px">
          <p class="b2" style="font-weight:700">{S["a_photos_name"]}</p>
          <p class="cap">{S["a_photos_meta"]}</p>
          <button class="btn ghost" style="height:30px;align-self:flex-start;padding:0 8px">{ic("plus",16)}{S["a_photos_add"]}</button>
        </div>
        <button class="ibtn" style="border:0" onClick="{{{{clear}}}}" aria-label="{S["a_remove"]}">{ic("x",20)}</button>
      </div>
    </sc-if>'''

def submit_row(S, label, note, href):
    return f'''<sc-if value="{{{{empty}}}}" hint-placeholder-val="{{{{true}}}}">
      <div style="display:flex;align-items:center;justify-content:flex-end;gap:16px">
        <span class="cap" style="text-align:right">{note}</span>
        <span class="btn dis">{ic("sparkle",18,"rgba(28,30,44,.38)")}{label}</span>
      </div>
    </sc-if>
    <sc-if value="{{{{picked}}}}" hint-placeholder-val="{{{{false}}}}">
      <div style="display:flex;align-items:center;justify-content:flex-end;gap:16px">
        <span class="cap" style="text-align:right">{note}</span>
        <a class="btn primary" href="{href}">{ic("sparkle",18,"#fff")}{label}</a>
      </div>
    </sc-if>'''

# ---------- screens ----------
def course(S, L):
    body = header(S, "Main", S["course"], crumb=S["crumb_course"]) + f'''
<div class="body"><div class="col">
  <div class="card row" style="padding:20px 24px">
    <span style="width:72px;height:72px;border-radius:50%;background:#eef1ff;display:flex;align-items:center;justify-content:center;color:#395ad2;flex:0 0 72px">{ic("book",34)}</span>
    <div style="flex:1 1 auto;min-width:0;display:flex;flex-direction:column;gap:6px">
      <h2 class="h3">{S["course"]}</h2>
      <p class="b2 muted">{S["course_meta"]}</p>
      <p class="cap" style="display:flex;align-items:center;gap:6px">{ic("book",12)}{S["book"]}</p>
    </div>
    <div style="display:flex;flex-direction:column;align-items:flex-end;gap:6px">
      <span class="cap">{S["progress"]}</span>
    </div>
  </div>
  {sect(S["wk7"], f'<span class="cap">{S["wk7_pub"]}</span>')}
  <p class="topic">{S["t71"]}</p>
  {lo_row("play", S["lo_video"], S["lo_video_s"], chip=lt(S["lt_video"]), done=True)}
  {lo_row("filetext", S["lo_pdf"], S["lo_pdf_s"], chip=lt(S["lt_doc"]), done=True)}
  <p class="topic">{S["t72"]}</p>
  {lo_row("table", S["lo_xlsx"], S["lo_xlsx_s"], chip=lt(S["lt_file"]), done=True)}
  {lo_row("filetext", S["lo_fb7_name"], S["lo_fb_s"], chip=lt(S["lt_fb"], True) + f'<span class="chip wait">{S["chip_notsub"]}</span>', href=fn("02-Assignment",L), sparkle=True)}
  {sect(S["wk6"], f'<span class="cap">{S["wk6_pub"]}</span>')}
  <p class="topic">{S["t61"]}</p>
  {lo_row("filetext", S["lo_fb6_name"], S["lo_fb_s"], chip=lt(S["lt_fb"], True) + f'<span class="chip done">{S["chip_returned"]}</span>', sparkle=True, done=True)}
  {lo_row("message", S["lo_ref6_name"], S["lo_ref_s"], chip=lt(S["lt_fb"], True) + f'<span class="chip done">{S["chip_returned"]}</span>', sparkle=True, done=True)}
  {sect(S["wk8"], f'<span class="chip pre">{ic("lock",12)}{S["wk8_from"]}</span>', muted=True)}
  <p class="topic">{S["t81"]}</p>
  {lo_row("filetext", S["lo_fb8_name"], S["lo_fb8_s"], chip=lt(S["lt_fb"], True) + f'<span class="chip pre">{S["chip_pre"]}</span>', sparkle=True, off=True)}
  <div style="height:8px"></div>
</div></div>'''
    return page(S, S["titles"]["course"], body)

def assignment(S, L):
    crit = "".join(f'<span class="chip neutral">{c}</span>' for c in S["criteria"])
    steps = ""
    for i, (l, s) in enumerate(S["steps"]):
        steps += f'<div class="step{" cur" if i == 0 else ""}"><span class="line"></span><span class="dot">{i+1}</span><span class="l">{l}</span><span class="s">{s}</span></div>'
    body = header(S, "02-Assignment", S["lo_fb7"], crumb=S["a_crumb"], back_href=fn("Main",L)) + f'''
<div class="body"><div class="col">
  <div class="card" style="padding:24px;display:flex;flex-direction:column;gap:16px">
    <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px">
      <div style="display:flex;flex-direction:column;gap:6px;min-width:0">
        <h2 class="h3">{S["a_h"]}</h2>
        <p class="b2 muted">{S["a_meta"]}</p>
      </div>
      <span class="chip wait" style="height:28px">{ic("clock",14)}{S["a_due"]}</span>
    </div>
    <p class="b1">{S["a_desc"]}</p>
    <div class="divider"></div>
    <div style="display:flex;flex-direction:column;gap:10px">
      <p class="sub1">{S["a_crit_h"]}</p>
      <div class="crit">{crit}</div>
    </div>
  </div>
  <div class="card" style="padding:24px 24px 20px">
    <p class="sub1" style="margin-bottom:20px">{S["a_flow_h"]}</p>
    <div class="steps">{steps}</div>
  </div>
  <div class="card" style="padding:24px;display:flex;flex-direction:column;gap:16px">
    <div style="display:flex;align-items:center;justify-content:space-between;gap:16px">
      <p class="sub1">{S["a_upload_h"]}</p>
      <sc-if value="{{{{isFile}}}}" hint-placeholder-val="{{{{true}}}}"><span class="cap">{S["a_upload_meta"]}</span></sc-if>
    </div>
    <div class="seg" style="align-self:flex-start;height:36px">
      <button class="seg-i {{{{mf}}}}" onClick="{{{{toFile}}}}">{ic("upload",14)}{S["a_mode_file"]}</button>
      <button class="seg-i {{{{mt}}}}" onClick="{{{{toText}}}}">{ic("filetext",14)}{S["a_mode_text"]}</button>
    </div>
    <sc-if value="{{{{isFile}}}}" hint-placeholder-val="{{{{true}}}}">
    {upload_block(S, S["a_submit"], S["a_file"], S["a_file_meta"], S["a_note"], fn("03-Pending",L))}
    </sc-if>
    <sc-if value="{{{{isTyping}}}}" hint-placeholder-val="{{{{false}}}}">
      <label class="cap" for="ta-answer" style="display:none">{S["a_mode_text"]}</label>
      <textarea id="ta-answer" class="ta" placeholder="{S["a_ta_ph"]}" maxlength="500" defaultValue="{{{{ttext}}}}" onInput="{{{{onType}}}}"></textarea>
      <div style="display:flex;align-items:center;justify-content:space-between;gap:16px">
        <span class="cap">{S["a_ta_note"]}</span>
        <span class="cap" style="white-space:nowrap;font-weight:700">{{{{tcount}}}} / 500 {S["a_ta_unit"]}</span>
      </div>
      <div style="display:flex;align-items:center;justify-content:flex-end;gap:16px">
        <sc-if value="{{{{noText}}}}" hint-placeholder-val="{{{{true}}}}"><span class="btn dis">{ic("check",18,"rgba(28,30,44,.38)")}{S["a_ta_confirm"]}</span></sc-if>
        <sc-if value="{{{{hasText}}}}" hint-placeholder-val="{{{{false}}}}"><button class="btn neutral" onClick="{{{{confirm}}}}">{ic("check",18)}{S["a_ta_confirm"]}</button></sc-if>
      </div>
    </sc-if>
    <sc-if value="{{{{isConfirmed}}}}" hint-placeholder-val="{{{{false}}}}">
      <div class="filerow" style="align-items:flex-start">
        <span class="ficon">{ic("filetext",22)}</span>
        <div style="flex:1 1 auto;min-width:0;display:flex;flex-direction:column;gap:6px">
          <p class="b2" style="font-weight:700;display:flex;align-items:center;gap:6px">{ic("check",14,"#1f7a4d",3)}{S["a_ta_confirmed"]} {S["sep"]} {{{{tcount}}}} {S["a_ta_unit"]}</p>
          <p class="b2 muted" style="white-space:pre-wrap;max-height:88px;overflow:hidden">{{{{ttext}}}}</p>
        </div>
        <button class="btn neutral" style="height:36px;font-size:13px" onClick="{{{{edit}}}}">{S["a_ta_edit"]}</button>
      </div>
    </sc-if>
  </div>
  {precheck_block(S)}
  {decl_block(S)}
  <div class="card" style="padding:16px 24px">
    {submit_row(S, S["a_submit"], S["a_note"], fn("03-Pending",L))}
  </div>
  <div style="height:8px"></div>
</div></div>'''
    logic = """state = { picked: "", mode: "file", tlen: 0, ttext: "", confirmed: false, d0: false, d1: false, d2: false, d3: false };
  renderVals() {
    const isText = this.state.mode === "text";
    const ready = isText ? this.state.confirmed : this.state.picked !== "";
    return {
      picked: ready,
      empty: !ready,
      pickedFile: !isText && this.state.picked === "file",
      pickedPhotos: !isText && this.state.picked === "photos",
      isFile: !isText, isText: isText,
      isTyping: isText && !this.state.confirmed,
      isConfirmed: isText && this.state.confirmed,
      noText: this.state.tlen === 0, hasText: this.state.tlen > 0,
      mf: isText ? "" : "on", mt: isText ? "on" : "",
      toFile: () => this.setState({ mode: "file" }),
      toText: () => this.setState({ mode: "text" }),
      onType: (e) => { const v = e.target.value || ""; this.setState({ tlen: v.length, ttext: v }); },
      confirm: () => this.setState({ confirmed: true }),
      edit: () => this.setState({ confirmed: false }),
      ttext: this.state.ttext,
      tcount: String(this.state.tlen),
      pick: () => this.setState({ picked: "file" }),
      pickPhotos: () => this.setState({ picked: "photos" }),
      clear: () => this.setState({ picked: "" }),""" + DECL_LOGIC + """
    };
  }"""
    return page(S, S["titles"]["assign"], body, logic)

def pending(S, L, draft=1):
    (l1, s1), (l2, s2), (l3, s3) = S["p_steps"]
    if draft == 2:
        s1 = S["p2_step1"]
    chip = S["p_chip"] if draft == 1 else S["p2_chip"]
    received = S["p_received"] if draft == 1 else S["p2_received"]
    expect = S["p_expect"]
    file_name = S["a_file"] if draft == 1 else S["r_file"]
    file_meta = S["p_file_meta"] if draft == 1 else S["p2_file_meta"]
    demo_to = fn("04-Feedback",L) if draft == 1 else fn("08-Feedback2",L)
    back = fn("Main",L) if draft == 1 else fn("04-Feedback",L)
    replace_to = fn("02-Assignment",L) if draft == 1 else fn("06-Resubmit",L)
    replace_note = S["p_replace_note"] if draft == 1 else S["p2_replace_note"]
    teacher_body = S["p_teacher_body"].replace("{due}", S["p_due1"] if draft == 1 else S["p_due2"])
    screen = "03-Pending" if draft == 1 else "07-Pending2"
    body = header(S, screen, S["lo_fb7"], crumb=S["a_crumb"], back_href=back,
                  right_extra=f'<span class="chip review" style="height:28px">{ic("clock",14)}{chip}</span>') + f'''
<div class="body"><div class="col">
  <div class="card" style="padding:32px 24px;display:flex;flex-direction:column;align-items:center;gap:12px;text-align:center">
    <span style="width:64px;height:64px;border-radius:50%;background:#e6f5ee;display:flex;align-items:center;justify-content:center;color:#1f7a4d">{ic("check",32,"#1f7a4d",2.6)}</span>
    <h2 class="h3">{S["p_h"]}</h2>
    <p class="b1 muted">{received}</p>
  </div>
  <div class="card" style="padding:24px 24px 20px">
    <div class="steps">
      <div class="step done"><span class="line"></span><span class="dot">{ic("check",16,"#fff",3)}</span><span class="l">{l1}</span><span class="s">{s1}</span></div>
      <div class="step cur"><span class="line"></span><span class="dot">2</span><span class="l">{l2}</span><span class="s">{s2}</span></div>
      <div class="step"><span class="line"></span><span class="dot">3</span><span class="l">{l3}</span><span class="s">{s3}</span></div>
    </div>
    <div class="divider" style="margin:16px 0 12px"></div>
    <div style="display:flex;align-items:center;justify-content:center;gap:10px">
      {ic("bell",16,"#395ad2")}<span class="b2" style="font-weight:500">{expect}</span>
    </div>
  </div>
  <div class="card" style="padding:24px;display:flex;gap:20px;align-items:flex-start">
    <span class="tav">{ic("person",20)}</span>
    <div style="display:flex;flex-direction:column;gap:8px;flex:1 1 auto">
      <p class="sub1">{S["p_teacher_h"]}</p>
      <p class="b1">{teacher_body}</p>
    </div>
  </div>
  <div class="card" style="padding:20px 24px;display:flex;flex-direction:column;gap:12px">
    <p class="sub1">{S["p_sub_h"]}</p>
    <div class="filerow" style="border:0;background:#f2f2f4">
      <span class="ficon">{ic("filetext",22)}</span>
      <div style="flex:1 1 auto;min-width:0;display:flex;flex-direction:column;gap:2px">
        <p class="b2" style="font-weight:700">{file_name}</p>
        <p class="cap">{file_meta}</p>
      </div>
      <button class="btn ghost">{ic("eye",18)}{S["p_view"]}</button>
      <a class="btn neutral" href="{replace_to}">{ic("refresh",18)}{S["p_replace"]}</a>
    </div>
    <p class="cap">{replace_note}</p>
  </div>
  <div style="height:8px"></div>
</div></div>
<a class="demo" href="{demo_to}"><span class="tag">DEMO</span>{S["p_demo"]}{ic("right",16,"#fff",2.4)}</a>'''
    return page(S, S["titles"]["pending" if draft == 1 else "pending2"], body)

def feedback_cards(S, cards, jump_prefix="j"):
    out = ""
    for i, (kind, crit, quote, body, ref) in enumerate(cards):
        n = i + 1
        out += f'''<div id="card-{n}" class="fb-card {{{{h{n}}}}}">
      <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding-right:36px"><span class="badge {kind}"><i class="n">{n}</i>{S["labels"][kind]}</span><span class="ctag">{crit}</span></div>
      <blockquote class="quote {kind}">“{quote}”</blockquote>
      <p class="fbody">{body}</p>
      <span class="ref">{ic("book",14)}{ref}</span>
      <button class="jump" onClick="{{{{jc{n}}}}}" aria-label="{S["f_jump"]}">{ic("scan",18)}</button>
    </div>'''
    return out

def marks_html(raw, kinds_by_para):
    """kinds_by_para: {para_index: (n, kind)}"""
    ps = []
    for i, p in enumerate(raw):
        if i in kinds_by_para:
            n, kind = kinds_by_para[i]
            ps.append(f'<p class="raw"><button id="mark-{n}" class="fbm {kind} {{{{h{n}}}}}" onClick="{{{{jm{n}}}}}"><i class="n">{n}</i>{p}</button></p>')
        else:
            ps.append(f'<p class="raw">{p}</p>')
    return "".join(ps)

HIT_LOGIC = """state = { hit: 0, from: "" };
  componentDidUpdate(prevProps, prevState) {
    if (!this.state.hit || (prevState.hit === this.state.hit && prevState.from === this.state.from)) return;
    const target = (this.state.from === "mark" ? "card-" : "mark-") + this.state.hit;
    const el = document.getElementById(target);
    if (el && el.scrollIntoView) el.scrollIntoView({ block: "center", behavior: "smooth" });
  }
  renderVals() {
    const h = this.state.hit;
    const cls = (n) => (h === n ? "hit" : "");
    const go = (n, from) => () => this.setState({ hit: n, from });
    return {
      h1: cls(1), h2: cls(2), h3: cls(3),
      jm1: go(1, "mark"), jm2: go(2, "mark"), jm3: go(3, "mark"),
      jc1: go(1, "card"), jc2: go(2, "card"), jc3: go(3, "card"),
    };
  }"""

def feedback(S, L):
    raw_html = marks_html(S["raw"], {1: (1, "good"), 2: (2, "ask"), 3: (3, "todo")})
    footer = f'<p class="cap" style="padding:0 4px 8px">{S["f_footer"]}</p>' if S["f_footer"] else ""
    body = header(S, "04-Feedback", S["lo_fb7"], crumb=S["a_crumb"], back_href=fn("Main",L),
                  right_extra=f'<span class="chip done" style="height:28px">{ic("check",14,"#1f7a4d",2.6)}{S["f_chip"]}</span>') + f'''
<div class="body" style="display:flex;flex-direction:column;gap:16px;overflow:hidden">
  <div style="display:flex;align-items:center;justify-content:space-between;gap:16px;flex:0 0 auto">
    <div style="display:flex;flex-direction:column;gap:2px;min-width:0">
      <h2 class="h4" style="font-size:20px;line-height:28px;font-weight:700">{S["a_h"]}</h2>
      <p class="b2 muted">{S["f_meta"]}</p>
      {("<p class=cap>" + S["f_decl_echo"] + "</p>") if DECL else ""}
    </div>
    <div style="display:flex;flex-direction:column;align-items:flex-end;gap:6px">
      <div style="display:flex;gap:12px">
        <button class="btn neutral">{ic("download",18)}{S["f_save"]}</button>
        <a class="btn primary" href="{fn("06-Resubmit",L)}">{S["f_resubmit"]}{ic("right",18,"#fff",2.4)}</a>
      </div>
      <span class="cap">{S["f_resub_due"]}</span>
    </div>
  </div>
  <div style="display:flex;gap:16px;flex:1 1 auto;min-height:0">
    <section class="pane" style="flex:1.1 1 0">
      <div class="pane-h">
        <div class="row" style="gap:10px">{ic("filetext",18,"#404564")}<span class="b2" style="font-weight:700">{S["a_file"]}</span></div>
      </div>
      <div class="pane-b">
        <h3 style="font-size:18px;line-height:28px;font-weight:700;margin:0 0 4px;text-align:center">{S["f_raw_title"]}</h3>
        <p class="cap" style="text-align:center;margin-bottom:20px">{S["f_raw_meta"]}</p>
        {raw_html}
      </div>
    </section>
    <section class="pane" style="flex:0.9 1 0;background:transparent;box-shadow:none;overflow:visible">
      <div class="pane-b" style="padding:0;display:flex;flex-direction:column;gap:12px">
        <div class="fb-card" style="background:#eef1ff;border-color:#dfe4ff;flex-direction:row;gap:14px;align-items:flex-start">
          <span class="tav" style="background:#fff">{ic("person",20)}</span>
          <div style="display:flex;flex-direction:column;gap:6px;flex:1 1 auto">
            <p class="sub1" style="font-size:14px;line-height:18px">{S["f_tnote_h"]}</p>
            <p class="b2" style="line-height:22px">{S["f_tnote"]}</p>
          </div>
        </div>
        <div class="fb-card">
          <span class="badge sum">{S["f_sum"]}</span>
          <p class="fbody">{S["f_sum_body"]}</p>
        </div>
        {feedback_cards(S, S["cards"])}
        {footer}
      </div>
    </section>
  </div>
</div>'''
    return page(S, S["titles"]["fb"], body, HIT_LOGIC)

def resubmit(S, L):
    prev = ""
    for i, (kind, crit, quote, body, ref) in enumerate(S["cards"]):
        n = i + 1
        if kind == "good":
            prev += f'''<div class="chk" style="cursor:default"><span class="st" style="width:22px;height:22px;border-radius:50%;background:#e6f5ee;color:#1f7a4d;display:flex;align-items:center;justify-content:center;flex:0 0 22px;margin-top:1px">{ic("check",13,"currentColor",3)}</span>
        <div class="tt"><b><i class="n" style="display:inline-flex;width:18px;height:18px;border-radius:50%;background:#1f7a4d;color:#fff;font-size:11px;font-style:normal;align-items:center;justify-content:center;vertical-align:middle;margin:-2px 6px 0 0">{n}</i>{S["labels"][kind]} {S["sep"]} {crit}</b><span class="cap">{S["r_keep"]}</span></div></div>'''
        else:
            prev += f'''<button class="chk {{{{k{n}}}}}" onClick="{{{{tk{n}}}}}"><span class="box">{ic("check",13,"#fff",3)}</span>
        <div class="tt"><b><i class="n" style="display:inline-flex;width:18px;height:18px;border-radius:50%;background:{"#395ad2" if kind=="ask" else "#d13842"};color:#fff;font-size:11px;font-style:normal;align-items:center;justify-content:center;vertical-align:middle;margin:-2px 6px 0 0">{n}</i>{S["labels"][kind]} {S["sep"]} {crit}</b><span class="cap">{quote}</span></div></button>'''
    selfchips = "".join(f'<button class="chip pick {{{{s{i}}}}}" onClick="{{{{ts{i}}}}}">{lbl}</button>' for i, lbl in enumerate(S["r_self"]))
    body = header(S, "06-Resubmit", S["r_title"], crumb=S["a_crumb"], back_href=fn("04-Feedback",L),
                  right_extra=f'<span class="chip wait" style="height:28px">{ic("refresh",14)}{S["r_h"]} {S["sep"]} {S["r_due"]}</span>') + f'''
<div class="body" style="display:flex;gap:16px;overflow:hidden">
  <section class="pane" style="flex:0.95 1 0">
    <div class="pane-h"><p class="sub1">{S["r_prev_h"]}</p><span class="cap">{S["r_prev_sub"]}</span></div>
    <div class="pane-b" style="display:flex;flex-direction:column;gap:12px">
      <div>{prev}</div>
      <div class="fb-card" style="background:#eef1ff;border-color:#dfe4ff;flex-direction:row;gap:14px;align-items:flex-start">
        <span class="tav" style="background:#fff">{ic("person",20)}</span>
        <p class="b2" style="line-height:22px">{S["f_tnote"]}</p>
      </div>
    </div>
  </section>
  <section style="flex:1.05 1 0;min-height:0;overflow:auto;display:flex;flex-direction:column;gap:16px">
    <div class="card" style="padding:24px;display:flex;flex-direction:column;gap:16px">
      <div style="display:flex;align-items:center;justify-content:space-between">
        <p class="sub1">{S["a_upload_h"]}</p>
        <span class="cap">{S["a_upload_meta"]}</span>
      </div>
      {upload_block(S, S["r_submit"], S["r_file"], S["r_file_meta"], S["r_note"], fn("07-Pending2",L))}
    </div>
    {precheck_block(S)}
    {decl_block(S)}
    <div class="card" style="padding:16px 24px">
      {submit_row(S, S["r_submit"], S["r_note"], fn("07-Pending2",L))}
    </div>
    <div style="height:4px"></div>
  </section>
</div>'''
    logic = """state = { picked: "", k2: false, k3: false, s0: true, s1: false, d0: false, d1: false, d2: false, d3: false };
  renderVals() {
    return {
      picked: this.state.picked !== "",
      empty: this.state.picked === "",
      pickedFile: this.state.picked === "file",
      pickedPhotos: this.state.picked === "photos",
      pick: () => this.setState({ picked: "file" }),
      pickPhotos: () => this.setState({ picked: "photos" }),
      clear: () => this.setState({ picked: "" }),
      k2: this.state.k2 ? "on" : "", k3: this.state.k3 ? "on" : "",
      tk2: () => this.setState({ k2: !this.state.k2 }),
      tk3: () => this.setState({ k3: !this.state.k3 }),
      s0: this.state.s0 ? "sel" : "", s1: this.state.s1 ? "sel" : "",
      ts0: () => this.setState({ s0: true, s1: false }),
      ts1: () => this.setState({ s0: false, s1: true }),""" + DECL_LOGIC + """
    };
  }"""
    return page(S, S["titles"]["resub"], body, logic)

def feedback2(S, L):
    raw_html = marks_html(S["raw2"], {2: (1, "good"), 3: (2, "good"), 0: (3, "todo")})
    footer = f'<p class="cap" style="padding:0 4px 8px">{S["f2_footer"]}</p>' if S["f2_footer"] else ""
    chg = ""
    for st, txt in S["f2_chg"]:
        icon = ic("check",13,"currentColor",3) if st == "done" else ic("alert",13,"currentColor",2.4)
        chg += f'<div class="chg {st}"><span class="st">{icon}</span><span>{txt}</span></div>'
    body = header(S, "08-Feedback2", S["lo_fb7"], crumb=S["a_crumb"], back_href=fn("Main",L),
                  right_extra=f'<span class="chip done" style="height:28px">{ic("check",14,"#1f7a4d",2.6)}{S["f2_chip"]}</span>') + f'''
<div class="body" style="display:flex;flex-direction:column;gap:16px;overflow:hidden">
  <div style="display:flex;align-items:center;justify-content:space-between;gap:16px;flex:0 0 auto">
    <div style="display:flex;flex-direction:column;gap:2px;min-width:0">
      <h2 class="h4" style="font-size:20px;line-height:28px;font-weight:700">{S["a_h"]}</h2>
      <p class="b2 muted">{S["f2_meta"]}</p>
    </div>
    <div style="display:flex;gap:12px">
      <button class="btn primary">{ic("download",18)}{S["f_save"]}</button>
    </div>
  </div>
  <div style="display:flex;gap:16px;flex:1 1 auto;min-height:0">
    <section class="pane" style="flex:1.1 1 0">
      <div class="pane-h">
        <div class="row" style="gap:10px">{ic("filetext",18,"#404564")}<span class="b2" style="font-weight:700">{S["r_file"]}</span></div>
      </div>
      <div class="pane-b">
        <h3 style="font-size:18px;line-height:28px;font-weight:700;margin:0 0 4px;text-align:center">{S["f_raw_title"]}</h3>
        <p class="cap" style="text-align:center;margin-bottom:20px">{S["f2_raw_meta"]}</p>
        {raw_html}
      </div>
    </section>
    <section class="pane" style="flex:0.9 1 0;background:transparent;box-shadow:none;overflow:visible">
      <div class="pane-b" style="padding:0;display:flex;flex-direction:column;gap:12px">
        <div class="fb-card">
          <div style="display:flex;align-items:center;justify-content:space-between"><p class="sub1" style="font-size:14px;line-height:18px">{S["f2_chg_h"]}</p></div>
          {chg}
          <p class="cap" style="display:flex;align-items:center;gap:6px">{ic("check",12,"#1f7a4d",3)}{S["f2_own"]}</p>
        </div>
        <div class="fb-card" style="background:#eef1ff;border-color:#dfe4ff;flex-direction:row;gap:14px;align-items:flex-start">
          <span class="tav" style="background:#fff">{ic("person",20)}</span>
          <div style="display:flex;flex-direction:column;gap:6px;flex:1 1 auto">
            <p class="sub1" style="font-size:14px;line-height:18px">{S["f_tnote_h"]}</p>
            <p class="b2" style="line-height:22px">{S["f2_tnote"]}</p>
          </div>
        </div>
        <div class="fb-card">
          <span class="badge sum">{S["f_sum"]}</span>
          <p class="fbody">{S["f2_sum_body"]}</p>
        </div>
        {feedback_cards(S, S["cards2"])}
        {footer}
      </div>
    </section>
  </div>
</div>'''
    return page(S, S["titles"]["fb2"], body, HIT_LOGIC)

def todo(S, L):
    sep = " ・ " if L == "ja" else " · "
    def trow(icon, title, course_, chip, href=None, sparkle=False, done=False, off=False, when=""):
        return lo_row(icon, title, f'{course_}{(sep + when) if when else ""}', chip=chip, href=href, sparkle=sparkle, done=done, off=off)
    body = header(S, "05-Todo", S["todo"], crumb=S["crumb_study"]) + f'''
<div class="body"><div class="col">
  <div style="display:flex;align-items:center;justify-content:space-between">
    <p class="sub1">{S["t_week"]}</p>
    <span class="cap">{S["t_week_cap"]}</span>
  </div>
  {trow("filetext", S["lo_fb7"], S["course"], f'<span class="chip wait">{ic("refresh",12)}{S["t_fb7_chip"]}</span>', href=fn("04-Feedback",L), sparkle=True, when=S["t_fb7_when"])}
  {trow("message", S["t_ref7"], S["course"], f'<span class="chip review">{S["p_chip"]}</span>', sparkle=True, when=S["t_ref7_when"])}
  {trow("sparkle", S["t_sim"], S["t_sim_course"], f'<span class="chip wait">{S["t_sim_chip"]}</span>', sparkle=True)}
  {trow("play", S["t_video"], S["course"], f'<span class="chip done">{S["t_done"]}</span>', done=True)}
  {sect(f'<span style="color:#d13842">{S["t_late_h"]}</span>')}
  {trow("filetext", S["t_late"], S["course"], f'<span class="chip late">{S["t_late_chip"]}</span>', sparkle=True, href=fn("02-Assignment",L))}
  {sect(S["t_up_h"], f'<span class="cap">{S["t_up_cap"]}</span>', muted=True)}
  {trow("filetext", S["lo_fb8"], S["course"], f'<span class="chip pre">{S["t_fb8_chip"]}</span>', sparkle=True, off=True)}
  <div style="height:8px"></div>
</div></div>'''
    return page(S, S["titles"]["todo"], body)

BUILDERS = {"Main": course, "02-Assignment": assignment, "03-Pending": lambda S, L: pending(S, L, 1), "04-Feedback": feedback,
            "06-Resubmit": resubmit, "07-Pending2": lambda S, L: pending(S, L, 2), "08-Feedback2": feedback2, "05-Todo": todo}

# ======================= MOBILE (375 x 812) =======================
import random

def paper_svg():
    """A drawn stand-in for a photographed handwritten answer sheet (no image assets available offline)."""
    r = random.Random(7)
    parts = ['<rect width="210" height="297" fill="#fdfdfb"/>']
    for y in range(34, 290, 9):
        parts.append(f'<line x1="14" y1="{y}" x2="196" y2="{y}" stroke="#dcdfe9" stroke-width=".5"/>')
    def squig(x0, y, x1, amp=1.6, step=4.5):
        d = f"M{x0} {y}"
        x = x0
        while x < x1:
            cx = x + step / 2; cy = y + r.uniform(-amp, amp)
            x2 = min(x + step, x1); y2 = y + r.uniform(-amp * .6, amp * .6)
            d += f" Q{cx:.1f} {cy:.1f} {x2:.1f} {y2:.1f}"
            x = x2
        return d
    parts.append(f'<path d="{squig(40, 24, 168, 2.2, 6)}" fill="none" stroke="#2f3550" stroke-width="1.7" stroke-linecap="round"/>')
    ys = list(range(43, 130, 9)) + list(range(205, 286, 9))
    for i, y in enumerate(ys):
        x1 = (196 - r.uniform(0, 40)) if i % 5 != 4 else (90 + r.uniform(0, 30))
        parts.append(f'<path d="{squig(16, y - 3, x1)}" fill="none" stroke="#2f3550" stroke-width="1.1" stroke-linecap="round"/>')
    parts.append('<rect x="40" y="136" width="130" height="62" fill="none" stroke="#2f3550" stroke-width="1"/>')
    parts.append('<line x1="48" y1="192" x2="164" y2="192" stroke="#2f3550" stroke-width="1"/><line x1="48" y1="142" x2="48" y2="192" stroke="#2f3550" stroke-width="1"/>')
    for k in range(14):
        x = 52 + k * 7.5 + r.uniform(-2, 2); yv = 188 - k * 2.6 + r.uniform(-7, 7)
        parts.append(f'<circle cx="{x:.1f}" cy="{yv:.1f}" r="1.6" fill="#395ad2"/>')
    parts.append('<circle cx="158" cy="147" r="2.2" fill="#d13842"/>')
    parts.append('<line x1="52" y1="186" x2="160" y2="156" stroke="#2f3550" stroke-width=".8" stroke-dasharray="2 2"/>')
    return f'<svg viewBox="0 0 210 297" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">{"".join(parts)}</svg>'
PAPER = paper_svg()

def paper(w, h, left, top, rot=-3, box=(375, 812)):
    """Placed as a share of its box, so the same markup holds at any viewport size."""
    bw, bh = box
    return (f'<div class="paper" style="left:{left / bw:.2%};top:{top / bh:.2%};'
            f'width:{w / bw:.2%};height:{h / bh:.2%};transform:rotate({rot}deg)">{PAPER}</div>')

def paper_inline(w, h, shadow=True):
    sh = "" if shadow else "box-shadow:none;"
    return f'<span class="paper" style="position:static;display:block;width:{w}px;height:{h}px;{sh}flex:0 0 {w}px">{PAPER}</span>'

def status_bar(dark=False):
    c = "#fff" if dark else "#000"
    return f'''<div class="sb" style="color:{c}"><span>9:41</span><span class="si">
      <svg width="18" height="12" viewBox="0 0 18 12" fill="{c}" aria-hidden="true"><rect x="0" y="8" width="3" height="4" rx=".8"/><rect x="5" y="5.5" width="3" height="6.5" rx=".8"/><rect x="10" y="3" width="3" height="9" rx=".8"/><rect x="15" y="0" width="3" height="12" rx=".8"/></svg>
      <svg width="16" height="12" viewBox="0 0 16 12" fill="none" stroke="{c}" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M1.5 4.2a9.5 9.5 0 0 1 13 0M4 7a6 6 0 0 1 8 0M6.5 9.7a2.5 2.5 0 0 1 3 0"/></svg>
      <svg width="27" height="13" viewBox="0 0 27 13" fill="none" aria-hidden="true"><rect x=".5" y=".5" width="23" height="12" rx="3" stroke="{c}" opacity=".5"/><rect x="2" y="2" width="18" height="9" rx="1.6" fill="{c}"/><path d="M25.5 4.5v4" stroke="{c}" opacity=".5" stroke-width="1.4" stroke-linecap="round"/></svg>
    </span></div>'''

def mlang(S, screen):
    ja_on = S["lang"] == "ja"
    ja = f'<span class="seg-i on">{S["m_lang_ja"]}</span>' if ja_on else f'<a class="seg-i" href="{fn(screen,"ja")}" lang="ja">{S["m_lang_ja"]}</a>'
    en = f'<span class="seg-i on">{S["m_lang_en"]}</span>' if not ja_on else f'<a class="seg-i" href="{fn(screen,"en")}" lang="en">{S["m_lang_en"]}</a>'
    return f'<div class="mseg" role="group" aria-label="{S["lang_aria"]}">{ja}{en}</div>'

def mheader(S, screen, title, back_href=None, right=""):
    left = (f'<a class="mib" href="{back_href}" aria-label="{S["m_back"]}">{ic("left",28)}</a>' if back_href
            else f'<button class="mib" aria-label="{S["m_back"]}">{ic("left",28)}</button>')
    return f'<header class="mhdr">{left}<h1 class="mt">{title}</h1>{right}{mlang(S, screen)}</header>'

def mnav(S, active=0):
    icons = ["book", "message", "calendar"]
    items = "".join(f'<span class="ni{" on" if i == active else ""}">{ic(icons[i],28,"currentColor",1.8)}{lbl}</span>' for i, lbl in enumerate(S["m_nav"]))
    return f'<nav class="mnav">{items}</nav>'

def mpage(S, screen, title, body, logic="renderVals(){ return {}; }", dark=False, over_nav=False):
    return f'''<!doctype html>
<html lang="{S["lang"]}">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
{HELMET}
<div class="mroot{" dark" if dark else ""}" style="width: 375px; height: 812px;">
{status_bar(dark)}
{body}
{device_toggle(S, screen, mobile=True, over_nav=over_nav)}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":375,"height":812}}}}'>
class Component extends DCLogic {{
  {logic}
}}
</script>
</body>
</html>
'''

def m_main(S, L):
    fbchip = lt(S["lt_fb"], True) + f'<span class="chip wait">{S["chip_notsub"]}</span>'
    body = mheader(S, "M-Main", S["t71"]) + f'''
<div class="mbody nav">
  <p class="cap" style="margin:-4px 0 -8px">{S["m_crumb"]}</p>
  <div class="banner">{ic("check",24,"#fff",2.6)}<b>{S["m_banner_n"]}</b><span>{S["m_banner_l"]}</span></div>
  {lo_row("play", S["lo_video"], S["lo_video_s"], chip=lt(S["lt_video"]), done=True)}
  {lo_row("filetext", S["lo_pdf"], S["lo_pdf_s"], chip=lt(S["lt_doc"]), done=True)}
  {lo_row("table", S["lo_xlsx"], S["lo_xlsx_s"], chip=lt(S["lt_file"]), done=True)}
  {lo_row("filetext", S["lo_fb7_name"], S["lo_fb_s"], chip=fbchip, href=fn("M-Assignment",L), sparkle=True)}
</div>
{mnav(S, 0)}'''
    return mpage(S, "M-Main", S["m_titles"]["main"], body, over_nav=True)

def m_assignment(S, L):
    crit = "".join(f'<span class="chip neutral">{c}</span>' for c in S["criteria"])
    pcs = "".join(f'<div class="pc pend"><span class="st">{ic("minus",14,"currentColor",3)}</span><div class="tt muted">{label}</div></div>' for _, label, _ in S["pc_items"])
    body = mheader(S, "M-Assignment", S["lo_fb7_name"], back_href=fn("M-Main",L)) + f'''
<div class="mbody">
  <div class="mcard">
    <div style="display:flex;flex-direction:column;gap:6px">
      <h2 class="mh">{S["a_h"]}</h2>
      <p class="cap">{S["a_meta"]}</p>
      <span class="chip wait" style="align-self:flex-start">{ic("clock",14)}{S["a_due"]}</span>
    </div>
    <p class="b2" style="line-height:22px">{S["a_desc"]}</p>
    <div class="divider"></div>
    <p class="sub1" style="font-size:14px">{S["a_crit_h"]}</p>
    <div class="crit">{crit}</div>
  </div>
  <div class="mcard">
    <p class="sub1" style="font-size:14px">{S["a_upload_h"]}</p>
    <a class="opt pri" href="{fn("M-Camera",L)}"><span class="oi">{ic("camera",24)}</span><span class="ot"><b>{S["m_opt_cam"]}</b><span>{S["m_opt_cam_s"]}</span></span>{ic("right",20,"#395ad2",2.4)}</a>
    <a class="opt" href="{fn("M-File",L)}"><span class="oi">{ic("upload",24)}</span><span class="ot"><b>{S["m_opt_file"]}</b><span>{S["m_opt_file_s"]}</span></span>{ic("right",20,"#c7c7cc",2.4)}</a>
    <a class="opt" href="{fn("M-Type",L)}"><span class="oi">{ic("filetext",24)}</span><span class="ot"><b>{S["m_opt_text"]}</b><span>{S["m_opt_text_s"]}</span></span>{ic("right",20,"#c7c7cc",2.4)}</a>
    <p class="cap">{S["a_note"]}</p>
  </div>
  <div class="mcard" style="gap:4px">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px;gap:8px"><p class="sub1" style="font-size:14px">{S["pc_h"]}</p><span class="cap">{S["pc_note"]}</span></div>
    {pcs}
  </div>
</div>'''
    return mpage(S, "M-Assignment", S["m_titles"]["assign"], body)

def m_camera(S, L):
    body = f'''
<div class="desk"></div>
{paper(250, 340, 62, 215, -3)}
<div class="cam-scrim"></div>
<div class="ctop"><a class="cbtn" href="{fn("M-Assignment",L)}" aria-label="{S["m_close"]}">{ic("x",22)}</a><span class="t">{S["m_cam_title"]}</span><span class="cpill">{ic("filetext",14)}{S["m_cam_page"]}</span></div>
<div class="guide" style="left:9.07%;top:21.92%;width:81.87%;height:51.48%"><i class="tl"></i><i class="tr"></i><i class="bl"></i><i class="br"></i></div>
<p class="chint">{S["m_cam_hint"]}</p>
<div class="shutter-row">
  <button class="gbtn l" aria-label="{S["m_cam_gallery"]}">{ic("image",22)}</button>
  <a class="shutter" href="{fn("M-Crop",L)}" aria-label="{S["m_cam_shutter"]}">{ic("camera",30,"#fff",2)}</a>
  <button class="gbtn r" aria-label="{S["m_cam_flash"]}">{ic("flash",22)}</button>
</div>'''
    return mpage(S, "M-Camera", S["m_titles"]["cam"], body, dark=True)

# The band is a share of the photo box, so it holds at any viewport size.
CROP_LOGIC = """state = { fit: false };
  renderVals() {
    const W = 343, H = 452;
    const r = this.state.fit ? { l: 48, t: 62, w: 247, h: 328 } : { l: 26, t: 30, w: 291, h: 392 };
    const x = (v) => (100 * v / W).toFixed(3) + "%";
    const y = (v) => (100 * v / H).toFixed(3) + "%";
    return {
      fitOn: this.state.fit ? "on" : "",
      toggle: () => this.setState({ fit: !this.state.fit }),
      bl: x(r.l), bt: y(r.t), bw: x(r.w), bh: y(r.h),
      vt: y(r.t), vb: y(H - r.t - r.h), vl: x(r.l), vr: x(W - r.l - r.w),
    };
  }"""

def m_crop(S, L):
    body = f'''
<div class="ctop flow"><a class="cbtn" href="{fn("M-Camera",L)}" aria-label="{S["m_close"]}">{ic("x",22)}</a><span class="t">{S["m_crop_title"]}</span><span class="cpill">{S["m_cam_page"]}</span></div>
<div class="photo">
  <div class="desk"></div>
  {paper(230, 315, 56, 68, -3, box=(343, 452))}
  <div class="veil" style="left:0;right:0;top:0;height:{{{{vt}}}}"></div>
  <div class="veil" style="left:0;right:0;bottom:0;height:{{{{vb}}}}"></div>
  <div class="veil" style="left:0;top:{{{{vt}}}};height:{{{{bh}}}};width:{{{{vl}}}}"></div>
  <div class="veil" style="right:0;top:{{{{vt}}}};height:{{{{bh}}}};width:{{{{vr}}}}"></div>
  <div class="band" style="left:{{{{bl}}}};top:{{{{bt}}}};width:{{{{bw}}}};height:{{{{bh}}}}"><span class="hd tl"></span><span class="hd tr"></span><span class="hd bl"></span><span class="hd br"></span></div>
</div>
<div class="cctl">
  <p class="crop-cap">{S["m_crop_cap"]}</p>
  <div class="ctools">
    <button class="tool {{{{fitOn}}}}" onClick="{{{{toggle}}}}">{ic("scan",15)}{S["m_crop_auto"]}</button>
    <button class="tool">{ic("rotate",15)}{S["m_crop_rotate"]}</button>
    <a class="tool" href="{fn("M-Camera",L)}">{ic("camera",15)}{S["m_crop_retake"]}</a>
  </div>
  <p class="cnote">{S["m_crop_note"]}</p>
  <div class="thumbs">
    <span class="thumb-w"><span class="thumb on"><span class="no">1</span>{paper_inline(40, 52, False)}</span>{S["m_cam_page"]}</span>
    <span class="thumb-w"><a class="thumb add" href="{fn("M-Camera",L)}" aria-label="{S["m_add_page"]}">{ic("plus",24)}</a>{S["m_add_page"]}</span>
  </div>
  <a class="crop-next" href="{fn("M-Pages",L)}">{S["m_next"]}{ic("right",18,"#fff",2.4)}</a>
</div>'''
    return mpage(S, "M-Crop", S["m_titles"]["crop"], body, logic=CROP_LOGIC, dark=True)

def m_submit_row(S, href):
    """Disabled until something is picked or confirmed, then the real submit."""
    return f'''<sc-if value="{{{{empty}}}}" hint-placeholder-val="{{{{true}}}}">
    <span class="mbtn dis">{ic("sparkle",18,"rgba(28,30,44,.38)")}{S["a_submit"]}</span>
  </sc-if>
  <sc-if value="{{{{picked}}}}" hint-placeholder-val="{{{{false}}}}">
    <a class="mbtn primary" href="{href}">{ic("sparkle",18,"#fff")}{S["a_submit"]}</a>
  </sc-if>
  <p class="cap" style="text-align:center">{S["a_note"]}</p>'''

def m_file(S, L):
    """The file / photos path on the phone: same upload block and checks as PC."""
    body = mheader(S, "M-File", S["m_file_title"], back_href=fn("M-Assignment",L)) + f'''
<div class="mbody">
  <div class="mcard">
    <p class="sub1" style="font-size:14px">{S["a_upload_h"]}</p>
    <p class="cap">{S["a_upload_meta"]}</p>
    {upload_block(S, S["a_submit"], S["a_file"], S["a_file_meta"], S["a_note"], fn("M-Pending",L))}
  </div>
  {precheck_block(S)}
  {m_submit_row(S, fn("M-Pending",L))}
  <div style="height:8px"></div>
</div>'''
    logic = """state = { picked: "" };
  renderVals() {
    return {
      picked: this.state.picked !== "",
      empty: this.state.picked === "",
      pickedFile: this.state.picked === "file",
      pickedPhotos: this.state.picked === "photos",
      pick: () => this.setState({ picked: "file" }),
      pickPhotos: () => this.setState({ picked: "photos" }),
      clear: () => this.setState({ picked: "" }),
    };
  }"""
    return mpage(S, "M-File", S["m_titles"]["file"], body, logic=logic)

def m_type(S, L):
    """The typed-answer path on the phone: 500-character limit, confirm, then the checks."""
    body = mheader(S, "M-Type", S["m_type_title"], back_href=fn("M-Assignment",L)) + f'''
<div class="mbody">
  <div class="mcard">
    <p class="sub1" style="font-size:14px">{S["a_upload_h"]}</p>
    <sc-if value="{{{{isTyping}}}}" hint-placeholder-val="{{{{true}}}}">
      <label class="cap" for="ta-answer" style="display:none">{S["m_type_title"]}</label>
      <textarea id="ta-answer" class="ta" style="min-height:220px" placeholder="{S["a_ta_ph"]}" maxlength="500" defaultValue="{{{{ttext}}}}" onInput="{{{{onType}}}}"></textarea>
      <div style="display:flex;align-items:center;justify-content:space-between;gap:12px">
        <span class="cap">{S["a_ta_note"]}</span>
        <span class="cap" style="white-space:nowrap;font-weight:700">{{{{tcount}}}} / 500 {S["a_ta_unit"]}</span>
      </div>
      <sc-if value="{{{{noText}}}}" hint-placeholder-val="{{{{true}}}}"><span class="mbtn dis">{ic("check",18,"rgba(28,30,44,.38)")}{S["a_ta_confirm"]}</span></sc-if>
      <sc-if value="{{{{hasText}}}}" hint-placeholder-val="{{{{false}}}}"><button class="mbtn neutral" onClick="{{{{confirm}}}}">{ic("check",18)}{S["a_ta_confirm"]}</button></sc-if>
    </sc-if>
    <sc-if value="{{{{isConfirmed}}}}" hint-placeholder-val="{{{{false}}}}">
      <div class="filerow" style="align-items:flex-start">
        <span class="ficon" style="background:#eef1ff;color:#395ad2">{ic("filetext",22)}</span>
        <div style="flex:1 1 auto;min-width:0;display:flex;flex-direction:column;gap:6px">
          <p class="b2" style="font-weight:700;display:flex;align-items:center;gap:6px">{ic("check",14,"#1f7a4d",3)}{S["a_ta_confirmed"]} {S["sep"]} {{{{tcount}}}} {S["a_ta_unit"]}</p>
          <p class="b2 muted" style="white-space:pre-wrap;max-height:110px;overflow:hidden">{{{{ttext}}}}</p>
        </div>
      </div>
      <button class="mbtn neutral" onClick="{{{{edit}}}}">{S["a_ta_edit"]}</button>
    </sc-if>
  </div>
  {precheck_block(S)}
  {m_submit_row(S, fn("M-Pending",L))}
  <div style="height:8px"></div>
</div>'''
    logic = """state = { tlen: 0, ttext: "", confirmed: false };
  renderVals() {
    return {
      picked: this.state.confirmed,
      empty: !this.state.confirmed,
      isTyping: !this.state.confirmed,
      isConfirmed: this.state.confirmed,
      noText: this.state.tlen === 0, hasText: this.state.tlen > 0,
      onType: (e) => { const v = e.target.value || ""; this.setState({ tlen: v.length, ttext: v }); },
      confirm: () => this.setState({ confirmed: true }),
      edit: () => this.setState({ confirmed: false }),
      ttext: this.state.ttext,
      tcount: String(this.state.tlen),
    };
  }"""
    return mpage(S, "M-Type", S["m_titles"]["type"], body, logic=logic)

def m_pages(S, L):
    items = ""
    for st, label, note in S["pc_items"][:-1]:
        icon = ic("check",14,"currentColor",3) if st == "ok" else ic("alert",14,"currentColor",2.4)
        items += f'<div class="pc {st}"><span class="st">{icon}</span><div class="tt"><b>{label}</b>{("<br><span class=cap>" + note + "</span>") if note else ""}</div></div>'
    items += f'<div class="pc ok"><span class="st">{ic("check",14,"currentColor",3)}</span><div class="tt"><b>{S["m_pc_pages"]}</b></div></div>'
    body = mheader(S, "M-Pages", S["m_pages_title"], back_href=fn("M-Crop",L)) + f'''
<div class="mbody">
  <div class="mcard" style="gap:10px">
    <div class="pstrip">
      <button class="pth on"><span class="no">1</span>{paper_inline(56, 74, False)}</button>
      <button class="pth"><span class="no">2</span>{paper_inline(56, 74, False)}</button>
      <a class="pth add" href="{fn("M-Camera",L)}" aria-label="{S["m_add_page"]}">{ic("plus",24)}</a>
    </div>
    <p class="cap" style="display:flex;align-items:center;gap:6px">{ic("grip",14)}{S["m_pages_hint"]}</p>
    <div class="preview">{paper_inline(200, 275)}<span class="pg">{S["m_pages_count"]}</span></div>
  </div>
  <div class="mcard" style="gap:4px">
    <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:4px;gap:8px"><p class="sub1" style="font-size:14px">{S["pc_h"]}</p><span class="cap">{S["pc_note"]}</span></div>
    {items}
  </div>
  <a class="mbtn primary" href="{fn("M-Pending",L)}">{ic("sparkle",18,"#fff")}{S["a_submit"]}</a>
  <p class="cap" style="text-align:center">{S["a_note"]}</p>
</div>'''
    return mpage(S, "M-Pages", S["m_titles"]["pages"], body)

def m_pending(S, L):
    (l1, s1), (l2, s2), (l3, s3) = S["p_steps"]
    teacher_body = S["p_teacher_body"].replace("{due}", S["p_due1"])
    body = mheader(S, "M-Pending", S["lo_fb7_name"], back_href=fn("M-Main",L)) + f'''
<div class="mbody">
  <div class="mcard" style="align-items:center;text-align:center;gap:8px;padding:24px 16px">
    <span style="width:56px;height:56px;border-radius:50%;background:#e6f5ee;display:flex;align-items:center;justify-content:center;color:#1f7a4d">{ic("check",28,"#1f7a4d",2.6)}</span>
    <h2 class="mh">{S["p_h"]}</h2>
    <p class="cap">{S["p_received"]}</p>
    <span class="chip review">{ic("clock",14)}{S["p_chip"]}</span>
  </div>
  <div class="mcard">
    <div class="vsteps">
      <div class="vstep done"><span class="line"></span><span class="dot">{ic("check",14,"#fff",3)}</span><span class="tt"><b>{l1}</b><span>{s1}</span></span></div>
      <div class="vstep cur"><span class="line"></span><span class="dot">2</span><span class="tt"><b>{l2}</b><span>{s2}</span></span></div>
      <div class="vstep"><span class="line"></span><span class="dot">3</span><span class="tt"><b>{l3}</b><span>{s3}</span></span></div>
    </div>
    <div class="divider"></div>
    <div style="display:flex;align-items:center;gap:8px">{ic("bell",16,"#395ad2")}<span class="b2" style="font-weight:500">{S["p_expect"]}</span></div>
  </div>
  <div class="mcard" style="flex-direction:row;gap:12px;align-items:flex-start">
    <span class="tav">{ic("person",20)}</span>
    <div style="display:flex;flex-direction:column;gap:6px;flex:1 1 auto;min-width:0"><p class="sub1" style="font-size:14px">{S["p_teacher_h"]}</p><p class="b2" style="line-height:22px">{teacher_body}</p></div>
  </div>
  <div class="mcard">
    <p class="sub1" style="font-size:14px">{S["p_sub_h"]}</p>
    <div style="display:flex;gap:12px;align-items:center">
      <div style="display:flex;gap:6px">{paper_inline(40, 52, False)}{paper_inline(40, 52, False)}</div>
      <div style="flex:1 1 auto;min-width:0;display:flex;flex-direction:column;gap:2px"><p class="b2" style="font-weight:700">{S["lo_fb7_name"]}</p><p class="cap">{S["m_pending_pages"]}</p></div>
    </div>
    <div style="display:flex;gap:8px">
      <button class="mbtn neutral" style="flex:1 1 0">{ic("eye",18)}{S["p_view"]}</button>
      <a class="mbtn neutral" style="flex:1 1 0" href="{fn("M-Assignment",L)}">{ic("refresh",18)}{S["m_pending_replace"]}</a>
    </div>
    <p class="cap">{S["p_replace_note"]}</p>
  </div>
  <div style="height:40px"></div>
</div>
<a class="demo" style="right:12px;bottom:14px;padding:8px 10px 8px 12px" href="{fn("M-Feedback",L)}" aria-label="{S["p_demo"]}"><span class="tag">DEMO</span>{ic("right",16,"#fff",2.4)}</a>'''
    return mpage(S, "M-Pending", S["m_titles"]["pending"], body)

def m_sheet_block(S, n, kind, crit, quote, body, ref):
    return f'''<sc-if value="{{{{s{n}}}}}" hint-placeholder-val="{{{{false}}}}">
      <div style="display:flex;align-items:center;gap:8px;flex-wrap:wrap;padding-right:36px"><span class="badge {kind}"><i class="n">{n}</i>{S["labels"][kind]}</span><span class="ctag">{crit}</span></div>
      <blockquote class="quote {kind}">“{quote}”</blockquote>
      <p class="fbody">{body}</p>
      <span class="ref">{ic("book",14)}{ref}</span>
    </sc-if>'''

def m_feedback(S, L, init=0):
    screen = "M-Feedback" if init == 0 else "M-Sheet"
    raw_html = marks_html(S["raw"], {1: (1, "good"), 2: (2, "ask"), 3: (3, "todo")}).replace('class="raw"', 'class="mraw"')
    sheets = "".join(m_sheet_block(S, i + 1, *c) for i, c in enumerate(S["cards"]))
    pts = "".join(
        f'<button class="pt {{{{h{i+1}}}}}" onClick="{{{{jm{i+1}}}}}"><span class="badge {k}" style="height:20px;padding:0 6px;font-size:11px"><i class="n" style="width:14px;height:14px;font-size:9px">{i+1}</i>{S["labels"][k]}</span>{crit}</button>'
        for i, (k, crit, *_rest) in enumerate(S["cards"]))
    body = mheader(S, screen, S["lo_fb7_name"], back_href=fn("M-Main",L)) + f'''
<div class="mbody">
  <div class="mcard" style="gap:6px">
    <h2 class="mh" style="font-size:16px;line-height:24px">{S["a_h"]}</h2>
    <p class="cap">{S["f_meta"]}</p>
    <span class="chip done" style="align-self:flex-start">{ic("check",14,"#1f7a4d",2.6)}{S["f_chip"]}</span>
  </div>
  <div class="mcard" style="flex-direction:row;gap:12px;align-items:flex-start">
    <span class="tav">{ic("person",20)}</span>
    <div style="display:flex;flex-direction:column;gap:6px;flex:1 1 auto;min-width:0"><p class="sub1" style="font-size:14px">{S["f_tnote_h"]}</p><p class="b2" style="line-height:22px">{S["f_tnote"]}</p></div>
  </div>
  <div class="mcard" style="gap:8px">
    <span class="badge sum">{S["f_sum"]}</span>
    <p class="fbody" style="font-size:14px;line-height:1.8">{S["f_sum_body"]}</p>
  </div>
  <div class="mcard" style="gap:10px">
    <p class="sub1" style="font-size:14px">{S["m_fb_doc_h"]}</p>
    <p class="cap">{S["m_fb_points"]}</p>
    <div class="pts">{pts}</div>
    <div class="divider"></div>
    <h3 style="font-size:15px;line-height:22px;font-weight:700;margin:0;text-align:center">{S["f_raw_title"]}</h3>
    <p class="cap" style="text-align:center;margin-bottom:8px">{S["f_raw_meta"]}</p>
    {raw_html}
  </div>
  <a class="mbtn primary" href="{fn("M-Assignment",L)}">{S["f_resubmit"]}{ic("right",18,"#fff",2.4)}</a>
  <p class="cap" style="text-align:center;margin-top:-8px">{S["f_resub_due"]}</p>
  <button class="mbtn neutral">{ic("download",18)}{S["f_save"]}</button>
  <div style="height:32px"></div>
</div>
<sc-if value="{{{{open}}}}" hint-placeholder-val="{{{{false}}}}">
  <button class="scrim" onClick="{{{{close}}}}" aria-label="{S["m_close"]}"></button>
  <div class="sheet">
    <span class="grab"></span>
    <button class="sx" onClick="{{{{close}}}}" aria-label="{S["m_close"]}">{ic("x",18)}</button>
    {sheets}
    <div class="sheet-nav">
      <button class="snb" onClick="{{{{prev}}}}">{ic("left",16)}{S["m_prev"]}</button>
      <span class="cap">{{{{pos}}}} / 3</span>
      <button class="snb" onClick="{{{{next}}}}">{S["m_next_pt"]}{ic("right",16)}</button>
    </div>
  </div>
</sc-if>'''
    logic = f"""state = {{ sheet: {init} }};
  componentDidUpdate(prevProps, prevState) {{
    const s = this.state.sheet;
    if (!s || prevState.sheet === s) return;
    const el = document.getElementById("mark-" + s);
    if (el && el.scrollIntoView) el.scrollIntoView({{ block: "center", behavior: "smooth" }});
  }}
  renderVals() {{
    const s = this.state.sheet;
    const go = (n) => () => this.setState({{ sheet: n }});
    return {{
      open: s > 0, s1: s === 1, s2: s === 2, s3: s === 3, pos: String(s),
      h1: s === 1 ? "hit" : "", h2: s === 2 ? "hit" : "", h3: s === 3 ? "hit" : "",
      jm1: go(1), jm2: go(2), jm3: go(3),
      close: go(0), prev: go(s > 1 ? s - 1 : 3), next: go(s < 3 ? s + 1 : 1),
    }};
  }}"""
    return mpage(S, screen, S["m_titles"]["fb" if init == 0 else "sheet"], body, logic=logic)

MBUILDERS = {"M-Main": m_main, "M-Assignment": m_assignment, "M-Camera": m_camera, "M-Crop": m_crop, "M-Pages": m_pages,
             "M-File": m_file, "M-Type": m_type,
             "M-Pending": m_pending, "M-Feedback": lambda S, L: m_feedback(S, L, 0), "M-Sheet": lambda S, L: m_feedback(S, L, 2)}

# ======================= TEACHER / BACK OFFICE (1440 x 900) =======================
# Layout, labels and components follow the production Back Office (school-portal-admin,
# syllabus squad): the manabieV5 theme tokens, the Book detail accordion tree, and
# DialogCreateLearningMaterial, whose fields are chosen per LO type. AI Feedback is one
# more LO type in that dialog; its settings are the new part. The nav follows the live
# LMS 2.0 tenant the PM screenshotted, which carries more squads than the syllabus one.

# MUI filled icon paths (24 viewBox), as the Back Office renders them.
MI = {
    "dashboard": "M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z",
    "search": "M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z",
    "aiTutor": "M17 1.01 7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14zm-5-2.5 1.09-2.41L15.5 13l-2.41-1.09L12 9.5l-1.09 2.41L8.5 13l2.41 1.09L12 16.5z",
    "library": "M4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm16-4H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-1 9H9V9h10v2zm-4 4H9v-2h6v2zm4-8H9V5h10v2z",
    "reader": "M13 12h7v1.5h-7zm0-2.5h7V11h-7zm0 5h7V16h-7zM21 4H3c-1.1 0-2 .9-2 2v13c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 15h-9V6h9v13z",
    "people": "M16 11c1.66 0 2.99-1.34 2.99-3S17.66 5 16 5c-1.66 0-3 1.34-3 3s1.34 3 3 3zm-8 0c1.66 0 2.99-1.34 2.99-3S9.66 5 8 5C6.34 5 5 6.34 5 8s1.34 3 3 3zm0 2c-2.33 0-7 1.17-7 3.5V19h14v-2.5c0-2.33-4.67-3.5-7-3.5zm8 0c-.29 0-.62.02-.97.05 1.16.84 1.97 1.97 1.97 3.45V19h6v-2.5c0-2.33-4.67-3.5-7-3.5z",
    "video": "M21 3H3c-1.11 0-2 .89-2 2v12c0 1.1.89 2 2 2h5v2h8v-2h5c1.1 0 1.99-.9 1.99-2L23 5c0-1.11-.9-2-2-2zm0 14H3V5h18v12zm-5-6-7 4V7z",
    "event": "M17 12h-5v5h5v-5zM16 1v2H8V1H6v2H5c-1.11 0-1.99.9-1.99 2L3 19c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2h-1V1h-2zm3 18H5V8h14v11z",
    "bell": "M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z",
    "person": "M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z",
    "more": "M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z",
    "add": "M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z",
    "up": "M4 12l1.41 1.41L11 7.83V20h2V7.83l5.58 5.59L20 12l-8-8-8 8z",
    "down": "M20 12l-1.41-1.41L13 16.17V4h-2v12.17l-5.58-5.59L4 12l8 8 8-8z",
    "expandMore": "M16.59 8.59 12 13.17 7.41 8.59 6 10l6 6 6-6-1.41-1.41z",
    "expandLess": "M12 8l-6 6 1.41 1.41L12 10.83l4.59 4.58L18 14z",
    "collapseL": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm4-9h-6V8l-4 4 4 4v-3h6v-2z",
    "close": "M19 6.41 17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z",
    "lo": "M12 3 1 9l11 6 9-4.91V17h2V9L12 3z",
    "link": "M3.9 12c0-1.71 1.39-3.1 3.1-3.1h4V7H7c-2.76 0-5 2.24-5 5s2.24 5 5 5h4v-1.9H7c-1.71 0-3.1-1.39-3.1-3.1zM8 13h8v-2H8v2zm9-6h-4v1.9h4c1.71 0 3.1 1.39 3.1 3.1s-1.39 3.1-3.1 3.1h-4V17h4c2.76 0 5-2.24 5-5s-2.24-5-5-5z",
    "flash": "M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 14H4V6h16v12zM6 10h2v2H6zm0 4h8v2H6zm10-4h2v2h-2zm-6 0h4v2h-4z",
    "mic": "M12 14c1.66 0 3-1.34 3-3V5c0-1.66-1.34-3-3-3S9 3.34 9 5v6c0 1.66 1.34 3 3 3zm5-3c0 2.76-2.24 5-5 5s-5-2.24-5-5H5c0 3.53 2.61 6.43 6 6.92V21h2v-3.08c3.39-.49 6-3.39 6-6.92h-2z",
    "checks": "M20 2H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-8.09 12L7.5 9.59 8.91 8.18l3 3 5.59-5.59L18.91 7 11.91 14zM4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6z",
    "shuffle": "M10.59 9.17 5.41 4 4 5.41l5.17 5.17 1.42-1.41zM14.5 4l2.04 2.04L4 18.59 5.41 20 17.96 7.46 20 9.5V4h-5.5zm.33 9.41-1.41 1.41 3.13 3.13L14.5 20H20v-5.5l-2.04 2.04-3.13-3.13z",
    "spark": "M19 9l1.25-2.75L23 5l-2.75-1.25L19 1l-1.25 2.75L15 5l2.75 1.25L19 9zm-7.5.5L9 4 6.5 9.5 1 12l5.5 2.5L9 20l2.5-5.5L17 12l-5.5-2.5zM19 15l-1.25 2.75L15 19l2.75 1.25L19 23l1.25-2.75L23 19l-2.75-1.25L19 15z",
    # the AI Feedback type: MUI RateReview, distinct from the AI Tutor sparkle
    "rateReview": "M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 14v-2.47l6.88-6.88c.2-.2.51-.2.71 0l1.77 1.77c.2.2.2.51 0 .71L8.47 14H6zm12 0h-7.5l2-2H18v2z",
    "lock": "M18 8h-1V6c0-2.76-2.24-5-5-5S7 3.24 7 6v2H6c-1.1 0-2 .9-2 2v10c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V10c0-1.1-.9-2-2-2zM9 6c0-1.66 1.34-3 3-3s3 1.34 3 3v2H9V6zm9 14H6V10h12v10z",
    "info": "M11 7h2v2h-2zm0 4h2v6h-2zm1-9C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.58-8 8-8 8 3.59 8 8-3.59 8-8 8z",
    "warning": "M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z",
    "calendar": "M20 3h-1V1h-2v2H7V1H5v2H4c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 18H4V8h16v13z",
    "cloudUp": "M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM14 13v4h-4v-4H7l5-5 5 5h-3z",
    "eye": "M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z",
    "eyeOff": "M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78 3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z",
    "check": "M9 16.17 4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z",
    "checkCircle": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z",
    "schedule": "M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zM12 20c-4.42 0-8-3.58-8-8s3.58-8 8-8 8 3.58 8 8-3.58 8-8 8zm.5-13H11v6l5.25 3.15.75-1.23-4.5-2.67z",
    "description": "M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z",
    "back": "M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z",
    "autorenew": "M12 6v3l4-4-4-4v3c-4.42 0-8 3.58-8 8 0 1.57.46 3.03 1.24 4.26L6.7 14.8c-.45-.83-.7-1.79-.7-2.8 0-3.31 2.69-6 6-6zm6.76 1.74L17.3 9.2c.44.84.7 1.79.7 2.8 0 3.31-2.69 6-6 6v-3l-4 4 4 4v-3c4.42 0 8-3.58 8-8 0-1.57-.46-3.03-1.24-4.26z",
    "edit": "M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z",
    "del": "M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z",
    "send": "M2.01 21 23 12 2.01 3 2 10l15 2-15 2z",
    "assignment": "M19 3h-4.18C14.4 1.84 13.3 1 12 1c-1.3 0-2.4.84-2.82 2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 0c.55 0 1 .45 1 1s-.45 1-1 1-1-.45-1-1 .45-1 1-1zm-2 14-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z",
    "globe": "M11.99 2C6.47 2 2 6.48 2 12s4.47 10 9.99 10C17.52 22 22 17.52 22 12S17.52 2 11.99 2zm6.93 6h-2.95c-.32-1.25-.78-2.45-1.38-3.56 1.84.63 3.37 1.91 4.33 3.56zM12 4.04c.83 1.2 1.48 2.53 1.91 3.96h-3.82c.43-1.43 1.08-2.76 1.91-3.96zM4.26 14C4.1 13.36 4 12.69 4 12s.1-1.36.26-2h3.38c-.08.66-.14 1.32-.14 2s.06 1.34.14 2H4.26zm.82 2h2.95c.32 1.25.78 2.45 1.38 3.56-1.84-.63-3.37-1.9-4.33-3.56zm2.95-8H5.08c.96-1.66 2.49-2.93 4.33-3.56C8.81 5.55 8.35 6.75 8.03 8zM12 19.96c-.83-1.2-1.48-2.53-1.91-3.96h3.82c-.43 1.43-1.08 2.76-1.91 3.96zM14.34 14H9.66c-.09-.66-.16-1.32-.16-2s.07-1.35.16-2h4.68c.09.65.16 1.32.16 2s-.07 1.34-.16 2zm.25 5.56c.6-1.11 1.06-2.31 1.38-3.56h2.95c-.96 1.65-2.49 2.93-4.33 3.56zM16.36 14c.08-.66.14-1.32.14-2s-.06-1.34-.14-2h3.38c.16.64.26 1.31.26 2s-.1 1.36-.26 2h-3.38z",
    "filter": "M10 18h4v-2h-4v2zM3 6v2h18V6H3zm3 7h12v-2H6v2z",
    "history": "M13 3a9 9 0 0 0-9 9H1l3.89 3.89.07.14L9 12H6c0-3.87 3.13-7 7-7s7 3.13 7 7-3.13 7-7 7c-1.93 0-3.68-.79-4.94-2.06l-1.42 1.42A8.954 8.954 0 0 0 13 21a9 9 0 0 0 0-18zm-1 5v5l4.28 2.54.72-1.21-3.5-2.08V8H12z",
    "personAdd": "M15 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm-9-2V7H4v3H1v2h3v3h2v-3h3v-2H6zm9 4c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z",
}
def mi(name, size=24, color="currentColor"):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="{color}" aria-hidden="true" '
            f'style="flex-shrink:0;display:block"><path d="{MI[name]}"/></svg>')

# manabieV5 tokens: src/styles/themes/variants/manabieV5.ts
TCSS = """
.troot{width:1440px;height:900px;display:flex;overflow:hidden;background:#fff;color:#212121;position:relative;
  font-family:Roboto,'Noto Sans JP',-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;font-size:14px;line-height:1.43;letter-spacing:.15px}
.troot a{color:#2196F3;text-decoration:none}
/* drawer */
.tnav{width:260px;flex:0 0 260px;background:#FAFAFA;border-right:1px solid #E0E0E0;display:flex;flex-direction:column;min-height:0}
.torg{height:64px;flex:0 0 64px;display:flex;align-items:center;justify-content:space-between;padding:0 8px 0 16px;gap:8px}
.torg .id{display:flex;align-items:center;gap:12px;min-width:0}
.torg .mark{width:32px;height:32px;border-radius:8px;background:#2196F3;color:#fff;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:16px;flex:0 0 32px}
.torg .name{font-weight:600;font-size:18px;color:rgba(0,0,0,.87);white-space:nowrap}
.ticon{width:36px;height:36px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;color:rgba(0,0,0,.54);flex:0 0 auto;background:transparent;border:0;padding:0;cursor:pointer}
.ticon.sm{width:30px;height:30px}
.ticon.primary{color:#2196F3}
.ticon.dis{color:#BDBDBD}
.tmenu-b{flex:1 1 auto;overflow:auto;padding-bottom:8px;min-height:0}
.tn{display:flex;align-items:center;min-height:48px;padding:4px 0;color:#424242;position:relative}
.tn .mi{width:60px;flex:0 0 60px;display:flex;align-items:center;justify-content:center;color:#9E9E9E}
.tn .lb{font-size:14px;line-height:1.43;padding-right:28px}
.tn .caret{position:absolute;right:16px;color:rgba(0,0,0,.54)}
.tn.child{min-height:36px}
.tn.child .mi::before{content:"";width:6px;height:6px;border-radius:50%;background:#9E9E9E}
.tn.on{background:#1976D21F}
.tn.on .lb,.tn.branch .lb{color:rgba(0,0,0,.87)}
.tn.on .mi,.tn.branch .mi{color:#0B79D0}
.tn.on.child .mi::before{background:#0B79D0}
.tuser{flex:0 0 auto;border-top:1px solid #E0E0E0;padding:10px 16px;display:flex;align-items:center;gap:10px}
.tuser .tav{width:32px;height:32px;border-radius:50%;background:#E3F2FD;color:#0B79D0;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:500;flex:0 0 32px}
/* prototype-only pills: the role switch sits in the drawer, in flow, so it covers nothing */
.troot .dev{position:static;flex:0 0 auto;margin:0 10px 10px;display:flex;justify-content:center;flex-wrap:wrap;gap:2px;box-shadow:none}
.troot .dev-i{height:24px;padding:0 8px;font-size:11px;gap:4px}
.troot .seg{flex:0 0 auto;border-color:#E0E0E0;font-family:inherit}
.troot .seg-i{color:#757575;font-weight:500}
.troot .seg-i.on{background:#EDF7FE;color:#0B79D0}
/* main */
.tmain{flex:1 1 auto;min-width:0;display:flex;flex-direction:column;overflow:hidden;background:#fff;position:relative}
.tmain>.tscroll{flex:1 1 auto;overflow:auto;padding:24px 32px 28px}
.tcrumbs{display:flex;align-items:center;gap:8px;font-size:14px;color:#757575;margin-bottom:8px;flex-wrap:wrap}
.tcrumbs .sep{color:#BDBDBD}
.tcrumbs a{color:#757575}
.tphead{display:flex;align-items:flex-start;justify-content:space-between;gap:16px;margin-bottom:24px}
.tphead h1{font-size:24px;font-weight:500;line-height:1.334;letter-spacing:0;margin:0;display:flex;align-items:center;gap:12px;flex-wrap:wrap}
.tphead .acts{display:flex;align-items:center;gap:8px;flex:0 0 auto}
.tright{display:flex;align-items:center;gap:12px;flex:0 0 auto}
.testing{display:inline-flex;align-items:center;height:22px;padding:0 10px;border-radius:11px;border:1px solid #F44336;color:#E31B0C;font-size:11px;font-weight:700;letter-spacing:.06em}
/* buttons (MUI) */
.tbtn{display:inline-flex;align-items:center;justify-content:center;gap:8px;height:36px;padding:0 16px;border-radius:4px;border:1px solid transparent;
  background:transparent;font-size:14px;font-weight:500;letter-spacing:.4px;white-space:nowrap;color:#2196F3;cursor:pointer;font-family:inherit}
.tbtn.contained{background:#2196F3;color:#fff;box-shadow:0 3px 1px -2px rgba(0,0,0,.2),0 2px 2px rgba(0,0,0,.14),0 1px 5px rgba(0,0,0,.12)}
.tbtn.outlined{border-color:rgba(33,150,243,.5)}
.tbtn.neutral{color:#757575;border-color:#E0E0E0}
.tbtn.sm{height:30px;padding:0 10px;font-size:13px}
.tbtn.dis{color:#BDBDBD;background:#EEEEEE;box-shadow:none;cursor:default}
.tbtn.danger{color:#E31B0C}
/* chips */
.tchip{display:inline-flex;align-items:center;gap:6px;height:24px;padding:0 10px;border-radius:12px;font-size:12px;line-height:1;border:1px solid #E0E0E0;color:#212121;background:#fff;white-space:nowrap}
.tchip.filled{border-color:transparent;background:#EEEEEE}
.tchip.published{background:rgba(76,175,80,.14);border-color:transparent;color:#3B873E}
.tchip.unpublished{background:#EEEEEE;border-color:transparent;color:#616161}
.tchip.wait{background:rgba(255,152,0,.16);border-color:transparent;color:#C77700}
.tchip.type{background:#E3F2FD;border-color:transparent;color:#0B79D0}
.tchip.new{background:#FFF4E5;border-color:transparent;color:#663C00;font-weight:700;height:18px;padding:0 6px;font-size:10px}
.tchip.red{background:#FEEBEE;border-color:transparent;color:#C62828}
/* accordion tree (BookDetail) */
.acc{border:1px solid rgba(0,0,0,.12);margin-bottom:10px;background:#fff}
.acc.open{border-left:4px solid #2196F3}
.acc-sum{display:flex;align-items:center;gap:8px;padding:10px 16px;background:#fff}
.acc.open>.acc-sum{background:#F5F5F5}
.acc-sum .title{flex:1 1 auto;font-size:14px;font-weight:500;color:#212121;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.acc-sum .tools{display:flex;align-items:center;gap:2px;flex:0 0 auto}
.acc-body{padding:8px 0 12px}
.acc.tp{margin:8px 16px 8px 32px}
.acc.tp.open{border-left:4px solid #64B6F7}
.acc.tp>.acc-sum{padding:8px 16px}
.lm-list{list-style:none;margin:0;padding:0 0 0 32px}
.lm{display:flex;align-items:center;gap:10px;padding:8px 16px 8px 8px;border-radius:4px}
.lm .nm{color:#2196F3;font-size:14px;min-width:0;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.lm-type{width:24px;height:24px;border-radius:4px;display:flex;align-items:center;justify-content:center;flex:0 0 auto;background:#E3F2FD;color:#0B79D0}
.lm .spc{flex:1 1 auto}
.lm.just-created{background:#EDF7FE;box-shadow:inset 3px 0 0 #2196F3}
/* dialog */
.tscrim{position:absolute;inset:0;background:rgba(0,0,0,.5);z-index:80;display:flex;align-items:center;justify-content:center;padding:12px}
.dlg{background:#fff;border-radius:4px;width:100%;max-width:900px;max-height:calc(100% - 24px);display:flex;flex-direction:column;
  box-shadow:0 11px 15px -7px rgba(0,0,0,.2),0 24px 38px 3px rgba(0,0,0,.14),0 9px 46px 8px rgba(0,0,0,.12)}
.dlg-head{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 24px;border-bottom:1px solid #E0E0E0}
.dlg-head h2{margin:0;font-size:20px;font-weight:500}
.dlg-body{padding:20px 24px 16px;overflow:auto;display:flex;flex-direction:column;gap:16px;min-height:0}
.dlg-foot{display:flex;justify-content:flex-end;gap:8px;padding:8px 24px;border-top:1px solid #E0E0E0}
.sec-head{font-size:16px;font-weight:500;margin:0 0 14px}
.lm-section+.lm-section{padding-top:16px;border-top:1px solid #E0E0E0}
.lm-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px 48px}
.lm-grid .span2{grid-column:1 / -1}
/* MUI outlined field */
.field{position:relative;display:block}
.field>.lbl{position:absolute;left:9px;top:-8px;padding:0 5px;background:#fff;font-size:12px;color:#757575;pointer-events:none;z-index:1;line-height:16px}
.field>.lbl .req{color:#F44336}
.field .in{width:100%;height:40px;padding:0 14px;border-radius:4px;border:1px solid #BDBDBD;background:#fff;font-size:14px;color:#212121;display:flex;align-items:center;gap:8px}
.field .in.ph{color:#9E9E9E}
.field .in.area{height:auto;min-height:60px;padding:10px 14px;align-items:flex-start;line-height:1.5;display:block}
.field .in .gr{margin-left:auto;color:rgba(0,0,0,.54);flex:0 0 auto}
.field.focus .in{border-color:#2196F3;box-shadow:inset 0 0 0 1px #2196F3}
.helper{font-size:12px;color:#757575;margin-top:4px;display:block;line-height:1.5}
.tinput{height:40px;padding:0 14px;border:1px solid #BDBDBD;border-radius:4px;font:inherit;font-size:14px;color:#212121;flex:1 1 auto;min-width:0;background:#fff}
.tinput:focus{outline:0;border-color:#2196F3;box-shadow:inset 0 0 0 1px #2196F3}
.tinput::placeholder{color:#9E9E9E}
/* settings list */
.settings-list{display:flex;flex-direction:column}
.settings-list>.setting+.setting{margin-top:12px;padding-top:12px;border-top:1px dashed #E0E0E0}
.setting{display:flex;flex-direction:column;gap:6px}
.setting .hint{font-size:12px;line-height:1.5;color:#757575;margin:0}
.setting .eyebrow{font-size:12px;color:#757575}
.setting-label{font-size:14px;color:#212121}
/* MUI switch */
.switch{display:inline-flex;align-items:center;gap:12px;font-size:14px;cursor:pointer;background:none;border:0;padding:4px 0;color:#212121;font-family:inherit;text-align:left}
.switch .track{position:relative;width:34px;height:14px;border-radius:7px;background:rgba(0,0,0,.38);flex:0 0 auto;margin:0 3px}
.switch .track::after{content:"";position:absolute;left:-3px;top:-3px;width:20px;height:20px;border-radius:50%;background:#fafafa;
  box-shadow:0 2px 1px -1px rgba(0,0,0,.2),0 1px 1px rgba(0,0,0,.14),0 1px 3px rgba(0,0,0,.12)}
.switch.on .track{background:#64B6F7}
.switch.on .track::after{transform:translateX(17px);background:#2196F3}
/* MUI checkbox */
.check{display:flex;align-items:center;gap:10px;font-size:14px;cursor:pointer;background:none;border:0;padding:3px 0;color:#212121;font-family:inherit;text-align:left}
.check .cbx{width:18px;height:18px;border:2px solid #9E9E9E;border-radius:2px;background:#fff;flex:0 0 auto;display:flex;align-items:center;justify-content:center;color:#fff}
.check .cbx svg{display:none}
.check.on .cbx{background:#2196F3;border-color:#2196F3}
.check.on .cbx svg{display:block}
/* alert */
.alert{display:flex;gap:12px;padding:10px 16px;border-radius:4px;font-size:14px;align-items:flex-start;line-height:1.45}
.alert.info{background:#EDF7FE;color:#0d3c61}
.alert.warn{background:#FFF4E5;color:#663C00}
.alert svg{flex:0 0 auto;margin-top:1px}
/* select menu (MUI Menu paper) */
.tpop{position:absolute;z-index:90;background:#fff;border-radius:4px;padding:8px 0;min-width:320px;
  box-shadow:0 5px 5px -3px rgba(0,0,0,.2),0 8px 10px 1px rgba(0,0,0,.14),0 3px 14px 2px rgba(0,0,0,.12)}
.tpop .it{display:flex;align-items:center;gap:10px;padding:8px 16px;font-size:14px;color:#212121;min-height:36px}
.tpop .it.sel{background:#1976D21F}
/* snackbar */
.snack{position:absolute;left:24px;bottom:24px;z-index:120;background:#2E7D32;color:#fff;border-radius:4px;padding:12px 16px;font-size:14px;
  box-shadow:0 5px 5px -3px rgba(0,0,0,.2),0 8px 10px 1px rgba(0,0,0,.14),0 3px 14px 2px rgba(0,0,0,.12);display:flex;gap:12px;align-items:center;max-width:480px}
/* tabs */
.tabs{display:flex;border-bottom:1px solid #E0E0E0;margin-bottom:24px}
.tab{position:relative;padding:12px 16px;font-size:14px;font-weight:500;letter-spacing:.4px;color:#757575;white-space:nowrap}
.tab.on{color:#2196F3}
.tab.on::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:2px;background:#2196F3}
/* paper, tables, kv */
.tpaper{background:#fff;border:1px solid #E0E0E0;border-radius:4px}
.tpaper .ph{padding:16px 20px;border-bottom:1px solid #E0E0E0;display:flex;align-items:center;justify-content:space-between;gap:12px}
.tpaper .ph h3{margin:0;font-size:16px;font-weight:500}
.tpaper .pb{padding:20px}
table.m{width:100%;border-collapse:collapse;font-size:14px}
table.m thead th{position:relative;text-align:left;font-weight:500;color:#212121;padding:12px 16px;border-bottom:1px solid #E0E0E0;white-space:nowrap;background:#fff}
table.m thead th:not(:last-child)::after{content:"";position:absolute;width:2px;height:14px;right:0;top:50%;transform:translateY(-50%);background:#E0E0E0}
table.m tbody td{padding:12px 16px;border-bottom:1px solid #E0E0E0;vertical-align:middle;background:#fff}
table.m tbody tr:last-child td{border-bottom:0}
.name-cell{display:flex;align-items:center;gap:10px}
.avatar{width:32px;height:32px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;background:#E3F2FD;color:#0B79D0;font-size:12px;font-weight:500;flex:0 0 auto}
.pagination{display:flex;align-items:center;justify-content:flex-end;gap:24px;padding:8px 16px;border-top:1px solid #E0E0E0;font-size:13px;color:#757575}
.tkv{display:grid;grid-template-columns:200px 1fr;gap:14px 24px;max-width:760px;margin:0}
.tkv dt{color:#757575;font-size:14px;margin:0}
.tkv dd{margin:0;font-size:14px}
/* analysis cards (AI Tutor assignment detail) */
.analysis{border:1px solid #E0E0E0;border-radius:8px;background:#FAFAFA;padding:16px 20px}
.analysis h4{margin:0 0 12px;font-size:20px;font-weight:700}
.analysis .grid{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}
.metric{background:#fff;border:1px solid #E0E0E0;border-radius:8px;padding:16px}
.metric.hot{border-color:#FF9800;background:#FFFBF2}
.metric .m-top{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:12px}
.metric .m-lbl{display:flex;align-items:center;gap:6px;font-size:16px;font-weight:700}
.metric .m-lbl svg{color:rgba(0,0,0,.54)}
.metric .m-val{background:#424242;color:#fff;border-radius:4px;min-width:32px;text-align:center;padding:2px 8px;font-size:12px;font-variant-numeric:tabular-nums}
.metric .m-desc{font-size:14px;color:#212121;margin:0 0 12px}
/* material page bits */
.tdrop{border:1px dashed #90CAF9;border-radius:4px;background:#EDF7FE;padding:18px 20px;display:flex;align-items:center;justify-content:center;gap:10px;color:#0B79D0;font-weight:500;font-size:14px}
.tfile{display:inline-flex;align-items:center;gap:10px;border:1px solid #E0E0E0;border-radius:4px;padding:8px 12px 8px 10px;font-size:14px;background:#fff}
.tfile .fi{width:28px;height:28px;border-radius:4px;display:flex;align-items:center;justify-content:center;flex:0 0 28px}
.titem{display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid #E0E0E0;font-size:14px}
.titem:last-child{border-bottom:0}
.titem .src{margin-left:auto;font-size:12px;color:#616161;background:#F5F5F5;border-radius:4px;padding:2px 8px;white-space:nowrap}
.trubric{font-family:Georgia,"Times New Roman","Noto Serif JP",serif;border:1px solid #E0E0E0;border-radius:4px;padding:16px 22px 14px;background:#FAFAFA;font-size:14px;line-height:1.6;color:#212121}
.trubric h5{margin:0 0 8px;font-size:15px;font-weight:700;display:flex;align-items:center;justify-content:space-between;gap:12px}
.trubric ol{margin:0;padding-left:22px}.trubric li{margin-bottom:4px}.trubric li b{font-weight:700}
/* review two-pane */
.tpanes{display:flex;gap:16px;flex:1 1 auto;min-height:0}
.tpane{flex:1 1 0;border:1px solid #E0E0E0;border-radius:4px;display:flex;flex-direction:column;min-height:0;overflow:hidden;background:#fff}
.tpane .thd{padding:11px 16px;border-bottom:1px solid #E0E0E0;display:flex;align-items:center;justify-content:space-between;gap:10px;font-size:14px;font-weight:500;background:#FAFAFA}
.tpane .tbd{padding:16px 18px;overflow:auto;flex:1 1 auto}
.traw{font-size:14px;line-height:2;margin:0 0 14px}
.tdraft{border:1px solid #E0E0E0;border-radius:4px;padding:14px;display:flex;flex-direction:column;gap:9px;margin-bottom:12px}
.tdraft.edited{border-color:#2196F3;background:#EDF7FE}
.tdq{margin:0;padding:2px 0 2px 10px;border-left:3px solid #E0E0E0;font-size:13px;line-height:20px;color:#616161}
.tdb{margin:0;font-size:14px;line-height:1.8;white-space:pre-wrap}
.tdacts{display:flex;align-items:center;gap:4px;margin-top:2px}
.tbar{flex:0 0 auto;display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 32px 16px;border-top:1px solid #E0E0E0;background:#fff}
.tbody-flex{flex:1 1 auto;min-height:0;display:flex;flex-direction:column;padding:24px 32px 16px;overflow:hidden}
/* Submission Grading (To Review): status tones, filter bar, segments, wide table, grading layout */
.tchip.st-default{background:#EEEEEE;border-color:transparent;color:#424242}
.tchip.st-warning{background:rgba(255,152,0,.16);border-color:transparent;color:#C77700}
.tchip.st-secondary{background:#FBDCE7;border-color:transparent;color:#C2185B}
.tchip.st-success{background:rgba(76,175,80,.16);border-color:transparent;color:#3B873E}
.tchip.st-error{background:#FEEBEE;border-color:transparent;color:#E31B0C}
.tchip .tx{width:16px;height:16px;border-radius:50%;background:rgba(0,0,0,.26);display:inline-flex;align-items:center;justify-content:center;margin-left:2px}
.tfilterbar{display:flex;align-items:center;gap:16px}
.tfilterbar .left{display:flex;align-items:center;gap:8px;flex:1 1 320px;min-width:0}
.tfilterbar .right{display:flex;align-items:center;gap:8px;flex:0 0 auto}
.tsearch{position:relative;flex:1 1 240px;max-width:600px;height:40px;border:1px solid #BDBDBD;border-radius:4px;background:#fff;display:flex;align-items:center;gap:10px;padding:0 14px 0 12px;color:#9E9E9E;font-size:14px}
.tapplied{display:flex;align-items:center;gap:8px;font-size:13px;color:#757575;white-space:nowrap}
.tseg{display:inline-flex;border:1px solid #BDBDBD;border-radius:4px;overflow:hidden;align-self:flex-start}
.tseg span{color:#757575;padding:0 16px;height:36px;display:inline-flex;align-items:center;font-size:13px;font-weight:500;white-space:nowrap}
.tseg span+span{border-left:1px solid #BDBDBD}
.tseg span.on{background:#1976D21F;color:#0B79D0}
.table-scroll{overflow-x:auto}
table.m thead th.idx,table.m tbody td.idx{width:56px;color:#757575;padding-right:0}
table.m thead th.idx::after{display:none}
table.m thead th.cb,table.m tbody td.cb{width:52px;padding-right:0}
table.m thead th.cb::after{display:none}
.cbx-th,.cbx-td{display:inline-block;width:18px;height:18px;border:2px solid #9E9E9E;border-radius:2px;background:#fff;vertical-align:middle}
.cell-link{color:#2196F3}.cell-muted{color:#757575}.num{font-variant-numeric:tabular-nums}.dd{color:#9E9E9E}
table.m tbody td{vertical-align:top;white-space:nowrap}
.grade-layout{display:grid;grid-template-columns:400px 1fr;gap:24px;align-items:start}
.info-panel{border:1px solid #E0E0E0;border-radius:4px;background:#fff;padding:20px;display:flex;flex-direction:column;gap:22px}
.info-sec h3{margin:0 0 12px;font-size:16px;font-weight:500}
.info-rows{display:grid;grid-template-columns:minmax(96px,auto) 1fr;gap:10px 16px;font-size:14px;align-items:baseline;margin:0}
.info-rows dt{color:#757575;margin:0}.info-rows dd{margin:0;overflow-wrap:anywhere}
.report{border:1px solid #E0E0E0;border-radius:4px;background:#fff;overflow:hidden}
.report-head{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 20px;border-bottom:1px solid #E0E0E0}
.q-item{padding:20px;border-bottom:1px solid #E0E0E0}.q-item:last-child{border-bottom:0}
.q-item.edited{background:#F7FBFF;box-shadow:inset 3px 0 0 #2196F3}
.q-top{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:10px}
.q-top .q-no{font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#757575}
.q-top .q-title{font-weight:500;flex:1 1 200px;min-width:0}
.q-prompt{margin:0 0 12px;color:#212121;line-height:1.7;white-space:pre-wrap}
.q-answer{background:#FAFAFA;border:1px solid #E0E0E0;border-radius:4px;padding:12px 14px;margin-bottom:12px;line-height:1.7;font-size:14px}
.q-answer .who{display:block;font-size:12px;color:#757575;margin-bottom:6px}
/* Dashboard (GroupDashboard / StudentDashboard): filter row, overview cards, toggle group, progress, LO matrix, split */
.dash-filter{display:flex;align-items:center;gap:16px;flex-wrap:wrap}
.dash-filter .fld{flex:1 1 220px;min-width:180px;max-width:360px}
.dash-filter .vr{width:1px;align-self:stretch;min-height:28px;background:#E0E0E0}
.chiplist{display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-top:16px}
.ov-row{display:flex;gap:12px;flex-wrap:wrap;margin-bottom:16px}
.ov-card{display:flex;align-items:center;gap:14px;border:1px solid #E0E0E0;border-radius:8px;background:#fff;padding:12px 20px 12px 14px;width:fit-content;min-width:200px}
.ov-card .ic{width:44px;height:44px;border-radius:50%;display:flex;align-items:center;justify-content:center;flex:0 0 auto;background:#F5F5F5;color:#757575}
.ov-card .ic.blue{background:#EDF7FE;color:#2196F3}
.ov-card .ic.orange{background:#FFF4E5;color:#ED6C02}
.ov-card .ic.green{background:#E8F5E9;color:#4CAF50}
.ov-card .ic.red{background:#FEEBEE;color:#F44336}
.ov-card .lbl-sm{font-size:14px;color:#757575;display:block;white-space:nowrap}
.ov-card .val{font-size:24px;line-height:1.2;font-variant-numeric:tabular-nums;display:block}
.ov-card .val small{font-size:14px;color:#757575;margin-left:6px}
.ov-card .sub{font-size:12px;color:#757575;display:block;white-space:nowrap}
.ov-card.hot{border-color:#FF9800;background:#FFFBF2}
.toggle-group{display:inline-flex;border:1px solid rgba(33,150,243,.5);border-radius:4px;overflow:hidden;flex:0 0 auto}
.toggle-group span{color:#2196F3;padding:0 14px;height:34px;display:inline-flex;align-items:center;font-size:14px;font-weight:500;white-space:nowrap}
.toggle-group span+span{border-left:1px solid rgba(33,150,243,.5)}
.toggle-group span.on{background:#1976D21F;color:#0B79D0}
.progress{display:flex;align-items:center;gap:8px;width:100%;min-width:140px}
.progress .pct{min-width:38px;font-size:14px;font-variant-numeric:tabular-nums}
.progress .bar{flex:1 1 auto;height:4px;border-radius:2px;background:#EEEEEE;overflow:hidden}
.progress .bar i{display:block;height:100%;border-radius:2px;background:#2196F3}
.progress .bar i.good{background:#4CAF50}.progress .bar i.warn{background:#FF9800}
.matrix{border:1px solid #E0E0E0;border-radius:4px;overflow:auto;background:#fff;max-height:560px}
.matrix table{border-collapse:separate;border-spacing:0;font-size:14px}
.matrix th,.matrix td{padding:0;vertical-align:top;text-align:left}
.matrix .stu-col{position:sticky;left:0;z-index:2;background:#fff;width:210px;min-width:210px;max-width:210px;border-right:1px solid #E0E0E0}
.matrix thead .stu-col{z-index:4}
.matrix thead th{position:sticky;top:0;z-index:3;background:#fff;border-bottom:1px solid #E0E0E0}
.matrix .stu-head{padding:16px 10px;font-weight:500}
.matrix .stu-cell{padding:16px 10px;height:52px;box-sizing:border-box;display:flex;align-items:center}
.lo-col{width:200px;min-width:200px;max-width:200px;border-right:1px solid #E0E0E0;padding:6px 10px;box-sizing:border-box}
.lo-col .lo-name{display:flex;align-items:center;gap:6px;color:#2196F3;font-weight:500;overflow:hidden;white-space:nowrap;margin-bottom:2px}
.lo-col .lo-name span{overflow:hidden;text-overflow:ellipsis}
.lo-col .kv-line{font-size:12px;color:#757575;display:flex;gap:4px;line-height:1.5}
.lo-col .kv-line b{font-weight:400;color:#212121;font-variant-numeric:tabular-nums}
.matrix tbody td{border-bottom:1px solid #E0E0E0}
.matrix tbody tr:last-child td{border-bottom:0}
.stat-cell{display:flex;align-items:center;gap:8px;padding:0 10px;height:52px;box-sizing:border-box;border-right:1px solid #F5F5F5}
.stat-cell.miss{background:rgba(239,83,80,.1);color:#E31B0C}
.stat-cell .score{font-variant-numeric:tabular-nums}
.stat-cell .grow{margin-left:auto;color:#2196F3;display:flex;align-items:center;gap:6px}
.stat-cell .grow .cnt{font-size:12px;color:#757575;display:inline-flex;align-items:center;gap:2px;font-variant-numeric:tabular-nums}
.split{display:grid;grid-template-columns:240px minmax(0,1fr);gap:24px;align-items:start}
.stu-list{border:1px solid #E0E0E0;border-radius:4px;background:#fff;overflow:hidden}
.stu-list .sl-hd{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:12px 16px;border-bottom:1px solid #E0E0E0;font-weight:500}
.stu-list a.sl-item{display:block;padding:12px 16px;border-bottom:1px solid #E0E0E0;color:#212121}
.stu-list a.sl-item:last-child{border-bottom:0}
.stu-list a.sl-item.on{background:#EDF7FE;box-shadow:inset 3px 0 0 #2196F3}
.stu-list .sl-sub{font-size:12px;color:#757575;display:block}
table.m.tight thead th,table.m.tight tbody td{padding:12px 10px}
.dash-filter .field .in>.ell{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0}
.dash-h2{font-size:20px;font-weight:500;margin:0}
.insight{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.insight .tpaper .ph h3{font-size:15px}
.insight .tpaper .ph .helper{margin:2px 0 0}
.crit-row{display:grid;grid-template-columns:minmax(120px,1fr) 2fr auto;gap:12px;align-items:center;padding:8px 0;border-bottom:1px solid #F5F5F5;font-size:14px}
.crit-row:last-child{border-bottom:0}
.crit-row .n{font-variant-numeric:tabular-nums;color:#757575;font-size:13px;white-space:nowrap}
table.m tbody tr.sub td{background:#FAFAFA;padding:0 16px 16px 54px;border-bottom:1px solid #E0E0E0}
table.m table.inner{border:1px solid #E0E0E0;border-radius:4px;background:#fff;width:100%}
table.m table.inner thead th{background:#fff}
"""

THELMET = ('<helmet><link rel="preconnect" href="https://fonts.googleapis.com">'
           '<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&amp;family=Noto+Sans+JP:wght@400;500;700&amp;display=swap" rel="stylesheet">'
           f'<style>{CSS}{TCSS}</style></helmet>')

TJA = dict(
    t_lang="ja", t_org="LMS 2.0",
    t_nav=["ダッシュボード", "AIチューター", "生徒", "コース", "教材", "レッスン", "カレンダー", "お知らせ", "スタッフ"],
    t_nav_sub=["ブック管理", "学習計画の統計", "コンテンツバンク"],
    t_user="HTN Admin（LMS 2.0）", t_user_sub="LMS 2.0 ・ 集団（+6）・ 東京", t_testing="FOR TESTING",
    t_bm="ブック管理", t_book="地域環境統計学 テキスト（2026年度）", t_pub="公開中", t_unpub="未公開",
    t_topics="トピック", t_add_chapter="チャプターを追加", t_add_topic="トピックを追加", t_add_lo="LOを追加",
    t_ch6="第6回　データの整理と代表値", t_ch7="第7回　データの分析と仮説検定", t_ch8="第8回　回帰分析",
    t_tp71="7-1　相関分析", t_tp72="7-2　仮説検定",
    t_los=[("第7回 講義動画", "link", False), ("第7回 講義資料", "lo", False), ("第7回 確認クイズ", "lo", True)],
    t_new_lo="第7回 演習レポート", t_snack="LOを作成しました。",
    # Add Learning Objective dialog
    t_dlg_title="学習目標（LO）を追加", t_dlg_general="基本情報", t_dlg_settings="設定", t_dlg_select="LOタイプを選択",
    t_types=["ランダム学習", "学習目標", "フラッシュカード", "録音課題", "演習提出", "外部コンテンツ"],
    t_type_fb="AIフィードバック", t_new="NEW",
    t_f_name="学習目標", t_ph_name="LO名を入力", t_f_ext="外部LO ID", t_ph_ext="英数字のみ",
    t_f_desc="課題の説明（生徒に表示）",
    t_v_desc="総務省「社会生活統計指標」の都道府県別データから2つの変数を選び、Excel で相関係数を求めて散布図を作成してください。結果の解釈と、有意性の確認までを A4 2枚程度にまとめて提出します。",
    t_s_when="公開と提出期間", t_f_start="開始日時", t_v_start="2026/11/06 09:00", t_f_due="締切日時", t_v_due="2026/11/13 23:59",
    t_when_note="開始日時に生徒の「やること」に表示されます。締切までは提出と差し替えができ、締切のあとに先生が確認します。",
    t_f_resub="再提出を許可する", t_v_resub="2026/11/20 23:59 まで",
    t_s_how="提出方法", t_how=["ファイル（PDF ・ Word ・ Excel ・ PowerPoint）", "写真（複数枚まとめて）", "直接入力"],
    t_how_limit="文字数の上限 500字",
    t_s_review="先生の確認", t_review_on="返却前に先生が確認する",
    t_review_body="下書きは締切のあとに作成され、先生が確認・編集して返却するまで生徒には表示されません。生徒には先生からのフィードバックとして届きます。",
    t_review_off="締切のあと、先生の確認なしに自動で返却されます。",
    t_cancel="キャンセル", t_confirm="確定",
    # LO page
    t_lo_tabs=["内容", "設定"], t_course_tabs=["概要", "提出一覧"], t_publish="公開する", t_edit="設定を編集", t_save="保存",
    t_nav_course=["コース管理", "学習計画管理", "提出物の採点", "AIグレーディング"], t_toreview="提出物の採点", t_f_type="種類",
    t_course="コース", t_course_name="地域環境統計学（2026年度）", t_view_subs="提出状況を見る", t_edit_in_bm="ブック管理で編集",
    t_queue_sub="確認が必要な提出の一覧です。AIフィードバックの下書きは、先生の確認を待ってここに並びます。",
    t_queue_cols=["LO", "コース", "締切", "提出", "確認待ち", "返却済み", ""], t_open="開く", t_f_course="コース", t_filters="フィルター",
    t_queue=[("第7回 演習レポート", "11月13日 23:59", "12 / 30", "12", "9"), ("第7週 週次リフレクション", "11月15日 23:59", "21 / 30", "0", "21"),
             ("第6回 演習レポート", "11月6日 23:59", "30 / 30", "0", "30")],
    t_s_mat="この課題の教材", t_mat_note="アップロードした教材から、提出条件とコメントの観点を抽出します。",
    t_drop="ファイルをドラッグ＆ドロップ、またはファイルを選ぶ", t_drop_types="PDF ・ Word ・ PNG ・ JPG",
    t_file1="第7回_課題説明.pdf", t_file2="評価基準_2026.docx",
    t_extract="提出条件と観点を生成する", t_extracted="生成済み",
    t_s_cond="提出の基本条件", t_cond_note="生徒の提出画面に表示され、ファイルを選んだ時点で確認されます。",
    t_conds=[("散布図が含まれている", "課題説明 p.1"), ("相関係数が記載されている", "課題説明 p.1"),
             ("有意性の検定が記載されている", "課題説明 p.2"), ("参照した講義資料の記載", "評価基準 2.(3)"),
             ("ページ数 2枚程度", "課題説明 p.1")],
    t_add_cond="条件を追加", t_req_ph="例：データの出典が記載されている", t_req_src_me="先生が追加", t_add="追加", t_req_toggle="提出前に条件を確認する",
    t_req_off="オフのとき、条件は生徒に表示されず、提出時の確認も行いません。",
    t_s_crit="コメントの観点（ルーブリック）",
    t_crit_note="提出物はこの観点に沿って読まれ、各コメントには対応する観点が付きます。",
    t_rubric_h="評価基準",
    t_rubric=[("Excelスキル", "関数・数式を用いて相関係数を正しく算出している"), ("図表の見やすさ", "軸ラベル・単位・タイトルのある散布図になっている"),
              ("統計処理", "相関係数と有意性の検定を適切な手順で示している"), ("解釈", "相関と因果を区別して結果を解釈している"),
              ("論理構成", "目的・方法・結果・考察の流れがある"), ("生成AIリテラシー", "生成AIの利用を適切に扱い、自分の言葉で書いている")],
    t_regen="生成し直す", t_edit_rubric="編集", t_preview="生徒に表示される画面を見る",
    # overview
    t_s_status="提出状況", t_st1="提出済み", t_st1_n="12 / 30", t_st1_s="30人中12人が提出しました",
    t_st2="未確認", t_st2_n="8", t_st2_s="下書きができています。確認して返却してください", t_st3="返却済み", t_st3_n="3 / 30", t_st3_s="30人中3人に返却しました",
    t_open_list="確認する（8件）",
    t_s_sum="設定", t_sum=[("提出期間", "11月6日 09:00 — 11月13日 23:59"), ("再提出", "11月20日 23:59 まで"),
                            ("提出方法", "ファイル ・ 写真 ・ 直接入力"), ("先生の確認", "あり（返却前に確認）"),
                            ("提出条件", "5件"), ("コメントの観点", "6件")],
    # submissions
    t_cols=["生徒", "提出", "状態", ""], t_bulk="一括操作", t_bulk_note="内容を見てから返却することをおすすめします",
    t_rows=[("山田 花子", "11月11日 14:32", "wait", "確認待ち"), ("佐藤 太郎", "11月11日 18:05", "wait", "確認待ち"),
            ("鈴木 一郎", "11月12日 08:12", "wait", "確認待ち"), ("田中 美咲", "11月12日 21:40", "done", "返却済み"),
            ("高橋 健", "—", "none", "未提出")],
    t_review_btn="確認する", t_view="見る", t_rows_of="1-5 / 30", t_rows_pp="表示件数:",
    # Submission Grading (ToReviewListPage) — the AI Feedback statuses in the marking tones
    t_sg_invalid="無効な確認者", t_sg_tabs=["提出物", "学習目標"], t_sg_search="提出ID・生徒名・LO名で検索", t_applied="絞り込み:", t_lo_type="LOタイプ", t_all="すべて",
    t_status={"nr": ("未確認", "st-default"), "ir": ("確認中", "st-warning"), "ret": ("返却済み", "st-success"), "back": ("差し戻し", "st-error")},
    t_sec={"auto": "自動返却", "resub": "再提出"},
    t_sg_cols=["提出ID", "LO名", "生徒名", "ユーザー名", "外部ID", "コース", "ブック", "確認者", "状態", "コメント", "提出日時", "確認日時", "返却日時"],
    t_sg_cols_lo=["提出ID", "生徒名", "ユーザー名", "外部ID", "確認者", "状態", "コメント", "提出日時", "確認日時", "返却日時"],
    t_teacher="安本 正義",
    t_subs=[dict(id="FB-260911", lo="第7回 演習レポート", student="山田 花子", user="hanako.yamada", ext="KU-2041", reviewer="安本 正義", st="ir", sec="", n=3, sub="2026/11/14 09:12", rev="--", ret="--"),
            dict(id="FB-260912", lo="第7回 演習レポート", student="佐藤 太郎", user="taro.sato", ext="KU-2042", reviewer="--", st="nr", sec="", n=3, sub="2026/11/11 18:05", rev="--", ret="--"),
            dict(id="FB-260913", lo="第7回 演習レポート", student="鈴木 一郎", user="ichiro.suzuki", ext="KU-2043", reviewer="--", st="nr", sec="", n=3, sub="2026/11/12 08:12", rev="--", ret="--"),
            dict(id="FB-260914", lo="第7回 演習レポート", student="田中 美咲", user="misaki.tanaka", ext="KU-2044", reviewer="安本 正義", st="ret", sec="", n=3, sub="2026/11/12 21:40", rev="2026/11/14 10:05", ret="2026/11/14 10:05"),
            dict(id="FB-260915", lo="第7週 週次リフレクション", student="山田 花子", user="hanako.yamada", ext="KU-2041", reviewer="--", st="ret", sec="auto", n=2, sub="2026/11/15 20:11", rev="--", ret="2026/11/16 00:05"),
            dict(id="FB-260916", lo="第7週 週次リフレクション", student="高橋 健", user="ken.takahashi", ext="KU-2045", reviewer="--", st="ret", sec="auto", n=2, sub="2026/11/15 22:47", rev="--", ret="2026/11/16 00:05"),
            dict(id="FB-260917", lo="第6回 演習レポート", student="佐藤 太郎", user="taro.sato", ext="KU-2042", reviewer="安本 正義", st="back", sec="", n=3, sub="2026/11/04 17:20", rev="2026/11/07 09:30", ret="--"),
            dict(id="FB-260918", lo="第6回 演習レポート", student="佐藤 太郎", user="taro.sato", ext="KU-2042", reviewer="--", st="nr", sec="resub", n=3, sub="2026/11/09 13:02", rev="--", ret="--")],
    t_subs_extra=[dict(id="FB-260919", lo="第7回 演習レポート", student="伊藤 さくら", user="sakura.ito", ext="KU-2046", reviewer="--", st="nr", sec="", n=3, sub="2026/11/13 22:58", rev="--", ret="--")],
    t_comment="コメント", t_passage="該当箇所（生徒の提出物より）", t_recognised="読み取ったテキスト",
    t_reviewer_info="確認者情報", t_reviewer="確認者", t_auto_return="自動返却", t_off="オフ", t_sub_info="提出情報", t_student_name="生徒名", t_submitted="提出日時", t_file="ファイル",
    t_comments_h="コメント", t_drafts="下書き", t_criteria="観点",
    # review
    t_rev_title="確認して返却 ・ 山田 花子", t_rev_meta="11月11日 14:32 提出",
    t_rev_hidden="生徒には未公開", t_rev_left="提出物", t_rev_right="フィードバックの下書き",
    t_rev_right_n="3件 ・ 観点 6", t_rev_note_h="先生からのひとこと（任意）",
    t_rev_note="東京都を除いて再計算したところ、よく気づきました。②の点は次回の授業でも取り上げるので、自分の考えを用意しておいてください。",
    t_rev_edited="編集済み", t_rev_edit="編集", t_rev_drop="削除", t_rev_back="差し戻す", t_rev_send="承認して返却する",
    t_rev_count="3件のうち1件を編集しました",
    t_role_t="先生（BO）", t_role_s="生徒画面", t_role_aria="表示する役割",
    # Dashboard (GroupDashboard / StudentDashboard) with the AI Feedback overview fitted in
    t_dash_tabs=["グループダッシュボード", "生徒ダッシュボード", "リアルタイムダッシュボード", "AIダッシュボード"],
    t_f_book="ブック", t_apply="適用", t_dash_chips=["在籍: 在籍中", "期間: 有効"], t_reset="初期設定に戻す",
    t_ai_solved="AIで解決した質問", t_ai_solved_n="1,284",
    t_ov=[("rateReview", "blue", "AIフィードバック 提出", "41", "/ 90", "3 LO ・ 30人", "T-Queue"),
          ("schedule", "orange", "確認待ち", "9", "", "先生の確認を待つ下書き", "T-Queue"),
          ("checkCircle", "green", "返却済み", "27", "", "うち自動返却 21", None),
          ("autorenew", "", "再提出", "4", "", "差し戻し 1 を含む", None),
          ("event", "", "返却までの平均", "1.8", "日", "締切から返却まで", None)],
    t_dash_search="生徒名で検索", t_dash_modes=["トピックダッシュボード", "LOダッシュボード"], t_topic_lbl="トピック:",
    t_score_modes=["最新スコア", "最高スコア"], t_stu_name="生徒名",
    t_lo_kv=["平均スコア", "完了率", "AIが回答した質問"], t_fb_kv=["提出", "確認待ち", "返却済み"],
    t_completed="完了", t_marking="採点中",
    t_matrix_help="スコアをクリックすると、その生徒のLOの提出一覧を表示します。AIフィードバックの状態をクリックすると「提出物の採点」で開きます。",
    t_mx_los=[("第7回 講義動画", "comp", ("--", "28/30", "0")), ("第7回 確認クイズ", "score", ("74", "26/30", "38")),
              ("第7回 演習レポート", "fb", ("12/30", "8", "3")), ("第7週 週次リフレクション", "fb", ("21/30", "0", "21"))],
    t_mx_students=[("山田 花子", [("comp",), ("score", "9/10", False, False), ("fb", "ir", 3, ""), ("fb", "ret", 2, "auto")]),
                   ("佐藤 太郎", [("comp",), ("score", "6/10", True, False), ("fb", "nr", 3, ""), ("fb", "ret", 2, "auto")]),
                   ("鈴木 一郎", [("comp",), ("score", "7/10", False, False), ("fb", "nr", 3, ""), ("fb", "ret", 1, "auto")]),
                   ("田中 美咲", [("comp",), ("score", "10/10", False, False), ("fb", "ret", 3, ""), ("fb", "ret", 2, "auto")]),
                   ("高橋 健", [("none",), ("score", "4/10", False, True), ("none",), ("fb", "ret", 2, "auto")]),
                   ("伊藤 さくら", [("comp",), ("score", "8/10", True, False), ("fb", "nr", 3, ""), ("none",)]),
                   ("渡辺 大輝", [("comp",), ("score", "5/10", False, True), ("none",), ("fb", "ret", 2, "auto")])],
    t_crit_h="観点別の指摘 ・ 第7回 演習レポート", t_crit_sub="下書き12件のうち、改善点のコメントが付いた割合",
    t_crit_rows=[("統計処理", 8), ("解釈", 6), ("図表の見やすさ", 4), ("論理構成", 3), ("Excelスキル", 2), ("生成AIリテラシー", 1)], t_crit_of=12,
    t_reqf_h="提出前チェックで止まった条件", t_reqf_sub="ファイル選択時に満たされていなかった回数（提出前に修正）",
    t_reqf_rows=[("有意性の検定が記載されている", 9), ("散布図が含まれている", 4), ("ページ数 2枚程度", 3), ("参照した講義資料の記載", 2), ("相関係数が記載されている", 0)],
    t_times="回",
    # Student Dashboard
    t_stu_list="生徒リスト",
    t_students=[("山田 花子", "3年 ・ KU-2041"), ("佐藤 太郎", "3年 ・ KU-2042"), ("鈴木 一郎", "3年 ・ KU-2043"), ("田中 美咲", "2年 ・ KU-2044"), ("高橋 健", "3年 ・ KU-2045")],
    t_ind_cols=["チャプター名", "トピック名", "学習日", "平均スコア", "完了"], t_sub_cols=["学習目標", "最終提出", "最新スコア", "最高スコア"],
    t_ind_rows=[("第6回　データの整理と代表値", "6-1　度数分布とヒストグラム", "2026/10/23", 85, "3/3", False, []),
                ("第6回　データの整理と代表値", "6-2　代表値と散布度", "2026/11/09", 80, "3/3", True,
                 [("第6回 講義動画", "2026/10/28", "comp", "comp"), ("第6回 確認クイズ", "2026/10/29", "8/10", "8/10"), ("第6回 演習レポート", "2026/11/09", "fb:ret", "resub")]),
                ("第7回　データの分析と仮説検定", "7-1　相関分析", "2026/11/14", 90, "3/4", True,
                 [("第7回 講義動画", "2026/11/08", "comp", "comp"), ("第7回 講義資料", "2026/11/08", "comp", "comp"), ("第7回 確認クイズ", "2026/11/10", "9/10", "9/10"), ("第7回 演習レポート", "2026/11/14", "fb:ir", "--")]),
                ("第7回　データの分析と仮説検定", "7-2　仮説検定", "2026/11/15", -1, "1/2", False, []),
                ("第8回　回帰分析", "8-1　単回帰分析", "--", -1, "0/3", False, [])],
    t_resub_n="再提出 1回",
    t_stu_fb_h="AIフィードバックの提出", t_stu_fb_sub="この生徒のAIフィードバックLOの提出と返却",
    t_stu_ov=[("rateReview", "blue", "提出", "3", "/ 3 LO", ""), ("checkCircle", "green", "返却済み", "2", "", "うち自動返却 1"), ("schedule", "orange", "確認待ち", "1", "", ""),
              ("autorenew", "", "再提出", "1", "回", "第6回 演習レポート"), ("description", "", "受けたコメント", "8", "", "良い点 3 ・ 改善点 5"), ("checks", "", "再提出で修正した指摘", "2", "/ 3", "第6回 1回目 → 2回目")],
    t_stu_fb_cols=["LO名", "状態", "提出日時", "返却日時", "コメント", ""],
    t_stu_fb_rows=[("第7回 演習レポート", "2026/11/14 09:12", "ir", "", "3", "--", "--", "確認する"),
                   ("第7週 週次リフレクション", "2026/11/15 20:11", "ret", "auto", "2", "--", "2026/11/16 00:05", "見る"),
                   ("第6回 演習レポート", "2026/11/09 13:02", "ret", "resub", "3", "2回目", "2026/11/10 17:40", "見る")],
    t_prof_h="観点別の傾向", t_prof_sub="返却済みコメントの観点ごとの内訳（良い点 ・ 改善点 ・ 再提出で修正）",
    t_prof_rows=[("統計処理", 0, 2, 1), ("解釈", 1, 1, 1), ("図表の見やすさ", 1, 0, 0), ("論理構成", 0, 1, 0), ("Excelスキル", 1, 0, 0), ("生成AIリテラシー", 0, 1, 0)],
    t_prof_lbl=("良い点", "改善点", "修正済み"),
    t_titles={"book": "BO — ブック管理（ブック詳細）", "dialog": "BO — LOを追加（AIフィードバック）", "created": "BO — 作成後のツリー",
              "mat": "BO — LO 内容（教材と提出条件）", "queue": "BO — コース › 提出物の採点", "det": "BO — 提出状況 概要", "list": "BO — 提出一覧", "rev": "BO — 確認して返却",
              "dg": "BO — グループダッシュボード", "ds": "BO — 生徒ダッシュボード"},
)
TEN = dict(
    t_lang="en", t_org="LMS 2.0",
    t_nav=["Dashboard", "AI Tutor", "Student", "Course", "Learning Material", "Lesson", "Calendar", "Notification", "Staff"],
    t_nav_sub=["Book", "Study Plan Stats", "Content Bank"],
    t_user="HTN Admin (LMS 2.0)", t_user_sub="LMS 2.0 · Group (+6) · Tokyo", t_testing="FOR TESTING",
    t_bm="Book Management", t_book="Regional & Environmental Statistics — Textbook (2026)", t_pub="Published", t_unpub="Unpublished",
    t_topics="Topic(s)", t_add_chapter="Add chapter", t_add_topic="Add topic", t_add_lo="Add LO",
    t_ch6="Session 6 · Organising data and averages", t_ch7="Session 7 · Data analysis and hypothesis testing", t_ch8="Session 8 · Regression analysis",
    t_tp71="7-1 · Correlation analysis", t_tp72="7-2 · Hypothesis testing",
    t_los=[("Session 7 lecture video", "link", False), ("Session 7 lecture slides", "lo", False), ("Session 7 check-up quiz", "lo", True)],
    t_new_lo="Session 7 exercise report", t_snack="You have created a new LO successfully.",
    t_dlg_title="Add Learning Objective", t_dlg_general="General Info", t_dlg_settings="Settings", t_dlg_select="Select LO Type",
    t_types=["Random Activity", "Learning Objective", "Flash Card", "Recording Assignment", "Practice Submission", "External Content"],
    t_type_fb="AI Feedback", t_new="NEW",
    t_f_name="Learning Objective", t_ph_name="Enter LO Name", t_f_ext="External LO ID", t_ph_ext="Alphanumeric characters only",
    t_f_desc="Assignment description (shown to students)",
    t_v_desc="Choose two variables from the Statistics Bureau's prefectural social indicators, compute the correlation coefficient in Excel and draw a scatter plot. Submit about two A4 pages covering your interpretation and the test of significance.",
    t_s_when="Availability and submission window", t_f_start="Opens", t_v_start="6 Nov 2026, 09:00", t_f_due="Due", t_v_due="13 Nov 2026, 23:59",
    t_when_note="It appears in the student's To-do when it opens. They can submit and replace their work until the due date; you review after it.",
    t_f_resub="Allow resubmission", t_v_resub="until 20 Nov 2026, 23:59",
    t_s_how="How students submit", t_how=["File (PDF · Word · Excel · PowerPoint)", "Photos (several at once)", "Typed answer"],
    t_how_limit="500-character limit",
    t_s_review="Teacher review", t_review_on="I review the feedback before it is returned",
    t_review_body="The draft is written after the due date and stays hidden until you review, edit and return it. Students receive it as feedback from you.",
    t_review_off="Feedback is returned to students automatically after the due date, without a review step.",
    t_cancel="Cancel", t_confirm="Confirm",
    t_lo_tabs=["Content", "Settings"], t_course_tabs=["Overview", "Submissions"], t_publish="Publish", t_edit="Edit settings", t_save="Save",
    t_nav_course=["Course Management", "Study Plan Management", "Submission Grading", "AI Grading"], t_toreview="Submission Grading", t_f_type="Type",
    t_course="Course", t_course_name="Regional & Environmental Statistics (2026)", t_view_subs="View submissions", t_edit_in_bm="Edit in Book Management",
    t_queue_sub="Submissions waiting on you. AI Feedback drafts queue here until you review them, alongside manual grading.",
    t_queue_cols=["LO", "Course", "Due", "Submitted", "Waiting for you", "Returned", ""], t_open="Open", t_f_course="Course", t_filters="Filters",
    t_queue=[("Session 7 exercise report", "13 Nov, 23:59", "12 / 30", "12", "9"), ("Week 7 weekly reflection", "15 Nov, 23:59", "21 / 30", "0", "21"),
             ("Session 6 exercise report", "6 Nov, 23:59", "30 / 30", "0", "30")],
    t_s_mat="Material for this assignment", t_mat_note="The submission requirements and the comment criteria are extracted from what you upload.",
    t_drop="Drag and drop a file, or choose one", t_drop_types="PDF · Word · PNG · JPG",
    t_file1="Session7_assignment_brief.pdf", t_file2="Marking_criteria_2026.docx",
    t_extract="Generate requirements and criteria", t_extracted="Generated",
    t_s_cond="Basic requirements", t_cond_note="Shown on the student's submit screen and checked as soon as they choose a file.",
    t_conds=[("A scatter plot is included", "brief p.1"), ("The correlation coefficient is stated", "brief p.1"),
             ("The test of significance is stated", "brief p.2"), ("The lecture material is cited", "criteria 2.(3)"),
             ("About 2 pages", "brief p.1")],
    t_add_cond="Add a requirement", t_req_ph="e.g. The data source is cited", t_req_src_me="Added by you", t_add="Add", t_req_toggle="Check requirements before submission",
    t_req_off="Off: the requirements are not shown to the student and nothing is checked at submission.",
    t_s_crit="Comment criteria (rubric)",
    t_crit_note="Each submission is read against these criteria, and every comment is tagged with the one it concerns.",
    t_rubric_h="Rubric",
    t_rubric=[("Excel skills", "Computes the correlation coefficient correctly with functions and formulas"), ("Clarity of charts", "A scatter plot with labelled axes, units and a title"),
              ("Statistical processing", "Shows the coefficient and the test of significance in the right order"), ("Interpretation", "Interprets the result while distinguishing correlation from causation"),
              ("Logical structure", "Purpose, method, results and discussion follow in sequence"), ("Generative-AI literacy", "Handles any use of generative AI appropriately and writes in their own words")],
    t_regen="Regenerate", t_edit_rubric="Edit", t_preview="Preview what the student sees",
    t_s_status="Submissions", t_st1="Submitted", t_st1_n="12 / 30", t_st1_s="12 of 30 students have submitted",
    t_st2="Not Reviewed", t_st2_n="8", t_st2_s="Drafts are ready. Review them and return", t_st3="Returned", t_st3_n="3 / 30", t_st3_s="Returned to 3 of 30 students",
    t_open_list="Review (8)",
    t_s_sum="Settings", t_sum=[("Window", "6 Nov 09:00 — 13 Nov 23:59"), ("Resubmission", "until 20 Nov 23:59"),
                               ("Submission", "File · Photos · Typed"), ("Teacher review", "On — before it is returned"),
                               ("Requirements", "5"), ("Criteria", "6")],
    t_cols=["Student", "Submitted", "Status", ""], t_bulk="Bulk Action", t_bulk_note="Reading them first is the safer habit",
    t_rows=[("Hanako Yamada", "11 Nov, 14:32", "wait", "Waiting for you"), ("Taro Sato", "11 Nov, 18:05", "wait", "Waiting for you"),
            ("Ichiro Suzuki", "12 Nov, 08:12", "wait", "Waiting for you"), ("Misaki Tanaka", "12 Nov, 21:40", "done", "Returned"),
            ("Ken Takahashi", "—", "none", "Not submitted")],
    t_review_btn="Review", t_view="View", t_rows_of="1-5 of 30", t_rows_pp="Rows per page:",
    t_sg_invalid="Invalid Reviewers", t_sg_tabs=["Submissions", "Learning Objectives"], t_sg_search="Enter Submission ID, Student Name or LO Name", t_applied="You filter by", t_lo_type="LO Type", t_all="All",
    t_status={"nr": ("Not Reviewed", "st-default"), "ir": ("In Review", "st-warning"), "ret": ("Returned", "st-success"), "back": ("Sent Back", "st-error")},
    t_sec={"auto": "Auto-returned", "resub": "Resubmitted"},
    t_sg_cols=["Submission ID", "LO Name", "Student Name", "Username", "Ext. ID", "Course", "Book", "Reviewer", "Status", "Comments", "Submitted", "Reviewed Date", "Returned Date"],
    t_sg_cols_lo=["Submission ID", "Student Name", "Username", "Ext. ID", "Reviewer", "Status", "Comments", "Submitted", "Reviewed Date", "Returned Date"],
    t_teacher="Masayoshi Yasumoto",
    t_subs=[dict(id="FB-260911", lo="Session 7 exercise report", student="Hanako Yamada", user="hanako.yamada", ext="KU-2041", reviewer="Masayoshi Yasumoto", st="ir", sec="", n=3, sub="2026/11/14, 09:12", rev="--", ret="--"),
            dict(id="FB-260912", lo="Session 7 exercise report", student="Taro Sato", user="taro.sato", ext="KU-2042", reviewer="--", st="nr", sec="", n=3, sub="2026/11/11, 18:05", rev="--", ret="--"),
            dict(id="FB-260913", lo="Session 7 exercise report", student="Ichiro Suzuki", user="ichiro.suzuki", ext="KU-2043", reviewer="--", st="nr", sec="", n=3, sub="2026/11/12, 08:12", rev="--", ret="--"),
            dict(id="FB-260914", lo="Session 7 exercise report", student="Misaki Tanaka", user="misaki.tanaka", ext="KU-2044", reviewer="Masayoshi Yasumoto", st="ret", sec="", n=3, sub="2026/11/12, 21:40", rev="2026/11/14, 10:05", ret="2026/11/14, 10:05"),
            dict(id="FB-260915", lo="Week 7 weekly reflection", student="Hanako Yamada", user="hanako.yamada", ext="KU-2041", reviewer="--", st="ret", sec="auto", n=2, sub="2026/11/15, 20:11", rev="--", ret="2026/11/16, 00:05"),
            dict(id="FB-260916", lo="Week 7 weekly reflection", student="Ken Takahashi", user="ken.takahashi", ext="KU-2045", reviewer="--", st="ret", sec="auto", n=2, sub="2026/11/15, 22:47", rev="--", ret="2026/11/16, 00:05"),
            dict(id="FB-260917", lo="Session 6 exercise report", student="Taro Sato", user="taro.sato", ext="KU-2042", reviewer="Masayoshi Yasumoto", st="back", sec="", n=3, sub="2026/11/04, 17:20", rev="2026/11/07, 09:30", ret="--"),
            dict(id="FB-260918", lo="Session 6 exercise report", student="Taro Sato", user="taro.sato", ext="KU-2042", reviewer="--", st="nr", sec="resub", n=3, sub="2026/11/09, 13:02", rev="--", ret="--")],
    t_subs_extra=[dict(id="FB-260919", lo="Session 7 exercise report", student="Sakura Ito", user="sakura.ito", ext="KU-2046", reviewer="--", st="nr", sec="", n=3, sub="2026/11/13, 22:58", rev="--", ret="--")],
    t_comment="Comment", t_passage="The passage it refers to (from the submission)", t_recognised="Recognised text",
    t_reviewer_info="Reviewer Info", t_reviewer="Reviewer", t_auto_return="Auto-return", t_off="Off", t_sub_info="Submission Info", t_student_name="Student Name", t_submitted="Submitted", t_file="File",
    t_comments_h="Comments", t_drafts="Drafts", t_criteria="Criteria",
    t_rev_title="Review and return · Hanako Yamada", t_rev_meta="submitted 11 Nov, 14:32",
    t_rev_hidden="Not visible to the student", t_rev_left="Submission", t_rev_right="Draft feedback",
    t_rev_right_n="3 comments · 6 criteria", t_rev_note_h="A word from you (optional)",
    t_rev_note="Good catch recalculating without Tokyo. We will come back to point ② in the next class, so have your own view ready.",
    t_rev_edited="Edited", t_rev_edit="Edit", t_rev_drop="Delete", t_rev_back="Send back", t_rev_send="Approve and return",
    t_rev_count="1 of 3 comments edited",
    t_role_t="Teacher (BO)", t_role_s="Student", t_role_aria="Role shown",
    t_dash_tabs=["Group Dashboard", "Student Dashboard", "Real Time Dashboard", "AI Dashboard"],
    t_f_book="Book", t_apply="Apply", t_dash_chips=["Enrollment: Enrolled", "Duration: Active"], t_reset="Reset to default",
    t_ai_solved="Questions Solved via AI", t_ai_solved_n="1,284",
    t_ov=[("rateReview", "blue", "AI Feedback submissions", "41", "/ 90", "3 LOs · 30 students", "T-Queue"),
          ("schedule", "orange", "Waiting for review", "9", "", "drafts waiting on a teacher", "T-Queue"),
          ("checkCircle", "green", "Returned", "27", "", "21 of them auto-returned", None),
          ("autorenew", "", "Resubmissions", "4", "", "including 1 sent back", None),
          ("event", "", "Avg. time to return", "1.8", "days", "from due date to return", None)],
    t_dash_search="Search by Student Name", t_dash_modes=["Topic Dashboard", "LO Dashboard"], t_topic_lbl="Topic:",
    t_score_modes=["Latest Score", "Highest Score"], t_stu_name="Student Name",
    t_lo_kv=["Avg. Score", "Comp. Rate", "AI-answered questions"], t_fb_kv=["Submitted", "Waiting", "Returned"],
    t_completed="Completed", t_marking="Marking",
    t_matrix_help="You may click the score to view the list of submissions made by the student for the learning objective. Click an AI Feedback status to open it in Submission Grading.",
    t_mx_los=[("Session 7 lecture video", "comp", ("--", "28/30", "0")), ("Session 7 check-up quiz", "score", ("74", "26/30", "38")),
              ("Session 7 exercise report", "fb", ("12/30", "8", "3")), ("Week 7 weekly reflection", "fb", ("21/30", "0", "21"))],
    t_mx_students=[("Hanako Yamada", [("comp",), ("score", "9/10", False, False), ("fb", "ir", 3, ""), ("fb", "ret", 2, "auto")]),
                   ("Taro Sato", [("comp",), ("score", "6/10", True, False), ("fb", "nr", 3, ""), ("fb", "ret", 2, "auto")]),
                   ("Ichiro Suzuki", [("comp",), ("score", "7/10", False, False), ("fb", "nr", 3, ""), ("fb", "ret", 1, "auto")]),
                   ("Misaki Tanaka", [("comp",), ("score", "10/10", False, False), ("fb", "ret", 3, ""), ("fb", "ret", 2, "auto")]),
                   ("Ken Takahashi", [("none",), ("score", "4/10", False, True), ("none",), ("fb", "ret", 2, "auto")]),
                   ("Sakura Ito", [("comp",), ("score", "8/10", True, False), ("fb", "nr", 3, ""), ("none",)]),
                   ("Daiki Watanabe", [("comp",), ("score", "5/10", False, True), ("none",), ("fb", "ret", 2, "auto")])],
    t_crit_h="Comments by criterion · Session 7 exercise report", t_crit_sub="Share of the 12 drafts with an improvement comment on each criterion",
    t_crit_rows=[("Statistical processing", 8), ("Interpretation", 6), ("Clarity of charts", 4), ("Logical structure", 3), ("Excel skills", 2), ("Generative-AI literacy", 1)], t_crit_of=12,
    t_reqf_h="Requirements that stopped a submission", t_reqf_sub="Times a requirement was unmet when a file was chosen (fixed before submitting)",
    t_reqf_rows=[("The test of significance is stated", 9), ("A scatter plot is included", 4), ("About 2 pages", 3), ("The lecture material is cited", 2), ("The correlation coefficient is stated", 0)],
    t_times="×",
    t_stu_list="Student List",
    t_students=[("Hanako Yamada", "Year 3 · KU-2041"), ("Taro Sato", "Year 3 · KU-2042"), ("Ichiro Suzuki", "Year 3 · KU-2043"), ("Misaki Tanaka", "Year 2 · KU-2044"), ("Ken Takahashi", "Year 3 · KU-2045")],
    t_ind_cols=["Chapter Name", "Topic Name", "Study Date", "Average Score", "Completion"], t_sub_cols=["Learning Objective", "Latest Submission", "Latest Score", "Highest Score"],
    t_ind_rows=[("Session 6 · Organising data and averages", "6-1 · Frequency tables and histograms", "2026/10/23", 85, "3/3", False, []),
                ("Session 6 · Organising data and averages", "6-2 · Averages and dispersion", "2026/11/09", 80, "3/3", True,
                 [("Session 6 lecture video", "2026/10/28", "comp", "comp"), ("Session 6 check-up quiz", "2026/10/29", "8/10", "8/10"), ("Session 6 exercise report", "2026/11/09", "fb:ret", "resub")]),
                ("Session 7 · Data analysis and hypothesis testing", "7-1 · Correlation analysis", "2026/11/14", 90, "3/4", True,
                 [("Session 7 lecture video", "2026/11/08", "comp", "comp"), ("Session 7 lecture slides", "2026/11/08", "comp", "comp"), ("Session 7 check-up quiz", "2026/11/10", "9/10", "9/10"), ("Session 7 exercise report", "2026/11/14", "fb:ir", "--")]),
                ("Session 7 · Data analysis and hypothesis testing", "7-2 · Hypothesis testing", "2026/11/15", -1, "1/2", False, []),
                ("Session 8 · Regression analysis", "8-1 · Simple regression", "--", -1, "0/3", False, [])],
    t_resub_n="1 resubmission",
    t_stu_fb_h="AI Feedback submissions", t_stu_fb_sub="This student's AI Feedback LOs: submissions and returns",
    t_stu_ov=[("rateReview", "blue", "Submitted", "3", "/ 3 LOs", ""), ("checkCircle", "green", "Returned", "2", "", "1 of them auto-returned"), ("schedule", "orange", "Waiting for review", "1", "", ""),
              ("autorenew", "", "Resubmissions", "1", "", "Session 6 exercise report"), ("description", "", "Comments received", "8", "", "3 strengths · 5 to improve"), ("checks", "", "Points fixed on resubmission", "2", "/ 3", "Session 6, draft 1 → 2")],
    t_stu_fb_cols=["LO Name", "Status", "Submitted", "Returned Date", "Comments", ""],
    t_stu_fb_rows=[("Session 7 exercise report", "2026/11/14, 09:12", "ir", "", "3", "--", "--", "Review"),
                   ("Week 7 weekly reflection", "2026/11/15, 20:11", "ret", "auto", "2", "--", "2026/11/16, 00:05", "View"),
                   ("Session 6 exercise report", "2026/11/09, 13:02", "ret", "resub", "3", "2nd", "2026/11/10, 17:40", "View")],
    t_prof_h="By criterion", t_prof_sub="Returned comments for this student, per criterion (strengths · to improve · fixed on resubmission)",
    t_prof_rows=[("Statistical processing", 0, 2, 1), ("Interpretation", 1, 1, 1), ("Clarity of charts", 1, 0, 0), ("Logical structure", 0, 1, 0), ("Excel skills", 1, 0, 0), ("Generative-AI literacy", 0, 1, 0)],
    t_prof_lbl=("Strengths", "To improve", "Fixed"),
    t_titles={"book": "BO — Book Management (book detail)", "dialog": "BO — Add LO (AI Feedback)", "created": "BO — Tree after creating",
              "mat": "BO — LO content (material and requirements)", "queue": "BO — Course › Submission Grading", "det": "BO — Submissions overview", "list": "BO — Submissions", "rev": "BO — Review and return",
              "dg": "BO — Group Dashboard", "ds": "BO — Student Dashboard"},
)
JA.update(TJA); EN.update(TEN)

TSCREENS = ["T-Book", "T-Dialog", "T-Material", "T-Created", "T-Queue", "T-Detail", "T-List", "T-Review", "T-DashGroup", "T-DashStudent"]

def tfn(screen, lang):
    return f"{screen}.dc.html" if lang == "ja" else f"{screen}-en.dc.html"

def role_toggle(S):
    """Prototype-only: jump between the teacher's Back Office and the student's screen.
    It sits in the drawer, in flow, so it never covers the page's own controls."""
    L = S["t_lang"]
    student = f'<a class="dev-i" href="{fn("Main", L)}">{S["t_role_s"]}</a>'
    teacher = f'<span class="dev-i on">{S["t_role_t"]}</span>'
    return f'<div class="dev" role="group" aria-label="{S["t_role_aria"]}">{teacher}{student}</div>'

def tnav(S, side="book"):
    """The drawer, as the live LMS 2.0 tenant shows it. Course and Learning Material stay
    open, as production keeps its open groups; the active child is ブック管理 on the
    set-up boards and コース › 要確認 (To Review) on the submission boards."""
    L = S["t_lang"]
    icons = ["dashboard", "aiTutor", "people", "library", "reader", "video", "event", "bell", "person"]
    groups = {2, 3, 4, 5, 7, 8}
    opened = {3, 4}
    out = ""
    for i, label in enumerate(S["t_nav"]):
        branch = " branch" if (i == 4 and side == "book") or (i == 3 and side == "course") else ""
        if i == 0 and side == "dash":
            branch = " on"
        caret = f'<span class="caret">{mi("expandLess" if i in opened else "expandMore", 20)}</span>' if i in groups else ""
        lb = f'<a class="lb" href="{tfn("T-DashGroup", L)}" style="color:inherit">{label}</a>' if i == 0 else f'<span class="lb">{label}</span>'
        out += f'<div class="tn{branch}"><span class="mi">{mi(icons[i], 22)}</span>{lb}{caret}</div>'
        if i == 3:
            for j, sub in enumerate(S["t_nav_course"]):
                on = " on" if (j == 2 and side == "course") else ""
                lb = f'<a class="lb" href="{tfn("T-Queue", L)}" style="color:inherit">{sub}</a>' if j == 2 else f'<span class="lb">{sub}</span>'
                out += f'<div class="tn child{on}"><span class="mi"></span>{lb}</div>'
        if i == 4:
            for j, sub in enumerate(S["t_nav_sub"]):
                on = " on" if (j == 0 and side == "book") else ""
                lb = f'<a class="lb" href="{tfn("T-Book", L)}" style="color:inherit">{sub}</a>' if j == 0 else f'<span class="lb">{sub}</span>'
                out += f'<div class="tn child{on}"><span class="mi"></span>{lb}</div>'
    return f'''<nav class="tnav">
  <div class="torg"><div class="id"><span class="mark">m</span><span class="name">{S["t_org"]}</span></div><span class="ticon">{mi("collapseL", 24)}</span></div>
  <div class="tmenu-b">{out}</div>
  {role_toggle(S)}
  <div class="tuser"><span class="tav">H</span><span style="min-width:0"><b style="font-size:13px;display:block;font-weight:500">{S["t_user"]}</b><i style="font-style:normal;font-size:11px;color:#757575">{S["t_user_sub"]}</i></span></div>
</nav>'''

def tcrumbs(S, screen, parts):
    """Breadcrumb as the Back Office renders it (Book Management / Book / …), with the
    日本語 / English toggle and the tenant's FOR TESTING chip on the right."""
    items = []
    for i, (label, href) in enumerate(parts):
        if i: items.append('<span class="sep">/</span>')
        items.append(f'<a href="{href}">{label}</a>' if href else f'<span>{label}</span>')
    return (f'<div style="display:flex;align-items:flex-start;justify-content:space-between;gap:16px">'
            f'<div class="tcrumbs">{"".join(items)}</div>'
            f'<div class="tright">{lang_toggle(S, screen)}<span class="testing">{S["t_testing"]}</span></div></div>')

def tpage(S, screen, title, body, logic="renderVals(){ return {}; }"):
    return f'''<!doctype html>
<html lang="{S["t_lang"]}">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
{THELMET}
<div class="troot" style="width: 1440px; height: 900px;">
{body}
</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":900}}}}'>
class Component extends DCLogic {{
  {logic}
}}
</script>
</body>
</html>
'''

def tools(*names):
    return "".join(f'<span class="ticon sm{" dis" if n.endswith("!") else ""}">{mi(n.rstrip("!"), 18)}</span>' for n in names)

def lm_row(S, L, name, kind, ai=False, pub="published", created=False, href=None):
    icon = {"lo": "lo", "link": "link", "flash": "flash", "fb": "rateReview"}[kind]
    nm = f'<a class="nm" href="{href}">{name}</a>' if href else f'<span class="nm">{name}</span>'
    spark = f'<span class="ticon sm primary" title="AI Tutor">{mi("spark", 16)}</span>' if ai else ""
    chip = f'<span class="tchip {pub}">{S["t_pub"] if pub == "published" else S["t_unpub"]}</span>'
    return (f'<li class="lm{" just-created" if created else ""}"><span class="lm-type">{mi(icon, 16)}</span>{nm}{spark}{chip}'
            f'<span class="spc"></span><span class="ticon sm">{mi("more", 18)}</span></li>')

def book_tree(S, L, created=False, add_href=None):
    """BookDetail: chapter accordions → topic accordions → learning-material rows."""
    rows = "".join(lm_row(S, L, n, k, ai) for n, k, ai in S["t_los"])
    if created:
        rows += lm_row(S, L, S["t_new_lo"], "fb", False, "unpublished", created=True, href=tfn("T-Material", L))
    add_lo = (f'<a class="tbtn sm" href="{add_href}">{mi("add", 18)}{S["t_add_lo"]}</a>' if add_href
              else f'<span class="tbtn sm">{mi("add", 18)}{S["t_add_lo"]}</span>')
    def chapter(name, n, open_, body=""):
        return f'''<div class="acc{" open" if open_ else ""}">
      <div class="acc-sum"><span class="title">{name}</span><span class="tools"><span class="tchip filled">{n} {S["t_topics"]}</span>{tools("up", "down", "more")}</span></div>
      {f'<div class="acc-body">{body}</div>' if open_ else ""}
    </div>'''
    topic_open = f'''<div class="acc tp open">
        <div class="acc-sum"><span class="title">{S["t_tp71"]}</span><span class="tools">{tools("up!", "down", "more")}</span></div>
        <div class="acc-body">
          <ul class="lm-list">{rows}</ul>
          <div style="padding:4px 0 0 40px">{add_lo}</div>
        </div>
      </div>
      <div class="acc tp">
        <div class="acc-sum"><span class="title">{S["t_tp72"]}</span><span class="tools">{tools("up", "down!", "more")}</span></div>
      </div>
      <div style="padding:4px 0 0 32px"><span class="tbtn sm">{mi("add", 18)}{S["t_add_topic"]}</span></div>'''
    return chapter(S["t_ch6"], 2, False) + chapter(S["t_ch7"], 2, True, topic_open) + chapter(S["t_ch8"], 1, False)

def book_page(S, L, screen, created=False, add_href=None, extra=""):
    body = tnav(S) + f'''<div class="tmain">
<div class="tscroll">
  {tcrumbs(S, screen, [(S["t_bm"], "#"), (S["t_book"], None)])}
  <div class="tphead">
    <h1>{S["t_book"]}<span class="tchip published">{S["t_pub"]}</span></h1>
    <div class="acts"><span class="tbtn contained">{mi("add", 18)}{S["t_add_chapter"]}</span><span class="ticon">{mi("more", 24)}</span></div>
  </div>
  {book_tree(S, L, created=created, add_href=add_href)}
</div>
{extra}
</div>'''
    return body

def t_book(S, L):
    return tpage(S, "T-Book", S["t_titles"]["book"], book_page(S, L, "T-Book", add_href=tfn("T-Dialog", L)))

def t_created(S, L):
    return tpage(S, "T-Created", S["t_titles"]["created"], book_page(S, L, "T-Created", created=True, add_href=tfn("T-Dialog", L)))

TDLG_LOGIC = """state = { menu: false, review: true, resub: true, m0: true, m1: true, m2: true };
  renderVals() {
    const t = (k) => () => { const p = {}; p[k] = !this.state[k]; this.setState(p); };
    return {
      menuOpen: this.state.menu, toggleMenu: t("menu"),
      rv: this.state.review ? "on" : "", rvOff: !this.state.review, toggleRv: t("review"),
      rs: this.state.resub ? "on" : "", rsOn: this.state.resub, toggleRs: t("resub"),
      c0: this.state.m0 ? "on" : "", c1: this.state.m1 ? "on" : "", c2: this.state.m2 ? "on" : "",
      t0: t("m0"), t1: t("m1"), t2: t("m2"),
    };
  }"""

def field(label, value, required=False, placeholder=False, area=False, icon=None, extra=""):
    req = ' <span class="req">*</span>' if required else ""
    gr = f'<span class="gr">{mi(icon, 20)}</span>' if icon else ""
    cls = "in" + (" ph" if placeholder else "") + (" area" if area else "")
    return f'<label class="field"><span class="lbl">{label}{req}</span><span class="{cls}"{extra}>{value}{gr}</span></label>'

def t_dialog(S, L):
    # the type select: MUI Select rendered closed with AI Feedback chosen; click opens the option list
    types = "".join(f'<div class="it">{t}</div>' for t in S["t_types"])
    menu = f'''<sc-if value="{{{{menuOpen}}}}" hint-placeholder-val="{{{{false}}}}"><div class="tpop" style="left:0;top:44px;width:100%">
        {types}
        <div class="it sel"><span class="lm-type" style="width:22px;height:22px">{mi("rateReview", 14)}</span><b>{S["t_type_fb"]}</b><span class="tchip new">{S["t_new"]}</span></div>
      </div></sc-if>'''
    select = f'''<div style="position:relative">
      <button class="field" style="width:100%;text-align:left;background:none;border:0;padding:0;font:inherit;cursor:pointer" onClick="{{{{toggleMenu}}}}">
        <span class="lbl" style="color:#2196F3">{S["t_dlg_select"]} <span class="req">*</span></span>
        <span class="in" style="border-color:#2196F3;box-shadow:inset 0 0 0 1px #2196F3">{S["t_type_fb"]}<span class="gr">{mi("expandMore", 22)}</span></span>
      </button>{menu}</div>'''
    how = "".join(
        f'<button class="check {{{{c{i}}}}}" onClick="{{{{t{i}}}}}"><span class="cbx">{mi("check", 14, "#fff")}</span><span>{label}'
        + (f'<span class="helper" style="margin:0">{S["t_how_limit"]}</span>' if i == 2 else "") + '</span></button>'
        for i, label in enumerate(S["t_how"]))
    dialog = f'''<div class="tscrim">
  <div class="dlg">
    <div class="dlg-head"><h2>{S["t_dlg_title"]}</h2><a class="ticon" href="{tfn("T-Book", L)}" aria-label="{S["t_cancel"]}">{mi("close", 24)}</a></div>
    <div class="dlg-body">
      <div class="lm-section">
        <h3 class="sec-head">{S["t_dlg_general"]}</h3>
        <div class="lm-grid">
          {select}
          {field(S["t_f_name"], S["t_new_lo"], required=True)}
          <div class="span2">{field(S["t_f_desc"], S["t_v_desc"], area=True)}</div>
          {field(S["t_f_ext"], S["t_ph_ext"], placeholder=True)}
        </div>
      </div>
      <div class="lm-section">
        <h3 class="sec-head">{S["t_dlg_settings"]}</h3>
        <div class="settings-list">
          <div class="setting">
            <span class="setting-label" style="font-weight:500">{S["t_s_when"]}</span>
            <div class="lm-grid" style="margin-top:10px">
              {field(S["t_f_start"], S["t_v_start"], icon="calendar")}
              {field(S["t_f_due"], S["t_v_due"], icon="calendar")}
            </div>
            <p class="hint">{S["t_when_note"]}</p>
            <div style="display:flex;align-items:center;gap:16px;margin-top:4px">
              <button class="switch {{{{rs}}}}" onClick="{{{{toggleRs}}}}"><span class="track"></span><span>{S["t_f_resub"]}</span></button>
              <sc-if value="{{{{rsOn}}}}" hint-placeholder-val="{{{{true}}}}"><span class="in" style="display:inline-flex;align-items:center;gap:8px;height:34px;padding:0 12px;border:1px solid #BDBDBD;border-radius:4px;font-size:13px">{S["t_v_resub"]}{mi("calendar", 16, "rgba(0,0,0,.54)")}</span></sc-if>
            </div>
          </div>
          <div class="setting">
            <span class="setting-label" style="font-weight:500">{S["t_s_how"]}</span>
            <div style="display:flex;flex-direction:column;gap:2px;margin-top:4px">{how}</div>
          </div>
          <div class="setting">
            <span class="setting-label" style="font-weight:500">{S["t_s_review"]}</span>
            <button class="switch {{{{rv}}}}" onClick="{{{{toggleRv}}}}"><span class="track"></span><span>{S["t_review_on"]}</span></button>
            <sc-if value="{{{{rvOff}}}}" hint-placeholder-val="{{{{false}}}}"><div class="alert info">{mi("info", 20, "#2196F3")}<span>{S["t_review_off"]}</span></div></sc-if>
          </div>
        </div>
      </div>
    </div>
    <div class="dlg-foot"><a class="tbtn" href="{tfn("T-Book", L)}">{S["t_cancel"]}</a><a class="tbtn contained" href="{tfn("T-Material", L)}">{S["t_confirm"]}</a></div>
  </div>
</div>'''
    return tpage(S, "T-Dialog", S["t_titles"]["dialog"], book_page(S, L, "T-Dialog", extra=dialog), logic=TDLG_LOGIC)

def lo_head(S, L, screen, tab, pub, side="book"):
    """The LO's page header. Book Management (side="book") sets the LO up: Content and
    Settings tabs, Publish as an action, a link out to its submissions. Course › To
    Review (side="course") processes them: Overview and Submissions tabs, a link back
    to Book Management to edit (PM, 19 Sep: Book Management is for setting up LOs, not
    for the student submission flows)."""
    status = f'<span class="tchip {"published" if pub else "unpublished"}">{S["t_pub"] if pub else S["t_unpub"]}</span>'
    if side == "book":
        crumbs = [(S["t_bm"], tfn("T-Book", L)), (S["t_book"], tfn("T-Created" if not pub else "T-Book", L)), (S["t_new_lo"], None)]
        tabs_src = S["t_lo_tabs"]
        acts = (f'<a class="tbtn" href="{tfn("T-Detail", L)}">{mi("people", 18)}{S["t_view_subs"]}</a>'
                f'<span class="tbtn outlined">{mi("edit", 18)}{S["t_edit"]}</span>' +
                ("" if pub else f'<span class="tbtn contained">{S["t_publish"]}</span>'))
        sub = ""
    else:
        crumbs = [(S["t_course"], "#"), (S["t_toreview"], tfn("T-Queue", L)), (S["t_new_lo"], None)]
        tabs_src = S["t_course_tabs"]
        acts = f'<a class="tbtn outlined" href="{tfn("T-Created", L)}">{mi("edit", 18)}{S["t_edit_in_bm"]}</a>'
        sub = f'<p class="helper" style="margin:-16px 0 20px;font-size:13px">{S["t_course_name"]} {S["sep"]} {S["t_book"]} {S["sep"]} {S["t_ch7"]}</p>'
    tabs = "".join(f'<span class="tab{" on" if i == tab else ""}">{t}</span>' for i, t in enumerate(tabs_src))
    return f'''{tcrumbs(S, screen, crumbs)}
  <div class="tphead">
    <h1>{S["t_new_lo"]}<span class="tchip type">{mi("rateReview", 14)}{S["t_type_fb"]}</span>{status}</h1>
    <div class="acts">{acts}<span class="ticon">{mi("more", 24)}</span></div>
  </div>{sub}
  <div class="tabs">{tabs}</div>'''

TMAT_LOGIC = """state = { req: true, adding: false, draft: "", r: [true, true, true, true, true], a: ["", "", ""] };
  renderVals() {
    const v = { rq: this.state.req ? "on" : "", rqOn: this.state.req, rqOff: !this.state.req,
                toggleRq: () => this.setState({ req: !this.state.req }),
                adding: this.state.adding, draft: this.state.draft,
                addDis: this.state.draft.trim() ? "" : "dis",
                startAdd: () => this.setState({ adding: true }),
                cancelAdd: () => this.setState({ adding: false, draft: "" }),
                onDraft: (e) => this.setState({ draft: e.target.value || "" }),
                commitAdd: () => {
                  const t = this.state.draft.trim(); if (!t) return;
                  const a = this.state.a.slice(); const i = a.indexOf("");
                  if (i >= 0) a[i] = t;
                  this.setState({ a, adding: false, draft: "" });
                } };
    this.state.r.forEach((on, i) => { v["r" + i] = on; v["d" + i] = () => { const r = this.state.r.slice(); r[i] = false; this.setState({ r }); }; });
    this.state.a.forEach((t, j) => { v["a" + j + "on"] = !!t; v["a" + j] = t; v["da" + j] = () => { const a = this.state.a.slice(); a[j] = ""; this.setState({ a }); }; });
    return v;
  }"""

def t_material(S, L):
    conds = "".join(f'<sc-if value="{{{{r{i}}}}}" hint-placeholder-val="{{{{true}}}}"><div class="titem">{mi("checkCircle", 20, "#4CAF50")}<span>{c}</span><span class="src">{s}</span>'
                    f'<button class="ticon sm" onClick="{{{{d{i}}}}}" aria-label="{S["t_rev_drop"]}">{mi("close", 16)}</button></div></sc-if>'
                    for i, (c, s) in enumerate(S["t_conds"]))
    # rows the teacher adds by hand, up to three in the prototype
    conds += "".join(f'<sc-if value="{{{{a{j}on}}}}" hint-placeholder-val="{{{{false}}}}"><div class="titem">{mi("checkCircle", 20, "#4CAF50")}<span>{{{{a{j}}}}}</span><span class="src">{S["t_req_src_me"]}</span>'
                     f'<button class="ticon sm" onClick="{{{{da{j}}}}}" aria-label="{S["t_rev_drop"]}">{mi("close", 16)}</button></div></sc-if>' for j in range(3))
    conds += f'''<sc-if value="{{{{adding}}}}" hint-placeholder-val="{{{{false}}}}"><div class="titem" style="gap:8px;border-bottom:0;padding-top:12px">
            <input id="req-new" class="tinput" placeholder="{S["t_req_ph"]}" defaultValue="{{{{draft}}}}" onInput="{{{{onDraft}}}}">
            <button class="tbtn contained sm {{{{addDis}}}}" onClick="{{{{commitAdd}}}}">{S["t_add"]}</button>
            <button class="tbtn sm" onClick="{{{{cancelAdd}}}}">{S["t_cancel"]}</button>
          </div></sc-if>'''
    rubric = "".join(f"<li><b>{n}</b> — {d}</li>" for n, d in S["t_rubric"])
    body = tnav(S) + f'''<div class="tmain">
<div class="tscroll" style="padding-bottom:20px">
  {lo_head(S, L, "T-Material", 0, pub=False)}
  <div style="display:flex;flex-direction:column;gap:16px">
    <div class="tpaper">
      <div class="ph"><h3>{S["t_s_mat"]}</h3><span class="helper" style="margin:0">{S["t_mat_note"]}</span></div>
      <div class="pb" style="display:flex;flex-direction:column;gap:14px">
        <div class="tdrop">{mi("cloudUp", 22)}{S["t_drop"]}<span style="color:#757575;font-weight:400">{S["sep"]} {S["t_drop_types"]}</span></div>
        <div style="display:flex;align-items:center;gap:10px;flex-wrap:wrap">
          <span class="tfile"><span class="fi" style="background:#FEEBEE;color:#C62828">{mi("description", 18)}</span>{S["t_file1"]}<span class="ticon sm">{mi("close", 16)}</span></span>
          <span class="tfile"><span class="fi" style="background:#E3F2FD;color:#0B79D0">{mi("description", 18)}</span>{S["t_file2"]}<span class="ticon sm">{mi("close", 16)}</span></span>
          <span class="tbtn outlined" style="margin-left:6px">{mi("spark", 18)}{S["t_extract"]}</span>
          <span class="tchip published">{mi("check", 14)}{S["t_extracted"]}</span>
        </div>
      </div>
    </div>
    <div class="tpaper">
      <div class="ph"><h3>{S["t_s_cond"]}</h3>
        <span style="display:flex;align-items:center;gap:16px">
          <button class="switch {{{{rq}}}}" onClick="{{{{toggleRq}}}}"><span class="track"></span><span>{S["t_req_toggle"]}</span></button>
          <sc-if value="{{{{rqOn}}}}" hint-placeholder-val="{{{{true}}}}"><button class="tbtn sm" onClick="{{{{startAdd}}}}">{mi("add", 18)}{S["t_add_cond"]}</button></sc-if>
        </span></div>
      <sc-if value="{{{{rqOn}}}}" hint-placeholder-val="{{{{true}}}}"><div class="pb" style="padding-top:8px"><p class="helper" style="margin:0 0 6px">{S["t_cond_note"]}</p>{conds}</div></sc-if>
      <sc-if value="{{{{rqOff}}}}" hint-placeholder-val="{{{{false}}}}"><div class="pb"><p class="helper" style="margin:0">{S["t_req_off"]}</p></div></sc-if>
    </div>
    <div class="tpaper">
      <div class="ph"><h3>{S["t_s_crit"]}</h3><span style="display:flex;gap:4px"><span class="tbtn sm">{mi("autorenew", 18)}{S["t_regen"]}</span><span class="tbtn sm">{mi("edit", 18)}{S["t_edit_rubric"]}</span></span></div>
      <div class="pb"><p class="helper" style="margin:0 0 12px">{S["t_crit_note"]}</p>
        <div class="trubric"><h5>{S["t_rubric_h"]}</h5><ol>{rubric}</ol></div></div>
    </div>
  </div>
</div>
<div class="snack" role="status">{mi("checkCircle", 20)}{S["t_snack"]}</div>
<div class="tbar">
  <a class="tbtn" href="{fn("02-Assignment", L)}">{mi("eye", 18)}{S["t_preview"]}</a>
  <span style="display:flex;gap:8px"><a class="tbtn" href="{tfn("T-Created", L)}">{S["t_cancel"]}</a><a class="tbtn contained" href="{tfn("T-Created", L)}">{S["t_save"]}</a></span>
</div>
</div>'''
    return tpage(S, "T-Material", S["t_titles"]["mat"], body, logic=TMAT_LOGIC)

def st_chip(S, key):
    """A grading-status chip in the Back Office's tone families (st-default / warning /
    secondary / success / error), with the AI Feedback statuses in place of the marking ones."""
    label, tone = S["t_status"][key]
    return f'<span class="tchip {tone}">{label}</span>'

def sg_filterbar(S, applied=None, bulk=True):
    """Submission Grading filter bar: search, Filters, the applied-filter chips, Bulk Action."""
    chips = "".join(f'<span class="tchip" style="padding-right:4px">{c}<span class="tx">{mi("close", 12, "#fff")}</span></span>' for c in (applied or []))
    app = f'<span class="tapplied">{S["t_applied"]} {chips}</span>' if applied else ""
    right = f'<span class="tbtn contained dis">{S["t_bulk"]}{mi("expandMore", 18)}</span>' if bulk else ""
    return f'''<div class="tfilterbar">
    <div class="left"><span class="tsearch">{mi("search", 20, "#757575")}<span>{S["t_sg_search"]}</span></span>
      <span class="tbtn neutral">{mi("shuffle", 18)}{S["t_filters"]}</span>{app}</div>
    <div class="right">{right}</div>
  </div>'''

def sg_segments(S, counts, active="all"):
    keys = ["all", "nr", "ir", "ret", "back"]
    labels = {"all": S["t_all"], **{k: S["t_status"][k][0] for k in ("nr", "ir", "ret", "back")}}
    return '<div class="tseg" role="group">' + "".join(
        f'<span class="{"on" if k == active else ""}">{labels[k]} ({counts[k]})</span>' for k in keys) + "</div>"

def sg_table(S, L, rows, cols, lo_col=True, minw=1560):
    """The Submission Grading table: select column, index, then the columns the reference
    renders, with the AI Feedback status (and a secondary chip) where the marking status sits."""
    head = f'<th class="cb"><span class="cbx-th"></span></th><th class="idx">#</th>' + "".join(f"<th>{c}</th>" for c in cols)
    trs = ""
    for i, r in enumerate(rows):
        sec = f'<span class="tchip st-secondary">{S["t_sec"][r["sec"]]}</span>' if r.get("sec") else ""
        dd = lambda v: f'<span class="dd">--</span>' if v == "--" else v
        cells = [f'<a class="cell-link num" href="{tfn("T-Review", L)}">{r["id"]}</a>']
        if lo_col:
            cells.append(f'<a class="cell-link" href="{tfn("T-Detail", L)}">{r["lo"]}</a>')
        cells += [r["student"], f'<span class="cell-muted">{r["user"]}</span>', f'<span class="cell-muted num">{r["ext"]}</span>']
        if lo_col:
            cells += [S["t_course_name"], f'<span class="cell-muted">{S["t_book"]}</span>']
        cells += [dd(r["reviewer"]), f'<span style="display:flex;gap:6px;flex-wrap:nowrap">{st_chip(S, r["st"])}{sec}</span>',
                  f'<span class="num">{r["n"]}</span>', f'<span class="num">{r["sub"]}</span>', f'<span class="num">{dd(r["rev"])}</span>', f'<span class="num">{dd(r["ret"])}</span>']
        trs += f'<tr><td class="cb"><span class="cbx-td"></span></td><td class="idx num">{i+1}</td>' + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
    return f'''<div class="tpaper" style="overflow:hidden">
    <div class="table-scroll"><table class="m" style="min-width:{minw}px"><thead><tr>{head}</tr></thead><tbody>{trs}</tbody></table></div>
    <div class="pagination"><span>{S["t_rows_pp"]} 10</span><span>1-{len(rows)} / {len(rows)}</span><span style="display:flex">{tools("expandMore!", "expandMore!")}</span></div>
  </div>'''

def t_queue(S, L):
    """Course › Submission Grading (ToReviewListPage), production's home for submissions
    waiting on the teacher: Submissions and Learning Objectives tabs, the filter bar, the
    grading-status segments with counts, and the wide table — here with an LO Type filter
    applied, so it reads as the existing queue filtered to AI Feedback, and with the AI
    Feedback statuses in the same tone families as the marking ones."""
    rows = S["t_subs"]
    counts = {"all": len(rows)}
    for k in ("nr", "ir", "ret", "back"):
        counts[k] = sum(1 for r in rows if r["st"] == k)
    body = tnav(S, "course") + f'''<div class="tmain">
<div class="tscroll">
  {tcrumbs(S, "T-Queue", [(S["t_course"], "#"), (S["t_toreview"], None)])}
  <div class="tphead">
    <h1>{S["t_toreview"]}</h1>
    <div class="acts"><span class="tbtn neutral">{mi("cloudUp", 18)}{S["t_sg_invalid"]}</span><span class="ticon">{mi("more", 24)}</span></div>
  </div>
  <div class="tabs">{"".join(f'<span class="tab{" on" if i == 0 else ""}">{t}</span>' for i, t in enumerate(S["t_sg_tabs"]))}</div>
  <div style="display:flex;flex-direction:column;gap:16px">
    {sg_filterbar(S, applied=[f'{S["t_lo_type"]}: {S["t_type_fb"]}'])}
    {sg_segments(S, counts)}
    {sg_table(S, L, rows, S["t_sg_cols"])}
  </div>
</div>
</div>'''
    return tpage(S, "T-Queue", S["t_titles"]["queue"], body)

def t_detail(S, L):
    def metric(icon, label, n, desc, hot=False, cta=""):
        return f'''<div class="metric{" hot" if hot else ""}">
      <div class="m-top"><span class="m-lbl">{mi(icon, 20)}{label}</span><span class="m-val"><b>{n}</b></span></div>
      <p class="m-desc">{desc}</p>{cta}
    </div>'''
    cta = f'<a class="tbtn contained sm" href="{tfn("T-List", L)}">{S["t_open_list"]}</a>'
    kv = "".join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in S["t_sum"])
    body = tnav(S, "course") + f'''<div class="tmain">
<div class="tscroll">
  {lo_head(S, L, "T-Detail", 0, pub=True, side="course")}
  <div style="display:flex;flex-direction:column;gap:16px">
    <div class="analysis">
      <h4>{S["t_s_status"]}</h4>
      <div class="grid">
        {metric("description", S["t_st1"], S["t_st1_n"], S["t_st1_s"])}
        {metric("schedule", S["t_st2"], S["t_st2_n"], S["t_st2_s"], hot=True, cta=cta)}
        {metric("checkCircle", S["t_st3"], S["t_st3_n"], S["t_st3_s"])}
      </div>
    </div>
    <div class="tpaper"><div class="ph"><h3>{S["t_s_sum"]}</h3><a class="tbtn sm" href="{tfn("T-Created", L)}">{mi("edit", 18)}{S["t_edit_in_bm"]}</a></div><div class="pb"><dl class="tkv">{kv}</dl></div></div>
  </div>
</div>
</div>'''
    return tpage(S, "T-Detail", S["t_titles"]["det"], body)

def t_list(S, L):
    """The LO's Submissions tab: the same Submission Grading table, scoped to one LO (no LO,
    course or book columns), with its own status counts."""
    rows = [r for r in S["t_subs"] if r["lo"] == S["t_new_lo"]] + S["t_subs_extra"]
    counts = {"all": len(rows)}
    for k in ("nr", "ir", "ret", "back"):
        counts[k] = sum(1 for r in rows if r["st"] == k)
    body = tnav(S, "course") + f'''<div class="tmain">
<div class="tscroll">
  {lo_head(S, L, "T-List", 1, pub=True, side="course")}
  <div style="display:flex;flex-direction:column;gap:16px">
    {sg_filterbar(S)}
    {sg_segments(S, counts)}
    {sg_table(S, L, rows, S["t_sg_cols_lo"], lo_col=False, minw=1180)}
  </div>
</div>
</div>'''
    return tpage(S, "T-List", S["t_titles"]["list"], body)

def t_review(S, L):
    """GradingScorePage's layout for one AI Feedback submission: the info panel on the left
    (submission id and secondary chip, reviewer, submission info, the teacher's note, the
    comment counts), the report on the right — the recognised submission, then the draft
    comments as items, each with its criterion, the passage it points at, and Edit / Delete."""
    sub = S["t_subs"][0]
    items = ""
    for i, (kind, crit, quote, bodytext, ref) in enumerate(S["cards"]):
        n = i + 1
        edited = (n == 3)
        items += f'''<div class="q-item{" edited" if edited else ""}">
      <div class="q-top"><span class="q-no">{S["t_comment"]} {n}</span><span class="badge {kind}"><i class="n">{n}</i>{S["labels"][kind]}</span><span class="tchip">{crit}</span>
        {f'<span class="tchip type">{S["t_rev_edited"]}</span>' if edited else ""}</div>
      <div class="q-answer"><span class="who">{S["t_passage"]}</span>{quote}</div>
      <p class="q-prompt">{bodytext}</p>
      <div class="tdacts"><span class="tbtn sm">{mi("edit", 16)}{S["t_rev_edit"]}</span><span class="tbtn sm danger">{mi("del", 16)}{S["t_rev_drop"]}</span></div>
    </div>'''
    raw = "".join(f'<p style="margin:0 0 10px">{p}</p>' for p in S["raw"])
    body = tnav(S, "course") + f'''<div class="tmain">
<div class="tscroll">
  {tcrumbs(S, "T-Review", [(S["t_course"], "#"), (S["t_toreview"], tfn("T-Queue", L)), (S["t_new_lo"], None)])}
  <div class="tphead">
    <h1>{S["t_new_lo"]}{st_chip(S, "ir")}</h1>
    <div class="acts"><a class="tbtn outlined" href="{tfn("T-List", L)}">{S["t_rev_back"]}</a><a class="tbtn contained" href="{tfn("T-List", L)}">{S["t_rev_send"]}</a><span class="ticon">{mi("more", 24)}</span></div>
  </div>
  <div class="grade-layout">
    <div class="info-panel">
      <div class="info-sec"><div style="display:flex;align-items:center;gap:8px"><span class="helper num" style="margin:0">{sub["id"]}</span><span class="tchip st-error">{mi("eyeOff", 12)}{S["t_rev_hidden"]}</span></div></div>
      <div class="info-sec">
        <h3>{S["t_reviewer_info"]}</h3>
        <dl class="info-rows"><dt>{S["t_reviewer"]}</dt><dd>{S["t_teacher"]}</dd><dt>{S["t_auto_return"]}</dt><dd>{S["t_off"]}</dd></dl>
      </div>
      <div class="info-sec">
        <h3>{S["t_sub_info"]}</h3>
        <dl class="info-rows"><dt>{S["t_student_name"]}</dt><dd>{sub["student"]}</dd><dt>{S["t_course"]}</dt><dd>{S["t_course_name"]}</dd>
          <dt>{S["t_submitted"]}</dt><dd class="num">{sub["sub"]}</dd><dt>{S["t_file"]}</dt><dd>{S["a_file"]}</dd></dl>
      </div>
      <div class="info-sec">
        <h3>{S["t_rev_note_h"]}</h3>
        {field("", S["t_rev_note"], area=True)}
      </div>
      <div class="info-sec">
        <h3>{S["t_comments_h"]}</h3>
        <dl class="info-rows"><dt>{S["t_drafts"]}</dt><dd class="num">3</dd><dt>{S["t_rev_edited"]}</dt><dd class="num">1</dd><dt>{S["t_criteria"]}</dt><dd class="num">6</dd></dl>
      </div>
    </div>
    <div class="report">
      <div class="report-head"><strong style="font-weight:500">{S["t_rev_right"]}</strong><span class="helper" style="margin:0">{S["t_rev_right_n"]}</span></div>
      <div class="q-item">
        <div class="q-top"><span class="q-no">{S["t_rev_left"]}</span><span class="q-title">{S["a_file"]}</span><span class="tchip">{S["t_recognised"]}</span></div>
        <div class="q-answer" style="margin-bottom:0">{raw}</div>
      </div>
      {items}
    </div>
  </div>
</div>
</div>'''
    return tpage(S, "T-Review", S["t_titles"]["rev"], body)

def dash_head(S, L, screen, tab):
    """Dashboard page head as the Back Office renders it: h1, the four dashboard tabs (Group /
    Student link to each other), with the language toggle and FOR TESTING chip on the right."""
    hrefs = [tfn("T-DashGroup", L), tfn("T-DashStudent", L), None, None]
    tabs = "".join(
        (f'<a class="tab{" on" if i == tab else ""}" href="{h}">{t}</a>' if h else f'<span class="tab">{t}</span>')
        for i, (t, h) in enumerate(zip(S["t_dash_tabs"], hrefs)))
    return f'''{tcrumbs(S, screen, [])}
  <div class="tphead" style="margin-bottom:8px"><h1>{S["t_nav"][0]}</h1></div>
  <div class="tabs">{tabs}</div>'''

def dash_filter(S):
    """Course / Book selects, Filters, a divider, Apply — GroupDashboard's filter row."""
    return f'''<div class="dash-filter">
    <div class="fld">{field(S["t_course"], f'<span class="ell">{S["t_course_name"]}</span>', icon="expandMore")}</div>
    <div class="fld">{field(S["t_f_book"], f'<span class="ell">{S["t_book"]}</span>', icon="expandMore")}</div>
    <span class="tbtn neutral">{mi("filter", 18)}{S["t_filters"]}</span><span class="vr"></span>
    <span class="tbtn contained">{S["t_apply"]}</span>
  </div>'''

def ov_card(icon, tone, label, val, unit, sub, href=None, L="ja"):
    body = (f'<span class="ic{" " + tone if tone else ""}">{mi(icon, 22)}</span>'
            f'<span style="min-width:0"><span class="lbl-sm">{label}</span><span class="val">{val}{f"<small>{unit}</small>" if unit else ""}</span>'
            f'{f"<span class=sub>{sub}</span>" if sub else ""}</span>')
    if href:
        return f'<a class="ov-card{" hot" if tone == "orange" else ""}" href="{tfn(href, L)}" style="color:inherit">{body}</a>'
    return f'<div class="ov-card">{body}</div>'

def progress(v, tone=None):
    if v is None or v < 0:
        return '<span class="dd">--</span>'
    cls = tone if tone else ("good" if v > 50 else "warn")
    return f'<span class="progress"><span class="pct">{v}%</span><span class="bar"><i class="{cls}" style="width:{v}%"></i></span></span>'

def t_dash_group(S, L):
    """GroupDashboard in LO Dashboard mode, on topic 7-1: the production overview tile
    (Questions Solved via AI) with the AI Feedback overview beside it, then the student × LO
    matrix — regular LOs show Completed or a score as production does, the AI Feedback LOs show
    the submission status in the marking tones, with the comment count and a link into
    Submission Grading. Below, what the class missed: comments by criterion and the
    requirements that stopped a submission."""
    chips = "".join(f'<span class="tchip" style="padding-right:4px">{c}<span class="tx">{mi("close", 12, "#fff")}</span></span>' for c in S["t_dash_chips"])
    cards = ov_card("spark", "blue", S["t_ai_solved"], S["t_ai_solved_n"], "", "") + "".join(
        ov_card(*c[:6], href=c[6], L=L) for c in S["t_ov"])
    # LO column headers
    heads = ""
    for name, kind, (a, b, c) in S["t_mx_los"]:
        if kind == "fb":
            k1, k2, k3 = S["t_fb_kv"]
            nm = f'<a class="lo-name" href="{tfn("T-Detail", L)}" title="{name}"><span class="lm-type" style="width:20px;height:20px;flex:0 0 20px">{mi("rateReview", 12)}</span><span>{name}</span></a>'
            kv = (f'<span class="kv-line">{k1}: <b>{a}</b></span><span class="kv-line">{k2}: <b><a href="{tfn("T-List", L)}">{b}</a></b></span>'
                  f'<span class="kv-line">{k3}: <b>{c}</b></span>')
        else:
            k1, k2, k3 = S["t_lo_kv"]
            nm = f'<span class="lo-name" title="{name}"><span>{name}</span></span>'
            kv = f'<span class="kv-line">{k1}: <b>{a}</b></span><span class="kv-line">{k2}: <b><a href="#">{b}</a></b></span><span class="kv-line">{k3}: <b>{c}</b></span>'
        heads += f'<th><div class="lo-col">{nm}{kv}</div></th>'
    def cell(c):
        if c[0] == "none":
            return '<span class="stat-cell miss"><span class="dd">--</span></span>'
        if c[0] == "comp":
            return f'<span class="stat-cell"><span class="tchip published">{S["t_completed"]}</span><span class="grow">{mi("history", 16)}</span></span>'
        if c[0] == "score":
            _, sc, ai, failed = c
            spark = f'<span title="AI Tutor">{mi("spark", 16)}</span>' if ai else ""
            return f'<span class="stat-cell{" miss" if failed else ""}"><span class="score">{sc}</span><span class="grow">{spark}{mi("history", 16)}</span></span>'
        _, st, n, sec = c
        sec_chip = f'<span class="tchip st-secondary" style="height:20px;padding:0 6px;font-size:11px">{S["t_sec"][sec]}</span>' if sec else ""
        return (f'<a class="stat-cell" href="{tfn("T-List", L)}" style="color:inherit">{st_chip(S, st)}{sec_chip}'
                f'<span class="grow"><span class="cnt">{mi("rateReview", 14, "#757575")}{n}</span>{mi("history", 16)}</span></a>')
    rows = "".join(
        f'<tr><td class="stu-col"><div class="stu-cell"><a class="cell-link" href="{tfn("T-DashStudent", L)}">{name}</a></div></td>'
        + "".join(f'<td>{cell(c)}</td>' for c in cells) + '</tr>'
        for name, cells in S["t_mx_students"])
    crit = "".join(
        f'<div class="crit-row"><span>{c}</span>{progress(round(n * 100 / S["t_crit_of"]), None)}<span class="n">{n} / {S["t_crit_of"]}</span></div>'
        for c, n in S["t_crit_rows"])
    mx = max(n for _, n in S["t_reqf_rows"])
    reqf = "".join(
        f'<div class="crit-row"><span>{c}</span><span class="progress"><span class="pct"></span><span class="bar"><i style="width:{round(n * 100 / mx)}%;background:#9E9E9E"></i></span></span><span class="n">{n} {S["t_times"]}</span></div>'
        for c, n in S["t_reqf_rows"])
    body = tnav(S, "dash") + f'''<div class="tmain">
<div class="tscroll">
  {dash_head(S, L, "T-DashGroup", 0)}
  <div style="display:flex;flex-direction:column;gap:24px">
    <div>{dash_filter(S)}<div class="chiplist">{chips}<a href="#" style="margin-left:4px">{S["t_reset"]}</a></div></div>
    <div class="tpaper" style="padding:16px">
      <div class="ov-row">{cards}</div>
      <div style="display:flex;align-items:center;justify-content:space-between;gap:16px">
        <span class="tsearch">{mi("search", 20, "#757575")}<span>{S["t_dash_search"]}</span></span>
        <span class="toggle-group"><span>{S["t_dash_modes"][0]}</span><span class="on">{S["t_dash_modes"][1]}</span></span>
      </div>
      <div style="display:flex;align-items:center;justify-content:space-between;gap:16px;margin:16px 0 12px">
        <span style="display:flex;align-items:center;gap:8px"><span class="cell-muted">{S["t_topic_lbl"]}</span><span class="tbtn neutral" style="height:34px;color:#212121">{S["t_tp71"]}{mi("expandMore", 18, "#757575")}</span></span>
        <span class="toggle-group"><span class="on">{S["t_score_modes"][0]}</span><span>{S["t_score_modes"][1]}</span></span>
      </div>
      <div class="matrix"><table>
        <thead><tr><th class="stu-col"><div class="stu-head">{S["t_stu_name"]}</div></th>{heads}</tr></thead>
        <tbody>{rows}</tbody>
      </table></div>
      <p class="helper" style="margin:10px 0 0">{S["t_matrix_help"]}</p>
    </div>
    <div class="insight">
      <div class="tpaper"><div class="ph"><div><h3>{S["t_crit_h"]}</h3><span class="helper">{S["t_crit_sub"]}</span></div><a class="tbtn sm" href="{tfn("T-List", L)}">{S["t_view_subs"]}</a></div><div class="pb" style="padding:8px 20px">{crit}</div></div>
      <div class="tpaper"><div class="ph"><div><h3>{S["t_reqf_h"]}</h3><span class="helper">{S["t_reqf_sub"]}</span></div><a class="tbtn sm" href="{tfn("T-Material", L)}">{mi("edit", 16)}{S["t_edit_in_bm"]}</a></div><div class="pb" style="padding:8px 20px">{reqf}</div></div>
    </div>
  </div>
</div>
</div>'''
    return tpage(S, "T-DashGroup", S["t_titles"]["dg"], body)

def t_dash_student(S, L):
    """StudentDashboard: the student list on the left, the selected student's page on the
    right — filter row, the production chapter / topic table with its expandable LO rows
    (the AI Feedback LOs show their status where a score would be), then this student's AI
    Feedback overview: counts, the submissions with links into the review, and the by-criterion
    profile of the comments they received."""
    sel = S["t_students"][0]
    roster = "".join(
        f'<a class="sl-item{" on" if i == 0 else ""}" href="{tfn("T-DashStudent", L)}">{n}<span class="sl-sub">{g}</span></a>'
        for i, (n, g) in enumerate(S["t_students"]))
    def sub_val(v):
        if v == "comp":
            return S["t_completed"]
        if v == "--":
            return '<span class="dd">--</span>'
        if v == "resub":
            return f'<span class="cell-muted">{S["t_resub_n"]}</span>'
        if v.startswith("fb:"):
            return st_chip(S, v[3:])
        return v
    ind = ""
    for ch, tp, date, avg, comp, open_, los in S["t_ind_rows"]:
        ind += (f'<tr><td style="width:44px;padding-right:0"><span class="ticon sm">{mi("expandLess" if open_ else "expandMore", 20)}</span></td>'
                f'<td style="white-space:normal">{ch}</td><td style="white-space:normal">{tp}</td><td class="num">{date if date != "--" else "<span class=dd>--</span>"}</td>'
                f'<td style="width:170px">{progress(avg)}</td><td class="num" style="text-align:right">{comp}</td></tr>')
        if open_:
            inner = "".join(
                f'<tr><td>{n}</td><td class="num">{d}</td><td>{sub_val(a)}</td><td>{sub_val(b)}</td></tr>' for n, d, a, b in los)
            ind += (f'<tr class="sub"><td colspan="6"><table class="m inner"><thead><tr>'
                    + "".join(f'<th{" style=width:150px" if i else ""}>{c}</th>' for i, c in enumerate(S["t_sub_cols"]))
                    + f'</tr></thead><tbody>{inner}</tbody></table></td></tr>')
    cards = "".join(ov_card(*c) for c in S["t_stu_ov"])
    fb_rows = ""
    for lo, sub, st, sec, n, resub, ret, act in S["t_stu_fb_rows"]:
        sec_chip = f'<span class="tchip st-secondary">{S["t_sec"][sec]}</span>' if sec else ""
        attempt = f'<span class="cell-muted" style="display:block;font-size:12px">{S["t_sec"]["resub"]} {resub}</span>' if resub != "--" else ""
        fb_rows += (f'<tr><td><a class="cell-link" href="{tfn("T-Detail", L)}">{lo}</a>{attempt}</td>'
                    f'<td><span style="display:flex;gap:6px">{st_chip(S, st)}{sec_chip}</span></td><td class="num">{sub}</td>'
                    f'<td class="num">{ret if ret != "--" else "<span class=dd>--</span>"}</td><td class="num">{n}</td>'
                    f'<td style="text-align:right"><a class="tbtn sm" href="{tfn("T-Review", L)}">{act}</a></td></tr>')
    g, im, fx = S["t_prof_lbl"]
    prof = ""
    for c, a, b, d in S["t_prof_rows"]:
        chips = (f'<span class="tchip published">{g} {a}</span>' if a else "") + (f'<span class="tchip wait">{im} {b}</span>' if b else "") + (f'<span class="tchip">{mi("check", 12)}{fx} {d}</span>' if d else "")
        prof += f'<div class="crit-row" style="grid-template-columns:minmax(120px,1fr) auto"><span>{c}</span><span style="display:flex;gap:6px;justify-content:flex-end">{chips}</span></div>'
    body = tnav(S, "dash") + f'''<div class="tmain">
<div class="tscroll">
  {dash_head(S, L, "T-DashStudent", 1)}
  <div class="split">
    <div class="stu-list"><div class="sl-hd">{S["t_stu_list"]}<span class="ticon sm primary">{mi("personAdd", 20)}</span></div>{roster}</div>
    <div style="display:flex;flex-direction:column;gap:24px;min-width:0">
      <h2 class="dash-h2">{sel[0]}<span class="helper" style="display:inline;margin-left:10px">{sel[1]}</span></h2>
      {dash_filter(S)}
      <div class="tpaper" style="overflow:hidden"><div class="table-scroll"><table class="m tight">
        <thead><tr><th style="width:44px"></th>{"".join(f"<th{' style=text-align:right' if i == 4 else ''}>{c}</th>" for i, c in enumerate(S["t_ind_cols"]))}</tr></thead>
        <tbody>{ind}</tbody></table></div></div>
      <div class="tpaper">
        <div class="ph"><div><h3>{S["t_stu_fb_h"]}</h3><span class="helper" style="margin:2px 0 0">{S["t_stu_fb_sub"]}</span></div><a class="tbtn sm" href="{tfn("T-Queue", L)}">{S["t_toreview"]}</a></div>
        <div class="pb" style="padding:16px 20px 0"><div class="ov-row">{cards}</div></div>
        <div class="table-scroll"><table class="m tight"><thead><tr>{"".join(f"<th>{c}</th>" for c in S["t_stu_fb_cols"])}</tr></thead><tbody>{fb_rows}</tbody></table></div>
        <div class="pb" style="border-top:1px solid #E0E0E0"><h3 style="margin:0 0 2px;font-size:15px;font-weight:500">{S["t_prof_h"]}</h3><span class="helper" style="margin:0 0 8px">{S["t_prof_sub"]}</span>{prof}</div>
      </div>
    </div>
  </div>
</div>
</div>'''
    return tpage(S, "T-DashStudent", S["t_titles"]["ds"], body)

TBUILDERS = {"T-Book": t_book, "T-Dialog": t_dialog, "T-Created": t_created, "T-Material": t_material,
             "T-Queue": t_queue, "T-Detail": t_detail, "T-List": t_list, "T-Review": t_review,
             "T-DashGroup": t_dash_group, "T-DashStudent": t_dash_student}

# ---------- write ----------
boards, order = {}, []
titles = ["1 · Course — Feedback LO in the LO list", "2 · Assignment — check & submit", "3 · Submitted — teacher reviewing",
          "4 · Returned — approved feedback (draft 1)", "5 · Second submission — previous comments as checklist",
          "6 · Second submission — teacher reviewing", "7 · Returned (draft 2) — what changed", "8 · To-do — awaiting resubmission"]
ROW_Y = {"ja": 0, "en": 1400}
for lang, S in (("ja", JA), ("en", EN)):
    for i, screen in enumerate(SCREENS):
        CUR = screen
        name = fn(screen, lang)
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(BUILDERS[screen](S, lang))
        boards[name] = {"x": i * (W + GAP), "y": ROW_Y[lang], "w": W, "h": H,
                        "title": titles[i] + (" (EN)" if lang == "en" else " (JA)"), "is_interactive": True}
        order.append(name)

# mobile rows
MW, MH, MGAP = 375, 812, 80
MROW_Y = {"ja": 2900, "en": 4100}
mtitles = ["M1 · LO list under the topic", "M2 · Assignment — how to submit", "M3 · Snap — camera", "M4 · Crop the page",
           "M5 · Pages — check & submit", "M6 · File or photos — check & submit", "M7 · Typed answer — confirm & submit",
           "M8 · Submitted — teacher reviewing", "M9 · Returned — tap an underline", "M10 · Returned — comment sheet open"]
for lang, S in (("ja", JA), ("en", EN)):
    for i, screen in enumerate(MSCREENS):
        CUR = screen
        name = fn(screen, lang)
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(MBUILDERS[screen](S, lang))
        boards[name] = {"x": i * (MW + MGAP), "y": MROW_Y[lang], "w": MW, "h": MH,
                        "title": mtitles[i] + (" (EN)" if lang == "en" else " (JA)"), "is_interactive": True}
        order.append(name)

# teacher (Back Office) rows
TW, TH, TGAP = 1440, 900, 80
TROW_Y = {"ja": 5400, "en": 7000}
ttitles = ["T1 · Book detail — the tree, Add LO", "T2 · Add Learning Objective — AI Feedback type, its settings",
           "T3 · Created → LO content — material, requirements, criteria", "T4 · Back in the tree — Unpublished until published",
           "T5 · Submission Grading — the queue, filtered to AI Feedback", "T6 · Overview — who has submitted", "T7 · The LO's submissions — same table, one LO", "T8 · Review and return — the grading layout",
           "T9 · Group Dashboard — AI Feedback in the LO matrix, what the class missed", "T10 · Student Dashboard — one student's AI Feedback"]
for lang, S in (("ja", JA), ("en", EN)):
    for i, screen in enumerate(TSCREENS):
        CUR = screen
        name = tfn(screen, lang)
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(TBUILDERS[screen](S, lang))
        boards[name] = {"x": i * (TW + TGAP), "y": TROW_Y[lang], "w": TW, "h": TH,
                        "title": ttitles[i] + (" (EN)" if lang == "en" else " (JA)"), "is_interactive": True}
        order.append(name)

NW = 560
MNW = 375
TNW = 640
TNOTES = {
    "t1": "TEACHER, BACK OFFICE — rebuilt on 19 Sep against the prototype generated from production (school-portal-admin, syllabus squad). This is BookDetail as the code renders it: breadcrumb Book Management / book, the book title with its status chip and Add chapter top-right, chapters as accordions (blue left edge when open, N Topic(s), ↑ ↓ ⋮), topics as accordions inside them, and each learning material as a row with its type tile, the name as a link, the AI Tutor sparkle where that is on, and its publish chip. The nav follows the live LMS 2.0 tenant the PM screenshotted, which carries more squads than the syllabus one. Nothing here is new; + Add LO is where the new type enters →",
    "t2": "DialogCreateLearningMaterial, unchanged in shape: one 900-px dialog, General Info then Settings, Cancel / Confirm. Production chooses the fields by LO type (getVisibleFieldsByLMType) — Learning Objective gets Manual Grading, Practice Mode, AI Tutor…; this is the AI Feedback branch. General Info: type, LO name, External LO ID, the description the student sees. Settings (PM, 19 Sep): 公開と提出期間 — opens (the LO appears in the student's To-do) and due (submit and replace until then, the teacher reviews after); 再提出を許可する with its own date (default off in the product, on here to show it); 提出方法 — which of file / photos / typed the LO accepts, the 500-character limit riding with typed; 先生の確認 — the teacher-in-the-loop switch; off, a neutral notice says feedback goes out automatically after the due date. Click the type field to see where AI Feedback sits among the six existing types; the switches and checkboxes work. Confirm →",
    "t3": "Where Confirm lands (PM, 19 Sep): straight on the new LO's own page, Content tab, with the created snackbar — not back in the tree, because for this type the next thing the teacher does is upload the material. The LO is UNPUBLISHED, as every new learning material is in production; Publish is the action top-right, never part of creation. The page is the same one a regular LO opens to for authoring its questions; its tabs are Content and Settings only — 提出状況を見る jumps to Course › Submission Grading, where submissions are processed. This is where the pre-submission checklist comes from (PM, 19 Sep: 'extracted from teacher's content'): upload the brief and the marking criteria, 提出条件と観点を生成する (the button names its two outputs), and 提出の基本条件 comes back as an editable list where every row carries its source (課題説明 p.1, 評価基準 2.(3)). These are the structural checks the student sees on the submit screen and that run when a file is chosen; the switch on the card turns that check off for an LO that does not need one (PM, 19 Sep) — off, nothing is shown or checked. コメントの観点 (the rubric) is generated by the LLM as LaTeX from the same material and shown as one rendered block the teacher can edit or regenerate (PM, 19 Sep) — not as separate tags. Conditions gate the submission; the rubric shapes the comments. 生徒に表示される画面を見る jumps to the student's assignment screen.",
    "t4": "The tree afterwards, reached from the breadcrumb: the new LO sits under 7-1 with its own type tile (a review-comment icon, distinct from the sparkle, which on this tree means AI Tutor), highlighted as just-created and marked Unpublished. It stays that way until the teacher publishes it, from the row's ⋮ menu or from the LO page. Clicking the row reopens T3.",
    "t5": "THE SPLIT (PM, 19 Sep): Book Management sets the LO up; it does not process student submissions. Those live under Course › 提出物の採点 (Submission Grading, ToReviewListPage), production's existing home for submissions waiting on the teacher, reused rather than given a new menu item (PM, 19 Sep) and aligned to its format (PM, 19 Sep): Submissions / Learning Objectives tabs, search + Filters + Bulk Action, the status segments with counts, and the wide table (select, #, Submission ID, LO, student, username, ext. ID, course, book, reviewer, status, comments, submitted / reviewed / returned dates) — here with LO Type: AI Feedback applied. STATUSES, in the marking tones: 未確認 Not Reviewed (default) · 確認中 In Review (warning) · 返却済み Returned (success) · 差し戻し Sent Back (error), plus a secondary chip like production's Need Approval: 自動返却 Auto-returned for LOs with teacher review off, 再提出 Resubmitted for a second attempt. Submission ID → review; LO name → its overview.",
    "t6": "The LO's submission page under Course › To Review, Overview tab. The three cards are the analysis cards from the AI Tutor assignment detail (Started / Snaps / Completed in production), re-cut for this flow: 提出済み, 確認待ち — the queue the teacher-review switch creates — and 返却済み. Below, the settings as a read-only list, the Back Office's key-value pattern, so the dates and the review setting can be checked without reopening the dialog; ブック管理で編集 goes back to the LO in the tree.",
    "t7": "The LO's Submissions tab: the same Submission Grading table scoped to one LO (no LO, course or book columns), with its own status counts. Submission ID opens the review. Bulk Action is production's: contained, disabled until rows are selected — the teacher, not the model, returns the feedback, and a bulk return is a deliberate act on chosen rows.",
    "t8": "The teacher in the loop, on GradingScorePage's layout: title = LO with the status chip (確認中 In Review once opened), actions top-right (差し戻す outlined, 承認して返却する contained, ⋮). Left, the info panel: submission ID with the 生徒には未公開 chip, Reviewer Info (reviewer, auto-return off), Submission Info (student, course, submitted, file), the teacher's own ひとこと — which the student sees at the top of the returned screen — and the comment counts. Right, the report: the recognised submission first, then each draft comment as an item with its criterion, the passage it points at, the comment, and Edit / Delete; an edited one is marked. 承認して返却する is the only thing that makes the feedback exist for the student; 差し戻す sends it back for another submission. With the switch off this screen is skipped and the row shows 自動返却.",
    "t9": "DASHBOARD (PM, 20 Sep: fit the AI Feedback overview into the group and student dashboards). This is GroupDashboard as production renders it — Course / Book / Filters / Apply, the Enrollment and Duration chips, the paper with the Questions Solved via AI tile, search, the Topic / LO Dashboard toggle and, in LO mode, the student × LO matrix for one topic (sticky student column; regular LOs show 完了 Completed or a score with the AI Tutor sparkle and the history icon; a red tint means not done or failed). WHAT IS NEW: (1) AI Feedback tiles beside the production one — submissions across the course's AI Feedback LOs, 確認待ち (the queue, links to Submission Grading), 返却済み with how many were auto-returned, 再提出 with sent-backs, and the average time from due date to return. (2) In the matrix, an AI Feedback LO carries the review-comment tile, its header reads 提出 / 確認待ち / 返却済み instead of Avg. Score / Comp. Rate / AI-answered, and each cell is the submission status in the marking tones with a 自動返却 or 再提出 secondary chip and the comment count; the cell opens the LO's submissions. (3) Below the matrix, what the class missed: comments by criterion (the share of drafts with an improvement comment on each rubric criterion — the 'what did the class miss' view the PRD needs, from the criterion tag every comment carries) and the requirements that stopped a submission at the pre-check (from T3's list), each linking to where it is edited. Student name → the student dashboard.",
    "t10": "StudentDashboard as production renders it: the Student List (add-student icon, name and year, the selected one marked with the blue bar), the student's name, Course / Book / Filters / Apply, and the chapter / topic table with Study Date, Average Score and Completion, expandable to the LO rows (Learning Objective / Latest Submission / Latest Score / Highest Score). AI Feedback LOs sit in those rows with their status chip where a score would be, and 再提出 1回 where production shows the highest score. WHAT IS NEW, below the table: this student's AI Feedback — tiles (submitted, returned with auto-returns, waiting, resubmissions, comments received split into strengths and improvements, and how many points were fixed on resubmission — the revision trail from screen 7 seen from the teacher's side), the submission rows with status, comment count, which attempt, and 確認する / 見る into the review, and 観点別の傾向: the returned comments grouped by rubric criterion (strengths, improvements, fixed), so the teacher can see at a glance where this student keeps stumbling — here 統計処理 — before a consultation.",
}
MNOTES = {
    "m1": "MOBILE. Same LMS hierarchy: this is the LO list under Topic 7-1 (Figma Home/Course-ChapterList/TopicList: navigate header, primary banner, 343-wide LO cards, bottom nav). AI Feedback is the new LO type, with the yellow sparkle and the due chip. Tap the row →",
    "m2": "Assignment on the phone: same criteria chips, same 提出条件 list, and three ways to submit. 撮影して提出 is the primary option — the snap flow from unifiedapp (Snap → Crop → Review), adapted from 'ask about a question' to 'submit a handwritten answer'. File / photos and typed input are the other two (per the PC decisions of 18 Sep). Tap 撮影して提出 →",
    "m3": "Camera, as in the unifiedapp Snap tab: full-bleed dark viewfinder, scrim, blue 68-px shutter with gallery (left) and flash (right), close top-left. New here: a corner-bracket page guide and a page counter (1ページ目), because a handwritten answer is photographed one page at a time. Tap the shutter →",
    "m4": "Crop, the unifiedapp CropScreen adapted: dark stage, the photo with veils outside the frame, a blue band with four corner handles. For a paper answer the band is a rectangle that should hug the page edges, so 自動で合わせる snaps it to the paper (tap it — works in the prototype; handles are static here, draggable in the product). Thumbs strip below with ページを追加 → back to the camera for page 2. 次へ →",
    "m5": "Pages review (unifiedapp ReviewScreen shape, light theme): thumbnails in page order, hold to reorder, add a page, big preview. The basic-requirements check runs on the photographed pages (via the AI Grading OCR path, PRD C1) exactly as it does on a file or typed answer on PC. Submit →",
    "m6": "The file / photos path, reached from ファイル・写真を選ぶ on M2. Same upload block as PC: choose a file, or choose several photos at once — the picked state shows them as numbered thumbnails in page order (tap 答案の写真を選ぶ to see it). The 提出の基本条件 list fills in against whatever was picked, exactly as on PC, and only then does the submit button go live.",
    "m7": "The typed-answer path, reached from 直接入力する on M2, for short pieces like the weekly reflection. Type into the box (it counts up to the 500-character limit), then 回答を確定する — the checks run on the confirmed text, not while typing (PM, 18 Sep), and 編集する reopens the box. Which of the three paths an assignment offers is a Back Office setting on the Feedback LO.",
    "m8": "Waiting state on the phone: identical rules to PC — no AI mentioned, teacher gives the feedback after the due date, notification when returned, pages viewable / replaceable until the due date. Steps are vertical for the narrow screen. DEMO pill →",
    "m9": "Returned, on the phone: teacher's note, summary, then the recognised text of the answer with the same underlines. One layout for every submission type (PM, 18 Sep). Tapping an underline — or one of the three comment chips — opens the bottom sheet for that point (PM, 18 Sep) and highlights the passage. Resubmit and PDF export at the end.",
    "m10": "The same screen with comment ② open: the bottom sheet carries exactly what the PC card carries (badge + criterion tag, quoted passage, comment, lecture reference) plus 前へ / 次へ to step through the three points; the underline behind it is highlighted and scrolled to centre. Tap the scrim or × to close.",
}
notes = {
    "title": {"x": 0, "y": -300, "text": "AI Feedback — student experience on PC (Kindai 地域環境統計学, teacher-in-the-loop, revise loop) · 日本語", "kind": "title1", "maxW": 8 * W + 7 * GAP},
    "title_en": {"x": 0, "y": ROW_Y["en"] - 240, "text": "Same flow in English — the 日本語 / English toggle in every header jumps to the matching screen", "kind": "title1", "maxW": 8 * W + 7 * GAP},
    "n1": {"x": 0, "y": H + 60, "w": NW, "maxH": 260, "text":
        "Entry from the course, following the LMS hierarchy Book → Chapter → Topic → LO (Book Management PRD): the book is named on the course card, sessions are chapters, topics sit under them, and each row is an LO with its LO type as a small chip. AI Feedback is a NEW LO type (yellow chip + sparkle) alongside Learning Objective / Flashcard / Recording / Practice / External Content / Paper Submission; the assignment is created at the LO level. A course-level 'AI Feedback 対応' chip sat on the course card and was removed (PM, 19 Sep): the LO type chip already says which LOs have it. NAMING (PM, 19 Sep): 'AI' is gone from every student-facing label — the LO type reads フィードバック / Feedback, as do the screen titles and To-do rows — because the teacher may review the draft and return it as their own endorsed feedback. AI Feedback stays the internal / Back Office name. The two AI words a student still sees are the 生成AIリテラシー rubric criterion (Kindai's own, about the student's AI use) and AI演習 / AI Practice, a different product. Week 8 is dimmed: its start date has not passed. Click the 第7回 演習レポート row →"},
    "n2": {"x": 1 * (W + GAP), "y": H + 60, "w": NW, "maxH": 300, "text":
        "Two additions here. (a) 提出前チェック — structural checks only (chart present, coefficient stated, test stated, lecture material cited, page count), a separate 提出条件 field on the assignment in Back Office, not the rubric; for Kindai Correspondence this becomes the 13-rule check that would have removed 36% of resubmissions. (b) A lock line under the criteria stated the L0 boundary ('AI never writes your answer'); it was reworded on 19 Sep to drop the AI mention and then removed entirely (PM): once the student is not told AI is involved, the line answers a question nobody asked. The boundary itself is unchanged — it belongs in the teacher's brief and the PRD, not on the submit screen. An AI-use declaration was here and was removed on 18 Sep (PM decision: self-report is not evidence); the 生成AIリテラシー criterion stays the professor's to judge. (c) Upload accepts PDF / Word / Excel / PowerPoint and photos (PM, 18–19 Sep) — office files go in as they are rather than being exported to PDF, which matters for the Kindai exercise because the Excel-skill criterion is judged on the workbook itself; photos are picked several at a time and kept in page order (click 答案の写真を選ぶ to see that state), and photo submissions go through the AI Grading OCR path (PRD C1) before feedback. (d) A 直接入力 / Type-your-answer mode (PM, 18 Sep) for short pieces like the weekly reflection: textarea with a live count against a 500-character limit shown under the box (PM, 18 Sep: a target line in the header was tried and removed), then a 回答を確定する / Confirm answer step — the basic-requirements checks run on the confirmed text, exactly as they run on a chosen file (PM, 18 Sep), and 編集する reopens the box; which modes an assignment accepts is a Back Office setting on the Feedback LO. Choose a file, or type, to see the checks run."},
    "n3": {"x": 2 * (W + GAP), "y": H + 60, "w": NW, "maxH": 280, "text":
        "The waiting state. Still no AI content (PRD C3), and the copy no longer mentions AI at all (PM, 18 Sep): to the student, the teacher gives the feedback — no review step, no teacher name (PM, 18 Sep). A generic line says the student will be notified when the review is done — no date, no SLA countdown (PM decision 18 Sep: a teacher-set expected-return line was tried and removed). The file can be viewed or replaced until the due date (PM decision 18 Sep); the teacher reviews only after the due date, so the copy says so. The black DEMO pill simulates approval →"},
    "n4": {"x": 3 * (W + GAP), "y": H + 60, "w": NW, "maxH": 300, "text":
        "Draft-1 return. Every card now carries its Kindai criterion as a grey tag (統計処理, 解釈…) — no level, no number — which is the data the professor's 'what did the class miss' view needs. A 次の一歩 card was tried and removed (PM, 18 Sep): an AI-written next step prescribes the class flow, which is the teacher's — the guidance now lives inside each 改善点 card and in the teacher's own note. 修正して再提出 now leads to a real second-submission screen with its due date. コメントを PDF で保存 is the portable-structure proof for Correspondence/KULeD."},
    "n5": {"x": 4 * (W + GAP), "y": H + 60, "w": NW, "maxH": 300, "text":
        "THE BIG ADDITION. Left: last time's comments as a checklist — the student ticks what they addressed; strengths are shown as 'check it still holds'. The teacher's note travels with it. Right: upload and the basic-requirements list. A 自己チェック (rewrote in my own words / used AI sentences as-is) was here and was removed on 18 Sep for the same reason as the AI-use declaration: self-report is not evidence. Submitting goes through the teacher like any submission →"},
    "n6": {"x": 5 * (W + GAP), "y": H + 60, "w": NW, "maxH": 220, "text":
        "Same waiting state for the second submission, so the loop never bypasses the teacher. DEMO pill →"},
    "n7": {"x": 6 * (W + GAP), "y": H + 60, "w": NW, "maxH": 300, "text":
        "Draft-2 return opens with 前回からの変化: which earlier points were fixed (③ test, ② causation) and that one new comment exists — this is the exercise-view revision trail from C10.3, in the student's own hands. The 'rewritten in your own words' line appears only in the positive case; there is no accusatory counterpart. New cards: two strengths on the fixed passages, one new 改善点 on structure. No resubmit CTA — the teacher's note says one sentence completes it. No AI next-step card (PM, 18 Sep)."},
    "n8": {"x": 7 * (W + GAP), "y": H + 60, "w": NW, "maxH": 240, "text":
        "To-do now carries the state between return and resubmission: 再提出待ち ・ 11月20日まで with the return date, linking to the feedback where the resubmit CTA lives. Overdue in red, upcoming items held until their start date."},
    "n_lang": {"x": 0, "y": ROW_Y["en"] + H + 60, "w": 700, "maxH": 220, "text":
        "Language toggle: a segmented 日本語 / English control in the header, left of the bell. In the prototype it is a link to the twin screen, so the language holds as you click through (each artboard keeps its own state). In the product this would be the account's language setting."},
    "n_dev": {"x": 760, "y": ROW_Y["en"] + H + 60, "w": 700, "maxH": 220, "text":
        "PC / Mobile switch (18 Sep): the black pill in the bottom-left corner of every artboard jumps to the same step on the other device — PC ⇄ the mobile row below. Since 19 Sep it also carries 先生（BO）, which opens the teacher's Back Office (the row at the bottom of the canvas), so the two sides of the same setting can be read against each other. Prototype-only control, like the DEMO pill; in the product the device is simply whatever the student opened."},
    "title_m": {"x": 0, "y": MROW_Y["ja"] - 300, "text": "Mobile — snap a handwritten answer: LO list → assignment → camera → crop → pages → submit → returned (bottom sheet) · 日本語", "kind": "title1", "maxW": 8 * MW + 7 * MGAP},
    "title_m_en": {"x": 0, "y": MROW_Y["en"] - 240, "text": "Same mobile flow in English", "kind": "title1", "maxW": 8 * MW + 7 * MGAP},
    "title_t": {"x": 0, "y": TROW_Y["ja"] - 300, "text": "Back Office — inside Book Management, as production renders it: book tree → Add LO dialog with the AI Feedback type and its settings → LO content · then Course › Submission Grading: queue → overview → submissions → review and return · then Dashboard: group and student · 日本語", "kind": "title1", "maxW": 7 * TW + 6 * TGAP},
    "title_t_en": {"x": 0, "y": TROW_Y["en"] - 240, "text": "Same Back Office flow in English", "kind": "title1", "maxW": 6 * TW + 5 * TGAP},
    "n_role": {"x": 1520, "y": MROW_Y["en"] + MH + 60, "w": 700, "maxH": 240, "text":
        "Teacher / student switch (19 Sep): the bottom-left pill on the Back Office boards flips to the student's screen, so the same setting can be read from both sides — the dates on T2 against the waiting copy on screen 3, the checklist on T3 against 提出前チェック on screen 2. Prototype-only, like the DEMO and PC / Mobile pills."},
}
for i, key in enumerate(["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10"]):
    notes[key] = {"x": i * (MW + MGAP), "y": MROW_Y["ja"] + MH + 60, "w": MNW, "maxH": 420, "text": MNOTES[key]}
for i, key in enumerate(["t1", "t2", "t3", "t4", "t5", "t6", "t7", "t8", "t9", "t10"]):
    notes[key] = {"x": i * (TW + TGAP), "y": TROW_Y["ja"] + TH + 60, "w": TNW, "maxH": 460, "text": TNOTES[key]}

canvas = {
    "v": 3,
    "createdOnFiles": {"v": 1, "at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
    "title": "AI Feedback — Back Office + Student Prototype",
    "launch": {"view": "canvas"},
    "pages": [],
    "boards": boards,
    "order": order,
    "notes": notes,
    "designSystems": [],
}
with open(os.path.join(ROOT, "canvas.json"), "w", encoding="utf-8") as f:
    json.dump(canvas, f, ensure_ascii=False, indent=2)

print("wrote", len(order), "artboards")
for n in order:
    print(n, os.path.getsize(os.path.join(ROOT, n)), "bytes")

# ---------- standalone site for the prototype server (deploy/public) ----------
# Same artboards, rendered by deploy/public/dc-shim.js instead of the canvas runtime.
# The pages run as the app itself: the artboard fills the window, with no frame
# around it. The PC screens keep a desktop minimum width and scroll sideways
# below it, the way a desktop web app does on a narrow window.
SITE_CSS = """
html,body{height:100%}
body{margin:0;padding:0;display:block;overflow:hidden}
.root{width:100%;min-width:1024px;height:100vh;height:100dvh}
.troot{width:100%;min-width:1180px;height:100vh;height:100dvh}
.mroot{width:100%;max-width:520px;height:100vh;height:100dvh;margin:0 auto}
@media (max-width:1023px){body{overflow-x:auto}}
@media (max-width:1179px){body:has(.troot){overflow-x:auto}}
/* the drawn iOS status bar belongs to the artboard, not to a live page */
.sb{display:none}
.ctop{top:0}
"""

HOME_ICON = ('<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" style="flex-shrink:0;display:block">'
             '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/>'
             '<rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/></svg>')

def to_static(text, lang):
    """Turn one .dc.html artboard into a standalone page served by deploy/public."""
    title = re.search(r"<title>(.*?)</title>", text, re.S).group(1)
    helmet = re.search(r"<helmet>(.*?)</helmet>", text, re.S).group(1)
    markup = re.search(r"</helmet>\s*(.*?)\s*</x-dc>", text, re.S).group(1)
    logic = re.search(r'<script type="text/x-dc"[^>]*>(.*?)</script>', text, re.S).group(1)
    markup = markup.replace('.dc.html"', '.html"')      # links between screens
    # Drop the artboard's fixed size; the stylesheet gives it the window instead.
    markup = re.sub(r'\s*style="width: (?:1280|375|1440)px; height: (?:800|812|900)px;"', "", markup, count=1)
    # Fold an index link into the prototype-only device pill, so no page chrome is needed.
    home = "一覧" if lang == "ja" else "All"
    markup = re.sub(r'(<div class="dev[^"]*" role="group"[^>]*>)',
                    r'\1' + f'<a class="dev-i" href="/" aria-label="{home}">{HOME_ICON}<span class="dl">{home}</span></a>', markup, count=1)
    dark = "mroot dark" in markup
    bg = "#000" if dark else ("#fff" if 'class="troot"' in markup else "#f2f2f4")
    return f'''<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="theme-color" content="{"#000000" if dark else "#ffffff"}">
<link rel="icon" href="data:,">
<title>{title}</title>
{helmet}
<style>{SITE_CSS}
body{{background:{bg}}}</style>
</head>
<body>
<div id="dc-root"></div>
<template id="dc-template">{markup}</template>
<script src="/dc-shim.js"></script>
<script>
{logic}
window.__dcBoot(Component);
</script>
</body>
</html>
'''

def site_index():
    def links(screens, lang, titles):
        out = ""
        for i, screen in enumerate(screens):
            step, label = titles[i].split(" · ", 1)
            out += (f'<a class="step" href="{fn(screen, lang)[:-8]}.html">'
                    f'<span class="n">{step}</span><span class="l">{label}</span></a>')
        return out
    rows = [
        ("PC ・ 日本語", "1280 × 800", links(SCREENS, "ja", titles)),
        ("PC · English", "1280 × 800", links(SCREENS, "en", titles)),
        ("モバイル ・ 日本語", "375 × 812", links(MSCREENS, "ja", mtitles)),
        ("Mobile · English", "375 × 812", links(MSCREENS, "en", mtitles)),
        ("先生（バックオフィス）・ 日本語", "1440 × 900", links(TSCREENS, "ja", ttitles)),
        ("Teacher (Back Office) · English", "1440 × 900", links(TSCREENS, "en", ttitles)),
    ]
    blocks = "".join(
        f'<section class="row"><h2>{name}<span>{size}</span></h2><div class="steps">{body}</div></section>'
        for name, size, body in rows)
    return f'''<!doctype html>
<html lang="ja">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<link rel="icon" href="data:,">
<title>AI フィードバック — 生徒プロトタイプ</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&amp;display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box}}
body{{margin:0;padding:48px 20px 64px;background:#f2f2f4;color:rgba(28,30,44,.87);font-family:'Noto Sans JP',system-ui,sans-serif}}
main{{max-width:880px;margin:0 auto;display:flex;flex-direction:column;gap:28px}}
h1{{font-size:24px;line-height:36px;margin:0}}
.lead{{font-size:14px;line-height:22px;color:rgba(28,30,44,.6);margin:6px 0 0}}
.row h2{{font-size:16px;line-height:24px;margin:0 0 12px;display:flex;align-items:center;gap:10px}}
.row h2 span{{font-size:12px;font-weight:400;color:rgba(28,30,44,.6)}}
.steps{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}}
a.step{{display:flex;align-items:center;gap:12px;background:#fff;border-radius:8px;box-shadow:0 8px 16px rgba(0,0,0,.1);padding:14px 16px;text-decoration:none;color:inherit}}
a.step:hover{{background:#fafbff;box-shadow:0 8px 16px rgba(57,90,210,.18)}}
a.step .n{{display:inline-flex;align-items:center;justify-content:center;min-width:30px;height:30px;padding:0 8px;border-radius:1000px;background:#eef1ff;color:#395ad2;font-size:12px;font-weight:700;flex:0 0 auto}}
a.step .l{{font-size:14px;line-height:20px;font-weight:500}}
footer{{font-size:12px;line-height:20px;color:rgba(28,30,44,.6);border-top:1px solid rgba(28,30,44,.12);padding-top:16px}}
</style>
</head>
<body>
<main>
  <header>
    <h1>AI フィードバック — プロトタイプ</h1>
    <p class="lead">近畿大学「地域環境統計学」の演習レポートを題材に、先生がバックオフィスで課題を設定し、生徒が提出し、先生が確認して返却するまでの流れを描いた試作です。実装ではありません。<br>
    各画面のヘッダーで 日本語 / English、左下のピルで PC / モバイル、バックオフィスでは 先生 / 生徒 を切り替えられます。待機画面の DEMO ピルは、先生が確認して返却したところまで進めます。<br>
    <span lang="en">A prototype of AI Feedback — the teacher's Back Office setup and the student's submission and return — not an implementation. Every screen has a Japanese / English toggle in the header and a device or role switch in the bottom-left corner.</span></p>
  </header>
  {blocks}
  <footer>社内検討用。外部への共有はご遠慮ください。 ・ 仕様は <code>PRDs/ai-feedback-university-prd.md</code>。<br>
  <span lang="en">Internal review only. The specification is in the repository's PRD.</span></footer>
</main>
</body>
</html>
'''

for lang in ("ja", "en"):
    for screen in SCREENS + MSCREENS + TSCREENS:
        name = fn(screen, lang)
        with open(os.path.join(ROOT, name), encoding="utf-8") as f:
            src = f.read()
        with open(os.path.join(SITE, name[:-8] + ".html"), "w", encoding="utf-8") as f:
            f.write(to_static(src, lang))
with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
    f.write(site_index())
print("wrote", len(order) + 1, "pages to deploy/public")
