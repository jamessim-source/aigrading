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
    lang="ja", student="山田 花子", back="もどる", menu="メニュー", notif="お知らせ 6件", lang_aria="言語",
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
    lang="en", student="Hanako Yamada", back="Back", menu="Menu", notif="6 notifications", lang_aria="Language",
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
    m_dev_pc="PC", m_dev_mobile="モバイル", m_dev_aria="表示デバイス",
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
    m_dev_pc="PC", m_dev_mobile="Mobile", m_dev_aria="Device",
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
        pc = f'<a class="dev-i" href="{fn(TO_PC[screen], L)}">{ic("monitor",14)}{S["m_dev_pc"]}</a>'
        mb = f'<span class="dev-i on">{ic("phone",14)}{S["m_dev_mobile"]}</span>'
    else:
        pc = f'<span class="dev-i on">{ic("monitor",14)}{S["m_dev_pc"]}</span>'
        mb = f'<a class="dev-i" href="{fn(TO_MOBILE[screen], L)}">{ic("phone",14)}{S["m_dev_mobile"]}</a>'
    cls = "dev" + (" m" if mobile else "") + (" nav" if over_nav else "")
    return f'<div class="{cls}" role="group" aria-label="{S["m_dev_aria"]}">{pc}{mb}</div>'

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
          <p class="b2" style="font-weight:700;display:flex;align-items:center;gap:6px">{ic("check",14,"#1f7a4d",3)}{S["a_ta_confirmed"]} ・ {{{{tcount}}}} {S["a_ta_unit"]}</p>
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
        <div class="tt"><b><i class="n" style="display:inline-flex;width:18px;height:18px;border-radius:50%;background:#1f7a4d;color:#fff;font-size:11px;font-style:normal;align-items:center;justify-content:center;vertical-align:middle;margin:-2px 6px 0 0">{n}</i>{S["labels"][kind]} ・ {crit}</b><span class="cap">{S["r_keep"]}</span></div></div>'''
        else:
            prev += f'''<button class="chk {{{{k{n}}}}}" onClick="{{{{tk{n}}}}}"><span class="box">{ic("check",13,"#fff",3)}</span>
        <div class="tt"><b><i class="n" style="display:inline-flex;width:18px;height:18px;border-radius:50%;background:{"#395ad2" if kind=="ask" else "#d13842"};color:#fff;font-size:11px;font-style:normal;align-items:center;justify-content:center;vertical-align:middle;margin:-2px 6px 0 0">{n}</i>{S["labels"][kind]} ・ {crit}</b><span class="cap">{quote}</span></div></button>'''
    selfchips = "".join(f'<button class="chip pick {{{{s{i}}}}}" onClick="{{{{ts{i}}}}}">{lbl}</button>' for i, lbl in enumerate(S["r_self"]))
    body = header(S, "06-Resubmit", S["r_title"], crumb=S["a_crumb"], back_href=fn("04-Feedback",L),
                  right_extra=f'<span class="chip wait" style="height:28px">{ic("refresh",14)}{S["r_h"]} ・ {S["r_due"]}</span>') + f'''
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
          <p class="b2" style="font-weight:700;display:flex;align-items:center;gap:6px">{ic("check",14,"#1f7a4d",3)}{S["a_ta_confirmed"]} ・ {{{{tcount}}}} {S["a_ta_unit"]}</p>
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

NW = 560
MNW = 375
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
        "PC / Mobile switch (18 Sep): the black pill in the bottom-left corner of every artboard jumps to the same step on the other device — PC ⇄ the mobile row below. Prototype-only control, like the DEMO pill; in the product the device is simply whatever the student opened."},
    "title_m": {"x": 0, "y": MROW_Y["ja"] - 300, "text": "Mobile — snap a handwritten answer: LO list → assignment → camera → crop → pages → submit → returned (bottom sheet) · 日本語", "kind": "title1", "maxW": 8 * MW + 7 * MGAP},
    "title_m_en": {"x": 0, "y": MROW_Y["en"] - 240, "text": "Same mobile flow in English", "kind": "title1", "maxW": 8 * MW + 7 * MGAP},
}
for i, key in enumerate(["m1", "m2", "m3", "m4", "m5", "m6", "m7", "m8", "m9", "m10"]):
    notes[key] = {"x": i * (MW + MGAP), "y": MROW_Y["ja"] + MH + 60, "w": MNW, "maxH": 420, "text": MNOTES[key]}

canvas = {
    "v": 3,
    "createdOnFiles": {"v": 1, "at": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")},
    "title": "AI Feedback — Student PC Prototype",
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
.mroot{width:100%;max-width:520px;height:100vh;height:100dvh;margin:0 auto}
@media (max-width:1023px){body{overflow-x:auto}}
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
    markup = re.sub(r'\s*style="width: (?:1280|375)px; height: (?:800|812)px;"', "", markup, count=1)
    # Fold an index link into the prototype-only device pill, so no page chrome is needed.
    home = "一覧" if lang == "ja" else "All"
    markup = re.sub(r'(<div class="dev[^"]*" role="group"[^>]*>)',
                    r'\1' + f'<a class="dev-i" href="/">{HOME_ICON}{home}</a>', markup, count=1)
    dark = "mroot dark" in markup
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
body{{background:{"#000" if dark else "#f2f2f4"}}}</style>
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
    <h1>AI フィードバック — 生徒プロトタイプ</h1>
    <p class="lead">近畿大学「地域環境統計学」の演習レポートを題材に、提出から先生の返却までの生徒側の流れを描いた試作です。実装ではありません。<br>
    各画面のヘッダーで 日本語 / English、左下のピルで PC / モバイルを切り替えられます。待機画面の DEMO ピルは、先生が確認して返却したところまで進めます。<br>
    <span lang="en">A prototype of the student side of AI Feedback, not an implementation. Every screen has a Japanese / English toggle in the header and a PC / Mobile switch in the bottom-left corner.</span></p>
  </header>
  {blocks}
  <footer>社内検討用。外部への共有はご遠慮ください。 ・ 仕様は <code>PRDs/ai-feedback-university-prd.md</code>。<br>
  <span lang="en">Internal review only. The specification is in the repository's PRD.</span></footer>
</main>
</body>
</html>
'''

for lang in ("ja", "en"):
    for screen in SCREENS + MSCREENS:
        name = fn(screen, lang)
        with open(os.path.join(ROOT, name), encoding="utf-8") as f:
            src = f.read()
        with open(os.path.join(SITE, name[:-8] + ".html"), "w", encoding="utf-8") as f:
            f.write(to_static(src, lang))
with open(os.path.join(SITE, "index.html"), "w", encoding="utf-8") as f:
    f.write(site_index())
print("wrote", len(order) + 1, "pages to deploy/public")
