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

def get_theme():
    cloud = os.getenv("CLOUD_PROVIDER", "local")
    themes = {
        "aws":    {"p1":"#FF9900","p2":"#FF6B35","label":"Amazon Web Services","short":"AWS"},
        "gcp":    {"p1":"#4285F4","p2":"#34A853","label":"Google Cloud Platform","short":"GCP"},
        "render": {"p1":"#7C3AED","p2":"#06B6D4","label":"Render Cloud","short":"RENDER"},
        "local":  {"p1":"#7C3AED","p2":"#06B6D4","label":"Local Kubernetes","short":"LOCAL"}
    }
    return themes.get(cloud.lower(), themes["local"])

NAV = '''
<nav>
  <div class="nav-brand">SAMUEL<span>/</span>DEVOPS</div>
  <div class="nav-links">
    <a href="/" class="nav-link">Home</a>
    <a href="/about" class="nav-link">About</a>
    <a href="/architecture" class="nav-link">Architecture</a>
    <a href="/techstack" class="nav-link">Tech Stack</a>
    <a href="/pipeline" class="nav-link">Pipeline</a>
    <a href="/demo" class="nav-link">Live Demo</a>
  </div>
  <div class="nav-right">
    <a href="https://github.com/JOSESAMUEL14/multicloud-cicd" target="_blank" class="nav-github"><i class="fa-brands fa-github"></i></a>
    <div class="live-pill"><span class="live-dot"></span>LIVE</div>
  </div>
</nav>
'''
BASE_STYLE = '''
<link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;600;700;800;900&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box}
:root{--p1:#7C3AED;--p2:#06B6D4;--bg:#06061a;--glass:rgba(255,255,255,0.04);--border:rgba(255,255,255,0.08);--muted:rgba(255,255,255,0.4)}
html{scroll-behavior:smooth}
body{font-family:"Exo 2",sans-serif;background:var(--bg);color:#fff;overflow-x:hidden}
#cv{position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none;opacity:0.6}
.vig{position:fixed;inset:0;z-index:1;pointer-events:none;background:radial-gradient(ellipse at 50% 50%,transparent 25%,rgba(6,6,26,0.8) 100%)}
nav{position:fixed;top:0;left:0;right:0;z-index:100;display:flex;align-items:center;justify-content:space-between;padding:1rem 2rem;background:rgba(6,6,26,0.8);backdrop-filter:blur(20px);border-bottom:1px solid var(--border)}
.nav-brand{font-family:"Space Mono",monospace;font-size:14px;font-weight:700;letter-spacing:2px;color:#fff}
.nav-brand span{color:var(--p1)}
.nav-links{display:flex;gap:24px}
.nav-link{font-family:"Space Mono",monospace;font-size:10px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);text-decoration:none;transition:color 0.3s}
.nav-link:hover{color:#fff}
.nav-right{display:flex;align-items:center;gap:12px}
.nav-github{color:var(--muted);font-size:18px;transition:color 0.3s;text-decoration:none}
.nav-github:hover{color:#fff}
.live-pill{display:flex;align-items:center;gap:6px;padding:5px 12px;border-radius:100px;background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;color:#10b981}
.live-dot{width:6px;height:6px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;animation:blink 2s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.2}}
.section{position:relative;z-index:10;min-height:100vh;padding:6rem 2rem 4rem;max-width:1000px;margin:0 auto}
.section-tag{display:inline-flex;align-items:center;gap:8px;font-family:"Space Mono",monospace;font-size:10px;letter-spacing:3px;text-transform:uppercase;color:var(--muted);padding:6px 14px;border-radius:100px;border:1px solid var(--border);margin-bottom:1.5rem}
.section-title{font-size:clamp(2.5rem,6vw,4.5rem);font-weight:900;letter-spacing:-1px;line-height:0.9;margin-bottom:1rem}
.section-title .w{color:#fff}
.section-title .a{background:linear-gradient(135deg,var(--p1),var(--p2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.section-desc{font-size:1rem;color:var(--muted);line-height:1.8;max-width:600px;margin-bottom:3rem}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:1.5rem}
.grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:1.5rem}
.card{background:var(--glass);border:1px solid var(--border);border-radius:20px;padding:1.5rem;backdrop-filter:blur(20px);transition:all 0.4s cubic-bezier(.16,1,.3,1)}
.card:hover{transform:translateY(-6px);border-color:rgba(255,255,255,0.15);box-shadow:0 20px 60px rgba(0,0,0,0.5)}
.card-icon{font-size:2rem;margin-bottom:1rem}
.card-title{font-size:1.1rem;font-weight:700;margin-bottom:0.5rem;color:#fff}
.card-desc{font-size:0.85rem;color:var(--muted);line-height:1.6}
.pipe-step{display:flex;gap:1.5rem;margin-bottom:2rem;align-items:flex-start}
.pipe-num{font-family:"Space Mono",monospace;font-size:3rem;font-weight:700;color:rgba(255,255,255,0.08);min-width:80px;line-height:1}
.pipe-content{flex:1;padding-top:8px}
.pipe-title{font-size:1.3rem;font-weight:800;margin-bottom:0.5rem;background:linear-gradient(135deg,var(--p1),var(--p2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.pipe-desc{font-size:0.9rem;color:var(--muted);line-height:1.7}
.pipe-tag{display:inline-block;font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;padding:4px 12px;border-radius:100px;background:rgba(124,58,237,0.15);border:1px solid rgba(124,58,237,0.3);color:var(--p1);margin-top:8px}
.fade-in{opacity:0;transform:translateY(30px);transition:all 0.7s cubic-bezier(.16,1,.3,1)}
.fade-in.visible{opacity:1;transform:translateY(0)}
.divider{width:100%;height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:2rem 0}
.arch-diagram{background:var(--glass);border:1px solid var(--border);border-radius:20px;padding:2rem;margin-bottom:2rem}
.arch-row{display:flex;align-items:center;justify-content:center;gap:0;flex-wrap:wrap;margin-bottom:1.5rem}
.arch-box{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.12);border-radius:14px;padding:1rem 1.2rem;text-align:center;min-width:100px;transition:all 0.3s}
.arch-box:hover{background:rgba(124,58,237,0.15);border-color:rgba(124,58,237,0.4);transform:translateY(-4px)}
.arch-box-icon{font-size:1.5rem;margin-bottom:6px}
.arch-box-name{font-size:11px;font-weight:700;color:#fff}
.arch-box-desc{font-size:9px;color:var(--muted);margin-top:2px}
.arch-arrow{font-size:1.5rem;color:rgba(255,255,255,0.2);padding:0 8px;margin-bottom:28px}
.arch-label{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);text-align:center;margin-bottom:1rem}
.arch-divider{width:100%;height:1px;background:linear-gradient(90deg,transparent,var(--border),transparent);margin:1.5rem 0}
.demo-card{background:var(--glass);border:1px solid var(--border);border-radius:20px;padding:2rem;margin-bottom:1.5rem;backdrop-filter:blur(20px)}
.demo-title{font-size:1.1rem;font-weight:800;margin-bottom:0.5rem;display:flex;align-items:center;gap:10px}
.demo-desc{font-size:13px;color:var(--muted);margin-bottom:1.5rem;line-height:1.6}
.response-box{background:rgba(0,0,0,0.4);border:1px solid rgba(255,255,255,0.1);border-radius:12px;padding:1rem;font-family:"Space Mono",monospace;font-size:12px;color:#10b981;min-height:60px;margin-top:1rem;display:none;white-space:pre-wrap}
.response-box.show{display:block}
.stat-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:1rem}
.stat-item{background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:1rem;text-align:center}
.stat-label{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-top:4px}
.modal{display:none;position:fixed;inset:0;z-index:200;align-items:center;justify-content:center;background:rgba(0,0,0,0.7);backdrop-filter:blur(10px)}
.modal.show{display:flex}
.modal-box{background:#0d0d1a;border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:2rem;max-width:400px;width:90%;text-align:center}
.modal-title{font-size:1.2rem;font-weight:800;margin-bottom:0.5rem}
.modal-sub{font-size:12px;color:var(--muted);margin-bottom:1.5rem;line-height:1.6}
.modal-btns{display:flex;gap:10px;justify-content:center}
.modal-btn{padding:10px 24px;border-radius:100px;font-size:11px;font-weight:700;cursor:pointer;border:none;transition:all 0.3s;font-family:"Space Mono",monospace}
@media(max-width:768px){.grid-2,.grid-3{grid-template-columns:1fr}.nav-links{display:none}.section-title{font-size:2.5rem}}
</style>
'''

HEX_BG = '''
<canvas id="cv"></canvas>
<div class="vig"></div>
<script>
const cv=document.getElementById("cv"),ctx=cv.getContext("2d");
let W,H,t=0;
function rsz(){W=cv.width=innerWidth;H=cv.height=innerHeight;}
rsz();window.addEventListener("resize",rsz);
const S=28;
function draw(){
  ctx.fillStyle="#06061a";ctx.fillRect(0,0,W,H);
  t+=0.04;
  const rows=Math.ceil(H/(S*1.5))+2,cols=Math.ceil(W/(S*1.73))+2;
  for(let r=0;r<rows;r++){
    for(let c=0;c<cols;c++){
      const x=c*S*1.73+(r%2)*S*0.866;
      const y=r*S*1.5;
      const v=(Math.sin(t+c*0.45+r*0.65)+Math.sin(t*0.85+c*0.75-r*0.45)+Math.sin(t*1.2-c*0.3+r*0.8))/3;
      const a=0.04+v*0.18;
      ctx.beginPath();
      for(let i=0;i<6;i++){
        const ang=Math.PI/180*(60*i-30);
        i===0?ctx.moveTo(x+(S-1)*Math.cos(ang),y+(S-1)*Math.sin(ang)):ctx.lineTo(x+(S-1)*Math.cos(ang),y+(S-1)*Math.sin(ang));
      }
      ctx.closePath();
      ctx.strokeStyle=`rgba(6,182,212,${Math.max(0.03,a)})`;ctx.lineWidth=0.8;ctx.stroke();
      if(v>0.5){ctx.fillStyle=`rgba(124,58,237,${(v-0.5)*0.2})`;ctx.fill();}
      if(v>0.75){ctx.fillStyle=`rgba(6,182,212,${(v-0.75)*0.4})`;ctx.fill();}
    }
  }
  requestAnimationFrame(draw);
}
draw();
const obs=new IntersectionObserver(entries=>{
  entries.forEach(e=>{if(e.isIntersecting)e.target.classList.add("visible");});
},{threshold:0.1});
document.querySelectorAll(".fade-in").forEach(el=>obs.observe(el));
</script>
'''
@app.route("/")
def home():
    cloud = os.getenv("CLOUD_PROVIDER", "local")
    region = os.getenv("CLOUD_REGION", "my-laptop")
    hostname = socket.gethostname()
    python_ver = platform.python_version()
    t = get_theme()
    github_repo = "JOSESAMUEL14/multicloud-cicd"
    cloud_icon = "<i class='fa-brands fa-aws'></i>" if cloud.lower()=="aws" else "<i class='fa-brands fa-google'></i>" if cloud.lower()=="gcp" else "<i class='fa-solid fa-cloud'></i>"
    cloud_label = "AWS" if cloud.lower()=="aws" else "GCP" if cloud.lower()=="gcp" else "Cloud"

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MultiCloud CI/CD</title>
{BASE_STYLE}
<style>
.hero-wrap{{min-height:100vh;display:flex;align-items:center;justify-content:center;padding:6rem 2rem 2rem;position:relative;z-index:10}}
.hero{{text-align:center;max-width:800px}}
.hero-eye{{font-family:"Space Mono",monospace;font-size:10px;letter-spacing:4px;text-transform:uppercase;color:var(--muted);margin-bottom:1rem;display:flex;align-items:center;justify-content:center;gap:12px}}
.hero-eye::before,.hero-eye::after{{content:"";width:40px;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.2))}}
.hero-eye::after{{background:linear-gradient(90deg,rgba(255,255,255,0.2),transparent)}}
h1{{font-size:clamp(3rem,9vw,6rem);font-weight:900;letter-spacing:-2px;line-height:0.9;margin-bottom:1rem}}
h1 .w{{color:#fff}}
h1 .a{{background:linear-gradient(135deg,{t["p1"]},{t["p2"]});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.hero-sub{{font-family:"Space Mono",monospace;font-size:10px;letter-spacing:3px;text-transform:uppercase;color:var(--muted);margin-bottom:2.5rem;display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap}}
.pill-row{{display:flex;gap:10px;justify-content:center;margin-bottom:3rem;flex-wrap:wrap}}
.pill{{display:inline-flex;align-items:center;gap:7px;padding:8px 18px;border-radius:100px;font-family:"Space Mono",monospace;font-size:10px;letter-spacing:1.5px;text-transform:uppercase;backdrop-filter:blur(10px);text-decoration:none;transition:all 0.3s;border:none;cursor:pointer}}
.pill:hover{{transform:translateY(-3px)}}
.pill-primary{{background:linear-gradient(135deg,{t["p1"]},{t["p2"]});color:#fff;box-shadow:0 4px 20px rgba(124,58,237,0.3)}}
.pill-outline{{background:var(--glass);border:1px solid var(--border);color:var(--muted)}}
.pill-green{{background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);color:#10b981}}
.dashboard{{max-width:900px;margin:0 auto;padding:0 2rem 4rem;position:relative;z-index:10}}
.pipeline-strip{{width:100%;background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);border-radius:20px;padding:1.2rem 1.5rem;backdrop-filter:blur(30px);display:flex;align-items:center;justify-content:space-between;margin-bottom:1.2rem;position:relative}}
.pipeline-strip::before{{content:"PIPELINE";position:absolute;top:8px;left:16px;font-family:"Space Mono",monospace;font-size:7px;font-weight:700;letter-spacing:3px;color:rgba(255,255,255,0.1)}}
.pstep{{display:flex;flex-direction:column;align-items:center;gap:7px;flex:1}}
.p-icon{{width:48px;height:48px;border-radius:14px;background:transparent;border:2px solid {t["p1"]};display:flex;align-items:center;justify-content:center;font-size:18px;transition:all 0.4s;box-shadow:0 0 10px rgba(124,58,237,0.25)}}
.p-icon:hover{{transform:translateY(-6px);box-shadow:0 0 25px rgba(124,58,237,0.5);border-color:{t["p2"]}}}
.p-icon i{{font-size:20px;color:#fff}}
.p-icon svg{{width:22px;height:22px}}
.p-label{{font-family:"Space Mono",monospace;font-size:8px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted)}}
.pconn{{flex:1;display:flex;align-items:center;padding-bottom:24px}}
.pline{{width:100%;height:1.5px;background:linear-gradient(90deg,{t["p1"]},{t["p2"]});opacity:0.2;position:relative;overflow:hidden}}
.pline::after{{content:"";position:absolute;top:0;left:-50%;width:30%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,1),transparent);animation:sweep 2s linear infinite}}
@keyframes sweep{{to{{left:150%}}}}
.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin-bottom:1.2rem}}
.dcard{{background:rgba(10,10,30,0.85);border-radius:16px;padding:1rem;display:flex;flex-direction:column;gap:8px;position:relative;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,0.5),0 0 0 1px rgba(255,255,255,0.06),inset 0 1px 0 rgba(255,255,255,0.08);border-top:1px solid rgba(226,232,240,0.2);transition:all 0.5s;cursor:default;transform-style:preserve-3d}}
.dcard::after{{content:"";position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#94a3b8,#ffffff,#94a3b8);opacity:0.4;animation:bargl 3s ease-in-out infinite alternate}}
@keyframes bargl{{from{{opacity:0.2}}to{{opacity:0.7}}}}
.dcard:hover{{transform:perspective(400px) rotateX(8deg) rotateY(-3deg) translateY(-8px) scale(1.03)}}
.dcard-top{{display:flex;align-items:center;justify-content:space-between}}
.dcard-icon{{width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,#94a3b8,#ffffff);display:flex;align-items:center;justify-content:center;font-size:14px;color:#06061a;transition:transform 0.5s}}
.dcard:hover .dcard-icon{{transform:rotate(-12deg) scale(1.15)}}
.dcard-ping{{width:6px;height:6px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;animation:blink 2s infinite}}
.dcard-label{{font-family:"Space Mono",monospace;font-size:8px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3)}}
.dcard-value{{font-size:1rem;font-weight:800;background:linear-gradient(135deg,#e2e8f0,#ffffff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.dcard-sub{{font-size:9px;color:rgba(255,255,255,0.2)}}
.dcard-live{{font-size:8px;color:#10b981;font-weight:600}}
.actions{{display:flex;gap:8px;flex-wrap:wrap;justify-content:center}}
.btn-action{{display:inline-flex;align-items:center;gap:7px;padding:10px 18px;border-radius:100px;font-family:"Space Mono",monospace;font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border:none;cursor:pointer;transition:all 0.3s;text-decoration:none}}
.btn-action:hover{{transform:translateY(-3px)}}
.btn-deploy{{background:linear-gradient(135deg,{t["p1"]},{t["p2"]});color:#fff;box-shadow:0 4px 20px rgba(124,58,237,0.3)}}
.btn-github{{background:var(--glass);border:1px solid var(--border);color:#fff}}
.btn-health{{background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);color:#10b981}}
.btn-metrics{{background:rgba(234,179,8,0.1);border:1px solid rgba(234,179,8,0.25);color:#eab308}}
.status-bar{{display:flex;align-items:center;justify-content:center;gap:8px;flex-wrap:wrap;margin-top:1rem}}
.chip{{display:inline-flex;align-items:center;gap:7px;padding:8px 16px;border-radius:100px;font-family:"Space Mono",monospace;font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;backdrop-filter:blur(16px);transition:all 0.3s}}
.chip-green{{background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);color:#10b981}}
.chip-white{{background:var(--glass);border:1px solid var(--border);color:rgba(255,255,255,0.7)}}
.chip-mono{{background:var(--glass);border:1px solid var(--border);color:var(--muted)}}
.modal-confirm{{background:linear-gradient(135deg,{t["p1"]},{t["p2"]});color:#fff}}
.modal-cancel{{background:rgba(255,255,255,0.08);color:#fff;border:1px solid rgba(255,255,255,0.15)}}
</style>
</head>
<body>
{HEX_BG}
{NAV}
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
<div class="hero-wrap">
  <div class="hero">
    <div class="hero-eye">Multi · Cloud · Infrastructure</div>
    <h1><span class="w">MULTI</span><span class="a">CLOUD</span><br><span class="w">CI</span><span class="a">/CD</span></h1>
    <div class="hero-sub">Kubernetes &nbsp;·&nbsp; Docker &nbsp;·&nbsp; GitHub Actions &nbsp;·&nbsp; Terraform &nbsp;·&nbsp; AWS</div>
    <div class="pill-row">
      <a href="/about" class="pill pill-primary"><i class="fa-solid fa-circle-info"></i> Learn More</a>
      <a href="/demo" class="pill pill-green"><i class="fa-solid fa-rocket"></i> Live Demo</a>
      <a href="https://github.com/JOSESAMUEL14/multicloud-cicd" target="_blank" class="pill pill-outline"><i class="fa-brands fa-github"></i> GitHub</a>
    </div>
  </div>
</div>
<div class="dashboard">
  <div class="pipeline-strip">
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
<script>
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
</script>
</body>
</html>'''
@app.route("/about")
def about():
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>About — MultiCloud CI/CD</title>
{BASE_STYLE}
</head>
<body>
{HEX_BG}
{NAV}
<div class="section">
  <div class="section-tag">About This Project</div>
  <div class="section-title fade-in"><span class="w">WHAT IS</span><br><span class="a">CI/CD?</span></div>
  <div class="section-desc fade-in">CI/CD stands for Continuous Integration and Continuous Deployment. It is a method to frequently deliver apps by introducing automation into the stages of app development.</div>
  <div class="grid-2" style="margin-bottom:3rem">
    <div class="card fade-in">
      <div class="card-icon">⚡</div>
      <div class="card-title">Continuous Integration (CI)</div>
      <div class="card-desc">Every time a developer pushes code to GitHub, the system automatically builds and tests the application. This catches bugs early and ensures the code always works correctly.</div>
    </div>
    <div class="card fade-in">
      <div class="card-icon">🚀</div>
      <div class="card-title">Continuous Deployment (CD)</div>
      <div class="card-desc">After CI passes, the new version is automatically deployed to production servers. Users get new features instantly without any manual work. Push code — users see it in 60 seconds!</div>
    </div>
  </div>
  <div class="divider"></div>
  <div class="section-tag" style="margin-top:2rem">The Problem</div>
  <div class="section-title fade-in"><span class="w">WHY DO COMPANIES</span><br><span class="a">NEED THIS?</span></div>
  <div class="grid-3" style="margin-bottom:3rem">
    <div class="card fade-in">
      <div class="card-icon">😰</div>
      <div class="card-title">Without CI/CD</div>
      <div class="card-desc">Manual deployments take hours. Bugs discovered late. Servers configured by hand. Different environments cause issues. Teams work slowly.</div>
    </div>
    <div class="card fade-in">
      <div class="card-icon">✅</div>
      <div class="card-title">With CI/CD</div>
      <div class="card-desc">Deployments take 60 seconds. Bugs caught immediately. Infrastructure as code. Consistent environments. Teams move fast with confidence.</div>
    </div>
    <div class="card fade-in">
      <div class="card-icon">🏢</div>
      <div class="card-title">Who Uses This?</div>
      <div class="card-desc">Netflix deploys hundreds of times per day. Amazon deploys every 11 seconds. Google, Uber, Swiggy, Zomato all use CI/CD pipelines like this.</div>
    </div>
  </div>
  <div class="divider"></div>
  <div class="section-tag" style="margin-top:2rem">This Project</div>
  <div class="section-title fade-in"><span class="w">WHAT WE</span><br><span class="a">BUILT</span></div>
  <div class="section-desc fade-in">A complete production-grade CI/CD pipeline demonstrating every stage of modern software delivery — from writing code to monitoring it in production.</div>
  <div class="grid-2" style="margin-bottom:3rem">
    <div class="card fade-in">
      <div class="card-icon">🎯</div>
      <div class="card-title">Purpose</div>
      <div class="card-desc">This project demonstrates how a real DevOps engineer sets up infrastructure. It covers containerisation, orchestration, automation, cloud deployment, and monitoring.</div>
    </div>
    <div class="card fade-in">
      <div class="card-icon">🌐</div>
      <div class="card-title">Multi-Cloud</div>
      <div class="card-desc">The application is deployed on both AWS EC2 and Render cloud simultaneously. This shows vendor independence — not being locked into one cloud provider.</div>
    </div>
    <div class="card fade-in">
      <div class="card-icon">🔄</div>
      <div class="card-title">Automation</div>
      <div class="card-desc">Every step is automated. Push code to GitHub — GitHub Actions builds Docker image — pushes to Docker Hub — deploys to cloud. Zero manual steps required.</div>
    </div>
    <div class="card fade-in">
      <div class="card-icon">📊</div>
      <div class="card-title">Observability</div>
      <div class="card-desc">Prometheus collects metrics every 15 seconds. Grafana displays live dashboards showing CPU, memory, request rates, and system health in real time.</div>
    </div>
  </div>
  <div class="divider"></div>
  <div class="section-tag" style="margin-top:2rem">The Builder</div>
  <div class="section-title fade-in"><span class="w">ABOUT</span><br><span class="a">SAMUEL</span></div>
  <div class="card fade-in" style="max-width:500px">
    <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem">
      <div style="width:60px;height:60px;border-radius:50%;background:linear-gradient(135deg,#7C3AED,#06B6D4);display:flex;align-items:center;justify-content:center;font-size:1.5rem">👨‍💻</div>
      <div>
        <div style="font-size:1.1rem;font-weight:800">Jose Samuel D</div>
        <div style="font-size:12px;color:var(--muted)">Aspiring DevOps and Cloud Engineer</div>
        <div style="font-size:12px;color:var(--muted)">Final Year CSE — Prathyusha Engineering College</div>
      </div>
    </div>
    <div style="display:flex;gap:10px;flex-wrap:wrap">
      <a href="https://github.com/JOSESAMUEL14" target="_blank" style="display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:100px;background:var(--glass);border:1px solid var(--border);color:var(--muted);font-family:Space Mono,monospace;font-size:10px;text-decoration:none"><i class="fa-brands fa-github"></i> GitHub</a>
      <a href="https://linkedin.com/in/samueld14" target="_blank" style="display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:100px;background:var(--glass);border:1px solid var(--border);color:var(--muted);font-family:Space Mono,monospace;font-size:10px;text-decoration:none"><i class="fa-brands fa-linkedin"></i> LinkedIn</a>
      <a href="mailto:Josesamueld2005@gmail.com" style="display:inline-flex;align-items:center;gap:6px;padding:6px 14px;border-radius:100px;background:var(--glass);border:1px solid var(--border);color:var(--muted);font-family:Space Mono,monospace;font-size:10px;text-decoration:none"><i class="fa-solid fa-envelope"></i> Email</a>
    </div>
  </div>
</div>
<script>
const obs=new IntersectionObserver(entries=>{{entries.forEach(e=>{{if(e.isIntersecting)e.target.classList.add("visible");}});}},{{threshold:0.1}});
document.querySelectorAll(".fade-in").forEach(el=>obs.observe(el));
</script>
</body>
</html>'''


@app.route("/architecture")
def architecture():
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Architecture — MultiCloud CI/CD</title>
{BASE_STYLE}
</head>
<body>
{HEX_BG}
{NAV}
<div class="section">
  <div class="section-tag">System Design</div>
  <div class="section-title fade-in"><span class="w">ARCHITECTURE</span><br><span class="a">DIAGRAM</span></div>
  <div class="section-desc fade-in">How all components connect and communicate in this multi-cloud CI/CD system.</div>
  <div class="arch-diagram fade-in">
    <div class="arch-label">Developer Workflow</div>
    <div class="arch-row">
      <div class="arch-box"><div class="arch-box-icon">💻</div><div class="arch-box-name">Developer</div><div class="arch-box-desc">Writes code</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-box"><div class="arch-box-icon"><i class="fa-brands fa-github"></i></div><div class="arch-box-name">GitHub</div><div class="arch-box-desc">git push</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-box"><div class="arch-box-icon">⚡</div><div class="arch-box-name">GitHub Actions</div><div class="arch-box-desc">CI/CD trigger</div></div>
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
    <div class="arch-label">Infrastructure and Monitoring</div>
    <div class="arch-row">
      <div class="arch-box"><div class="arch-box-icon">🏗️</div><div class="arch-box-name">Terraform</div><div class="arch-box-desc">Provisions AWS</div></div>
      <div class="arch-arrow">+</div>
      <div class="arch-box"><div class="arch-box-icon">📊</div><div class="arch-box-name">Prometheus</div><div class="arch-box-desc">Scrapes metrics</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-box"><div class="arch-box-icon">📈</div><div class="arch-box-name">Grafana</div><div class="arch-box-desc">Visualises</div></div>
      <div class="arch-arrow">→</div>
      <div class="arch-box"><div class="arch-box-icon">🔔</div><div class="arch-box-name">Alerts</div><div class="arch-box-desc">On anomalies</div></div>
    </div>
  </div>
  <div class="divider"></div>
  <div class="section-tag" style="margin-top:2rem">Key Concepts</div>
  <div class="grid-2" style="margin-bottom:2rem">
    <div class="card fade-in">
      <div class="card-icon">🐳</div>
      <div class="card-title">Containerisation</div>
      <div class="card-desc">The Flask app is packaged inside a Docker container with everything it needs — Python, dependencies, code. It runs identically on any machine, laptop or cloud server.</div>
    </div>
    <div class="card fade-in">
      <div class="card-icon">☸️</div>
      <div class="card-title">Orchestration</div>
      <div class="card-desc">Kubernetes manages containers. It keeps 2 replicas running always. If one crashes, K8s automatically starts a new one. Rolling updates mean zero downtime.</div>
    </div>
    <div class="card fade-in">
      <div class="card-icon">🏗️</div>
      <div class="card-title">Infrastructure as Code</div>
      <div class="card-desc">Terraform defines the entire AWS infrastructure in code files. Instead of clicking buttons in AWS console, you write code that provisions servers automatically.</div>
    </div>
    <div class="card fade-in">
      <div class="card-icon">📊</div>
      <div class="card-title">Observability</div>
      <div class="card-desc">Prometheus scrapes metrics every 15 seconds. Grafana creates live dashboards showing CPU, memory, request rates. Engineers know about problems before users do.</div>
    </div>
  </div>
</div>
<script>
const obs=new IntersectionObserver(entries=>{{entries.forEach(e=>{{if(e.isIntersecting)e.target.classList.add("visible");}});}},{{threshold:0.1}});
document.querySelectorAll(".fade-in").forEach(el=>obs.observe(el));
</script>
</body>
</html>'''
@app.route("/techstack")
def techstack():
    tools = [
        {"icon":"fa-brands fa-docker","name":"Docker","color":"#2496ED","desc":"Containerisation platform. Packages app and dependencies into portable containers that run anywhere.","why":"Industry standard for containerisation. Used by every major company worldwide.","alt":"Podman, containerd"},
        {"icon":"fa-solid fa-ship","name":"Kubernetes","color":"#326CE5","desc":"Container orchestration system. Manages, scales, and heals containers automatically across servers.","why":"Most popular orchestration platform. K8s skills are highest in demand for DevOps roles.","alt":"Docker Swarm, Nomad"},
        {"icon":"fa-brands fa-github","name":"GitHub Actions","color":"#ffffff","desc":"CI/CD automation built into GitHub. Runs pipelines automatically on every code push.","why":"Free, integrated with GitHub, easy to use. Perfect for open source and student projects.","alt":"Jenkins, GitLab CI, CircleCI"},
        {"icon":"fa-solid fa-layer-group","name":"Terraform","color":"#7B42BC","desc":"Infrastructure as Code tool. Defines cloud resources in code and provisions them automatically.","why":"Works on any cloud provider. Most popular IaC tool in the industry today.","alt":"AWS CloudFormation, Pulumi, Ansible"},
        {"icon":"fa-brands fa-aws","name":"AWS EC2","color":"#FF9900","desc":"Amazon Web Services virtual server. Runs our containerised application in the cloud.","why":"AWS is the largest cloud provider. EC2 knowledge is fundamental for any cloud role.","alt":"GCP Compute Engine, Azure VM"},
        {"icon":"fa-solid fa-chart-line","name":"Prometheus","color":"#E6522C","desc":"Open source monitoring system. Scrapes and stores metrics from applications and servers.","why":"Industry standard for cloud-native monitoring. Used with Kubernetes everywhere.","alt":"Datadog, New Relic, InfluxDB"},
        {"icon":"fa-solid fa-chart-bar","name":"Grafana","color":"#F46800","desc":"Visualisation platform. Creates beautiful dashboards from Prometheus and other data sources.","why":"Most popular open source dashboard tool. Works with 50+ data sources.","alt":"Kibana, Datadog dashboards"},
        {"icon":"fa-brands fa-python","name":"Python Flask","color":"#3776AB","desc":"Lightweight Python web framework. Powers the dashboard application with REST API endpoints.","why":"Simple, fast, perfect for microservices. Python is most popular DevOps scripting language.","alt":"FastAPI, Django, Node.js"},
    ]
    cards = ""
    for tool in tools:
        cards += f'''
        <div class="card fade-in">
          <div style="display:flex;align-items:center;gap:12px;margin-bottom:1rem">
            <div style="width:48px;height:48px;border-radius:14px;background:rgba(255,255,255,0.06);display:flex;align-items:center;justify-content:center;font-size:22px;flex-shrink:0">
              <i class="{tool["icon"]}" style="color:{tool["color"]}"></i>
            </div>
            <div>
              <div style="font-size:1rem;font-weight:800">{tool["name"]}</div>
              <div style="width:40px;height:2px;background:linear-gradient(90deg,{tool["color"]},transparent);margin-top:4px;border-radius:2px"></div>
            </div>
          </div>
          <div style="font-size:13px;color:rgba(255,255,255,0.7);line-height:1.6;margin-bottom:1rem">{tool["desc"]}</div>
          <div style="font-size:11px;color:var(--muted);margin-bottom:6px"><span style="color:{tool["color"]};font-weight:700">Why:</span> {tool["why"]}</div>
          <div style="font-size:11px;color:var(--muted)"><span style="font-weight:700">Alternatives:</span> {tool["alt"]}</div>
        </div>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Tech Stack — MultiCloud CI/CD</title>
{BASE_STYLE}
</head>
<body>
{HEX_BG}
{NAV}
<div class="section">
  <div class="section-tag">Tools and Technologies</div>
  <div class="section-title fade-in"><span class="w">THE TECH</span><br><span class="a">STACK</span></div>
  <div class="section-desc fade-in">8 industry-standard tools used to build this project. Each tool was chosen because it is used by real companies in production environments.</div>
  <div class="grid-2">{cards}</div>
</div>
<script>
const obs=new IntersectionObserver(entries=>{{entries.forEach(e=>{{if(e.isIntersecting)e.target.classList.add("visible");}});}},{{threshold:0.1}});
document.querySelectorAll(".fade-in").forEach(el=>obs.observe(el));
</script>
</body>
</html>'''


@app.route("/pipeline")
def pipeline_page():
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Pipeline — MultiCloud CI/CD</title>
{BASE_STYLE}
</head>
<body>
{HEX_BG}
{NAV}
<div class="section">
  <div class="section-tag">How It Works</div>
  <div class="section-title fade-in"><span class="w">THE</span><br><span class="a">PIPELINE</span></div>
  <div class="section-desc fade-in">From writing a single line of code to seeing it live in production — every step that happens automatically in under 60 seconds.</div>

  <div class="pipe-step fade-in">
    <div class="pipe-num">01</div>
    <div class="pipe-content">
      <div class="pipe-title">Developer Writes Code</div>
      <div class="pipe-desc">A developer makes changes to the Flask application — adding a feature, fixing a bug, or updating the UI. The code lives in a GitHub repository accessible to the entire team.</div>
      <div class="pipe-tag">Local Development</div>
    </div>
  </div>

  <div class="pipe-step fade-in">
    <div class="pipe-num">02</div>
    <div class="pipe-content">
      <div class="pipe-title">Push to GitHub</div>
      <div class="pipe-desc">Developer runs git push origin main. The code uploads to GitHub. This single action triggers the entire automated pipeline instantly.</div>
      <div class="pipe-tag">GitHub</div>
    </div>
  </div>

  <div class="pipe-step fade-in">
    <div class="pipe-num">03</div>
    <div class="pipe-content">
      <div class="pipe-title">GitHub Actions Triggers</div>
      <div class="pipe-desc">GitHub detects the push and automatically starts the CI/CD workflow defined in .github/workflows/deploy.yml. A virtual Ubuntu server spins up on GitHub infrastructure.</div>
      <div class="pipe-tag">GitHub Actions</div>
    </div>
  </div>

  <div class="pipe-step fade-in">
    <div class="pipe-num">04</div>
    <div class="pipe-content">
      <div class="pipe-title">Docker Image Built</div>
      <div class="pipe-desc">GitHub Actions reads the Dockerfile and builds a new Docker image containing the updated application. The image is tagged with the unique commit SHA so every version is traceable.</div>
      <div class="pipe-tag">Docker</div>
    </div>
  </div>

  <div class="pipe-step fade-in">
    <div class="pipe-num">05</div>
    <div class="pipe-content">
      <div class="pipe-title">Image Pushed to Docker Hub</div>
      <div class="pipe-desc">The built image is pushed to Docker Hub — a public registry. This makes the image available to any server in the world tagged as josesamuel14/multicloud-app:latest.</div>
      <div class="pipe-tag">Docker Hub</div>
    </div>
  </div>

  <div class="pipe-step fade-in">
    <div class="pipe-num">06</div>
    <div class="pipe-content">
      <div class="pipe-title">Kubernetes Deploys New Version</div>
      <div class="pipe-desc">Kubernetes pulls the new image and performs a Rolling Update — gradually replacing old containers with new ones. At no point is the application unavailable to users.</div>
      <div class="pipe-tag">Kubernetes</div>
    </div>
  </div>

  <div class="pipe-step fade-in">
    <div class="pipe-num">07</div>
    <div class="pipe-content">
      <div class="pipe-title">Live on AWS and Render</div>
      <div class="pipe-desc">The new version is now live on AWS EC2 Mumbai region and Render simultaneously. The entire process — from git push to live deployment — takes under 60 seconds. Automatically. Every time.</div>
      <div class="pipe-tag">AWS + Render</div>
    </div>
  </div>

  <div class="pipe-step fade-in">
    <div class="pipe-num">08</div>
    <div class="pipe-content">
      <div class="pipe-title">Prometheus Monitors Everything</div>
      <div class="pipe-desc">Prometheus scrapes metrics from the running application every 15 seconds. Grafana displays live dashboards. If anything goes wrong — high CPU, errors, slow responses — engineers are alerted immediately.</div>
      <div class="pipe-tag">Prometheus + Grafana</div>
    </div>
  </div>

  <div class="divider"></div>
  <div class="card fade-in" style="text-align:center;padding:2rem">
    <div style="font-size:2rem;margin-bottom:1rem">⚡</div>
    <div style="font-size:1.3rem;font-weight:800;margin-bottom:0.5rem">Total Time: Under 60 Seconds</div>
    <div style="font-size:14px;color:var(--muted)">From git push to live in production — fully automated, zero manual steps required</div>
  </div>
</div>
<script>
const obs=new IntersectionObserver(entries=>{{entries.forEach(e=>{{if(e.isIntersecting)e.target.classList.add("visible");}});}},{{threshold:0.1}});
document.querySelectorAll(".fade-in").forEach(el=>obs.observe(el));
</script>
</body>
</html>'''
@app.route("/demo")
def demo():
    t = get_theme()
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Live Demo — MultiCloud CI/CD</title>
{BASE_STYLE}
<style>
.demo-card{{background:var(--glass);border:1px solid var(--border);border-radius:20px;padding:2rem;margin-bottom:1.5rem;backdrop-filter:blur(20px)}}
.demo-title{{font-size:1.1rem;font-weight:800;margin-bottom:0.5rem;display:flex;align-items:center;gap:10px}}
.demo-desc{{font-size:13px;color:var(--muted);margin-bottom:1.5rem;line-height:1.6}}
.demo-btn{{display:inline-flex;align-items:center;gap:8px;padding:12px 24px;border-radius:100px;font-family:"Space Mono",monospace;font-size:11px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border:none;cursor:pointer;transition:all 0.3s;text-decoration:none}}
.demo-btn:hover{{transform:translateY(-3px)}}
.demo-btn-primary{{background:linear-gradient(135deg,{t["p1"]},{t["p2"]});color:#fff;box-shadow:0 4px 20px rgba(124,58,237,0.3)}}
.demo-btn-green{{background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);color:#10b981}}
.demo-btn-yellow{{background:rgba(234,179,8,0.1);border:1px solid rgba(234,179,8,0.25);color:#eab308}}
.demo-btn-outline{{background:var(--glass);border:1px solid var(--border);color:#fff}}
.stat-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;margin-top:1rem}}
.stat-item{{background:rgba(0,0,0,0.3);border:1px solid rgba(255,255,255,0.08);border-radius:12px;padding:1rem;text-align:center}}
.stat-val{{font-size:1.5rem;font-weight:800;background:linear-gradient(135deg,{t["p1"]},{t["p2"]});-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.stat-label{{font-family:"Space Mono",monospace;font-size:9px;letter-spacing:2px;text-transform:uppercase;color:var(--muted);margin-top:4px}}
.modal-confirm{{background:linear-gradient(135deg,{t["p1"]},{t["p2"]});color:#fff}}
.modal-cancel{{background:rgba(255,255,255,0.08);color:#fff;border:1px solid rgba(255,255,255,0.15)}}
</style>
</head>
<body>
{HEX_BG}
{NAV}
<div class="modal" id="deployModal">
  <div class="modal-box">
    <div class="modal-title">🚀 Trigger Deployment</div>
    <div class="modal-sub">This will trigger a real GitHub Actions pipeline run — building a new Docker image and deploying it automatically!</div>
    <div class="modal-btns">
      <button class="modal-btn modal-confirm" onclick="confirmDeploy()">Deploy Now</button>
      <button class="modal-btn modal-cancel" onclick="closeModal()">Cancel</button>
    </div>
    <div id="deploy-status" style="margin-top:1rem;font-size:11px;color:var(--muted)"></div>
  </div>
</div>
<div class="section">
  <div class="section-tag">Interactive Demo</div>
  <div class="section-title fade-in"><span class="w">LIVE</span><br><span class="a">DEMO</span></div>
  <div class="section-desc fade-in">Everything below is real and live. Click any button to interact with the actual running system.</div>

  <div class="demo-card fade-in">
    <div class="demo-title"><i class="fa-solid fa-heart-pulse" style="color:#10b981"></i> Health Check</div>
    <div class="demo-desc">Checks if the application is running and returns real system information — cloud provider, region, uptime, and hostname of the actual server running right now.</div>
    <button class="demo-btn demo-btn-green" onclick="checkHealth()"><i class="fa-solid fa-heart-pulse"></i> Check Health</button>
    <div class="response-box" id="health-response"></div>
  </div>

  <div class="demo-card fade-in">
    <div class="demo-title"><i class="fa-solid fa-chart-bar" style="color:#eab308"></i> Live Metrics</div>
    <div class="demo-desc">Fetches real-time statistics from the application — total requests served, current uptime, and system status. Data comes directly from Prometheus metrics endpoint.</div>
    <button class="demo-btn demo-btn-yellow" onclick="checkStats()"><i class="fa-solid fa-chart-bar"></i> Fetch Live Stats</button>
    <div class="stat-grid" id="stats-grid" style="display:none">
      <div class="stat-item"><div class="stat-val" id="stat-req">--</div><div class="stat-label">Total Requests</div></div>
      <div class="stat-item"><div class="stat-val" id="stat-up">--</div><div class="stat-label">Uptime</div></div>
      <div class="stat-item"><div class="stat-val" id="stat-status">--</div><div class="stat-label">Status</div></div>
    </div>
  </div>

  <div class="demo-card fade-in">
    <div class="demo-title"><i class="fa-solid fa-rocket" style="color:#7C3AED"></i> Trigger Pipeline</div>
    <div class="demo-desc">Click Deploy Now to trigger a real GitHub Actions CI/CD pipeline run. A new Docker image will be built and deployed automatically. Watch it happen live on GitHub!</div>
    <div style="display:flex;gap:10px;flex-wrap:wrap">
      <button class="demo-btn demo-btn-primary" onclick="showDeploy()"><i class="fa-solid fa-rocket"></i> Trigger Deploy</button>
      <a href="https://github.com/JOSESAMUEL14/multicloud-cicd/actions" target="_blank" class="demo-btn demo-btn-outline"><i class="fa-brands fa-github"></i> Watch on GitHub</a>
    </div>
  </div>

  <div class="demo-card fade-in">
    <div class="demo-title"><i class="fa-solid fa-code" style="color:#06B6D4"></i> Source Code</div>
    <div class="demo-desc">The entire project is open source. View the Dockerfile, Kubernetes configs, Terraform IaC, GitHub Actions workflow, and monitoring setup on GitHub.</div>
    <div style="display:flex;gap:10px;flex-wrap:wrap">
      <a href="https://github.com/JOSESAMUEL14/multicloud-cicd" target="_blank" class="demo-btn demo-btn-outline"><i class="fa-brands fa-github"></i> View GitHub Repo</a>
      <a href="/metrics" target="_blank" class="demo-btn demo-btn-outline"><i class="fa-solid fa-chart-line"></i> Raw Metrics</a>
    </div>
  </div>
</div>

<script>
async function checkHealth(){{
  const box=document.getElementById("health-response");
  box.classList.add("show");
  box.textContent="Fetching...";
  try{{
    const r=await fetch("/health");
    const d=await r.json();
    box.textContent=JSON.stringify(d,null,2);
  }}catch(e){{box.textContent="Error: "+e.message;}}
}}
async function checkStats(){{
  const grid=document.getElementById("stats-grid");
  grid.style.display="grid";
  try{{
    const r=await fetch("/stats");
    const d=await r.json();
    document.getElementById("stat-req").textContent=d.total_requests||"0";
    document.getElementById("stat-up").textContent=d.uptime||"--";
    document.getElementById("stat-status").textContent=d.status||"--";
  }}catch(e){{console.log(e);}}
}}
function showDeploy(){{document.getElementById("deployModal").classList.add("show");}}
function closeModal(){{document.getElementById("deployModal").classList.remove("show");document.getElementById("deploy-status").textContent="";}}
async function confirmDeploy(){{
  const s=document.getElementById("deploy-status");
  s.textContent="Triggering pipeline...";s.style.color="#eab308";
  try{{
    const r=await fetch("/deploy",{{method:"POST",headers:{{"Content-Type":"application/json"}}}});
    const d=await r.json();
    s.textContent=d.success?"✅ Pipeline triggered! Check GitHub Actions.":"❌ "+d.message;
    s.style.color=d.success?"#10b981":"#ef4444";
  }}catch(e){{s.textContent="❌ "+e.message;s.style.color="#ef4444";}}
}}
setInterval(checkStats,5000);
checkStats();
const obs=new IntersectionObserver(entries=>{{entries.forEach(e=>{{if(e.isIntersecting)e.target.classList.add("visible");}});}},{{threshold:0.1}});
document.querySelectorAll(".fade-in").forEach(el=>obs.observe(el));
</script>
</body>
</html>'''


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
    data = {
        "status": "HEALTHY",
        "total_requests": int(total),
        "uptime": get_uptime(),
        "cloud": os.getenv("CLOUD_PROVIDER", "local"),
        "hostname": socket.gethostname()
    }
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
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github.v3+json",
                "Content-Type": "application/json"
            },
            json={"event_type": "manual-deploy"},
            timeout=10
        )
        if r.status_code == 204:
            return jsonify({"success": True, "message": "Pipeline triggered!"})
        else:
            return jsonify({"success": False, "message": f"GitHub API error: {r.status_code}"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)