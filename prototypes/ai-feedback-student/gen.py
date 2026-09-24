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
.chip.hl{background:#fff3cc;color:#7a5a00;font-weight:500}
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

.ppdf{background:#fff;border:1px solid rgba(28,30,44,.12);border-radius:6px;padding:20px 24px;display:flex;flex-direction:column;gap:12px;box-shadow:0 8px 16px rgba(0,0,0,.08)}
.ppdf.m{padding:14px;gap:10px}
.pq{position:relative;display:flex;flex-direction:column;gap:6px;text-align:left;border:2px dashed rgba(28,30,44,.18);border-radius:6px;padding:10px 12px 10px 14px;background:#fff;font-family:inherit;color:inherit;cursor:pointer}
.pq:hover{border-color:rgba(57,90,210,.5)}
.pq.on{border:2px solid #395ad2;box-shadow:0 0 0 3px rgba(57,90,210,.18);background:#f7f8ff}
.pq .pno{position:absolute;left:-10px;top:-10px;width:22px;height:22px;border-radius:50%;background:#395ad2;color:#fff;font-size:12px;font-weight:700;display:none;align-items:center;justify-content:center}
.pq.on .pno{display:flex}
.popt{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:1.5px solid rgba(28,30,44,.16);border-radius:10px;padding:12px 14px;background:#fff;font-family:inherit;color:inherit;font-size:15px;line-height:22px;cursor:pointer}
.popt:hover{background:#fafafc}
.popt .mk{width:22px;height:22px;border-radius:50%;border:2px solid rgba(28,30,44,.24);flex:0 0 22px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#fff}
.popt.ok{border-color:#1f7a4d;background:#e6f5ee}.popt.ok .mk{background:#1f7a4d;border-color:#1f7a4d}
.popt.ng{border-color:#d13842;background:#fbe7e9}.popt.ng .mk{background:#d13842;border-color:#d13842}
.popt.dis{cursor:default}
.pfb{border-radius:10px;padding:12px 14px;font-size:14px;line-height:22px}
.pfb.ok{background:#e6f5ee;color:#1f7a4d}.pfb.ng{background:#fbe7e9;color:#8a1f2a}
.pfb b{display:block;margin-bottom:2px}
.prange{width:100%;accent-color:#395ad2;height:32px}
.pspin{width:44px;height:44px;border-radius:50%;border:4px solid rgba(57,90,210,.2);border-top-color:#395ad2;animation:pspin 1s linear infinite}
@keyframes pspin{to{transform:rotate(360deg)}}
.psq{padding:12px 0;border-top:1px solid rgba(28,30,44,.1);font-size:14px;line-height:22px}
.psq b{display:inline-block;width:40px}
.psq ol{margin:6px 0 0 40px;padding-left:18px}
.lo.on{border-color:#395ad2!important;box-shadow:0 0 0 3px rgba(57,90,210,.15)}
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
    lo_fb8="第8回 演習 のフィードバック", lo_fb8_s="11月20日 開始 ・ 開始日になると「やること」に表示されます", chip_pre="開始前",
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
    f_hl="この提出は、先生がクラスで紹介する例に選びました",
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
    lo_fb8="Feedback · Session 8 exercise", lo_fb8_s="Opens Nov 20 · appears in To-do on its start date", chip_pre="Not started",
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
    f_hl="Your teacher chose this work as an example to show the class",
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
  {lo_row("sparkle", S["p_lo"], S["p_course_sub"], chip=lt(S["p_lt"], True) + f'<span class="chip review">{S["p_todo_chip"]}</span>', href=fn("P-Sets",L), sparkle=True)}
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
            <span class="chip hl" style="align-self:flex-start">{mi("star", 14, "#b7791f")}{S["f_hl"]}</span>
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
  {trow("sparkle", S["p_lo"], S["course"], f'<span class="chip review">{S["p_todo_chip"]}</span>', href=fn("P-Sets",L), sparkle=True)}
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
  {lo_row("sparkle", S["p_lo"], S["p_course_sub"], chip=lt(S["p_lt"], True) + f'<span class="chip review">{S["p_todo_chip"]}</span>', href=fn("M-PSets",L), sparkle=True)}
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
    <div style="display:flex;flex-direction:column;gap:6px;flex:1 1 auto;min-width:0"><p class="sub1" style="font-size:14px">{S["f_tnote_h"]}</p><p class="b2" style="line-height:22px">{S["f_tnote"]}</p>
      <span class="chip hl" style="align-self:flex-start;height:auto;min-height:24px;padding:3px 10px;white-space:normal;line-height:16px">{mi("star", 14, "#b7791f")}{S["f_hl"]}</span></div>
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
    "star": "M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z",
    "fileDownload": "M19 9h-4V3H9v6H5l7 7 7-7zM5 18v2h14v-2H5z",
    # the AI Tutor class page's Share Access: MUI Share on the row, QrCode2 in the dialog, ContentCopy on the code
    "share": "M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z",
    "qrCode": "M15 21h-2v-2h2v2zm-2-7h-2v5h2v-5zm8-2h-2v4h2v-4zm-2-2h-2v2h2v-2zM7 12H5v2h2v-2zm-2-2H3v2h2v-2zm7-5h2V3h-2v2zm-7.5-.5v3h3v-3h-3zM9 9H3V3h6v6zm-4.5 7.5v3h3v-3h-3zM9 21H3v-6h6v6zm7.5-16.5v3h3v-3h-3zM21 9h-6V3h6v6zm-2 10v-3h-4v2h2v3h4v-2h-2zm-2-7h-4v2h4v-2zm-4-2H7v2h2v2h2v-2h2v-2zm1-1V7h-2V5h-2v4h4zM6.75 5.25h-1.5v1.5h1.5v-1.5zm0 12h-1.5v1.5h1.5v-1.5zm12-12h-1.5v1.5h1.5v-1.5z",
    "contentCopy": "M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z",
    "camera": "M12 15.2a3.2 3.2 0 1 0 0-6.4 3.2 3.2 0 0 0 0 6.4zM9 2 7.17 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2h-3.17L15 2H9zm3 15c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5z",
    "chevron": "M10 6 8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z",
    "starOff": "M22 9.24l-7.19-.62L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21 12 17.27 18.18 21l-1.63-7.03L22 9.24zM12 15.4l-3.76 2.27 1-4.28-3.32-2.88 4.38-.38L12 6.1l1.71 4.04 4.38.38-3.32 2.88 1 4.28L12 15.4z",
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
tr.just-created td{background:#EDF7FE}
/* full-screen dialog (MDialogCustom fullScreen) */
.tfull{position:absolute;inset:0;z-index:85;background:#F5F5F5;display:flex;flex-direction:column}
.tfull-head{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:12px 24px;background:#fff;border-bottom:1px solid #E0E0E0;flex:0 0 auto}
.tfull-head h2{margin:0;font-size:20px;font-weight:500}
.tfull-body{flex:1 1 auto;overflow:auto;padding:24px;display:flex;justify-content:center;align-items:flex-start;min-height:0}
.tfull-foot{display:flex;justify-content:flex-end;gap:8px;padding:12px 24px;background:#fff;border-top:1px solid #E0E0E0;flex:0 0 auto}
.tform{background:#fff;border-radius:4px;width:100%;max-width:760px;padding:24px 32px 32px;display:flex;flex-direction:column;gap:28px;
  box-shadow:0 1px 3px rgba(0,0,0,.12),0 1px 2px rgba(0,0,0,.24)}
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
.tpop .it{display:flex;align-items:center;gap:10px;padding:8px 16px;font-size:14px;color:#212121;min-height:36px;background:none;border:0;width:100%;box-sizing:border-box;text-align:left;font-family:inherit;text-decoration:none;cursor:pointer;white-space:nowrap}
.tpop .it:hover{background:#F5F5F5}
.rev-pager{display:flex;align-items:center;gap:6px}
.rev-pager .rp-mid{flex:1 1 auto;display:flex;flex-direction:column;align-items:center;gap:1px;min-width:0;text-align:center}
.rev-pager .rp-pos{font-size:13px;font-weight:500}
.rev-pager .rp-ctx{font-size:11px;color:#9E9E9E}
.rev-pager a.ticon{color:#616161;text-decoration:none}
.tpop.fpanel{left:0;top:44px;width:360px;padding:16px;display:flex;flex-direction:column;gap:14px;text-align:left;font-weight:400}
.tpop.fpanel h4{margin:0;font-size:15px;font-weight:500}
.tpop.fpanel .ffoot{display:flex;justify-content:flex-end;gap:8px;margin-top:4px;padding-top:12px;border-top:1px solid #E0E0E0}
.tbtn.neutral.on{background:#1976D21F;border-color:#1976D2;color:#0B79D0}
.tpop .it.sel{background:#1976D21F}
/* snackbar */
.snack{position:absolute;left:24px;bottom:24px;z-index:120;background:#2E7D32;color:#fff;border-radius:4px;padding:12px 16px;font-size:14px;
  box-shadow:0 5px 5px -3px rgba(0,0,0,.2),0 8px 10px 1px rgba(0,0,0,.14),0 3px 14px 2px rgba(0,0,0,.12);display:flex;gap:12px;align-items:center;max-width:480px}
/* tabs */
.tabs{display:flex;border-bottom:1px solid #E0E0E0;margin-bottom:24px}
.tab{position:relative;padding:12px 16px;font-size:14px;font-weight:500;letter-spacing:.4px;color:#757575;white-space:nowrap;background:none;border:0;font-family:inherit;cursor:pointer;line-height:1.43}
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
.toggle-group>span,.toggle-group>a{color:#2196F3;padding:0 14px;height:34px;display:inline-flex;align-items:center;font-size:14px;font-weight:500;white-space:nowrap;text-decoration:none}
.toggle-group>a:hover{background:#2196F30A}
.toggle-group>*+*{border-left:1px solid rgba(33,150,243,.5)}
.toggle-group span.on{background:#1976D21F;color:#0B79D0}
.toggle-group span.dis{color:#BDBDBD;background:#FAFAFA;cursor:default}
.toggle-group.dis{border-color:#E0E0E0}.toggle-group.dis>*+*{border-left-color:#E0E0E0}
/* Group Dashboard overview blocks */
.gd{display:grid;grid-template-columns:repeat(6,1fr);gap:12px}
.gd .blk{border:1px solid #E0E0E0;border-radius:8px;background:#fff;padding:12px 14px;display:flex;flex-direction:column;gap:6px;min-width:0}
.gd .blk.s2{grid-column:span 2}.gd .blk.s3{grid-column:span 3}
.gd .blk.hot{border-color:#FF9800;background:#FFFBF2}
.gd .blk h4{margin:0;font-size:12px;font-weight:500;color:#757575;letter-spacing:.04em;display:flex;align-items:center;gap:6px}
.gd .brow{display:flex;align-items:center;justify-content:space-between;gap:12px;font-size:13px;padding:4px 0;border-bottom:1px solid #F5F5F5}
.gd .brow:last-of-type{border-bottom:0}
.gd .brow .bl{display:flex;flex-direction:column;min-width:0;gap:1px}
.gd .brow .blo{color:#212121;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.gd .brow .bwho{font-size:12px;color:#757575;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.gd .brow .bn{font-size:20px;font-weight:500;font-variant-numeric:tabular-nums;white-space:nowrap;flex:0 0 auto}
.gd a.blrow{color:inherit;border-radius:4px;margin:0 -6px;padding:4px 6px}
.gd .bquotes{display:grid;grid-template-columns:1fr 1fr;gap:8px}
.df-sec{display:flex;align-items:center;gap:8px;font-size:13px;font-weight:500;color:#424242;margin-top:2px;padding-top:12px;border-top:1px solid #EEEEEE}
.df-range>.lbl{display:block;font-size:12px;color:#757575;margin-bottom:6px}
.df-2{display:grid;grid-template-columns:1fr 1fr;gap:10px}
.tchip.ins{height:20px;padding:0 8px;font-size:11px;border-color:transparent;font-weight:500;flex:0 0 auto}
.tchip.ins-miss{background:#FFE6E3;color:#C62828}.tchip.ins-good{background:rgba(76,175,80,.14);color:#2E7D32}
.tchip.ins-pick{background:#FFF3CC;color:#7A5A00}.tchip.ins-pace{background:#E3F2FD;color:#0B79D0}
.ins-row{display:flex;align-items:flex-start;gap:8px;font-size:13px;line-height:1.5;color:#424242;padding:4px 0}
.ins-row .tchip{margin-top:1px}
.tp-dates{display:flex;align-items:center;gap:4px;font-size:12px;color:#757575;margin:2px 0 6px;white-space:nowrap}
.tp-dates .sep{margin:0 2px;color:#BDBDBD}
.tp-ins{display:flex;align-items:flex-start;gap:6px;margin-top:8px;font-size:12px;color:#424242;line-height:1.45;white-space:normal;max-width:560px}
.tp-ins svg{flex:0 0 auto;margin-top:1px}
.tp-ins b{font-weight:500;color:#757575}
.tp-more{flex:0 0 auto;display:inline-flex;align-items:center;gap:2px;background:none;border:0;padding:0;color:#2196F3;font:inherit;font-size:12px;cursor:pointer;margin-left:4px;white-space:nowrap}
.tp-more.on svg{transform:rotate(180deg)}
table.m tbody tr.sub td .gd .blk{border:0;padding:0;background:transparent}
.gd a.bquote{display:flex;align-items:center;gap:10px;background:#FAFAFA;border-radius:6px;padding:8px 10px;color:inherit;text-decoration:none;min-width:0}
.gd a.bquote:hover{background:#F0F0F0}
.gd a.bquote .bq{flex:1 1 auto;font-size:12px;line-height:1.45;color:#424242;min-width:0}
.gd a.bquote .bwho{flex:0 0 auto;font-size:11px;color:#757575;white-space:nowrap}
.gd a.blrow .blo{color:#2196F3}
.gd .breason{color:#212121;font-size:13px;margin-left:8px}
.gd .breason::before{content:"— ";color:#9E9E9E}
.gd a.blrow:hover{background:#F5F5F5}
.gd .bline{font-size:14px;line-height:1.5;margin:0}
.gd .bwhy{font-size:11px;color:#9E9E9E;margin-top:auto}
.gd .blink{font-size:13px;align-self:flex-start}
.gd .bchips{display:flex;gap:6px;flex-wrap:wrap}
.gd .bchips .tchip b{font-weight:500;margin-left:2px}
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
.matrix tbody tr.hide{display:none}
.matrix tbody tr:last-child td{border-bottom:0}
.stat-cell{display:flex;align-items:center;gap:8px;padding:0 10px;height:52px;box-sizing:border-box;border-right:1px solid #F5F5F5}
.stat-cell.miss{background:rgba(239,83,80,.1);color:#E31B0C}
.stat-cell .score{font-variant-numeric:tabular-nums}
.stat-cell .grow{margin-left:auto;color:#2196F3;display:flex;align-items:center;gap:6px}
.stat-cell.hl{flex-wrap:wrap;height:auto;min-height:52px;padding:6px 10px;align-content:center;row-gap:2px}
.stat-cell .hl-why{flex:1 0 100%;font-size:11px;line-height:1.3;color:#7a5a00;white-space:normal}
.stat-cell .hl-why::before{content:"★ ";color:#ED6C02}
.stat-cell .grow .cnt{font-size:12px;color:#757575;display:inline-flex;align-items:center;gap:2px;font-variant-numeric:tabular-nums}
.split{display:grid;grid-template-columns:240px minmax(0,1fr);gap:24px;align-items:start}
.stu-list{border:1px solid #E0E0E0;border-radius:4px;background:#fff;overflow:hidden}
.stu-list .sl-hd{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:12px 16px;border-bottom:1px solid #E0E0E0;font-weight:500}
.stu-list a.sl-item{display:block;padding:12px 16px;border-bottom:1px solid #E0E0E0;color:#212121}
.stu-list a.sl-item:last-child{border-bottom:0}
.stu-list a.sl-item.on{background:#EDF7FE;box-shadow:inset 3px 0 0 #2196F3}
.stu-list .sl-sub{font-size:12px;color:#757575;display:block}
table.m.tight thead th,table.m.tight tbody td{padding:12px 10px}
button.tchip.hlf{cursor:pointer;font-family:inherit;gap:4px;color:#ED6C02;border-color:#FFB74D;background:#fff}
button.tchip.hlf.on{background:#FFF4E5;border-color:transparent;font-weight:500}
table.m tbody tr.hide{display:none}
.hl-star{display:inline-flex;color:#ED6C02;vertical-align:middle;margin-right:4px}
.dash-filter .field .in>.ell{overflow:hidden;text-overflow:ellipsis;white-space:nowrap;min-width:0}
.dash-h2{font-size:20px;font-weight:500;margin:0}
.insight{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.insight .tpaper .ph h3{font-size:15px}
.insight .tpaper .ph .helper{margin:2px 0 0}
.crit-row{display:grid;grid-template-columns:minmax(120px,1fr) 2fr auto;gap:12px;align-items:center;padding:8px 0;border-bottom:1px solid #F5F5F5;font-size:14px}
.crit-row:last-child{border-bottom:0}
.crit-row .n{font-variant-numeric:tabular-nums;color:#757575;font-size:13px;white-space:nowrap}
table.m>tbody>tr.sub>td{background:#FAFAFA;padding:0 16px 16px 54px;border-bottom:1px solid #E0E0E0}
table.m table.inner{border:1px solid #E0E0E0;border-radius:4px;background:#fff;width:100%;table-layout:fixed}
table.m table.inner col.c-lo{width:24%}table.m table.inner col.c-sub{width:13%}table.m table.inner col.c-sc{width:9%}
table.m table.inner col.c-st{width:18%}table.m table.inner col.c-cr{width:21%}table.m table.inner col.c-act{width:6%}
table.m table.inner thead th{white-space:normal}
table.m table.inner thead th{background:#fff;padding:10px 8px;font-size:13px}
table.m table.inner tbody td{padding:10px 8px;background:#fff;vertical-align:middle;border-bottom:1px solid #E0E0E0;font-size:13px}
table.m table.inner td{white-space:normal;overflow-wrap:anywhere}
table.m table.inner td.fcrit{font-size:12px;line-height:1.4}
table.m table.inner td.cms{line-height:1.35}
table.m table.inner td .tchip{white-space:nowrap}
table.m table.inner td .tchip{height:20px;padding:0 7px;font-size:11px}
table.m table.inner tbody tr.det td{padding:0 12px 10px 28px;border-top:0;background:#FFFDF7}
table.m table.inner tbody tr.det .tp-ins>span:first-of-type{flex:1 1 320px;min-width:0;white-space:normal}
table.m table.inner tbody tr.det .tp-ins>svg{margin-top:2px}
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
    t_new_lo="第7回 演習レポート", t_snack="LOを作成しました。", t_pub_snack="LOを公開しました。開始日から生徒の一覧に表示されます。",
    # Add Learning Objective dialog
    t_dlg_title="学習目標（LO）を追加", t_dlg_general="基本情報", t_dlg_settings="設定", t_dlg_select="LOタイプを選択",
    t_types=["ランダム学習", "学習目標", "フラッシュカード", "録音課題", "演習提出", "外部コンテンツ"],
    t_type_fb="AIフィードバック", t_new="NEW",
    t_f_name="学習目標", t_ph_name="LO名を入力", t_f_ext="外部LO ID", t_ph_ext="英数字のみ",
    t_f_desc="課題の説明（生徒に表示）",
    t_v_desc="総務省「社会生活統計指標」の都道府県別データから2つの変数を選び、Excel で相関係数を求めて散布図を作成してください。結果の解釈と、有意性の確認までを A4 2枚程度にまとめて提出します。",
    # Dates left the LO (PM, 22 Sep): the submission window is the course's, set in Course Management
    t_s_when="公開期間と締切", t_f_start="開始日時", t_v_start="2026/11/06 09:00", t_f_due="締切日時", t_v_due="2026/11/13 23:59",
    t_when_course="公開開始日・締切・再提出締切は、この教材を割り当てたコースの「コース管理 › 教材 › 学習項目の公開期間」で設定します。同じ教材を複数のコースで使う場合、コースごとに別の日程を管理できます。",
    t_when_link="コース管理で日程を設定する",
    t_f_resub="再提出を許可する", t_v_resub="2026/11/20 23:59 まで", t_resub_note="再提出の締切はコース管理で設定します",
    t_s_how="提出方法", t_how=["ファイル（PDF ・ Word ・ Excel ・ PowerPoint）", "写真（複数枚まとめて）", "直接入力"],
    t_how_limit="文字数の上限 500字",
    t_s_review="先生の確認", t_review_on="返却前に先生が確認する",
    t_review_body="下書きは締切のあとに作成され、先生が確認・編集して返却するまで生徒には表示されません。生徒には先生からのフィードバックとして届きます。",
    t_review_off="締切のあと、先生の確認なしに自動で返却されます。",
    t_cancel="キャンセル", t_confirm="確定",
    t_dlg_edit_title="学習目標（LO）を編集", t_type_fixed="LOタイプは作成後に変更できません",
    # LO page
    t_lo_tabs=["内容", "設定"], t_course_tabs=["概要", "提出一覧"], t_publish="公開する", t_edit="設定を編集", t_save="保存",
    # Settings tab (read-only; Edit reopens the dialog prefilled)
    t_set_gen=[("種類", "AIフィードバック"), ("学習目標", "第7回 演習レポート"), ("外部LO ID", "—"), ("課題の説明（生徒に表示）", "__desc__")],
    t_set_set=[("公開期間と締切", "__course__"), ("再提出", "許可する"),
               ("提出方法", "ファイル（PDF ・ Word ・ Excel ・ PowerPoint） ・ 写真（複数枚まとめて） ・ 直接入力（上限 500字）"), ("先生の確認", "あり ・ 返却前に先生が確認する")],
    t_set_h_status="公開状態", t_set_status=[("状態", "__status__"), ("作成", "2026/11/05 14:12 ・ HTN Admin"), ("最終更新", "2026/11/05 14:40 ・ HTN Admin")],
    t_set_note="設定はLOを追加したダイアログで入力した内容です。「設定を編集」で同じダイアログが入力済みで開きます。公開期間と締切はコースごとにコース管理で設定します。教材・提出条件・観点は「内容」タブにあります。",
    t_set_course_lead="コース管理で設定（コースごと）", t_edit_dates="コース管理で日程を編集",
    t_set_courses=[("地域環境統計学（2026年度）", "2026/11/06 09:00 — 2026/11/13 23:59", "再提出 2026/11/20 23:59 まで"),
                   ("地域環境統計学（2026年度・金曜クラス）", "2026/11/07 09:00 — 2026/11/14 23:59", "再提出 2026/11/21 23:59 まで")],
    t_nav_course=["コース管理", "学習計画管理", "提出物の採点", "AIグレーディング"], t_toreview="提出物の採点", t_f_type="種類",
    t_course="コース", t_course_name="地域環境統計学（2026年度）", t_view_subs="提出状況を見る", t_edit_in_bm="ブック管理で編集",
    # Course Management (CourseList / CourseDetail / CourseBookDetail, syllabus squad) — the submission window lives here (PM, 22 Sep)
    t_cm="コース管理", t_cm_search="キーワードを入力", t_cm_add="コースの追加", t_cm_cols=["コース名", "コース指導法種別", "コースタイプ", "科目"],
    t_cm_rows=[("地域環境統計学（2026年度）", "集団", "講義", "統計学", True), ("地域環境統計学（2026年度・金曜クラス）", "集団", "講義", "統計学", True),
               ("社会調査法（2026年度）", "集団", "講義", "社会学", False), ("情報リテラシー入門", "個別", "演習", "情報", False)],
    t_course2_name="地域環境統計学（2026年度・金曜クラス）",
    t_c_tabs=["教材", "学習計画", "レッスン", "生徒", "クラス", "設定"], t_c_books_h="教材", t_c_book_cols=["教材名"],
    t_c_alert="学習項目（LO）の公開開始日と公開終了日を設定できます。教材を選択し、設定をしてください。",
    t_lo_av="学習項目の公開期間", t_lo_av_edit="編集", t_imp_exp="インポート/エクスポート",
    # Share Access — the AI Tutor class page's QR dialog (AIClassShare.tsx), borrowed for the course so students join by QR
    t_share="アクセスを共有", t_share_qr="QRコードを学生と共有してクラスに参加させる", t_share_code="このコードを学生と共有してクラスに参加させる",
    t_code="コード", t_download="ダウンロード", t_copy="コピー", t_copied="コードをコピーしました", t_close="閉じる", t_class_code="7QK4M2",
    t_share_row="QRコードで参加",
    # Add course — DialogUpsertCourse (fullScreen MDialogCustom) + CourseForm, the fields in production's order
    t_c_menu=["編集する", "教材を割り当てる"],
    t_add_title="コースの追加", t_f_cname="コース名", t_f_loc="拠点", t_f_method="コース指導法種別", t_f_ctype="コースタイプ", t_f_subj="科目",
    t_f_adaptive="AI学習", t_f_cbook="教材", t_loc_val="東京", t_created_msg="正常に作成されました",
    t_new_course=("地域環境統計学（2026年度・集中クラス）", "集団", "講義", "統計学"),
    # the course's Student tab (StudentTab.tsx → StudentsListAction / StudentsListFormFilterAdvanced / StudentsListTable) + one proposed column, 参加方法
    t_stu_h="生徒情報", t_stu_action="変更", t_stu_search="生徒名を入力", t_stu_filters=["学年度", "クラス", "学校", "拠点"],
    t_stu_cols=["生徒名", "学年度", "拠点", "コース期間", "クラス", "学校"],
    t_join_qr="QRコード", t_join_code="コード入力", t_join_manual="手動追加", t_join_by="追加者",
    t_join_help="参加方法は、QRコードの読み取り・コード入力で参加した生徒と、先生が手動で追加した生徒を区別します。どちらもコースの学習項目を公開開始日から見られます。",
    t_stu_rows=[("山田 花子", "KU-2041", "2026年度", "東京", "2026/10/01 - 2027/03/31", "木曜クラス", "近畿大学", "2026年度 標準", "qr", "2026/10/02 14:05"),
                ("佐藤 太郎", "KU-2042", "2026年度", "東京", "2026/10/01 - 2027/03/31", "木曜クラス", "近畿大学", "2026年度 標準", "code", "2026/10/02 14:11"),
                ("鈴木 一郎", "KU-2043", "2026年度", "東京", "2026/10/01 - 2027/03/31", "木曜クラス", "近畿大学", "2026年度 標準", "manual", "HTN Admin ・ 2026/09/28"),
                ("田中 美咲", "KU-2044", "2026年度", "東京", "2026/10/01 - 2027/03/31", "木曜クラス", "近畿大学", "2026年度 標準", "qr", "2026/10/02 14:06"),
                ("高橋 健", "KU-2045", "2026年度", "東京", "2026/10/01 - 2027/03/31", "木曜クラス", "近畿大学", "2026年度 標準", "manual", "HTN Admin ・ 2026/09/28"),
                ("伊藤 さくら", "KU-2046", "2026年度", "東京", "2026/10/09 - 2027/03/31", "木曜クラス", "近畿大学", "2026年度 標準", "qr", "2026/10/09 13:58"),
                ("渡辺 大輔", "KU-2047", "2026年度", "東京", "2026/10/09 - 2027/03/31", "—", "近畿大学", "—", "code", "2026/10/09 21:40")],
    t_av_cols=["チャプター名", "トピック名", "学習項目名", "開始日", "終了日", "再提出締切"], t_av_ph="yyyy/mm/dd, hh:mm", t_av_none="—", t_av_off="許可なし",
    t_av_saved="学習項目の公開期間が正常に更新されました",
    t_av_shared="この教材は 2 つのコースに割り当てられています（木曜クラス・金曜クラス）。公開期間はコースごとに設定します。",
    t_av_source="開始日・終了日は学習計画（study plan）のデータです。ここで保存した日程は学習計画に書き込まれ、学習計画管理で変更した日程もここに反映されます。",
    t_av_nodates="公開期間が未設定です ・ 日程を入れるまで、公開した時点で生徒に表示されます",
    # per-student due-date extension (V2 proposal): a row action on the Student tab → dialog
    t_ext_action="期限を延長", t_ext_title="期限の延長", t_ext_v2="V2 案", t_ext_lead="この生徒だけ締切を変更します。コースの日程（学習項目の公開期間）は変わりません。",
    t_ext_cols=["学習項目", "コースの公開期間", "この生徒の終了日"], t_ext_plus="＋7日", t_ext_saved="{name} の締切を延長しました", t_ext_chip="締切延長あり",
    t_av_fb_help="AIフィードバックのLOは、開始日に生徒の「やること」に表示され、終了日（締切）まで提出・差し替えができます。締切のあとに先生が確認します。再提出締切は、再提出を許可したLOにだけあります。",
    t_av_rows=[("第6回　データの整理と代表値", [("6-1　度数分布とヒストグラム", [("第6回 講義動画", "link", "2026/10/30, 09:00", "", None), ("第6回 講義資料", "lo", "2026/10/30, 09:00", "", None)]),
                                                ("6-2　代表値と散布度", [("第6回 確認クイズ", "lo", "2026/10/30, 09:00", "", None), ("第6回 演習レポート", "fb", "2026/10/30, 09:00", "2026/11/06, 23:59", "2026/11/13, 23:59")])]),
               ("第7回　データの分析と仮説検定", [("7-1　相関分析", [("第7回 講義動画", "link", "2026/11/06, 09:00", "", None), ("第7回 講義資料", "lo", "2026/11/06, 09:00", "", None), ("第7回 確認クイズ", "lo", "2026/11/06, 09:00", "", None),
                                                                   ("第7回 演習レポート", "fb", "2026/11/06, 09:00", "2026/11/13, 23:59", "2026/11/20, 23:59"), ("第7回 類題演習（相関分析）", "prac", "2026/11/06, 09:00", "", None)]),
                                                ("7-2　仮説検定", [("第7週 週次リフレクション", "fb", "2026/11/08, 09:00", "2026/11/15, 23:59", "off")])]),
               ("第8回　回帰分析", [("8-1　単回帰分析", [("第8回 講義資料", "lo", "2026/11/20, 09:00", "", None), ("第8回 演習レポート", "fb", "2026/11/20, 09:00", "2026/11/27, 23:59", "off"), ("第9回 演習レポート（追加）", "fb", "", "", "off")])])],
    t_queue_sub="確認が必要な提出の一覧です。AIフィードバックの下書きは、先生の確認を待ってここに並びます。",
    t_queue_cols=["LO", "コース", "締切", "提出", "確認待ち", "返却済み", ""], t_open="開く", t_f_course="コース", t_filters="フィルター",
    t_queue=[("第7回 演習レポート", "11月13日 23:59", "12 / 30", "12", "9"), ("第7週 週次リフレクション", "11月15日 23:59", "21 / 30", "0", "21"),
             ("第6回 演習レポート", "11月6日 23:59", "30 / 30", "0", "30")],
    t_s_mat="この課題の教材", t_mat_note="教材をアップロードすると、提出条件とコメントの観点が自動で生成されます。",
    t_drop="ファイルをドラッグ＆ドロップ、またはファイルを選ぶ", t_drop_types="PDF ・ Word ・ PNG ・ JPG",
    t_file1="第7回_課題説明.pdf", t_file2="評価基準_2026.docx",
    t_extracted="アップロード時に自動生成済み",
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
    t_rev_prev="前の提出", t_rev_next="次の提出", t_rev_pos="3 / 12", t_rev_pos_ctx="提出一覧の順 ・ 未確認から",
    t_rev_more=["この生徒の提出履歴", "元のファイルをダウンロード", "下書きを生成し直す", "生徒に表示される画面を見る"], t_rev_more_title="その他の操作",
    # overview
    t_s_status="提出状況", t_st1="提出済み", t_st1_n="12 / 30", t_st1_s="30人中12人が提出しました",
    t_st2="未確認", t_st2_n="8", t_st2_s="下書きができています。確認して返却してください", t_st3="返却済み", t_st3_n="3 / 30", t_st3_s="30人中3人に返却しました",
    t_open_list="確認する（8件）",
    t_s_sum="設定", t_sum=[("提出期間（コース）", "11月6日 09:00 — 11月13日 23:59 ・ 地域環境統計学（2026年度）"), ("再提出", "許可する ・ 11月20日 23:59 まで（コース）"),
                            ("提出方法", "ファイル ・ 写真 ・ 直接入力"), ("先生の確認", "あり（返却前に確認）")],
    # submissions
    t_cols=["生徒", "提出", "状態", ""], t_bulk="一括操作", t_bulk_note="内容を見てから返却することをおすすめします",
    t_rows=[("山田 花子", "11月11日 14:32", "wait", "確認待ち"), ("佐藤 太郎", "11月11日 18:05", "wait", "確認待ち"),
            ("鈴木 一郎", "11月12日 08:12", "wait", "確認待ち"), ("田中 美咲", "11月12日 21:40", "done", "返却済み"),
            ("高橋 健", "—", "none", "未提出")],
    t_review_btn="確認する", t_view="見る", t_rows_of="1-5 / 30", t_rows_pp="表示件数:",
    # Submission Grading (ToReviewListPage) — the AI Feedback statuses in the marking tones
    t_sg_invalid="無効な採点者", t_sg_invalid_title="本番の機能：担当が無効になっている採点者の一覧をエクスポートします（AIフィードバックとは無関係）", t_sg_tabs=["提出物", "学習目標"], t_sg_search="提出ID・生徒名・LO名で検索", t_applied="絞り込み:", t_lo_type="LOタイプ", t_all="すべて",
    t_f_status="状態", t_hl_applied="注目: あり", t_hl_f_help="先生が「クラスで紹介する」に選んだ提出だけを表示します",
    t_status={"nr": ("未確認", "st-default"), "ir": ("確認中", "st-warning"), "ret": ("返却済み", "st-success"), "back": ("差し戻し", "st-error")},
    t_sec={"auto": "自動返却", "resub": "再提出"},
    t_sg_cols=["提出ID", "LO名", "生徒名", "ユーザー名", "外部ID", "コース", "ブック", "確認者", "状態", "コメント", "提出日時", "確認日時", "返却日時"],
    t_sg_cols_lo=["提出ID", "生徒名", "ユーザー名", "外部ID", "確認者", "状態", "コメント", "提出日時", "確認日時", "返却日時"],
    t_teacher="安本 正義",
    t_subs=[dict(id="FB-260911", lo="第7回 演習レポート", student="山田 花子", user="hanako.yamada", ext="KU-2041", reviewer="安本 正義", st="ir", sec="", n=3, sub="2026/11/14 09:12", rev="--", ret="--"),
            dict(id="FB-260912", lo="第7回 演習レポート", student="佐藤 太郎", user="taro.sato", ext="KU-2042", reviewer="--", st="nr", sec="", n=3, sub="2026/11/11 18:05", rev="--", ret="--"),
            dict(id="FB-260913", lo="第7回 演習レポート", student="鈴木 一郎", user="ichiro.suzuki", ext="KU-2043", reviewer="--", st="nr", sec="", n=3, sub="2026/11/12 08:12", rev="--", ret="--"),
            dict(id="FB-260914", lo="第7回 演習レポート", student="田中 美咲", user="misaki.tanaka", ext="KU-2044", reviewer="安本 正義", st="ret", sec="", n=3, sub="2026/11/12 21:40", rev="2026/11/14 10:05", ret="2026/11/14 10:05", hl=True),
            dict(id="FB-260915", lo="第7週 週次リフレクション", student="山田 花子", user="hanako.yamada", ext="KU-2041", reviewer="--", st="ret", sec="auto", n=2, sub="2026/11/15 20:11", rev="--", ret="2026/11/16 00:05", hl=True),
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
    t_f_book="ブック", t_apply="適用", t_dash_chips=["在籍: 在籍中", "期間: 有効", "AIフィードバック 開始日: 2026/11/01 – 2026/11/30", "AIフィードバック 締切日: 2026/11/06 – 2026/11/30"], t_reset="初期設定に戻す",
    # the dashboard Filters panel: production's Enrollment status / Duration, plus the AI Feedback start and due date ranges (PM, 20 Sep)
    t_df_enroll="在籍状況", t_df_enroll_v="在籍中", t_df_dur="期間", t_df_dur_v="有効", t_df_fb="AIフィードバック",
    t_df_start="開始日", t_df_due="締切日", t_df_from="から", t_df_to="まで", t_df_start_v=("2026/11/01", "2026/11/30"), t_df_due_v=("2026/11/06", "2026/11/30"),
    t_df_help="開始日・締切日がこの範囲にあるAIフィードバックLOだけを表に残します",
    t_ai_solved="AIで解決した質問", t_ai_solved_n="1,284",
    t_ov=[("rateReview", "blue", "AIフィードバック 提出", "41", "/ 90", "3 LO ・ 30人", "T-Queue"),
          ("schedule", "orange", "確認待ち", "9", "", "先生の確認を待つ下書き", "T-Queue"),
          ("checkCircle", "green", "返却済み", "27", "", "うち自動返却 21", None),
          ("autorenew", "", "再提出", "4", "", "差し戻し 1 を含む", None)],
    t_dash_search="生徒名で検索", t_dash_modes=["トピックダッシュボード", "LOダッシュボード"], t_topic_lbl="トピック:",
    t_score_modes=["最新スコア", "最高スコア"], t_stu_name="生徒名",
    t_hl="注目", t_hl_title="クラスで紹介する例に選んだ提出", t_hl_action="クラスで紹介する", t_hl_only="注目のみ",
    t_lo_kv=["平均スコア", "完了率", "AIが回答した質問"], t_fb_kv=["提出", "確認待ち", "返却済み"],
    t_completed="完了", t_marking="採点中",
    t_matrix_help="スコアをクリックすると、その生徒のLOの提出一覧を表示します。AIフィードバックの状態をクリックすると「提出物の採点」で開きます。最新／最高スコアの切り替えはスコアのあるLOがあるときだけ使え、AIフィードバックのLOは常に最新の提出の状態を表示します。★は先生がクラスで紹介する例に選んだ提出で、選んだときの一言の理由が下に表示され、クリックするとその提出を開きます。右端の時計アイコンはその生徒の提出履歴（本番と同じ）です。",
    t_mx_los=[("第6回 演習レポート", "fb", ("30/30", "1", "28", "1")),
              ("第7回 演習レポート", "fb", ("12/30", "8", "3", "1")), ("第7週 週次リフレクション", "fb", ("21/30", "0", "21", "2")),
              ("第7回 類題演習（相関分析）", "prac", ("5/30", "12", "40 ・ 31"))],
    t_mx_students=[("山田 花子", [("fb", "ret", 3, "resub"), ("fb", "ir", 3, ""), ("fb", "ret", 2, "auto", "自分の言葉で問いを立てた"), ("prac", 2, 8, 10, 6, 0)]),
                   ("佐藤 太郎", [("fb", "nr", 3, "resub"), ("fb", "nr", 3, ""), ("fb", "ret", 2, "auto"), ("prac", 1, 4, 4, 3, 0)]),
                   ("鈴木 一郎", [("fb", "ret", 3, ""), ("fb", "nr", 3, ""), ("fb", "ret", 1, "auto"), ("prac", 0, 0, 0, 0, 0)]),
                   ("田中 美咲", [("fb", "ret", 3, "", "外れ値の扱いが的確"), ("fb", "ret", 3, "", "相関と因果を区別している"), ("fb", "ret", 2, "auto", "講義内容と結びつけた考察"), ("prac", 1, 6, 6, 6, 1)]),
                   ("高橋 健", [("fb", "ret", 3, ""), ("none",), ("fb", "ret", 2, "auto"), ("prac", 0, 0, 0, 0, 1)]),
                   ("伊藤 さくら", [("fb", "ret", 3, ""), ("fb", "nr", 3, ""), ("none",), ("prac", 1, 2, 6, 1, 0)]),
                   ("渡辺 大輝", [("fb", "back", 3, ""), ("none",), ("fb", "ret", 2, "auto"), ("prac", 0, 0, 0, 0, 0)])],
    t_no_scores="この表示にスコアのあるLOはありません", t_history="提出履歴",
    # Topic Dashboard (production's table: chapter / topic / average score / completion) plus the AI Feedback column
    t_tp_cols=["チャプター名", "トピック名", "平均スコア", "AIフィードバック ・ 類題演習", "完了"],
    t_tp_fb_lbl=["提出", "確認待ち", "返却済み"], t_tp_none="AIフィードバックのLOなし", t_tp_open="LOダッシュボードで開く",
    t_tp_help="トピック名をクリックすると、そのトピックのLOダッシュボード（生徒×LOの表）を表示します。平均スコアと完了は本番と同じ（スコアのあるLOの平均、トピックを完了した生徒数）。AIフィードバック列はそのトピックのフィードバックLOの提出・確認待ち・返却済みの件数と、先生がクラスで紹介する例に選んだ★の数、そして「インサイト」— 提出物と生成された下書きを観点に沿って読み、見落とし・良い傾向・紹介候補・提出状況のうち最も優先度の高いものをLLMが選んだ一言です。率は使いません。",
    t_ins_types={"miss": "見落とし", "good": "良い傾向", "pick": "紹介候補", "pace": "提出状況"},
    t_tp_ins={1: ("good", "外れ値の除外前後で相関係数を比べた下書きが 21/30件。第6回の狙いは届いています。"), 2: ("miss", "有意性の検定に進まない下書きが 8/12件 ・ 次回冒頭の候補"), 3: ("pick", "自分で問いを立てた振り返りが 4件 ・ クラスで紹介する候補（★2件は選択済み）")},
    t_tp_more="詳しく", t_tp_less="閉じる", t_tp_ins_lbl="インサイト", t_tp_search="チャプター名・トピック名で検索", t_tp_start="開始", t_tp_due="締切",
    t_tp_rows=[("第6回　データの整理と代表値", "6-1　度数分布とヒストグラム", 78, "30/30", None),
               ("第6回　データの整理と代表値", "6-2　代表値と散布度", 81, "29/30", ("第6回 演習レポート", "30/30", "1", "28", "1", "2026/10/30 09:00", "2026/11/06 23:59")),
               ("第7回　データの分析と仮説検定", "7-1　相関分析", 84, "11/30", ("第7回 演習レポート", "12/30", "8", "3", "1", "2026/11/06 09:00", "2026/11/13 23:59")),
               ("第7回　データの分析と仮説検定", "7-2　仮説検定", -1, "0/30", ("第7週 週次リフレクション", "21/30", "0", "21", "2", "2026/11/08 09:00", "2026/11/15 23:59")),
               ("第8回　回帰分析", "8-1　単回帰分析", -1, "0/30", None)],
    # Group Dashboard overview blocks (PRD C10.3a jobs A–C, B2 revision outcome, §1.6.4 rules)
    t_gd=dict(h="AIフィードバック ・ 今週の状況", sub="11月8日〜11月14日 ・ 対象 30人",
              b1_h="未提出", b1_rows=[("第7回 演習レポート", "18人", "高橋 健、渡辺 大輝、伊藤 さくら 他15人"), ("第7週 週次リフレクション", "9人", "伊藤 さくら 他8人")], b1_link="名簿で確認",
              b1_why="人数と名前のみ。提出率は使いません",
              b2_h="先生の確認待ち", b2_rows=[("第7回 演習レポート", "8件", "最も古いもの 3日前"), ("第6回 演習レポート", "1件", "再提出 ・ 2日前")], b2_link="確認する",
              b2_why="返却までの時間は、ここで止まっています",
              b3_h="今週のインサイト", b3_lo="第7回 演習レポート ・ 提出 12件とその下書き（返却済み 3）", b3_rank="優先 1 / 3 ・ 優先度はLLMが判断", b3_more_h="その他のインサイト",
              b3_more=[("good", "解釈のコメントで外れ値の扱いに触れた下書きが 5/12件。第6回の学びが残っています。"), ("pace", "未提出 18人。第6回は全員提出だったので、締切の周知より内容の難しさが理由の可能性があります。")], b3_line="有意性の検定の手順が最も多く指摘されています。次回の冒頭で取り上げる候補です。",
              b3_chips=[("統計処理", 8), ("解釈", 6), ("図表の見やすさ", 4)], b3_unit="件",
              b3_insight="12件のうち8件が、相関係数 r を求めたところで止まり、有意性の検定に進んでいません。そのうち3件は r ≈ 0.4 を因果の証拠として書いています。相関は「関係の強さ」、検定は「偶然ではないか」という別の問いだと次回の冒頭で一度に整理すると、両方に効きます。",
              b3_quotes=[("r = 0.42 なので、人口密度が高いほど大気汚染が進むといえる。", "佐藤 太郎 ・ 統計処理 / 解釈"), ("相関が確認できたため、仮説は正しいと判断した。", "鈴木 一郎 ・ 統計処理")],
              b3_gen="提出物と生成されたフィードバック（下書き）から、観点に沿って生成 ・ 返却前から表示 ・ 先生のみ ・ 根拠は下の件数と引用", b3_upd="更新 2026/11/14 21:05 ・ 新しい提出や下書きの編集があるたびに自動で更新", b3_open="この提出を開く",
              b4_h="フィードバックを活かした", b4_lo="第6回 演習レポート ・ 1回目 → 2回目", b4_rows=[("再提出した", "14人"), ("解消した指摘", "31 / 42件"), ("自分の言葉で書き直した", "12人")],
              b4_why="人数と件数のみ。下書き間のコメント数は比べません",
              b5_h="クラスで紹介する例", b5_rows=[("田中 美咲", "第6回 演習レポート", "外れ値の扱いが的確"), ("田中 美咲", "第7回 演習レポート", "相関と因果を区別している"),
                                                 ("山田 花子", "第7週 週次リフレクション", "自分の言葉で問いを立てた"), ("田中 美咲", "第7週 週次リフレクション", "講義内容と結びつけた考察")],
              b5_link="提出物の採点で開く", b5_open="この提出を開く", b5_why="理由は先生が「クラスで紹介する」を押すときに一言で入力します"),
    t_crit_h="観点別の指摘 ・ 第7回 演習レポート", t_crit_sub="下書き12件のうち、改善点のコメントが付いた割合",
    t_crit_rows=[("統計処理", 8), ("解釈", 6), ("図表の見やすさ", 4), ("論理構成", 3), ("Excelスキル", 2), ("生成AIリテラシー", 1)], t_crit_of=12,
    t_reqf_h="提出前チェックで止まった条件", t_reqf_sub="ファイル選択時に満たされていなかった回数（提出前に修正）",
    t_reqf_rows=[("有意性の検定が記載されている", 9), ("散布図が含まれている", 4), ("ページ数 2枚程度", 3), ("参照した講義資料の記載", 2), ("相関係数が記載されている", 0)],
    t_times="回",
    # Student Dashboard
    t_stu_list="生徒リスト",
    t_students=[("山田 花子", "3年 ・ KU-2041"), ("佐藤 太郎", "3年 ・ KU-2042"), ("鈴木 一郎", "3年 ・ KU-2043"), ("田中 美咲", "2年 ・ KU-2044"), ("高橋 健", "3年 ・ KU-2045")],
    t_ind_cols=["チャプター名", "トピック名", "学習日", "平均スコア", "完了"], t_sub_cols=["学習目標", "最終提出", "最新スコア", "最高スコア", "状態", "指摘された観点", ""],
    t_ind_rows=[("第6回　データの整理と代表値", "6-1　度数分布とヒストグラム", "2026/10/23", 85, "3/3", False, []),
                ("第6回　データの整理と代表値", "6-2　代表値と散布度", "2026/11/09", 80, "3/3", True,
                 [("第6回 講義動画", "2026/10/28", "comp", "comp"), ("第6回 確認クイズ", "2026/10/29", "8/10", "8/10"), ("第6回 演習レポート", "2026/11/09", "fb:ret", "resub")]),
                ("第7回　データの分析と仮説検定", "7-1　相関分析", "2026/11/14", 90, "3/4", True,
                 [("第7回 講義動画", "2026/11/08", "comp", "comp"), ("第7回 講義資料", "2026/11/08", "comp", "comp"), ("第7回 確認クイズ", "2026/11/10", "9/10", "9/10"), ("第7回 演習レポート", "2026/11/14", "fb:ir", "--"), ("第7回 類題演習（相関分析）", "2026/11/14", "prac", "--")]),
                ("第7回　データの分析と仮説検定", "7-2　仮説検定", "2026/11/15", -1, "1/2", True,
                 [("第7週 週次リフレクション", "2026/11/15", "fb:ret", "--"), ("第7回 仮説検定 演習問題", "--", "--", "--")]),
                ("第8回　回帰分析", "8-1　単回帰分析", "--", -1, "0/3", False, [])],
    t_resub_n="再提出 1回",
    # AI Feedback detail shown inside the LO rows (PM, 20 Sep: merged from a separate paper): per LO
    t_stu_det={"第7回 演習レポート": ("2026/11/14 09:12", "", "3", "1", "2", "", "統計処理 ・ 解釈", "", "確認する"),
               "第7週 週次リフレクション": ("2026/11/15 20:11", "2026/11/16 00:05", "2", "1", "1", "", "生成AIリテラシー", "自分の言葉で問いを立てた", "見る"),
               "第6回 演習レポート": ("2026/11/09 13:02", "2026/11/10 17:40", "3", "1", "2", "2", "統計処理 ・ 解釈（再提出で修正済み）", "", "見る")},
    t_stu_auto={"第7週 週次リフレクション"},
    t_stu_det_lbl={"sub": "提出", "ret": "返却", "cm": "コメント", "good": "良い点", "imp": "改善点", "fixed": "修正済み", "crit": "観点", "attempt": "2回目"},
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
              "courses": "BO — コース管理", "course": "BO — コース詳細（教材）", "cbook": "BO — 学習項目の公開期間",
              "mat": "BO — LO 内容（教材と提出条件）", "set": "BO — LO 設定", "queue": "BO — コース › 提出物の採点", "det": "BO — 提出状況 概要", "list": "BO — 提出一覧", "rev": "BO — 確認して返却",
              "dt": "BO — グループダッシュボード（トピック）", "dg": "BO — グループダッシュボード（LO）", "ds": "BO — 生徒ダッシュボード"},
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
    t_new_lo="Session 7 exercise report", t_snack="You have created a new LO successfully.", t_pub_snack="LO published. Students see it in their list from the start date.",
    t_dlg_title="Add Learning Objective", t_dlg_general="General Info", t_dlg_settings="Settings", t_dlg_select="Select LO Type",
    t_types=["Random Activity", "Learning Objective", "Flash Card", "Recording Assignment", "Practice Submission", "External Content"],
    t_type_fb="AI Feedback", t_new="NEW",
    t_f_name="Learning Objective", t_ph_name="Enter LO Name", t_f_ext="External LO ID", t_ph_ext="Alphanumeric characters only",
    t_f_desc="Assignment description (shown to students)",
    t_v_desc="Choose two variables from the Statistics Bureau's prefectural social indicators, compute the correlation coefficient in Excel and draw a scatter plot. Submit about two A4 pages covering your interpretation and the test of significance.",
    t_s_when="Availability and due date", t_f_start="Opens", t_v_start="6 Nov 2026, 09:00", t_f_due="Due", t_v_due="13 Nov 2026, 23:59",
    t_when_course="The start date, due date and resubmission deadline are set per course, under Course Management › Books › Learning Objectives Availability, for each course this book is assigned to. One book used by several courses can run on a different schedule in each.",
    t_when_link="Set the dates in Course Management",
    t_f_resub="Allow resubmission", t_v_resub="until 20 Nov 2026, 23:59", t_resub_note="The resubmission deadline is set in Course Management",
    t_s_how="How students submit", t_how=["File (PDF · Word · Excel · PowerPoint)", "Photos (several at once)", "Typed answer"],
    t_how_limit="500-character limit",
    t_s_review="Teacher review", t_review_on="I review the feedback before it is returned",
    t_review_body="The draft is written after the due date and stays hidden until you review, edit and return it. Students receive it as feedback from you.",
    t_review_off="Feedback is returned to students automatically after the due date, without a review step.",
    t_cancel="Cancel", t_confirm="Confirm",
    t_dlg_edit_title="Edit Learning Objective", t_type_fixed="The LO type cannot be changed after creation",
    t_lo_tabs=["Content", "Settings"], t_course_tabs=["Overview", "Submissions"], t_publish="Publish", t_edit="Edit settings", t_save="Save",
    t_set_gen=[("Type", "AI Feedback"), ("Learning Objective", "Session 7 exercise report"), ("External LO ID", "—"), ("Assignment description (shown to students)", "__desc__")],
    t_set_set=[("Availability and due date", "__course__"), ("Resubmission", "Allowed"),
               ("Submission methods", "File (PDF · Word · Excel · PowerPoint) · Photos (several at once) · Typed (500-character limit)"), ("Teacher review", "On · the teacher reviews before it is returned")],
    t_set_h_status="Publishing", t_set_status=[("Status", "__status__"), ("Created", "5 Nov 2026, 14:12 · HTN Admin"), ("Last updated", "5 Nov 2026, 14:40 · HTN Admin")],
    t_set_note="These are the values entered in the Add LO dialog. Edit settings reopens that dialog prefilled. The availability and due dates are set per course in Course Management. The material, the submission requirements and the criteria live on the Content tab.",
    t_set_course_lead="Set in Course Management, per course", t_edit_dates="Edit dates in Course Management",
    t_set_courses=[("Regional & Environmental Statistics (2026)", "2026/11/06, 09:00 — 2026/11/13, 23:59", "resubmission until 2026/11/20, 23:59"),
                   ("Regional & Environmental Statistics (2026 · Friday class)", "2026/11/07, 09:00 — 2026/11/14, 23:59", "resubmission until 2026/11/21, 23:59")],
    t_nav_course=["Course Management", "Study Plan Management", "Submission Grading", "AI Grading"], t_toreview="Submission Grading", t_f_type="Type",
    t_course="Course", t_course_name="Regional & Environmental Statistics (2026)", t_view_subs="View submissions", t_edit_in_bm="Edit in Book Management",
    t_cm="Course Management", t_cm_search="Enter your keyword", t_cm_add="Add course", t_cm_cols=["Course Name", "Teaching Method", "Course Type", "Subject"],
    t_cm_rows=[("Regional & Environmental Statistics (2026)", "Group", "Lecture", "Statistics", True), ("Regional & Environmental Statistics (2026 · Friday class)", "Group", "Lecture", "Statistics", True),
               ("Social Research Methods (2026)", "Group", "Lecture", "Sociology", False), ("Introduction to Information Literacy", "Individual", "Seminar", "Informatics", False)],
    t_course2_name="Regional & Environmental Statistics (2026 · Friday class)",
    t_c_tabs=["Books", "Study Plan", "Lesson", "Student", "Class", "Settings"], t_c_books_h="Books", t_c_book_cols=["Book Name"],
    t_c_alert="Availability dates for each learning objective in a book can be set using specific dates. To begin configuring, open the book.",
    t_lo_av="Learning Objectives Availability", t_lo_av_edit="Edit Date", t_imp_exp="Import/Export",
    t_share="Share Access", t_share_qr="Share the QR code with students to join your class", t_share_code="Share this code with students to join your class",
    t_code="Code", t_download="Download", t_copy="Copy", t_copied="Code copied", t_close="Close", t_class_code="7QK4M2",
    t_share_row="Join by QR code",
    t_c_menu=["Edit", "Assign Books"],
    t_add_title="Add course", t_f_cname="Course Name", t_f_loc="Location", t_f_method="Teaching Method", t_f_ctype="Course Type", t_f_subj="Subject",
    t_f_adaptive="Adaptive", t_f_cbook="Book", t_loc_val="Tokyo", t_created_msg="Created successfully",
    t_new_course=("Regional & Environmental Statistics (2026 · Intensive class)", "Group", "Lecture", "Statistics"),
    t_stu_h="Student Info", t_stu_action="Action", t_stu_search="Enter student name", t_stu_filters=["Academic Year", "Class", "School", "Location"],
    t_stu_cols=["Student Name", "Academic Year", "Location", "Enrollment Date", "Class", "School"],
    t_join_qr="QR code", t_join_code="Code entered", t_join_manual="Added manually", t_join_by="Added by",
    t_join_help="Joined via tells apart students who joined by scanning the QR code or entering the code from students a teacher added manually. Both see the course's learning objectives from their start dates.",
    t_stu_rows=[("Hanako Yamada", "KU-2041", "2026", "Tokyo", "2026/10/01 - 2027/03/31", "Thursday class", "Kindai University", "2026 Standard", "qr", "2026/10/02 14:05"),
                ("Taro Sato", "KU-2042", "2026", "Tokyo", "2026/10/01 - 2027/03/31", "Thursday class", "Kindai University", "2026 Standard", "code", "2026/10/02 14:11"),
                ("Ichiro Suzuki", "KU-2043", "2026", "Tokyo", "2026/10/01 - 2027/03/31", "Thursday class", "Kindai University", "2026 Standard", "manual", "HTN Admin · 2026/09/28"),
                ("Misaki Tanaka", "KU-2044", "2026", "Tokyo", "2026/10/01 - 2027/03/31", "Thursday class", "Kindai University", "2026 Standard", "qr", "2026/10/02 14:06"),
                ("Ken Takahashi", "KU-2045", "2026", "Tokyo", "2026/10/01 - 2027/03/31", "Thursday class", "Kindai University", "2026 Standard", "manual", "HTN Admin · 2026/09/28"),
                ("Sakura Ito", "KU-2046", "2026", "Tokyo", "2026/10/09 - 2027/03/31", "Thursday class", "Kindai University", "2026 Standard", "qr", "2026/10/09 13:58"),
                ("Daisuke Watanabe", "KU-2047", "2026", "Tokyo", "2026/10/09 - 2027/03/31", "—", "Kindai University", "—", "code", "2026/10/09 21:40")],
    t_av_cols=["Chapter Name", "Topic Name", "LO Name", "Start Date", "End Date", "Resubmission Due"], t_av_ph="yyyy/mm/dd, hh:mm", t_av_none="—", t_av_off="Off",
    t_av_saved="Learning Objectives Availability is updated successfully",
    t_av_shared="This book is assigned to 2 courses (Thursday and Friday classes). Availability is set per course.",
    t_av_source="Start and end dates are the study plan's data: dates saved here are written to the study plan, and dates changed in Study Plan Management show here.",
    t_av_nodates="No window set · shown to students from the moment it is published, until dates are entered",
    t_ext_action="Extend due date", t_ext_title="Extend due date", t_ext_v2="V2 proposal", t_ext_lead="Changes the due date for this student only. The course's dates (Learning Objectives Availability) stay as they are.",
    t_ext_cols=["Learning Objective", "Course window", "This student's end date"], t_ext_plus="+7 days", t_ext_saved="Due date extended for {name}", t_ext_chip="Due date extended",
    t_av_fb_help="An AI Feedback LO appears in the student's To-do on its start date; students can submit and replace their work until the end date (the due date), and the teacher reviews after it. Resubmission Due exists only for LOs that allow resubmission.",
    t_av_rows=[("Session 6 · Organising data and averages", [("6-1 · Frequency tables and histograms", [("Session 6 lecture video", "link", "2026/10/30, 09:00", "", None), ("Session 6 lecture slides", "lo", "2026/10/30, 09:00", "", None)]),
                                                                ("6-2 · Averages and dispersion", [("Session 6 check-up quiz", "lo", "2026/10/30, 09:00", "", None), ("Session 6 exercise report", "fb", "2026/10/30, 09:00", "2026/11/06, 23:59", "2026/11/13, 23:59")])]),
               ("Session 7 · Data analysis and hypothesis testing", [("7-1 · Correlation analysis", [("Session 7 lecture video", "link", "2026/11/06, 09:00", "", None), ("Session 7 lecture slides", "lo", "2026/11/06, 09:00", "", None), ("Session 7 check-up quiz", "lo", "2026/11/06, 09:00", "", None),
                                                                                                    ("Session 7 exercise report", "fb", "2026/11/06, 09:00", "2026/11/13, 23:59", "2026/11/20, 23:59"), ("Session 7 similar-questions practice (correlation)", "prac", "2026/11/06, 09:00", "", None)]),
                                                                    ("7-2 · Hypothesis testing", [("Week 7 weekly reflection", "fb", "2026/11/08, 09:00", "2026/11/15, 23:59", "off")])]),
               ("Session 8 · Regression analysis", [("8-1 · Simple regression", [("Session 8 lecture slides", "lo", "2026/11/20, 09:00", "", None), ("Session 8 exercise report", "fb", "2026/11/20, 09:00", "2026/11/27, 23:59", "off"), ("Session 9 exercise report (added)", "fb", "", "", "off")])])],
    t_queue_sub="Submissions waiting on you. AI Feedback drafts queue here until you review them, alongside manual grading.",
    t_queue_cols=["LO", "Course", "Due", "Submitted", "Waiting for you", "Returned", ""], t_open="Open", t_f_course="Course", t_filters="Filters",
    t_queue=[("Session 7 exercise report", "13 Nov, 23:59", "12 / 30", "12", "9"), ("Week 7 weekly reflection", "15 Nov, 23:59", "21 / 30", "0", "21"),
             ("Session 6 exercise report", "6 Nov, 23:59", "30 / 30", "0", "30")],
    t_s_mat="Material for this assignment", t_mat_note="The submission requirements and the comment criteria are generated automatically from what you upload.",
    t_drop="Drag and drop a file, or choose one", t_drop_types="PDF · Word · PNG · JPG",
    t_file1="Session7_assignment_brief.pdf", t_file2="Marking_criteria_2026.docx",
    t_extracted="Generated automatically on upload",
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
    t_rev_prev="Previous submission", t_rev_next="Next submission", t_rev_pos="3 / 12", t_rev_pos_ctx="in the list's order · Not Reviewed first",
    t_rev_more=["This student's submission history", "Download the original file", "Regenerate the draft", "Preview what the student sees"], t_rev_more_title="More actions",
    t_s_status="Submissions", t_st1="Submitted", t_st1_n="12 / 30", t_st1_s="12 of 30 students have submitted",
    t_st2="Not Reviewed", t_st2_n="8", t_st2_s="Drafts are ready. Review them and return", t_st3="Returned", t_st3_n="3 / 30", t_st3_s="Returned to 3 of 30 students",
    t_open_list="Review (8)",
    t_s_sum="Settings", t_sum=[("Window (course)", "6 Nov 09:00 — 13 Nov 23:59 · Regional & Environmental Statistics (2026)"), ("Resubmission", "Allowed · until 20 Nov 23:59 (course)"),
                               ("Submission", "File · Photos · Typed"), ("Teacher review", "On — before it is returned")],
    t_cols=["Student", "Submitted", "Status", ""], t_bulk="Bulk Action", t_bulk_note="Reading them first is the safer habit",
    t_rows=[("Hanako Yamada", "11 Nov, 14:32", "wait", "Waiting for you"), ("Taro Sato", "11 Nov, 18:05", "wait", "Waiting for you"),
            ("Ichiro Suzuki", "12 Nov, 08:12", "wait", "Waiting for you"), ("Misaki Tanaka", "12 Nov, 21:40", "done", "Returned"),
            ("Ken Takahashi", "—", "none", "Not submitted")],
    t_review_btn="Review", t_view="View", t_rows_of="1-5 of 30", t_rows_pp="Rows per page:",
    t_sg_invalid="Invalid Markers", t_sg_invalid_title="Production control: exports the list of markers whose assignment is no longer valid (not part of AI Feedback)", t_sg_tabs=["Submissions", "Learning Objectives"], t_sg_search="Enter Submission ID, Student Name or LO Name", t_applied="You filter by", t_lo_type="LO Type", t_all="All",
    t_f_status="Status", t_hl_applied="Highlighted: yes", t_hl_f_help="Only submissions the teacher chose to show the class",
    t_status={"nr": ("Not Reviewed", "st-default"), "ir": ("In Review", "st-warning"), "ret": ("Returned", "st-success"), "back": ("Sent Back", "st-error")},
    t_sec={"auto": "Auto-returned", "resub": "Resubmitted"},
    t_sg_cols=["Submission ID", "LO Name", "Student Name", "Username", "Ext. ID", "Course", "Book", "Reviewer", "Status", "Comments", "Submitted", "Reviewed Date", "Returned Date"],
    t_sg_cols_lo=["Submission ID", "Student Name", "Username", "Ext. ID", "Reviewer", "Status", "Comments", "Submitted", "Reviewed Date", "Returned Date"],
    t_teacher="Masayoshi Yasumoto",
    t_subs=[dict(id="FB-260911", lo="Session 7 exercise report", student="Hanako Yamada", user="hanako.yamada", ext="KU-2041", reviewer="Masayoshi Yasumoto", st="ir", sec="", n=3, sub="2026/11/14, 09:12", rev="--", ret="--"),
            dict(id="FB-260912", lo="Session 7 exercise report", student="Taro Sato", user="taro.sato", ext="KU-2042", reviewer="--", st="nr", sec="", n=3, sub="2026/11/11, 18:05", rev="--", ret="--"),
            dict(id="FB-260913", lo="Session 7 exercise report", student="Ichiro Suzuki", user="ichiro.suzuki", ext="KU-2043", reviewer="--", st="nr", sec="", n=3, sub="2026/11/12, 08:12", rev="--", ret="--"),
            dict(id="FB-260914", lo="Session 7 exercise report", student="Misaki Tanaka", user="misaki.tanaka", ext="KU-2044", reviewer="Masayoshi Yasumoto", st="ret", sec="", n=3, sub="2026/11/12, 21:40", rev="2026/11/14, 10:05", ret="2026/11/14, 10:05", hl=True),
            dict(id="FB-260915", lo="Week 7 weekly reflection", student="Hanako Yamada", user="hanako.yamada", ext="KU-2041", reviewer="--", st="ret", sec="auto", n=2, sub="2026/11/15, 20:11", rev="--", ret="2026/11/16, 00:05", hl=True),
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
    t_f_book="Book", t_apply="Apply", t_dash_chips=["Enrollment: Enrolled", "Duration: Active", "AI Feedback start: 1 Nov – 30 Nov 2026", "AI Feedback due: 6 Nov – 30 Nov 2026"], t_reset="Reset to default",
    t_df_enroll="Enrollment status", t_df_enroll_v="Enrolled", t_df_dur="Duration", t_df_dur_v="Active", t_df_fb="AI Feedback",
    t_df_start="Start date", t_df_due="Due date", t_df_from="From", t_df_to="To", t_df_start_v=("1 Nov 2026", "30 Nov 2026"), t_df_due_v=("6 Nov 2026", "30 Nov 2026"),
    t_df_help="Keeps only the AI Feedback LOs whose start or due date falls in the range",
    t_ai_solved="Questions Solved via AI", t_ai_solved_n="1,284",
    t_ov=[("rateReview", "blue", "AI Feedback submissions", "41", "/ 90", "3 LOs · 30 students", "T-Queue"),
          ("schedule", "orange", "Waiting for review", "9", "", "drafts waiting on a teacher", "T-Queue"),
          ("checkCircle", "green", "Returned", "27", "", "21 of them auto-returned", None),
          ("autorenew", "", "Resubmissions", "4", "", "including 1 sent back", None)],
    t_dash_search="Search by Student Name", t_dash_modes=["Topic Dashboard", "LO Dashboard"], t_topic_lbl="Topic:",
    t_score_modes=["Latest Score", "Highest Score"], t_stu_name="Student Name",
    t_hl="Highlighted", t_hl_title="Chosen as an example to show the class", t_hl_action="Highlight for class", t_hl_only="Highlighted only",
    t_lo_kv=["Avg. Score", "Comp. Rate", "AI-answered questions"], t_fb_kv=["Submitted", "Waiting", "Returned"],
    t_completed="Completed", t_marking="Marking",
    t_matrix_help="You may click the score to view the list of submissions made by the student for the learning objective. Click an AI Feedback status to open it in Submission Grading. Latest / Highest Score is available only when a scored LO is in view; an AI Feedback LO always shows the status of the latest submission. ★ marks a submission the teacher chose to show the class, with the few-word reason typed when highlighting it; that cell opens the submission. The clock icon at the right of a cell is production's Submission history for that student.",
    t_mx_los=[("Session 6 exercise report", "fb", ("30/30", "1", "28", "1")),
              ("Session 7 exercise report", "fb", ("12/30", "8", "3", "1")), ("Week 7 weekly reflection", "fb", ("21/30", "0", "21", "2")),
              ("Session 7 similar-questions practice (correlation)", "prac", ("5/30", "12", "40 · 31"))],
    t_mx_students=[("Hanako Yamada", [("fb", "ret", 3, "resub"), ("fb", "ir", 3, ""), ("fb", "ret", 2, "auto", "Asked a question of her own"), ('prac', 2, 8, 10, 6, 0)]),
                   ("Taro Sato", [("fb", "nr", 3, "resub"), ("fb", "nr", 3, ""), ("fb", "ret", 2, "auto"), ('prac', 1, 4, 4, 3, 0)]),
                   ("Ichiro Suzuki", [("fb", "ret", 3, ""), ("fb", "nr", 3, ""), ("fb", "ret", 1, "auto"), ('prac', 0, 0, 0, 0, 0)]),
                   ("Misaki Tanaka", [("fb", "ret", 3, "", "Handled the outlier well"), ("fb", "ret", 3, "", "Separates correlation from causation"), ("fb", "ret", 2, "auto", "Ties it back to the lecture"), ('prac', 1, 6, 6, 6, 1)]),
                   ("Ken Takahashi", [("fb", "ret", 3, ""), ("none",), ("fb", "ret", 2, "auto"), ('prac', 0, 0, 0, 0, 1)]),
                   ("Sakura Ito", [("fb", "ret", 3, ""), ("fb", "nr", 3, ""), ("none",), ('prac', 1, 2, 6, 1, 0)]),
                   ("Daiki Watanabe", [("fb", "back", 3, ""), ("none",), ("fb", "ret", 2, "auto"), ('prac', 0, 0, 0, 0, 0)])],
    t_no_scores="No scored LOs in this view", t_history="Submission history",
    t_tp_cols=["Chapter Name", "Topic Name", "Average Score", "AI Feedback · Practice", "Completion"],
    t_tp_fb_lbl=["Submitted", "Waiting", "Returned"], t_tp_none="No AI Feedback LO", t_tp_open="Open in the LO Dashboard",
    t_tp_help="Click a topic name to open its LO Dashboard (the student × LO matrix). Average Score and Completion are production's: the average over the topic's scored LOs and the number of students who completed the topic. The AI Feedback column shows the topic's feedback LO with its submitted / waiting / returned counts, the ★ number of submissions the teacher chose to show the class, and “Insights” — one line read from the submissions and their draft feedback along the rubric: of what was missed, what is going well, what is worth showing and how submissions stand, the one the LLM ranks highest. Counts, never rates.",
    t_ins_types={"miss": "Missed", "good": "Going well", "pick": "Worth showing", "pace": "Submissions"},
    t_tp_ins={1: ("good", "21 of 30 drafts compare the correlation before and after removing the outlier — Session 6's point has landed."), 2: ("miss", "8 of 12 drafts never reach the test of significance · a candidate for the next lecture's opening"), 3: ("pick", "4 reflections ask a question of their own · candidates to show the class (★ 2 already chosen)")},
    t_tp_more="Details", t_tp_less="Close", t_tp_ins_lbl="Insights", t_tp_search="Search by Chapter Name or Topic Name", t_tp_start="Start", t_tp_due="Due",
    t_tp_rows=[("Session 6 · Organising data and averages", "6-1 · Frequency tables and histograms", 78, "30/30", None),
               ("Session 6 · Organising data and averages", "6-2 · Averages and dispersion", 81, "29/30", ("Session 6 exercise report", "30/30", "1", "28", "1", "30 Oct 2026, 09:00", "6 Nov 2026, 23:59")),
               ("Session 7 · Data analysis and hypothesis testing", "7-1 · Correlation analysis", 84, "11/30", ("Session 7 exercise report", "12/30", "8", "3", "1", "6 Nov 2026, 09:00", "13 Nov 2026, 23:59")),
               ("Session 7 · Data analysis and hypothesis testing", "7-2 · Hypothesis testing", -1, "0/30", ("Week 7 weekly reflection", "21/30", "0", "21", "2", "8 Nov 2026, 09:00", "15 Nov 2026, 23:59")),
               ("Session 8 · Regression analysis", "8-1 · Simple regression", -1, "0/30", None)],
    t_gd=dict(h="AI Feedback · this week", sub="8–14 Nov · 30 students",
              b1_h="Not submitted", b1_rows=[("Session 7 exercise report", "18", "Ken Takahashi, Daiki Watanabe, Sakura Ito and 15 more"), ("Week 7 weekly reflection", "9", "Sakura Ito and 8 more")], b1_link="See the roster",
              b1_why="Counts and names, never a rate",
              b2_h="Waiting on you", b2_rows=[("Session 7 exercise report", "8", "oldest 3 days ago"), ("Session 6 exercise report", "1", "resubmission · 2 days ago")], b2_link="Review",
              b2_why="Time to return stops here",
              b3_h="Insights this week", b3_lo="Session 7 exercise report · 12 submissions and their drafts (3 returned)", b3_rank="Priority 1 of 3 · ranked by the LLM", b3_more_h="Other insights",
              b3_more=[("good", "5 of 12 drafts mention the handling of the outlier in their interpretation — Session 6's lesson is holding."), ("pace", "18 not yet submitted. Session 6 had everyone in, so the cause is more likely the difficulty than the deadline.")], b3_line="The test-of-significance procedure is the most-flagged point. A candidate for the opening recap next lecture.",
              b3_chips=[("Statistical processing", 8), ("Interpretation", 6), ("Clarity of charts", 4)], b3_unit="",
              b3_insight="8 of the 12 drafts stop at the correlation coefficient and never reach the test of significance; 3 of those read r ≈ 0.4 as evidence of causation. Correlation answers “how strong is the relationship”, the test answers “could this be chance” — sorting the two questions apart at the start of the next lecture addresses both.",
              b3_quotes=[("r = 0.42, so higher population density can be said to cause more air pollution.", "Taro Sato · Statistics / Interpretation"), ("Since a correlation was confirmed, the hypothesis was judged correct.", "Ichiro Suzuki · Statistics")],
              b3_gen="Generated from the submissions and their draft feedback, along the rubric · available before anything is returned · teacher only · grounded in the counts and quotes below", b3_upd="Updated 14 Nov 2026, 21:05 · refreshes itself whenever a submission or a draft changes", b3_open="Open this submission",
              b4_h="Acted on the feedback", b4_lo="Session 6 exercise report · draft 1 → 2", b4_rows=[("Resubmitted", "14 students"), ("Points resolved", "31 / 42"), ("Rewrote in their own words", "12 students")],
              b4_why="Counts only; comment counts are never compared across drafts",
              b5_h="Highlighted for class", b5_rows=[("Misaki Tanaka", "Session 6 exercise report", "Handled the outlier well"), ("Misaki Tanaka", "Session 7 exercise report", "Separates correlation from causation"),
                                                     ("Hanako Yamada", "Week 7 weekly reflection", "Asked a question of her own"), ("Misaki Tanaka", "Week 7 weekly reflection", "Ties it back to the lecture")],
              b5_link="Open in Submission Grading", b5_open="Open this submission", b5_why="The reason is a few words the teacher types when pressing Highlight for class"),
    t_crit_h="Comments by criterion · Session 7 exercise report", t_crit_sub="Share of the 12 drafts with an improvement comment on each criterion",
    t_crit_rows=[("Statistical processing", 8), ("Interpretation", 6), ("Clarity of charts", 4), ("Logical structure", 3), ("Excel skills", 2), ("Generative-AI literacy", 1)], t_crit_of=12,
    t_reqf_h="Requirements that stopped a submission", t_reqf_sub="Times a requirement was unmet when a file was chosen (fixed before submitting)",
    t_reqf_rows=[("The test of significance is stated", 9), ("A scatter plot is included", 4), ("About 2 pages", 3), ("The lecture material is cited", 2), ("The correlation coefficient is stated", 0)],
    t_times="×",
    t_stu_list="Student List",
    t_students=[("Hanako Yamada", "Year 3 · KU-2041"), ("Taro Sato", "Year 3 · KU-2042"), ("Ichiro Suzuki", "Year 3 · KU-2043"), ("Misaki Tanaka", "Year 2 · KU-2044"), ("Ken Takahashi", "Year 3 · KU-2045")],
    t_ind_cols=["Chapter Name", "Topic Name", "Study Date", "Average Score", "Completion"], t_sub_cols=["Learning Objective", "Latest Submission", "Latest Score", "Highest Score", "Status", "Flagged criteria", ""],
    t_ind_rows=[("Session 6 · Organising data and averages", "6-1 · Frequency tables and histograms", "2026/10/23", 85, "3/3", False, []),
                ("Session 6 · Organising data and averages", "6-2 · Averages and dispersion", "2026/11/09", 80, "3/3", True,
                 [("Session 6 lecture video", "2026/10/28", "comp", "comp"), ("Session 6 check-up quiz", "2026/10/29", "8/10", "8/10"), ("Session 6 exercise report", "2026/11/09", "fb:ret", "resub")]),
                ("Session 7 · Data analysis and hypothesis testing", "7-1 · Correlation analysis", "2026/11/14", 90, "3/4", True,
                 [("Session 7 lecture video", "2026/11/08", "comp", "comp"), ("Session 7 lecture slides", "2026/11/08", "comp", "comp"), ("Session 7 check-up quiz", "2026/11/10", "9/10", "9/10"), ("Session 7 exercise report", "2026/11/14", "fb:ir", "--"), ("Session 7 similar-questions practice (correlation)", "2026/11/14", "prac", "--")]),
                ("Session 7 · Data analysis and hypothesis testing", "7-2 · Hypothesis testing", "2026/11/15", -1, "1/2", True,
                 [("Week 7 weekly reflection", "2026/11/15", "fb:ret", "--"), ("Session 7 hypothesis-testing exercises", "--", "--", "--")]),
                ("Session 8 · Regression analysis", "8-1 · Simple regression", "--", -1, "0/3", False, [])],
    t_resub_n="1 resubmission",
    t_stu_det={"Session 7 exercise report": ("14 Nov 2026, 09:12", "", "3", "1", "2", "", "Statistics · Interpretation", "", "Review"),
               "Week 7 weekly reflection": ("15 Nov 2026, 20:11", "16 Nov 2026, 00:05", "2", "1", "1", "", "Generative-AI literacy", "Asked a question of her own", "View"),
               "Session 6 exercise report": ("9 Nov 2026, 13:02", "10 Nov 2026, 17:40", "3", "1", "2", "2", "Statistics · Interpretation (fixed on resubmission)", "", "View")},
    t_stu_auto={"Week 7 weekly reflection"},
    t_stu_det_lbl={"sub": "Submitted", "ret": "Returned", "cm": "Comments", "good": "strengths", "imp": "to improve", "fixed": "fixed", "crit": "Criteria", "attempt": "2nd attempt"},
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
              "courses": "BO — Course Management", "course": "BO — Course detail (Books)", "cbook": "BO — Learning Objectives Availability",
              "mat": "BO — LO content (material and requirements)", "set": "BO — LO settings", "queue": "BO — Course › Submission Grading", "det": "BO — Submissions overview", "list": "BO — Submissions", "rev": "BO — Review and return",
              "dt": "BO — Group Dashboard (Topic)", "dg": "BO — Group Dashboard (LO)", "ds": "BO — Student Dashboard"},
)
JA.update(TJA); EN.update(TEN)

TSCREENS = ["T-Book", "T-Dialog", "T-Material", "T-Settings", "T-Created", "T-Courses", "T-Course", "T-CourseBook", "T-Queue", "T-Detail", "T-List", "T-Review", "T-DashTopic", "T-DashGroup", "T-DashStudent"]

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
        branch = " branch" if (i == 4 and side == "book") or (i == 3 and side in ("course", "cm")) else ""
        if i == 0 and side == "dash":
            branch = " on"
        caret = f'<span class="caret">{mi("expandLess" if i in opened else "expandMore", 20)}</span>' if i in groups else ""
        lb = f'<a class="lb" href="{tfn("T-DashTopic", L)}" style="color:inherit">{label}</a>' if i == 0 else f'<span class="lb">{label}</span>'
        out += f'<div class="tn{branch}"><span class="mi">{mi(icons[i], 22)}</span>{lb}{caret}</div>'
        if i == 3:
            for j, sub in enumerate(S["t_nav_course"]):
                on = " on" if (j == 2 and side == "course") or (j == 0 and side == "cm") else ""
                if j == 2:
                    lb = f'<a class="lb" href="{tfn("T-Queue", L)}" style="color:inherit">{sub}</a>'
                elif j == 0:  # Course Management — where the submission window is set (PM, 22 Sep)
                    lb = f'<a class="lb" href="{tfn("T-Courses", L)}" style="color:inherit">{sub}</a>'
                else:
                    lb = f'<span class="lb">{sub}</span>'
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

def lm_row(S, L, name, kind, ai=False, pub="published", created=False, href=None, src=False):
    icon = {"lo": "lo", "link": "link", "flash": "flash", "fb": "rateReview", "prac": "spark"}[kind]
    nm = f'<a class="nm" href="{href}">{name}</a>' if href else f'<span class="nm">{name}</span>'
    spark = f'<span class="ticon sm primary" title="AI Tutor">{mi("spark", 16)}</span>' if ai else ""
    # AI Practice (24 Sep): the source PDF LO carries a small 演習の元 chip; the practice LO its type chip
    spark += f'<span class="tchip type" style="height:20px;font-size:11px">{S["p_src_chip"]}</span>' if src else ""
    spark += f'<span class="tchip type" style="height:20px;font-size:11px">{S["p_type_short"]}</span>' if kind == "prac" else ""
    chip = f'<span class="tchip {pub}">{S["t_pub"] if pub == "published" else S["t_unpub"]}</span>'
    return (f'<li class="lm{" just-created" if created else ""}"><span class="lm-type">{mi(icon, 16)}</span>{nm}{spark}{chip}'
            f'<span class="spc"></span><span class="ticon sm">{mi("more", 18)}</span></li>')

def book_tree(S, L, created=False, add_href=None):
    """BookDetail: chapter accordions → topic accordions → learning-material rows."""
    rows = "".join(lm_row(S, L, n, k, ai, src=(n == S["p_src_lo"]), href=(tfn("P-Source", L) if n == S["p_src_lo"] else None)) for n, k, ai in S["t_los"])
    rows += lm_row(S, L, S["p_lo"], "prac", False, href=tfn("P-Detail", L))
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

def lo_dialog(S, L, edit=False):
    """DialogCreateLearningMaterial. Create mode (T2): the type select is live and Confirm
    creates the LO. Edit mode (opened from Edit settings on T4): the same dialog prefilled,
    the type field read-only — the LO type is fixed once created (PM, 20 Sep) — and Save
    closes it."""
    if edit:
        select = f'''<label class="field" style="cursor:default">
        <span class="lbl">{S["t_f_type"]}</span>
        <span class="in" style="background:#F5F5F5;color:#616161;border-color:#E0E0E0"><span class="lm-type" style="width:20px;height:20px;flex:0 0 20px">{mi("rateReview", 12)}</span>{S["t_type_fb"]}{mi("lock", 18, "#9E9E9E")}</span>
        <span class="helper" style="margin:4px 0 0">{S["t_type_fixed"]}</span>
      </label>'''
        title, close, foot = (S["t_dlg_edit_title"],
                              f'<button class="ticon" onClick="{{{{closeEdit}}}}" aria-label="{S["t_cancel"]}">{mi("close", 24)}</button>',
                              f'<button class="tbtn" onClick="{{{{closeEdit}}}}">{S["t_cancel"]}</button><button class="tbtn contained" onClick="{{{{closeEdit}}}}">{S["t_save"]}</button>')
        ext_val = S["t_ph_ext"]
    else:
        title, close, foot = (S["t_dlg_title"], f'<a class="ticon" href="{tfn("T-Book", L)}" aria-label="{S["t_cancel"]}">{mi("close", 24)}</a>',
                              f'<a class="tbtn" href="{tfn("T-Book", L)}">{S["t_cancel"]}</a><a class="tbtn contained" href="{tfn("T-Material", L)}">{S["t_confirm"]}</a>')
        ext_val = S["t_ph_ext"]
    # the type select: MUI Select rendered closed with AI Feedback chosen; click opens the option list
    types = "".join(f'<div class="it">{t}</div>' for t in S["t_types"])
    menu = f'''<sc-if value="{{{{menuOpen}}}}" hint-placeholder-val="{{{{false}}}}"><div class="tpop" style="left:0;top:44px;width:100%">
        {types}
        <div class="it sel"><span class="lm-type" style="width:22px;height:22px">{mi("rateReview", 14)}</span><b>{S["t_type_fb"]}</b><span class="tchip new">{S["t_new"]}</span></div>
        <a class="it" href="{tfn("P-Dialog", L)}"><span class="lm-type" style="width:22px;height:22px">{mi("spark", 14)}</span><b>{S["p_type"]}</b><span class="tchip new">{S["t_new"]}</span></a>
      </div></sc-if>'''
    if not edit:
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
    <div class="dlg-head"><h2>{title}</h2>{close}</div>
    <div class="dlg-body">
      <div class="lm-section">
        <h3 class="sec-head">{S["t_dlg_general"]}</h3>
        <div class="lm-grid">
          {select}
          {field(S["t_f_name"], S["t_new_lo"], required=True)}
          <div class="span2">{field(S["t_f_desc"], S["t_v_desc"], area=True)}</div>
          {field(S["t_f_ext"], ext_val, placeholder=True)}
        </div>
      </div>
      <div class="lm-section">
        <h3 class="sec-head">{S["t_dlg_settings"]}</h3>
        <div class="settings-list">
          <div class="setting">
            <span class="setting-label" style="font-weight:500">{S["t_s_when"]}</span>
            <!-- Start, due and resubmission dates left this dialog (PM, 22 Sep): they belong to the course, in Course Management -->
            <div class="alert info" style="margin-top:10px">{mi("calendar", 20, "#2196F3")}<span>{S["t_when_course"]}<br><a href="{tfn("T-CourseBook", L)}" style="font-weight:500;display:inline-block;margin-top:4px">{S["t_when_link"]} →</a></span></div>
            <div style="display:flex;align-items:center;gap:16px;margin-top:12px">
              <button class="switch {{{{rs}}}}" onClick="{{{{toggleRs}}}}"><span class="track"></span><span>{S["t_f_resub"]}</span></button>
              <sc-if value="{{{{rsOn}}}}" hint-placeholder-val="{{{{true}}}}"><span class="helper" style="margin:0">{S["t_resub_note"]}</span></sc-if>
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
    <div class="dlg-foot">{foot}</div>
  </div>
</div>'''
    return dialog

def t_dialog(S, L):
    return tpage(S, "T-Dialog", S["t_titles"]["dialog"], book_page(S, L, "T-Dialog", extra=lo_dialog(S, L)), logic=TDLG_LOGIC)

def lo_head(S, L, screen, tab, pub, side="book", edit_action=False):
    """The LO's page header. Book Management (side="book") sets the LO up: Content and
    Settings tabs, Publish as an action, a link out to its submissions. Course › To
    Review (side="course") processes them: Overview and Submissions tabs, a link back
    to Book Management to edit (PM, 19 Sep: Book Management is for setting up LOs, not
    for the student submission flows)."""
    status = f'<span class="tchip {"published" if pub else "unpublished"}">{S["t_pub"] if pub else S["t_unpub"]}</span>'
    if side == "book" and not pub:
        # Publish works in the prototype (PM, 20 Sep): the chip flips to 公開中 and the button goes away
        status = (f'<sc-if value="{{{{pubOff}}}}" hint-placeholder-val="{{{{true}}}}"><span class="tchip unpublished">{S["t_unpub"]}</span></sc-if>'
                  f'<sc-if value="{{{{pubOn}}}}" hint-placeholder-val="{{{{false}}}}"><span class="tchip published">{S["t_pub"]}</span></sc-if>')
    if side == "book":
        crumbs = [(S["t_bm"], tfn("T-Book", L)), (S["t_book"], tfn("T-Created" if not pub else "T-Book", L)), (S["t_new_lo"], None)]
        tabs_src = S["t_lo_tabs"]
        acts = (f'<a class="tbtn" href="{tfn("T-Detail", L)}">{mi("people", 18)}{S["t_view_subs"]}</a>' +
                (f'<button class="tbtn outlined" onClick="{{{{openEdit}}}}">{mi("edit", 18)}{S["t_edit"]}</button>' if edit_action
                 else f'<a class="tbtn outlined" href="{tfn("T-Settings", L)}" title="{S["t_set_note"]}">{mi("edit", 18)}{S["t_edit"]}</a>') +
                ("" if pub else f'<sc-if value="{{{{pubOff}}}}" hint-placeholder-val="{{{{true}}}}"><button class="tbtn contained" onClick="{{{{doPublish}}}}">{S["t_publish"]}</button></sc-if>'))
        sub = ""
    else:
        crumbs = [(S["t_course"], "#"), (S["t_toreview"], tfn("T-Queue", L)), (S["t_new_lo"], None)]
        tabs_src = S["t_course_tabs"]
        # the header carried ブック管理で編集 and a ⋮ — both removed (PM, 20 Sep: the settings card below
        # has its own ブック管理で編集, and the ⋮ had nothing behind it on this page)
        acts = ""
        sub = f'<p class="helper" style="margin:-16px 0 20px;font-size:13px">{S["t_course_name"]} {S["sep"]} {S["t_book"]} {S["sep"]} {S["t_ch7"]}</p>'
    tab_hrefs = [tfn("T-Material", L), tfn("T-Settings", L)] if side == "book" else [None, None]
    tabs = "".join(
        (f'<a class="tab{" on" if i == tab else ""}" href="{h}">{t}</a>' if h and i != tab else f'<span class="tab{" on" if i == tab else ""}">{t}</span>')
        for i, (t, h) in enumerate(zip(tabs_src, tab_hrefs)))
    return f'''{tcrumbs(S, screen, crumbs)}
  <div class="tphead">
    <h1>{S["t_new_lo"]}<span class="tchip type">{mi("rateReview", 14)}{S["t_type_fb"]}</span>{status}</h1>
    <div class="acts">{acts}{"" if side == "course" else f'<span class="ticon">{mi("more", 24)}</span>'}</div>
  </div>{sub}
  <div class="tabs">{tabs}</div>'''

TMAT_LOGIC = """state = { req: true, adding: false, draft: "", r: [true, true, true, true, true], a: ["", "", ""], pub: false };
  renderVals() {
    const v = { rq: this.state.req ? "on" : "", rqOn: this.state.req, rqOff: !this.state.req,
                pubOn: this.state.pub, pubOff: !this.state.pub, doPublish: () => this.setState({ pub: true }),
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
          <span class="tchip published" style="margin-left:6px">{mi("spark", 14)}{S["t_extracted"]}</span>
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
<sc-if value="{{{{pubOff}}}}" hint-placeholder-val="{{{{true}}}}"><div class="snack" role="status">{mi("checkCircle", 20)}{S["t_snack"]}</div></sc-if>
<sc-if value="{{{{pubOn}}}}" hint-placeholder-val="{{{{false}}}}"><div class="snack" role="status">{mi("checkCircle", 20)}{S["t_pub_snack"]}</div></sc-if>
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

def sg_filterbar(S, applied=None, bulk=True, hl_filter=False):
    """Submission Grading filter bar: search, Filters, the applied-filter chips, Bulk Action —
    and, for AI Feedback, a clickable ★ chip that narrows the table to highlighted submissions."""
    chips = "".join(f'<span class="tchip" style="padding-right:4px">{c}<span class="tx">{mi("close", 12, "#fff")}</span></span>' for c in (applied or []))
    hl_chip = (f'<sc-if value="{{{{hlOn}}}}" hint-placeholder-val="{{{{false}}}}"><button class="tchip" style="padding-right:4px;cursor:pointer" onClick="{{{{toggleHl}}}}" title="{S["t_hl_title"]}">{mi("star", 12, "#ED6C02")}{S["t_hl_applied"]}<span class="tx">{mi("close", 12, "#fff")}</span></button></sc-if>'
               if hl_filter else "")
    if applied:
        app = f'<span class="tapplied">{S["t_applied"]} {chips}{hl_chip}</span>'
    elif hl_filter:
        app = f'<sc-if value="{{{{hlOn}}}}" hint-placeholder-val="{{{{false}}}}"><span class="tapplied">{S["t_applied"]} {hl_chip}</span></sc-if>'
    else:
        app = ""
    # the Filters panel (PM, 20 Sep: the Highlighted option lives under Filters, not as a chip in the bar)
    ro = ' style="background:#FAFAFA"'
    panel = (f'''<sc-if value="{{{{fOpen}}}}" hint-placeholder-val="{{{{false}}}}"><div class="tpop fpanel">
        <h4>{S["t_filters"]}</h4>
        {field(S["t_lo_type"], S["t_type_fb"], icon="expandMore", extra=ro)}
        {field(S["t_f_status"], S["t_all"], icon="expandMore", extra=ro)}
        {field(S["t_reviewer"], S["t_all"], icon="expandMore", extra=ro)}
        <button class="check {{{{hlCls}}}}" onClick="{{{{toggleHl}}}}"><span class="cbx">{mi("check", 14, "#fff")}</span><span style="display:flex;align-items:center;gap:6px">{mi("star", 16, "#ED6C02")}{S["t_hl_only"]}</span></button>
        <span class="helper" style="margin:-4px 0 0 28px">{S["t_hl_f_help"]}</span>
        <div class="ffoot"><button class="tbtn" onClick="{{{{resetF}}}}">{S["t_reset"]}</button><button class="tbtn contained" onClick="{{{{closeF}}}}">{S["t_apply"]}</button></div>
      </div></sc-if>''' if hl_filter else "")
    filters = (f'<span style="position:relative"><button class="tbtn neutral {{{{fCls}}}}" onClick="{{{{toggleF}}}}">{mi("shuffle", 18)}{S["t_filters"]}</button>{panel}</span>'
               if hl_filter else f'<span class="tbtn neutral">{mi("shuffle", 18)}{S["t_filters"]}</span>')
    right = f'<span class="tbtn contained dis">{S["t_bulk"]}{mi("expandMore", 18)}</span>' if bulk else ""
    return f'''<div class="tfilterbar">
    <div class="left"><span class="tsearch">{mi("search", 20, "#757575")}<span>{S["t_sg_search"]}</span></span>
      {filters}{app}</div>
    <div class="right">{right}</div>
  </div>'''

SG_LOGIC = """state = { hl: false, f: false };
  renderVals() {
    return { hlCls: this.state.hl ? "on" : "", hlOn: this.state.hl, hideRow: this.state.hl ? "hide" : "",
             toggleHl: () => this.setState({ hl: !this.state.hl }),
             fOpen: this.state.f, fCls: this.state.f ? "on" : "", toggleF: () => this.setState({ f: !this.state.f }),
             closeF: () => this.setState({ f: false }), resetF: () => this.setState({ hl: false, f: false }) };
  }"""

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
        star = f'<span class="hl-star" title="{S["t_hl_title"]}">{mi("star", 16)}</span>' if r.get("hl") else ""
        cells = [f'{star}<a class="cell-link num" href="{tfn("T-Review", L)}">{r["id"]}</a>']
        if lo_col:
            cells.append(f'<a class="cell-link" href="{tfn("T-Detail", L)}">{r["lo"]}</a>')
        cells += [r["student"], f'<span class="cell-muted">{r["user"]}</span>', f'<span class="cell-muted num">{r["ext"]}</span>']
        if lo_col:
            cells += [S["t_course_name"], f'<span class="cell-muted">{S["t_book"]}</span>']
        cells += [dd(r["reviewer"]), f'<span style="display:flex;gap:6px;flex-wrap:nowrap">{st_chip(S, r["st"])}{sec}</span>',
                  f'<span class="num">{r["n"]}</span>', f'<span class="num">{r["sub"]}</span>', f'<span class="num">{dd(r["rev"])}</span>', f'<span class="num">{dd(r["ret"])}</span>']
        cls = "" if r.get("hl") else ' class="{{hideRow}}"'
        trs += f'<tr{cls}><td class="cb"><span class="cbx-td"></span></td><td class="idx num">{i+1}</td>' + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
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
    <div class="acts"><span class="ticon">{mi("more", 24)}</span></div>
  </div>
  <div class="tabs">{"".join(f'<span class="tab{" on" if i == 0 else ""}">{t}</span>' for i, t in enumerate(S["t_sg_tabs"]))}</div>
  <div style="display:flex;flex-direction:column;gap:16px">
    {sg_filterbar(S, applied=[f'{S["t_lo_type"]}: {S["t_type_fb"]}'], hl_filter=True)}
    {sg_segments(S, counts)}
    {sg_table(S, L, rows, S["t_sg_cols"])}
  </div>
</div>
</div>'''
    return tpage(S, "T-Queue", S["t_titles"]["queue"], body, SG_LOGIC)

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
    <div class="tpaper"><div class="ph"><h3>{S["t_s_sum"]}</h3><span style="display:flex;gap:4px"><a class="tbtn sm" href="{tfn("T-CourseBook", L)}">{mi("calendar", 18)}{S["t_edit_dates"]}</a><a class="tbtn sm" href="{tfn("T-Settings", L)}">{mi("edit", 18)}{S["t_edit_in_bm"]}</a></span></div><div class="pb"><dl class="tkv">{kv}</dl></div></div>
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
    {sg_filterbar(S, hl_filter=True)}
    {sg_segments(S, counts)}
    {sg_table(S, L, rows, S["t_sg_cols_lo"], lo_col=False, minw=1180)}
  </div>
</div>
</div>'''
    return tpage(S, "T-List", S["t_titles"]["list"], body, SG_LOGIC)

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
    # ⋮ — production's kebab on the grading page; here it holds the secondary actions that do not
    # merit a button (PM, 20 Sep: asked what it is for): history, download, regenerate, preview
    m_hist, m_dl, m_regen, m_prev = S["t_rev_more"]
    more_menu = f'''<sc-if value="{{{{moreOpen}}}}" hint-placeholder-val="{{{{false}}}}"><div class="tpop" style="right:0;top:44px;min-width:280px">
        <a class="it" href="{tfn("T-List", L)}">{mi("history", 20, "#757575")}{m_hist}</a>
        <button class="it" onClick="{{{{toggleMore}}}}">{mi("fileDownload", 20, "#757575")}{m_dl}</button>
        <button class="it" onClick="{{{{toggleMore}}}}">{mi("autorenew", 20, "#757575")}{m_regen}</button>
        <a class="it" href="{fn("04-Feedback", L)}">{mi("eye", 20, "#757575")}{m_prev}</a>
      </div></sc-if>'''
    body = tnav(S, "course") + f'''<div class="tmain">
<div class="tscroll">
  {tcrumbs(S, "T-Review", [(S["t_course"], "#"), (S["t_toreview"], tfn("T-Queue", L)), (S["t_new_lo"], None)])}
  <div class="tphead">
    <h1>{S["t_new_lo"]}{st_chip(S, "ir")}</h1>
    <div class="acts"><span class="tbtn" title="{S["t_hl_title"]}">{mi("starOff", 18)}{S["t_hl_action"]}</span><a class="tbtn outlined" href="{tfn("T-List", L)}">{S["t_rev_back"]}</a><a class="tbtn contained" href="{tfn("T-List", L)}">{S["t_rev_send"]}</a>
      <span style="position:relative"><button class="ticon" onClick="{{{{toggleMore}}}}" aria-label="{S["t_rev_more_title"]}" title="{S["t_rev_more_title"]}">{mi("more", 24)}</button>{more_menu}</span></div>
  </div>
  <div class="grade-layout">
    <div class="info-panel">
      <div class="info-sec"><div class="rev-pager">
        <a class="ticon sm" href="{tfn("T-Review", L)}" title="{S["t_rev_prev"]}" aria-label="{S["t_rev_prev"]}"><span style="display:flex;transform:rotate(180deg)">{mi("chevron", 20)}</span></a>
        <span class="rp-mid"><span class="helper num" style="margin:0">{sub["id"]}</span><span class="rp-pos num">{S["t_rev_pos"]}</span><span class="rp-ctx">{S["t_rev_pos_ctx"]}</span></span>
        <a class="ticon sm" href="{tfn("T-Review", L)}" title="{S["t_rev_next"]}" aria-label="{S["t_rev_next"]}">{mi("chevron", 20)}</a>
      </div></div>
      <!-- previous / next submission (PM, 20 Sep): steps through the LO's submissions in the list's order
           without going back to it; in the prototype both arrows reload this one submission -->
      <!-- a 生徒には未公開 / Not visible to the student chip sat beside the ID and was removed (PM, 20 Sep):
           the status chip says In Review and the report header says draft feedback -->
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
    </div>
    <!-- a Comments section (drafts 3 / edited 1 / criteria 6) closed the panel and was removed
         (PM, 20 Sep: not useful when the comments are right there in the report) -->
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
    return tpage(S, "T-Review", S["t_titles"]["rev"], body, logic=TREV_LOGIC)

TREV_LOGIC = """state = { more: false };
  renderVals() { return { moreOpen: this.state.more, toggleMore: () => this.setState({ more: !this.state.more }) }; }"""

def dash_head(S, L, screen, tab):
    """Dashboard page head as the Back Office renders it: h1, the four dashboard tabs (Group /
    Student link to each other), with the language toggle and FOR TESTING chip on the right."""
    hrefs = [tfn("T-DashTopic", L), tfn("T-DashStudent", L), None, None]
    tabs = "".join(
        (f'<a class="tab{" on" if i == tab else ""}" href="{h}">{t}</a>' if h else f'<span class="tab">{t}</span>')
        for i, (t, h) in enumerate(zip(S["t_dash_tabs"], hrefs)))
    return f'''{tcrumbs(S, screen, [])}
  <div class="tphead" style="margin-bottom:8px"><h1>{S["t_nav"][0]}</h1></div>
  <div class="tabs">{tabs}</div>'''

DF_JS = """fOpen: this.state.f, fCls: this.state.f ? "on" : "", toggleF: () => this.setState({ f: !this.state.f }), closeF: () => this.setState({ f: false }),"""
DFILT_LOGIC = """state = { f: false };
  renderVals() { return { """ + DF_JS + """ }; }"""

def dash_filter(S):
    """Course / Book selects, Filters, a divider, Apply — GroupDashboard's filter row. Filters opens
    production's panel (Enrollment status, Duration) with an AI Feedback section added (PM, 20 Sep):
    start-date and due-date ranges that keep only the feedback LOs falling inside them."""
    ro = ' style="background:#FAFAFA"'
    def date(v):
        return f'<span class="in{"" if v else " ph"}">{v or "YYYY/MM/DD"}{mi("calendar", 18, "rgba(0,0,0,.54)")}</span>'
    def rng(label, vals):
        a, b = vals
        return (f'<div class="df-range"><span class="lbl">{label}</span><div class="df-2">'
                f'<label class="field"><span class="lbl">{S["t_df_from"]}</span>{date(a)}</label>'
                f'<label class="field"><span class="lbl">{S["t_df_to"]}</span>{date(b)}</label></div></div>')
    panel = f'''<sc-if value="{{{{fOpen}}}}" hint-placeholder-val="{{{{false}}}}"><div class="tpop fpanel" style="width:440px">
        <h4>{S["t_filters"]}</h4>
        {field(S["t_df_enroll"], S["t_df_enroll_v"], icon="expandMore", extra=ro)}
        {field(S["t_df_dur"], S["t_df_dur_v"], icon="expandMore", extra=ro)}
        <div class="df-sec"><span class="lm-type" style="width:20px;height:20px;flex:0 0 20px">{mi("rateReview", 12)}</span>{S["t_df_fb"]}</div>
        {rng(S["t_df_start"], S["t_df_start_v"])}
        {rng(S["t_df_due"], S["t_df_due_v"])}
        <span class="helper" style="margin:-4px 0 0">{S["t_df_help"]}</span>
        <div class="ffoot"><button class="tbtn" onClick="{{{{closeF}}}}">{S["t_reset"]}</button><button class="tbtn contained" onClick="{{{{closeF}}}}">{S["t_apply"]}</button></div>
      </div></sc-if>'''
    return f'''<div class="dash-filter">
    <div class="fld">{field(S["t_course"], f'<span class="ell">{S["t_course_name"]}</span>', icon="expandMore")}</div>
    <div class="fld">{field(S["t_f_book"], f'<span class="ell">{S["t_book"]}</span>', icon="expandMore")}</div>
    <span style="position:relative"><button class="tbtn neutral {{{{fCls}}}}" onClick="{{{{toggleF}}}}">{mi("filter", 18)}{S["t_filters"]}</button>{panel}</span><span class="vr"></span>
    <span class="tbtn contained">{S["t_apply"]}</span>
  </div>'''

def ov_card(icon, tone, label, val, unit, sub, href=None, L="ja"):
    body = (f'<span class="ic{" " + tone if tone else ""}">{mi(icon, 22)}</span>'
            f'<span style="min-width:0"><span class="lbl-sm">{label}</span><span class="val">{val}{f"<small>{unit}</small>" if unit else ""}</span>'
            f'{f"<span class=sub>{sub}</span>" if sub else ""}</span>')
    if href:
        return f'<a class="ov-card{" hot" if tone == "orange" else ""}" href="{tfn(href, L)}" style="color:inherit">{body}</a>'
    return f'<div class="ov-card">{body}</div>'

def dash_modes(S, L, on):
    """GroupDashboard's Topic Dashboard / LO Dashboard toggle; the mode not shown links to its board."""
    hrefs = [tfn("T-DashTopic", L), tfn("T-DashGroup", L)]
    return '<span class="toggle-group">' + "".join(
        f'<span class="on">{m}</span>' if i == on else f'<a href="{h}">{m}</a>'
        for i, (m, h) in enumerate(zip(S["t_dash_modes"], hrefs))) + '</span>'

def class_missed(S, L):
    """今週クラスが見落とした点 / What the class missed — an insight written by an LLM pass over the
    week's submissions and their generated draft feedback, grouped by rubric criterion (PM, 20 Sep:
    the basis is the drafts, not the returned comments — the teacher sees this before anything is
    returned), grounded two ways: the criterion counts stay as the anchor and the quoted passages
    link into the submissions they come from. Teacher-facing only. Lives in the Topic Dashboard's
    expanded row (PM, 20 Sep: merged there from the LO Dashboard's overview paper)."""
    G = S["t_gd"]
    quotes = "".join(
        f'<a class="bquote" href="{tfn("T-Review", L)}" title="{G["b3_open"]}"><span class="bq">“{q}”</span><span class="bwho">{who}</span>{mi("chevron", 16, "#9E9E9E")}</a>'
        for q, who in G["b3_quotes"])
    others = "".join(f'<div class="ins-row"><span class="tchip ins ins-{t}">{S["t_ins_types"][t]}</span><span>{x}</span></div>' for t, x in G["b3_more"])
    return (f'<div class="gd"><div class="blk" style="grid-column:1 / -1"><div style="display:flex;align-items:center;justify-content:space-between;gap:12px"><h4>{mi("rateReview", 14)}{G["b3_h"]}</h4>'
            f'<span class="helper num" style="margin:0;white-space:nowrap">{G["b3_upd"]}</span></div><span class="helper" style="margin:0">{G["b3_lo"]}</span>'
            f'<div style="display:flex;align-items:center;gap:8px;margin-top:2px"><span class="tchip ins ins-miss">{S["t_ins_types"]["miss"]}</span><span class="helper" style="margin:0">{G["b3_rank"]}</span></div>'
            f'<p class="bline" style="margin-top:2px">{G["b3_insight"]}</p><div class="bquotes">{quotes}</div>'
            f'<span class="helper" style="margin:6px 0 0;font-weight:500;color:#757575">{G["b3_more_h"]}</span>{others}<div class="bchips">'
            + "".join(f'<span class="tchip">{c}<b>{n}{G["b3_unit"]}</b></span>' for c, n in G["b3_chips"])
            + f'</div><div style="display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap"><a class="blink" href="{tfn("T-List", L)}">{S["t_view_subs"]}</a><span class="bwhy" style="margin:0">{mi("spark", 12)} {G["b3_gen"]}</span></div></div></div>')

TTOP_LOGIC = """state = { o: -1, f: false };
  renderVals() {
    const v = { """ + DF_JS + """ };
    for (let i = 0; i < 6; i++) { v["s" + i] = this.state.o === i ? "" : "hide"; v["oc" + i] = this.state.o === i ? "on" : ""; v["t" + i] = () => this.setState({ o: this.state.o === i ? -1 : i }); }
    return v;
  }"""

def t_dash_topic(S, L):
    """GroupDashboard in Topic Dashboard mode — production's default — as the code renders it:
    chapter / topic / average score / completion per topic, the topic name opening the LO matrix.
    For AI Feedback data one column is added: the topic's feedback LO with its counts."""
    chips = "".join(f'<span class="tchip" style="padding-right:4px">{c}<span class="tx">{mi("close", 12, "#fff")}</span></span>' for c in S["t_dash_chips"])
    k1, k2, k3 = S["t_tp_fb_lbl"]
    rows = ""
    # What the class missed (PM, 20 Sep: merged here from the LO Dashboard's overview) — one line per
    # feedback LO under its counts; 7-1 opens the full insight with its quotes in an expanded row
    for i, (ch, tp, avg, comp, fb) in enumerate(S["t_tp_rows"]):
        if not fb:
            continue  # topics without an AI Feedback LO are left off the board (PM, 20 Sep: clearer demo)
        ins = S["t_tp_ins"].get(i)
        full = False  # a 詳しく Details expansion (full insight, quotes, counts) was here and was removed (PM, 20 Sep:
                      # the teacher checks the submissions themself; the line only has to alert them)
        if fb:
            lo, sub, wait, ret, hl, start, due = fb
            wait_chip = (f'<a class="tchip wait" href="{tfn("T-List", L)}">{k2} {wait}</a>' if wait != "0"
                         else f'<span class="tchip" style="color:#757575">{k2} {wait}</span>')
            # start and due dates under the LO name (PM, 20 Sep: display them here too)
            dates = f'<span class="tp-dates num">{mi("calendar", 13, "#9E9E9E")}{S["t_tp_start"]} {start}<span class="sep">・</span>{S["t_tp_due"]} {due}</span>'
            more = (f'<button class="tp-more {{{{oc{i}}}}}" onClick="{{{{t{i}}}}}">{S["t_tp_more"]}{mi("expandMore", 16)}</button>' if full else "")
            if ins:
                typ, text = ins
                ins_line = f'<span class="tp-ins"><span class="tchip ins ins-{typ}">{S["t_ins_types"][typ]}</span><span>{text}</span>{more}</span>'
            else:
                ins_line = ""
            cell = (f'<a class="cell-link" href="{tfn("T-Detail", L)}" style="display:block">{lo}</a>{dates}'
                    f'<span style="display:flex;gap:6px"><span class="tchip">{k1} {sub}</span>{wait_chip}'
                    f'<span class="tchip published">{k3} {ret}</span>'
                    f'<span class="tchip" style="color:#ED6C02;gap:2px" title="{S["t_hl_title"]}">{mi("star", 12)}{hl}</span></span>{ins_line}')
            if tp == S["t_tp71"]:
                # AI Practice (24 Sep): the topic's practice LO under the feedback LO — from practice sets only
                cell += f'<a class="tp-ins" href="{tfn("T-DashGroup", L)}" style="color:#424242;margin-top:10px;padding-top:8px;border-top:1px dashed #E0E0E0">{S["p_tp_line"]}</a>'
        else:
            cell = f'<span class="cell-muted">{S["t_tp_none"]}</span>'
        rows += (f'<tr><td style="white-space:normal">{ch}</td>'
                 f'<td style="white-space:normal"><a class="cell-link" href="{tfn("T-DashGroup", L)}" title="{S["t_tp_open"]}">{tp}</a></td>'
                 f'<td style="width:170px">{progress(avg)}</td><td style="min-width:360px">{cell}</td>'
                 f'<td class="num" style="text-align:right;width:120px"><a href="{tfn("T-DashGroup", L)}">{comp}</a></td></tr>')
        if full:
            rows += f'<tr class="sub {{{{s{i}}}}}"><td colspan="5" style="padding:12px 16px 16px;white-space:normal">{class_missed(S, L)}</td></tr>'
    body = tnav(S, "dash") + f'''<div class="tmain">
<div class="tscroll">
  {dash_head(S, L, "T-DashTopic", 0)}
  <div style="display:flex;flex-direction:column;gap:24px">
    <div>{dash_filter(S)}<div class="chiplist">{chips}<a href="#" style="margin-left:4px">{S["t_reset"]}</a></div></div>
    <div class="tpaper" style="padding:16px">
      <div style="display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:16px">
        <span class="tsearch">{mi("search", 20, "#757575")}<span>{S["t_tp_search"]}</span></span>
        {dash_modes(S, L, 0)}
      </div>
      <div class="table-scroll"><table class="m tight"><thead><tr>{"".join(f"<th{' style=text-align:right' if i == 4 else ''}>{c}</th>" for i, c in enumerate(S["t_tp_cols"]))}</tr></thead>
        <tbody>{rows}</tbody></table></div>
      <p class="helper" style="margin:10px 0 0">{S["t_tp_help"]}</p>
    </div>
  </div>
</div>
</div>'''
    return tpage(S, "T-DashTopic", S["t_titles"]["dt"], body, logic=TTOP_LOGIC)

def progress(v, tone=None):
    if v is None or v < 0:
        return '<span class="dd">--</span>'
    cls = tone if tone else ("good" if v > 50 else "warn")
    return f'<span class="progress"><span class="pct">{v}%</span><span class="bar"><i class="{cls}" style="width:{v}%"></i></span></span>'

def t_dash_group(S, L):
    """GroupDashboard in LO Dashboard mode, on topic 7-1: the student × LO
    matrix — regular LOs show Completed or a score as production does, the AI Feedback LOs show
    the submission status in the marking tones and a link into Submission Grading."""
    chips = "".join(f'<span class="tchip" style="padding-right:4px">{c}<span class="tx">{mi("close", 12, "#fff")}</span></span>' for c in S["t_dash_chips"])
    # a tile row sat at the top of the paper — production's Questions Solved via AI, then the AI
    # Feedback overview tiles — and was removed (PM, 20 Sep: not required); the matrix carries the counts
    # LO column headers
    heads = ""
    for name, kind, vals in S["t_mx_los"]:
        if kind == "fb":
            a, b, c, hl = vals
            k1, k2, k3 = S["t_fb_kv"]
            nm = f'<a class="lo-name" href="{tfn("T-Detail", L)}" title="{name}"><span class="lm-type" style="width:20px;height:20px;flex:0 0 20px">{mi("rateReview", 12)}</span><span>{name}</span></a>'
            kv = (f'<span class="kv-line">{k1}: <b>{a}</b></span><span class="kv-line">{k2}: <b><a href="{tfn("T-List", L)}">{b}</a></b></span>'
                  f'<span class="kv-line">{k3}: <b>{c}</b><span style="display:inline-flex;align-items:center;gap:2px;margin-left:8px;color:#ED6C02">{mi("star", 12)}<b style="color:#ED6C02">{hl}</b></span></span>')
        elif kind == "prac":
            # AI Practice (24 Sep, C10.5): students with sets, sets, questions done · correct — from practice sets only
            a, b, c = vals
            k1, k2, k3 = S["p_mx_kv"]
            nm = f'<a class="lo-name" href="{tfn("P-Detail", L)}" title="{name}"><span class="lm-type" style="width:20px;height:20px;flex:0 0 20px">{mi("spark", 12)}</span><span>{name}</span></a>'
            kv = f'<span class="kv-line">{k1}: <b>{a}</b></span><span class="kv-line">{k2}: <b>{b}</b></span><span class="kv-line">{k3}: <b>{c}</b></span>'
        else:
            a, b, c = vals
            k1, k2, k3 = S["t_lo_kv"]
            nm = f'<span class="lo-name" title="{name}"><span>{name}</span></span>'
            kv = f'<span class="kv-line">{k1}: <b>{a}</b></span><span class="kv-line">{k2}: <b><a href="#">{b}</a></b></span><span class="kv-line">{k3}: <b>{c}</b></span>'
        heads += f'<th><div class="lo-col">{nm}{kv}</div></th>'
    hist = f'<span title="{S["t_history"]}" style="display:flex">{mi("history", 16)}</span>'
    def cell(c):
        if c[0] == "prac":
            # the practice LO's cell: sets · done/total · correct with the accuracy bar; informal ad hoc sessions
            # (the widget's) kept apart and labelled, never merged (C10.5); no completion status
            _, sets, done, total, correct, adhoc = c
            adhoc_l = f'<span class="cell-muted" style="font-size:11px;flex:1 0 100%">{S["p_adhoc_n"].format(n=adhoc)}</span>' if adhoc else ""
            if not sets:
                return f'<span class="stat-cell miss" style="flex-wrap:wrap;height:auto;min-height:52px;padding:8px 10px;gap:2px"><span class="dd">--</span>{adhoc_l}</span>'
            acc = int(correct / done * 100) if done else 0
            return (f'<a class="stat-cell" href="{tfn("T-DashStudent", L)}" style="color:inherit;flex-wrap:wrap;height:auto;min-height:52px;padding:8px 10px;gap:4px 8px">'
                    f'<span class="tchip type">{S["p_sets_n"].format(n=sets)}</span><span class="num" style="font-size:13px">{S["p_done_of"].format(d=done, t=total)} ・ {S["p_correct_n"].format(c=correct)}</span>'
                    f'<span class="progress" style="min-width:0;width:140px"><span class="pct">{acc}%</span><span class="bar"><i class="good" style="width:{acc}%"></i></span></span>{adhoc_l}</a>')
        if c[0] == "none":
            return '<span class="stat-cell miss"><span class="dd">--</span></span>'
        if c[0] == "comp":
            spark = f'<span title="AI Tutor">{mi("spark", 16)}</span>' if len(c) > 1 and c[1] else ""
            return f'<span class="stat-cell"><span class="tchip published">{S["t_completed"]}</span><span class="grow">{spark}{hist}</span></span>'
        if c[0] == "score":
            _, sc, ai, failed = c
            spark = f'<span title="AI Tutor">{mi("spark", 16)}</span>' if ai else ""
            return f'<span class="stat-cell{" miss" if failed else ""}"><span class="score">{sc}</span><span class="grow">{spark}{hist}</span></span>'
        _, st, n, sec = c[:4]
        hl = len(c) > 4 and c[4]
        # the 自動返却 Auto-returned secondary chip is not shown in the matrix (PM, 20 Sep: not needed);
        # it stays in Submission Grading and on the student dashboard rows. 再提出 Resubmitted stays.
        sec_chip = f'<span class="tchip st-secondary" style="height:20px;padding:0 6px;font-size:11px">{S["t_sec"][sec]}</span>' if sec and sec != "auto" else ""
        # a highlighted cell (PM, 20 Sep: the ★ Highlighted block is merged into the matrix) shows the
        # teacher's few-word reason under the status and opens that submission's review screen
        star = ""  # the lone ★ beside the status was dropped (PM, 20 Sep): the reason line below carries the star
        why = f'<span class="hl-why" title="{S["t_gd"]["b5_open"]}">{hl}</span>' if isinstance(hl, str) and hl else ""
        href = tfn("T-Review", L) if hl else tfn("T-List", L)
        return (f'<a class="stat-cell{" hl" if hl else ""}" href="{href}" style="color:inherit">{st_chip(S, st)}{sec_chip}'
                f'<span class="grow">{star}{hist}</span>{why}</a>')
    def has_hl(cells):
        return any(c[0] == "fb" and len(c) > 4 and c[4] for c in cells)
    hide_attr = ' class="{{hideRow}}"'
    rows = "".join(
        f'<tr{"" if has_hl(cells) else hide_attr}><td class="stu-col"><div class="stu-cell"><a class="cell-link" href="{tfn("T-DashStudent", L)}">{name}</a></div></td>'
        + "".join(f'<td>{cell(c)}</td>' for c in cells) + '</tr>'
        for name, cells in S["t_mx_students"])
    hl_chip = f'<button class="tchip hlf {{{{hlCls}}}}" onClick="{{{{toggleHl}}}}" title="{S["t_hl_title"]}">{mi("star", 14)}{S["t_hl_only"]}</button>'
    # the whole Latest / Highest Score toggle is greyed out when nothing in the matrix carries a score (PM, 20 Sep)
    has_score = any(kind == "score" for _, kind, _ in S["t_mx_los"])
    hi_dis = "" if has_score else f' class="dis" title="{S["t_no_scores"]}"'
    # two insight panels sat below the matrix (comments by criterion, requirements that stopped a
    # submission) and were removed (PM, 20 Sep: not required)
    # a "Not submitted" block (counts and names per LO) was first in the row and was removed (PM, 20 Sep):
    # the matrix header's 提出 12/30 and the tinted -- cells already carry it
    # a "Waiting on you" block (drafts awaiting approval per LO, oldest one's age) followed and was
    # removed too (PM, 20 Sep: not required) — the matrix header's 確認待ち count and Submission Grading carry it
    # the OVERVIEW PAPER (AI Feedback · this week) sat here with its blocks; every block was removed or
    # merged in turn (PM, 20 Sep): not-submitted, waiting, acted-on — not required; ★ highlighted — merged
    # into the matrix cells; what the class missed — merged into the Topic Dashboard (T10), where the
    # teacher lands. This board is the matrix alone now.
    body = tnav(S, "dash") + f'''<div class="tmain">
<div class="tscroll">
  {dash_head(S, L, "T-DashGroup", 0)}
  <div style="display:flex;flex-direction:column;gap:24px">
    <div>{dash_filter(S)}<div class="chiplist">{chips}<a href="#" style="margin-left:4px">{S["t_reset"]}</a></div></div>
    <div class="tpaper" style="padding:16px">
      <div style="display:flex;align-items:center;justify-content:space-between;gap:16px">
        <span class="tsearch">{mi("search", 20, "#757575")}<span>{S["t_dash_search"]}</span></span>
        {dash_modes(S, L, 1)}
      </div>
      <div style="display:flex;align-items:center;justify-content:flex-start;gap:16px;margin:16px 0 12px">
        <span class="toggle-group{" dis" if not has_score else ""}"><span{" class=on" if has_score else hi_dis}>{S["t_score_modes"][0]}</span><span{hi_dis}>{S["t_score_modes"][1]}</span></span>
        {hl_chip}
      </div>
      <div class="matrix"><table>
        <thead><tr><th class="stu-col"><div class="stu-head">{S["t_stu_name"]}</div></th>{heads}</tr></thead>
        <tbody>{rows}</tbody>
      </table></div>
      <p class="helper" style="margin:10px 0 0">{S["t_matrix_help"]}</p>
    </div>
  </div>
</div>
</div>'''
    return tpage(S, "T-DashGroup", S["t_titles"]["dg"], body, SG_LOGIC)

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
            return '<span class="dd">--</span>'  # production shows Completed here for an unscored LO; with a Status column it moves there (PM, 21 Sep)
        if v == "--":
            return '<span class="dd">--</span>'
        if v == "resub":
            return '<span class="dd">--</span>'  # a feedback LO has no highest score; the attempt count sits with the submission date (PM, 21 Sep)
        if v.startswith("fb:"):
            return '<span class="dd">--</span>'  # a feedback LO has no score; its status has its own column (PM, 21 Sep)
        if v == "prac":
            return f'<span class="num">{S["p_stu_score"]}</span>'  # AI Practice: questions correct / done across the student's sets — not a score, no max
        return v
    ind = ""
    for ch, tp, date, avg, comp, open_, los in S["t_ind_rows"]:
        ind += (f'<tr><td style="width:44px;padding-right:0"><span class="ticon sm">{mi("expandLess" if open_ else "expandMore", 20)}</span></td>'
                f'<td style="white-space:normal">{ch}</td><td style="white-space:normal">{tp}</td><td class="num">{date if date != "--" else "<span class=dd>--</span>"}</td>'
                f'<td style="width:170px">{progress(avg)}</td><td class="num" style="text-align:right">{comp}</td></tr>')
        if open_:
            def fb_cells(n, a, b):
                """Returned / Comments / Criteria / action for a feedback LO row; -- for the others
                (PM, 20 Sep: the details fit into the table as columns, not a row beneath)."""
                det = S["t_stu_det"].get(n) if a.startswith("fb:") else None
                dd = '<span class="dd">--</span>'
                if a == "prac":
                    # AI Practice (24 Sep, C10.5): status derived from the sets, never a completion flag; the sets behind the ▾
                    status = (f'<span style="display:flex;gap:4px;align-items:center;flex-wrap:wrap"><span class="tchip wait">{S["p_stu_status_prog"]}</span></span>'
                              f'<span class="cell-muted num" style="display:block;font-size:12px;margin-top:4px">{S["p_stu_sets_line"]}</span>')
                    return (f'<td>{status}</td><td class="fcrit"><span class="dd">--</span></td>'
                            f'<td style="text-align:right;padding-left:0"><a class="tbtn sm" style="height:24px;padding:0 6px;min-width:0" href="{tfn("T-DashGroup", L)}">{S["p_stu_view"]}</a></td>')
                if not det:
                    done = f'<span class="tchip published">{S["t_completed"]}</span>' if a == "comp" else dd
                    return f'<td>{done}</td><td>{dd}</td><td></td>'
                sub_dt, ret_dt, cm, good, imp, fixed, crit, hl, act = det
                Lb = S["t_stu_det_lbl"]
                cms = f'<b style="font-weight:500">{cm}</b> <span class="cell-muted" style="font-size:12px">{Lb["good"]} {good} ・ {Lb["imp"]} {imp}' + (f' ・ {Lb["fixed"]} {fixed}' if fixed else "") + '</span>'
                # Status column (PM, 21 Sep): the status chip, its secondary chip, and the date of that status beneath
                ret_day = (ret_dt.split(",")[0] if "," in ret_dt else ret_dt.split(" ")[0]) if ret_dt else ""
                st_key = a[3:]
                sec_key = "resub" if b == "resub" else ("auto" if n in S["t_stu_auto"] else "")
                sec_chip = f'<span class="tchip st-secondary" style="height:20px;padding:0 6px;font-size:11px">{S["t_sec"][sec_key]}</span>' if sec_key else ""
                when = f'<span class="cell-muted num" style="display:block;font-size:12px;margin-top:4px">{Lb["ret"]} {ret_day}</span>' if ret_day else ""
                status = f'<span style="display:flex;gap:4px;align-items:center;flex-wrap:wrap">{st_chip(S, st_key)}{sec_chip}</span>{when}'
                # the comment count (3 ・ 良い点 1 ・ 改善点 2) was a column and was dropped (PM, 21 Sep: not useful);
                # the flagged criteria stay — they say where this student stumbles
                return (f'<td>{status}</td>'
                        f'<td class="fcrit">{crit}</td>'
                        f'<td style="text-align:right;padding-left:0"><a class="tbtn sm" style="height:24px;padding:0 6px;min-width:0" href="{tfn("T-Review", L)}">{act}</a></td>')
            def lo_name(n, a):
                det = S["t_stu_det"].get(n) if a.startswith("fb:") else None
                hl = det[7] if det else ""
                # a feedback LO's name links to its overview in Submission Grading (PM, 20 Sep)
                name = f'<a class="cell-link" href="{tfn("T-Detail", L)}">{n}</a>' if det else n
                if a == "prac":
                    name = f'<a class="cell-link" href="{tfn("P-Detail", L)}" style="display:inline-flex;align-items:center;gap:6px"><span class="lm-type" style="width:20px;height:20px;flex:0 0 20px">{mi("spark", 12)}</span>{n}</a>'
                return name + (f'<span class="hl-why" style="display:block;margin-top:2px">{hl}</span>' if hl else "")
            def sub_date(d, b):
                return d + (f'<span class="cell-muted" style="display:block;font-size:12px">{S["t_resub_n"]}</span>' if b == "resub" else "")
            inner = "".join(
                f'<tr><td style="white-space:normal">{lo_name(n, a)}</td><td class="num">{sub_date(d, b)}</td><td>{sub_val(a)}</td><td>{sub_val(b)}</td>{fb_cells(n, a, b)}</tr>' for n, d, a, b in los)
            ind += (f'<tr class="sub"><td colspan="6"><table class="m inner"><colgroup><col class="c-lo"><col class="c-sub"><col class="c-sc"><col class="c-sc"><col class="c-st"><col class="c-cr"><col class="c-act"></colgroup><thead><tr>'
                    + "".join(f'<th>{c}</th>' for c in S["t_sub_cols"])
                    + f'</tr></thead><tbody>{inner}</tbody></table></td></tr>')
    # a separate AI Feedback paper (count tiles, a submissions table, a by-criterion profile) sat below the
    # production table and was merged into the LO rows above (PM, 20 Sep: merge into the existing matrix)
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
    </div>
  </div>
</div>
</div>'''
    return tpage(S, "T-DashStudent", S["t_titles"]["ds"], body, logic=DFILT_LOGIC)

TSET_LOGIC = """state = { pub: false, editing: false, review: true, resub: true, m0: true, m1: true, m2: true };
  renderVals() {
    const t = (k) => () => { const p = {}; p[k] = !this.state[k]; this.setState(p); };
    return {
      pubOn: this.state.pub, pubOff: !this.state.pub, doPublish: () => this.setState({ pub: true }),
      editing: this.state.editing, openEdit: () => this.setState({ editing: true }), closeEdit: () => this.setState({ editing: false }),
      rv: this.state.review ? "on" : "", rvOff: !this.state.review, toggleRv: t("review"),
      rs: this.state.resub ? "on" : "", rsOn: this.state.resub, toggleRs: t("resub"),
      c0: this.state.m0 ? "on" : "", c1: this.state.m1 ? "on" : "", c2: this.state.m2 ? "on" : "",
      t0: t("m0"), t1: t("m1"), t2: t("m2"),
    };
  }"""

def t_settings(S, L):
    """The LO's Settings tab (PM, 20 Sep): what the Add LO dialog collected, read-only in the
    Back Office's key-value pattern — General Info, Settings, publishing state — with Edit
    settings reopening the dialog prefilled. Content (material, requirements, criteria) is the
    other tab."""
    def kv(rows):
        out = ""
        for k, v in rows:
            if v == "__desc__":
                v = f'<span style="display:block;max-width:640px;line-height:1.6">{S["t_v_desc"]}</span>'
            elif v == "__status__":
                v = (f'<sc-if value="{{{{pubOff}}}}" hint-placeholder-val="{{{{true}}}}"><span class="tchip unpublished">{S["t_unpub"]}</span></sc-if>'
                     f'<sc-if value="{{{{pubOn}}}}" hint-placeholder-val="{{{{false}}}}"><span class="tchip published">{S["t_pub"]}</span></sc-if>')
            elif v == "__course__":
                # the window is the course's (PM, 22 Sep): one line per course this book is assigned to, and the way there
                per_course = "".join(f'<span style="display:block;line-height:1.7">{c}: <span class="num">{w}</span> <span class="cell-muted">・ {r}</span></span>' for c, w, r in S["t_set_courses"])
                v = (f'<span style="display:block;color:#757575;font-size:13px;margin-bottom:2px">{S["t_set_course_lead"]}</span>{per_course}'
                     f'<a class="tbtn sm" href="{tfn("T-CourseBook", L)}" style="margin:6px 0 0 -10px">{mi("calendar", 16)}{S["t_edit_dates"]}</a>')
            out += f'<dt>{k}</dt><dd>{v}</dd>'
        return f'<dl class="tkv" style="max-width:none">{out}</dl>'
    edit = f'<button class="tbtn sm" onClick="{{{{openEdit}}}}">{mi("edit", 18)}{S["t_edit"]}</button>'
    body = tnav(S) + f'''<div class="tmain">
<div class="tscroll">
  {lo_head(S, L, "T-Settings", 1, pub=False, edit_action=True)}
  <div style="display:flex;flex-direction:column;gap:16px">
    <p class="helper" style="margin:-8px 0 0">{S["t_set_note"]}</p>
    <div class="tpaper"><div class="ph"><h3>{S["t_dlg_general"]}</h3>{edit}</div><div class="pb">{kv(S["t_set_gen"])}</div></div>
    <div class="tpaper"><div class="ph"><h3>{S["t_dlg_settings"]}</h3>{edit}</div><div class="pb">{kv(S["t_set_set"])}</div></div>
    <div class="tpaper"><div class="ph"><h3>{S["t_set_h_status"]}</h3></div><div class="pb">{kv(S["t_set_status"])}</div></div>
  </div>
</div>
<sc-if value="{{{{pubOn}}}}" hint-placeholder-val="{{{{false}}}}"><div class="snack" role="status">{mi("checkCircle", 20)}{S["t_pub_snack"]}</div></sc-if>
<sc-if value="{{{{editing}}}}" hint-placeholder-val="{{{{false}}}}">{lo_dialog(S, L, edit=True)}</sc-if>
</div>'''
    return tpage(S, "T-Settings", S["t_titles"]["set"], body, logic=TSET_LOGIC)


# ---------- Course Management (CourseList → CourseDetail › Books → CourseBookDetail: LO Availability) ----------
# The submission window moved from the LO to the course (PM, 22 Sep). Production already has the page for
# it: Course › Books › <book> shows "Learning Objectives Availability" — chapter / topic / LO / start / end,
# edited in bulk (Edit Date → Save), importable and exportable as CSV. These three boards are that flow, as
# the syllabus squad renders it, with the AI Feedback LOs carrying their window there and nowhere else.

def course_head(S, L, screen, crumbs, title, acts=""):
    return f'''{tcrumbs(S, screen, crumbs)}
  <div class="tphead"><h1>{title}</h1><div class="acts">{acts}</div></div>'''

def qr_svg(data, size=120):
    """A real QR code (error correction H, margin 1 — QRCode.toCanvas's options in AIClassShare) as an inline SVG."""
    import qrcode
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=1, border=1)
    q.add_data(data); q.make(fit=True)
    m = q.get_matrix(); n = len(m)
    d = "".join(f"M{x} {y}h1v1h-1z" for y, row in enumerate(m) for x, v in enumerate(row) if v)
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 {n} {n}" shape-rendering="crispEdges" role="img" aria-label="QR {data}" '
            f'style="display:block"><rect width="{n}" height="{n}" fill="#fff"/><path d="{d}" fill="#212121"/></svg>')

TSHARE_LOGIC = """state = { share: false, copied: false };
  renderVals() {
    return { shareOpen: this.state.share, openShare: () => this.setState({ share: true, copied: false }),
             closeShare: () => this.setState({ share: false, copied: false }),
             copied: this.state.copied, copyCode: () => this.setState({ copied: true }) };
  }"""

TCOURSES_LOGIC = """state = { share: false, copied: false, add: false, created: false };
  renderVals() {
    return { shareOpen: this.state.share, openShare: () => this.setState({ share: true, copied: false }),
             closeShare: () => this.setState({ share: false, copied: false }),
             copied: this.state.copied, copyCode: () => this.setState({ copied: true }),
             addOpen: this.state.add, openAdd: () => this.setState({ add: true, created: false }),
             closeAdd: () => this.setState({ add: false }), saveAdd: () => this.setState({ add: false, created: true }),
             created: this.state.created, notCreated: !this.state.created };
  }"""

def add_course_dialog(S, L):
    """DialogUpsertCourse in ADD mode — a full-screen MDialogCustom: the title bar, the form on one paper
    (MPaperSectionWrapper › CourseForm), Cancel / Save in the footer. CourseForm's fields in its order:
    the course icon (AvatarInputHF), a dashed divider, Course Name (required), Location (SelectLocationInputHF —
    chips, a tree dialog behind it), Teaching Method (required; Individual / Group), Course Type, Subject,
    Book (multiple; the Adaptive switch that BookOrAdaptiveClass adds when the AI-learning feature is on is
    left out — PM, 23 Sep: remove). Drawn filled in,
    a third class of the statistics course linking the same book — Save adds it to the list."""
    name, method, ctype, subj = S["t_new_course"]
    chip = lambda t: f'<span class="tchip filled" style="height:26px">{t}<span style="display:inline-flex;width:16px;height:16px;border-radius:50%;background:#BDBDBD;color:#fff;align-items:center;justify-content:center;margin-left:2px">{mi("close", 12)}</span></span>'
    return f'''<sc-if value="{{{{addOpen}}}}" hint-placeholder-val="{{{{false}}}}"><div class="tfull" role="dialog" aria-label="{S["t_add_title"]}">
  <div class="tfull-head"><h2>{S["t_add_title"]}</h2><button class="ticon" onClick="{{{{closeAdd}}}}" aria-label="{S["t_cancel"]}">{mi("close", 24)}</button></div>
  <div class="tfull-body">
    <div class="tform">
      <div style="display:flex;justify-content:center">
        <span style="position:relative;width:112px;height:112px">
          <span style="width:112px;height:112px;border-radius:50%;background:#E3F2FD;color:#0B79D0;display:flex;align-items:center;justify-content:center">{mi("library", 44)}</span>
          <span class="ticon" style="position:absolute;right:-4px;bottom:-4px;background:#fff;box-shadow:0 1px 3px rgba(0,0,0,.3);color:#616161">{mi("camera", 20)}</span>
        </span>
      </div>
      <div style="border-top:1px dashed #BDBDBD"></div>
      {field(S["t_f_cname"], name, required=True)}
      {field(S["t_f_loc"], chip(S["t_loc_val"]), extra=' style="height:auto;min-height:40px;padding:6px 14px;gap:6px;flex-wrap:wrap"')}
      {field(S["t_f_method"], method, required=True, icon="expandMore")}
      {field(S["t_f_ctype"], ctype, icon="expandMore")}
      {field(S["t_f_subj"], subj, icon="expandMore")}
      {field(S["t_f_cbook"], chip(S["t_book"]), icon="expandMore", extra=' style="height:auto;min-height:40px;padding:6px 14px;gap:6px;flex-wrap:wrap"')}
    </div>
  </div>
  <div class="tfull-foot"><button class="tbtn" onClick="{{{{closeAdd}}}}">{S["t_cancel"]}</button><button class="tbtn contained" onClick="{{{{saveAdd}}}}">{S["t_save"]}</button></div>
</div></sc-if>
<sc-if value="{{{{created}}}}" hint-placeholder-val="{{{{false}}}}"><div class="snack" role="status" style="z-index:130">{mi("checkCircle", 20)}{S["t_created_msg"]}</div></sc-if>'''

def tcourse_logic(S):
    """T7's logic: Share Access, the ⋮ menu, the Books / Student tabs, and the per-student extension dialog
    (ext = the row index it is open for, -1 closed; extSavedFor = the row whose due date was extended)."""
    import json
    names = json.dumps([r[0] for r in S["t_stu_rows"]], ensure_ascii=False)
    n = len(S["t_stu_rows"])
    opens = ", ".join(f"openExt{i}: () => this.setState({{ ext: {i}, extSaved: false }})" for i in range(n))
    dones = ", ".join(f"extDone{i}: this.state.extSavedFor === {i}" for i in range(n))
    return f"""state = {{ share: false, copied: false, tab: "books", menu: false, ext: -1, extSaved: false, extSavedFor: -1 }};
  renderVals() {{
    const names = {names};
    return {{ shareOpen: this.state.share, openShare: () => this.setState({{ share: true, copied: false, menu: false }}),
             closeShare: () => this.setState({{ share: false, copied: false }}),
             menuOpen: this.state.menu, toggleMenu: () => this.setState({{ menu: !this.state.menu }}),
             copied: this.state.copied, copyCode: () => this.setState({{ copied: true }}),
             booksOn: this.state.tab === "books", stuOn: this.state.tab === "students",
             tabBooks: this.state.tab === "books" ? "on" : "", tabStu: this.state.tab === "students" ? "on" : "",
             showBooks: () => this.setState({{ tab: "books" }}), showStu: () => this.setState({{ tab: "students" }}),
             extOpen: this.state.ext >= 0, extName: this.state.ext >= 0 ? names[this.state.ext] : (this.state.extSavedFor >= 0 ? names[this.state.extSavedFor] : ""),
             closeExt: () => this.setState({{ ext: -1 }}), saveExt: () => this.setState({{ ext: -1, extSaved: true, extSavedFor: this.state.ext }}),
             extSaved: this.state.extSaved, {opens}, {dones} }};
  }}"""

def ext_dialog(S, L):
    """V2 proposal (24 Sep: per-student due-date extension is common in higher education and lives at the
    study plan's student level, not in the course's dates). Opened from a row on the Student tab: the
    course's AI Feedback LOs with their window, and one editable end date for this student; the first row is
    drawn already moved a week later. Save → snackbar and a chip on the student's row."""
    rows = ""
    first = True
    for ch, topics in S["t_av_rows"]:
        for tp, los in topics:
            for name, kind, start, end, resub in los:
                if kind != "fb" or not end: continue
                own = end
                extra = ""
                if first:
                    # the extension itself: a week after the course's end date
                    d = end.split(",")[0]; y, m, dd = d.split("/")
                    import datetime
                    nd = datetime.date(int(y), int(m), int(dd)) + datetime.timedelta(days=7)
                    own = f"{nd.year}/{nd.month:02d}/{nd.day:02d},{end.split(',')[1]}"
                    extra = f'<span class="tchip type" style="margin-left:8px">{S["t_ext_plus"]}</span>'
                    first = False
                rows += (f'<tr><td style="white-space:normal;min-width:220px"><span class="name-cell"><span class="lm-type" style="width:22px;height:22px;flex:0 0 22px">{mi("rateReview", 14)}</span><span style="font-weight:500">{name}</span></span></td>'
                         f'<td class="num" style="white-space:nowrap;color:#757575">{start} – {end}</td>'
                         f'<td style="white-space:nowrap"><span style="display:inline-flex;align-items:center"><input class="tinput" style="width:170px;height:36px;padding:0 8px;font-size:13px" value="{own}">{extra}</span></td></tr>')
    head = "".join(f"<th>{c}</th>" for c in S["t_ext_cols"])
    saved = S["t_ext_saved"].replace("{name}", "{{extName}}")
    return f'''<sc-if value="{{{{extOpen}}}}" hint-placeholder-val="{{{{false}}}}"><div class="tscrim">
  <div class="dlg" style="max-width:820px">
    <div class="dlg-head"><h2 style="display:flex;align-items:center;gap:10px">{S["t_ext_title"]} — {{{{extName}}}}<span class="tchip new">{S["t_ext_v2"]}</span></h2><button class="ticon" onClick="{{{{closeExt}}}}" aria-label="{S["t_cancel"]}">{mi("close", 24)}</button></div>
    <div class="dlg-body">
      <div class="alert info">{mi("info", 20, "#2196F3")}<span>{S["t_ext_lead"]}</span></div>
      <div class="tpaper" style="overflow:hidden"><div class="table-scroll"><table class="m" style="font-size:13px"><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div></div>
    </div>
    <div class="dlg-foot"><button class="tbtn" onClick="{{{{closeExt}}}}">{S["t_cancel"]}</button><button class="tbtn contained" onClick="{{{{saveExt}}}}">{S["t_save"]}</button></div>
  </div>
</div></sc-if>
<sc-if value="{{{{extSaved}}}}" hint-placeholder-val="{{{{false}}}}"><div class="snack" role="status" style="z-index:130">{mi("checkCircle", 20)}{saved}</div></sc-if>'''

def student_tab(S, L):
    """StudentTab.tsx as production lays it out: the 生徒情報 Student Info head with its 変更 Action menu
    (StudentsListAction), the name search and filter chips (StudentsListFormFilterAdvanced), then
    StudentsListTable — checkbox, Student Name (a link), Academic Year, Location, Enrollment Date
    (yyyy/LL/dd - yyyy/LL/dd), Class, School — production's columns minus Study Plan: with the course's dates
    auto-creating the study plan and enrolling every student (24 Sep), the column has nothing to say to a
    university tenant. A 参加方法 Joined via column was drawn and dropped (PM, 23 Sep). One row action is
    added as a V2 proposal: 期限を延長 Extend due date → a dialog that moves this student's end date only."""
    chips = "".join(f'<span class="tchip">{f}{mi("expandMore", 16)}</span>' for f in S["t_stu_filters"])
    head = ('<th style="width:44px;padding:0 8px"><span class="check"><span class="cbx"></span></span></th>'
            + "".join(f"<th>{c}</th>" for c in S["t_stu_cols"]) + '<th style="width:56px"></th>')
    trs = ""
    for i, (name, sid, year, loc, period, cls, school, plan, how, detail) in enumerate(S["t_stu_rows"]):
        done = f'<sc-if value="{{{{extDone{i}}}}}" hint-placeholder-val="{{{{false}}}}"><span class="tchip type" style="margin-top:4px">{mi("event", 12)}{S["t_ext_chip"]}</span></sc-if>'
        trs += (f'<tr><td style="padding:0 8px"><span class="check"><span class="cbx"></span></span></td>'
                f'<td><a class="cell-link" href="{tfn("T-DashStudent", L)}">{name}</a><br><span class="cell-muted" style="font-size:12px">{sid}</span>{done}</td>'
                f'<td>{year}</td><td>{loc}</td><td class="num" style="white-space:nowrap">{period}</td><td>{cls}</td><td>{school}</td>'
                f'<td style="text-align:right;padding:6px 12px"><button class="ticon sm" style="color:#757575" onClick="{{{{openExt{i}}}}}" title="{S["t_ext_action"]}">{mi("event", 20)}</button></td></tr>')
    return f'''<div style="display:flex;flex-direction:column;gap:16px">
    <div style="display:flex;align-items:center;justify-content:space-between;gap:16px;height:36px">
      <h3 style="margin:0;font-size:16px;font-weight:500">{S["t_stu_h"]}</h3>
      <span class="tbtn outlined">{S["t_stu_action"]}{mi("expandMore", 18)}</span>
    </div>
    <div style="display:flex;align-items:center;gap:12px;flex-wrap:wrap">
      <span class="tsearch" style="flex:0 1 360px">{mi("search", 20, "#757575")}<span>{S["t_stu_search"]}</span></span>
      <span style="display:flex;gap:8px">{chips}</span>
    </div>
    <div class="tpaper" style="overflow:hidden">
      <div class="table-scroll"><table class="m" style="font-size:13px"><thead><tr>{head}</tr></thead><tbody>{trs}</tbody></table></div>
      <div class="pagination"><span>{S["t_rows_pp"]} 10</span><span>1-{len(S["t_stu_rows"])} / {len(S["t_stu_rows"])}</span><span style="display:flex">{tools("expandMore!", "expandMore!")}</span></div>
    </div>
  </div>'''

def share_dialog(S, L):
    """AIClassShare (src/squads/syllabus/@share/aiTutor/components/AIClassShare.tsx), the AI Tutor class page's
    Share Access dialog, opened for the course: the QR code students scan to join (Download), a divider, the
    class code to type instead (Copy → snackbar), Close. Under sc-if so the board renders closed; the row's
    share icon / the header's button open it."""
    return f'''<sc-if value="{{{{shareOpen}}}}" hint-placeholder-val="{{{{false}}}}"><div class="tscrim">
  <div class="dlg" style="max-width:520px">
    <div class="dlg-head"><h2>{S["t_share"]}</h2><button class="ticon" onClick="{{{{closeShare}}}}" aria-label="{S["t_close"]}">{mi("close", 24)}</button></div>
    <div class="dlg-body" style="gap:0;padding:24px">
      <div style="display:flex;justify-content:space-between;align-items:center;gap:16px">
        <div><div style="font-size:14px;font-weight:500">{S["t_share"]}</div><div class="cell-muted" style="font-size:12px;margin-top:2px">{S["t_share_qr"]}</div></div>
        <span class="tbtn outlined">{mi("fileDownload", 18)}{S["t_download"]}</span>
      </div>
      <div style="margin-top:16px;width:fit-content;border:1px solid #E0E0E0;border-radius:4px;padding:8px">{qr_svg(S["t_class_code"], 136)}</div>
      <hr style="border:0;border-top:1px solid #E0E0E0;margin:24px 0">
      <div style="font-size:14px;font-weight:500">{S["t_code"]}</div><div class="cell-muted" style="font-size:12px;margin-top:2px">{S["t_share_code"]}</div>
      <div style="display:flex;gap:16px;align-items:center;margin-top:16px">
        <span class="field" style="flex:1 1 auto"><span class="lbl">{S["t_code"]}</span><span class="in num" style="color:#757575;letter-spacing:1px">{S["t_class_code"]}</span></span>
        <button class="tbtn outlined" onClick="{{{{copyCode}}}}">{mi("contentCopy", 18)}{S["t_copy"]}</button>
      </div>
    </div>
    <div class="dlg-foot"><button class="tbtn" style="color:#212121" onClick="{{{{closeShare}}}}">{S["t_close"]}</button></div>
  </div>
</div></sc-if>
<sc-if value="{{{{copied}}}}" hint-placeholder-val="{{{{false}}}}"><div class="snack" role="status" style="z-index:130">{mi("checkCircle", 20)}{S["t_copied"]}</div></sc-if>'''

def t_courses(S, L):
    """CourseList: page title, keyword search, Add course, the course table (Course Name with its avatar,
    Teaching Method, Course Type, Subject). Two courses share the statistics book — the Thursday and the
    Friday class — so the same LOs run on two schedules, which is what the move to the course is for."""
    head = f'<th class="idx">#</th>' + "".join(f"<th>{c}</th>" for c in S["t_cm_cols"]) + '<th style="width:56px"></th>'
    trs = ""
    for i, (name, method, ctype, subj, shared) in enumerate(S["t_cm_rows"]):
        av = f'<span class="avatar" style="background:{"#E3F2FD" if shared else "#F5F5F5"};color:{"#0B79D0" if shared else "#757575"}">{mi("library", 16)}</span>'
        nm = f'<a class="cell-link" href="{tfn("T-Course", L)}">{name}</a>' if shared else f'<span>{name}</span>'
        # ClassListTable's actions column: MIconButtonBase + ShareIcon (color primary) → AIClassShare; here it opens the same dialog for the course
        share = (f'<button class="ticon sm" style="color:#2196F3" onClick="{{{{openShare}}}}" title="{S["t_share"]}">{mi("share", 20)}</button>' if shared
                 else f'<span class="ticon sm" style="color:#BDBDBD" title="{S["t_share"]}">{mi("share", 20)}</span>')
        trs += (f'<tr><td class="idx num">{i+1}</td><td><span class="name-cell">{av}{nm}</span></td>'
                f'<td>{method}</td><td>{ctype}</td><td>{subj}</td><td style="text-align:right;padding:6px 12px">{share}</td></tr>')
    n = len(S["t_cm_rows"]); nname, nmethod, nctype, nsubj = S["t_new_course"]
    new_row = (f'<sc-if value="{{{{created}}}}" hint-placeholder-val="{{{{false}}}}"><tr class="just-created">'
               f'<td class="idx num" style="box-shadow:inset 3px 0 0 #2196F3">{n+1}</td><td><span class="name-cell"><span class="avatar">{mi("library", 16)}</span><a class="cell-link" href="{tfn("T-Course", L)}">{nname}</a></span></td>'
               f'<td>{nmethod}</td><td>{nctype}</td><td>{nsubj}</td><td style="text-align:right;padding:6px 12px">'
               f'<button class="ticon sm" style="color:#2196F3" onClick="{{{{openShare}}}}" title="{S["t_share"]}">{mi("share", 20)}</button></td></tr></sc-if>')
    trs += new_row
    count = (f'<sc-if value="{{{{notCreated}}}}" hint-placeholder-val="{{{{true}}}}"><span>1-{n} / {n}</span></sc-if>'
             f'<sc-if value="{{{{created}}}}" hint-placeholder-val="{{{{false}}}}"><span>1-{n+1} / {n+1}</span></sc-if>')
    body = tnav(S, "cm") + f'''<div class="tmain">
<div class="tscroll">
  {tcrumbs(S, "T-Courses", [])}
  <div class="tphead"><h1>{S["t_cm"]}</h1></div>
  <div style="display:flex;align-items:center;justify-content:space-between;gap:16px;margin-bottom:16px">
    <span class="tsearch">{mi("search", 20, "#757575")}<span>{S["t_cm_search"]}</span></span>
    <span style="display:flex;gap:8px"><button class="tbtn contained" onClick="{{{{openAdd}}}}">{mi("add", 18)}{S["t_cm_add"]}</button><span class="ticon">{mi("more", 24)}</span></span>
  </div>
  <div class="tpaper" style="overflow:hidden">
    <div class="table-scroll"><table class="m"><thead><tr>{head}</tr></thead><tbody>{trs}</tbody></table></div>
    <div class="pagination"><span>{S["t_rows_pp"]} 10</span>{count}<span style="display:flex">{tools("expandMore!", "expandMore!")}</span></div>
  </div>
</div>
</div>
{share_dialog(S, L)}
{add_course_dialog(S, L)}'''
    return tpage(S, "T-Courses", S["t_titles"]["courses"], body, logic=TCOURSES_LOGIC)

def t_course(S, L):
    """CourseDetail, Books tab (production's first tab when course-book is on): the course's name, its ⋮
    (Edit / Assign Books), the tabs Books · Study Plan · Lesson · Student · Class · Settings, the info alert
    that says the LO dates are set per book, and the book table — the book name opens its availability page."""
    def tab(i, t):
        if i == 0: return f'<button class="tab {{{{tabBooks}}}}" onClick="{{{{showBooks}}}}">{t}</button>'
        if i == 3: return f'<button class="tab {{{{tabStu}}}}" onClick="{{{{showStu}}}}">{t}</button>'
        return f'<span class="tab">{t}</span>'
    tabs = "".join(tab(i, t) for i, t in enumerate(S["t_c_tabs"]))
    row = (f'<tr><td class="idx num">1</td><td><a class="cell-link" href="{tfn("T-CourseBook", L)}">{S["t_book"]}</a></td></tr>')
    body = tnav(S, "cm") + f'''<div class="tmain">
<div class="tscroll">
  {course_head(S, L, "T-Course", [(S["t_cm"], tfn("T-Courses", L)), (S["t_course_name"], None)], S["t_course_name"],
               f'<span style="position:relative"><button class="ticon" onClick="{{{{toggleMenu}}}}" aria-label="More">{mi("more", 24)}</button>'
               f'<sc-if value="{{{{menuOpen}}}}" hint-placeholder-val="{{{{false}}}}"><div class="tpop" style="right:0;top:40px;min-width:220px">'
               f'<span class="it">{mi("edit", 20, "#757575")}{S["t_c_menu"][0]}</span><span class="it">{mi("library", 20, "#757575")}{S["t_c_menu"][1]}</span>'
               f'<button class="it" onClick="{{{{openShare}}}}">{mi("qrCode", 20, "#757575")}{S["t_share"]}</button></div></sc-if></span>')}
  <div class="tabs">{tabs}</div>
  <sc-if value="{{{{booksOn}}}}" hint-placeholder-val="{{{{true}}}}"><div style="display:flex;flex-direction:column;gap:16px">
    <h3 style="margin:0;font-size:16px;font-weight:500">{S["t_c_books_h"]}</h3>
    <div class="tpaper" style="overflow:hidden">
      <div class="table-scroll"><table class="m"><thead><tr><th class="idx">#</th><th>{S["t_c_book_cols"][0]}</th></tr></thead><tbody>{row}</tbody></table></div>
      <div class="pagination"><span>{S["t_rows_pp"]} 10</span><span>1-1 / 1</span><span style="display:flex">{tools("expandMore!", "expandMore!")}</span></div>
    </div>
  </div></sc-if>
  <sc-if value="{{{{stuOn}}}}" hint-placeholder-val="{{{{false}}}}">{student_tab(S, L)}</sc-if>
</div>
</div>
{share_dialog(S, L)}
{ext_dialog(S, L)}'''
    return tpage(S, "T-Course", S["t_titles"]["course"], body, logic=tcourse_logic(S))

TAV_LOGIC = """state = { edit: false, saved: false };
  renderVals() {
    return { editing: this.state.edit, viewing: !this.state.edit, saved: this.state.saved,
             openEdit: () => this.setState({ edit: true, saved: false }), cancelEdit: () => this.setState({ edit: false }),
             saveEdit: () => this.setState({ edit: false, saved: true }) };
  }"""

def av_table(S, L, edit=False):
    """CourseBookDetailContent's LO Availability table: chapter and topic cells span their rows as the
    production table merges them; each LO has its type icon; Start / End show as text, or as inputs in
    edit mode. One column is added for AI Feedback: 再提出締切 Resubmission Due — the resubmission date
    had nowhere else to go once dates left the LO (proposal, not yet decided by the PM)."""
    icon = {"lo": "lo", "link": "link", "flash": "flash", "fb": "rateReview", "prac": "spark"}
    def cell(v, kind="date"):
        if edit and kind == "date":
            return f'<input class="tinput" style="width:150px;height:36px;padding:0 8px;font-size:13px" value="{v}" placeholder="{S["t_av_ph"]}">'
        if not v:
            return f'<span class="dd">{S["t_av_none"]}</span>'
        return f'<span class="num">{v}</span>'
    trs = ""
    for ci, (ch, topics) in enumerate(S["t_av_rows"]):
        ch_rows = sum(len(los) for _, los in topics)
        first_ch = True
        for tp, los in topics:
            first_tp = True
            for name, kind, start, end, resub in los:
                cells = ""
                if first_ch:
                    cells += f'<td class="idx num" rowspan="{ch_rows}">{ci+1}</td><td rowspan="{ch_rows}" style="white-space:normal;vertical-align:top;width:170px;min-width:170px">{ch}</td>'
                    first_ch = False
                if first_tp:
                    cells += f'<td rowspan="{len(los)}" style="white-space:normal;vertical-align:top;border-left:1px solid #E0E0E0;width:170px;min-width:170px">{tp}</td>'
                    first_tp = False
                fb = kind == "fb"
                fb_chip = f'<span class="tchip type" style="margin-left:4px">{S["t_type_fb"]}</span>' if fb else (f'<span class="tchip type" style="margin-left:4px">{S["p_type_short"]}</span>' if kind == "prac" else "")
                bold = ' style="font-weight:500"' if fb else ""
                lo_cell = (f'<span class="name-cell"><span class="lm-type" style="width:22px;height:22px;flex:0 0 22px">{mi(icon[kind], 14)}</span>'
                           f'<span{bold}>{name}</span>{fb_chip}</span>')
                if not start and not end:   # an LO added to the book after the dates were set: no window yet
                    lo_cell += f'<span class="cell-muted" style="display:block;font-size:12px;margin:4px 0 0 30px">{mi("warning", 14, "#C77700")} {S["t_av_nodates"]}</span>'
                    if edit: lo_cell = lo_cell.replace(S["t_av_nodates"], S["t_av_nodates"].split(" ・ ")[0].split(" · ")[0])
                if resub is None:
                    rs = f'<span class="dd">{S["t_av_none"]}</span>'
                elif resub == "off":
                    rs = f'<span class="cell-muted">{S["t_av_off"]}</span>'
                else:
                    rs = cell(resub)
                cells += (f'<td style="border-left:1px solid #E0E0E0;white-space:normal;min-width:220px">{lo_cell}</td>'
                          f'<td style="border-left:1px solid #E0E0E0;padding:12px 10px">{cell(start)}</td><td style="padding:12px 10px">{cell(end)}</td><td style="padding:12px 10px">{rs}</td>')
                trs += f'<tr>{cells}</tr>'
    head = f'<th class="idx">#</th>' + "".join(f"<th>{c}</th>" for c in S["t_av_cols"])
    return f'''<div class="tpaper" style="overflow:hidden">
      <div class="table-scroll"><table class="m"><thead><tr>{head}</tr></thead><tbody>{trs}</tbody></table></div>
      <div class="pagination"><span>{S["t_rows_pp"]} 10</span><span>1-3 / 3</span><span style="display:flex">{tools("expandMore!", "expandMore!")}</span></div>
    </div>'''

def t_coursebook(S, L):
    """CourseBookDetail: breadcrumb Course Management / course / book, the book as the title, then the
    section head 学習項目の公開期間 with Edit Date and Import/Export (ActionPanelV2); Edit Date turns the
    date cells into inputs and swaps the actions for Cancel / Save; Save shows production's success
    snackbar. Click 編集 — it works."""
    acts_view = (f'<sc-if value="{{{{viewing}}}}" hint-placeholder-val="{{{{true}}}}"><span style="display:flex;gap:8px">'
                 f'<button class="tbtn outlined" onClick="{{{{openEdit}}}}">{mi("calendar", 18)}{S["t_lo_av_edit"]}</button>'
                 f'<span class="tbtn outlined">{mi("cloudUp", 18)}{S["t_imp_exp"]}</span></span></sc-if>')
    acts_edit = (f'<sc-if value="{{{{editing}}}}" hint-placeholder-val="{{{{false}}}}"><span style="display:flex;gap:8px">'
                 f'<button class="tbtn outlined" onClick="{{{{cancelEdit}}}}">{S["t_cancel"]}</button>'
                 f'<button class="tbtn contained" onClick="{{{{saveEdit}}}}">{S["t_save"]}</button></span></sc-if>')
    body = tnav(S, "cm") + f'''<div class="tmain">
<div class="tscroll">
  {course_head(S, L, "T-CourseBook", [(S["t_cm"], tfn("T-Courses", L)), (S["t_course_name"], tfn("T-Course", L)), (S["t_book"], None)], S["t_book"])}
  <div style="display:flex;flex-direction:column;gap:16px">
    <div style="display:flex;align-items:center;justify-content:space-between;gap:16px;height:40px">
      <h3 style="margin:0;font-size:16px;font-weight:500">{S["t_lo_av"]}</h3>{acts_view}{acts_edit}
    </div>
    <div class="alert info">{mi("info", 20, "#2196F3")}<span>{S["t_av_shared"]} {S["t_av_source"]}<br><span class="cell-muted" style="font-size:13px">{S["t_av_fb_help"]}</span></span></div>
    <sc-if value="{{{{viewing}}}}" hint-placeholder-val="{{{{true}}}}">{av_table(S, L)}</sc-if>
    <sc-if value="{{{{editing}}}}" hint-placeholder-val="{{{{false}}}}">{av_table(S, L, edit=True)}</sc-if>
  </div>
</div>
<sc-if value="{{{{saved}}}}" hint-placeholder-val="{{{{false}}}}"><div class="snack" role="status">{mi("checkCircle", 20)}{S["t_av_saved"]}</div></sc-if>
</div>'''
    return tpage(S, "T-CourseBook", S["t_titles"]["cbook"], body, logic=TAV_LOGIC)

TBUILDERS = {"T-Book": t_book, "T-Dialog": t_dialog, "T-Created": t_created, "T-Material": t_material, "T-Settings": t_settings,
             "T-Courses": t_courses, "T-Course": t_course, "T-CourseBook": t_coursebook,
             "T-Queue": t_queue, "T-Detail": t_detail, "T-List": t_list, "T-Review": t_review,
             "T-DashTopic": t_dash_topic, "T-DashGroup": t_dash_group, "T-DashStudent": t_dash_student}


# =====================================================================================
# AI PRACTICE — the Similar Questions Practice LO (RISO first; here fitted into the Kindai course)
# Source: jamessim-source/AIpractice — docs/prototype-plan.md, docs/c10-finalized-logic.md (PRD C10,
# PM decisions of 24 Sep), contract/openapi.yaml, mock-service/seed.py, and the clickable prototype
# prototype/sqp-prototype.html (branch `prototype`). The logic below is that prototype's, redrawn on this
# canvas's production components: Book Management, Course Management, the dashboards, the student app.
# The bank is statistics (Topic 7-1 相関分析) so the practice LO sits in the same book as the rest.
# =====================================================================================

P_JA = dict(
    # names
    p_type="類題演習 LO", p_type_short="類題演習", p_type_en="Similar Questions Practice LO",
    p_lo="第7回 類題演習（相関分析）", p_src_lo="第7回 講義資料", p_src_lo_full="第7回 講義資料（PDF）",
    p_src_chip="演習の元", p_ai="AI",
    # Back Office — Add LO dialog
    p_dlg_title="学習目標（LO）を追加", p_dlg_name="第7回 類題演習（相関分析）", p_dlg_ext="—",
    p_dlg_desc="第7回 講義資料（PDF）の問題を切り取ると、AIが類題を集めて演習セットをつくります。何度でもセットを追加できます。",
    p_f_link="リンク元の LO", p_link_req="必須", p_link_hint="この教材の中で「演習の元として利用可」がオンの LO だけが表示されます。すでに他の類題演習 LO にリンクされている LO も選べます。",
    p_link_none="この教材に対象の LO がありません。先に PDF LO の「演習の元として利用可」をオンにしてください。",
    p_empty_lbl="対象 LO がないときの表示",
    p_hidden="この種類では非表示：満点、合格点、手動採点、AI Tutor、パスワード。生徒にはセット数・解答数・正解数だけを表示し、完了ステータスはありません。",
    p_cant_save="保存できません：類題演習 LO は作成時に対象 LO へのリンクが必要です。",
    p_gate="Syllabus_BackOffice_AIPractice ・ syllabus.ai_practice.is_enabled",
    p_gate_note="フラグとテナント設定の両方がオンのときだけ、この種類が選べます。",
    # Back Office — source LO settings
    p_src_type="学習目標（PDF 学習ガイド付き）", p_src_pages="24ページ ・ 公開中",
    p_tog="演習の元として利用可", p_tog_desc="生徒はこの LO の PDF から類題演習セットを作れます。既定はオフ。",
    p_tog_locked="オフにできません：生徒がすでに演習セットを作成しています。",
    p_linked_by="リンクされている類題演習 LO", p_linked_none="まだこの LO にリンクする類題演習 LO はありません。",
    p_src_kv=[("種類", "学習目標"), ("学習ガイド", "第7回_講義資料.pdf ・ 24ページ"), ("AI Tutor", "オフ"), ("公開期間", "__course__")],
    # Back Office — practice LO detail
    p_det_kv_link="リンク元の LO", p_det_sets="生徒が作ったセット数", p_det_sets_v="12 セット（生徒 5人 / 30人）",
    p_det_comp="完了ステータス", p_det_comp_v="なし（仕様 ・ PRD C3）", p_det_over="先生・管理者による操作", p_det_over_v="なし ・ セットの削除・変更・再生成はできません",
    p_det_visible="生徒アプリでの見え方", p_det_visible_v="トピック「7-1　相関分析」の中に ✦ バッジと「類題演習」タグ付きのカードとして表示されます。セット数だけを示し、完了チップはありません。",
    p_det_dates="公開期間", p_det_dates_v="コース管理で開始日を設定（終了日なし ・ 締切のない LO）", p_det_dash="ダッシュボードで見る",
    p_det_stock="用意された類題", p_det_stock_v="出典 3問 ・ 在庫は生徒に表示しません",
    # dashboards
    p_dash_col="類題演習", p_mx_kv=["セットのある生徒", "セット", "解答 ・ 正解"], p_mx_none="--",
    p_sets_n="{n}セット", p_done_of="{d}/{t}問", p_correct_n="正解 {c}", p_adhoc_n="非公式 {n}回", p_acc="正答率",
    p_tp_line="✦ 第7回 類題演習 ・ セットのある生徒 5/30 ・ セット 12 ・ 解答 40問 ・ 正解 31問",
    p_stu_sets_line="セット 2（完了 1 ・ 途中 1）", p_stu_status_prog="途中", p_stu_status_done="完了", p_stu_view="セット一覧",
    p_stu_score="正解 6/8",
    # student — course / to-do
    p_lt="類題演習", p_course_sub="第7回 講義資料 の PDF から ・ 2セット", p_todo_chip="セット2 つづき 2/4",
    # student — practice LO screen
    p_questions="問題数", p_correct="正解数", p_round_line="1回 10問ずつ ・ {d}/{t}問 解答 ・ 間違い {w}問",
    p_sets_h="セット", p_set_n="セット{i}", p_done="完了", p_notdone="未完了", p_q_n="{d}/{t}問", p_correct_q="正解 {c}問",
    p_print="印刷する", p_add_set="演習を追加する", p_create_set="演習セットをつくる", p_from_pdf="第7回 講義資料 の PDF から",
    p_history="学習履歴", p_hist_row="{r}/{n}問 正解", p_hist=[("11月9日 14:02", 1, 5, 6)],
    p_cta_done_note="セット1 は完了しています（解き直しはありません）", p_cta_print="セット1 を印刷する", p_cta_print2="セット2 を印刷する",
    p_cta_resume_note="セット2 ・ つづき（2/4）", p_resume="つづきから始める", p_start="演習を始める",
    p_no_status="完了ステータスやマスターレベルはありません。セットは何度でも追加できます。",
    # student — crop
    p_crop_title="第7回 講義資料（PDF）", p_crop_mode="演習をつくる", p_crop_hint="PDF の問題を枠で囲んでください（複数可）。学習ガイド画面の「Mana AI」クロップと同じ操作です。",
    p_crop_pages="p.12–14 / 24", p_crop_cta="演習をつくる →", p_frames_n="{n}か所 選択中", p_frames_none="枠を1つ以上選ぶと「演習をつくる」が押せます",
    p_pdf_h="7-1 相関分析 — 演習問題", p_pdf_sub="第7回 講義資料 p.12–14",
    # student — setup
    p_setup_title="切り取った範囲", p_dest="追加先", p_count="問題数", p_per_q="問 × {k}問題", p_max_per="1問につき 最大 {m}問",
    p_total="全部で {n}問つくります", p_cap_hint="上限は選んだ範囲でいちばん少ない在庫に合わせています。在庫の総数は表示しません。",
    p_create="演習を作る", p_question="問題", p_one="1問",
    p_nomatch_t="この範囲の類題は用意されていません。", p_nomatch_b="問題全体が枠に入るように切り取って、もう一度お試しください。",
    p_nomatch_h="セットは作成されません。生成へのフォールバックはありません。", p_recrop="もう一度 切り取る", p_demo_nomatch="DEMO：一致なし",
    p_demo_match="DEMO：一致あり",
    # student — wait / practice
    p_making="作成中", p_collecting="類題を集めています…", p_wait_note="作成のときだけ表示します。読み取りだけなら待たせません。",
    p_practice="類題演習", p_one_attempt="1回だけ答えられます", p_next="次へ →", p_end_round="この回を終える",
    p_correct_bang="正解！", p_correct_is="正解は {ci}", p_round_done="演習 おわり！", p_round_sum="{n}問のうち {r}問 正解",
    p_set_done="このセットは完了しました", p_back_sets="セット一覧に戻る", p_q_of="{i} / {n}",
    # student — print
    p_sheet_title="類題演習 セット1（6問）", p_sheet_chip="印刷プレビュー ・ PDF は都度再生成", p_q_label="問{n}",
    p_sheet_foot="出典の問題と在庫数は印刷しません。", p_print_btn="印刷する", p_close="閉じる",
    # titles
    p_titles={"dialog": "BO — LOを追加（類題演習）", "src": "BO — 元の LO の設定（演習の元として利用可）", "det": "BO — 類題演習 LO の詳細",
              "sets": "類題演習 — セット一覧", "crop": "類題演習 — PDF を切り取る", "setup": "類題演習 — 切り取った範囲", "wait": "類題演習 — 作成中",
              "prac": "類題演習 — 解く", "print": "類題演習 — 印刷", "msets": "モバイル — 類題演習 セット一覧", "mcrop": "モバイル — PDF を切り取る",
              "msetup": "モバイル — 切り取った範囲", "mwait": "モバイル — 作成中", "mprac": "モバイル — 解く"},
)

P_EN = dict(
    p_type="Similar Questions Practice LO", p_type_short="Similar Questions Practice", p_type_en="Similar Questions Practice LO",
    p_lo="Session 7 similar-questions practice (correlation)", p_src_lo="Session 7 lecture slides", p_src_lo_full="Session 7 lecture slides (PDF)",
    p_src_chip="source", p_ai="AI",
    p_dlg_title="Add Learning Objective", p_dlg_name="Session 7 similar-questions practice (correlation)", p_dlg_ext="—",
    p_dlg_desc="Crop questions from the Session 7 lecture slides (PDF) and the AI collects similar questions into a practice set. Add as many sets as you like.",
    p_f_link="Linked source LO", p_link_req="required", p_link_hint="Only LOs in this book with \"Available as practice source\" turned on are offered. An LO already linked by another practice LO stays available.",
    p_link_none="No eligible LOs in this book. Turn on \"Available as practice source\" on a PDF LO first.",
    p_empty_lbl="Empty state",
    p_hidden="Hidden for this type: max score, grade to pass, manual grading, AI Tutor, password. Students see sets, questions done and questions correct — no completion status.",
    p_cant_save="Cannot save: a Similar Questions Practice LO must be linked to an eligible LO when created.",
    p_gate="Syllabus_BackOffice_AIPractice · syllabus.ai_practice.is_enabled",
    p_gate_note="The type is offered only when the feature flag and the tenant setting are both on.",
    p_src_type="Learning Objective (with study-guide PDF)", p_src_pages="24 pages · Published",
    p_tog="Available as practice source", p_tog_desc="Students can build similar-question practice sets from this LO's PDF. Default off.",
    p_tog_locked="Cannot be turned off: students already have practice sets.",
    p_linked_by="Linked by (Similar Questions Practice LOs)", p_linked_none="No practice LO links to this LO yet.",
    p_src_kv=[("Type", "Learning Objective"), ("Study guide", "Session7_lecture_slides.pdf · 24 pages"), ("AI Tutor", "Off"), ("Availability", "__course__")],
    p_det_kv_link="Linked source LO", p_det_sets="Sets created by students", p_det_sets_v="12 sets (5 of 30 students)",
    p_det_comp="Completion status", p_det_comp_v="None by design (PRD C3)", p_det_over="Teacher / admin override", p_det_over_v="None · sets cannot be deleted, altered or regenerated",
    p_det_visible="Visible to students as", p_det_visible_v="A card in topic \"7-1 · Correlation analysis\" with the ✦ badge and the tag \"Similar Questions Practice\". It shows the set count only; there is no completion chip.",
    p_det_dates="Availability", p_det_dates_v="Start date set in Course Management (no end date — an LO without a deadline)", p_det_dash="Open in the dashboard",
    p_det_stock="Prepared similar questions", p_det_stock_v="3 source questions · stock is never shown to students",
    p_dash_col="Similar Questions Practice", p_mx_kv=["Students with sets", "Sets", "Done · correct"], p_mx_none="--",
    p_sets_n="{n} sets", p_done_of="{d}/{t} questions", p_correct_n="{c} correct", p_adhoc_n="{n} informal", p_acc="Accuracy",
    p_tp_line="✦ Session 7 similar-questions practice · students with sets 5/30 · sets 12 · done 40 · correct 31",
    p_stu_sets_line="2 sets (1 completed · 1 in progress)", p_stu_status_prog="In progress", p_stu_status_done="Completed", p_stu_view="View sets",
    p_stu_score="6/8 correct",
    p_lt="Practice", p_course_sub="From the Session 7 lecture slides PDF · 2 sets", p_todo_chip="Set 2 · continue 2/4",
    p_questions="Questions", p_correct="Correct", p_round_line="10 per round · {d}/{t} answered · {w} wrong",
    p_sets_h="Sets", p_set_n="Set {i}", p_done="Done", p_notdone="Not done", p_q_n="{d}/{t} questions", p_correct_q="{c} correct",
    p_print="Print set", p_add_set="Add practice", p_create_set="Create practice set", p_from_pdf="from the Session 7 lecture slides PDF",
    p_history="History", p_hist_row="{r}/{n} correct", p_hist=[("9 Nov, 14:02", 1, 5, 6)],
    p_cta_done_note="Set 1 is completed (no re-practice)", p_cta_print="Print set 1", p_cta_print2="Print set 2",
    p_cta_resume_note="Set 2 · continue (2/4)", p_resume="Continue", p_start="Start practice",
    p_no_status="No completion status and no mastery level. Sets can be added at any time.",
    p_crop_title="Session 7 lecture slides (PDF)", p_crop_mode="Make practice", p_crop_hint="Draw frames around the questions in the PDF (several allowed). Same gesture as the \"Mana AI\" crop on the study-guide screen.",
    p_crop_pages="p.12–14 / 24", p_crop_cta="Make practice →", p_frames_n="{n} selected", p_frames_none="Select at least one frame to enable \"Make practice\"",
    p_pdf_h="7-1 Correlation analysis — exercises", p_pdf_sub="Session 7 lecture slides p.12–14",
    p_setup_title="Cropped range", p_dest="Add to", p_count="Questions", p_per_q=" per question × {k}", p_max_per="up to {m} per question",
    p_total="{n} questions in total", p_cap_hint="The maximum follows the question with the least stock in your selection. Stock totals are never shown.",
    p_create="Create practice", p_question="question", p_one="1",
    p_nomatch_t="Similar questions are not available for this range.", p_nomatch_b="Please ensure your crop contains the question in full and try again.",
    p_nomatch_h="No set is created. There is no generative fallback.", p_recrop="Crop again", p_demo_nomatch="DEMO: no match",
    p_demo_match="DEMO: match",
    p_making="Creating", p_collecting="Collecting similar questions…", p_wait_note="Shown for creation only, never for read-only transitions.",
    p_practice="Similar questions", p_one_attempt="One attempt per question", p_next="Next →", p_end_round="Finish this round",
    p_correct_bang="Correct!", p_correct_is="The correct answer is {ci}", p_round_done="Round complete!", p_round_sum="{r} of {n} correct",
    p_set_done="This set is completed", p_back_sets="Back to sets", p_q_of="{i} / {n}",
    p_sheet_title="Similar questions · Set 1 (6 questions)", p_sheet_chip="Print preview · PDF re-rendered on demand", p_q_label="Q{n}",
    p_sheet_foot="Source question and stock counts are not printed.", p_print_btn="Print", p_close="Close",
    p_titles={"dialog": "BO — Add LO (Similar Questions Practice)", "src": "BO — Source LO settings (Available as practice source)", "det": "BO — Similar Questions Practice LO detail",
              "sets": "Practice — sets", "crop": "Practice — crop the PDF", "setup": "Practice — cropped range", "wait": "Practice — creating",
              "prac": "Practice — solve", "print": "Practice — print", "msets": "Mobile — practice sets", "mcrop": "Mobile — crop the PDF",
              "msetup": "Mobile — cropped range", "mwait": "Mobile — creating", "mprac": "Mobile — solve"},
)
JA.update(P_JA); EN.update(P_EN)

# The bank: three source questions on the Session 7 slides (p.12–14), stock 4 / 3 / 2, so the shallowest-stock
# cap is visible (cropping all three gives max 2). Content in JA and EN; the correct option index is fixed.
P_BANK = [
    {"id": "sq_r", "page": 12, "label": ("問1 相関係数の解釈", "Q1 Interpreting r"), "variants": [
        (("相関係数 r = 0.82 のとき、2変数の関係として最も適切なものはどれか。", "For r = 0.82, which best describes the relationship between the two variables?"),
         (("強い正の相関", "Strong positive correlation"), ("弱い正の相関", "Weak positive correlation"), ("強い負の相関", "Strong negative correlation"), ("相関なし", "No correlation")), 0,
         ("r が 0.7 を超えると一般に強い相関とされ、符号が正なので正の相関。", "r above about 0.7 is generally called strong, and the sign is positive.")),
        (("相関係数 r = −0.15 のとき、最も適切なものはどれか。", "For r = −0.15, which is the best description?"),
         (("強い負の相関", "Strong negative correlation"), ("弱い負の相関", "Weak negative correlation"), ("強い正の相関", "Strong positive correlation"), ("完全な相関", "Perfect correlation")), 1,
         ("絶対値が 0.2 未満なのでほとんど相関がなく、符号が負。", "An absolute value under 0.2 is barely any correlation, and the sign is negative.")),
        (("相関係数 r = −0.91 のとき、最も適切なものはどれか。", "For r = −0.91, which is the best description?"),
         (("弱い負の相関", "Weak negative correlation"), ("相関なし", "No correlation"), ("強い負の相関", "Strong negative correlation"), ("強い正の相関", "Strong positive correlation")), 2,
         ("絶対値が 0.9 を超えるので強い相関、符号が負。", "An absolute value above 0.9 is a strong correlation, and the sign is negative.")),
        (("相関係数 r が取りうる値の範囲はどれか。", "What is the range of values the correlation coefficient r can take?"),
         (("0 以上 1 以下", "0 to 1"), ("−1 以上 1 以下", "−1 to 1"), ("−∞ から ∞", "−∞ to ∞"), ("0 以上 100 以下", "0 to 100")), 1,
         ("相関係数は共分散を両標準偏差の積で割った値で、−1 から 1 の範囲に収まる。", "r is the covariance divided by the product of the two standard deviations, which stays between −1 and 1.")),
    ]},
    {"id": "sq_scatter", "page": 13, "label": ("問2 散布図の読み取り", "Q2 Reading a scatter plot"), "variants": [
        (("散布図で点が右下がりに並ぶとき、相関係数の符号はどれか。", "When the points of a scatter plot run downward to the right, what is the sign of r?"),
         (("正", "Positive"), ("負", "Negative"), ("0", "Zero"), ("決まらない", "Cannot be told")), 1,
         ("一方が増えると他方が減る関係なので負の相関。", "One variable falls as the other rises, so the correlation is negative.")),
        (("散布図で点がほぼ水平に散らばっているとき、相関係数はどれに近いか。", "When the points are scattered almost horizontally, what is r close to?"),
         (("1", "1"), ("−1", "−1"), ("0", "0"), ("0.5", "0.5")), 2,
         ("x が変わっても y の傾向が変わらないので、相関はほとんどない。", "y shows no trend as x changes, so there is almost no correlation.")),
        (("散布図で点がほぼ一直線上に右上がりに並ぶとき、相関係数はどれに近いか。", "When the points lie almost on a straight line rising to the right, what is r close to?"),
         (("0", "0"), ("−1", "−1"), ("0.3", "0.3"), ("1", "1")), 3,
         ("直線に近く右上がりなので、1 に近い強い正の相関。", "Nearly a straight rising line means a strong positive correlation close to 1.")),
    ]},
    {"id": "sq_cause", "page": 14, "label": ("問3 相関と因果", "Q3 Correlation and causation"), "variants": [
        (("アイスクリームの売上と水難事故の件数に正の相関がある。最も適切な解釈はどれか。", "Ice-cream sales and drowning accidents are positively correlated. Which interpretation is best?"),
         (("アイスクリームが事故の原因である", "Ice cream causes the accidents"), ("事故がアイスクリームの売上を増やす", "Accidents increase ice-cream sales"), ("気温など第三の変数の影響の可能性がある", "A third variable such as temperature may drive both"), ("相関があるので因果もある", "Correlation implies causation")), 2,
         ("両方に影響する第三の変数（気温）を疑うのが妥当。相関は因果を意味しない。", "Suspect a third variable (temperature) that affects both. Correlation does not imply causation.")),
        (("相関係数が高いとき、必ず言えることはどれか。", "When r is high, which statement is always true?"),
         (("一方が他方の原因である", "One variable causes the other"), ("2変数は直線的に関連している", "The two variables are linearly related"), ("外れ値はない", "There are no outliers"), ("サンプルサイズが十分である", "The sample size is sufficient")), 1,
         ("高い相関が示すのは直線的な関連の強さだけで、因果・外れ値・標本サイズは別の話。", "A high r shows only the strength of a linear relationship; causation, outliers and sample size are separate questions.")),
    ]},
]
def pl(pair, L):
    return pair[0] if L == "ja" else pair[1]

# Set 1 (completed, 6 questions): Q1 ×4 + Q2 ×2 — 5 correct. Set 2 (in progress, 4 questions): Q2 v3, Q3 v1, Q3 v2, Q1 v1
# — the first two answered (1 correct), the last two open. The student resumes at the third.
P_SET1 = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1)]
P_SET2 = [(1, 2), (2, 0), (2, 1), (0, 0)]
def pq(ref):
    sq, v = ref
    return P_BANK[sq]["variants"][v]

# ---------- Back Office ----------
def p_dialog(S, L):
    """DialogCreateLearningMaterial with the new sub-type chosen (C10.3 'Add learning material'): the type
    select reads 類題演習 LO, General Info as for any LO, and in Settings the required 'Linked source LO'
    picker fed by the book's eligible LOs (one radio option here — the Session 7 slides PDF, marked 演習の元),
    with production's empty-state copy noted, the hidden-fields note and the flag/tenant-setting gate.
    Confirm goes to the new LO's page. Cancel back to the tree."""
    pick = (f'<div class="tpaper" style="padding:0;overflow:hidden;border:1px solid #BDBDBD;box-shadow:none">'
            f'<button class="check on" style="width:100%;padding:12px 14px;gap:12px" onClick="{{{{noop}}}}"><span class="cbx" style="border-radius:50%">{mi("check", 14, "#fff")}</span>'
            f'<span class="lm-type">{mi("lo", 16)}</span><span style="flex:1 1 auto;text-align:left">{S["p_src_lo"]}</span>'
            f'<span class="tchip type">{S["p_src_chip"]}</span><span class="cell-muted" style="font-size:12px">p.1–24</span></button></div>'
            f'<span class="helper">{S["p_link_hint"]}</span>')
    dialog = f'''<div class="tscrim">
  <div class="dlg">
    <div class="dlg-head"><h2>{S["p_dlg_title"]}</h2><a class="ticon" href="{tfn("T-Book", L)}" aria-label="{S["t_cancel"]}">{mi("close", 24)}</a></div>
    <div class="dlg-body">
      <div class="lm-section">
        <h3 class="sec-head">{S["t_dlg_general"]}</h3>
        <div class="lm-grid">
          <label class="field"><span class="lbl">{S["t_dlg_select"]} <span class="req">*</span></span><span class="in" style="gap:8px"><span class="lm-type" style="width:22px;height:22px">{mi("spark", 14)}</span>{S["p_type"]}<span class="tchip new">{S["t_new"]}</span><span class="gr">{mi("expandMore", 22)}</span></span></label>
          {field(S["t_f_name"], S["p_dlg_name"], required=True)}
          <div class="span2">{field(S["t_f_desc"], S["p_dlg_desc"], area=True)}</div>
          {field(S["t_f_ext"], S["t_ph_ext"], placeholder=True)}
        </div>
        <span class="helper" style="display:flex;gap:6px;align-items:center;margin-top:10px">{mi("lock", 14, "#9E9E9E")}<span class="num">{S["p_gate"]}</span> ・ {S["p_gate_note"]}</span>
      </div>
      <div class="lm-section">
        <h3 class="sec-head">{S["t_dlg_settings"]}</h3>
        <div class="settings-list">
          <div class="setting">
            <span class="setting-label" style="font-weight:500">{S["p_f_link"]} <span class="req" style="color:#F44336">*</span> <span class="cell-muted" style="font-weight:400;font-size:12px">{S["p_link_req"]}</span></span>
            {pick}
            <span class="helper" style="color:#9E9E9E;display:flex;gap:6px;align-items:flex-start"><span style="flex:0 0 auto;margin-top:2px">{mi("info", 14, "#9E9E9E")}</span><span><b style="color:#757575">{S["p_empty_lbl"]}:</b> {S["p_link_none"]}</span></span>
          </div>
          <div class="setting"><div class="alert info">{mi("info", 20, "#2196F3")}<span>{S["p_hidden"]}</span></div></div>
        </div>
      </div>
    </div>
    <div class="dlg-foot"><a class="tbtn" href="{tfn("T-Book", L)}">{S["t_cancel"]}</a><a class="tbtn contained" href="{tfn("P-Detail", L)}">{S["t_confirm"]}</a></div>
  </div>
</div>'''
    return tpage(S, "P-Dialog", S["p_titles"]["dialog"], book_page(S, L, "P-Dialog", extra=dialog), logic='state = {}; renderVals(){ return { noop: () => {} }; }')

def p_head(S, L, screen, name, type_chip, crumbs, acts=""):
    return f'''{tcrumbs(S, screen, crumbs)}
  <div class="tphead">
    <h1>{name}{type_chip}<span class="tchip published">{S["t_pub"]}</span></h1>
    <div class="acts">{acts}<span class="ticon">{mi("more", 24)}</span></div>
  </div>
  <div class="tabs"><span class="tab">{S["t_lo_tabs"][0]}</span><span class="tab on">{S["t_lo_tabs"][1]}</span></div>'''

P_SRC_LOGIC = """state = { on: true };
  renderVals() { return { tg: this.state.on ? "on" : "", tgOn: this.state.on, toggle: () => {} }; }"""

def p_source(S, L):
    """The source LO's Settings tab (C10.3 'LO detail / edit — source LO'): production's read-only settings
    for a Learning Objective with a study-guide PDF, plus the eligibility switch 'Available as practice source'
    — on, and locked with the reason because students already have sets — and 'Linked by', listing the
    practice LO that points here. Shown only for supported types (v1: a PDF LO), default off."""
    kv = ""
    for k, v in S["p_src_kv"]:
        if v == "__course__":
            v = f'{S["t_course_name"]} ・ 2026/11/06 09:00 – ・ <a href="{tfn("T-CourseBook", L)}">{S["t_edit_dates"]}</a>'
        kv += f'<dt>{k}</dt><dd>{v}</dd>'
    body = tnav(S) + f'''<div class="tmain">
<div class="tscroll">
  {p_head(S, L, "P-Source", S["p_src_lo"], f'<span class="tchip type">{mi("lo", 14)}{S["p_src_type"]}</span>',
          [(S["t_bm"], tfn("T-Book", L)), (S["t_book"], tfn("T-Book", L)), (S["p_src_lo"], None)],
          f'<a class="tbtn outlined" href="#">{mi("edit", 18)}{S["t_edit"]}</a>')}
  <div style="display:flex;flex-direction:column;gap:16px">
    <div class="tpaper"><div class="ph"><h3>{S["t_dlg_settings"]}</h3></div><div class="pb"><dl class="tkv" style="max-width:none">{kv}</dl></div></div>
    <div class="tpaper">
      <div class="ph"><h3>{S["p_type_short"]}</h3></div>
      <div class="pb" style="display:flex;flex-direction:column;gap:14px">
        <div style="display:flex;align-items:flex-start;gap:16px">
          <span class="switch on" style="opacity:.55;cursor:default"><span class="track"></span><span style="font-weight:500">{S["p_tog"]}</span></span>
        </div>
        <span class="helper" style="margin:-6px 0 0 62px">{S["p_tog_desc"]}</span>
        <div class="alert warn" style="margin-left:62px">{mi("lock", 20, "#ED6C02")}<span>{S["p_tog_locked"]}</span></div>
        <div class="divider" style="height:1px;background:#E0E0E0"></div>
        <span class="setting-label" style="font-weight:500">{S["p_linked_by"]}</span>
        <ul class="lm-list" style="padding:0"><li class="lm" style="padding-left:0"><span class="lm-type">{mi("spark", 16)}</span><a class="nm" href="{tfn("P-Detail", L)}">{S["p_lo"]}</a><span class="tchip type">{S["p_type_short"]}</span><span class="cell-muted" style="font-size:12px">{S["p_det_sets_v"]}</span></li></ul>
      </div>
    </div>
  </div>
</div>
</div>'''
    return tpage(S, "P-Source", S["p_titles"]["src"], body, logic=P_SRC_LOGIC)

def p_detail(S, L):
    """The practice LO's own page (C10.3 'Practice LO detail'): Settings shows only the linked source LO
    (a link to its settings) — PM, 24 Sep — plus how it looks to students and a way into the dashboard.
    The set count, the start date (Course Management, no end date), completion status none by design and
    no teacher/admin override are recorded in the board's note, not on the page."""
    # Settings shows only the linked source LO (PM comment on P3, 24 Sep: "Show only linked source LO").
    # The stock, set count, dates, completion-status and override statements moved to the board's note.
    rows = [
        (S["p_det_kv_link"], f'<a href="{tfn("P-Source", L)}" style="display:inline-flex;align-items:center;gap:6px"><span class="lm-type" style="width:20px;height:20px">{mi("lo", 12)}</span>{S["p_src_lo_full"]}</a> <span class="tchip type">{S["p_src_chip"]}</span>'),
    ]
    kv = "".join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in rows)
    body = tnav(S) + f'''<div class="tmain">
<div class="tscroll">
  {p_head(S, L, "P-Detail", S["p_lo"], f'<span class="tchip type">{mi("spark", 14)}{S["p_type"]}</span>',
          [(S["t_bm"], tfn("T-Book", L)), (S["t_book"], tfn("T-Book", L)), (S["p_lo"], None)],
          f'<a class="tbtn" href="{tfn("T-DashGroup", L)}">{mi("dashboard", 18)}{S["p_det_dash"]}</a><a class="tbtn outlined" href="{tfn("P-Dialog", L)}">{mi("edit", 18)}{S["t_edit"]}</a>')}
  <div style="display:flex;flex-direction:column;gap:16px">
    <div class="tpaper"><div class="ph"><h3>{S["t_dlg_settings"]}</h3></div><div class="pb"><dl class="tkv" style="max-width:none">{kv}</dl></div></div>
    <div class="tpaper"><div class="ph"><h3>{S["p_det_visible"]}</h3></div><div class="pb"><div class="alert info">{mi("spark", 20, "#2196F3")}<span>{S["p_det_visible_v"]}</span></div></div></div>
  </div>
</div>
<sc-if value="{{{{created}}}}" hint-placeholder-val="{{{{true}}}}"><div class="snack" role="status">{mi("checkCircle", 20)}{S["t_snack"]}</div></sc-if>
</div>'''
    return tpage(S, "P-Detail", S["p_titles"]["det"], body, logic='state = { created: true }; renderVals(){ return { created: this.state.created }; }')

# ---------- student, shared pieces ----------
def p_ring(d, t, size=44):
    deg = int(d / t * 360) if t else 0
    inner = size - 10
    return (f'<span style="width:{size}px;height:{size}px;border-radius:50%;flex:0 0 {size}px;display:flex;align-items:center;justify-content:center;'
            f'background:conic-gradient(#395ad2 {deg}deg, rgba(28,30,44,.12) 0)"><span style="width:{inner}px;height:{inner}px;border-radius:50%;background:#fff;display:flex;align-items:center;justify-content:center;font-size:11px;font-weight:700">{d}/{t}</span></span>')

def p_stat(S, done, total, correct, wide=False):
    pct = int(done / total * 100) if total else 0
    return f'''<div class="{"card" if wide else "mcard"}" style="{"padding:20px 24px" if wide else ""}">
    <div style="display:flex">
      <div style="flex:1;text-align:center"><b style="display:block;font-size:28px;line-height:36px;color:#395ad2">{done}<span style="font-size:14px;color:rgba(28,30,44,.45)">/{total}</span></b><span class="cap">{S["p_questions"]}</span></div>
      <div style="flex:1;text-align:center;border-left:1px solid rgba(28,30,44,.12)"><b style="display:block;font-size:28px;line-height:36px;color:#395ad2">{correct}</b><span class="cap">{S["p_correct"]}</span></div>
    </div>
    <div style="height:8px;border-radius:999px;background:rgba(28,30,44,.12);overflow:hidden;margin-top:12px"><i style="display:block;height:100%;width:{pct}%;background:#395ad2;border-radius:999px"></i></div>
    <p class="cap" style="text-align:center;margin-top:8px">{S["p_round_line"].format(d=done, t=total, w=done - correct)}</p>
  </div>'''

P_SETS_LOGIC = """state = { sel: 2 };
  renderVals() {
    const s = this.state.sel;
    return { sel1: s === 1 ? "on" : "", sel2: s === 2 ? "on" : "", is1: s === 1, is2: s === 2,
             pick1: () => this.setState({ sel: 1 }), pick2: () => this.setState({ sel: 2 }) };
  }"""

def p_set_rows(S, L, mobile=False):
    """Two set rows (Koki's prototype: tapping a row selects it and the bottom CTA follows; default = the
    topmost unfinished set), the dashed ＋ row, and the history. Set 1 is completed; Set 2 is 2/4. Every set is printable."""
    row_cls = "lo" if not mobile else "lo"
    def row(i, d, t, c, done, sel_hole, pick_hole):
        chip = (f'<span class="chip done">{S["p_done"]}</span>' if done else f'<span class="chip pre">{S["p_notdone"]}</span>')
        extra = f'<span>{S["p_q_n"].format(d=d, t=t)}</span>' + (f'<span>{S["p_correct_q"].format(c=c)}</span>' if done else "")
        # print is available for every generated set, finished or not (PM, 24 Sep): the sheet is question + options only
        pr = (f'<a class="btn ghost" style="height:36px" href="{fn("P-Print", L)}" aria-label="{S["p_print"]}" title="{S["p_print"]}">{ic("download", 18)}</a>' if not mobile
              else f'<span class="btn ghost" style="height:36px;padding:0 8px" aria-label="{S["p_print"]}">{ic("download", 18)}</span>')
        return (f'<button class="{row_cls} {{{{{sel_hole}}}}}" style="border:2px solid transparent" onClick="{{{{{pick_hole}}}}}">{p_ring(d, t)}'
                f'<span class="t"><b>{S["p_set_n"].format(i=i)}</b><i>{chip}{extra}</i></span>{pr}</button>')
    rows = row(1, 6, 6, 5, True, "sel1", "pick1") + row(2, 2, 4, 1, False, "sel2", "pick2")
    add = (f'<a class="{row_cls}" style="box-shadow:none;border:2px dashed rgba(28,30,44,.2);background:transparent" href="{fn("P-Crop" if not mobile else "M-PCrop", L)}">'
           f'<span class="tile" style="background:#fff;box-shadow:0 2px 6px rgba(0,0,0,.08)">{ic("plus", 26)}</span><span class="t"><b>{S["p_add_set"]}</b><i><span>{S["p_from_pdf"]}</span></i></span>{ic("right", 20, "#c7c7cc", 2.4)}</a>')
    hist = "".join(f'<div style="display:flex;justify-content:space-between;align-items:center;padding:10px 4px;border-top:1px solid rgba(28,30,44,.08)"><span class="b2 muted">{when} <b style="color:rgba(28,30,44,.87)">{S["p_set_n"].format(i=i)}</b></span><b class="b2">{S["p_hist_row"].format(r=r, n=n)}</b></div>'
                   for when, i, r, n in S["p_hist"])
    return rows, add, hist

def p_cta(S, L, mobile=False):
    """The bottom CTA that follows the selected set: Set 1 (completed) → print; Set 2 → continue at 2/4, with print beside it
    (print is available at any point for a generated set — PM, 24 Sep)."""
    go_prac = fn("M-PPractice" if mobile else "P-Practice", L)
    go_print = fn("P-Print", L)
    btn = "mbtn primary" if mobile else "btn primary"
    return (f'<sc-if value="{{{{is1}}}}" hint-placeholder-val="{{{{false}}}}"><div style="display:flex;flex-direction:column;gap:8px;align-items:stretch"><p class="cap" style="text-align:center">{S["p_cta_done_note"]}</p>'
            f'<a class="{btn}" href="{go_print}">{ic("download", 18)}{S["p_cta_print"]}</a></div></sc-if>'
            f'<sc-if value="{{{{is2}}}}" hint-placeholder-val="{{{{true}}}}"><div style="display:flex;flex-direction:column;gap:8px;align-items:stretch"><p class="cap" style="text-align:center">{S["p_cta_resume_note"]}</p>'
            f'<a class="{btn}" href="{go_prac}">{ic("play", 18)}{S["p_resume"]}</a>'
            + (f'<span class="mbtn neutral">{ic("download", 18)}{S["p_cta_print2"]}</span>' if mobile else f'<a class="btn ghost" href="{go_print}">{ic("download", 18)}{S["p_cta_print2"]}</a>')
            + '</div></sc-if>')

# ---------- student, PC ----------
def p_sets(S, L):
    """The practice LO screen on the web (C10.4 screen 2): stat box (問題数 done/total, 正解数, bar, the
    round line), the set list — selecting a row swaps the CTA — the ＋ row, the history, no completion chip
    on the LO, no crown, no delete."""
    rows, add, hist = p_set_rows(S, L)
    body = header(S, "P-Sets", S["p_lo"], crumb=f'{S["course"]} › {S["wk7"]} › {S["t71"]}', back_href=fn("Main", L),
                  right_extra=f'<span class="chip lt fb" style="height:26px">{ic("sparkle", 12)}{S["p_type_short"]}</span>') + f'''
<div class="body"><div class="col" style="width:760px">
  {p_stat(S, 8, 10, 6, wide=True)}
  {sect(S["p_sets_h"], f'<span class="cap">{S["p_no_status"]}</span>')}
  {rows}
  {add}
  {sect(S["p_history"])}
  <div class="card" style="padding:6px 16px">{hist}</div>
  <div class="card" style="padding:16px 24px">{p_cta(S, L)}</div>
  <div style="height:8px"></div>
</div></div>'''
    return page(S, S["p_titles"]["sets"], body, logic=P_SETS_LOGIC)

P_CROP_LOGIC = """state = { f: [false, false, false] };
  renderVals() {
    const f = this.state.f, n = f.filter(Boolean).length;
    const tog = (i) => () => { const g = f.slice(); g[i] = !g[i]; this.setState({ f: g }); };
    const no = (i) => f[i] ? String(f.slice(0, i + 1).filter(Boolean).length) : "";
    return { f0: f[0] ? "on" : "", f1: f[1] ? "on" : "", f2: f[2] ? "on" : "", n0: no(0), n1: no(1), n2: no(2),
             t0: tog(0), t1: tog(1), t2: tog(2), any: n > 0, none: n === 0, n: String(n) };
  }"""

def p_pdf_page(S, L, mobile=False):
    """The Session 7 slides as a PDF page: three exercise boxes (p.12–14) that toggle a numbered blue frame
    when clicked — the 'Mana AI' crop gesture in practice mode."""
    boxes = ""
    for i, sq in enumerate(P_BANK):
        v = sq["variants"][0]
        boxes += (f'<button class="pq {{{{f{i}}}}}" onClick="{{{{t{i}}}}}"><span class="pno">{{{{n{i}}}}}</span>'
                  f'<span style="display:flex;justify-content:space-between;gap:8px;align-items:baseline"><b>{pl(sq["label"], L)}</b><span class="cap">p.{sq["page"]}</span></span>'
                  f'<span class="b2" style="line-height:20px">{pl(v[0], L)}</span></button>')
    return f'''<div class="ppdf{" m" if mobile else ""}">
    <div style="display:flex;justify-content:space-between;align-items:baseline"><b style="font-size:{13 if mobile else 15}px">{S["p_pdf_h"]}</b><span class="cap">{S["p_pdf_sub"]}</span></div>
    <div style="height:6px;border-radius:3px;background:#e9e9ec;width:60%"></div><div style="height:6px;border-radius:3px;background:#e9e9ec;width:85%"></div>
    {boxes}
  </div>'''

P_CSS = """
.ppdf{background:#fff;border:1px solid rgba(28,30,44,.12);border-radius:6px;padding:20px 24px;display:flex;flex-direction:column;gap:12px;box-shadow:0 8px 16px rgba(0,0,0,.08)}
.ppdf.m{padding:14px;gap:10px}
.pq{position:relative;display:flex;flex-direction:column;gap:6px;text-align:left;border:2px dashed rgba(28,30,44,.18);border-radius:6px;padding:10px 12px 10px 14px;background:#fff;font-family:inherit;color:inherit;cursor:pointer}
.pq:hover{border-color:rgba(57,90,210,.5)}
.pq.on{border:2px solid #395ad2;box-shadow:0 0 0 3px rgba(57,90,210,.18);background:#f7f8ff}
.pq .pno{position:absolute;left:-10px;top:-10px;width:22px;height:22px;border-radius:50%;background:#395ad2;color:#fff;font-size:12px;font-weight:700;display:none;align-items:center;justify-content:center}
.pq.on .pno{display:flex}
.popt{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:1.5px solid rgba(28,30,44,.16);border-radius:10px;padding:12px 14px;background:#fff;font-family:inherit;color:inherit;font-size:15px;line-height:22px;cursor:pointer}
.popt:hover{background:#fafafc}
.popt .mk{width:22px;height:22px;border-radius:50%;border:2px solid rgba(28,30,44,.24);flex:0 0 22px;display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;color:#fff}
.popt.ok{border-color:#1f7a4d;background:#e6f5ee}.popt.ok .mk{background:#1f7a4d;border-color:#1f7a4d}
.popt.ng{border-color:#d13842;background:#fbe7e9}.popt.ng .mk{background:#d13842;border-color:#d13842}
.popt.dis{cursor:default}
.pfb{border-radius:10px;padding:12px 14px;font-size:14px;line-height:22px}
.pfb.ok{background:#e6f5ee;color:#1f7a4d}.pfb.ng{background:#fbe7e9;color:#8a1f2a}
.pfb b{display:block;margin-bottom:2px}
.prange{width:100%;accent-color:#395ad2;height:32px}
.pspin{width:44px;height:44px;border-radius:50%;border:4px solid rgba(57,90,210,.2);border-top-color:#395ad2;animation:pspin 1s linear infinite}
@keyframes pspin{to{transform:rotate(360deg)}}
.psq{padding:12px 0;border-top:1px solid rgba(28,30,44,.1);font-size:14px;line-height:22px}
.psq b{display:inline-block;width:40px}
.psq ol{margin:6px 0 0 40px;padding-left:18px}
"""

def p_crop(S, L):
    """The PDF crop in practice mode (C10.4 screen 3): the linked LO's study guide with the existing
    'Mana AI' frames — up to five, spanning pages — and the confirm pill relabelled 演習をつくる →, enabled
    once one frame is drawn. Click the exercises to frame them."""
    body = header(S, "P-Crop", S["p_crop_title"], crumb=f'{S["course"]} › {S["t71"]} › {S["p_lo"]}', back_href=fn("P-Sets", L),
                  right_extra=f'<span class="chip review" style="height:28px">{ic("scan", 14)}{S["p_crop_mode"]}</span>') + f'''
<div class="body"><div style="width:1080px;margin:0 auto;display:grid;grid-template-columns:1fr 320px;gap:24px;align-items:start">
  <div style="display:flex;flex-direction:column;gap:12px">
    <div style="display:flex;justify-content:space-between;align-items:center"><span class="cap" style="white-space:nowrap;flex:0 0 auto">{S["p_crop_pages"]}</span><span class="cap" style="text-align:right">{S["p_crop_hint"]}</span></div>
    {p_pdf_page(S, L)}
  </div>
  <div style="display:flex;flex-direction:column;gap:16px;position:sticky;top:0">
    <div class="card" style="display:flex;flex-direction:column;gap:12px">
      <p class="sub1">{S["p_setup_title"]}</p>
      <sc-if value="{{{{any}}}}" hint-placeholder-val="{{{{true}}}}"><p class="b2">{S["p_frames_n"].replace("{n}", "{{n}}")}</p></sc-if>
      <sc-if value="{{{{none}}}}" hint-placeholder-val="{{{{false}}}}"><p class="b2 muted">{S["p_frames_none"]}</p></sc-if>
      <p class="cap">{S["p_dest"]}: <b>{S["p_lo"]}</b></p>
      <sc-if value="{{{{any}}}}" hint-placeholder-val="{{{{true}}}}"><a class="btn primary" href="{fn("P-Setup", L)}">{ic("sparkle", 16)}{S["p_crop_cta"]}</a></sc-if>
      <sc-if value="{{{{none}}}}" hint-placeholder-val="{{{{false}}}}"><span class="btn dis">{ic("sparkle", 16)}{S["p_crop_cta"]}</span></sc-if>
    </div>
  </div>
</div></div>'''
    return page(S, S["p_titles"]["crop"], body, logic=P_CROP_LOGIC)

P_SETUP_LOGIC = """state = { count: 2, nomatch: false };
  renderVals() {
    const c = this.state.count, k = 3;
    return { count: String(c), total: String(c * k), onCount: (e) => this.setState({ count: +e.target.value || 1 }),
             match: !this.state.nomatch, nomatch: this.state.nomatch, toggleDemo: () => this.setState({ nomatch: !this.state.nomatch }) };
  }"""

def p_setup_rows(S, L):
    return "".join(f'<div style="display:flex;align-items:center;gap:12px;padding:10px 0;border-bottom:1px solid rgba(28,30,44,.08)"><span class="ctag">p.{sq["page"]}</span><span class="b2" style="flex:1 1 auto;font-weight:700">{pl(sq["label"], L)}</span><span class="chip neutral" style="height:22px">{S["p_question"]}</span></div>'
                   for sq in P_BANK)

def p_slider(S, L, mobile=False):
    k = 3
    return f'''<div style="display:flex;justify-content:space-between;align-items:baseline"><b style="font-size:{22 if mobile else 26}px;color:#395ad2">{{{{count}}}}<span style="font-size:14px;color:rgba(28,30,44,.6);font-weight:500">{S["p_per_q"].format(k=k)}</span></b><span class="cap">{S["p_max_per"].format(m=2)}</span></div>
    <input class="prange" type="range" min="1" max="2" step="1" value="{{{{count}}}}" onInput="{{{{onCount}}}}" aria-label="{S["p_count"]}">
    <div style="display:flex;justify-content:space-between"><span class="cap">{S["p_one"]}</span><span class="cap">2</span></div>
    <p class="sub1" style="text-align:center;color:#395ad2">{S["p_total"].replace("{n}", "{{total}}")}</p>
    <p class="cap">{S["p_cap_hint"]}</p>'''

def p_nomatch(S, L, mobile=False):
    return f'''<div class="{"mcard" if mobile else "card"}" style="border-left:4px solid #d13842">
      <p class="sub1" style="color:#d13842">{S["p_nomatch_t"]}</p>
      <p class="b2" style="line-height:20px">{S["p_nomatch_b"]}</p>
      <p class="cap">{S["p_nomatch_h"]}</p>
    </div>'''

def p_setup(S, L):
    """切り取った範囲 (C10.4 screen 4): after Next the frames are uploaded and matched — one row per detected
    question with its page, the read-only 追加先 line, and a per-question slider 1..max where max is the
    shallowest remaining stock in the crop (2 here), with the live total. The DEMO pill flips to NO_MATCH:
    the committed copy, もう一度 切り取る, nothing created."""
    body = header(S, "P-Setup", S["p_setup_title"], crumb=f'{S["course"]} › {S["t71"]} › {S["p_lo"]}', back_href=fn("P-Crop", L),
                  right_extra=f'<button class="chip pick" onClick="{{{{toggleDemo}}}}"><sc-if value="{{{{match}}}}" hint-placeholder-val="{{{{true}}}}">{S["p_demo_nomatch"]}</sc-if><sc-if value="{{{{nomatch}}}}" hint-placeholder-val="{{{{false}}}}">{S["p_demo_match"]}</sc-if></button>') + f'''
<div class="body"><div class="col" style="width:760px">
  <sc-if value="{{{{match}}}}" hint-placeholder-val="{{{{true}}}}">
  <div class="card" style="padding:8px 24px">{p_setup_rows(S, L)}
    <div style="display:flex;align-items:center;gap:12px;padding:12px 0"><span class="cap">{S["p_dest"]}</span><span class="b2" style="font-weight:700">{S["p_lo"]}</span></div></div>
  {sect(S["p_count"])}
  <div class="card" style="padding:20px 24px;display:flex;flex-direction:column;gap:10px">{p_slider(S, L)}</div>
  <div class="card" style="padding:16px 24px;display:flex;justify-content:flex-end"><a class="btn primary" href="{fn("P-Wait", L)}">{ic("sparkle", 16)}{S["p_create"]}</a></div>
  </sc-if>
  <sc-if value="{{{{nomatch}}}}" hint-placeholder-val="{{{{false}}}}">
  {p_nomatch(S, L)}
  <div class="card" style="padding:16px 24px;display:flex;justify-content:flex-end"><a class="btn primary" href="{fn("P-Crop", L)}">{ic("scan", 16)}{S["p_recrop"]}</a></div>
  </sc-if>
</div></div>'''
    return page(S, S["p_titles"]["setup"], body, logic=P_SETUP_LOGIC)

def p_wait(S, L):
    """The wait state (C10.4 screen 5), for creation only: spinner and 類題を集めています… — retrieval, not
    generation. DEMO → the set list with the new set."""
    body = header(S, "P-Wait", S["p_making"], back_href=fn("P-Setup", L)) + f'''
<div class="body" style="display:flex;align-items:center;justify-content:center">
  <div class="card" style="width:420px;padding:40px 32px;display:flex;flex-direction:column;align-items:center;gap:16px;text-align:center">
    <span class="pspin"></span>
    <p class="sub1">{S["p_collecting"]}</p>
    <p class="cap">{S["p_wait_note"]}</p>
  </div>
</div>
<a class="demo" href="{fn("P-Sets", L)}"><span class="tag">DEMO</span>{S["p_sets_h"]} {ic("right", 16, "#fff", 2.4)}</a>'''
    return page(S, S["p_titles"]["wait"], body)

def p_practice_logic(L):
    """Set 2 resumes at its third question. Two open questions (Q3 v1, Q1 v1) are drawn as sc-if blocks; the
    option classes and the feedback box are holes. Correct so far: 1 of 2 answered."""
    qs = [pq(P_SET2[2]), pq(P_SET2[3])]
    corr = [q[2] for q in qs]
    return f"""state = {{ i: 0, sel: [-1, -1], right: 1, end: false }};
  renderVals() {{
    const corr = {corr}; const i = this.state.i, sel = this.state.sel;
    const v = {{ q0: i === 0 && !this.state.end, q1: i === 1 && !this.state.end, end: this.state.end,
                 idx: String(i + 3), right: String(this.state.right), lastQ: i === 1 }};
    for (let q = 0; q < 2; q++) {{
      const a = sel[q] >= 0;
      v["a" + q] = a; v["u" + q] = !a;
      v["ok" + q] = a && sel[q] === corr[q]; v["ng" + q] = a && sel[q] !== corr[q];
      for (let o = 0; o < 4; o++) {{
        v["c" + q + o] = !a ? "" : (o === corr[q] ? "ok" : (o === sel[q] ? "ng" : "dis"));
        v["m" + q + o] = !a ? "" : (o === corr[q] ? "✓" : (o === sel[q] ? "✗" : ""));
        v["p" + q + o] = () => {{ if (sel[q] >= 0) return; const s = sel.slice(); s[q] = o; this.setState({{ sel: s, right: this.state.right + (o === corr[q] ? 1 : 0) }}); }};
      }}
    }}
    v.next = () => this.setState({{ i: 1 }}); v.finish = () => this.setState({{ end: true }});
    return v;
  }}"""

def p_question_block(S, L, q, n, total, qi, mobile=False):
    """One question card: text, four options (letters A–D, marks and tones from holes), the feedback box."""
    text, opts, corr, expl = q
    letters = "ABCD"
    options = "".join(f'<button class="popt {{{{c{qi}{o}}}}}" onClick="{{{{p{qi}{o}}}}}"><span class="mk">{{{{m{qi}{o}}}}}</span><span>{letters[o]}. {pl(opt, L)}</span></button>' for o, opt in enumerate(opts))
    ci = letters[corr]
    fb = (f'<sc-if value="{{{{ok{qi}}}}}" hint-placeholder-val="{{{{false}}}}"><div class="pfb ok"><b>{S["p_correct_bang"]}</b>{pl(expl, L)}</div></sc-if>'
          f'<sc-if value="{{{{ng{qi}}}}}" hint-placeholder-val="{{{{false}}}}"><div class="pfb ng"><b>{S["p_correct_is"].format(ci=ci)}. {pl(opts[corr], L)}</b>{pl(expl, L)}</div></sc-if>')
    return f'''<div class="{"mcard" if mobile else "card"}" style="display:flex;flex-direction:column;gap:12px;{"" if mobile else "padding:24px"}">
      <span class="cap">{n} / {total}</span>
      <p class="{"b1" if not mobile else "b2"}" style="font-weight:700;line-height:{26 if not mobile else 22}px">{pl(text, L)}</p>
      <div style="display:flex;flex-direction:column;gap:8px">{options}</div>
      {fb}
    </div>'''

def p_footer(S, L, qi, mobile=False, back=None):
    btn = "mbtn primary" if mobile else "btn primary"
    nxt = (f'<button class="{btn}" onClick="{{{{next}}}}">{S["p_next"]}</button>' if qi == 0 else f'<button class="{btn}" onClick="{{{{finish}}}}">{S["p_end_round"]}</button>')
    return (f'<sc-if value="{{{{u{qi}}}}}" hint-placeholder-val="{{{{true}}}}"><p class="cap" style="text-align:center">{S["p_one_attempt"]}</p></sc-if>'
            f'<sc-if value="{{{{a{qi}}}}}" hint-placeholder-val="{{{{false}}}}">{nxt}</sc-if>')

def p_end_block(S, L, mobile=False):
    back = fn("M-PSets" if mobile else "P-Sets", L)
    btn = "mbtn primary" if mobile else "btn primary"
    return f'''<div class="{"mcard" if mobile else "card"}" style="align-items:center;text-align:center;gap:10px;padding:32px 24px;display:flex;flex-direction:column">
      <b style="font-size:40px;line-height:48px;color:#395ad2">{{{{right}}}}/4</b>
      <p class="sub1">{S["p_round_done"]}</p>
      <p class="b2">{S["p_round_sum"].replace("{n}", "4").replace("{r}", "{{right}}")}</p>
      <p class="cap">{S["p_set_done"]}</p>
      <a class="{btn}" style="margin-top:8px" href="{back}">{S["p_back_sets"]}</a>
    </div>'''

def p_practice(S, L):
    """Practice (C10.4 screen 6) — the reused web MCQ module in a webview: one attempt per question, the
    correct option marked and the wrong one crossed, the explanation under the options, 次へ →, then
    この回を終える → the round-end screen with the set completed. Resumes at question 3 of 4."""
    qs = [pq(P_SET2[2]), pq(P_SET2[3])]
    body = header(S, "P-Practice", S["p_practice"], crumb=f'{S["p_lo"]} › {S["p_set_n"].format(i=2)}', back_href=fn("P-Sets", L),
                  right_extra=f'<span class="chip neutral" style="height:28px">{S["p_q_of"].replace("{i}", "{{idx}}").replace("{n}", "4")}</span>') + f'''
<div class="body"><div class="col" style="width:720px">
  <sc-if value="{{{{q0}}}}" hint-placeholder-val="{{{{true}}}}">{p_question_block(S, L, qs[0], 3, 4, 0)}<div class="card" style="padding:16px 24px;display:flex;justify-content:flex-end">{p_footer(S, L, 0)}</div></sc-if>
  <sc-if value="{{{{q1}}}}" hint-placeholder-val="{{{{false}}}}">{p_question_block(S, L, qs[1], 4, 4, 1)}<div class="card" style="padding:16px 24px;display:flex;justify-content:flex-end">{p_footer(S, L, 1)}</div></sc-if>
  <sc-if value="{{{{end}}}}" hint-placeholder-val="{{{{false}}}}">{p_end_block(S, L)}</sc-if>
</div></div>'''
    return page(S, S["p_titles"]["prac"], body, logic=p_practice_logic(L))

def p_print(S, L):
    """Print (C10.4 screen 7): the whole set as a sheet — questions and options only; the source question
    and stock counts never printed; re-rendered on demand, nothing stored."""
    items = ""
    for n, ref in enumerate(P_SET1):
        text, opts, corr, expl = pq(ref)
        items += f'<div class="psq"><b>{S["p_q_label"].format(n=n + 1)}</b>{pl(text, L)}<ol type="A">{"".join(f"<li>{pl(o, L)}</li>" for o in opts)}</ol></div>'
    body = header(S, "P-Print", S["p_sheet_title"], crumb=f'{S["p_lo"]} › {S["p_set_n"].format(i=1)}', back_href=fn("P-Sets", L),
                  right_extra=f'<span class="chip review" style="height:28px">{S["p_sheet_chip"]}</span>') + f'''
<div class="body"><div class="col" style="width:760px">
  <div class="card" style="padding:32px 40px;display:flex;flex-direction:column">
    <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:8px"><b class="h4" style="font-size:20px">{S["p_sheet_title"]}</b><span class="cap">{S["course"]} ・ {S["t71"]}</span></div>
    {items}
    <p class="cap" style="margin-top:16px">{S["p_sheet_foot"]}</p>
  </div>
  <div class="card" style="padding:16px 24px;display:flex;justify-content:flex-end;gap:12px"><a class="btn neutral" href="{fn("P-Sets", L)}">{S["p_close"]}</a><span class="btn primary">{ic("download", 18)}{S["p_print_btn"]}</span></div>
</div></div>'''
    return page(S, S["p_titles"]["print"], body)

# ---------- student, mobile ----------
def m_psets(S, L):
    rows, add, hist = p_set_rows(S, L, mobile=True)
    body = mheader(S, "M-PSets", S["p_lo"], back_href=fn("M-Main", L)) + f'''
<div class="mbody" style="padding-bottom:140px">
  <p class="cap" style="margin:-4px 0 -8px;display:flex;gap:6px;align-items:center">{ic("sparkle", 12)}{S["p_type_short"]} ・ {S["t71"]}</p>
  {p_stat(S, 8, 10, 6)}
  <p class="cap" style="margin:-4px 0 -8px;font-weight:700">{S["p_sets_h"]}</p>
  {rows}
  {add}
  <p class="cap" style="margin:-4px 0 -8px;font-weight:700">{S["p_history"]}</p>
  <div class="mcard" style="padding:2px 12px">{hist}</div>
</div>
<div style="position:absolute;left:0;right:0;bottom:0;background:#fff;border-top:1px solid rgba(28,30,44,.12);padding:12px 16px 24px;z-index:20">{p_cta(S, L, mobile=True)}</div>'''
    return mpage(S, "M-PSets", S["p_titles"]["msets"], body, logic=P_SETS_LOGIC)

def m_pcrop(S, L):
    body = mheader(S, "M-PCrop", S["p_crop_title"], back_href=fn("M-PSets", L), right=f'<span class="chip review" style="height:26px;font-size:11px">{S["p_crop_mode"]}</span>') + f'''
<div class="mbody" style="padding-bottom:160px">
  <p class="cap">{S["p_crop_hint"]}</p>
  {p_pdf_page(S, L, mobile=True)}
  <p class="cap" style="text-align:center">{S["p_crop_pages"]}</p>
</div>
<div style="position:absolute;left:0;right:0;bottom:0;background:#fff;border-top:1px solid rgba(28,30,44,.12);padding:12px 16px 24px;z-index:20;display:flex;flex-direction:column;gap:8px">
  <sc-if value="{{{{any}}}}" hint-placeholder-val="{{{{true}}}}"><p class="cap" style="text-align:center">{S["p_frames_n"].replace("{n}", "{{n}}")}</p><a class="mbtn primary" href="{fn("M-PSetup", L)}">{ic("sparkle", 16)}{S["p_crop_cta"]}</a></sc-if>
  <sc-if value="{{{{none}}}}" hint-placeholder-val="{{{{false}}}}"><p class="cap" style="text-align:center">{S["p_frames_none"]}</p><span class="mbtn dis">{ic("sparkle", 16)}{S["p_crop_cta"]}</span></sc-if>
</div>'''
    return mpage(S, "M-PCrop", S["p_titles"]["mcrop"], body, logic=P_CROP_LOGIC)

def m_psetup(S, L):
    body = mheader(S, "M-PSetup", S["p_setup_title"], back_href=fn("M-PCrop", L), right=f'<button class="chip pick" style="height:26px;font-size:11px;padding:0 10px" onClick="{{{{toggleDemo}}}}"><sc-if value="{{{{match}}}}" hint-placeholder-val="{{{{true}}}}">{S["p_demo_nomatch"]}</sc-if><sc-if value="{{{{nomatch}}}}" hint-placeholder-val="{{{{false}}}}">{S["p_demo_match"]}</sc-if></button>') + f'''
<div class="mbody" style="padding-bottom:120px">
  <sc-if value="{{{{match}}}}" hint-placeholder-val="{{{{true}}}}">
  <div class="mcard" style="padding:4px 14px;gap:0">{p_setup_rows(S, L)}<div style="display:flex;align-items:center;gap:10px;padding:10px 0"><span class="cap">{S["p_dest"]}</span><span class="b2" style="font-weight:700">{S["p_lo"]}</span></div></div>
  <p class="cap" style="margin:-4px 0 -8px;font-weight:700">{S["p_count"]}</p>
  <div class="mcard" style="gap:8px">{p_slider(S, L, mobile=True)}</div>
  </sc-if>
  <sc-if value="{{{{nomatch}}}}" hint-placeholder-val="{{{{false}}}}">{p_nomatch(S, L, mobile=True)}</sc-if>
</div>
<div style="position:absolute;left:0;right:0;bottom:0;background:#fff;border-top:1px solid rgba(28,30,44,.12);padding:12px 16px 24px;z-index:20">
  <sc-if value="{{{{match}}}}" hint-placeholder-val="{{{{true}}}}"><a class="mbtn primary" href="{fn("M-PWait", L)}">{ic("sparkle", 16)}{S["p_create"]}</a></sc-if>
  <sc-if value="{{{{nomatch}}}}" hint-placeholder-val="{{{{false}}}}"><a class="mbtn primary" href="{fn("M-PCrop", L)}">{ic("scan", 16)}{S["p_recrop"]}</a></sc-if>
</div>'''
    return mpage(S, "M-PSetup", S["p_titles"]["msetup"], body, logic=P_SETUP_LOGIC)

def m_pwait(S, L):
    body = mheader(S, "M-PWait", S["p_making"], back_href=fn("M-PSetup", L)) + f'''
<div class="mbody" style="align-items:center;justify-content:center;text-align:center">
  <span class="pspin"></span>
  <p class="sub1">{S["p_collecting"]}</p>
  <p class="cap">{S["p_wait_note"]}</p>
</div>
<a class="demo" style="right:12px;bottom:14px;padding:8px 10px 8px 12px" href="{fn("M-PSets", L)}"><span class="tag">DEMO</span>{ic("right", 16, "#fff", 2.4)}</a>'''
    return mpage(S, "M-PWait", S["p_titles"]["mwait"], body)

def m_ppractice(S, L):
    qs = [pq(P_SET2[2]), pq(P_SET2[3])]
    body = mheader(S, "M-PPractice", S["p_practice"], back_href=fn("M-PSets", L), right=f'<span class="chip neutral" style="height:26px;font-size:11px">{S["p_q_of"].replace("{i}", "{{idx}}").replace("{n}", "4")}</span>') + f'''
<div class="mbody" style="padding-bottom:120px">
  <sc-if value="{{{{q0}}}}" hint-placeholder-val="{{{{true}}}}">{p_question_block(S, L, qs[0], 3, 4, 0, mobile=True)}</sc-if>
  <sc-if value="{{{{q1}}}}" hint-placeholder-val="{{{{false}}}}">{p_question_block(S, L, qs[1], 4, 4, 1, mobile=True)}</sc-if>
  <sc-if value="{{{{end}}}}" hint-placeholder-val="{{{{false}}}}">{p_end_block(S, L, mobile=True)}</sc-if>
</div>
<div style="position:absolute;left:0;right:0;bottom:0;background:#fff;border-top:1px solid rgba(28,30,44,.12);padding:12px 16px 24px;z-index:20;display:flex;flex-direction:column;gap:8px">
  <sc-if value="{{{{q0}}}}" hint-placeholder-val="{{{{true}}}}">{p_footer(S, L, 0, mobile=True)}</sc-if>
  <sc-if value="{{{{q1}}}}" hint-placeholder-val="{{{{false}}}}">{p_footer(S, L, 1, mobile=True)}</sc-if>
  <sc-if value="{{{{end}}}}" hint-placeholder-val="{{{{false}}}}"><p class="cap" style="text-align:center">{S["p_no_status"]}</p></sc-if>
</div>'''
    return mpage(S, "M-PPractice", S["p_titles"]["mprac"], body, logic=p_practice_logic(L))

PSCREENS_T = ["P-Dialog", "P-Source", "P-Detail"]
PSCREENS_W = ["P-Sets", "P-Crop", "P-Setup", "P-Wait", "P-Practice", "P-Print"]
PSCREENS_M = ["M-PSets", "M-PCrop", "M-PSetup", "M-PWait", "M-PPractice"]
PBUILDERS = {"P-Dialog": p_dialog, "P-Source": p_source, "P-Detail": p_detail,
             "P-Sets": p_sets, "P-Crop": p_crop, "P-Setup": p_setup, "P-Wait": p_wait, "P-Practice": p_practice, "P-Print": p_print,
             "M-PSets": m_psets, "M-PCrop": m_pcrop, "M-PSetup": m_psetup, "M-PWait": m_pwait, "M-PPractice": m_ppractice}
TO_MOBILE.update({"P-Sets": "M-PSets", "P-Crop": "M-PCrop", "P-Setup": "M-PSetup", "P-Wait": "M-PWait", "P-Practice": "M-PPractice", "P-Print": "M-PSets"})
TO_PC.update({"M-PSets": "P-Sets", "M-PCrop": "P-Crop", "M-PSetup": "P-Setup", "M-PWait": "P-Wait", "M-PPractice": "P-Practice"})

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
           "T3 · Created → LO content — material, requirements, criteria", "T4 · LO settings tab — what the dialog collected, read-only", "T5 · Back in the tree — Unpublished until published",
           "T6 · Course Management — the course list, two courses on one book, Add course, Share Access (join by QR)", "T7 · Course detail — Books tab, the book that carries the dates; ⋮ with Share Access; Student tab, Extend due date (V2)", "T8 · Learning Objectives Availability — start, end and resubmission per LO, per course; an LO with no window yet",
           "T9 · Submission Grading — the queue, filtered to AI Feedback", "T10 · Overview — who has submitted", "T11 · The LO's submissions — same table, one LO", "T12 · Review and return — the grading layout",
           "T13 · Group Dashboard — Topic Dashboard, the AI Feedback LO per topic, what the class missed", "T14 · Group Dashboard — LO Dashboard, AI Feedback in the student × LO matrix", "T15 · Student Dashboard — one student's AI Feedback"]
for lang, S in (("ja", JA), ("en", EN)):
    for i, screen in enumerate(TSCREENS):
        CUR = screen
        name = tfn(screen, lang)
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(TBUILDERS[screen](S, lang))
        boards[name] = {"x": i * (TW + TGAP), "y": TROW_Y[lang], "w": TW, "h": TH,
                        "title": ttitles[i] + (" (EN)" if lang == "en" else " (JA)"), "is_interactive": True}
        order.append(name)

# AI Practice rows (24 Sep): the Similar Questions Practice LO across Back Office, PC and mobile
PROW_Y = {"ja": 8800, "en": 10500}
ptitles = ["P1 · Add LO — the Similar Questions Practice type, the required linked source LO",
           "P2 · Source LO settings — Available as practice source, locked once sets exist; Linked by",
           "P3 · Practice LO detail — linked LO, sets created, no completion status, no override",
           "P4 · Student PC — the practice LO: sets, questions done and correct; the CTA follows the selected set",
           "P5 · Student PC — crop the PDF with the Mana AI frames, then 演習をつくる",
           "P6 · Student PC — 切り取った範囲: detected questions, a per-question count capped by the shallowest stock; DEMO no-match",
           "P7 · Student PC — creating (retrieval, not generation)",
           "P8 · Student PC — practice: one attempt per question, explanation, round end",
           "P9 · Student PC — print the set",
           "P10 · Mobile — the practice LO screen", "P11 · Mobile — crop the PDF", "P12 · Mobile — 切り取った範囲", "P13 · Mobile — creating", "P14 · Mobile — practice"]
PSCREENS_ALL = PSCREENS_T + PSCREENS_W + PSCREENS_M
PSIZE = {**{k: (TW, TH) for k in PSCREENS_T}, **{k: (W, H) for k in PSCREENS_W}, **{k: (MW, MH) for k in PSCREENS_M}}
PX = {}
for lang, S in (("ja", JA), ("en", EN)):
    x = 0
    for i, screen in enumerate(PSCREENS_ALL):
        CUR = screen
        name = fn(screen, lang)
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(PBUILDERS[screen](S, lang))
        w, h = PSIZE[screen]
        boards[name] = {"x": x, "y": PROW_Y[lang], "w": w, "h": h,
                        "title": ptitles[i] + (" (EN)" if lang == "en" else " (JA)"), "is_interactive": True}
        order.append(name)
        PX[screen] = x
        x += w + 80

NW = 560
MNW = 375
TNW = 640
TNOTES = {
    "tc1": "COURSE MANAGEMENT (PM, 22 Sep: the submission start and due date are managed on the Course Management page; the book is linked to the course; the course's window gates student submissions). This is CourseList as the syllabus squad renders it (CourseList.tsx / CourseTable.tsx): the page title, the keyword search, コースの追加 Add course, and the table — Course Name with its avatar (a link into the course), Teaching Method (個別 Individual / 集団 Group), Course Type, Subject. Two courses carry the statistics book: the Thursday class and a Friday class. Both link the same book (T1), both list the same LOs, and each sets its own dates on T8 — that is the 'multiple schedule management' the move to the course buys, and why the LO dialog (T2) and the LO settings tab (T4) no longer carry dates. Nothing on this board is new for AI Feedback; the AI Feedback LO is just one more learning objective whose window the course sets. JOIN BY QR CODE (comment, 23 Sep: add a way for students to join the class by QR code, the function the AI Tutor page already has): the share icon at the end of each course row is the AI Tutor class list's (ClassListTable.tsx: MIconButtonBase + ShareIcon → AIClassShare), and it opens production's アクセスを共有 Share Access dialog as it is — the QR code the student scans to join (QRCode.toCanvas of the class code, error correction H; here a real QR of the code 7QK4M2) with ダウンロード Download, then コード Code, the same code typed instead, with コピー Copy and its snackbar. Scanning it enrols the student in the course, so the course's LOs — the AI Feedback LO among them — appear on their course tab from each LO's start date (T8). Click the share icon — it works; T7 has the same dialog behind its Share Access button. ADD COURSE (comment, 23 Sep: the add-course UX flow, from production): コースの追加 Add course opens DialogUpsertCourse — a full-screen dialog (MDialogCustom fullScreen) with the form on one paper (CourseForm), the fields in production's order: the course icon (AvatarInputHF, 112px, the camera button), a dashed divider, コース名 Course Name (required), 拠点 Location (SelectLocationInputHF — chips; a location tree dialog behind it), コース指導法種別 Teaching Method (required; 個別 Individual / 集団 Group; changing it later asks for confirmation), コースタイプ Course Type, 科目 Subject, 教材 Book (multiple; production also shows an AI学習 Adaptive switch when that feature setting is on — left out here, PM 23 Sep). It is drawn filled in: a third class of the statistics course, linking the same book — 保存 Save adds it to the list (highlighted, 1-5 / 5) with production's 正常に作成されました snackbar (commonMessage.createdSuccess); キャンセル Cancel closes. The book is linked at creation, or later from ⋮ › Assign Books on T7; the course's dates then follow on T8. Nothing here is new for AI Feedback. Click the first course →",
    "tc2": "CourseDetail (CourseDetail.tsx), landing on its Books tab as production does when the course-book setting is on: breadcrumb コース管理 / course, the course name with its ⋮ (Edit, Assign Books), the tabs 教材 Books · 学習計画 Study Plan · レッスン Lesson · 生徒 Student · クラス Class · 設定 Settings, then the Books tab's own head and the book table (production also shows an info alert here, courseBook.infoMessage, about setting availability dates per book — removed, PM 23 Sep) (CourseBookListTable: one column, Book Name, a link). This is where the book gets linked to the course (Assign Books under ⋮, AssignBooksDialog) — the link the PM's decision rests on. the ⋮ opens production's menu — 編集する Edit, 教材を割り当てる Assign Books — with アクセスを共有 Share Access added as its third item (PM, 23 Sep: in the 3-dot menu, not a button); it opens the AI Tutor class page's QR dialog (AIClassShare.tsx) for this course: the student scans the QR or types the code to join, and sees the course's LOs from their start dates. THE STUDENT TAB (comment, 23 Sep: add the student list here — who joined by code or was added manually). Click 生徒 Student — it works: production's StudentTab.tsx as it is — 生徒情報 Student Info with its 変更 Action menu (assign to class, assign study plans, …), the student-name search with the 学年度 / クラス / 学校 / 拠点 filter chips, and StudentsListTable's columns: Student Name (a link to the student's dashboard, T15), Academic Year, Location, Enrollment Date (yyyy/LL/dd - yyyy/LL/dd, the student's course period), Class, School, Study Plan — production's columns, nothing added. A 参加方法 Joined via column (QR code / code entered / added manually) was drawn and dropped: for AI Feedback nothing downstream depends on how a student got in (PM, 23 Sep: no separate column required). Seven students, five of whom joined by QR or code on the first two Thursdays; the last one has no class yet. NO STUDY PLAN COLUMN (24 Sep: the dates on T8 auto-create the course's study plan in the back end and every enrolled student — QR-joined ones included — is on it, so there is nothing to assign and nothing to show a university tenant; production's Study Plan column is hidden here). EXTEND DUE DATE, A V2 PROPOSAL (24 Sep: per-student extension is common in higher education — Canvas, Moodle — and lives at the study plan's student level, never in the course's dates): the calendar icon at the end of each row opens 期限の延長 for that student — the course's AI Feedback LOs with their window, and one editable end date for this student, the first drawn a week later; the course's dates on T8 do not move. 保存 Save closes it with a snackbar and marks the row 締切延長あり. Click the icon on any row — it works. Click the book →",
    "tc3": "LEARNING OBJECTIVES AVAILABILITY (CourseBookDetail.tsx → CourseBookDetailContent → LOAvailabilityTable), production's page for exactly this: per course, per book, the start and end date of every LO in the book, in one table — Chapter Name, Topic Name, LO Name (with its type icon), Start Date, End Date — with chapter and topic cells merged over their rows, 編集 Edit Date switching every date cell to an input (yyyy/mm/dd, hh:mm) and the actions to キャンセル / 保存, and インポート/エクスポート for CSV (useImportCSVLOAvailability / useExportCSVLOAvailability). Save posts BulkUpdateLOAvailability and shows the success snackbar (click 編集, then 保存 — both work). WHAT THE AI FEEDBACK LOs GET HERE: nothing new in kind — their window is a Start Date and an End Date like any LO's, and the End Date is the due date: the LO shows on the student's course tab from the start date and is not clickable before it; it enters the To-do on the start date; submission and replacement run until the end date; the teacher reviews after it; a late submission is refused unless this end date is extended here (PM, 22 Sep). ONE ADDED COLUMN, A PROPOSAL: 再提出締切 Resubmission Due, shown only for LOs whose 再提出を許可する switch is on (T2/T4) — the PM left 'where the resubmission date lives' open when dates moved to the course, and this is the one place all the LO's dates can sit together; it is drawn to be decided, not decided. DATA SOURCE (PM, 24 Sep: start and end dates should be based on the study plan backend): the Start Date and End Date here are the course's study plan items' available_from / available_to — the same rows Study Plan Management edits — not a separate availability table. Save writes them to the study plan; a change made in 学習計画管理 Study Plan Management shows here, and the student's course tab, To-do and the dashboards all read the same dates. The proposed Resubmission Due would be one more study-plan-item field. AN LO WITH NO WINDOW YET: the last row, 第9回 演習レポート（追加）, was added to the book after the dates were set — its Start and End are empty and a warning line says it is shown to students from publish until dates are entered; in edit mode its inputs are empty. The alert at the top says this book is assigned to two courses, that availability is set per course, and that the dates are the study plan's; the Friday class has its own copy of this page with later dates (T4 lists both). Production's Chapter/Topic/LO values here match T1's tree and T13's dashboard rows; the dates match the student's course tab (screen 1: 第7回 11月6日 公開, 第8回 11月20日から) and the Topic Dashboard's 開始 / 締切 line.",
    "t1": "TEACHER, BACK OFFICE — rebuilt on 19 Sep against the prototype generated from production (school-portal-admin, syllabus squad). This is BookDetail as the code renders it: breadcrumb Book Management / book, the book title with its status chip and Add chapter top-right, chapters as accordions (blue left edge when open, N Topic(s), ↑ ↓ ⋮), topics as accordions inside them, and each learning material as a row with its type tile, the name as a link, the AI Tutor sparkle where that is on, and its publish chip. The nav follows the live LMS 2.0 tenant the PM screenshotted, which carries more squads than the syllabus one. Nothing here is new; + Add LO is where the new type enters →",
    "t2": "DialogCreateLearningMaterial, unchanged in shape: one 900-px dialog, General Info then Settings, Cancel / Confirm. Production chooses the fields by LO type (getVisibleFieldsByLMType) — Learning Objective gets Manual Grading, Practice Mode, AI Tutor…; this is the AI Feedback branch. General Info: type, LO name, External LO ID, the description the student sees. Settings (PM, 19 Sep, then 22 Sep): the dates are GONE from this dialog — the start date, the due date and the resubmission deadline belong to the course (PM, 22 Sep: the submission start and due date are managed on the Course Management page; the book is linked to the course; the course's window gates submissions), so the 公開期間と締切 block is now a pointer to Course Management › Books › Learning Objectives Availability (T8), where one book assigned to two courses runs on two schedules; 再提出を許可する stays as the switch alone, its deadline set with the other dates on the course; 提出方法 — which of file / photos / typed the LO accepts, the 500-character limit riding with typed; 先生の確認 — the teacher-in-the-loop switch; off, a neutral notice says feedback goes out automatically after the due date. Click the type field to see where AI Feedback sits among the six existing types; the switches and checkboxes work. The type is chosen here once: after creation it cannot be changed (PM, 20 Sep) — the edit dialog on T4 shows it as a fixed field. Confirm →",
    "t3": "Where Confirm lands (PM, 19 Sep): straight on the new LO's own page, Content tab, with the created snackbar — not back in the tree, because for this type the next thing the teacher does is upload the material. The LO is UNPUBLISHED, as every new learning material is in production; Publish is the action top-right, never part of creation — click it (it works in the prototype, PM 20 Sep): the chip flips to 公開中 Published, the button goes away and a snackbar confirms; T5 shows the tree as it is before that click; the 設定 tab (T4) lists what the dialog collected. The page is the same one a regular LO opens to for authoring its questions; its tabs are Content and Settings only — 提出状況を見る jumps to Course › Submission Grading, where submissions are processed. This is where the pre-submission checklist comes from (PM, 19 Sep: 'extracted from teacher's content'): upload the brief and the marking criteria and the two outputs are generated automatically on upload — no button to press (PM, 24 Sep: no manual trigger; the chip on the file row says アップロード時に自動生成済み, and 生成し直す on the criteria card is the only way to run it again) — so 提出の基本条件 comes back as an editable list where every row carries its source (課題説明 p.1, 評価基準 2.(3)). These are the structural checks the student sees on the submit screen and that run when a file is chosen; the switch on the card turns that check off for an LO that does not need one (PM, 19 Sep) — off, nothing is shown or checked. コメントの観点 (the rubric) is generated by the LLM as LaTeX from the same material and shown as one rendered block the teacher can edit or regenerate (PM, 19 Sep) — not as separate tags. Conditions gate the submission; the rubric shapes the comments. 生徒に表示される画面を見る jumps to the student's assignment screen.",
    "t4": "The LO's SETTINGS tab (PM, 20 Sep: 'add the settings page'). Production shows an LO's settings as what its Add LO dialog collected, read-only, and Edit settings reopens that dialog (DialogCreateLearningMaterial in edit mode) prefilled — so this tab holds exactly T2's fields and nothing new: 基本情報 General Info (type, LO name, External LO ID, the description the student sees), 設定 Settings (公開期間と締切 — no longer a pair of dates but the per-course windows read from Course Management, one line per course this book is assigned to, with コース管理で日程を編集 opening T8 — PM 22 Sep; 再提出 as the switch alone; 提出方法 with the 500-character limit on typed; 先生の確認), and 公開状態 — the Published / Unpublished chip with created and updated stamps. 設定を編集 on each card and top-right opens the same dialog in EDIT mode over this page (click it — it works): prefilled, titled 学習目標を編集, with the LO type shown as a locked read-only field because the type cannot be changed after creation (PM, 20 Sep); everything else is editable, and 保存 closes it. Not here, deliberately: the material, the 提出の基本条件 and the rubric — those are content and stay on the 内容 tab (T3). The two tabs link to each other; 公開する works on this tab too. The course side (T7) shows the same values read-only with ブック管理で編集, which lands back here.",
    "t5": "The tree afterwards, reached from the breadcrumb: the new LO sits under 7-1 with its own type tile (a review-comment icon, distinct from the sparkle, which on this tree means AI Tutor), highlighted as just-created and marked Unpublished. It stays that way until the teacher publishes it, from the row's ⋮ menu or from the LO page. Clicking the row reopens T3.",
    "t6": "THE SPLIT (PM, 19 Sep): Book Management sets the LO up; it does not process student submissions. Those live under Course › 提出物の採点 (Submission Grading, ToReviewListPage), production's existing home for submissions waiting on the teacher, reused rather than given a new menu item (PM, 19 Sep) and aligned to its format (PM, 19 Sep): Submissions / Learning Objectives tabs (production's Invalid Markers export, which sits top-right on the real page, is left off this board — PM, 20 Sep: nothing to do with AI Feedback), search + Filters + Bulk Action, the status segments with counts, and the wide table (select, #, Submission ID, LO, student, username, ext. ID, course, book, reviewer, status, comments, submitted / reviewed / returned dates) — here with LO Type: AI Feedback applied. STATUSES, in the marking tones: 未確認 Not Reviewed (default) · 確認中 In Review (warning) · 返却済み Returned (success) · 差し戻し Sent Back (error), plus a secondary chip like production's Need Approval: 自動返却 Auto-returned for LOs with teacher review off, 再提出 Resubmitted for a second attempt. Submission ID → review; LO name → its overview. HIGHLIGHTED (PM, 20 Sep): a submission the teacher picked as an example for the class carries an orange ★ before its ID. The ★ 注目のみ / Highlighted only filter is an option inside フィルター / Filters (PM, 20 Sep: under Filters, not a chip in the bar) — open Filters, tick it, and the table narrows to those rows with a 注目: あり chip among the applied filters; it works in the prototype. The panel's other fields (LO Type, Status, Reviewer) are production's, static here.",
    "t7": "The LO's submission page under Course › To Review, Overview tab. The three cards are the analysis cards from the AI Tutor assignment detail (Started / Snaps / Completed in production), re-cut for this flow: 提出済み, 確認待ち — the queue the teacher-review switch creates — and 返却済み. Below, the settings as a read-only list, the Back Office's key-value pattern, so the dates and the review setting can be checked without reopening the dialog; the window row names the course it belongs to (PM, 22 Sep: dates are the course's), コース管理で日程を編集 opens the course's LO Availability page (T8) and ブック管理で編集 opens the LO's Settings tab (T4). Two count rows — 提出条件 5件, コメントの観点 6件 — were removed (PM, 20 Sep: not useful here; the conditions and the rubric are read on the LO's Content tab). The header's own ブック管理で編集 and ⋮ were removed too (PM, 20 Sep): the card's button is the one way back, and the ⋮ had nothing behind it.",
    "t8": "The LO's Submissions tab: the same Submission Grading table scoped to one LO (no LO, course or book columns), with its own status counts, and the same ★ marker and the 注目のみ / Highlighted only option inside Filters (PM, 20 Sep) so the teacher can pull up the few examples chosen for the class. Submission ID opens the review. Bulk Action is production's: contained, disabled until rows are selected — the teacher, not the model, returns the feedback, and a bulk return is a deliberate act on chosen rows.",
    "t9": "The teacher in the loop, on GradingScorePage's layout: title = LO with the status chip (確認中 In Review once opened), actions top-right (クラスで紹介する — a text button that stars this submission as an example to show the class and asks for a few-word reason, PM 20 Sep, which the dashboards then count, mark ★ and list with that reason —, 差し戻す outlined, 承認して返却する contained, and production's ⋮ kebab — asked about by the PM (20 Sep) and given its items: this student's submission history, download the original file, regenerate the draft, preview what the student sees; click it). Left, the info panel: a PREVIOUS / NEXT pager around the submission ID — 3 / 12, stepping through the LO's submissions in the list's order, Not Reviewed first, so a teacher clearing the queue never goes back to the table (PM, 20 Sep; in the prototype both arrows reload this submission) — (a 生徒には未公開 / Not visible to the student chip sat beside the ID and was removed, PM 20 Sep: the 確認中 status and the report's 下書き header already say it), Reviewer Info (reviewer, auto-return off), Submission Info (student, course, submitted, file), and the teacher's own ひとこと — which the student sees at the top of the returned screen. A Comments count section (drafts 3, edited 1, criteria 6) closed the panel and was removed (PM, 20 Sep: not useful when the comments themselves are in the report beside it; the edited mark sits on the comment). Right, the report: the recognised submission first, then each draft comment as an item with its criterion, the passage it points at, the comment, and Edit / Delete; an edited one is marked. 承認して返却する is the only thing that makes the feedback exist for the student; 差し戻す sends it back for another submission. With the switch off this screen is skipped and the row shows 自動返却.",
    "t10": "DASHBOARD (PM, 20 Sep: fit the AI Feedback overview into the group and student dashboards). This is GroupDashboard in TOPIC DASHBOARD mode, production's default view and where the Dashboard menu lands — Course / Book / Filters / Apply, the Enrollment and Duration chips (FILTERS opens production's panel — 在籍状況 Enrollment status, 期間 Duration — with an AI Feedback section added, PM 20 Sep: 開始日 start-date and 締切日 due-date ranges that keep only the feedback LOs falling inside them; the applied ranges show as chips beside Enrollment and Duration — AIフィードバック 開始日: 11/01 – 11/30, 締切日: 11/06 – 11/30 (PM, 20 Sep: show the selected ranges here); click Filters, it opens; same panel on the LO and Student dashboards), the paper with search and the Topic / LO Dashboard toggle, then production's topic table: Chapter Name, Topic Name (a link that opens the LO Dashboard for that topic, T11 →), Average Score as the progress bar over the topic's scored LOs (quizzes; -- where there is none) and Completion as the number of students who completed the topic. ADDED FOR AI FEEDBACK (PM, 20 Sep: the topic dashboard, per production, but for AI Feedback data): one column, AIフィードバック, with the topic's feedback LO (a link to its overview), its 開始 start and 締切 due dates under the name (PM, 20 Sep; since 22 Sep these are the course's dates from T8, not the LO's own) and its counts — 提出 12/30, 確認待ち 8 (a link into the LO's submissions when there are any), 返却済み 3 — and the ★ number of submissions the teacher picked to show the class. Topics without a feedback LO (6-1, 8-1) were shown with “no AI Feedback LO” and are left off the board for a clearer demo (PM, 20 Sep); in the product every topic of the book is listed, as production does. Counts, never rates (PRD §1.6.4); no score is invented for a feedback LO, so Average Score stays what production computes from the quizzes. 6-2, 7-1 and 7-2 carry the three feedback LOs the LO Dashboard shows. INSIGHTS (PM, 20 Sep: merged here from the LO Dashboard's overview paper, which is gone; the 詳しく Details expansion that opened the full insight with quotes and counts was then removed too — PM, 20 Sep: the teacher checks the submissions themself, the line only has to alert them; then broadened, PM 20 Sep, from strictly 'what the class missed' to insights of several kinds — 見落とし what was missed, 良い傾向 what is going well, 紹介候補 what is worth showing the class, 提出状況 how submissions stand — with the LLM ranking them and the top one shown per LO): under each feedback LO's counts, one line with its kind as a tag, read by an LLM pass over that LO's submissions and their generated draft feedback along the rubric — 6-2 良い傾向: 21/30 compare before and after the outlier; 7-1 見落とし: 有意性の検定に進まない下書きが 8/12件, 次回冒頭の候補; 7-2 紹介候補: 4 asked a question of their own — nothing more: no expansion, no quotes, no counts on this board (the LO's overview and submissions are one click away). It is generated from the submissions and their draft feedback, so it is there before anything is returned (PM, 20 Sep), refreshes itself whenever a submission or a draft changes (a Regenerate button was tried and removed, PM 20 Sep: no reason a teacher should have to ask), and is teacher-facing only. The rubric is the prompt's structure; every claim must trace to a count in the data.",
    "t11": "GroupDashboard in LO DASHBOARD mode, reached from a topic name on T10 or from the toggle. This is GroupDashboard as production renders it — the same filter row and chips, the paper with search, the Topic / LO Dashboard toggle and, in LO mode, the student × LO matrix for the topic (a Topic select above the matrix was tried and removed, PM 20 Sep: not in production; the Latest Score / Highest Score toggle keeps production's labels — a rename to Latest / Best Submission was tried and reverted (PM, 20 Sep) because a feedback LO has nothing to rank by, so its cells ignore the toggle and always show the latest submission's status; and the whole toggle — Latest Score and Highest Score — is greyed out when nothing in the matrix carries a score (PM, 20 Sep) — as here; it comes back live when a quiz or other scored LO is in view. For a clearer demo the matrix shows only AI Feedback LOs (PM, 20 Sep): the Session 6 report (all returned, one 差し戻し, two 再提出), the Session 7 report and the weekly reflection, so all four statuses and both secondary chips are on screen; instead a ★ marks a submission the teacher picked as an example to show the class (PM, 20 Sep: a requirement, so the teacher can find a few quickly) — set from the review screen's クラスで紹介する / Highlight for class action, counted in the LO's header, and the ★ 注目のみ / Highlighted only chip beside the score toggle narrows the matrix to students with a highlighted submission (PM, 20 Sep; it works — click it); sticky student column; regular LOs show 完了 Completed or a score with the AI Tutor sparkle and the history icon; a red tint means not done or failed). A tile row (production's Questions Solved via AI, then AI Feedback count tiles) was tried and removed (PM, 20 Sep: not required). In its place, on the PM's 'try it' (20 Sep), an OVERVIEW PAPER was built from the PRD — the three C10.3a jobs, B2's revision outcome and the §1.6.4 rules — and then taken apart block by block, so that this board is the matrix alone: (1) 未提出 Not submitted was here as counts and names per LO and was removed (PM, 20 Sep): the matrix header's 提出 12/30 and the tinted -- cells already carry it; (2) 先生の確認待ち Waiting on you — drafts awaiting approval per LO with the oldest one's age — was tried and removed as well (PM, 20 Sep: not required; the matrix header's 確認待ち count and Submission Grading carry it); (3) 今週クラスが見落とした点 What the class missed: first a templated sentence over the criteria counts; then, on the PM's 'try it' (20 Sep), an INSIGHT written by an LLM pass over the week's SUBMISSIONS AND THEIR DRAFT FEEDBACK grouped by rubric criterion (PM, 20 Sep: not the returned comments — the teacher opens this dashboard after the due date, before anything is returned, so the basis is every draft the checks produced; a returned comment counts the same, and the teacher's edits flow in once made) — what the recurring mistake actually is (8 of 12 drafts stop before the significance test, 3 read r ≈ 0.4 as causation) and one recap point — grounded two ways: the criterion counts stay beneath it as the anchor, and two quoted passages link into the submissions they come from. Teacher-facing only, one call per LO per week, the rubric as the prompt's structure; it refreshes itself when the drafts change (a Regenerate button was tried and removed, PM 20 Sep). It is also a review aid: it tells the teacher what the drafts are about to say to the class before they approve them. The PM's question that led here: is the criterion just a count (yes: drafts with an improvement comment per criterion) and could a generic agent read the feedback against the rubric instead (this is that); (4) フィードバックを活かした Acted on the feedback — resubmitted, points resolved, rewrote in their own words — was tried and removed (PM, 20 Sep: not required); (5) ★ Highlighted for class — the teacher's picks with the few-word reason typed when highlighting, each a link into the submission — was a block here and was MERGED INTO THE MATRIX (PM, 20 Sep): a highlighted cell now shows that reason under the status with a small ★ before it (★ 外れ値の扱いが的確, ★ 相関と因果を区別している…; the separate ★ icon beside the status was dropped as redundant, PM 20 Sep) and opens the submission's review screen, the LO header keeps the ★ count, and the ★ 注目のみ chip narrows the matrix to those students — and block 3 itself, What the class missed, was merged into the Topic Dashboard (T10, PM 20 Sep), one line per feedback LO with the full insight in an expanded row; so the overview paper is gone. Not shown, deliberately: score or completion-rate tiles, per-student comparisons, average time to return. Block 3 depends on criterion keys being fixed per assignment (PRD §1.6.5, U22); block 5 is collectable today. THE MATRIX below is the drill-down: in it, an AI Feedback LO carries the review-comment tile, its header reads 提出 / 確認待ち / 返却済み instead of Avg. Score / Comp. Rate / AI-answered (確認待ち links to the LO's submissions), and each cell is the submission status in the marking tones with a 再提出 secondary chip where the submission is a resubmission (the 自動返却 Auto-returned chip was shown too and removed, PM 20 Sep: not needed in the matrix — it stays in Submission Grading and on the student dashboard rows; a per-cell comment count was tried and removed, PM 20 Sep: use case unclear — it stays in Submission Grading); the cell opens the LO's submissions. Two insight panels below the matrix — comments by rubric criterion and the requirements that stopped a submission at the pre-check — were tried and removed (PM, 20 Sep: not required). Student name → the student dashboard.",
    "t12": "StudentDashboard as production renders it: the Student List (add-student icon, name and year, the selected one marked with the blue bar), the student's name, Course / Book / Filters / Apply, and the chapter / topic table with Study Date, Average Score and Completion, expandable to the LO rows (Learning Objective / Latest Submission / Latest Score / Highest Score). AI Feedback LOs sit in those rows with -- under Latest Score and Highest Score (a feedback LO has none; 再提出 1回 sat there first and was moved under the submission date, PM 21 Sep: it describes the submission, not a score). WHAT IS NEW is in the LO table itself (PM, 20 Sep: merged into the existing matrix rather than a table of its own; then, PM 20 Sep, fitted as columns rather than a detail row — the submission date was already a column): three feedback columns after production's four — 状態 Status (for every LO, PM 21 Sep: production writes 完了 Completed into the score columns of a video or slide deck, which read as statuses in score columns once a Status column existed, so 完了 moved here and the score columns show -- for anything unscored; for a feedback LO the status chip with its 再提出 / 自動返却 secondary chip and the date it was reached beneath, PM 21 Sep: a column of its own rather than sitting where a score would be), 指摘された観点 Flagged criteria — the rubric criteria that drew an improvement comment, with 再提出で修正済み where the resubmission fixed them (a コメント count column — 3, 良い点 1 ・ 改善点 2 — sat between and was dropped, PM 21 Sep: not useful; where the student stumbles is, and it is here), and 確認する / 見る into the review — the feedback LO's name a link to its overview (T7, PM 20 Sep), with the ★ reason under it where the teacher highlighted it; other LO rows show -- there. A separate paper below the table — count tiles, a submissions table and a by-criterion profile — was built first and removed in the merge. 7-2 is expanded so the weekly reflection shows too.",
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
    "m9": "Returned, on the phone: teacher's note (with the ★ line when the teacher chose this work as an example for the class, PM 20 Sep), summary, then the recognised text of the answer with the same underlines. One layout for every submission type (PM, 18 Sep). Tapping an underline — or one of the three comment chips — opens the bottom sheet for that point (PM, 18 Sep) and highlights the passage. Resubmit and PDF export at the end.",
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
        "Draft-1 return. Every card now carries its Kindai criterion as a grey tag (統計処理, 解釈…) — no level, no number — which is the data the professor's 'what did the class miss' view needs. A 次の一歩 card was tried and removed (PM, 18 Sep): an AI-written next step prescribes the class flow, which is the teacher's — the guidance now lives inside each 改善点 card and in the teacher's own note. 修正して再提出 now leads to a real second-submission screen with its due date. コメントを PDF で保存 is the portable-structure proof for Correspondence/KULeD. The ★ line in the teacher's note card (PM, 20 Sep) appears only when the teacher chose this submission as an example to show the class — set from the Back Office review screen — so the student is told before it comes up in class."},
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
    "title_t": {"x": 0, "y": TROW_Y["ja"] - 300, "text": "Back Office — inside Book Management, as production renders it: book tree → Add LO dialog with the AI Feedback type and its settings → LO content · then Course › Submission Grading: queue → overview → submissions → review and return · then Dashboard: group (topic → LO) and student · 日本語", "kind": "title1", "maxW": 8 * TW + 7 * TGAP},
    "title_t_en": {"x": 0, "y": TROW_Y["en"] - 240, "text": "Same Back Office flow in English", "kind": "title1", "maxW": 6 * TW + 5 * TGAP},
    "n_role": {"x": 1520, "y": MROW_Y["en"] + MH + 60, "w": 700, "maxH": 240, "text":
        "Teacher / student switch (19 Sep): the bottom-left pill on the Back Office boards flips to the student's screen, so the same setting can be read from both sides — the dates on T2 against the waiting copy on screen 3, the checklist on T3 against 提出前チェック on screen 2. Prototype-only, like the DEMO and PC / Mobile pills."},
}
for i, key in enumerate(["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10"]):
    notes[key] = {"x": i * (MW + MGAP), "y": MROW_Y["ja"] + MH + 60, "w": MNW, "maxH": 420, "text": MNOTES[key]}
for i, key in enumerate(["t1", "t2", "t3", "t4", "t5", "tc1", "tc2", "tc3", "t6", "t7", "t8", "t9", "t10", "t11", "t12"]):
    notes[key] = {"x": i * (TW + TGAP), "y": TROW_Y["ja"] + TH + 60, "w": TNW, "maxH": 460, "text": TNOTES[key]}
PNOTES = {
    "P-Dialog": "AI PRACTICE — the Similar Questions Practice LO (jamessim-source/AIpractice: docs/prototype-plan.md, docs/c10-finalized-logic.md = PRD C10 as decided by the PM on 24 Sep; the clickable prototype on branch `prototype`). Redrawn here on this canvas's production components and fitted into the Kindai course: the practice LO sits in Topic 7-1 beside the AI Feedback LO, linked to the Session 7 lecture slides PDF, so Book Management, Course Management, the dashboards and the student app all show it as one more LO. THIS BOARD: DialogCreateLearningMaterial with the new frontend sub-type chosen (a plain LEARNING_OBJECTIVE with ai_practice=true, like Random Activity or Paper Submission — not a new proto type). Type name decided: Similar Questions Practice LO (JA 類題演習 LO is a placeholder; Random Activity already uses AI演習). General Info as for any LO; Settings = the required リンク元の LO picker, fed by the book's LOs whose 演習の元として利用可 switch is on — one here — with the empty-state copy (turn the switch on a PDF LO first); the note of the fields hidden for this type; the flag + tenant-setting gate. Creation and linking are one save. One eligible LO may be linked by several practice LOs. Confirm → P3. T2's type menu also lists this type (click it).",
    "P-Source": "THE SOURCE LO (C10.3): the Session 7 lecture slides — a Learning Objective with a study-guide PDF, the only supported source type in v1 — on its Settings tab. Production's read-only settings, then the eligibility switch 演習の元として利用可 Available as practice source: shown only for supported types, default off; ON here, and LOCKED with the reason (students already have practice sets) — disabled with the reason, never an error on save. Below it, リンクされている類題演習 LO: the practice LOs pointing at this LO (one), with its set count. T1's tree marks this LO with a small 演習の元 chip.",
    "P-Detail": "THE PRACTICE LO's PAGE (C10.3): Settings shows ONLY the linked source LO (a link to P2) — PM, 24 Sep: \"Show only linked source LO\". What was on the page before and now lives here as record: the prepared source questions (three; the stock is never shown to students), the sets students created (12, by 5 of 30 students — the dashboard button in the header leads there), its availability (a start date set in Course Management with no end date, because a practice LO has no deadline — T8 shows the row with 開始 only), no completion status (C3), and no teacher/admin override (sets cannot be deleted, altered or regenerated). Below the settings: how it looks to students (the ✦ card with the set count only, no completion chip). Header: ダッシュボードで見る, 編集する (reopens the dialog; the type is locked).",
    "P-Sets": "STUDENT, PC (C10.4 screen 2 — Koki's prototype adopted, the PRD's rules trimming it): the practice LO opened from the course tab. StatBox 問題数 8/10 · 正解数 6 with the done-ratio bar and the round line (1回 10問ずつ). SETS: one selectable row per set — ring x/N, 完了 / 未完了 chip, 正解 k問 and the PRINT icon on every set — a generated set can be printed at any point, finished or not (PM, 24 Sep); tapping a row selects it and the bottom CTA follows (セット1 → 印刷する; セット2 → つづきから始める 2/4 with 印刷する beside it; default = the topmost unfinished set). ＋ 演習を追加する always at the end (sets accumulate; creation is never blocked by an unfinished set). 学習履歴: one row per finished round. NO crown, no LO-level completion, no delete, no edit mode, no re-practice (C3). Click a row, then the CTA.",
    "P-Crop": "CROP IN PRACTICE MODE (screen 3): the linked LO's study-guide PDF with the existing 'Mana AI' crop — up to five frames, may span pages — its confirm pill relabelled 演習をつくる →, enabled once a frame exists. Click the exercises on p.12–14 to frame them (numbered); the panel counts them and names the destination (the practice LO). With one linked LO the crop opens directly; more than one would show a chooser sheet first. No cross-book, no cross-LO practice.",
    "P-Setup": "切り取った範囲 (screen 4): at Next the frames were uploaded and MATCHED (RAG against the prepared bank) — so NO_MATCH surfaces here, before a count is chosen, and creates nothing. One row per detected question (page, 問題 tag), the read-only 追加先 line, then ONE number per question: a slider 1..max where max = the shallowest remaining stock among the cropped questions (2 here: stock 4/3/2), shown as a stated maximum — 1問につき 最大 2問 — with the live total 全部で 6問つくります; stock totals are never shown. DEMO pill top-right flips to NO_MATCH: the committed copy (PBT-3825: 'Please ensure your crop contains the question in full and try again'), もう一度 切り取る, no set. STOCK_EXHAUSTED is a distinct message (not drawn). 演習を作る → P7.",
    "P-Wait": "WAIT STATE (screen 5), for creation only — never for read-only transitions: 類題を集めています… (retrieval, not generation: RISO is generation-off; the mock calls the similar_question graph so the flow is clickable today). Failure → toast, no partial set left behind. DEMO → the set list with the new set selected.",
    "P-Practice": "PRACTICE (screen 6): the AI Tutor web app's existing MCQ practice module (modules/practice) mounted in a webview via a new ai-practice/embed route — so app and Flutter web share it and LaTeX/JSXGraph keep rendering. One attempt per question: pick an option → the correct one is marked ✓, a wrong pick ✗, the explanation box appears; 次へ →; the last question of the round ends with この回を終える → the round-end screen 演習 おわり！ N問のうち k問 正解, back to the sets. Rounds of 10 (config, pending TL), one history row per finished round. Answers are persisted per question so a reconnect resumes at the first unanswered one — this set resumes at 3/4. A completed set opens read-only; no Try Another. Click an option.",
    "P-Print": "PRINT (screen 7): the whole set as a sheet — question and options only; the source question and stock counts are never printed; re-rendered on demand, the file is not stored (GET /sets/{id}/print). Print is RISO's primary use, so it sits on every generated set — finished or not (PM, 24 Sep) — and on the CTA. Real PDF rendering, page caps and JSXGraph print fidelity are the TL's C8 items.",
    "M-PSets": "MOBILE (the learner app; the practice screens reuse manabie_ui and the existing BookFlowLOHorizontalCard, not the Duolingo-style redesign): the practice LO screen — the same StatBox, set rows, ＋ row, history and the fixed bottom CTA that follows the selected set. Reached from M1's new ✦ card (set count only, no completion chip).",
    "M-PCrop": "Mobile crop in practice mode: the existing study-guide screen (LearningVideoAndStudyGuideLMSV2Screen) with CropToAskEnabledBuilder forced on and the confirm action relabelled 演習をつくる →; the CTA is fixed at the bottom and stays disabled until a frame exists. Tap the exercises to frame them.",
    "M-PSetup": "Mobile 切り取った範囲: the same rows, destination line, the per-question slider bounded by the shallowest stock and the live total. DEMO pill → NO_MATCH with もう一度 切り取る. 演習を作る → the wait screen.",
    "M-PWait": "Mobile wait state — 類題を集めています… — creation only. DEMO → back to the practice LO with the new set.",
    "M-PPractice": "Mobile practice: the same web MCQ module in ManabieAITutorWebView (a new practice source mode), one attempt per question, the explanation under the options, 次へ / この回を終える, the round-end screen, back to the sets. Tap an option.",
}
for screen in PSCREENS_ALL:
    w = TNW if screen in PSCREENS_T else (NW if screen in PSCREENS_W else MNW)
    notes["p_" + screen] = {"x": PX[screen], "y": PROW_Y["ja"] + PSIZE[screen][1] + 60, "w": w, "maxH": 520, "text": PNOTES[screen]}
notes["title_p"] = {"x": 0, "y": PROW_Y["ja"] - 300, "text": "AI Practice — the Similar Questions Practice LO, fitted into the same course: Back Office set-up (Add LO → source LO → practice LO) → student PC (sets → crop → count → create → practice → print) → mobile · 日本語", "kind": "title1", "maxW": 12800}
notes["title_p_en"] = {"x": 0, "y": PROW_Y["en"] - 240, "text": "Same AI Practice flow in English", "kind": "title1", "maxW": 12800}

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
    "attachments": {},  # the live copy carries this key; keep it so a republish is a clean superset
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
        ("AI演習（類題演習 LO）・ 日本語", "BO 1440 ・ PC 1280 ・ モバイル 375", links(PSCREENS_ALL, "ja", ptitles)),
        ("AI Practice (Similar Questions Practice LO) · English", "BO 1440 · PC 1280 · Mobile 375", links(PSCREENS_ALL, "en", ptitles)),
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
    for screen in SCREENS + MSCREENS + TSCREENS + PSCREENS_ALL:
        name = fn(screen, lang)
        with open(os.path.join(ROOT, name), encoding="utf-8") as f:
            src = f.read()
        with open(os.path.join(SITE, name[:-8] + ".html"), "w", encoding="utf-8") as f:
            f.write(to_static(src, lang))
with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
    f.write(site_index())
print("wrote", len(order) + 1, "pages to deploy/public")
