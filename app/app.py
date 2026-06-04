from flask import Flask, jsonify, request
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
    github_token = os.getenv("GITHUB_TOKEN", "")
    has_token = "true" if github_token else "false"

    themes = {
        "aws":    {"p1":"#FF9900","p2":"#FF6B35","p3":"#FFD700","label":"Amazon Web Services","short":"AWS"},
        "gcp":    {"p1":"#4285F4","p2":"#34A853","p3":"#FBBC05","label":"Google Cloud Platform","short":"GCP"},
        "render": {"p1":"#7C3AED","p2":"#06B6D4","p3":"#EC4899","label":"Render Cloud","short":"RENDER"},
        "local":  {"p1":"#7C3AED","p2":"#06B6D4","p3":"#EC4899","label":"Local Kubernetes","short":"LOCAL"}
    }
    t = themes.get(cloud.lower(), themes["local"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>MultiCloud CI/CD</title>
<link href="https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{--p1:{t['p1']};--p2:{t['p2']};--bg:#06061a;--glass:rgba(255,255,255,0.04);--border:rgba(255,255,255,0.08);--muted:rgba(255,255,255,0.38)}}
html,body{{width:100%;min-height:100vh;overflow-x:hidden}}
body{{font-family:'Exo 2',sans-serif;background:var(--bg);color:#fff;display:flex;align-items:center;justify-content:center;padding:1rem}}
#cv{{position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}}
.vig{{position:fixed;inset:0;z-index:1;pointer-events:none;background:radial-gradient(ellipse at 50% 50%,transparent 25%,rgba(6,6,26,0.7) 100%)}}
.wrap{{position:relative;z-index:10;width:100%;max-width:900px;padding:1rem 1.2rem;display:flex;flex-direction:column;align-items:center;gap:1.1rem}}
.pill{{display:inline-flex;align-items:center;gap:8px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);backdrop-filter:blur(16px);padding:6px 18px;border-radius:100px;font-size:10px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--muted);animation:fadeDown 0.6s cubic-bezier(.16,1,.3,1)}}
.pill-dot{{width:7px;height:7px;border-radius:50%;background:var(--p1);box-shadow:0 0 10px var(--p1);animation:blink 2s infinite}}
@keyframes blink{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:0.3;transform:scale(0.6)}}}}
.hero{{text-align:center;animation:fadeUp 0.7s cubic-bezier(.16,1,.3,1)}}
.hero-eye{{font-size:9px;font-weight:600;letter-spacing:4px;text-transform:uppercase;color:var(--muted);margin-bottom:0.5rem;display:flex;align-items:center;justify-content:center;gap:12px}}
.hero-eye::before,.hero-eye::after{{content:'';width:40px;height:1px;background:linear-gradient(90deg,transparent,rgba(255,255,255,0.2))}}
.hero-eye::after{{background:linear-gradient(90deg,rgba(255,255,255,0.2),transparent)}}
h1{{font-size:clamp(2.2rem,5.5vw,4rem);font-weight:900;letter-spacing:-1px;line-height:0.92;margin-bottom:0.5rem}}
h1 .w{{color:#ffffff}}
h1 .a{{background:linear-gradient(135deg,var(--p1),var(--p2));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}}
.hero-sub{{font-size:9px;font-weight:600;letter-spacing:3px;text-transform:uppercase;color:var(--muted);display:flex;align-items:center;justify-content:center;gap:10px;flex-wrap:wrap}}
.dot{{width:3px;height:3px;border-radius:50%;background:var(--p1);opacity:0.5}}
.pipeline{{width:100%;background:rgba(255,255,255,0.025);border:1px solid rgba(255,255,255,0.07);border-radius:20px;padding:1.2rem 1.5rem;backdrop-filter:blur(30px);display:flex;align-items:center;justify-content:space-between;position:relative;overflow:hidden;animation:fadeUp 0.9s cubic-bezier(.16,1,.3,1)}}
.pipeline::before{{content:'PIPELINE';position:absolute;top:8px;left:16px;font-size:7px;font-weight:800;letter-spacing:3px;color:rgba(255,255,255,0.1)}}
.pstep{{display:flex;flex-direction:column;align-items:center;gap:7px;flex:1}}
.p-icon{{width:48px;height:48px;border-radius:14px;background:transparent;border:2px solid var(--p1);display:flex;align-items:center;justify-content:center;font-size:18px;position:relative;transition:all 0.4s cubic-bezier(.16,1,.3,1);box-shadow:0 0 10px color-mix(in srgb,var(--p1) 25%,transparent),inset 0 0 10px color-mix(in srgb,var(--p1) 8%,transparent)}}
.p-icon:hover{{transform:translateY(-6px) scale(1.08);box-shadow:0 0 22px color-mix(in srgb,var(--p1) 55%,transparent),0 0 45px color-mix(in srgb,var(--p1) 25%,transparent);border-color:var(--p2)}}
.p-icon i{{font-size:20px;color:#fff}}
.p-icon svg{{width:22px;height:22px}}
.p-label{{font-size:8px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--muted)}}
.pconn{{flex:1;display:flex;align-items:center;padding-bottom:24px}}
.pline{{width:100%;height:1.5px;background:linear-gradient(90deg,var(--p1),var(--p2));opacity:0.2;position:relative;overflow:hidden;border-radius:2px}}
.pline::after{{content:'';position:absolute;top:0;left:-50%;width:30%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,1),transparent);animation:sweep 2s linear infinite}}
@keyframes sweep{{to{{left:150%}}}}
.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;width:100%;animation:fadeUp 1.1s cubic-bezier(.16,1,.3,1)}}
.card{{background:rgba(10,10,30,0.85);border-radius:16px;padding:1rem 1rem;display:flex;flex-direction:column;gap:8px;position:relative;overflow:hidden;box-shadow:0 8px 32px rgba(0,0,0,0.5),0 0 0 1px rgba(255,255,255,0.06),inset 0 1px 0 rgba(255,255,255,0.08);border-top:1px solid rgba(226,232,240,0.2);transition:all 0.5s cubic-bezier(.16,1,.3,1);cursor:default;transform-style:preserve-3d}}
.card::after{{content:'';position:absolute;bottom:0;left:0;right:0;height:2px;background:linear-gradient(90deg,#94a3b8,#ffffff,#94a3b8);opacity:0.4;animation:bargl 3s ease-in-out infinite alternate}}
@keyframes bargl{{from{{opacity:0.2}}to{{opacity:0.7}}}}
.card:hover{{transform:perspective(400px) rotateX(8deg) rotateY(-3deg) translateY(-8px) scale(1.03);box-shadow:0 25px 70px rgba(0,0,0,0.7),0 0 0 1px rgba(255,255,255,0.12),inset 0 1px 0 rgba(255,255,255,0.15)}}
.card-top{{display:flex;align-items:center;justify-content:space-between}}
.card-icon{{width:34px;height:34px;border-radius:10px;background:linear-gradient(135deg,#94a3b8,#ffffff);display:flex;align-items:center;justify-content:center;font-size:14px;color:#06061a;box-shadow:0 4px 14px rgba(255,255,255,0.2);transition:transform 0.5s cubic-bezier(.16,1,.3,1);flex-shrink:0}}
.card:hover .card-icon{{transform:rotate(-12deg) scale(1.15)}}
.card-ping{{width:6px;height:6px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;animation:blink 2s infinite}}
.card-label{{font-size:8px;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:rgba(255,255,255,0.3)}}
.card-value{{font-size:1rem;font-weight:800;background:linear-gradient(135deg,#e2e8f0,#ffffff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;line-height:1.1}}
.card-sub{{font-size:9px;color:rgba(255,255,255,0.2);font-weight:400}}
.card-live{{font-size:8px;color:#10b981;font-weight:600;letter-spacing:1px}}
.actions{{display:flex;gap:8px;flex-wrap:wrap;justify-content:center;width:100%;animation:fadeUp 1.2s cubic-bezier(.16,1,.3,1)}}
.btn-action{{display:inline-flex;align-items:center;gap:7px;padding:10px 18px;border-radius:100px;font-size:10px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;border:none;cursor:pointer;transition:all 0.3s;text-decoration:none;font-family:'Exo 2',sans-serif}}
.btn-action:hover{{transform:translateY(-3px)}}
.btn-deploy{{background:linear-gradient(135deg,var(--p1),var(--p2));color:#fff;box-shadow:0 4px 20px color-mix(in srgb,var(--p1) 40%,transparent)}}
.btn-github{{background:rgba(255,255,255,0.08);border:1px solid rgba(255,255,255,0.15);color:#fff}}
.btn-health{{background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.25);color:#10b981}}
.btn-metrics{{background:rgba(234,179,8,0.1);border:1px solid rgba(234,179,8,0.25);color:#eab308}}
.statusbar{{display:flex;align-items:center;gap:8px;flex-wrap:wrap;justify-content:center;animation:fadeUp 1.3s cubic-bezier(.16,1,.3,1)}}
.chip{{display:inline-flex;align-items:center;gap:7px;padding:8px 16px;border-radius:100px;font-size:9px;font-weight:700;letter-spacing:1.5px;text-transform:uppercase;backdrop-filter:blur(16px);transition:all 0.3s;cursor:default}}
.chip:hover{{transform:translateY(-3px)}}
.chip-green{{background:rgba(16,185,129,0.08);border:1px solid rgba(16,185,129,0.25);color:#10b981}}
.chip-white{{background:rgba(255,255,255,0.06);border:1px solid rgba(255,255,255,0.15);color:rgba(255,255,255,0.7)}}
.chip-mono{{background:var(--glass);border:1px solid var(--border);color:var(--muted)}}
.modal{{display:none;position:fixed;inset:0;z-index:100;align-items:center;justify-content:center;background:rgba(0,0,0,0.7);backdrop-filter:blur(10px)}}
.modal.show{{display:flex}}
.modal-box{{background:#0d0d1a;border:1px solid rgba(255,255,255,0.1);border-radius:20px;padding:2rem;max-width:400px;width:90%;text-align:center}}
.modal-title{{font-size:1.2rem;font-weight:800;margin-bottom:0.5rem}}
.modal-sub{{font-size:12px;color:var(--muted);margin-bottom:1.5rem;line-height:1.6}}
.modal-btns{{display:flex;gap:10px;justify-content:center}}
.modal-btn{{padding:10px 24px;border-radius:100px;font-size:11px;font-weight:700;letter-spacing:1px;cursor:pointer;border:none;transition:all 0.3s;font-family:'Exo 2',sans-serif}}
.modal-confirm{{background:linear-gradient(135deg,var(--p1),var(--p2));color:#fff}}
.modal-cancel{{background:rgba(255,255,255,0.08);color:#fff;border:1px solid rgba(255,255,255,0.15)}}
@keyframes fadeDown{{from{{opacity:0;transform:translateY(-18px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes fadeUp{{from{{opacity:0;transform:translateY(22px)}}to{{opacity:1;transform:translateY(0)}}}}
@media(max-width:640px){{.cards{{grid-template-columns:1fr 1fr}}.p-icon{{width:38px;height:38px}}h1{{font-size:2rem}}}}
</style>
</head>
<body>
<canvas id="cv"></canvas>
<div class="vig"></div>
<div class="modal" id="deployModal">
  <div class="modal-box">
    <div class="modal-title">🚀 Trigger Deployment</div>
    <div class="modal-sub">This will trigger a new GitHub Actions pipeline run — building and deploying the latest version automatically!</div>
    <div class="modal-btns">
      <button class="modal-btn modal-confirm" onclick="confirmDeploy()">Deploy Now</button>
      <button class="modal-btn modal-cancel" onclick="closeModal()">Cancel</button>
    </div>
    <div id="deploy-status" style="margin-top:1rem;font-size:11px;color:var(--muted)"></div>
  </div>
</div>
<div class="wrap">
  <div class="pill"><span class="pill-dot"></span>{t['short']} &nbsp;·&nbsp; {t['label']} &nbsp;·&nbsp; Live</div>
  <div class="hero">
    <div class="hero-eye">Multi · Cloud · Infrastructure</div>
    <h1><span class="w">MULTI</span><span class="a">CLOUD</span><br><span class="w">CI</span><span class="a">/</span><span class="w">CD</span></h1>
    <div class="hero-sub">Kubernetes<span class="dot"></span>Docker<span class="dot"></span>GitHub Actions<span class="dot"></span>Terraform<span class="dot"></span>AWS · GCP</div>
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
    <div class="pstep">
      <div class="p-icon">{'<i class="fa-brands fa-aws"></i>' if cloud.lower()=='aws' else '<i class="fa-brands fa-google"></i>' if cloud.lower()=='gcp' else '<i class="fa-solid fa-cloud"></i>'}</div>
      <div class="p-label">{'AWS' if cloud.lower()=='aws' else 'GCP' if cloud.lower()=='gcp' else 'Cloud'}</div>
    </div>
  </div>
  <div class="cards">
    <div class="card">
      <div class="card-top"><div class="card-icon"><i class="fa-solid fa-cloud"></i></div><div class="card-ping"></div></div>
      <div class="card-label">Cloud Provider</div>
      <div class="card-value">{cloud.upper()}</div>
      <div class="card-sub">Active environment</div>
    </div>
    <div class="card">
      <div class="card-top"><div class="card-icon"><i class="fa-solid fa-location-dot"></i></div><div class="card-ping"></div></div>
      <div class="card-label">Region</div>
      <div class="card-value">{region}</div>
      <div class="card-sub">Deployment zone</div>
    </div>
    <div class="card">
      <div class="card-top"><div class="card-icon"><i class="fa-solid fa-microchip"></i></div><div class="card-ping"></div></div>
      <div class="card-label">Requests</div>
      <div class="card-value" id="req-count">--</div>
      <div class="card-live">↻ live</div>
    </div>
    <div class="card">
      <div class="card-top"><div class="card-icon"><i class="fa-solid fa-clock"></i></div><div class="card-ping"></div></div>
      <div class="card-label">Uptime</div>
      <div class="card-value" id="uptime">--</div>
      <div class="card-live">↻ live</div>
    </div>
    <div class="card">
      <div class="card-top"><div class="card-icon"><i class="fa-brands fa-docker"></i></div><div class="card-ping"></div></div>
      <div class="card-label">Container</div>
      <div class="card-value">Docker</div>
      <div class="card-sub">Image registry</div>
    </div>
    <div class="card">
      <div class="card-top"><div class="card-icon"><i class="fa-brands fa-python"></i></div><div class="card-ping"></div></div>
      <div class="card-label">Python</div>
      <div class="card-value">{python_ver}</div>
      <div class="card-sub">Runtime version</div>
    </div>
    <div class="card">
      <div class="card-top"><div class="card-icon"><i class="fa-solid fa-circle-nodes"></i></div><div class="card-ping"></div></div>
      <div class="card-label">Replicas</div>
      <div class="card-value">2 / 2</div>
      <div class="card-sub">All pods healthy</div>
    </div>
    <div class="card">
      <div class="card-top"><div class="card-icon"><i class="fa-solid fa-heart-pulse"></i></div><div class="card-ping"></div></div>
      <div class="card-label">Health</div>
      <div class="card-value" id="health-status">--</div>
      <div class="card-live">↻ live</div>
    </div>
  </div>
  <div class="actions">
    <button class="btn-action btn-deploy" onclick="showDeploy()"><i class="fa-solid fa-rocket"></i> Trigger Deploy</button>
    <a href="https://github.com/{github_repo}/actions" target="_blank" class="btn-action btn-github"><i class="fa-brands fa-github"></i> View Pipeline</a>
    <a href="/health" target="_blank" class="btn-action btn-health"><i class="fa-solid fa-heart-pulse"></i> Health Check</a>
    <a href="/metrics" target="_blank" class="btn-action btn-metrics"><i class="fa-solid fa-chart-bar"></i> Metrics</a>
  </div>
  <div class="statusbar">
    <div class="chip chip-green"><span style="width:6px;height:6px;border-radius:50%;background:#10b981;box-shadow:0 0 8px #10b981;animation:blink 1.5s infinite;display:inline-block"></span> All Systems Operational</div>
    <div class="chip chip-white"><i class="fa-solid fa-bolt"></i> Auto-Deploy Active</div>
    <div class="chip chip-mono" id="clk">--:--:--</div>
  </div>
</div>
<script>
const HAS_TOKEN = {has_token};
function tick(){{const n=new Date();document.getElementById('clk').textContent=n.toTimeString().slice(0,8);}}
setInterval(tick,1000);tick();
async function updateLiveMetrics(){{
  try{{
    const r=await fetch('/stats');
    const d=await r.json();
    document.getElementById('req-count').textContent=d.total_requests||'0';
    document.getElementById('uptime').textContent=d.uptime||'--';
    document.getElementById('health-status').textContent=d.status||'--';
  }}catch(e){{console.log('metrics error',e);}}
}}
setInterval(updateLiveMetrics,5000);
updateLiveMetrics();
function showDeploy(){{document.getElementById('deployModal').classList.add('show');}}
function closeModal(){{document.getElementById('deployModal').classList.remove('show');document.getElementById('deploy-status').textContent='';}}
async function confirmDeploy(){{
  const status=document.getElementById('deploy-status');
  status.textContent='Triggering pipeline...';
  status.style.color='#eab308';
  try{{
    const r=await fetch('/deploy',{{method:'POST',headers:{{'Content-Type':'application/json'}}}});
    const d=await r.json();
    if(d.success){{
      status.textContent='✅ Pipeline triggered! Check GitHub Actions.';
      status.style.color='#10b981';
    }}else{{
      status.textContent='❌ '+d.message;
      status.style.color='#ef4444';
    }}
  }}catch(e){{
    status.textContent='❌ Error: '+e.message;
    status.style.color='#ef4444';
  }}
}}
const cv=document.getElementById('cv'),ctx=cv.getContext('2d');
let W,H,t=0;
function rsz(){{W=cv.width=innerWidth;H=cv.height=innerHeight;}}
rsz();window.addEventListener('resize',rsz);
const S=26;
function draw(){{
  ctx.fillStyle='#06061a';ctx.fillRect(0,0,W,H);
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
        metrics_data = requests.get(
            "http://localhost:5000/metrics",
            timeout=2
        ).text
        total = 0
        for line in metrics_data.split('\n'):
            if 'flask_http_request_total' in line and not line.startswith('#'):
                try:
                    total += float(line.split(' ')[-1])
                except:
                    pass
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
        return jsonify({{"success": False, "message": "GITHUB_TOKEN not configured"}}), 200
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
            return jsonify({{"success": False, "message": f"GitHub API error: {{r.status_code}} - {{r.text}}"}}), 200
    except Exception as e:
        return jsonify({{"success": False, "message": str(e)}}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
