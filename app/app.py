from flask import Flask, jsonify
import os, platform, socket, time, requests
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'MultiCloud CI/CD App', version='1.0.0')

START_TIME = time.time()

def get_uptime():
    seconds = int(time.time() - START_TIME)
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    return f"{hours:02d}:{mins:02d}:{secs:02d}"

@app.route("/")
def home():
    cloud = os.getenv("CLOUD_PROVIDER", "local")
    region = os.getenv("CLOUD_REGION", "my-laptop")
    hostname = socket.gethostname()
    python_ver = platform.python_version()
    github_repo = "JOSESAMUEL14/multicloud-cicd"
    themes = {
        "aws":    {"p1":"#FF9900","p2":"#FF6B35","label":"Amazon Web Services","short":"AWS"},
        "gcp":    {"p1":"#4285F4","p2":"#34A853","label":"Google Cloud Platform","short":"GCP"},
        "render": {"p1":"#7C3AED","p2":"#06B6D4","label":"Render Cloud","short":"RENDER"},
        "local":  {"p1":"#7C3AED","p2":"#06B6D4","label":"Local Kubernetes","short":"LOCAL"}
    }
    t = themes.get(cloud.lower(), themes["local"])
    p1 = t['p1']
    p2 = t['p2']
    cloud_icon = "<i class='fa-brands fa-aws'></i>" if cloud.lower()=="aws" else "<i class='fa-brands fa-google'></i>" if cloud.lower()=="gcp" else "<i class='fa-solid fa-cloud'></i>"
    cloud_label = "AWS" if cloud.lower()=="aws" else "GCP" if cloud.lower()=="gcp" else "Cloud"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="Multi-Cloud CI/CD Pipeline by Samuel — Docker, Kubernetes, GitHub Actions, Terraform, AWS">
<title>MultiCloud CI/CD — Samuel</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Exo+2:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{
  --p1:{p1};--p2:{p2};
  --bg:#06061a;
  --glass:rgba(255,255,255,0.04);
  --border:rgba(255,255,255,0.08);
  --muted:rgba(255,255,255,0.4);
  --card-bg:rgba(15,20,45,0.8);
}}
html{{scroll-behavior:smooth}}
body{{font-family:"Exo 2",sans-serif;background:var(--bg);color:#fff;overflow-x:hidden}}
#cv{{position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}}
.vig{{position:fixed;inset:0;z-index:1;pointer-events:none;background:radial-gradient(ellipse at 50% 50%,transparent 30%,rgba(6,6,26,0.8) 100%)}}

/* ── NAV ── */
nav{{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:0.75rem 2rem;background:rgba(6,6,26,0.92);backdrop-filter:blur(20px);border-bottom:1px solid var(--border)}}
.nav-logo{{display:flex;align-items:center;gap:10px;text-decoration:none;cursor:pointer;background:none;border:none}}
.nav-logo-dots{{display:flex;flex-direction:column;gap:4px;justify-content:center}}
.nav-logo-dot{{width:8px;height:8px;border-radius:50%}}
.nav-logo-textblock{{display:flex;flex-direction:column;gap:1px}}
.nav-logo-name{{font-family:"Space Mono",monospace;font-size:13px;font-weight:700;letter-spacing:0.5px;color:#fff;line-height:1}}
.nav-logo-sub{{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:3px;color:rgba(255,255,255,0.35);text-transform:uppercase;line-height:1}}
.nav-links{{display:flex;gap:18px}}
.nav-link{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);background:none;border:none;cursor:pointer;padding:4px 0;transition:color 0.3s}}
.nav-link:hover{{color:#fff}}
.nav-right{{display:flex;align-items:center;gap:10px}}
.nav-github{{color:var(--muted);font-size:18px;transition:color 0.3s;text-decoration:none}}
.nav-github:hover{{color:#fff}}
.live-pill{{display:flex;align-items:center;gap:6px;padding:5px 12px;border-radius:100px;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;color:#10b981}}
.live-dot{{width:6px;height:6px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;animation:blink 2s infinite}}
.nav-hamburger{{display:none;flex-direction:column;gap:4px;background:none;border:none;cursor:pointer;padding:4px}}
.nav-hamburger span{{width:20px;height:1.5px;background:var(--muted);display:block}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:0.2}}}}

/* ── MODAL ── */
.modal{{display:none;position:fixed;inset:0;z-index:200;align-items:center;justify-content:center;background:rgba(0,0,0,0.75);backdrop-filter:blur(12px)}}
.modal.show{{display:flex}}
.modal-box{{background:#0d0d1a;border:1px solid rgba(255,255,255,0.12);border-radius:20px;padding:2rem;max-width:400px;width:90%;text-align:center}}
.modal-title{{font-size:1.2rem;font-weight:800;margin-bottom:0.5rem}}
.modal-sub{{font-size:12px;color:var(--muted);margin-bottom:1.5rem;line-height:1.6}}
.modal-btns{{display:flex;gap:10px;justify-content:center}}
.modal-btn{{padding:10px 24px;border-radius:100px;font-size:10px;font-weight:700;cursor:pointer;border:none;font-family:"Space Mono",monospace;letter-spacing:1px;transition:all 0.3s}}
.modal-confirm{{background:linear-gradient(135deg,{p1},{p2});color:#fff}}
.modal-cancel{{background:rgba(255,255,255,0.08);color:#fff;border:1px solid rgba(255,255,255,0.2)}}
.modal-status{{margin-top:1rem;font-size:11px;color:var(--muted);font-family:"Space Mono",monospace;min-height:16px}}

/* ── SHARED ── */
.section{{position:relative;z-index:10;padding:5rem 2rem 4rem;max-width:1000px;margin:0 auto}}
.section-tag{{display:inline-flex;align-items:center;gap:8px;font-family:"Space Mono",monospace;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--muted);padding:5px 14px;border-radius:100px;border:1px solid var(--border);margin-bottom:1.2rem}}
.sec-title{{font-size:clamp(2.5rem,6vw,4.5rem);font-weight:900;letter-spacing:-1px;line-height:0.9;margin-bottom:1rem}}
.sec-title .w{{color:#fff}}
.sec-title .a{{background:linear-gradient(135deg,{p1},{p2});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.sec-desc{{font-size:1rem;color:var(--muted);line-height:1.8;max-width:620px;margin-bottom:2.5rem}}
.alt-bg{{background:rgba(255,255,255,0.015);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}}
.divider{{width:100%;height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:3rem 0}}
.fade-in{{opacity:0;transform:translateY(28px);transition:all 0.7s cubic-bezier(.16,1,.3,1)}}
.fade-in.visible{{opacity:1;transform:translateY(0)}}

/* ── GRID ── */
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem;margin-bottom:2rem}}
.grid-3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.5rem;margin-bottom:2rem}}

/* ── INFO CARDS ── */
.card{{background:var(--card-bg);border:1px solid var(--border);border-radius:20px;padding:1.8rem;backdrop-filter:blur(20px);transition:all 0.4s cubic-bezier(.16,1,.3,1)}}
.card:hover{{transform:translateY(-5px);border-color:rgba(255,255,255,0.15);box-shadow:0 24px 60px rgba(0,0,0,0.5)}}
.card-icon{{font-size:2.2rem;margin-bottom:1rem}}
.card-title{{font-size:1.1rem;font-weight:800;margin-bottom:0.5rem;color:#fff}}
.card-desc{{font-size:0.88rem;color:var(--muted);line-height:1.7}}

/* ── TERMINAL ── */
.terminal-wrap{{background:#0d1117;border:1px solid rgba(255,255,255,0.1);border-radius:16px;overflow:hidden;margin-bottom:2.5rem;max-width:780px}}
.terminal-bar{{background:#161b27;padding:12px 18px;display:flex;align-items:center;gap:8px;border-bottom:1px solid rgba(255,255,255,0.06)}}
.t-dot{{width:12px;height:12px;border-radius:50%}}
.terminal-title{{font-family:"Space Mono",monospace;font-size:11px;color:rgba(255,255,255,0.4);margin-left:10px;letter-spacing:1px}}
.terminal-body{{padding:1.5rem 1.8rem;font-family:"Space Mono",monospace;font-size:13px;line-height:2;min-height:220px}}
.t-line{{opacity:0;transition:opacity 0.4s;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.t-line.show{{opacity:1}}
.t-prompt{{color:rgba(255,255,255,0.45)}}
.t-cmd{{color:#fff;font-weight:700}}
.t-green{{color:#10b981;font-weight:700}}
.t-blue{{color:#60a5fa}}
.t-yellow{{color:#fbbf24}}
.t-muted{{color:rgba(255,255,255,0.38)}}
.t-badge{{display:inline-block;background:#10b981;color:#000;font-size:11px;padding:1px 10px;border-radius:5px;font-weight:700;margin-left:8px;vertical-align:middle}}
.t-badge-blue{{display:inline-block;background:#3b82f6;color:#fff;font-size:11px;padding:1px 10px;border-radius:5px;font-weight:700;margin-left:8px;vertical-align:middle}}
.t-cursor{{display:inline-block;width:8px;height:14px;background:#fff;animation:cur 1s step-end infinite;vertical-align:-2px}}
@keyframes cur{{0%,100%{{opacity:1}}50%{{opacity:0}}}}

/* ── STAT ROW (5 items) ── */
.stat-row5{{display:grid;grid-template-columns:repeat(5,1fr);gap:1rem;margin-bottom:2rem}}
.stat-card5{{background:var(--card-bg);border:1px solid var(--border);border-radius:18px;padding:1.4rem 1rem;text-align:center;transition:all 0.3s}}
.stat-card5:hover{{background:rgba(255,255,255,0.07);transform:translateY(-3px)}}
.stat-num5{{font-family:"Space Mono",monospace;font-size:2.2rem;font-weight:700;background:linear-gradient(135deg,{p1},{p2});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.1}}
.stat-label5{{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-top:8px;line-height:1.4}}

/* ── PIPE STEPS ── */
.pipe-step{{display:flex;gap:1.5rem;margin-bottom:1.5rem;align-items:flex-start;padding:1.2rem;border-radius:18px;transition:background 0.3s;border:1px solid transparent}}
.pipe-step:hover{{background:rgba(255,255,255,0.03);border-color:var(--border)}}
.pipe-icon-box{{width:54px;height:54px;border-radius:14px;background:rgba(124,58,237,0.15);border:1px solid rgba(124,58,237,0.3);display:flex;align-items:center;justify-content:center;font-size:1.4rem;flex-shrink:0}}
.pipe-content{{flex:1}}
.pipe-title{{font-size:1.1rem;font-weight:800;margin-bottom:6px;color:{p1}}}
.pipe-desc{{font-size:0.88rem;color:var(--muted);line-height:1.7}}
.pipe-tag{{display:inline-block;font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;padding:3px 12px;border-radius:100px;background:rgba(124,58,237,0.15);border:1px solid rgba(124,58,237,0.3);color:{p1};margin-top:8px}}
.pipe-num{{font-family:"Space Mono",monospace;font-size:3rem;font-weight:700;color:rgba(255,255,255,0.06);min-width:70px;line-height:1;text-align:right;flex-shrink:0;align-self:center}}

/* ── ARCHITECTURE DIAGRAM ── */
.arch-wrap{{background:var(--card-bg);border:1px solid var(--border);border-radius:20px;padding:2rem;margin-bottom:2rem}}
.arch-section-label{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--muted);text-align:center;margin-bottom:1.2rem;display:flex;align-items:center;justify-content:center;gap:8px}}
.arch-section-label::before,.arch-section-label::after{{content:"";flex:1;max-width:80px;height:1px;background:linear-gradient(90deg,transparent,var(--border))}}
.arch-section-label::after{{background:linear-gradient(90deg,var(--border),transparent)}}
.arch-row{{display:flex;align-items:center;justify-content:center;gap:0;flex-wrap:nowrap;margin-bottom:0}}
.arch-node{{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);border-radius:14px;padding:1rem 1.2rem;text-align:center;min-width:110px;transition:all 0.3s;cursor:default}}
.arch-node:hover{{background:rgba(124,58,237,0.2);border-color:rgba(124,58,237,0.5);transform:translateY(-4px)}}
.arch-node-icon{{font-size:1.8rem;margin-bottom:6px}}
.arch-node-name{{font-size:12px;font-weight:700;color:#fff;margin-bottom:2px}}
.arch-node-desc{{font-size:9px;color:var(--muted)}}
.arch-arrow{{font-size:1.2rem;color:rgba(255,255,255,0.25);padding:0 6px;margin-bottom:28px;flex-shrink:0}}
.arch-sep{{width:100%;height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:1.5rem 0}}

/* ── TECH TOOL CARDS ── */
.tool-card{{background:var(--card-bg);border:1px solid var(--border);border-radius:18px;padding:1.5rem;transition:all 0.3s}}
.tool-card:hover{{transform:translateY(-4px);border-color:rgba(255,255,255,0.15);box-shadow:0 20px 50px rgba(0,0,0,0.5)}}
.tool-header{{display:flex;align-items:center;gap:12px;margin-bottom:0.9rem}}
.tool-icon-box{{width:48px;height:48px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0}}
.tool-name{{font-size:1rem;font-weight:800}}
.tool-line{{width:40px;height:2px;border-radius:2px;margin-top:4px}}
.tool-desc{{font-size:12px;color:rgba(255,255,255,0.7);line-height:1.6;margin-bottom:0.5rem}}
.tool-why{{font-size:10px;color:var(--muted)}}

/* ── DASHBOARD HOME ── */
.dash-wrap{{position:relative;z-index:10;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:4.5rem 1.2rem 2rem}}
.pill-badge{{display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);backdrop-filter:blur(16px);padding:6px 18px;border-radius:100px;font-family:"Space Mono",monospace;font-size:9px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:1.2rem}}
.pill-dot{{width:7px;height:7px;border-radius:50%;background:{p1};box-shadow:0 0 10px {p1};animation:blink 2s infinite}}
.hero-eye{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:4px;text-transform:uppercase;color:var(--muted);margin-bottom:0.4rem;display:flex;align-items:center;justify-content:center;gap:10px}}
.hero-eye::before,.hero-eye::after{{content:"";width:35px;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.2))}}
.hero-eye::after{{background:linear-gradient(90deg,rgba(255,255,255,0.2),transparent)}}
h1{{font-size:clamp(2.5rem,6vw,4.5rem);font-weight:900;letter-spacing:-1px;line-height:0.92;margin-bottom:0.6rem;text-align:center}}
h1 .w{{color:#fff}}
h1 .a{{background:linear-gradient(135deg,{p1},{p2});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.hero-sub{{font-family:"Space Mono",monospace;font-size:9px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:var(--muted);display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;margin-bottom:1.2rem}}
.hero-dot{{width:3px;height:3px;border-radius:50%;background:{p1};opacity:0.5;display:inline-block}}
.scroll-cta{{display:flex;gap:10px;justify-content:center;margin-bottom:1.5rem;flex-wrap:wrap}}
.cta-btn{{display:inline-flex;align-items:center;gap:7px;padding:10px 22px;border-radius:100px;font-family:"Space Mono",monospace;font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;text-decoration:none;transition:all 0.3s;border:none;cursor:pointer}}
.cta-btn:hover{{transform:translateY(-3px)}}
.cta-primary{{background:linear-gradient(135deg,{p1},{p2});color:#fff;box-shadow:0 4px 16px rgba(124,58,237,0.3)}}
.cta-outline{{background:var(--glass);border:1px solid var(--border);color:rgba(255,255,255,0.6)}}
.cta-green{{background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);color:#10b981}}

/* ── PIPELINE STRIP ── */
.pipeline{{width:100%;max-width:880px;background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);border-radius:18px;padding:1rem 1.5rem;backdrop-filter:blur(30px);display:flex;align-items:center;justify-content:space-between;position:relative;margin-bottom:1rem;overflow-x:auto}}
.pipeline::before{{content:"PIPELINE";position:absolute;top:7px;left:14px;font-family:"Space Mono",monospace;font-size:7px;font-weight:700;letter-spacing:3px;color:rgba(255,255,255,0.1)}}
.pstep{{display:flex;flex-direction:column;align-items:center;gap:6px;flex:1;min-width:48px}}
.p-icon{{width:46px;height:46px;border-radius:13px;background:transparent;border:2px solid {p1};display:flex;align-items:center;justify-content:center;transition:all 0.4s;box-shadow:0 0 10px rgba(124,58,237,0.2)}}
.p-icon:hover{{transform:translateY(-5px);box-shadow:0 0 22px rgba(124,58,237,0.5);border-color:{p2}}}
.p-icon i{{font-size:18px;color:#fff}}
.p-icon svg{{width:20px;height:20px}}
.p-label{{font-family:"Space Mono",monospace;font-size:7px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted)}}
.pconn{{flex:1;display:flex;align-items:center;padding-bottom:22px;min-width:8px}}
.pline{{width:100%;height:1.5px;background:linear-gradient(90deg,{p1},{p2});opacity:0.2;position:relative;overflow:hidden;border-radius:2px}}
.pline::after{{content:"";position:absolute;top:0;left:-50%;width:30%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,1),transparent);animation:sweep 2s linear infinite}}
@keyframes sweep{{to{{left:150%}}}}

/* ── METRIC CARDS ── */
.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;width:100%;max-width:880px;margin-bottom:1rem}}
.dcard{{background:rgba(10,12,35,0.9);border-radius:16px;padding:1rem;display:flex;flex-direction:column;gap:8px;position:relative;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,0.5),0 0 0 1px rgba(255,255,255,0.06),inset 0 1px 0 rgba(255,255,255,0.08);border-top:1px solid rgba(226,232,240,0.2);transition:all 0.5s;cursor:default;transform-style:preserve-3d}}
.dcard::after{{content:"";position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#94a3b8,#ffffff,#94a3b8);opacity:0.4;animation:bargl 3s ease-in-out infinite alternate}}
@keyframes bargl{{from{{opacity:0.2}}to{{opacity:0.7}}}}
.dcard:hover{{transform:perspective(400px) rotateX(8deg) rotateY(-3deg) translateY(-7px) scale(1.03)}}
.dcard-top{{display:flex;align-items:center;justify-content:space-between}}
.dcard-icon{{width:32px;height:32px;border-radius:9px;background:linear-gradient(135deg,#94a3b8,#ffffff);display:flex;align-items:center;justify-content:center;font-size:13px;color:#06061a;transition:transform 0.5s}}
.dcard:hover .dcard-icon{{transform:rotate(-12deg) scale(1.15)}}
.dcard-ping{{width:6px;height:6px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;animation:blink 2s infinite}}
.dcard-label{{font-family:"Space Mono",monospace;font-size:7px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3)}}
.dcard-value{{font-size:0.95rem;font-weight:800;background:linear-gradient(135deg,#e2e8f0,#ffffff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.1}}
.dcard-sub{{font-size:8px;color:rgba(255,255,255,0.2)}}
.dcard-live{{font-size:8px;color:#10b981;font-weight:600}}

/* ── ACTIONS ── */
.actions{{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;width:100%;max-width:880px}}
.btn-action{{display:inline-flex;align-items:center;gap:7px;padding:10px 18px;border-radius:100px;font-family:"Space Mono",monospace;font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border:none;cursor:pointer;transition:all 0.3s;text-decoration:none}}
.btn-action:hover{{transform:translateY(-3px)}}
.btn-deploy{{background:linear-gradient(135deg,{p1},{p2});color:#fff;box-shadow:0 4px 16px rgba(124,58,237,0.3)}}
.btn-github{{background:var(--glass);border:1px solid var(--border);color:#fff}}
.btn-health{{background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);color:#10b981}}
.btn-metrics{{background:rgba(234,179,8,0.1);border:1px solid rgba(234,179,8,0.25);color:#eab308}}
.status-bar{{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:center;width:100%;max-width:880px;margin-top:0.8rem}}
.chip{{display:inline-flex;align-items:center;gap:7px;padding:7px 14px;border-radius:100px;font-family:"Space Mono",monospace;font-size:8px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;backdrop-filter:blur(16px);transition:all 0.3s}}
.chip-green{{background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);color:#10b981}}
.chip-white{{background:var(--glass);border:1px solid var(--border);color:rgba(255,255,255,0.7)}}
.chip-mono{{background:var(--glass);border:1px solid var(--border);color:var(--muted)}}

/* ── DEMO ── */
.demo-card{{background:var(--card-bg);border:1px solid var(--border);border-radius:18px;padding:1.8rem;margin-bottom:1.2rem;backdrop-filter:blur(20px)}}
.demo-card-title{{font-size:1.1rem;font-weight:800;margin-bottom:0.5rem;display:flex;align-items:center;gap:10px}}
.demo-card-desc{{font-size:13px;color:var(--muted);margin-bottom:1.2rem;line-height:1.7}}
.demo-btn{{display:inline-flex;align-items:center;gap:7px;padding:10px 20px;border-radius:100px;font-family:"Space Mono",monospace;font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border:none;cursor:pointer;transition:all 0.3s;text-decoration:none;margin-right:8px;margin-bottom:8px}}
.demo-btn:hover{{transform:translateY(-2px)}}
.demo-btn-green{{background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);color:#10b981}}
.demo-btn-yellow{{background:rgba(234,179,8,0.1);border:1px solid rgba(234,179,8,0.3);color:#eab308}}
.demo-btn-primary{{background:linear-gradient(135deg,{p1},{p2});color:#fff}}
.demo-btn-outline{{background:var(--glass);border:1px solid var(--border);color:rgba(255,255,255,0.7)}}
.response-box{{display:none;margin-top:0.8rem;background:rgba(0,0,0,0.5);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:0.8rem;font-family:"Space Mono",monospace;font-size:11px;color:#10b981;white-space:pre-wrap;word-break:break-all}}
.response-box.show{{display:block}}
.stats-display{{display:none;margin-top:0.8rem;gap:8px}}
.stats-display.show{{display:grid;grid-template-columns:1fr 1fr 1fr}}
.stat-item{{background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:0.8rem;text-align:center}}
.stat-val{{font-size:1.1rem;font-weight:800;background:linear-gradient(135deg,{p1},{p2});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.stat-lbl{{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:1px;text-transform:uppercase;color:var(--muted);margin-top:3px}}

/* ── FOOTER ── */
footer{{position:relative;z-index:10;text-align:center;padding:2.5rem 2rem;border-top:1px solid var(--border)}}
.footer-text{{font-family:"Space Mono",monospace;font-size:10px;color:var(--muted);line-height:2}}
.footer-text a{{color:{p1};text-decoration:none;transition:color 0.3s}}
.footer-text a:hover{{color:{p2}}}

/* ── MOBILE ── */
@media(max-width:900px){{
  .stat-row5{{grid-template-columns:repeat(3,1fr)}}
  .arch-row{{flex-wrap:wrap;gap:6px;justify-content:center}}
  .arch-arrow{{margin-bottom:0;display:none}}
  .arch-node{{min-width:80px}}
}}
@media(max-width:768px){{
  .nav-links{{display:none}}
  .nav-hamburger{{display:flex}}
  .cards{{grid-template-columns:1fr 1fr}}
  .grid-2,.grid-3{{grid-template-columns:1fr}}
  .stat-row5{{grid-template-columns:1fr 1fr}}
  .pipeline{{padding:0.8rem 0.6rem}}
  .p-icon{{width:36px;height:36px}}
  .p-icon i{{font-size:14px}}
  .p-label{{font-size:6px}}
  h1{{font-size:2.4rem}}
  .sec-title{{font-size:2.2rem}}
  .section{{padding:4rem 1rem 3rem}}
  .dash-wrap{{padding:4rem 1rem 2rem}}
  .terminal-body{{font-size:11px;padding:1rem 1.2rem}}
  .pipe-num{{font-size:2rem;min-width:50px}}
}}
@media(max-width:480px){{
  .cards{{grid-template-columns:1fr 1fr}}
  .stat-row5{{grid-template-columns:1fr 1fr}}
  .scroll-cta,.actions{{flex-direction:column;align-items:center}}
  .pconn{{min-width:4px}}
}}
</style>
</head>
<body>
<canvas id="cv"></canvas>
<div class="vig"></div>

<!-- ── NAV ── -->
<nav>
  <button class="nav-logo" onclick="goTo('dashboard')" aria-label="Home">
    <div class="nav-logo-dots">
      <div class="nav-logo-dot" style="background:#FF9900"></div>
      <div class="nav-logo-dot" style="background:#1D9E75"></div>
      <div class="nav-logo-dot" style="background:#185FA5"></div>
    </div>
    <div class="nav-logo-textblock">
      <span class="nav-logo-name">MultiCloud</span>
      <span class="nav-logo-sub">AWS &nbsp;·&nbsp; GCP &nbsp;·&nbsp; Azure</span>
    </div>
  </button>
  <div class="nav-links">
    <button class="nav-link" onclick="goTo('dashboard')">Home</button>
    <button class="nav-link" onclick="goTo('about')">About</button>
    <button class="nav-link" onclick="goTo('architecture')">Architecture</button>
    <button class="nav-link" onclick="goTo('techstack')">Tech Stack</button>
    <button class="nav-link" onclick="goTo('pipeline-section')">Pipeline</button>
    <button class="nav-link" onclick="goTo('demo')">Demo</button>
    <button class="nav-link" onclick="window.location.href='mailto:Josesamueld2005@gmail.com?subject=Regarding MultiCloud CI/CD Project'">Contact</button>
  </div>
  <div class="nav-right">
    <a href="https://github.com/JOSESAMUEL14/multicloud-cicd" target="_blank" rel="noopener" class="nav-github"><i class="fa-brands fa-github"></i></a>
    <div class="live-pill"><span class="live-dot"></span>LIVE</div>
    <button class="nav-hamburger" onclick="toggleMobileNav()" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>

<!-- Mobile nav -->
<div id="mobile-nav" style="display:none;position:fixed;top:52px;left:0;right:0;z-index:99;background:rgba(6,6,26,0.98);border-bottom:1px solid var(--border);padding:1.2rem 2rem;backdrop-filter:blur(20px)">
  <div style="display:flex;flex-direction:column;gap:16px">
    <button class="nav-link" onclick="goTo('dashboard');closeMobileNav()">Home</button>
    <button class="nav-link" onclick="goTo('about');closeMobileNav()">About</button>
    <button class="nav-link" onclick="goTo('architecture');closeMobileNav()">Architecture</button>
    <button class="nav-link" onclick="goTo('techstack');closeMobileNav()">Tech Stack</button>
    <button class="nav-link" onclick="goTo('pipeline-section');closeMobileNav()">Pipeline</button>
    <button class="nav-link" onclick="goTo('demo');closeMobileNav()">Demo</button>
    <button class="nav-link" onclick="window.location.href='mailto:Josesamueld2005@gmail.com?subject=Regarding MultiCloud CI/CD Project';closeMobileNav()">Contact</button>
  </div>
</div>

<!-- DEPLOY MODAL -->
<div class="modal" id="deployModal">
  <div class="modal-box">
    <div class="modal-title">🚀 Trigger Deployment</div>
    <div class="modal-sub">This will trigger a real GitHub Actions CI/CD pipeline — building a new Docker image and deploying automatically!</div>
    <div class="modal-btns">
      <button class="modal-btn modal-confirm" onclick="confirmDeploy()">Deploy Now</button>
      <button class="modal-btn modal-cancel" onclick="closeModal()">Cancel</button>
    </div>
    <div class="modal-status" id="deploy-status"></div>
  </div>
</div>

<!-- ═══════════════════════════════════ -->
<!-- SECTION 1 — HOME DASHBOARD         -->
<!-- ═══════════════════════════════════ -->
<div id="dashboard" class="dash-wrap">
  <div class="pill-badge"><span class="pill-dot"></span>{t['short']} &nbsp;·&nbsp; {t['label']} &nbsp;·&nbsp; Live</div>
  <div class="hero-eye">Multi · Cloud · Infrastructure</div>
  <h1><span class="w">MULTI</span><span class="a">CLOUD</span><br><span class="w">CI</span><span class="a">/CD</span></h1>
  <div class="hero-sub">
    Kubernetes<span class="hero-dot"></span>Docker<span class="hero-dot"></span>GitHub Actions<span class="hero-dot"></span>Terraform<span class="hero-dot"></span>AWS
  </div>
  <div class="scroll-cta">
    <button class="cta-btn cta-primary" onclick="goTo('about')"><i class="fa-solid fa-circle-info"></i> Learn More</button>
    <button class="cta-btn cta-green" onclick="goTo('demo')"><i class="fa-solid fa-rocket"></i> Live Demo</button>
    <a href="https://github.com/JOSESAMUEL14/multicloud-cicd" target="_blank" rel="noopener" class="cta-btn cta-outline"><i class="fa-brands fa-github"></i> GitHub</a>
  </div>
  <div class="pipeline">
    <div class="pstep"><div class="p-icon"><i class="fa-solid fa-code"></i></div><div class="p-label">Code</div></div>
    <div class="pconn"><div class="pline"></div></div>
    <div class="pstep"><div class="p-icon"><i class="fa-brands fa-github"></i></div><div class="p-label">GitHub</div></div>
    <div class="pconn"><div class="pline"></div></div>
    <div class="pstep"><div class="p-icon"><i class="fa-brands fa-docker"></i></div><div class="p-label">Docker</div></div>
    <div class="pconn"><div class="pline"></div></div>
    <div class="pstep"><div class="p-icon"><svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><path fill="#fff" d="M16 2a1.3 1.3 0 0 0-.5.1L5.1 7.2a1.3 1.3 0 0 0-.7 1L3.1 19.7a1.3 1.3 0 0 0 .3 1l7.6 8.6a1.3 1.3 0 0 0 1 .4h8.1a1.3 1.3 0 0 0 1-.4l7.6-8.6a1.3 1.3 0 0 0 .3-1L27.6 8.2a1.3 1.3 0 0 0-.7-1L16.6 2.1A1.3 1.3 0 0 0 16 2zm.1 2.1l9.8 4.8 1.2 10.7-7 7.9h-7.9l-7-7.9 1.2-10.7zm-.1 4a1 1 0 0 0-1 1v6.2l-4 2.4a1 1 0 1 0 1 1.7L16 17l4 2.4a1 1 0 1 0 1-1.7l-4-2.4V9a1 1 0 0 0-1-1z"/></svg></div><div class="p-label">K8s</div></div>
    <div class="pconn"><div class="pline"></div></div>
    <div class="pstep"><div class="p-icon">{cloud_icon}</div><div class="p-label">{cloud_label}</div></div>
  </div>
  <div class="cards">
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-solid fa-cloud"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Cloud</div><div class="dcard-value">{cloud.upper()}</div><div class="dcard-sub">Environment</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-solid fa-location-dot"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Region</div><div class="dcard-value">{region}</div><div class="dcard-sub">Zone</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-solid fa-microchip"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Requests</div><div class="dcard-value" id="req-count">--</div><div class="dcard-live">↻ live</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-solid fa-clock"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Uptime</div><div class="dcard-value" id="uptime">--</div><div class="dcard-live">↻ live</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-brands fa-docker"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Container</div><div class="dcard-value">Docker</div><div class="dcard-sub">Registry</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-brands fa-python"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Python</div><div class="dcard-value">{python_ver}</div><div class="dcard-sub">Runtime</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-solid fa-circle-nodes"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Replicas</div><div class="dcard-value">2 / 2</div><div class="dcard-sub">Healthy</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-solid fa-heart-pulse"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Health</div><div class="dcard-value" id="health-val">--</div><div class="dcard-live">↻ live</div></div>
  </div>
  <div class="actions">
    <button class="btn-action btn-deploy" onclick="showDeploy()"><i class="fa-solid fa-rocket"></i> Trigger Deploy</button>
    <a href="https://github.com/{github_repo}/actions" target="_blank" rel="noopener" class="btn-action btn-github"><i class="fa-brands fa-github"></i> View Pipeline</a>
    <a href="/health" target="_blank" rel="noopener" class="btn-action btn-health"><i class="fa-solid fa-heart-pulse"></i> Health Check</a>
    <a href="/metrics" target="_blank" rel="noopener" class="btn-action btn-metrics"><i class="fa-solid fa-chart-bar"></i> Metrics</a>
  </div>
  <div class="status-bar">
    <div class="chip chip-green"><span style="width:6px;height:6px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;animation:blink 1.5s infinite;display:inline-block"></span>All Systems Operational</div>
    <div class="chip chip-white"><i class="fa-solid fa-bolt"></i> Auto-Deploy Active</div>
    <div class="chip chip-mono" id="clk">--:--:--</div>
  </div>
</div>

<!-- ═══════════════════════════════════ -->
<!-- SECTION 2 — ABOUT                  -->
<!-- ═══════════════════════════════════ -->
<div class="alt-bg">
<div id="about" class="section">
  <div class="section-tag">About This Project</div>
  <div class="sec-title fade-in"><span class="w">WHAT IS</span><br><span class="a">CI/CD?</span></div>
  <div class="sec-desc fade-in">CI/CD stands for Continuous Integration and Continuous Deployment — the method used by Netflix, Amazon, Google and every modern tech company to ship software fast and reliably.</div>

  <!-- TERMINAL ANIMATION -->
  <div class="terminal-wrap fade-in">
    <div class="terminal-bar">
      <div class="t-dot" style="background:#ef4444"></div>
      <div class="t-dot" style="background:#f59e0b"></div>
      <div class="t-dot" style="background:#10b981"></div>
      <span class="terminal-title">samuel@multicloud-cicd — GitHub Actions — Run #47</span>
    </div>
    <div class="terminal-body" id="terminal-body">
      <div class="t-line" id="tl0"><span class="t-prompt">samuel@multicloud:~/multicloud-cicd$</span> <span class="t-cmd">git push origin main</span></div>
      <div class="t-line" id="tl1"><span class="t-muted">Enumerating objects: 5, done. Writing objects: 100%</span></div>
      <div class="t-line" id="tl2"><span class="t-green">✓ GitHub Actions triggered</span><span class="t-badge-blue">Build #47</span></div>
      <div class="t-line" id="tl3"><span class="t-muted">· Step 1/4 </span><span class="t-blue">Checkout repository...</span><span class="t-muted"> (0.8s)</span></div>
      <div class="t-line" id="tl4"><span class="t-green">✓ Set up Docker Buildx</span><span class="t-muted"> (1.2s)</span></div>
      <div class="t-line" id="tl5"><span class="t-green">✓ Build Docker image</span><span class="t-muted"> → </span><span class="t-blue">josesamuel14/multicloud-app:latest</span><span class="t-muted"> (9.4s)</span></div>
      <div class="t-line" id="tl6"><span class="t-green">✓ Push to Docker Hub</span><span class="t-muted"> (4.1s)</span></div>
      <div class="t-line" id="tl7"><span class="t-yellow">&#10003; Deploying to AWS EC2 ap-south-1 (Mumbai)...</span></div>
      <div class="t-line" id="tl8"><span class="t-muted">&nbsp;&nbsp;↳ SSH connect → docker pull → restart container</span></div>
      <div class="t-line" id="tl9"><span class="t-green">✓ <strong>Pipeline complete!</strong></span><span class="t-badge">26s total</span><span class="t-muted"> 🚀 Live on multicloud-cicd.onrender.com</span></div>
      <div class="t-line" id="tl10"><span class="t-prompt">samuel@multicloud:~/multicloud-cicd$</span> <span class="t-cursor"></span></div>
    </div>
  </div>

  <!-- STAT ROW — 5 items like image 4 -->
  <div class="stat-row5 fade-in">
    <div class="stat-card5"><div class="stat-num5" id="about-req">0</div><div class="stat-label5">Pipeline<br>Runs</div></div>
    <div class="stat-card5"><div class="stat-num5">60s</div><div class="stat-label5">Deploy<br>Time</div></div>
    <div class="stat-card5"><div class="stat-num5">8</div><div class="stat-label5">Tools<br>Used</div></div>
    <div class="stat-card5"><div class="stat-num5">2</div><div class="stat-label5">Cloud<br>Providers</div></div>
    <div class="stat-card5"><div class="stat-num5">100%</div><div class="stat-label5">Automated</div></div>
  </div>

  <div class="divider"></div>

  <div class="grid-2">
    <div class="card fade-in"><div class="card-icon">⚡</div><div class="card-title">Continuous Integration</div><div class="card-desc">Every code push automatically builds and tests the application. Bugs caught immediately — no more "it works on my machine" problems. Code is always in a deployable state.</div></div>
    <div class="card fade-in"><div class="card-icon">🚀</div><div class="card-title">Continuous Deployment</div><div class="card-desc">After CI passes, the new version deploys to production automatically. Push code — users see it in 60 seconds. Zero manual steps, zero human error.</div></div>
  </div>
  <div class="grid-3">
    <div class="card fade-in"><div class="card-icon">😰</div><div class="card-title">Without CI/CD</div><div class="card-desc">Deployments take hours. Bugs discovered late. Manual server configuration. Teams move slowly with fear of breaking things.</div></div>
    <div class="card fade-in"><div class="card-icon">✅</div><div class="card-title">With CI/CD</div><div class="card-desc">Deployments take 60 seconds. Bugs caught instantly. Infrastructure as code. Teams ship with confidence multiple times a day.</div></div>
    <div class="card fade-in"><div class="card-icon">🏢</div><div class="card-title">Real World Usage</div><div class="card-desc">Netflix deploys 100+ times daily. Amazon every 11 seconds. Swiggy, Zomato, Freshworks all use CI/CD pipelines like this one.</div></div>
  </div>

  <!-- Samuel card -->
  <div class="card fade-in" style="max-width:520px">
    <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1.2rem">
      <div style="width:56px;height:56px;border-radius:50%;background:linear-gradient(135deg,{p1},{p2});display:flex;align-items:center;justify-content:center;font-size:1.4rem;flex-shrink:0">👨‍💻</div>
      <div>
        <div style="font-size:1.05rem;font-weight:800">Samuel</div>
        <div style="font-size:12px;color:var(--muted)">Aspiring DevOps and Cloud Engineer</div>
        <div style="font-size:12px;color:var(--muted)">Final Year CSE · Prathyusha Engineering College</div>
      </div>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <a href="https://github.com/JOSESAMUEL14" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:5px;padding:7px 14px;border-radius:100px;background:var(--glass);border:1px solid var(--border);color:var(--muted);font-family:Space Mono,monospace;font-size:9px;text-decoration:none"><i class="fa-brands fa-github"></i> GitHub</a>
      <a href="https://linkedin.com/in/samueld14" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:5px;padding:7px 14px;border-radius:100px;background:var(--glass);border:1px solid var(--border);color:var(--muted);font-family:Space Mono,monospace;font-size:9px;text-decoration:none"><i class="fa-brands fa-linkedin"></i> LinkedIn</a>
      <a href="mailto:Josesamueld2005@gmail.com?subject=Regarding%20MultiCloud%20CI/CD%20Project" style="display:inline-flex;align-items:center;gap:5px;padding:7px 14px;border-radius:100px;background:var(--glass);border:1px solid var(--border);color:var(--muted);font-family:Space Mono,monospace;font-size:9px;text-decoration:none"><i class="fa-solid fa-envelope"></i> Email</a>
    </div>
  </div>
</div>
</div>

<!-- ═══════════════════════════════════ -->
<!-- SECTION 3 — ARCHITECTURE           -->
<!-- ═══════════════════════════════════ -->
<div id="architecture" class="section">
  <div class="section-tag">System Design</div>
  <div class="sec-title fade-in"><span class="w">ARCHITECTURE</span><br><span class="a">DIAGRAM</span></div>
  <div class="sec-desc fade-in">How all components connect and communicate in this multi-cloud CI/CD system.</div>

  <div class="arch-wrap fade-in">
    <!-- Row 1: Developer Workflow -->
    <div class="arch-section-label">Developer Workflow</div>
    <div class="arch-row">
      <div class="arch-node"><div class="arch-node-icon">💻</div><div class="arch-node-name">Developer</div><div class="arch-node-desc">Writes code</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-node"><div class="arch-node-icon"><i class="fa-brands fa-github" style="font-size:1.6rem"></i></div><div class="arch-node-name">GitHub</div><div class="arch-node-desc">git push</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-node" style="background:rgba(251,191,36,0.1);border-color:rgba(251,191,36,0.3)"><div class="arch-node-icon">⚡</div><div class="arch-node-name">GH Actions</div><div class="arch-node-desc">CI/CD trigger</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-node" style="background:rgba(36,150,237,0.1);border-color:rgba(36,150,237,0.3)"><div class="arch-node-icon"><i class="fa-brands fa-docker" style="color:#2496ED;font-size:1.6rem"></i></div><div class="arch-node-name">Docker Build</div><div class="arch-node-desc">Image created</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-node" style="background:rgba(36,150,237,0.1);border-color:rgba(36,150,237,0.3)"><div class="arch-node-icon">🐋</div><div class="arch-node-name">Docker Hub</div><div class="arch-node-desc">Registry</div></div>
    </div>
    <div class="arch-sep"></div>
    <!-- Row 2: Cloud Deployment -->
    <div class="arch-section-label">Cloud Deployment</div>
    <div class="arch-row">
      <div class="arch-node" style="background:rgba(36,150,237,0.1);border-color:rgba(36,150,237,0.3)"><div class="arch-node-icon">🐋</div><div class="arch-node-name">Docker Hub</div><div class="arch-node-desc">Image pulled</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-node" style="background:rgba(50,108,229,0.1);border-color:rgba(50,108,229,0.3)"><div class="arch-node-icon">☸️</div><div class="arch-node-name">Kubernetes</div><div class="arch-node-desc">Orchestration</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-node" style="background:rgba(255,153,0,0.1);border-color:rgba(255,153,0,0.3)"><div class="arch-node-icon"><i class="fa-brands fa-aws" style="color:#FF9900;font-size:1.6rem"></i></div><div class="arch-node-name">AWS EC2</div><div class="arch-node-desc">Mumbai</div></div>
      <div class="arch-arrow">+</div>
      <div class="arch-node"><div class="arch-node-icon">☁️</div><div class="arch-node-name">Render</div><div class="arch-node-desc">24/7 hosting</div></div>
    </div>
    <div class="arch-sep"></div>
    <!-- Row 3: Monitoring -->
    <div class="arch-section-label">Monitoring Stack</div>
    <div class="arch-row">
      <div class="arch-node" style="background:rgba(123,66,188,0.1);border-color:rgba(123,66,188,0.3)"><div class="arch-node-icon" style="font-size:1.4rem">🏗️</div><div class="arch-node-name">Terraform</div><div class="arch-node-desc">IaC</div></div>
      <div class="arch-arrow">+</div>
      <div class="arch-node" style="background:rgba(230,82,44,0.1);border-color:rgba(230,82,44,0.3)"><div class="arch-node-icon"><i class="fa-solid fa-chart-line" style="color:#E6522C;font-size:1.5rem"></i></div><div class="arch-node-name">Prometheus</div><div class="arch-node-desc">Metrics</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-node" style="background:rgba(244,104,0,0.1);border-color:rgba(244,104,0,0.3)"><div class="arch-node-icon"><i class="fa-solid fa-chart-bar" style="color:#F46800;font-size:1.5rem"></i></div><div class="arch-node-name">Grafana</div><div class="arch-node-desc">Dashboards</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-node" style="background:rgba(251,191,36,0.1);border-color:rgba(251,191,36,0.3)"><div class="arch-node-icon">🔔</div><div class="arch-node-name">Alerts</div><div class="arch-node-desc">Anomalies</div></div>
    </div>
  </div>

  <div class="grid-2">
    <div class="card fade-in"><div class="card-icon">🐳</div><div class="card-title">Containerisation</div><div class="card-desc">Flask app packaged in Docker with all dependencies. Runs identically on any machine — laptop or cloud server. No "works on my machine" issues.</div></div>
    <div class="card fade-in"><div class="card-icon">☸️</div><div class="card-title">Orchestration</div><div class="card-desc">Kubernetes keeps 2 replicas running always. Auto-restarts crashed containers. Rolling updates mean zero downtime during deployments.</div></div>
    <div class="card fade-in"><div class="card-icon">🏗️</div><div class="card-title">Infrastructure as Code</div><div class="card-desc">Terraform defines AWS infrastructure in code files. No manual clicking in AWS console — everything provisioned automatically.</div></div>
    <div class="card fade-in"><div class="card-icon">📊</div><div class="card-title">Observability</div><div class="card-desc">Prometheus scrapes metrics every 15 seconds. Grafana live dashboards show CPU, memory, request rates. Problems caught before users notice.</div></div>
  </div>
</div>

<!-- ═══════════════════════════════════ -->
<!-- SECTION 4 — TECH STACK             -->
<!-- ═══════════════════════════════════ -->
<div class="alt-bg">
<div id="techstack" class="section">
  <div class="section-tag">Tools and Technologies</div>
  <div class="sec-title fade-in"><span class="w">THE TECH</span><br><span class="a">STACK</span></div>
  <div class="sec-desc fade-in">8 industry-standard tools — each chosen because it is used by real companies in production environments worldwide.</div>
  <div class="grid-2">
    <div class="tool-card fade-in"><div class="tool-header"><div class="tool-icon-box" style="background:rgba(36,150,237,0.15);border:1px solid rgba(36,150,237,0.3)"><i class="fa-brands fa-docker" style="color:#2496ED;font-size:22px"></i></div><div><div class="tool-name">Docker</div><div class="tool-line" style="background:linear-gradient(90deg,#2496ED,transparent)"></div></div></div><div class="tool-desc">Containerisation platform. Packages app and all dependencies into portable containers that run anywhere.</div><div class="tool-why"><span style="color:#2496ED;font-weight:700">Why:</span> Industry standard. Every major company uses Docker.</div></div>
    <div class="tool-card fade-in"><div class="tool-header"><div class="tool-icon-box" style="background:rgba(50,108,229,0.15);border:1px solid rgba(50,108,229,0.3)"><i class="fa-solid fa-ship" style="color:#326CE5;font-size:22px"></i></div><div><div class="tool-name">Kubernetes</div><div class="tool-line" style="background:linear-gradient(90deg,#326CE5,transparent)"></div></div></div><div class="tool-desc">Container orchestration. Manages, scales, and auto-heals containers across servers without manual intervention.</div><div class="tool-why"><span style="color:#326CE5;font-weight:700">Why:</span> Most in-demand DevOps skill in 2025.</div></div>
    <div class="tool-card fade-in"><div class="tool-header"><div class="tool-icon-box" style="background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15)"><i class="fa-brands fa-github" style="color:#fff;font-size:22px"></i></div><div><div class="tool-name">GitHub Actions</div><div class="tool-line" style="background:linear-gradient(90deg,#fff,transparent)"></div></div></div><div class="tool-desc">CI/CD automation built into GitHub. Runs pipelines automatically on every code push — free for public repos.</div><div class="tool-why"><span style="color:#fff;font-weight:700">Why:</span> Free, integrated, used by millions of developers.</div></div>
    <div class="tool-card fade-in"><div class="tool-header"><div class="tool-icon-box" style="background:rgba(123,66,188,0.15);border:1px solid rgba(123,66,188,0.3)"><i class="fa-solid fa-layer-group" style="color:#7B42BC;font-size:22px"></i></div><div><div class="tool-name">Terraform</div><div class="tool-line" style="background:linear-gradient(90deg,#7B42BC,transparent)"></div></div></div><div class="tool-desc">Infrastructure as Code. Defines and provisions cloud resources automatically with repeatable code.</div><div class="tool-why"><span style="color:#7B42BC;font-weight:700">Why:</span> Most popular IaC tool. Works on any cloud provider.</div></div>
    <div class="tool-card fade-in"><div class="tool-header"><div class="tool-icon-box" style="background:rgba(255,153,0,0.15);border:1px solid rgba(255,153,0,0.3)"><i class="fa-brands fa-aws" style="color:#FF9900;font-size:22px"></i></div><div><div class="tool-name">AWS EC2</div><div class="tool-line" style="background:linear-gradient(90deg,#FF9900,transparent)"></div></div></div><div class="tool-desc">Amazon Web Services virtual server. Runs the containerised application in Mumbai cloud region.</div><div class="tool-why"><span style="color:#FF9900;font-weight:700">Why:</span> Largest cloud provider. Fundamental for cloud roles.</div></div>
    <div class="tool-card fade-in"><div class="tool-header"><div class="tool-icon-box" style="background:rgba(230,82,44,0.15);border:1px solid rgba(230,82,44,0.3)"><i class="fa-solid fa-chart-line" style="color:#E6522C;font-size:22px"></i></div><div><div class="tool-name">Prometheus</div><div class="tool-line" style="background:linear-gradient(90deg,#E6522C,transparent)"></div></div></div><div class="tool-desc">Open source monitoring. Scrapes and stores metrics from applications every 15 seconds automatically.</div><div class="tool-why"><span style="color:#E6522C;font-weight:700">Why:</span> Industry standard for cloud-native monitoring.</div></div>
    <div class="tool-card fade-in"><div class="tool-header"><div class="tool-icon-box" style="background:rgba(244,104,0,0.15);border:1px solid rgba(244,104,0,0.3)"><i class="fa-solid fa-chart-bar" style="color:#F46800;font-size:22px"></i></div><div><div class="tool-name">Grafana</div><div class="tool-line" style="background:linear-gradient(90deg,#F46800,transparent)"></div></div></div><div class="tool-desc">Visualisation platform. Creates beautiful live dashboards from Prometheus and other data sources.</div><div class="tool-why"><span style="color:#F46800;font-weight:700">Why:</span> Most popular open source dashboard tool worldwide.</div></div>
    <div class="tool-card fade-in"><div class="tool-header"><div class="tool-icon-box" style="background:rgba(55,118,171,0.15);border:1px solid rgba(55,118,171,0.3)"><i class="fa-brands fa-python" style="color:#3776AB;font-size:22px"></i></div><div><div class="tool-name">Python Flask</div><div class="tool-line" style="background:linear-gradient(90deg,#3776AB,transparent)"></div></div></div><div class="tool-desc">Lightweight web framework powering the dashboard with REST API endpoints for health, metrics, and deploy.</div><div class="tool-why"><span style="color:#3776AB;font-weight:700">Why:</span> Simple, fast, perfect for microservices and APIs.</div></div>
  </div>
</div>
</div>

<!-- ═══════════════════════════════════ -->
<!-- SECTION 5 — PIPELINE               -->
<!-- ═══════════════════════════════════ -->
<div id="pipeline-section" class="section">
  <div class="section-tag">How It Works</div>
  <div class="sec-title fade-in"><span class="w">THE</span><br><span class="a">PIPELINE</span></div>
  <div class="sec-desc fade-in">From writing a single line of code to seeing it live in production — every step that happens automatically in under 60 seconds.</div>

  <div class="pipe-step fade-in"><div class="pipe-icon-box">💻</div><div class="pipe-content"><div class="pipe-title">Developer Writes Code</div><div class="pipe-desc">Developer makes changes to the Flask application — adding features, fixing bugs, or updating the UI. Code lives in GitHub accessible to the entire team.</div><div class="pipe-tag">Local Development</div></div><div class="pipe-num">01</div></div>
  <div class="pipe-step fade-in"><div class="pipe-icon-box"><i class="fa-brands fa-github"></i></div><div class="pipe-content"><div class="pipe-title">Push to GitHub</div><div class="pipe-desc">Developer runs git push origin main. This single action triggers the entire automated pipeline instantly with no manual intervention needed.</div><div class="pipe-tag">GitHub</div></div><div class="pipe-num">02</div></div>
  <div class="pipe-step fade-in"><div class="pipe-icon-box">⚡</div><div class="pipe-content"><div class="pipe-title">GitHub Actions Triggers</div><div class="pipe-desc">GitHub detects the push and starts the CI/CD workflow automatically. A virtual Ubuntu server spins up on GitHub's free infrastructure to run the pipeline.</div><div class="pipe-tag">GitHub Actions</div></div><div class="pipe-num">03</div></div>
  <div class="pipe-step fade-in"><div class="pipe-icon-box"><i class="fa-brands fa-docker" style="color:#2496ED"></i></div><div class="pipe-content"><div class="pipe-title">Docker Image Built</div><div class="pipe-desc">GitHub Actions reads the Dockerfile and builds a new Docker image with the updated application. Tagged with unique commit SHA — every version is traceable.</div><div class="pipe-tag">Docker</div></div><div class="pipe-num">04</div></div>
  <div class="pipe-step fade-in"><div class="pipe-icon-box">🐋</div><div class="pipe-content"><div class="pipe-title">Image Pushed to Docker Hub</div><div class="pipe-desc">The built image is pushed to Docker Hub registry — making it available to any server worldwide as josesamuel14/multicloud-app:latest.</div><div class="pipe-tag">Docker Hub</div></div><div class="pipe-num">05</div></div>
  <div class="pipe-step fade-in"><div class="pipe-icon-box">☸️</div><div class="pipe-content"><div class="pipe-title">Kubernetes Rolling Update</div><div class="pipe-desc">Kubernetes pulls the new image and performs a Rolling Update — gradually replacing old containers. Zero downtime. Users never notice.</div><div class="pipe-tag">Kubernetes</div></div><div class="pipe-num">06</div></div>
  <div class="pipe-step fade-in"><div class="pipe-icon-box"><i class="fa-brands fa-aws" style="color:#FF9900"></i></div><div class="pipe-content"><div class="pipe-title">Live on AWS and Render</div><div class="pipe-desc">New version is live on AWS EC2 Mumbai and Render simultaneously. Total time from git push to live: under 60 seconds. Every time. Automatically.</div><div class="pipe-tag">AWS + Render</div></div><div class="pipe-num">07</div></div>
  <div class="pipe-step fade-in"><div class="pipe-icon-box">📊</div><div class="pipe-content"><div class="pipe-title">Prometheus Monitors</div><div class="pipe-desc">Prometheus scrapes metrics every 15 seconds. Grafana shows live dashboards. Engineers know about problems before users do.</div><div class="pipe-tag">Prometheus + Grafana</div></div><div class="pipe-num">08</div></div>

  <div class="card fade-in" style="text-align:center;padding:2.5rem;background:linear-gradient(135deg,rgba(124,58,237,0.08),rgba(6,182,212,0.08));border-color:rgba(124,58,237,0.2)">
    <div style="font-size:3rem;margin-bottom:0.8rem">⚡</div>
    <div style="font-size:1.5rem;font-weight:800;margin-bottom:0.5rem">Total Time: Under 60 Seconds</div>
    <div style="font-size:14px;color:var(--muted)">From git push to live in production — fully automated, zero manual steps, zero downtime</div>
  </div>
</div>

<!-- ═══════════════════════════════════ -->
<!-- SECTION 6 — LIVE DEMO              -->
<!-- ═══════════════════════════════════ -->
<div class="alt-bg">
<div id="demo" class="section">
  <div class="section-tag">Interactive Demo</div>
  <div class="sec-title fade-in"><span class="w">LIVE</span><br><span class="a">DEMO</span></div>
  <div class="sec-desc fade-in">Everything below is real and live. Click any button to interact with the actual running system right now.</div>

  <div class="demo-card fade-in">
    <div class="demo-card-title"><i class="fa-solid fa-heart-pulse" style="color:#10b981"></i> Health Check</div>
    <div class="demo-card-desc">Returns real system information — cloud provider, region, uptime, and hostname of the actual server running this app right now.</div>
    <button class="demo-btn demo-btn-green" onclick="checkHealth()"><i class="fa-solid fa-heart-pulse"></i> Check Health</button>
    <div class="response-box" id="health-response"></div>
  </div>

  <div class="demo-card fade-in">
    <div class="demo-card-title"><i class="fa-solid fa-chart-bar" style="color:#eab308"></i> Live Statistics</div>
    <div class="demo-card-desc">Fetches real-time statistics — total HTTP requests served, current uptime, and system status. Data from Prometheus metrics endpoint.</div>
    <button class="demo-btn demo-btn-yellow" onclick="checkStats()"><i class="fa-solid fa-chart-bar"></i> Fetch Live Stats</button>
    <div class="stats-display" id="stats-display">
      <div class="stat-item"><div class="stat-val" id="stat-req">--</div><div class="stat-lbl">Requests</div></div>
      <div class="stat-item"><div class="stat-val" id="stat-up">--</div><div class="stat-lbl">Uptime</div></div>
      <div class="stat-item"><div class="stat-val" id="stat-status">--</div><div class="stat-lbl">Status</div></div>
    </div>
  </div>

  <div class="demo-card fade-in">
    <div class="demo-card-title"><i class="fa-solid fa-rocket" style="color:{p1}"></i> Trigger CI/CD Pipeline</div>
    <div class="demo-card-desc">Click Deploy Now to trigger a real GitHub Actions pipeline run. A new Docker image will be built and deployed automatically. Watch it live on GitHub!</div>
    <button class="demo-btn demo-btn-primary" onclick="showDeploy()"><i class="fa-solid fa-rocket"></i> Trigger Deploy</button>
    <a href="https://github.com/JOSESAMUEL14/multicloud-cicd/actions" target="_blank" rel="noopener" class="demo-btn demo-btn-outline"><i class="fa-brands fa-github"></i> Watch on GitHub</a>
  </div>

  <div class="demo-card fade-in">
    <div class="demo-card-title"><i class="fa-solid fa-code" style="color:#06B6D4"></i> Source Code</div>
    <div class="demo-card-desc">The entire project is open source — Dockerfile, Kubernetes configs, Terraform IaC, GitHub Actions workflow, and monitoring setup.</div>
    <a href="https://github.com/JOSESAMUEL14/multicloud-cicd" target="_blank" rel="noopener" class="demo-btn demo-btn-outline"><i class="fa-brands fa-github"></i> View GitHub Repo</a>
    <a href="/metrics" target="_blank" rel="noopener" class="demo-btn demo-btn-yellow"><i class="fa-solid fa-chart-line"></i> Raw Metrics</a>
  </div>
</div>
</div>

<!-- FOOTER -->
<footer>
  <div class="footer-text">
    Built by <a href="https://github.com/JOSESAMUEL14" target="_blank" rel="noopener">Samuel</a>
    &nbsp;·&nbsp;
    <a href="https://github.com/JOSESAMUEL14/multicloud-cicd" target="_blank" rel="noopener">GitHub</a>
    &nbsp;·&nbsp;
    <a href="https://linkedin.com/in/samueld14" target="_blank" rel="noopener">LinkedIn</a>
    &nbsp;·&nbsp;
    <a href="mailto:Josesamueld2005@gmail.com?subject=Regarding%20MultiCloud%20CI/CD%20Project">Contact</a>
    <br><br>
    <span style="font-size:9px;opacity:0.5">MultiCloud CI/CD Pipeline · Docker · Kubernetes · GitHub Actions · Terraform · AWS · Prometheus · Grafana</span>
  </div>
</footer>

<script>
function goTo(id) {{
  var el = document.getElementById(id);
  if (!el) return;
  var top = el.getBoundingClientRect().top + window.pageYOffset - 58;
  window.scrollTo({{top: top, behavior: 'smooth'}});
}}
function toggleMobileNav() {{
  var m = document.getElementById('mobile-nav');
  m.style.display = (m.style.display === 'none' || m.style.display === '') ? 'block' : 'none';
}}
function closeMobileNav() {{
  document.getElementById('mobile-nav').style.display = 'none';
}}
function tick() {{
  var n = new Date();
  var el = document.getElementById('clk');
  if (el) el.textContent = String(n.getHours()).padStart(2,'0')+':'+String(n.getMinutes()).padStart(2,'0')+':'+String(n.getSeconds()).padStart(2,'0');
}}
setInterval(tick, 1000); tick();

function updateMetrics() {{
  fetch('/stats')
    .then(function(r) {{ return r.json(); }})
    .then(function(d) {{
      var rc = document.getElementById('req-count');
      var up = document.getElementById('uptime');
      var hv = document.getElementById('health-val');
      if (rc) rc.textContent = d.total_requests || '0';
      if (up) up.textContent = d.uptime || '--';
      if (hv) hv.textContent = d.status || '--';
    }})
    .catch(function() {{}});
}}
setInterval(updateMetrics, 5000); updateMetrics();

function showDeploy() {{ document.getElementById('deployModal').style.display = 'flex'; }}
function closeModal() {{
  document.getElementById('deployModal').style.display = 'none';
  document.getElementById('deploy-status').textContent = '';
}}
document.getElementById('deployModal').addEventListener('click', function(e) {{
  if (e.target === this) closeModal();
}});
function confirmDeploy() {{
  var s = document.getElementById('deploy-status');
  s.textContent = 'Triggering pipeline...'; s.style.color = '#fbbf24';
  fetch('/deploy', {{ method: 'POST', headers: {{'Content-Type': 'application/json'}} }})
    .then(function(r) {{ return r.json(); }})
    .then(function(d) {{
      s.textContent = d.success ? '✅ Pipeline triggered! Check GitHub Actions.' : '❌ ' + d.message;
      s.style.color = d.success ? '#10b981' : '#ef4444';
    }})
    .catch(function(e) {{ s.textContent = '❌ ' + e.message; s.style.color = '#ef4444'; }});
}}
function checkHealth() {{
  var box = document.getElementById('health-response');
  box.className = 'response-box show'; box.textContent = 'Fetching...';
  fetch('/health')
    .then(function(r) {{ return r.json(); }})
    .then(function(d) {{ box.textContent = JSON.stringify(d, null, 2); }})
    .catch(function(e) {{ box.textContent = 'Error: ' + e.message; }});
}}
function checkStats() {{
  var grid = document.getElementById('stats-display');
  grid.className = 'stats-display show';
  fetch('/stats')
    .then(function(r) {{ return r.json(); }})
    .then(function(d) {{
      document.getElementById('stat-req').textContent = d.total_requests || '0';
      document.getElementById('stat-up').textContent = d.uptime || '--';
      document.getElementById('stat-status').textContent = d.status || '--';
    }})
    .catch(function() {{}});
}}
setInterval(checkStats, 5000);

var obs = new IntersectionObserver(function(entries) {{
  entries.forEach(function(e) {{
    if (e.isIntersecting) {{
      e.target.classList.add('visible');
      if (e.target.classList.contains('terminal-wrap')) startTerminal();
      if (e.target.classList.contains('stat-row5')) animateCounter();
    }}
  }});
}}, {{threshold: 0.15}});
document.querySelectorAll('.fade-in').forEach(function(el) {{ obs.observe(el); }});

var terminalStarted = false;
function startTerminal() {{
  if (terminalStarted) return;
  terminalStarted = true;
  var delays = [0,700,1400,2100,2900,3700,4400,5200,5700,6500];
  for (var i = 0; i <= 10; i++) {{
    (function(idx, delay) {{
      var el = document.getElementById('tl'+idx);
      if (el) setTimeout(function() {{ el.classList.add('show'); }}, delay);
    }})(i, delays[i] || (i*600));
  }}
  setTimeout(function() {{
    terminalStarted = false;
    for (var i = 0; i <= 10; i++) {{
      var el = document.getElementById('tl'+i);
      if (el) el.classList.remove('show');
    }}
    setTimeout(startTerminal, 1500);
  }}, 11000);
}}

var counterDone = false;
function animateCounter() {{
  if (counterDone) return;
  counterDone = true;
  var el = document.getElementById('about-req');
  if (!el) return;
  var end = 47, start = 0, duration = 1400;
  var step = end / (duration / 16);
  var timer = setInterval(function() {{
    start += step;
    if (start >= end) {{ start = end; clearInterval(timer); }}
    el.textContent = Math.floor(start);
  }}, 16);
}}

var cv = document.getElementById('cv');
var ctx = cv.getContext('2d');
var W, H, ht = 0;
function rsz() {{ W = cv.width = window.innerWidth; H = cv.height = window.innerHeight; }}
rsz(); window.addEventListener('resize', rsz);
var S = 28;
function draw() {{
  ctx.fillStyle = '#06061a'; ctx.fillRect(0,0,W,H);
  ht += 0.045;
  var rows = Math.ceil(H/(S*1.5))+2, cols = Math.ceil(W/(S*1.73))+2;
  for (var r=0; r<rows; r++) {{
    for (var c=0; c<cols; c++) {{
      var x = c*S*1.73+(r%2)*S*0.866, y = r*S*1.5;
      var v = (Math.sin(ht+c*0.45+r*0.65)+Math.sin(ht*0.85+c*0.75-r*0.45)+Math.sin(ht*1.2-c*0.3+r*0.8))/3;
      var a = 0.04+v*0.2;
      ctx.beginPath();
      for (var i=0; i<6; i++) {{
        var ang = Math.PI/180*(60*i-30);
        var px = x+(S-1)*Math.cos(ang), py = y+(S-1)*Math.sin(ang);
        if(i===0) ctx.moveTo(px,py); else ctx.lineTo(px,py);
      }}
      ctx.closePath();
      ctx.strokeStyle = 'rgba(6,182,212,'+Math.max(0.03,a)+')';
      ctx.lineWidth = 0.9; ctx.stroke();
      if(v>0.45){{ ctx.fillStyle='rgba(124,58,237,'+(v-0.45)*0.25+')'; ctx.fill(); }}
      if(v>0.72){{ ctx.fillStyle='rgba(6,182,212,'+(v-0.72)*0.5+')'; ctx.fill(); }}
      if(v>0.88){{ ctx.fillStyle='rgba(255,255,255,'+(v-0.88)*0.12+')'; ctx.fill(); }}
    }}
  }}
  requestAnimationFrame(draw);
}}
draw();
</script>
</body>
</html>"""


@app.route("/health")
def health():
    data = {
        "status": "healthy",
        "cloud": os.getenv("CLOUD_PROVIDER", "local"),
        "region": os.getenv("CLOUD_REGION", "local"),
        "uptime": get_uptime(),
        "hostname": socket.gethostname(),
        "python": platform.python_version()
    }
    return jsonify(data), 200


@app.route("/stats")
def stats():
    data = {
        "status": "HEALTHY",
        "total_requests": 0,
        "uptime": get_uptime(),
        "cloud": os.getenv("CLOUD_PROVIDER", "local"),
        "hostname": socket.gethostname()
    }
    try:
        txt = requests.get("http://127.0.0.1:5000/metrics", timeout=1).text
        total = 0
        for line in txt.split('\n'):
            if 'flask_http_request_total' in line and not line.startswith('#'):
                try:
                    total += float(line.split(' ')[-1])
                except Exception:
                    pass
        data["total_requests"] = int(total)
    except Exception:
        pass
    return jsonify(data)


@app.route("/deploy", methods=["POST"])
def deploy():
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        return jsonify({"success": False, "message": "GITHUB_TOKEN not configured"})
    try:
        r = requests.post(
            "https://api.github.com/repos/JOSESAMUEL14/multicloud-cicd/dispatches",
            headers={
                "Authorization": "Bearer " + token,
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            },
            json={"event_type": "manual-deploy"},
            timeout=10
        )
        if r.status_code == 204:
            return jsonify({"success": True, "message": "Pipeline triggered!"})
        return jsonify({"success": False, "message": "GitHub API error: " + str(r.status_code)})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)