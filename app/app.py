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
<link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;600;700;800;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{
  --p1:{p1};--p2:{p2};
  --bg:#06061a;
  --glass:rgba(255,255,255,0.04);
  --border:rgba(255,255,255,0.08);
  --muted:rgba(255,255,255,0.4);
}}
html{{scroll-behavior:smooth}}
body{{font-family:"Exo 2",sans-serif;background:var(--bg);color:#fff;overflow-x:hidden}}
#cv{{position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}}
.vig{{position:fixed;inset:0;z-index:1;pointer-events:none;background:radial-gradient(ellipse at 50% 50%,transparent 25%,rgba(6,6,26,0.75) 100%)}}

/* ── NAV ── */
nav{{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:0.75rem 2rem;background:rgba(6,6,26,0.92);backdrop-filter:blur(20px);border-bottom:1px solid var(--border)}}

/* LOGO OPTION 5 — Tri-cloud dots */
.nav-logo{{display:flex;align-items:center;gap:10px;text-decoration:none;cursor:pointer}}
.nav-logo-dots{{display:flex;flex-direction:column;gap:4px;justify-content:center}}
.nav-logo-dot{{width:8px;height:8px;border-radius:50%}}
.nav-logo-dot-aws{{background:#FF9900}}
.nav-logo-dot-gcp{{background:#1D9E75}}
.nav-logo-dot-azure{{background:#185FA5}}
.nav-logo-textblock{{display:flex;flex-direction:column;gap:1px}}
.nav-logo-name{{font-family:"Space Mono",monospace;font-size:13px;font-weight:700;letter-spacing:0.5px;color:#fff;line-height:1}}
.nav-logo-sub{{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:3px;color:rgba(255,255,255,0.35);text-transform:uppercase;line-height:1}}

.nav-links{{display:flex;gap:18px}}
.nav-link{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);text-decoration:none;background:none;border:none;cursor:pointer;padding:4px 0;transition:color 0.3s}}
.nav-link:hover{{color:#fff}}
.nav-right{{display:flex;align-items:center;gap:10px}}
.nav-github{{color:var(--muted);font-size:17px;transition:color 0.3s;text-decoration:none}}
.nav-github:hover{{color:#fff}}
.live-pill{{display:flex;align-items:center;gap:5px;padding:4px 11px;border-radius:100px;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;color:#10b981}}
.live-dot{{width:5px;height:5px;border-radius:50%;background:#10b981;box-shadow:0 0 6px #10b981;animation:blink 2s infinite}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:0.2}}}}

/* ── HAMBURGER ── */
.hamburger{{display:none;flex-direction:column;gap:5px;background:none;border:none;cursor:pointer;padding:4px}}
.hamburger span{{width:22px;height:2px;background:rgba(255,255,255,0.6);border-radius:2px;transition:all 0.3s;display:block}}
.mobile-nav{{display:none;position:fixed;top:56px;left:0;right:0;z-index:99;background:rgba(6,6,26,0.98);backdrop-filter:blur(20px);border-bottom:1px solid var(--border);padding:1rem 2rem;flex-direction:column;gap:0}}
.mobile-nav.open{{display:flex}}
.mobile-nav-link{{font-family:"Space Mono",monospace;font-size:11px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);background:none;border:none;cursor:pointer;padding:14px 0;border-bottom:1px solid var(--border);text-align:left;width:100%;transition:color 0.3s}}
.mobile-nav-link:hover{{color:#fff}}

/* ── MODAL ── */
.modal{{display:none;position:fixed;inset:0;z-index:200;align-items:center;justify-content:center;background:rgba(0,0,0,0.75);backdrop-filter:blur(12px)}}
.modal.show{{display:flex}}
.modal-box{{background:#0d0d1a;border:1px solid rgba(255,255,255,0.12);border-radius:20px;padding:2rem;max-width:400px;width:90%;text-align:center}}
.modal-title{{font-size:1.2rem;font-weight:800;margin-bottom:0.5rem}}
.modal-sub{{font-size:12px;color:var(--muted);margin-bottom:1.5rem;line-height:1.6}}
.modal-btns{{display:flex;gap:10px;justify-content:center}}
.modal-btn{{padding:10px 24px;border-radius:100px;font-size:10px;font-weight:700;cursor:pointer;border:none;transition:all 0.3s;font-family:"Space Mono",monospace;letter-spacing:1px}}
.modal-confirm{{background:linear-gradient(135deg,{p1},{p2});color:#fff}}
.modal-cancel{{background:rgba(255,255,255,0.08);color:#fff;border:1px solid rgba(255,255,255,0.2)}}
.modal-status{{margin-top:1rem;font-size:11px;color:var(--muted);font-family:"Space Mono",monospace}}

/* ── SECTIONS ── */
.section{{position:relative;z-index:10;padding:5rem 2rem 4rem;max-width:960px;margin:0 auto}}
.section-tag{{display:inline-flex;align-items:center;gap:8px;font-family:"Space Mono",monospace;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--muted);padding:5px 14px;border-radius:100px;border:1px solid var(--border);margin-bottom:1.2rem}}
.sec-title{{font-size:clamp(2rem,5vw,3.5rem);font-weight:900;letter-spacing:-1px;line-height:0.92;margin-bottom:1rem}}
.sec-title .w{{color:#fff}}
.sec-title .a{{background:linear-gradient(135deg,{p1},{p2});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.sec-desc{{font-size:0.9rem;color:var(--muted);line-height:1.8;max-width:560px;margin-bottom:2.5rem}}
.divider{{width:100%;height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:3rem 0}}
.alt-bg{{background:rgba(255,255,255,0.015);border-top:1px solid var(--border);border-bottom:1px solid var(--border)}}

/* ── GRID ── */
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:1.2rem;margin-bottom:2rem}}
.grid-3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.2rem;margin-bottom:2rem}}

/* ── CARDS ── */
.card{{background:var(--glass);border:1px solid var(--border);border-radius:18px;padding:1.4rem;backdrop-filter:blur(20px);transition:all 0.4s cubic-bezier(.16,1,.3,1)}}
.card:hover{{transform:translateY(-5px);border-color:rgba(255,255,255,0.15);box-shadow:0 20px 50px rgba(0,0,0,0.5)}}
.card-title{{font-size:1rem;font-weight:700;margin-bottom:0.4rem;color:#fff}}
.card-desc{{font-size:0.82rem;color:var(--muted);line-height:1.6}}

/* ── FADE IN ── */
.fade-in{{opacity:0;transform:translateY(28px);transition:all 0.7s cubic-bezier(.16,1,.3,1)}}
.fade-in.visible{{opacity:1;transform:translateY(0)}}

/* ── TERMINAL ANIMATION (ABOUT SECTION) ── */
.terminal-wrap{{background:#0d1117;border:1px solid rgba(255,255,255,0.1);border-radius:14px;overflow:hidden;margin-bottom:2rem;box-shadow:0 20px 60px rgba(0,0,0,0.6)}}
.terminal-header{{display:flex;align-items:center;gap:8px;padding:12px 16px;background:#161b22;border-bottom:1px solid rgba(255,255,255,0.06)}}
.t-dot{{width:12px;height:12px;border-radius:50%}}
.t-dot-r{{background:#ff5f57}}
.t-dot-y{{background:#febc2e}}
.t-dot-g{{background:#28c840}}
.t-title-bar{{font-family:"Space Mono",monospace;font-size:11px;color:rgba(255,255,255,0.3);margin-left:8px}}
.terminal-body{{padding:20px 24px;font-family:"Space Mono",monospace;font-size:13px;line-height:2;min-height:200px}}
.t-prompt{{color:#6e7681}}
.t-cmd{{color:#79c0ff}}
.t-ok{{color:#3fb950}}
.t-warn{{color:#d29922}}
.t-info{{color:#58a6ff}}
.t-dim{{color:#484f58}}
.t-time{{color:#8b949e;font-size:11px}}
.t-line{{opacity:0;transform:translateY(4px);transition:opacity 0.4s ease,transform 0.4s ease}}
.t-line.show{{opacity:1;transform:translateY(0)}}
.t-cursor{{display:inline-block;width:9px;height:14px;background:#3fb950;animation:tcursor 0.8s step-end infinite;vertical-align:middle;margin-left:2px}}
@keyframes tcursor{{0%,100%{{opacity:1}}50%{{opacity:0}}}}
.t-spinner{{display:inline-block;animation:tspin 0.7s linear infinite}}
@keyframes tspin{{to{{transform:rotate(360deg)}}}}
.t-badge{{display:inline-block;background:rgba(63,185,80,0.15);border:1px solid rgba(63,185,80,0.3);color:#3fb950;font-size:10px;padding:2px 10px;border-radius:100px;margin-left:8px}}

/* ── ANIMATED STATS ── */
.stat-row{{display:flex;gap:1rem;margin-bottom:2rem;flex-wrap:wrap}}
.stat-box{{background:var(--glass);border:1px solid var(--border);border-radius:14px;padding:1.2rem;flex:1;min-width:120px;text-align:center}}
.stat-num{{font-size:2rem;font-weight:900;background:linear-gradient(135deg,{p1},{p2});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1}}
.stat-label{{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-top:4px}}

/* ── PIPE STEPS ── */
.pipe-step{{display:flex;gap:1.2rem;margin-bottom:1.8rem;align-items:flex-start;padding:1rem;border-radius:16px;transition:background 0.3s}}
.pipe-step:hover{{background:var(--glass)}}
.pipe-num{{font-family:"Space Mono",monospace;font-size:2.5rem;font-weight:700;color:rgba(255,255,255,0.07);min-width:65px;line-height:1}}
.pipe-content{{flex:1;padding-top:4px}}
.pipe-title{{font-size:1.05rem;font-weight:800;margin-bottom:4px;background:linear-gradient(135deg,{p1},{p2});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.pipe-desc{{font-size:0.82rem;color:var(--muted);line-height:1.6}}
.pipe-icon{{width:50px;height:50px;border-radius:14px;background:linear-gradient(135deg,rgba(124,58,237,0.2),rgba(6,182,212,0.2));border:1px solid rgba(124,58,237,0.3);display:flex;align-items:center;justify-content:center;font-size:1.3rem;flex-shrink:0;margin-top:4px}}
.pipe-tag{{display:inline-block;font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;padding:3px 10px;border-radius:100px;background:rgba(124,58,237,0.15);border:1px solid rgba(124,58,237,0.3);color:{p1};margin-top:6px}}

/* ── ARCH ── */
.arch-diagram{{background:var(--glass);border:1px solid var(--border);border-radius:18px;padding:1.5rem;margin-bottom:2rem;overflow-x:auto}}
.arch-row{{display:flex;align-items:center;justify-content:center;gap:0;flex-wrap:wrap;margin-bottom:1.2rem}}
.arch-box{{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);border-radius:12px;padding:0.7rem 0.9rem;text-align:center;min-width:85px;transition:all 0.3s;flex-shrink:0}}
.arch-box:hover{{background:rgba(124,58,237,0.2);border-color:rgba(124,58,237,0.5);transform:translateY(-3px)}}
.arch-box-icon{{font-size:1.2rem;margin-bottom:3px}}
.arch-box-name{{font-size:10px;font-weight:700;color:#fff}}
.arch-box-desc{{font-size:8px;color:var(--muted);margin-top:1px}}
.arch-arrow{{font-size:1.1rem;color:rgba(255,255,255,0.2);padding:0 5px;margin-bottom:22px;flex-shrink:0}}
.arch-label{{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);text-align:center;margin-bottom:0.8rem}}
.arch-divider{{width:100%;height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:1rem 0}}

/* ── HOME DASHBOARD ── */
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

/* ── HERO CLOUD BADGES ── */
.hero-cloud-badges{{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;margin-bottom:1.4rem}}
.cloud-badge{{display:inline-flex;align-items:center;gap:6px;padding:5px 13px;border-radius:100px;font-family:"Space Mono",monospace;font-size:9px;font-weight:700;letter-spacing:1px;border:1px solid;transition:transform 0.3s}}
.cloud-badge:hover{{transform:translateY(-2px)}}
.cb-aws{{background:rgba(255,153,0,0.1);border-color:rgba(255,153,0,0.3);color:#FF9900}}
.cb-k8s{{background:rgba(50,108,229,0.1);border-color:rgba(50,108,229,0.3);color:#326CE5}}
.cb-docker{{background:rgba(36,150,237,0.1);border-color:rgba(36,150,237,0.3);color:#2496ED}}
.cb-gha{{background:rgba(255,255,255,0.05);border-color:rgba(255,255,255,0.15);color:rgba(255,255,255,0.7)}}
.cb-tf{{background:rgba(123,66,188,0.1);border-color:rgba(123,66,188,0.3);color:#7B42BC}}
.cb-dot{{width:6px;height:6px;border-radius:50%;animation:blink 2s infinite}}

.scroll-cta{{display:flex;gap:10px;justify-content:center;margin-bottom:1.5rem;flex-wrap:wrap}}
.cta-btn{{display:inline-flex;align-items:center;gap:7px;padding:9px 20px;border-radius:100px;font-family:"Space Mono",monospace;font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;text-decoration:none;transition:all 0.3s;border:none;cursor:pointer}}
.cta-btn:hover{{transform:translateY(-3px)}}
.cta-primary{{background:linear-gradient(135deg,{p1},{p2});color:#fff;box-shadow:0 4px 16px rgba(124,58,237,0.3)}}
.cta-outline{{background:var(--glass);border:1px solid var(--border);color:rgba(255,255,255,0.6)}}
.cta-green{{background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);color:#10b981}}

/* ── PIPELINE STRIP ── */
.pipeline{{width:100%;max-width:860px;background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);border-radius:18px;padding:1rem 1.5rem;backdrop-filter:blur(30px);display:flex;align-items:center;justify-content:space-between;position:relative;margin-bottom:1rem;overflow-x:auto}}
.pipeline::before{{content:"PIPELINE";position:absolute;top:7px;left:14px;font-family:"Space Mono",monospace;font-size:7px;font-weight:700;letter-spacing:3px;color:rgba(255,255,255,0.1)}}
.pstep{{display:flex;flex-direction:column;align-items:center;gap:6px;flex:1;min-width:50px}}
.p-icon{{width:46px;height:46px;border-radius:13px;background:transparent;border:2px solid {p1};display:flex;align-items:center;justify-content:center;transition:all 0.4s;box-shadow:0 0 10px rgba(124,58,237,0.2)}}
.p-icon:hover{{transform:translateY(-5px);box-shadow:0 0 22px rgba(124,58,237,0.5);border-color:{p2}}}
.p-icon i{{font-size:18px;color:#fff}}
.p-icon svg{{width:20px;height:20px}}
.p-label{{font-family:"Space Mono",monospace;font-size:7px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted)}}
.pconn{{flex:1;display:flex;align-items:center;padding-bottom:22px;min-width:15px}}
.pline{{width:100%;height:1.5px;background:linear-gradient(90deg,{p1},{p2});opacity:0.2;position:relative;overflow:hidden;border-radius:2px}}
.pline::after{{content:"";position:absolute;top:0;left:-50%;width:30%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,1),transparent);animation:sweep 2s linear infinite}}
@keyframes sweep{{to{{left:150%}}}}

/* ── CARDS GRID ── */
.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:9px;width:100%;max-width:860px;margin-bottom:1rem}}
.dcard{{background:rgba(10,10,30,0.85);border-radius:15px;padding:0.9rem;display:flex;flex-direction:column;gap:7px;position:relative;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,0.5),0 0 0 1px rgba(255,255,255,0.06),inset 0 1px 0 rgba(255,255,255,0.08);border-top:1px solid rgba(226,232,240,0.2);transition:all 0.5s;cursor:default;transform-style:preserve-3d}}
.dcard::after{{content:"";position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#94a3b8,#ffffff,#94a3b8);opacity:0.4;animation:bargl 3s ease-in-out infinite alternate}}
@keyframes bargl{{from{{opacity:0.2}}to{{opacity:0.7}}}}
.dcard:hover{{transform:perspective(400px) rotateX(8deg) rotateY(-3deg) translateY(-7px) scale(1.03)}}
.dcard-top{{display:flex;align-items:center;justify-content:space-between}}
.dcard-icon{{width:32px;height:32px;border-radius:9px;background:linear-gradient(135deg,#94a3b8,#ffffff);display:flex;align-items:center;justify-content:center;font-size:13px;color:#06061a;transition:transform 0.5s}}
.dcard:hover .dcard-icon{{transform:rotate(-12deg) scale(1.15)}}
.dcard-ping{{width:6px;height:6px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;animation:blink 2s infinite}}
.dcard-label{{font-family:"Space Mono",monospace;font-size:7px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3)}}
.dcard-value{{font-size:0.95rem;font-weight:800;background:linear-gradient(135deg,#e2e8f0,#ffffff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.1;word-break:break-all}}
.dcard-sub{{font-size:8px;color:rgba(255,255,255,0.2)}}
.dcard-live{{font-size:8px;color:#10b981;font-weight:600}}

/* ── ACTION BUTTONS ── */
.actions{{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;width:100%;max-width:860px}}
.btn-action{{display:inline-flex;align-items:center;gap:7px;padding:9px 16px;border-radius:100px;font-family:"Space Mono",monospace;font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border:none;cursor:pointer;transition:all 0.3s;text-decoration:none;-webkit-appearance:none}}
.btn-action:hover{{transform:translateY(-3px)}}
.btn-deploy{{background:linear-gradient(135deg,{p1},{p2});color:#fff;box-shadow:0 4px 16px rgba(124,58,237,0.3)}}
.btn-github{{background:var(--glass);border:1px solid var(--border);color:#fff}}
.btn-health{{background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);color:#10b981}}
.btn-metrics{{background:rgba(234,179,8,0.1);border:1px solid rgba(234,179,8,0.25);color:#eab308}}
.status-bar{{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:center;width:100%;max-width:860px;margin-top:0.8rem}}
.chip{{display:inline-flex;align-items:center;gap:7px;padding:7px 14px;border-radius:100px;font-family:"Space Mono",monospace;font-size:8px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;backdrop-filter:blur(16px);transition:all 0.3s}}
.chip-green{{background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);color:#10b981}}
.chip-white{{background:var(--glass);border:1px solid var(--border);color:rgba(255,255,255,0.7)}}
.chip-mono{{background:var(--glass);border:1px solid var(--border);color:var(--muted)}}

/* ── DEMO CARDS ── */
.demo-card{{background:var(--glass);border:1px solid var(--border);border-radius:18px;padding:1.5rem;margin-bottom:1.2rem;backdrop-filter:blur(20px);transition:all 0.3s}}
.demo-card:hover{{border-color:rgba(255,255,255,0.15)}}
.demo-card-title{{font-size:1rem;font-weight:800;margin-bottom:0.4rem;display:flex;align-items:center;gap:8px}}
.demo-card-desc{{font-size:12px;color:var(--muted);margin-bottom:1rem;line-height:1.6}}
.demo-btn{{display:inline-flex;align-items:center;gap:7px;padding:9px 18px;border-radius:100px;font-family:"Space Mono",monospace;font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border:none;cursor:pointer;transition:all 0.3s;text-decoration:none;-webkit-appearance:none;margin-right:8px;margin-bottom:8px}}
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

/* ── CONTACT SECTION ── */
.contact-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-bottom:2rem}}
.contact-card{{background:var(--glass);border:1px solid var(--border);border-radius:18px;padding:1.5rem;text-align:center;text-decoration:none;color:#fff;transition:all 0.3s;display:flex;flex-direction:column;align-items:center;gap:0.6rem}}
.contact-card:hover{{transform:translateY(-5px);border-color:rgba(255,255,255,0.2);box-shadow:0 20px 40px rgba(0,0,0,0.4)}}
.contact-icon{{width:52px;height:52px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:22px;margin-bottom:4px}}
.contact-label{{font-size:0.85rem;font-weight:700}}
.contact-value{{font-family:"Space Mono",monospace;font-size:9px;color:var(--muted);letter-spacing:1px}}

/* ── FOOTER ── */
footer{{position:relative;z-index:10;text-align:center;padding:2rem;border-top:1px solid var(--border)}}
.footer-text{{font-family:"Space Mono",monospace;font-size:10px;color:var(--muted);line-height:1.8}}
.footer-text a{{color:{p1};text-decoration:none;transition:color 0.3s}}
.footer-text a:hover{{color:{p2}}}

/* ── RESPONSIVE ── */
@media(max-width:768px){{
  nav{{padding:0.75rem 1rem}}
  .nav-links{{display:none}}
  .hamburger{{display:flex}}
  .nav-logo-name{{font-size:11px}}
  .nav-logo-sub{{font-size:7px}}
  h1{{font-size:2.2rem}}
  .cards{{grid-template-columns:1fr 1fr}}
  .pipeline{{padding:0.8rem 0.6rem}}
  .p-icon{{width:36px;height:36px;border-radius:10px}}
  .p-icon i{{font-size:14px}}
  .p-label{{font-size:6px}}
  .grid-2,.grid-3{{grid-template-columns:1fr}}
  .arch-row{{flex-wrap:wrap;gap:6px;justify-content:flex-start}}
  .arch-arrow{{display:none}}
  .section{{padding:4rem 1rem 2.5rem}}
  .stat-row{{gap:0.6rem}}
  .stat-box{{min-width:80px;padding:0.8rem}}
  .stat-num{{font-size:1.5rem}}
  .terminal-body{{font-size:11px;padding:14px 16px}}
  .contact-grid{{grid-template-columns:1fr}}
  .scroll-cta{{gap:6px}}
  .cta-btn{{padding:8px 14px;font-size:8px}}
  .hero-cloud-badges{{gap:6px}}
  .cloud-badge{{font-size:8px;padding:4px 10px}}
  .dash-wrap{{padding:4rem 1rem 2rem}}
  .actions{{gap:6px}}
  .btn-action{{padding:8px 12px;font-size:8px}}
  .pipe-step{{gap:0.8rem}}
  .pipe-num{{font-size:1.8rem;min-width:45px}}
  .modal-box{{padding:1.5rem}}
  .stats-display.show{{grid-template-columns:1fr 1fr}}
}}
@media(max-width:400px){{
  .cards{{grid-template-columns:1fr}}
  h1{{font-size:1.9rem}}
  .hero-cloud-badges{{justify-content:center}}
  .terminal-body{{font-size:10px}}
}}
</style>
</head>
<body>
<canvas id="cv"></canvas>
<div class="vig"></div>

<!-- NAV -->
<nav>
  <a class="nav-logo" href="javascript:void(0)" onclick="goTo('dashboard')">
    <div class="nav-logo-dots">
      <div class="nav-logo-dot nav-logo-dot-aws"></div>
      <div class="nav-logo-dot nav-logo-dot-gcp"></div>
      <div class="nav-logo-dot nav-logo-dot-azure"></div>
    </div>
    <div class="nav-logo-textblock">
      <div class="nav-logo-name">MultiCloud</div>
      <div class="nav-logo-sub">AWS · GCP · Azure</div>
    </div>
  </a>
  <div class="nav-links">
    <button class="nav-link" onclick="goTo('dashboard')">Home</button>
    <button class="nav-link" onclick="goTo('about')">About</button>
    <button class="nav-link" onclick="goTo('architecture')">Architecture</button>
    <button class="nav-link" onclick="goTo('techstack')">Tech Stack</button>
    <button class="nav-link" onclick="goTo('pipeline-section')">Pipeline</button>
    <button class="nav-link" onclick="goTo('demo')">Demo</button>
    <button class="nav-link" onclick="goTo('contact')">Contact</button>
  </div>
  <div class="nav-right">
    <a href="https://github.com/JOSESAMUEL14/multicloud-cicd" target="_blank" rel="noopener" class="nav-github"><i class="fa-brands fa-github"></i></a>
    <div class="live-pill"><span class="live-dot"></span>LIVE</div>
    <button class="hamburger" onclick="toggleMobile()" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>

<!-- MOBILE NAV -->
<div class="mobile-nav" id="mobileNav">
  <button class="mobile-nav-link" onclick="goTo('dashboard');closeMobile()">Home</button>
  <button class="mobile-nav-link" onclick="goTo('about');closeMobile()">About</button>
  <button class="mobile-nav-link" onclick="goTo('architecture');closeMobile()">Architecture</button>
  <button class="mobile-nav-link" onclick="goTo('techstack');closeMobile()">Tech Stack</button>
  <button class="mobile-nav-link" onclick="goTo('pipeline-section');closeMobile()">Pipeline</button>
  <button class="mobile-nav-link" onclick="goTo('demo');closeMobile()">Demo</button>
  <button class="mobile-nav-link" onclick="goTo('contact');closeMobile()">Contact</button>
</div>

<!-- DEPLOY MODAL -->
<div class="modal" id="deployModal" role="dialog" aria-modal="true">
  <div class="modal-box">
    <div class="modal-title">&#128640; Trigger Deployment</div>
    <div class="modal-sub">This will trigger a real GitHub Actions CI/CD pipeline — building a new Docker image and deploying it automatically!</div>
    <div class="modal-btns">
      <button class="modal-btn modal-confirm" onclick="confirmDeploy()">Deploy Now</button>
      <button class="modal-btn modal-cancel" onclick="closeModal()">Cancel</button>
    </div>
    <div class="modal-status" id="deploy-status"></div>
  </div>
</div>

<!-- ═══════════ SECTION 1 — HOME DASHBOARD ═══════════ -->
<div id="dashboard" class="dash-wrap">
  <div class="pill-badge"><span class="pill-dot"></span>{t['short']} &nbsp;·&nbsp; {t['label']} &nbsp;·&nbsp; Live</div>
  <div class="hero-eye">Multi · Cloud · Infrastructure</div>
  <h1><span class="w">MULTI</span><span class="a">CLOUD</span><br><span class="w">CI</span><span class="a">/CD</span></h1>
  <div class="hero-sub">
    Kubernetes<span class="hero-dot"></span>
    Docker<span class="hero-dot"></span>
    GitHub Actions<span class="hero-dot"></span>
    Terraform<span class="hero-dot"></span>
    AWS
  </div>

  <!-- FLOATING TECH BADGES -->
  <div class="hero-cloud-badges">
    <span class="cloud-badge cb-aws"><span class="cb-dot" style="background:#FF9900"></span>AWS EC2</span>
    <span class="cloud-badge cb-docker"><span class="cb-dot" style="background:#2496ED"></span>Docker</span>
    <span class="cloud-badge cb-k8s"><span class="cb-dot" style="background:#326CE5"></span>Kubernetes</span>
    <span class="cloud-badge cb-gha"><span class="cb-dot" style="background:#fff"></span>GitHub Actions</span>
    <span class="cloud-badge cb-tf"><span class="cb-dot" style="background:#7B42BC"></span>Terraform</span>
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
    <div class="pstep">
      <div class="p-icon">
        <svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg"><path fill="#fff" d="M16 2a1.3 1.3 0 0 0-.5.1L5.1 7.2a1.3 1.3 0 0 0-.7 1L3.1 19.7a1.3 1.3 0 0 0 .3 1l7.6 8.6a1.3 1.3 0 0 0 1 .4h8.1a1.3 1.3 0 0 0 1-.4l7.6-8.6a1.3 1.3 0 0 0 .3-1L27.6 8.2a1.3 1.3 0 0 0-.7-1L16.6 2.1A1.3 1.3 0 0 0 16 2zm.1 2.1l9.8 4.8 1.2 10.7-7 7.9h-7.9l-7-7.9 1.2-10.7zm-.1 4a1 1 0 0 0-1 1v6.2l-4 2.4a1 1 0 1 0 1 1.7L16 17l4 2.4a1 1 0 1 0 1-1.7l-4-2.4V9a1 1 0 0 0-1-1z"/></svg>
      </div>
      <div class="p-label">K8s</div>
    </div>
    <div class="pconn"><div class="pline"></div></div>
    <div class="pstep"><div class="p-icon">{cloud_icon}</div><div class="p-label">{cloud_label}</div></div>
  </div>

  <div class="cards">
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-solid fa-cloud"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Cloud</div><div class="dcard-value">{cloud.upper()}</div><div class="dcard-sub">Environment</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-solid fa-location-dot"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Region</div><div class="dcard-value">{region}</div><div class="dcard-sub">Zone</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-solid fa-microchip"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Requests</div><div class="dcard-value" id="req-count">--</div><div class="dcard-live">&#8635; live</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-solid fa-clock"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Uptime</div><div class="dcard-value" id="uptime">--</div><div class="dcard-live">&#8635; live</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-brands fa-docker"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Container</div><div class="dcard-value">Docker</div><div class="dcard-sub">Registry</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-brands fa-python"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Python</div><div class="dcard-value">{python_ver}</div><div class="dcard-sub">Runtime</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-solid fa-circle-nodes"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Replicas</div><div class="dcard-value">2 / 2</div><div class="dcard-sub">Healthy</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-solid fa-heart-pulse"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Health</div><div class="dcard-value" id="health-val">--</div><div class="dcard-live">&#8635; live</div></div>
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

<!-- ═══════════ SECTION 2 — ABOUT ═══════════ -->
<div class="alt-bg">
<div id="about" class="section">
  <div class="section-tag">About This Project</div>
  <div class="sec-title fade-in"><span class="w">WHAT IS</span><br><span class="a">CI/CD?</span></div>
  <div class="sec-desc fade-in">CI/CD stands for Continuous Integration and Continuous Deployment — the method used by Netflix, Amazon, Google and every modern tech company to ship software fast and reliably.</div>

  <!-- TERMINAL PIPELINE ANIMATION -->
  <div class="terminal-wrap fade-in">
    <div class="terminal-header">
      <div class="t-dot t-dot-r"></div>
      <div class="t-dot t-dot-y"></div>
      <div class="t-dot t-dot-g"></div>
      <div class="t-title-bar">samuel@multicloud-cicd — GitHub Actions — Run #47</div>
    </div>
    <div class="terminal-body" id="term-body">
      <div class="t-line" id="tl-0"><span class="t-prompt">samuel@multicloud:~/multicloud-cicd$</span> <span class="t-cmd">git push origin main</span></div>
      <div class="t-line" id="tl-1"><span class="t-dim">Enumerating objects: 5, done. Writing objects: 100%</span></div>
      <div class="t-line" id="tl-2"><span class="t-ok">&#10003;</span> <span style="color:#fff">GitHub Actions triggered</span> <span class="t-badge">Build #47</span></div>
      <div class="t-line" id="tl-3"><span class="t-dim">&#9656; Step 1/4</span> <span class="t-info">Checkout repository...</span> <span class="t-time">(0.8s)</span></div>
      <div class="t-line" id="tl-4"><span class="t-ok">&#10003;</span> <span class="t-info">Set up Docker Buildx</span> <span class="t-time">(1.2s)</span></div>
      <div class="t-line" id="tl-5"><span class="t-ok">&#10003;</span> <span class="t-info">Build Docker image</span> <span style="color:#fff">→ josesamuel14/multicloud-app:latest</span> <span class="t-time">(9.4s)</span></div>
      <div class="t-line" id="tl-6"><span class="t-ok">&#10003;</span> <span class="t-info">Push to Docker Hub</span> <span class="t-time">(4.1s)</span></div>
      <div class="t-line" id="tl-7"><span class="t-warn"><span class="t-spinner" id="term-spin">&#9702;</span></span> <span class="t-warn">Deploying to AWS EC2 ap-south-1 (Mumbai)...</span></div>
      <div class="t-line" id="tl-8"><span class="t-dim">  &#9492;&#9472; SSH connect &#8594; docker pull &#8594; restart container</span></div>
      <div class="t-line" id="tl-9"><span class="t-ok">&#10003;</span> <span style="color:#fff;font-weight:700">Pipeline complete!</span> <span class="t-badge">26s total</span> <span class="t-time">&#128640; Live on multicloud-cicd.onrender.com</span></div>
      <div class="t-line" id="tl-10"><span class="t-prompt">samuel@multicloud:~/multicloud-cicd$</span> <span class="t-cursor"></span></div>
    </div>
  </div>

  <!-- Stats -->
  <div class="stat-row fade-in">
    <div class="stat-box"><div class="stat-num" id="counter-deploy">0</div><div class="stat-label">Pipeline Runs</div></div>
    <div class="stat-box"><div class="stat-num">26s</div><div class="stat-label">Deploy Time</div></div>
    <div class="stat-box"><div class="stat-num">8</div><div class="stat-label">Tools Used</div></div>
    <div class="stat-box"><div class="stat-num">2</div><div class="stat-label">Cloud Providers</div></div>
    <div class="stat-box"><div class="stat-num">100%</div><div class="stat-label">Automated</div></div>
  </div>

  <div class="grid-2">
    <div class="card fade-in">
      <div style="font-size:2.5rem;margin-bottom:0.8rem">&#9889;</div>
      <div class="card-title">Continuous Integration</div>
      <div class="card-desc">Every code push automatically builds and tests the application. Bugs caught immediately — no more "it works on my machine" problems. Code is always in a deployable state.</div>
    </div>
    <div class="card fade-in">
      <div style="font-size:2.5rem;margin-bottom:0.8rem">&#128640;</div>
      <div class="card-title">Continuous Deployment</div>
      <div class="card-desc">After CI passes, the new version deploys automatically to production servers. Push code — users see it in 26 seconds. Zero manual steps, zero human error.</div>
    </div>
  </div>
  <div class="grid-3">
    <div class="card fade-in">
      <div style="font-size:2rem;margin-bottom:0.8rem">&#128552;</div>
      <div class="card-title">Without CI/CD</div>
      <div class="card-desc">Deployments take hours. Bugs discovered late. Manual server configuration. Teams move slowly with fear of breaking things.</div>
    </div>
    <div class="card fade-in">
      <div style="font-size:2rem;margin-bottom:0.8rem">&#9989;</div>
      <div class="card-title">With CI/CD</div>
      <div class="card-desc">Deployments take 26 seconds. Bugs caught instantly. Infrastructure as code. Teams ship with confidence multiple times a day.</div>
    </div>
    <div class="card fade-in">
      <div style="font-size:2rem;margin-bottom:0.8rem">&#127962;</div>
      <div class="card-title">Real World Usage</div>
      <div class="card-desc">Netflix deploys 100+ times daily. Amazon every 11 seconds. Swiggy, Zomato, Freshworks all use CI/CD pipelines like this one.</div>
    </div>
  </div>

  <!-- About Samuel -->
  <div class="card fade-in" style="max-width:500px">
    <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem">
      <div style="width:55px;height:55px;border-radius:50%;background:linear-gradient(135deg,{p1},{p2});display:flex;align-items:center;justify-content:center;font-size:1.4rem;flex-shrink:0">&#128104;&#8205;&#128187;</div>
      <div>
        <div style="font-size:1rem;font-weight:800">Samuel</div>
        <div style="font-size:11px;color:var(--muted)">Aspiring DevOps and Cloud Engineer</div>
        <div style="font-size:11px;color:var(--muted)">Final Year CSE · Prathyusha Engineering College</div>
      </div>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <a href="https://github.com/JOSESAMUEL14" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:5px;padding:6px 13px;border-radius:100px;background:var(--glass);border:1px solid var(--border);color:var(--muted);font-family:Space Mono,monospace;font-size:9px;text-decoration:none;transition:color 0.3s" onmouseover="this.style.color='#fff'" onmouseout="this.style.color=''"><i class="fa-brands fa-github"></i> GitHub</a>
      <a href="https://linkedin.com/in/samueld14" target="_blank" rel="noopener" style="display:inline-flex;align-items:center;gap:5px;padding:6px 13px;border-radius:100px;background:var(--glass);border:1px solid var(--border);color:var(--muted);font-family:Space Mono,monospace;font-size:9px;text-decoration:none;transition:color 0.3s" onmouseover="this.style.color='#fff'" onmouseout="this.style.color=''"><i class="fa-brands fa-linkedin"></i> LinkedIn</a>
      <a href="mailto:Josesamueld2005@gmail.com" style="display:inline-flex;align-items:center;gap:5px;padding:6px 13px;border-radius:100px;background:var(--glass);border:1px solid var(--border);color:var(--muted);font-family:Space Mono,monospace;font-size:9px;text-decoration:none;transition:color 0.3s" onmouseover="this.style.color='#fff'" onmouseout="this.style.color=''"><i class="fa-solid fa-envelope"></i> Email</a>
    </div>
  </div>
</div>
</div>

<!-- ═══════════ SECTION 3 — ARCHITECTURE ═══════════ -->
<div id="architecture" class="section">
  <div class="section-tag">System Design</div>
  <div class="sec-title fade-in"><span class="w">ARCHITECTURE</span><br><span class="a">DIAGRAM</span></div>
  <div class="sec-desc fade-in">How all components connect and communicate in this multi-cloud CI/CD system.</div>

  <div class="arch-diagram fade-in">
    <div class="arch-label">&#9658; Developer Workflow</div>
    <div class="arch-row">
      <div class="arch-box"><div class="arch-box-icon">&#128187;</div><div class="arch-box-name">Developer</div><div class="arch-box-desc">Writes code</div></div>
      <div class="arch-arrow">&#8594;</div>
      <div class="arch-box"><div class="arch-box-icon"><i class="fa-brands fa-github"></i></div><div class="arch-box-name">GitHub</div><div class="arch-box-desc">git push</div></div>
      <div class="arch-arrow">&#8594;</div>
      <div class="arch-box"><div class="arch-box-icon">&#9889;</div><div class="arch-box-name">GH Actions</div><div class="arch-box-desc">CI/CD trigger</div></div>
      <div class="arch-arrow">&#8594;</div>
      <div class="arch-box"><div class="arch-box-icon"><i class="fa-brands fa-docker"></i></div><div class="arch-box-name">Docker Build</div><div class="arch-box-desc">Image created</div></div>
      <div class="arch-arrow">&#8594;</div>
      <div class="arch-box"><div class="arch-box-icon">&#128055;</div><div class="arch-box-name">Docker Hub</div><div class="arch-box-desc">Registry</div></div>
    </div>
    <div class="arch-divider"></div>
    <div class="arch-label">&#9658; Cloud Deployment</div>
    <div class="arch-row">
      <div class="arch-box"><div class="arch-box-icon">&#128055;</div><div class="arch-box-name">Docker Hub</div><div class="arch-box-desc">Image pulled</div></div>
      <div class="arch-arrow">&#8594;</div>
      <div class="arch-box"><div class="arch-box-icon">&#9096;&#65039;</div><div class="arch-box-name">Kubernetes</div><div class="arch-box-desc">Orchestration</div></div>
      <div class="arch-arrow">&#8594;</div>
      <div class="arch-box"><div class="arch-box-icon"><i class="fa-brands fa-aws"></i></div><div class="arch-box-name">AWS EC2</div><div class="arch-box-desc">Mumbai</div></div>
      <div class="arch-arrow">+</div>
      <div class="arch-box"><div class="arch-box-icon">&#9729;&#65039;</div><div class="arch-box-name">Render</div><div class="arch-box-desc">24/7 hosting</div></div>
    </div>
    <div class="arch-divider"></div>
    <div class="arch-label">&#9658; Monitoring Stack</div>
    <div class="arch-row">
      <div class="arch-box"><div class="arch-box-icon">&#127959;&#65039;</div><div class="arch-box-name">Terraform</div><div class="arch-box-desc">IaC</div></div>
      <div class="arch-arrow">+</div>
      <div class="arch-box"><div class="arch-box-icon">&#128202;</div><div class="arch-box-name">Prometheus</div><div class="arch-box-desc">Metrics</div></div>
      <div class="arch-arrow">&#8594;</div>
      <div class="arch-box"><div class="arch-box-icon">&#128200;</div><div class="arch-box-name">Grafana</div><div class="arch-box-desc">Dashboards</div></div>
      <div class="arch-arrow">&#8594;</div>
      <div class="arch-box"><div class="arch-box-icon">&#128276;</div><div class="arch-box-name">Alerts</div><div class="arch-box-desc">Anomalies</div></div>
    </div>
  </div>

  <div class="grid-2">
    <div class="card fade-in"><div style="font-size:2rem;margin-bottom:0.8rem">&#128051;</div><div class="card-title">Containerisation</div><div class="card-desc">Flask app packaged in Docker with all dependencies. Runs identically on any machine — laptop or cloud server. No "works on my machine" issues.</div></div>
    <div class="card fade-in"><div style="font-size:2rem;margin-bottom:0.8rem">&#9096;&#65039;</div><div class="card-title">Orchestration</div><div class="card-desc">Kubernetes keeps 2 replicas running always. Auto-restarts crashed containers. Rolling updates ensure zero downtime during deployments.</div></div>
    <div class="card fade-in"><div style="font-size:2rem;margin-bottom:0.8rem">&#127959;&#65039;</div><div class="card-title">Infrastructure as Code</div><div class="card-desc">Terraform defines AWS infrastructure in code files. No manual clicking in AWS console — everything provisioned automatically and reproducibly.</div></div>
    <div class="card fade-in"><div style="font-size:2rem;margin-bottom:0.8rem">&#128202;</div><div class="card-title">Observability</div><div class="card-desc">Prometheus scrapes metrics every 15 seconds. Grafana live dashboards show CPU, memory, request rates. Problems detected before users notice.</div></div>
  </div>
</div>

<!-- ═══════════ SECTION 4 — TECH STACK ═══════════ -->
<div class="alt-bg">
<div id="techstack" class="section">
  <div class="section-tag">Tools and Technologies</div>
  <div class="sec-title fade-in"><span class="w">THE TECH</span><br><span class="a">STACK</span></div>
  <div class="sec-desc fade-in">8 industry-standard tools — each chosen because it is used by real companies in production environments worldwide.</div>
  <div class="grid-2">
    <div class="card fade-in"><div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem"><div style="width:44px;height:44px;border-radius:13px;background:rgba(36,150,237,0.15);border:1px solid rgba(36,150,237,0.3);display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0"><i class="fa-brands fa-docker" style="color:#2496ED"></i></div><div><div style="font-size:0.95rem;font-weight:800">Docker</div><div style="width:35px;height:2px;background:linear-gradient(90deg,#2496ED,transparent);margin-top:3px;border-radius:2px"></div></div></div><div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:0.5rem">Containerisation platform. Packages app and all dependencies into portable containers that run anywhere.</div><div style="font-size:10px;color:var(--muted)"><span style="color:#2496ED;font-weight:700">Why:</span> Industry standard. Every major company uses Docker.</div></div>
    <div class="card fade-in"><div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem"><div style="width:44px;height:44px;border-radius:13px;background:rgba(50,108,229,0.15);border:1px solid rgba(50,108,229,0.3);display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0"><i class="fa-solid fa-ship" style="color:#326CE5"></i></div><div><div style="font-size:0.95rem;font-weight:800">Kubernetes</div><div style="width:35px;height:2px;background:linear-gradient(90deg,#326CE5,transparent);margin-top:3px;border-radius:2px"></div></div></div><div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:0.5rem">Container orchestration. Manages, scales, and auto-heals containers across servers.</div><div style="font-size:10px;color:var(--muted)"><span style="color:#326CE5;font-weight:700">Why:</span> Most in-demand DevOps skill in 2025.</div></div>
    <div class="card fade-in"><div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem"><div style="width:44px;height:44px;border-radius:13px;background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0"><i class="fa-brands fa-github" style="color:#fff"></i></div><div><div style="font-size:0.95rem;font-weight:800">GitHub Actions</div><div style="width:35px;height:2px;background:linear-gradient(90deg,#fff,transparent);margin-top:3px;border-radius:2px"></div></div></div><div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:0.5rem">CI/CD automation built into GitHub. Runs pipelines automatically on every code push.</div><div style="font-size:10px;color:var(--muted)"><span style="color:#fff;font-weight:700">Why:</span> Free, integrated, used by millions of developers.</div></div>
    <div class="card fade-in"><div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem"><div style="width:44px;height:44px;border-radius:13px;background:rgba(123,66,188,0.15);border:1px solid rgba(123,66,188,0.3);display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0"><i class="fa-solid fa-layer-group" style="color:#7B42BC"></i></div><div><div style="font-size:0.95rem;font-weight:800">Terraform</div><div style="width:35px;height:2px;background:linear-gradient(90deg,#7B42BC,transparent);margin-top:3px;border-radius:2px"></div></div></div><div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:0.5rem">Infrastructure as Code. Defines and provisions cloud resources automatically.</div><div style="font-size:10px;color:var(--muted)"><span style="color:#7B42BC;font-weight:700">Why:</span> Most popular IaC tool. Works on any cloud provider.</div></div>
    <div class="card fade-in"><div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem"><div style="width:44px;height:44px;border-radius:13px;background:rgba(255,153,0,0.15);border:1px solid rgba(255,153,0,0.3);display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0"><i class="fa-brands fa-aws" style="color:#FF9900"></i></div><div><div style="font-size:0.95rem;font-weight:800">AWS EC2</div><div style="width:35px;height:2px;background:linear-gradient(90deg,#FF9900,transparent);margin-top:3px;border-radius:2px"></div></div></div><div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:0.5rem">Amazon Web Services virtual server. Runs the containerised app in Mumbai cloud region.</div><div style="font-size:10px;color:var(--muted)"><span style="color:#FF9900;font-weight:700">Why:</span> Largest cloud provider. Fundamental for cloud roles.</div></div>
    <div class="card fade-in"><div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem"><div style="width:44px;height:44px;border-radius:13px;background:rgba(230,82,44,0.15);border:1px solid rgba(230,82,44,0.3);display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0"><i class="fa-solid fa-chart-line" style="color:#E6522C"></i></div><div><div style="font-size:0.95rem;font-weight:800">Prometheus</div><div style="width:35px;height:2px;background:linear-gradient(90deg,#E6522C,transparent);margin-top:3px;border-radius:2px"></div></div></div><div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:0.5rem">Open source monitoring. Scrapes and stores metrics from applications every 15 seconds.</div><div style="font-size:10px;color:var(--muted)"><span style="color:#E6522C;font-weight:700">Why:</span> Industry standard for cloud-native monitoring.</div></div>
    <div class="card fade-in"><div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem"><div style="width:44px;height:44px;border-radius:13px;background:rgba(244,104,0,0.15);border:1px solid rgba(244,104,0,0.3);display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0"><i class="fa-solid fa-chart-bar" style="color:#F46800"></i></div><div><div style="font-size:0.95rem;font-weight:800">Grafana</div><div style="width:35px;height:2px;background:linear-gradient(90deg,#F46800,transparent);margin-top:3px;border-radius:2px"></div></div></div><div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:0.5rem">Visualisation platform. Creates beautiful live dashboards from Prometheus data.</div><div style="font-size:10px;color:var(--muted)"><span style="color:#F46800;font-weight:700">Why:</span> Most popular open source dashboard tool worldwide.</div></div>
    <div class="card fade-in"><div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem"><div style="width:44px;height:44px;border-radius:13px;background:rgba(55,118,171,0.15);border:1px solid rgba(55,118,171,0.3);display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0"><i class="fa-brands fa-python" style="color:#3776AB"></i></div><div><div style="font-size:0.95rem;font-weight:800">Python Flask</div><div style="width:35px;height:2px;background:linear-gradient(90deg,#3776AB,transparent);margin-top:3px;border-radius:2px"></div></div></div><div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:0.5rem">Lightweight web framework powering the dashboard with REST API endpoints.</div><div style="font-size:10px;color:var(--muted)"><span style="color:#3776AB;font-weight:700">Why:</span> Simple, fast, perfect for microservices and APIs.</div></div>
  </div>
</div>
</div>

<!-- ═══════════ SECTION 5 — PIPELINE ═══════════ -->
<div id="pipeline-section" class="section">
  <div class="section-tag">How It Works</div>
  <div class="sec-title fade-in"><span class="w">THE</span><br><span class="a">PIPELINE</span></div>
  <div class="sec-desc fade-in">From writing a single line of code to seeing it live in production — every step that happens automatically in under 26 seconds.</div>

  <div class="pipe-step fade-in"><div class="pipe-icon">&#128187;</div><div class="pipe-content"><div class="pipe-title">Developer Writes Code</div><div class="pipe-desc">Developer makes changes to the Flask application — adding features, fixing bugs, or updating the UI. Code lives in GitHub.</div><div class="pipe-tag">Local Development</div></div><div class="pipe-num">01</div></div>
  <div class="pipe-step fade-in"><div class="pipe-icon"><i class="fa-brands fa-github"></i></div><div class="pipe-content"><div class="pipe-title">Push to GitHub</div><div class="pipe-desc">Developer runs git push origin main. This single action triggers the entire automated pipeline instantly with no manual intervention.</div><div class="pipe-tag">GitHub</div></div><div class="pipe-num">02</div></div>
  <div class="pipe-step fade-in"><div class="pipe-icon">&#9889;</div><div class="pipe-content"><div class="pipe-title">GitHub Actions Triggers</div><div class="pipe-desc">GitHub detects the push and starts the CI/CD workflow automatically. A virtual Ubuntu server spins up on GitHub's infrastructure for free.</div><div class="pipe-tag">GitHub Actions</div></div><div class="pipe-num">03</div></div>
  <div class="pipe-step fade-in"><div class="pipe-icon"><i class="fa-brands fa-docker"></i></div><div class="pipe-content"><div class="pipe-title">Docker Image Built</div><div class="pipe-desc">GitHub Actions reads the Dockerfile and builds a new Docker image with the updated app. Tagged with unique commit SHA — every version is traceable.</div><div class="pipe-tag">Docker</div></div><div class="pipe-num">04</div></div>
  <div class="pipe-step fade-in"><div class="pipe-icon">&#128055;</div><div class="pipe-content"><div class="pipe-title">Image Pushed to Docker Hub</div><div class="pipe-desc">The built image is pushed to Docker Hub registry — making it available to any server worldwide as josesamuel14/multicloud-app:latest.</div><div class="pipe-tag">Docker Hub</div></div><div class="pipe-num">05</div></div>
  <div class="pipe-step fade-in"><div class="pipe-icon">&#9096;&#65039;</div><div class="pipe-content"><div class="pipe-title">Kubernetes Rolling Update</div><div class="pipe-desc">Kubernetes pulls the new image and performs a Rolling Update — gradually replacing old containers. Zero downtime. Users never notice.</div><div class="pipe-tag">Kubernetes</div></div><div class="pipe-num">06</div></div>
  <div class="pipe-step fade-in"><div class="pipe-icon"><i class="fa-brands fa-aws"></i></div><div class="pipe-content"><div class="pipe-title">Live on AWS and Render</div><div class="pipe-desc">New version is live on AWS EC2 Mumbai and Render simultaneously. Total time from git push to live: 26 seconds. Every time. Automatically.</div><div class="pipe-tag">AWS + Render</div></div><div class="pipe-num">07</div></div>
  <div class="pipe-step fade-in"><div class="pipe-icon">&#128202;</div><div class="pipe-content"><div class="pipe-title">Prometheus Monitors</div><div class="pipe-desc">Prometheus scrapes metrics every 15 seconds. Grafana shows live dashboards. Engineers know about problems before users do.</div><div class="pipe-tag">Prometheus + Grafana</div></div><div class="pipe-num">08</div></div>

  <div class="card fade-in" style="text-align:center;padding:2rem;background:linear-gradient(135deg,rgba(124,58,237,0.1),rgba(6,182,212,0.1));border-color:rgba(124,58,237,0.2)">
    <div style="font-size:2.5rem;margin-bottom:0.6rem">&#9889;</div>
    <div style="font-size:1.3rem;font-weight:800;margin-bottom:0.4rem">Total Time: 26 Seconds</div>
    <div style="font-size:13px;color:var(--muted)">From git push to live in production — fully automated, zero manual steps, zero downtime</div>
  </div>
</div>

<!-- ═══════════ SECTION 6 — LIVE DEMO ═══════════ -->
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
    <div class="demo-card-desc">Fetches real-time stats from the application — total HTTP requests served, current uptime, and system status. Data from Prometheus metrics.</div>
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

<!-- ═══════════ SECTION 7 — CONTACT ═══════════ -->
<div id="contact" class="section">
  <div class="section-tag">Get In Touch</div>
  <div class="sec-title fade-in"><span class="w">CONTACT</span><br><span class="a">SAMUEL</span></div>
  <div class="sec-desc fade-in">Open to DevOps and Cloud Engineering opportunities. Let's connect!</div>

  <div class="contact-grid fade-in">
    <a href="mailto:Josesamueld2005@gmail.com" class="contact-card">
      <div class="contact-icon" style="background:rgba(124,58,237,0.15);border:1px solid rgba(124,58,237,0.3)">
        <i class="fa-solid fa-envelope" style="color:{p1}"></i>
      </div>
      <div class="contact-label">Email</div>
      <div class="contact-value">Josesamueld2005@gmail.com</div>
      <div style="font-size:10px;color:var(--muted);margin-top:4px">Click to open mail</div>
    </a>
    <a href="https://github.com/JOSESAMUEL14" target="_blank" rel="noopener" class="contact-card">
      <div class="contact-icon" style="background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12)">
        <i class="fa-brands fa-github" style="color:#fff"></i>
      </div>
      <div class="contact-label">GitHub</div>
      <div class="contact-value">JOSESAMUEL14</div>
      <div style="font-size:10px;color:var(--muted);margin-top:4px">View all projects</div>
    </a>
    <a href="https://linkedin.com/in/samueld14" target="_blank" rel="noopener" class="contact-card">
      <div class="contact-icon" style="background:rgba(10,102,194,0.15);border:1px solid rgba(10,102,194,0.3)">
        <i class="fa-brands fa-linkedin" style="color:#0A66C2"></i>
      </div>
      <div class="contact-label">LinkedIn</div>
      <div class="contact-value">samueld14</div>
      <div style="font-size:10px;color:var(--muted);margin-top:4px">Connect with me</div>
    </a>
  </div>

  <div class="card fade-in" style="text-align:center;padding:2rem;background:linear-gradient(135deg,rgba(124,58,237,0.08),rgba(6,182,212,0.08));border-color:rgba(124,58,237,0.15)">
    <div style="font-size:1rem;font-weight:800;margin-bottom:0.5rem">Available for Internship &amp; Full-Time Roles</div>
    <div style="font-size:13px;color:var(--muted);margin-bottom:1.2rem">DevOps Engineer · Cloud Engineer · SRE · Platform Engineer</div>
    <a href="mailto:Josesamueld2005@gmail.com" class="cta-btn cta-primary" style="display:inline-flex">
      <i class="fa-solid fa-paper-plane"></i> Send me an Email
    </a>
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
    <a href="mailto:Josesamueld2005@gmail.com">Contact</a>
    <br><br>
    <span style="font-size:9px;opacity:0.5">MultiCloud CI/CD · Docker · Kubernetes · GitHub Actions · Terraform · AWS · Prometheus · Grafana</span>
  </div>
</footer>

<script>
// ── MOBILE NAV ──
function toggleMobile() {{
  var n = document.getElementById('mobileNav');
  n.classList.toggle('open');
}}
function closeMobile() {{
  document.getElementById('mobileNav').classList.remove('open');
}}

// ── SCROLL NAVIGATION ──
function goTo(id) {{
  var el = document.getElementById(id);
  if (el) {{
    var top = el.getBoundingClientRect().top + window.pageYOffset - 60;
    window.scrollTo({{top: top, behavior: 'smooth'}});
  }}
}}

// ── CLOCK ──
function tick() {{
  var n = new Date();
  document.getElementById('clk').textContent =
    String(n.getHours()).padStart(2,'0') + ':' +
    String(n.getMinutes()).padStart(2,'0') + ':' +
    String(n.getSeconds()).padStart(2,'0');
}}
setInterval(tick, 1000); tick();

// ── LIVE METRICS ──
function updateMetrics() {{
  fetch('/stats')
    .then(function(r) {{ return r.json(); }})
    .then(function(d) {{
      document.getElementById('req-count').textContent = d.total_requests || '0';
      document.getElementById('uptime').textContent = d.uptime || '--';
      document.getElementById('health-val').textContent = d.status || '--';
    }})
    .catch(function() {{}});
}}
setInterval(updateMetrics, 5000); updateMetrics();

// ── DEPLOY MODAL ──
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
  s.textContent = 'Triggering pipeline...'; s.style.color = '#eab308';
  fetch('/deploy', {{method:'POST',headers:{{'Content-Type':'application/json'}}}})
    .then(function(r) {{ return r.json(); }})
    .then(function(d) {{
      s.textContent = d.success ? '&#10003; Pipeline triggered! Check GitHub Actions.' : '&#10007; ' + d.message;
      s.style.color = d.success ? '#10b981' : '#ef4444';
    }})
    .catch(function(e) {{ s.textContent = '&#10007; ' + e.message; s.style.color = '#ef4444'; }});
}}

// ── HEALTH CHECK ──
function checkHealth() {{
  var box = document.getElementById('health-response');
  box.className = 'response-box show'; box.textContent = 'Fetching...';
  fetch('/health')
    .then(function(r) {{ return r.json(); }})
    .then(function(d) {{ box.textContent = JSON.stringify(d, null, 2); }})
    .catch(function(e) {{ box.textContent = 'Error: ' + e.message; }});
}}

// ── LIVE STATS ──
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

// ── COUNTER ANIMATION ──
function animateCounter(id, end, duration) {{
  var el = document.getElementById(id);
  if (!el) return;
  var start = 0, step = end / (duration / 16);
  var timer = setInterval(function() {{
    start += step;
    if (start >= end) {{ start = end; clearInterval(timer); }}
    el.textContent = Math.floor(start);
  }}, 16);
}}

// ── TERMINAL ANIMATION ──
var termLines = document.querySelectorAll('.t-line');
var termStarted = false;
function runTerminal() {{
  if (termStarted) return;
  termStarted = true;
  var delays = [0, 400, 900, 1400, 1900, 2500, 3100, 3700, 4000, 4800, 5400];
  termLines.forEach(function(line, i) {{
    setTimeout(function() {{ line.classList.add('show'); }}, delays[i] || i * 500);
  }});
  // stop spinner when deploy line shows
  setTimeout(function() {{
    var spin = document.getElementById('term-spin');
    if (spin) spin.style.animation = 'none';
    if (spin) spin.textContent = '&#10003;';
    if (spin) spin.style.color = '#3fb950';
  }}, 4600);
  // loop every 8 seconds
  setTimeout(function() {{
    termLines.forEach(function(line) {{ line.classList.remove('show'); }});
    termStarted = false;
    var spin = document.getElementById('term-spin');
    if (spin) {{ spin.style.animation = ''; spin.textContent = '&#9702;'; spin.style.color = ''; }}
    setTimeout(runTerminal, 600);
  }}, 9000);
}}

// ── SCROLL ANIMATIONS ──
var obs = new IntersectionObserver(function(entries) {{
  entries.forEach(function(e) {{
    if (e.isIntersecting) {{
      e.target.classList.add('visible');
      // trigger terminal when about section is visible
      if (e.target.closest && e.target.closest('#about')) runTerminal();
      if (e.target.id === 'counter-deploy') animateCounter('counter-deploy', 47, 1500);
    }}
  }});
}}, {{threshold: 0.1}});
document.querySelectorAll('.fade-in').forEach(function(el) {{ obs.observe(el); }});

// trigger terminal when terminal wrap comes into view
var termWrap = document.querySelector('.terminal-wrap');
if (termWrap) {{
  var termObs = new IntersectionObserver(function(entries) {{
    if (entries[0].isIntersecting) {{ runTerminal(); termObs.disconnect(); }}
  }}, {{threshold: 0.3}});
  termObs.observe(termWrap);
}}

// ── HEX GRID BACKGROUND ──
var cv = document.getElementById('cv');
var ctx = cv.getContext('2d');
var W, H, t = 0;
function rsz() {{ W = cv.width = window.innerWidth; H = cv.height = window.innerHeight; }}
rsz(); window.addEventListener('resize', rsz);
var S = 26;
function draw() {{
  ctx.fillStyle = '#06061a'; ctx.fillRect(0,0,W,H); t += 0.05;
  var rows = Math.ceil(H/(S*1.5))+2, cols = Math.ceil(W/(S*1.73))+2;
  for (var r=0; r<rows; r++) {{
    for (var c=0; c<cols; c++) {{
      var x = c*S*1.73 + (r%2)*S*0.866, y = r*S*1.5;
      var v = (Math.sin(t+c*0.45+r*0.65)+Math.sin(t*0.85+c*0.75-r*0.45)+Math.sin(t*1.2-c*0.3+r*0.8))/3;
      var a = 0.05+v*0.22;
      ctx.beginPath();
      for (var i=0; i<6; i++) {{
        var ang = Math.PI/180*(60*i-30);
        if (i===0) ctx.moveTo(x+(S-1)*Math.cos(ang), y+(S-1)*Math.sin(ang));
        else ctx.lineTo(x+(S-1)*Math.cos(ang), y+(S-1)*Math.sin(ang));
      }}
      ctx.closePath();
      ctx.strokeStyle = 'rgba(6,182,212,'+Math.max(0.04,a)+')'; ctx.lineWidth = 0.9; ctx.stroke();
      if (v>0.45) {{ ctx.fillStyle='rgba(124,58,237,'+(v-0.45)*0.28+')'; ctx.fill(); }}
      if (v>0.72) {{ ctx.fillStyle='rgba(6,182,212,'+(v-0.72)*0.55+')'; ctx.fill(); }}
      if (v>0.88) {{ ctx.fillStyle='rgba(255,255,255,'+(v-0.88)*0.15+')'; ctx.fill(); }}
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
    return jsonify({{
        "status": "healthy",
        "cloud": os.getenv("CLOUD_PROVIDER", "local"),
        "region": os.getenv("CLOUD_REGION", "local"),
        "uptime": get_uptime(),
        "hostname": socket.gethostname(),
        "python": platform.python_version()
    }}), 200


@app.route("/stats")
def stats():
    try:
        metrics_data = requests.get("http://localhost:5000/metrics", timeout=2).text
        total = 0
        for line in metrics_data.split('\n'):
            if 'flask_http_request_total' in line and not line.startswith('#'):
                try: total += float(line.split(' ')[-1])
                except: pass
    except:
        total = 0
    return jsonify({{
        "status": "HEALTHY",
        "total_requests": int(total),
        "uptime": get_uptime(),
        "cloud": os.getenv("CLOUD_PROVIDER", "local"),
        "hostname": socket.gethostname()
    }})


@app.route("/deploy", methods=["POST"])
def deploy():
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        return jsonify({{"success": False, "message": "GITHUB_TOKEN not configured"}})
    try:
        r = requests.post(
            "https://api.github.com/repos/JOSESAMUEL14/multicloud-cicd/dispatches",
            headers={{
                "Authorization": "Bearer " + token,
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            }},
            json={{"event_type": "manual-deploy"}},
            timeout=10
        )
        if r.status_code == 204:
            return jsonify({{"success": True, "message": "Pipeline triggered!"}})
        return jsonify({{"success": False, "message": "GitHub API error: " + str(r.status_code)}})
    except Exception as e:
        return jsonify({{"success": False, "message": str(e)}})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)