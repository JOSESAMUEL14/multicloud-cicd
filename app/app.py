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
        "aws":    {"p1":"#FF9900","p2":"#FF6B35","p3":"#FFD700","label":"Amazon Web Services","short":"AWS"},
        "gcp":    {"p1":"#4285F4","p2":"#34A853","p3":"#FBBC05","label":"Google Cloud Platform","short":"GCP"},
        "render": {"p1":"#7C3AED","p2":"#06B6D4","p3":"#EC4899","label":"Render Cloud","short":"RENDER"},
        "local":  {"p1":"#7C3AED","p2":"#06B6D4","p3":"#EC4899","label":"Local Kubernetes","short":"LOCAL"}
    }
    t = themes.get(cloud.lower(), themes["local"])
    cloud_icon = "<i class='fa-brands fa-aws'></i>" if cloud.lower()=="aws" else "<i class='fa-brands fa-google'></i>" if cloud.lower()=="gcp" else "<i class='fa-solid fa-cloud'></i>"
    cloud_label = "AWS" if cloud.lower()=="aws" else "GCP" if cloud.lower()=="gcp" else "Cloud"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MultiCloud CI/CD — Samuel DevOps</title>
<link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;600;700;800;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--p1:{t['p1']};--p2:{t['p2']};--bg:#06061a;--glass:rgba(255,255,255,0.04);--border:rgba(255,255,255,0.08);--muted:rgba(255,255,255,0.38)}}
html{{scroll-behavior:smooth}}
body{{font-family:"Exo 2",sans-serif;background:var(--bg);color:#fff;overflow-x:hidden}}
#cv{{position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}}
.vig{{position:fixed;inset:0;z-index:1;pointer-events:none;background:radial-gradient(ellipse at 50% 50%,transparent 25%,rgba(6,6,26,0.7) 100%)}}

/* NAV */
nav{{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:0.8rem 2rem;background:rgba(6,6,26,0.85);backdrop-filter:blur(20px);border-bottom:1px solid var(--border)}}
.nav-brand{{font-family:"Space Mono",monospace;font-size:13px;font-weight:700;letter-spacing:2px;color:#fff}}
.nav-brand span{{color:var(--p1)}}
.nav-links{{display:flex;gap:20px}}
.nav-link{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);text-decoration:none;transition:color 0.3s;cursor:pointer}}
.nav-link:hover{{color:#fff}}
.nav-right{{display:flex;align-items:center;gap:10px}}
.nav-github{{color:var(--muted);font-size:18px;transition:color 0.3s;text-decoration:none}}
.nav-github:hover{{color:#fff}}
.live-pill{{display:flex;align-items:center;gap:6px;padding:5px 12px;border-radius:100px;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;color:#10b981}}
.live-dot{{width:6px;height:6px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;animation:blink 2s infinite}}
@keyframes blink{{0%,100%{{opacity:1}}50%{{opacity:0.2}}}}

/* SECTIONS */
.section{{position:relative;z-index:10;padding:5rem 2rem 4rem;max-width:960px;margin:0 auto}}
.section-tag{{display:inline-flex;align-items:center;gap:8px;font-family:"Space Mono",monospace;font-size:9px;letter-spacing:3px;text-transform:uppercase;color:var(--muted);padding:5px 14px;border-radius:100px;border:1px solid var(--border);margin-bottom:1.2rem}}
.section-title{{font-size:clamp(2rem,5vw,3.8rem);font-weight:900;letter-spacing:-1px;line-height:0.9;margin-bottom:1rem}}
.section-title .w{{color:#fff}}
.section-title .a{{background:linear-gradient(135deg,var(--p1),var(--p2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.section-desc{{font-size:0.95rem;color:var(--muted);line-height:1.8;max-width:580px;margin-bottom:2.5rem}}
.divider{{width:100%;height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:3rem 0}}

/* CARDS */
.grid-2{{display:grid;grid-template-columns:1fr 1fr;gap:1.2rem;margin-bottom:2rem}}
.grid-3{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.2rem;margin-bottom:2rem}}
.card{{background:var(--glass);border:1px solid var(--border);border-radius:18px;padding:1.4rem;backdrop-filter:blur(20px);transition:all 0.4s cubic-bezier(.16,1,.3,1)}}
.card:hover{{transform:translateY(-5px);border-color:rgba(255,255,255,0.15);box-shadow:0 20px 50px rgba(0,0,0,0.5)}}
.card-icon{{font-size:1.8rem;margin-bottom:0.8rem}}
.card-title{{font-size:1rem;font-weight:700;margin-bottom:0.4rem;color:#fff}}
.card-desc{{font-size:0.82rem;color:var(--muted);line-height:1.6}}

/* FADE IN */
.fade-in{{opacity:0;transform:translateY(28px);transition:all 0.7s cubic-bezier(.16,1,.3,1)}}
.fade-in.visible{{opacity:1;transform:translateY(0)}}

/* PIPELINE STEPS */
.pipe-step{{display:flex;gap:1.2rem;margin-bottom:1.8rem;align-items:flex-start}}
.pipe-num{{font-family:"Space Mono",monospace;font-size:2.5rem;font-weight:700;color:rgba(255,255,255,0.07);min-width:70px;line-height:1}}
.pipe-content{{flex:1;padding-top:6px}}
.pipe-title{{font-size:1.1rem;font-weight:800;margin-bottom:4px;background:linear-gradient(135deg,var(--p1),var(--p2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.pipe-desc{{font-size:0.85rem;color:var(--muted);line-height:1.6}}
.pipe-tag{{display:inline-block;font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;padding:3px 10px;border-radius:100px;background:rgba(124,58,237,0.15);border:1px solid rgba(124,58,237,0.3);color:var(--p1);margin-top:6px}}

/* ARCH */
.arch-diagram{{background:var(--glass);border:1px solid var(--border);border-radius:18px;padding:1.5rem;margin-bottom:2rem}}
.arch-row{{display:flex;align-items:center;justify-content:center;gap:0;flex-wrap:wrap;margin-bottom:1.2rem}}
.arch-box{{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);border-radius:12px;padding:0.8rem 1rem;text-align:center;min-width:90px;transition:all 0.3s}}
.arch-box:hover{{background:rgba(124,58,237,0.15);border-color:rgba(124,58,237,0.4);transform:translateY(-3px)}}
.arch-box-icon{{font-size:1.3rem;margin-bottom:4px}}
.arch-box-name{{font-size:10px;font-weight:700;color:#fff}}
.arch-box-desc{{font-size:8px;color:var(--muted);margin-top:2px}}
.arch-arrow{{font-size:1.2rem;color:rgba(255,255,255,0.2);padding:0 6px;margin-bottom:24px}}
.arch-label{{font-family:"Space Mono",monospace;font-size:8px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);text-align:center;margin-bottom:0.8rem}}
.arch-divider{{width:100%;height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:1rem 0}}

/* TOOL CARDS */
.tool-card{{background:var(--glass);border:1px solid var(--border);border-radius:16px;padding:1.2rem;transition:all 0.3s}}
.tool-card:hover{{transform:translateY(-4px);border-color:var(--p1)}}

/* DASHBOARD SECTION */
.dash-wrap{{position:relative;z-index:10;min-height:100vh;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:5rem 1.2rem 2rem}}
.pill-badge{{display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);backdrop-filter:blur(16px);padding:6px 18px;border-radius:100px;font-family:"Space Mono",monospace;font-size:9px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-bottom:1.5rem}}
.pill-dot{{width:7px;height:7px;border-radius:50%;background:var(--p1);box-shadow:0 0 10px var(--p1);animation:blink 2s infinite}}
.hero-eye{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:4px;text-transform:uppercase;color:var(--muted);margin-bottom:0.5rem;display:flex;align-items:center;justify-content:center;gap:10px}}
.hero-eye::before,.hero-eye::after{{content:"";width:35px;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.2))}}
.hero-eye::after{{background:linear-gradient(90deg,rgba(255,255,255,0.2),transparent)}}
h1{{font-size:clamp(2.5rem,6vw,4.5rem);font-weight:900;letter-spacing:-1px;line-height:0.92;margin-bottom:0.6rem;text-align:center}}
h1 .w{{color:#fff}}
h1 .a{{background:linear-gradient(135deg,var(--p1),var(--p2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.hero-sub{{font-family:"Space Mono",monospace;font-size:9px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:var(--muted);display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap;margin-bottom:0.5rem}}
.hero-dot{{width:3px;height:3px;border-radius:50%;background:var(--p1);opacity:0.5}}

/* SCROLL CTA */
.scroll-cta{{display:flex;gap:10px;justify-content:center;margin:1.2rem 0;flex-wrap:wrap}}
.cta-btn{{display:inline-flex;align-items:center;gap:7px;padding:8px 18px;border-radius:100px;font-family:"Space Mono",monospace;font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;text-decoration:none;transition:all 0.3s;border:none;cursor:pointer}}
.cta-btn:hover{{transform:translateY(-3px)}}
.cta-primary{{background:linear-gradient(135deg,var(--p1),var(--p2));color:#fff;box-shadow:0 4px 16px rgba(124,58,237,0.3)}}
.cta-outline{{background:var(--glass);border:1px solid var(--border);color:var(--muted)}}

/* PIPELINE STRIP */
.pipeline{{width:100%;max-width:860px;background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);border-radius:18px;padding:1rem 1.5rem;backdrop-filter:blur(30px);display:flex;align-items:center;justify-content:space-between;position:relative;margin-bottom:1rem}}
.pipeline::before{{content:"PIPELINE";position:absolute;top:7px;left:14px;font-family:"Space Mono",monospace;font-size:7px;font-weight:700;letter-spacing:3px;color:rgba(255,255,255,0.1)}}
.pstep{{display:flex;flex-direction:column;align-items:center;gap:6px;flex:1}}
.p-icon{{width:46px;height:46px;border-radius:13px;background:transparent;border:2px solid var(--p1);display:flex;align-items:center;justify-content:center;font-size:17px;transition:all 0.4s;box-shadow:0 0 10px color-mix(in srgb,var(--p1) 25%,transparent)}}
.p-icon:hover{{transform:translateY(-5px);box-shadow:0 0 22px color-mix(in srgb,var(--p1) 55%,transparent);border-color:var(--p2)}}
.p-icon i{{font-size:18px;color:#fff}}
.p-icon svg{{width:20px;height:20px}}
.p-label{{font-family:"Space Mono",monospace;font-size:7px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted)}}
.pconn{{flex:1;display:flex;align-items:center;padding-bottom:22px}}
.pline{{width:100%;height:1.5px;background:linear-gradient(90deg,var(--p1),var(--p2));opacity:0.2;position:relative;overflow:hidden;border-radius:2px}}
.pline::after{{content:"";position:absolute;top:0;left:-50%;width:30%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,1),transparent);animation:sweep 2s linear infinite}}
@keyframes sweep{{to{{left:150%}}}}

/* CARDS GRID */
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
.dcard-value{{font-size:0.95rem;font-weight:800;background:linear-gradient(135deg,#e2e8f0,#ffffff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.1}}
.dcard-sub{{font-size:8px;color:rgba(255,255,255,0.2)}}
.dcard-live{{font-size:8px;color:#10b981;font-weight:600}}

/* ACTIONS */
.actions{{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;width:100%;max-width:860px}}
.btn-action{{display:inline-flex;align-items:center;gap:7px;padding:9px 16px;border-radius:100px;font-family:"Space Mono",monospace;font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border:none;cursor:pointer;transition:all 0.3s;text-decoration:none}}
.btn-action:hover{{transform:translateY(-3px)}}
.btn-deploy{{background:linear-gradient(135deg,var(--p1),var(--p2));color:#fff;box-shadow:0 4px 16px rgba(124,58,237,0.3)}}
.btn-github{{background:var(--glass);border:1px solid var(--border);color:#fff}}
.btn-health{{background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);color:#10b981}}
.btn-metrics{{background:rgba(234,179,8,0.1);border:1px solid rgba(234,179,8,0.25);color:#eab308}}
.status-bar{{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:center;width:100%;max-width:860px;margin-top:0.8rem}}
.chip{{display:inline-flex;align-items:center;gap:7px;padding:7px 14px;border-radius:100px;font-family:"Space Mono",monospace;font-size:8px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;backdrop-filter:blur(16px);transition:all 0.3s}}
.chip-green{{background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);color:#10b981}}
.chip-white{{background:var(--glass);border:1px solid var(--border);color:rgba(255,255,255,0.7)}}
.chip-mono{{background:var(--glass);border:1px solid var(--border);color:var(--muted)}}

/* MODAL */
.modal{{display:none;position:fixed;inset:0;z-index:200;align-items:center;justify-content:center;background:rgba(0,0,0,0.7);backdrop-filter:blur(10px)}}
.modal.show{{display:flex}}
.modal-box{{background:#0d0d1a;border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:2rem;max-width:400px;width:90%;text-align:center}}
.modal-title{{font-size:1.2rem;font-weight:800;margin-bottom:0.5rem}}
.modal-sub{{font-size:12px;color:var(--muted);margin-bottom:1.5rem;line-height:1.6}}
.modal-btns{{display:flex;gap:10px;justify-content:center}}
.modal-btn{{padding:10px 24px;border-radius:100px;font-size:11px;font-weight:700;cursor:pointer;border:none;transition:all 0.3s;font-family:"Space Mono",monospace}}
.modal-confirm{{background:linear-gradient(135deg,var(--p1),var(--p2));color:#fff}}
.modal-cancel{{background:rgba(255,255,255,0.08);color:#fff;border:1px solid rgba(255,255,255,0.15)}}

@media(max-width:640px){{
  .cards{{grid-template-columns:1fr 1fr}}
  .pipeline{{padding:0.8rem 0.8rem}}
  .p-icon{{width:36px;height:36px}}
  h1{{font-size:2.2rem}}
  .nav-links{{display:none}}
  .grid-2,.grid-3{{grid-template-columns:1fr}}
}}
</style>
</head>
<body>
<canvas id="cv"></canvas>
<div class="vig"></div>

<!-- NAV -->
<nav>
  <div class="nav-brand">SAMUEL<span>/</span>DEVOPS</div>
  <div class="nav-links">
    <a class="nav-link" onclick="scrollTo('dashboard')">Home</a>
    <a class="nav-link" onclick="scrollTo('about')">About</a>
    <a class="nav-link" onclick="scrollTo('architecture')">Architecture</a>
    <a class="nav-link" onclick="scrollTo('techstack')">Tech Stack</a>
    <a class="nav-link" onclick="scrollTo('pipeline-section')">Pipeline</a>
    <a class="nav-link" onclick="scrollTo('demo')">Demo</a>
  </div>
  <div class="nav-right">
    <a href="https://github.com/JOSESAMUEL14/multicloud-cicd" target="_blank" class="nav-github"><i class="fa-brands fa-github"></i></a>
    <div class="live-pill"><span class="live-dot"></span>LIVE</div>
  </div>
</nav>

<!-- MODAL -->
<div class="modal" id="deployModal">
  <div class="modal-box">
    <div class="modal-title">🚀 Trigger Deployment</div>
    <div class="modal-sub">This will trigger a real GitHub Actions pipeline run!</div>
    <div class="modal-btns">
      <button class="modal-btn modal-confirm" onclick="confirmDeploy()">Deploy Now</button>
      <button class="modal-btn modal-cancel" onclick="closeModal()">Cancel</button>
    </div>
    <div id="deploy-status" style="margin-top:1rem;font-size:11px;color:var(--muted)"></div>
  </div>
</div>

<!-- ═══════════════════════════════════════ -->
<!-- SECTION 1 — DASHBOARD (HOME)           -->
<!-- ═══════════════════════════════════════ -->
<div id="dashboard" class="dash-wrap">
  <div class="pill-badge"><span class="pill-dot"></span>{t['short']} &nbsp;·&nbsp; {t['label']} &nbsp;·&nbsp; Live</div>
  <div class="hero-eye">Multi · Cloud · Infrastructure</div>
  <h1><span class="w">MULTI</span><span class="a">CLOUD</span><br><span class="w">CI</span><span class="a">/CD</span></h1>
  <div class="hero-sub">Kubernetes<span class="hero-dot"></span>Docker<span class="hero-dot"></span>GitHub Actions<span class="hero-dot"></span>Terraform<span class="hero-dot"></span>AWS</div>
  <div class="scroll-cta">
    <button class="cta-btn cta-primary" onclick="scrollTo('about')"><i class="fa-solid fa-circle-info"></i> Learn More</button>
    <button class="cta-btn cta-outline" onclick="scrollTo('demo')"><i class="fa-solid fa-rocket"></i> Live Demo</button>
    <a href="https://github.com/JOSESAMUEL14/multicloud-cicd" target="_blank" class="cta-btn cta-outline"><i class="fa-brands fa-github"></i> GitHub</a>
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
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-solid fa-microchip"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Requests</div><div class="dcard-value" id="req-count">--</div><div class="dcard-live">↻ live</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-solid fa-clock"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Uptime</div><div class="dcard-value" id="uptime">--</div><div class="dcard-live">↻ live</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-brands fa-docker"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Container</div><div class="dcard-value">Docker</div><div class="dcard-sub">Registry</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-brands fa-python"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Python</div><div class="dcard-value">{python_ver}</div><div class="dcard-sub">Runtime</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-solid fa-circle-nodes"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Replicas</div><div class="dcard-value">2 / 2</div><div class="dcard-sub">Healthy</div></div>
    <div class="dcard"><div class="dcard-top"><div class="dcard-icon"><i class="fa-solid fa-heart-pulse"></i></div><div class="dcard-ping"></div></div><div class="dcard-label">Health</div><div class="dcard-value" id="health-val">--</div><div class="dcard-live">↻ live</div></div>
  </div>

  <div class="actions">
    <button class="btn-action btn-deploy" onclick="showDeploy()"><i class="fa-solid fa-rocket"></i> Trigger Deploy</button>
    <a href="https://github.com/{github_repo}/actions" target="_blank" class="btn-action btn-github"><i class="fa-brands fa-github"></i> View Pipeline</a>
    <a href="/health" target="_blank" class="btn-action btn-health"><i class="fa-solid fa-heart-pulse"></i> Health Check</a>
    <a href="/metrics" target="_blank" class="btn-action btn-metrics"><i class="fa-solid fa-chart-bar"></i> Metrics</a>
  </div>

  <div class="status-bar">
    <div class="chip chip-green"><span style="width:6px;height:6px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;animation:blink 1.5s infinite;display:inline-block"></span>All Systems Operational</div>
    <div class="chip chip-white"><i class="fa-solid fa-bolt"></i> Auto-Deploy Active</div>
    <div class="chip chip-mono" id="clk">--:--:--</div>
  </div>
</div>

<!-- ═══════════════════════════════════════ -->
<!-- SECTION 2 — ABOUT                      -->
<!-- ═══════════════════════════════════════ -->
<div style="background:rgba(255,255,255,0.015);border-top:1px solid var(--border);border-bottom:1px solid var(--border)">
<div id="about" class="section">
  <div class="section-tag">About This Project</div>
  <div class="section-title fade-in"><span class="w">WHAT IS</span><br><span class="a">CI/CD?</span></div>
  <div class="section-desc fade-in">CI/CD stands for Continuous Integration and Continuous Deployment — the method used by Netflix, Amazon, Google and every modern tech company to ship software fast and reliably.</div>
  <div class="grid-2">
    <div class="card fade-in"><div class="card-icon">⚡</div><div class="card-title">Continuous Integration</div><div class="card-desc">Every code push automatically builds and tests the app. Bugs caught immediately. No more manual testing before releases.</div></div>
    <div class="card fade-in"><div class="card-icon">🚀</div><div class="card-title">Continuous Deployment</div><div class="card-desc">After tests pass, new version deploys automatically to production. Push code — users see it in 60 seconds. Zero manual steps.</div></div>
  </div>
  <div class="grid-3">
    <div class="card fade-in"><div class="card-icon">😰</div><div class="card-title">Without CI/CD</div><div class="card-desc">Deployments take hours. Bugs found late. Servers configured manually. Teams move slowly with fear.</div></div>
    <div class="card fade-in"><div class="card-icon">✅</div><div class="card-title">With CI/CD</div><div class="card-desc">Deployments take 60 seconds. Bugs caught instantly. Infrastructure as code. Teams ship with confidence.</div></div>
    <div class="card fade-in"><div class="card-icon">🏢</div><div class="card-title">Who Uses This?</div><div class="card-desc">Netflix deploys 100s of times daily. Amazon every 11 seconds. Swiggy, Zomato, Freshworks all use this pattern.</div></div>
  </div>
  <div class="card fade-in" style="max-width:460px">
    <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem">
      <div style="width:52px;height:52px;border-radius:50%;background:linear-gradient(135deg,var(--p1),var(--p2));display:flex;align-items:center;justify-content:center;font-size:1.3rem;flex-shrink:0">👨‍💻</div>
      <div>
        <div style="font-size:1rem;font-weight:800">Jose Samuel D</div>
        <div style="font-size:11px;color:var(--muted)">Aspiring DevOps and Cloud Engineer</div>
        <div style="font-size:11px;color:var(--muted)">Final Year CSE · Prathyusha Engineering College</div>
      </div>
    </div>
    <div style="display:flex;gap:8px;flex-wrap:wrap">
      <a href="https://github.com/JOSESAMUEL14" target="_blank" style="display:inline-flex;align-items:center;gap:5px;padding:5px 12px;border-radius:100px;background:var(--glass);border:1px solid var(--border);color:var(--muted);font-family:Space Mono,monospace;font-size:9px;text-decoration:none"><i class="fa-brands fa-github"></i> GitHub</a>
      <a href="https://linkedin.com/in/samueld14" target="_blank" style="display:inline-flex;align-items:center;gap:5px;padding:5px 12px;border-radius:100px;background:var(--glass);border:1px solid var(--border);color:var(--muted);font-family:Space Mono,monospace;font-size:9px;text-decoration:none"><i class="fa-brands fa-linkedin"></i> LinkedIn</a>
      <a href="mailto:Josesamueld2005@gmail.com" style="display:inline-flex;align-items:center;gap:5px;padding:5px 12px;border-radius:100px;background:var(--glass);border:1px solid var(--border);color:var(--muted);font-family:Space Mono,monospace;font-size:9px;text-decoration:none"><i class="fa-solid fa-envelope"></i> Email</a>
    </div>
  </div>
</div>
</div>

<!-- ═══════════════════════════════════════ -->
<!-- SECTION 3 — ARCHITECTURE               -->
<!-- ═══════════════════════════════════════ -->
<div id="architecture" class="section">
  <div class="section-tag">System Design</div>
  <div class="section-title fade-in"><span class="w">ARCHITECTURE</span><br><span class="a">DIAGRAM</span></div>
  <div class="section-desc fade-in">How all components connect in this multi-cloud CI/CD system.</div>
  <div class="arch-diagram fade-in">
    <div class="arch-label">Developer Workflow</div>
    <div class="arch-row">
      <div class="arch-box"><div class="arch-box-icon">💻</div><div class="arch-box-name">Developer</div><div class="arch-box-desc">Writes code</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-box"><div class="arch-box-icon"><i class="fa-brands fa-github"></i></div><div class="arch-box-name">GitHub</div><div class="arch-box-desc">git push</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-box"><div class="arch-box-icon">⚡</div><div class="arch-box-name">GH Actions</div><div class="arch-box-desc">CI/CD trigger</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-box"><div class="arch-box-icon"><i class="fa-brands fa-docker"></i></div><div class="arch-box-name">Docker Build</div><div class="arch-box-desc">Image created</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-box"><div class="arch-box-icon">🐋</div><div class="arch-box-name">Docker Hub</div><div class="arch-box-desc">Registry</div></div>
    </div>
    <div class="arch-divider"></div>
    <div class="arch-label">Cloud Deployment</div>
    <div class="arch-row">
      <div class="arch-box"><div class="arch-box-icon">🐋</div><div class="arch-box-name">Docker Hub</div><div class="arch-box-desc">Image pulled</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-box"><div class="arch-box-icon">☸️</div><div class="arch-box-name">Kubernetes</div><div class="arch-box-desc">Orchestration</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-box"><div class="arch-box-icon"><i class="fa-brands fa-aws"></i></div><div class="arch-box-name">AWS EC2</div><div class="arch-box-desc">Mumbai</div></div>
      <div class="arch-arrow">+</div>
      <div class="arch-box"><div class="arch-box-icon">☁️</div><div class="arch-box-name">Render</div><div class="arch-box-desc">24/7 hosting</div></div>
    </div>
    <div class="arch-divider"></div>
    <div class="arch-label">Monitoring Stack</div>
    <div class="arch-row">
      <div class="arch-box"><div class="arch-box-icon">🏗️</div><div class="arch-box-name">Terraform</div><div class="arch-box-desc">IaC</div></div>
      <div class="arch-arrow">+</div>
      <div class="arch-box"><div class="arch-box-icon">📊</div><div class="arch-box-name">Prometheus</div><div class="arch-box-desc">Metrics</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-box"><div class="arch-box-icon">📈</div><div class="arch-box-name">Grafana</div><div class="arch-box-desc">Dashboards</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-box"><div class="arch-box-icon">🔔</div><div class="arch-box-name">Alerts</div><div class="arch-box-desc">Anomalies</div></div>
    </div>
  </div>
  <div class="grid-2">
    <div class="card fade-in"><div class="card-icon">🐳</div><div class="card-title">Containerisation</div><div class="card-desc">Flask app packaged in Docker with everything it needs. Runs identically on any machine — laptop or cloud server.</div></div>
    <div class="card fade-in"><div class="card-icon">☸️</div><div class="card-title">Orchestration</div><div class="card-desc">Kubernetes keeps 2 replicas running always. Auto-restarts crashed containers. Rolling updates = zero downtime.</div></div>
    <div class="card fade-in"><div class="card-icon">🏗️</div><div class="card-title">Infrastructure as Code</div><div class="card-desc">Terraform defines AWS infrastructure in code. No manual clicking in AWS console — everything automated.</div></div>
    <div class="card fade-in"><div class="card-icon">📊</div><div class="card-title">Observability</div><div class="card-desc">Prometheus scrapes metrics every 15 seconds. Grafana live dashboards. Engineers know problems before users do.</div></div>
  </div>
</div>

<!-- ═══════════════════════════════════════ -->
<!-- SECTION 4 — TECH STACK                 -->
<!-- ═══════════════════════════════════════ -->
<div style="background:rgba(255,255,255,0.015);border-top:1px solid var(--border);border-bottom:1px solid var(--border)">
<div id="techstack" class="section">
  <div class="section-tag">Tools and Technologies</div>
  <div class="section-title fade-in"><span class="w">THE TECH</span><br><span class="a">STACK</span></div>
  <div class="section-desc fade-in">8 industry-standard tools — each chosen because it is used by real companies in production.</div>
  <div class="grid-2">
    <div class="card fade-in"><div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem"><div style="width:42px;height:42px;border-radius:12px;background:rgba(36,150,237,0.15);display:flex;align-items:center;justify-content:center;font-size:20px"><i class="fa-brands fa-docker" style="color:#2496ED"></i></div><div><div style="font-size:0.95rem;font-weight:800">Docker</div><div style="width:35px;height:2px;background:linear-gradient(90deg,#2496ED,transparent);margin-top:3px;border-radius:2px"></div></div></div><div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:0.6rem">Containerisation platform. Packages app and all dependencies into portable containers that run anywhere.</div><div style="font-size:10px;color:var(--muted)"><span style="color:#2496ED;font-weight:700">Why:</span> Industry standard. Used by every major company.</div></div>
    <div class="card fade-in"><div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem"><div style="width:42px;height:42px;border-radius:12px;background:rgba(50,108,229,0.15);display:flex;align-items:center;justify-content:center;font-size:20px"><i class="fa-solid fa-ship" style="color:#326CE5"></i></div><div><div style="font-size:0.95rem;font-weight:800">Kubernetes</div><div style="width:35px;height:2px;background:linear-gradient(90deg,#326CE5,transparent);margin-top:3px;border-radius:2px"></div></div></div><div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:0.6rem">Container orchestration. Manages, scales, and heals containers automatically across servers.</div><div style="font-size:10px;color:var(--muted)"><span style="color:#326CE5;font-weight:700">Why:</span> Most in-demand DevOps skill in 2025.</div></div>
    <div class="card fade-in"><div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem"><div style="width:42px;height:42px;border-radius:12px;background:rgba(255,255,255,0.08);display:flex;align-items:center;justify-content:center;font-size:20px"><i class="fa-brands fa-github" style="color:#fff"></i></div><div><div style="font-size:0.95rem;font-weight:800">GitHub Actions</div><div style="width:35px;height:2px;background:linear-gradient(90deg,#fff,transparent);margin-top:3px;border-radius:2px"></div></div></div><div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:0.6rem">CI/CD automation built into GitHub. Runs pipelines automatically on every code push.</div><div style="font-size:10px;color:var(--muted)"><span style="color:#fff;font-weight:700">Why:</span> Free and integrated. Used by millions of developers.</div></div>
    <div class="card fade-in"><div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem"><div style="width:42px;height:42px;border-radius:12px;background:rgba(123,66,188,0.15);display:flex;align-items:center;justify-content:center;font-size:20px"><i class="fa-solid fa-layer-group" style="color:#7B42BC"></i></div><div><div style="font-size:0.95rem;font-weight:800">Terraform</div><div style="width:35px;height:2px;background:linear-gradient(90deg,#7B42BC,transparent);margin-top:3px;border-radius:2px"></div></div></div><div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:0.6rem">Infrastructure as Code. Defines cloud resources in code and provisions them automatically.</div><div style="font-size:10px;color:var(--muted)"><span style="color:#7B42BC;font-weight:700">Why:</span> Most popular IaC tool. Works on any cloud.</div></div>
    <div class="card fade-in"><div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem"><div style="width:42px;height:42px;border-radius:12px;background:rgba(255,153,0,0.15);display:flex;align-items:center;justify-content:center;font-size:20px"><i class="fa-brands fa-aws" style="color:#FF9900"></i></div><div><div style="font-size:0.95rem;font-weight:800">AWS EC2</div><div style="width:35px;height:2px;background:linear-gradient(90deg,#FF9900,transparent);margin-top:3px;border-radius:2px"></div></div></div><div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:0.6rem">Amazon Web Services virtual server. Runs the containerised application in the cloud.</div><div style="font-size:10px;color:var(--muted)"><span style="color:#FF9900;font-weight:700">Why:</span> Largest cloud provider. Fundamental for cloud roles.</div></div>
    <div class="card fade-in"><div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem"><div style="width:42px;height:42px;border-radius:12px;background:rgba(230,82,44,0.15);display:flex;align-items:center;justify-content:center;font-size:20px"><i class="fa-solid fa-chart-line" style="color:#E6522C"></i></div><div><div style="font-size:0.95rem;font-weight:800">Prometheus</div><div style="width:35px;height:2px;background:linear-gradient(90deg,#E6522C,transparent);margin-top:3px;border-radius:2px"></div></div></div><div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:0.6rem">Open source monitoring. Scrapes and stores metrics from applications and servers every 15 seconds.</div><div style="font-size:10px;color:var(--muted)"><span style="color:#E6522C;font-weight:700">Why:</span> Industry standard for cloud-native monitoring.</div></div>
    <div class="card fade-in"><div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem"><div style="width:42px;height:42px;border-radius:12px;background:rgba(244,104,0,0.15);display:flex;align-items:center;justify-content:center;font-size:20px"><i class="fa-solid fa-chart-bar" style="color:#F46800"></i></div><div><div style="font-size:0.95rem;font-weight:800">Grafana</div><div style="width:35px;height:2px;background:linear-gradient(90deg,#F46800,transparent);margin-top:3px;border-radius:2px"></div></div></div><div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:0.6rem">Visualisation platform. Creates beautiful live dashboards from Prometheus and other data sources.</div><div style="font-size:10px;color:var(--muted)"><span style="color:#F46800;font-weight:700">Why:</span> Most popular open source dashboard tool.</div></div>
    <div class="card fade-in"><div style="display:flex;align-items:center;gap:10px;margin-bottom:0.8rem"><div style="width:42px;height:42px;border-radius:12px;background:rgba(55,118,171,0.15);display:flex;align-items:center;justify-content:center;font-size:20px"><i class="fa-brands fa-python" style="color:#3776AB"></i></div><div><div style="font-size:0.95rem;font-weight:800">Python Flask</div><div style="width:35px;height:2px;background:linear-gradient(90deg,#3776AB,transparent);margin-top:3px;border-radius:2px"></div></div></div><div style="font-size:12px;color:rgba(255,255,255,0.7);line-height:1.5;margin-bottom:0.6rem">Lightweight web framework. Powers the dashboard with REST API endpoints for health, metrics, and deploy.</div><div style="font-size:10px;color:var(--muted)"><span style="color:#3776AB;font-weight:700">Why:</span> Simple, fast, perfect for microservices.</div></div>
  </div>
</div>
</div>

<!-- ═══════════════════════════════════════ -->
<!-- SECTION 5 — PIPELINE                   -->
<!-- ═══════════════════════════════════════ -->
<div id="pipeline-section" class="section">
  <div class="section-tag">How It Works</div>
  <div class="section-title fade-in"><span class="w">THE</span><br><span class="a">PIPELINE</span></div>
  <div class="section-desc fade-in">From writing code to live in production — every step that happens automatically in under 60 seconds.</div>

  <div class="pipe-step fade-in"><div class="pipe-num">01</div><div class="pipe-content"><div class="pipe-title">Developer Writes Code</div><div class="pipe-desc">Developer makes changes to the Flask app — adding features, fixing bugs, updating UI. Code lives in GitHub.</div><div class="pipe-tag">Local Development</div></div></div>
  <div class="pipe-step fade-in"><div class="pipe-num">02</div><div class="pipe-content"><div class="pipe-title">Push to GitHub</div><div class="pipe-desc">Developer runs git push origin main. This single action triggers the entire automated pipeline instantly.</div><div class="pipe-tag">GitHub</div></div></div>
  <div class="pipe-step fade-in"><div class="pipe-num">03</div><div class="pipe-content"><div class="pipe-title">GitHub Actions Triggers</div><div class="pipe-desc">GitHub detects the push and starts the CI/CD workflow automatically. A virtual Ubuntu server spins up on GitHub infrastructure.</div><div class="pipe-tag">GitHub Actions</div></div></div>
  <div class="pipe-step fade-in"><div class="pipe-num">04</div><div class="pipe-content"><div class="pipe-title">Docker Image Built</div><div class="pipe-desc">GitHub Actions reads the Dockerfile and builds a new Docker image with the updated application. Tagged with unique commit SHA.</div><div class="pipe-tag">Docker</div></div></div>
  <div class="pipe-step fade-in"><div class="pipe-num">05</div><div class="pipe-content"><div class="pipe-title">Image Pushed to Docker Hub</div><div class="pipe-desc">The built image is pushed to Docker Hub registry — making it available to any server worldwide as josesamuel14/multicloud-app:latest.</div><div class="pipe-tag">Docker Hub</div></div></div>
  <div class="pipe-step fade-in"><div class="pipe-num">06</div><div class="pipe-content"><div class="pipe-title">Kubernetes Rolling Update</div><div class="pipe-desc">Kubernetes pulls the new image and performs a Rolling Update — replacing old containers gradually. Zero downtime for users.</div><div class="pipe-tag">Kubernetes</div></div></div>
  <div class="pipe-step fade-in"><div class="pipe-num">07</div><div class="pipe-content"><div class="pipe-title">Live on AWS and Render</div><div class="pipe-desc">New version live on AWS EC2 Mumbai and Render simultaneously. Total time: under 60 seconds. Automatically. Every time.</div><div class="pipe-tag">AWS + Render</div></div></div>
  <div class="pipe-step fade-in"><div class="pipe-num">08</div><div class="pipe-content"><div class="pipe-title">Prometheus Monitors</div><div class="pipe-desc">Prometheus scrapes metrics every 15 seconds. Grafana shows live dashboards. Engineers know about problems before users do.</div><div class="pipe-tag">Prometheus + Grafana</div></div></div>

  <div class="card fade-in" style="text-align:center;padding:1.8rem">
    <div style="font-size:1.8rem;margin-bottom:0.8rem">⚡</div>
    <div style="font-size:1.2rem;font-weight:800;margin-bottom:0.4rem">Total Time: Under 60 Seconds</div>
    <div style="font-size:13px;color:var(--muted)">From git push to live in production — fully automated, zero manual steps</div>
  </div>
</div>

<!-- ═══════════════════════════════════════ -->
<!-- SECTION 6 — LIVE DEMO                  -->
<!-- ═══════════════════════════════════════ -->
<div style="background:rgba(255,255,255,0.015);border-top:1px solid var(--border)">
<div id="demo" class="section">
  <div class="section-tag">Interactive Demo</div>
  <div class="section-title fade-in"><span class="w">LIVE</span><br><span class="a">DEMO</span></div>
  <div class="section-desc fade-in">Everything below is real and live. Click any button to interact with the actual running system.</div>

  <div class="grid-2">
    <div class="card fade-in">
      <div class="card-icon" style="color:#10b981"><i class="fa-solid fa-heart-pulse"></i></div>
      <div class="card-title">Health Check</div>
      <div class="card-desc" style="margin-bottom:1rem">Returns real system info — cloud, region, uptime, hostname of the actual server running right now.</div>
      <button onclick="checkHealth()" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:100px;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);color:#10b981;font-family:Space Mono,monospace;font-size:9px;font-weight:700;letter-spacing:1px;cursor:pointer;border-style:solid"><i class="fa-solid fa-heart-pulse"></i> Check Now</button>
      <div id="health-response" style="display:none;margin-top:0.8rem;background:rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:0.8rem;font-family:Space Mono,monospace;font-size:11px;color:#10b981;white-space:pre-wrap"></div>
    </div>
    <div class="card fade-in">
      <div class="card-icon" style="color:#eab308"><i class="fa-solid fa-chart-bar"></i></div>
      <div class="card-title">Live Stats</div>
      <div class="card-desc" style="margin-bottom:1rem">Real-time stats — total requests served, current uptime, system status. Auto-updates every 5 seconds.</div>
      <button onclick="checkStats()" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:100px;background:rgba(234,179,8,0.1);border:1px solid rgba(234,179,8,0.25);color:#eab308;font-family:Space Mono,monospace;font-size:9px;font-weight:700;letter-spacing:1px;cursor:pointer;border-style:solid"><i class="fa-solid fa-chart-bar"></i> Fetch Stats</button>
      <div id="stats-display" style="display:none;margin-top:0.8rem;display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px">
        <div style="background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:0.8rem;text-align:center"><div id="stat-req" style="font-size:1.2rem;font-weight:800;background:linear-gradient(135deg,var(--p1),var(--p2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">--</div><div style="font-family:Space Mono,monospace;font-size:8px;letter-spacing:1px;color:var(--muted);margin-top:3px">REQUESTS</div></div>
        <div style="background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:0.8rem;text-align:center"><div id="stat-up" style="font-size:1.2rem;font-weight:800;background:linear-gradient(135deg,var(--p1),var(--p2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">--</div><div style="font-family:Space Mono,monospace;font-size:8px;letter-spacing:1px;color:var(--muted);margin-top:3px">UPTIME</div></div>
        <div style="background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.08);border-radius:10px;padding:0.8rem;text-align:center"><div id="stat-status" style="font-size:1rem;font-weight:800;background:linear-gradient(135deg,var(--p1),var(--p2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text">--</div><div style="font-family:Space Mono,monospace;font-size:8px;letter-spacing:1px;color:var(--muted);margin-top:3px">STATUS</div></div>
      </div>
    </div>
    <div class="card fade-in">
      <div class="card-icon" style="color:var(--p1)"><i class="fa-solid fa-rocket"></i></div>
      <div class="card-title">Trigger Pipeline</div>
      <div class="card-desc" style="margin-bottom:1rem">Click Deploy Now to trigger a real GitHub Actions CI/CD run. Watch it build and deploy live on GitHub!</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <button onclick="showDeploy()" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:100px;background:linear-gradient(135deg,var(--p1),var(--p2));color:#fff;font-family:Space Mono,monospace;font-size:9px;font-weight:700;letter-spacing:1px;cursor:pointer;border:none"><i class="fa-solid fa-rocket"></i> Deploy Now</button>
        <a href="https://github.com/JOSESAMUEL14/multicloud-cicd/actions" target="_blank" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:100px;background:var(--glass);border:1px solid var(--border);color:#fff;font-family:Space Mono,monospace;font-size:9px;font-weight:700;letter-spacing:1px;text-decoration:none"><i class="fa-brands fa-github"></i> Watch Live</a>
      </div>
    </div>
    <div class="card fade-in">
      <div class="card-icon" style="color:#06B6D4"><i class="fa-solid fa-code"></i></div>
      <div class="card-title">Source Code</div>
      <div class="card-desc" style="margin-bottom:1rem">Entire project is open source — Dockerfile, K8s configs, Terraform IaC, GitHub Actions workflow, monitoring setup.</div>
      <div style="display:flex;gap:8px;flex-wrap:wrap">
        <a href="https://github.com/JOSESAMUEL14/multicloud-cicd" target="_blank" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:100px;background:var(--glass);border:1px solid var(--border);color:#fff;font-family:Space Mono,monospace;font-size:9px;font-weight:700;letter-spacing:1px;text-decoration:none"><i class="fa-brands fa-github"></i> View Repo</a>
        <a href="/metrics" target="_blank" style="display:inline-flex;align-items:center;gap:6px;padding:8px 16px;border-radius:100px;background:rgba(234,179,8,0.1);border:1px solid rgba(234,179,8,0.25);color:#eab308;font-family:Space Mono,monospace;font-size:9px;font-weight:700;letter-spacing:1px;text-decoration:none"><i class="fa-solid fa-chart-line"></i> Raw Metrics</a>
      </div>
    </div>
  </div>
</div>
</div>

<!-- FOOTER -->
<footer style="position:relative;z-index:10;text-align:center;padding:2rem;border-top:1px solid var(--border);font-family:Space Mono,monospace;font-size:10px;color:var(--muted)">
  Built by <a href="https://github.com/JOSESAMUEL14" style="color:var(--p1);text-decoration:none">Jose Samuel D</a> &nbsp;·&nbsp;
  <a href="https://github.com/JOSESAMUEL14/multicloud-cicd" style="color:var(--muted);text-decoration:none">GitHub</a> &nbsp;·&nbsp;
  <a href="https://linkedin.com/in/samueld14" style="color:var(--muted);text-decoration:none">LinkedIn</a>
</footer>

<script>
function scrollTo(id){{
  document.getElementById(id).scrollIntoView({{behavior:"smooth"}});
}}
function tick(){{const n=new Date();document.getElementById("clk").textContent=n.toTimeString().slice(0,8);}}
setInterval(tick,1000);tick();
async function updateMetrics(){{
  try{{
    const r=await fetch("/stats");
    const d=await r.json();
    document.getElementById("req-count").textContent=d.total_requests||"0";
    document.getElementById("uptime").textContent=d.uptime||"--";
    document.getElementById("health-val").textContent=d.status||"--";
  }}catch(e){{}}
}}
setInterval(updateMetrics,5000);updateMetrics();
function showDeploy(){{document.getElementById("deployModal").classList.add("show");}}
function closeModal(){{document.getElementById("deployModal").classList.remove("show");document.getElementById("deploy-status").textContent="";}}
async function confirmDeploy(){{
  const s=document.getElementById("deploy-status");
  s.textContent="Triggering...";s.style.color="#eab308";
  try{{
    const r=await fetch("/deploy",{{method:"POST",headers:{{"Content-Type":"application/json"}}}});
    const d=await r.json();
    s.textContent=d.success?"✅ Pipeline triggered!":"❌ "+d.message;
    s.style.color=d.success?"#10b981":"#ef4444";
  }}catch(e){{s.textContent="❌ "+e.message;s.style.color="#ef4444";}}
}}
async function checkHealth(){{
  const box=document.getElementById("health-response");
  box.style.display="block";
  box.textContent="Fetching...";
  try{{
    const r=await fetch("/health");
    const d=await r.json();
    box.textContent=JSON.stringify(d,null,2);
  }}catch(e){{box.textContent="Error: "+e.message;}}
}}
async function checkStats(){{
  document.getElementById("stats-display").style.display="grid";
  try{{
    const r=await fetch("/stats");
    const d=await r.json();
    document.getElementById("stat-req").textContent=d.total_requests||"0";
    document.getElementById("stat-up").textContent=d.uptime||"--";
    document.getElementById("stat-status").textContent=d.status||"--";
  }}catch(e){{}}
}}
setInterval(checkStats,5000);
const obs=new IntersectionObserver(entries=>{{
  entries.forEach(e=>{{if(e.isIntersecting)e.target.classList.add("visible");}});
}},{{threshold:0.1}});
document.querySelectorAll(".fade-in").forEach(el=>obs.observe(el));

// Hex grid
const cv=document.getElementById("cv"),ctx=cv.getContext("2d");
let W,H,t=0;
function rsz(){{W=cv.width=innerWidth;H=cv.height=innerHeight;}}
rsz();window.addEventListener("resize",rsz);
const S=26;
function draw(){{
  ctx.fillStyle="#06061a";ctx.fillRect(0,0,W,H);
  t+=0.05;
  const rows=Math.ceil(H/(S*1.5))+2,cols=Math.ceil(W/(S*1.73))+2;
  for(let r=0;r<rows;r++){{
    for(let c=0;c<cols;c++){{
      const x=c*S*1.73+(r%2)*S*0.866;
      const y=r*S*1.5;
      const v=(Math.sin(t+c*0.45+r*0.65)+Math.sin(t*0.85+c*0.75-r*0.45)+Math.sin(t*1.2-c*0.3+r*0.8))/3;
      const a=0.05+v*0.22;
      ctx.beginPath();
      for(let i=0;i<6;i++){{
        const ang=Math.PI/180*(60*i-30);
        i===0?ctx.moveTo(x+(S-1)*Math.cos(ang),y+(S-1)*Math.sin(ang)):ctx.lineTo(x+(S-1)*Math.cos(ang),y+(S-1)*Math.sin(ang));
      }}
      ctx.closePath();
      ctx.strokeStyle=`rgba(6,182,212,${{Math.max(0.04,a)}})`;ctx.lineWidth=0.9;ctx.stroke();
      if(v>0.45){{ctx.fillStyle=`rgba(124,58,237,${{(v-0.45)*0.28}})`;ctx.fill();}}
      if(v>0.72){{ctx.fillStyle=`rgba(6,182,212,${{(v-0.72)*0.55}})`;ctx.fill();}}
      if(v>0.88){{ctx.fillStyle=`rgba(255,255,255,${{(v-0.88)*0.15}})`;ctx.fill();}}
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
    data = {{
        "status": "healthy",
        "cloud": os.getenv("CLOUD_PROVIDER", "local"),
        "region": os.getenv("CLOUD_REGION", "local"),
        "uptime": get_uptime(),
        "hostname": socket.gethostname(),
        "python": platform.python_version()
    }}
    return jsonify(data), 200


@app.route("/stats")
def stats():
    try:
        metrics_data = requests.get(
            "http://localhost:5000/metrics", timeout=2).text
        total = 0
        for line in metrics_data.split('\n'):
            if 'flask_http_request_total' in line and not line.startswith('#'):
                try:
                    total += float(line.split(' ')[-1])
                except:
                    pass
    except:
        total = 0
    data = {{
        "status": "HEALTHY",
        "total_requests": int(total),
        "uptime": get_uptime(),
        "cloud": os.getenv("CLOUD_PROVIDER", "local"),
        "hostname": socket.gethostname()
    }}
    return jsonify(data)


@app.route("/deploy", methods=["POST"])
def deploy():
    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        return jsonify({{"success": False, "message": "GITHUB_TOKEN not configured"}})
    try:
        r = requests.post(
            "https://api.github.com/repos/JOSESAMUEL14/multicloud-cicd/dispatches",
            headers={{
                "Authorization": f"Bearer {{token}}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            }},
            json={{"event_type": "manual-deploy"}},
            timeout=10
        )
        if r.status_code == 204:
            return jsonify({{"success": True, "message": "Pipeline triggered!"}})
        else:
            return jsonify({{"success": False, "message": f"GitHub API error: {{r.status_code}}"}})
    except Exception as e:
        return jsonify({{"success": False, "message": str(e)}})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)