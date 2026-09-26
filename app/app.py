from flask import Flask, jsonify, request
import os, platform, socket, time, requests, hmac
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'MultiCloud CI/CD App', version='1.0.0')

START_TIME = time.time()
total_requests = 0

@app.before_request
def count_requests():
    global total_requests
    total_requests += 1

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
    
    cloud_label = "AWS" if cloud.lower()=="aws" else "GCP" if cloud.lower()=="gcp" else "Render" if cloud.lower()=="render" else "Cloud"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<meta name="description" content="Multi-Cloud CI/CD Deployment System — Release Engineering Architecture & Portfolio Experience by Samuel D">
<title>Multi-Cloud CI/CD Deployment System — The Complete Journey</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
<style>
:root {{
  --bg-space: #030712;
  --bg-charcoal: #0F172A;
  --bg-surface-3d: rgba(15, 23, 42, 0.88);
  
  --orange-launch: #FF6B00;
  --aws-orange: #FF9900;
  --docker-blue: #099CEC;
  --k8s-blue: #326CE5;
  --github-dark: #1E293B;
  --sec-green: #10B981;
  --sec-red: #EF4444;
  --cyan-beam: #06B6D4;
  --purple-space: #8B5CF6;
  
  --text-main: #F8FAFC;
  --text-dim: #94A3B8;
  
  --border-light: rgba(255, 255, 255, 0.12);
  --border-orange: rgba(255, 107, 0, 0.4);
  --border-cyan: rgba(6, 182, 212, 0.4);
  
  --shadow-cinematic: 0 30px 80px rgba(0, 0, 0, 0.75), 0 0 40px rgba(255, 107, 0, 0.15);
  
  --tilt-x: 0deg;
  --tilt-y: 0deg;
}}

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

html {{ scroll-behavior: smooth; font-family: 'Plus Jakarta Sans', sans-serif; }}

section[id], main[id] {{
  scroll-margin-top: 100px;
}}

body {{
  background: var(--bg-space);
  color: var(--text-main);
  min-height: 100vh;
  overflow-x: hidden;
  perspective: none;
  position: relative;
  background-image: 
    radial-gradient(circle at 50% 15%, rgba(255, 107, 0, 0.14), transparent 50%),
    radial-gradient(circle at 15% 75%, rgba(6, 182, 212, 0.12), transparent 45%),
    radial-gradient(circle at 85% 85%, rgba(139, 92, 246, 0.12), transparent 45%),
    linear-gradient(180deg, #020617 0%, #030712 100%);
  background-attachment: fixed;
}}

/* Atmospheric Stars Background */
body::before {{
  content: "";
  position: fixed;
  inset: -100px;
  background-image: 
    radial-gradient(2px 2px at 40px 60px, rgba(255, 255, 255, 0.6), transparent),
    radial-gradient(1.5px 1.5px at 120px 180px, rgba(255, 165, 0, 0.5), transparent),
    radial-gradient(2px 2px at 280px 90px, rgba(6, 182, 212, 0.5), transparent),
    radial-gradient(1.5px 1.5px at 400px 320px, rgba(255, 255, 255, 0.4), transparent);
  background-size: 300px 300px;
  pointer-events: none;
  z-index: 0;
  animation: starRotate 140s linear infinite;
}}

@keyframes starRotate {{
  0% {{ transform: rotate(0deg); }}
  100% {{ transform: rotate(360deg); }}
}}

a {{ color: inherit; text-decoration: none; }}

/* NAVIGATION BAR */
.nav-space {{
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  background: rgba(3, 7, 18, 0.85);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-bottom: 1px solid var(--border-light);
}}

.nav-inner {{
  max-width: 1400px;
  margin: 0 auto;
  padding: 16px 32px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}}

.brand-space {{
  display: flex;
  align-items: center;
  gap: 14px;
}}

.brand-space-icon {{
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, var(--orange-launch), var(--aws-orange));
  display: flex;
  align-items: center;
  justify-content: center;
  color: #FFF;
  font-size: 20px;
  box-shadow: 0 0 25px rgba(255, 107, 0, 0.5);
  transform: rotate(-5deg);
}}

.brand-space-text h1 {{
  font-size: 18px;
  font-weight: 900;
  letter-spacing: -0.5px;
  background: linear-gradient(90deg, #FFFFFF, #CBD5E1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}}

.brand-space-text span {{
  display: block;
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: var(--orange-launch);
  letter-spacing: 2px;
  text-transform: uppercase;
}}

.nav-links-space {{
  display: flex;
  gap: 24px;
  list-style: none;
}}

.nav-link-item {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: var(--text-dim);
  font-weight: 600;
  transition: all 0.25s ease;
}}

.nav-link-item:hover {{
  color: var(--orange-launch);
  text-shadow: 0 0 10px rgba(255, 107, 0, 0.6);
}}

.live-indicator-pill {{
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 14px;
  border-radius: 999px;
  background: rgba(16, 185, 129, 0.12);
  border: 1px solid rgba(16, 185, 129, 0.3);
  color: var(--sec-green);
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
}}

.pulse-dot-green {{
  width: 8px; height: 8px;
  border-radius: 50%;
  background: var(--sec-green);
  box-shadow: 0 0 10px var(--sec-green);
  animation: pulseGreen 2s infinite;
}}

@keyframes pulseGreen {{
  0%, 100% {{ transform: scale(0.95); opacity: 0.8; }}
  50% {{ transform: scale(1.2); opacity: 1; }}
}}

/* BUTTON STYLES */
.btn-launch {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 14px 32px;
  border-radius: 14px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  border: 1px solid rgba(255, 255, 255, 0.3);
  background: linear-gradient(135deg, var(--orange-launch), var(--aws-orange));
  color: #FFF;
  box-shadow: 0 12px 35px rgba(255, 107, 0, 0.4), inset 0 1px 0 rgba(255, 255, 255, 0.4);
}}

.btn-launch:hover {{
  transform: translateY(-3px) scale(1.02);
  box-shadow: 0 20px 45px rgba(255, 107, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.6);
}}

.btn-explore {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 14px 28px;
  border-radius: 14px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid var(--border-light);
  background: rgba(255, 255, 255, 0.05);
  color: var(--text-main);
  backdrop-filter: blur(10px);
}}

.btn-explore:hover {{
  border-color: var(--cyan-beam);
  color: var(--cyan-beam);
  transform: translateY(-3px);
  box-shadow: 0 0 25px rgba(6, 182, 212, 0.3);
}}

/* CONTAINER & WRAPPER */
.section-wrapper {{
  max-width: 1400px;
  margin: 0 auto;
  padding: 110px 32px 80px;
  position: relative;
  z-index: 1;
}}

/* 1. HERO SECTION */
.hero-space-container {{
  min-height: 85vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  position: relative;
  padding-top: 30px;
  transform-style: preserve-3d;
}}

.hero-status-pill {{
  display: inline-flex;
  align-items: center;
  gap: 12px;
  padding: 8px 20px;
  border-radius: 999px;
  background: rgba(255, 107, 0, 0.1);
  border: 1px solid rgba(255, 107, 0, 0.3);
  color: var(--orange-launch);
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  margin-bottom: 24px;
}}

.hero-headline {{
  font-size: 62px;
  font-weight: 900;
  line-height: 1.05;
  letter-spacing: -2px;
  margin-bottom: 20px;
  max-width: 920px;
}}

.hero-headline .text-glow-orange {{
  background: linear-gradient(135deg, #FFF, var(--orange-launch), var(--aws-orange));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0 0 30px rgba(255, 107, 0, 0.4));
}}

.hero-subheadline {{
  font-size: 18px;
  color: var(--text-dim);
  max-width: 720px;
  line-height: 1.7;
  margin-bottom: 36px;
}}

.hero-cta-flex {{
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 50px;
}}

/* ROCKET LAUNCH FACILITY CANVAS */
.rocket-launch-facility {{
  width: 100%;
  max-width: 920px;
  height: 360px;
  background: linear-gradient(180deg, rgba(15, 23, 42, 0.6), rgba(3, 7, 18, 0.95));
  border: 1px solid var(--border-light);
  border-radius: 32px;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-cinematic);
  transform: rotateX(var(--tilt-y)) rotateY(var(--tilt-x));
  transition: transform 0.15s ease-out;
  display: flex;
  align-items: center;
  justify-content: center;
}}

.rocket-launch-pad {{
  position: relative;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  height: 100%;
  padding-bottom: 35px;
}}

.rocket-object {{
  width: 90px;
  height: 180px;
  position: relative;
  transition: transform 1.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  filter: drop-shadow(0 10px 20px rgba(0,0,0,0.7));
  transform-style: preserve-3d;
}}

.rocket-object.launching {{
  transform: translateY(-420px) scale(0.5);
}}

.rocket-flame {{
  position: absolute;
  bottom: -35px;
  left: 50%;
  transform: translateX(-50%);
  width: 28px;
  height: 45px;
  background: linear-gradient(180deg, #FFF, var(--orange-launch), transparent);
  border-radius: 50% 50% 20% 20%;
  filter: blur(2px);
  box-shadow: 0 0 30px var(--orange-launch);
  opacity: 0;
  transition: opacity 0.3s ease;
}}

.rocket-object.launching .rocket-flame {{
  opacity: 1;
  animation: flameFlicker 0.1s infinite alternate;
}}

@keyframes flameFlicker {{
  0% {{ transform: translateX(-50%) scaleY(1); }}
  100% {{ transform: translateX(-50%) scaleY(1.3); }}
}}

.orbit-station-node {{
  position: absolute;
  padding: 10px 16px;
  background: rgba(15, 23, 42, 0.85);
  border: 1px solid var(--border-light);
  border-radius: 12px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 8px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.5);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}}

.st-1 {{ top: 40px; left: 50px; }}
.st-2 {{ top: 140px; left: 30px; }}
.st-3 {{ top: 240px; left: 60px; }}
.st-4 {{ top: 40px; right: 50px; }}
.st-5 {{ top: 140px; right: 30px; }}
.st-6 {{ top: 240px; right: 60px; }}

/* STORY SECTIONS HEADER STYLING */
.story-section {{
  margin-bottom: 110px;
}}

.story-header {{
  text-align: center;
  margin-bottom: 50px;
}}

.story-num {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 800;
  color: var(--orange-launch);
  letter-spacing: 3px;
  margin-bottom: 8px;
}}

.story-title {{
  font-size: 36px;
  font-weight: 900;
  letter-spacing: -1px;
  margin-bottom: 12px;
}}

.story-desc {{
  font-size: 15px;
  color: var(--text-dim);
  max-width: 680px;
  margin: 0 auto;
  line-height: 1.6;
}}

/* 2. PROJECT OVERVIEW CARD */
.project-intro-card {{
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(3, 7, 18, 0.95));
  border: 1px solid var(--border-light);
  border-radius: 28px;
  padding: 40px;
  box-shadow: var(--shadow-cinematic);
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 32px;
  align-items: center;
}}

/* EVOLUTION CARDS GRID */
.evolution-cards-grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-top: 36px;
}}

.evolution-card {{
  background: rgba(15, 23, 42, 0.85);
  border: 1px solid var(--border-light);
  border-radius: 20px;
  padding: 24px;
  transition: all 0.3s ease;
}}

.evolution-card:hover {{
  border-color: var(--orange-launch);
  transform: translateY(-5px);
  box-shadow: 0 12px 30px rgba(255, 107, 0, 0.2);
}}

.evolution-icon {{
  font-size: 24px;
  color: var(--orange-launch);
  margin-bottom: 12px;
}}

/* ARCHITECTURE DIAGRAM FLOW */
.arch-flow-box {{
  background: rgba(15, 23, 42, 0.85);
  border: 1px solid var(--border-light);
  border-radius: 24px;
  padding: 32px;
  margin-top: 40px;
  box-shadow: var(--shadow-cinematic);
}}

.arch-flow-grid {{
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 10px;
  margin-top: 20px;
}}

.arch-node {{
  background: rgba(30, 41, 59, 0.85);
  border: 1px solid var(--border-light);
  padding: 10px 14px;
  border-radius: 12px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 700;
  color: var(--text-main);
  text-align: center;
  line-height: 1.3;
}}

.arch-node.arch-k8s {{
  border-color: var(--k8s-blue);
  color: #93C5FD;
  background: rgba(50, 108, 229, 0.15);
}}

.arch-node.arch-aws {{
  border-color: var(--aws-orange);
  color: #FDBA74;
  background: rgba(255, 153, 0, 0.15);
}}

.arch-node.arch-render {{
  border-color: var(--purple-space);
  color: #DDD6FE;
  background: rgba(139, 92, 246, 0.15);
}}

.arch-arrow {{
  color: var(--orange-launch);
  font-weight: 900;
  font-size: 13px;
}}

/* 3. 16-STAGE DEPLOYMENT JOURNEY GRID & INTERACTIVE CARDS */
.journey-16-grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 18px;
}}

.journey-step-card {{
  background: rgba(15, 23, 42, 0.75);
  border: 1px solid var(--border-light);
  border-radius: 18px;
  padding: 22px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 185px;
  transition: all 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  position: relative;
  cursor: pointer;
  outline: none;
}}

.journey-step-card:hover, .journey-step-card:focus, .journey-step-card.pop-active {{
  border-color: var(--orange-launch);
  transform: translateY(-6px) translateZ(15px);
  box-shadow: 0 15px 35px rgba(255, 107, 0, 0.25);
}}

.step-num-badge {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  font-weight: 800;
  color: var(--orange-launch);
  background: rgba(255, 107, 0, 0.12);
  padding: 3px 8px;
  border-radius: 6px;
  border: 1px solid rgba(255, 107, 0, 0.3);
  width: fit-content;
}}

.step-hover-hint {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: var(--cyan-beam);
  margin-top: 8px;
  display: flex;
  align-items: center;
  gap: 4px;
  opacity: 0.8;
  transition: opacity 0.2s ease;
}}

.journey-step-card:hover .step-hover-hint {{
  opacity: 1;
  color: var(--orange-launch);
}}

/* CINEMATIC STAGE POPOVER PANEL */
.stage-popover {{
  position: fixed;
  z-index: 999999;
  width: 360px;
  max-width: 90vw;
  background: rgba(10, 18, 32, 0.96);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border: 1.5px solid var(--orange-launch);
  border-radius: 18px;
  padding: 20px;
  box-shadow: 0 25px 60px rgba(0, 0, 0, 0.85), 0 0 30px rgba(255, 107, 0, 0.3);
  pointer-events: none;
  opacity: 0;
  visibility: hidden;
  transform: translateY(8px);
  transition: opacity 0.2s ease, transform 0.2s ease, visibility 0.2s;
}}

.stage-popover.visible {{
  opacity: 1;
  visibility: visible;
  transform: translateY(0);
}}

.popover-header {{
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
  padding-bottom: 10px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08);
}}

.popover-stage-pill {{
  flex-shrink: 0;
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  font-weight: 800;
  letter-spacing: 0.8px;
  padding: 4px 8px;
  border-radius: 6px;
  background: rgba(255, 107, 0, 0.14);
  color: var(--orange-launch);
  border: 1px solid rgba(255, 107, 0, 0.35);
}}

.popover-title {{
  font-size: 15px;
  font-weight: 850;
  color: #F8FAFC;
  letter-spacing: 0.1px;
  line-height: 1.3;
}}

.popover-field {{
  margin-bottom: 13px;
}}

.popover-label {{
  font-family: 'JetBrains Mono', monospace;
  font-size: 9.5px;
  font-weight: 800;
  color: var(--cyan-beam);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 5px;
  display: flex;
  align-items: center;
  gap: 6px;
}}

.popover-text {{
  font-size: 12px;
  color: #CBD5E1;
  line-height: 1.55;
}}

.popover-flow-box {{
  background: rgba(3, 7, 18, 0.72);
  border: 1px solid rgba(6, 182, 212, 0.22);
  border-radius: 8px;
  padding: 8px 10px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 10.5px;
  color: var(--cyan-beam);
  font-weight: 700;
  line-height: 1.5;
  box-shadow: inset 0 0 18px rgba(6, 182, 212, 0.04);
}}

/* 4. START -> FINISH SUMMARY BANNER */
.start-finish-banner {{
  background: linear-gradient(135deg, rgba(255, 107, 0, 0.12), rgba(6, 182, 212, 0.12));
  border: 1px solid var(--border-orange);
  border-radius: 24px;
  padding: 32px;
  text-align: center;
  margin-top: 36px;
}}

/* 5. INSIDE THE PIPELINE 3-LAYERS */
.layers-pipeline-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}}

.layer-card-3d {{
  background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(5, 11, 20, 0.95));
  border: 1px solid var(--border-light);
  border-radius: 24px;
  padding: 30px;
  box-shadow: var(--shadow-cinematic);
}}

.layer-card-3d h3 {{
  font-size: 20px;
  font-weight: 900;
  margin-bottom: 16px;
  color: var(--orange-launch);
}}

/* 6. CONTAINERIZATION (DOCKER) */
.docker-assembly-chamber {{
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 36px;
  align-items: center;
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(10, 15, 30, 0.95));
  border: 1px solid var(--border-light);
  border-radius: 28px;
  padding: 44px;
  box-shadow: var(--shadow-cinematic);
}}

.container-physical-stack {{
  display: flex;
  flex-direction: column;
  gap: 14px;
  perspective: 1000px;
}}

.stack-block-3d {{
  padding: 20px 24px;
  background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
  border: 1px solid var(--border-light);
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transform: rotateX(20deg) rotateY(-5deg);
  transition: transform 0.4s ease, border-color 0.3s ease;
  box-shadow: 0 10px 25px rgba(0,0,0,0.5);
}}

.container-physical-stack:hover .stack-block-3d:nth-child(1) {{ transform: rotateX(15deg) translateZ(30px); border-color: var(--orange-launch); }}
.container-physical-stack:hover .stack-block-3d:nth-child(2) {{ transform: rotateX(15deg) translateZ(15px); border-color: var(--cyan-beam); }}
.container-physical-stack:hover .stack-block-3d:nth-child(3) {{ transform: rotateX(15deg) translateZ(0px); border-color: var(--purple-space); }}

/* 7. SECURITY SCANNING CHAMBER (TRIVY) */
.security-laser-vault {{
  background: linear-gradient(135deg, rgba(20, 10, 30, 0.95), rgba(15, 23, 42, 0.95));
  border: 1px solid rgba(239, 68, 68, 0.35);
  border-radius: 28px;
  padding: 44px;
  position: relative;
  overflow: hidden;
  box-shadow: var(--shadow-cinematic);
}}

.laser-scan-line {{
  position: absolute;
  top: 0; bottom: 0; left: -20%;
  width: 15%;
  background: linear-gradient(90deg, transparent, rgba(239, 68, 68, 0.4), transparent);
  animation: laserSweep 5s linear infinite;
  pointer-events: none;
}}

@keyframes laserSweep {{
  0% {{ left: -20%; }}
  100% {{ left: 120%; }}
}}

.sec-checks-grid {{
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-top: 30px;
}}

.sec-check-card {{
  background: rgba(0, 0, 0, 0.4);
  border: 1px solid var(--border-light);
  border-radius: 16px;
  padding: 22px;
  text-align: center;
}}

/* 8. KUBERNETES CITY (KIND CI VALIDATION) */
.k8s-city-vault {{
  background: linear-gradient(135deg, rgba(5, 11, 20, 0.95), rgba(15, 23, 42, 0.95));
  border: 1px solid rgba(50, 108, 229, 0.35);
  border-radius: 28px;
  padding: 44px;
  box-shadow: var(--shadow-cinematic);
}}

.k8s-pods-flex {{
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 40px;
  margin-top: 36px;
  flex-wrap: wrap;
}}

.pod-active-card {{
  background: rgba(15, 23, 42, 0.9);
  border: 2px solid var(--k8s-blue);
  border-radius: 20px;
  padding: 28px 40px;
  text-align: center;
  box-shadow: 0 0 35px rgba(50, 108, 229, 0.3);
  transition: transform 0.3s ease;
}}

.pod-active-card:hover {{
  transform: scale(1.05);
}}

/* 9. CLOUD EXPANSE (AWS & RENDER) */
.cloud-expanse-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 32px;
}}

.cloud-zone-card {{
  background: linear-gradient(145deg, rgba(15, 23, 42, 0.9), rgba(10, 15, 30, 0.95));
  border: 1px solid var(--border-light);
  border-radius: 28px;
  padding: 40px;
  box-shadow: var(--shadow-cinematic);
  position: relative;
  overflow: hidden;
}}

.cloud-zone-card.aws-zone {{
  border-color: rgba(255, 153, 0, 0.35);
}}

.cloud-zone-card.render-zone {{
  border-color: rgba(139, 92, 246, 0.35);
}}

/* 10. OBSERVABILITY CONTROL ROOM */
.observability-control-room {{
  background: linear-gradient(135deg, rgba(2, 6, 23, 0.95), rgba(15, 23, 42, 0.95));
  border: 1px solid var(--border-light);
  border-radius: 28px;
  padding: 44px;
  box-shadow: var(--shadow-cinematic);
}}

.monitors-grid-3d {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-top: 30px;
}}

.monitor-hud-card {{
  background: rgba(0, 0, 0, 0.5);
  border: 1px solid var(--border-light);
  border-radius: 18px;
  padding: 22px;
}}

.monitor-val-big {{
  font-size: 32px;
  font-weight: 900;
  color: var(--cyan-beam);
  margin: 8px 0;
}}

.terminal-dev-hud {{
  background: #020617;
  border: 1px solid var(--border-light);
  border-radius: 20px;
  overflow: hidden;
  margin-top: 30px;
  box-shadow: inset 0 0 20px rgba(0,0,0,0.8);
}}

.terminal-hud-header {{
  background: #0F172A;
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid var(--border-light);
  font-family: 'JetBrains Mono', monospace;
  font-size: 11px;
  color: var(--text-dim);
}}

.terminal-hud-body {{
  padding: 28px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  line-height: 2.2;
  color: #CBD5E1;
}}

/* 11. WHY THESE TOOLS GRID — 5 COLUMNS ON DESKTOP FOR 15 CARDS (5+5+5 NO GAP) */
.tools-purpose-grid {{
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 20px;
}}

.tool-purpose-card {{
  background: rgba(15, 23, 42, 0.8);
  border: 1px solid var(--border-light);
  border-radius: 18px;
  padding: 22px;
  transition: all 0.3s ease;
}}

.tool-purpose-card:hover {{
  border-color: var(--cyan-beam);
  transform: translateY(-4px);
}}

/* 12. PROJECT RESULTS CHECKLIST GRID — 3 COLUMNS FOR 15 ITEMS (3+3+3+3+3 NO GAP) */
.results-check-grid {{
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}}

.check-item-card {{
  background: rgba(16, 185, 129, 0.08);
  border: 1px solid rgba(16, 185, 129, 0.25);
  border-radius: 14px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 14px;
  font-weight: 700;
  color: var(--sec-green);
}}

/* 13. ABOUT THE BUILDER (PERSONAL PORTFOLIO CARD) */
.about-builder-section {{
  margin-top: 140px;
  margin-bottom: 60px;
}}

.profile-card-3d {{
  background: linear-gradient(135deg, rgba(15, 23, 42, 0.95), rgba(3, 7, 18, 0.98));
  border: 2px solid var(--orange-launch);
  border-radius: 32px;
  padding: 48px;
  box-shadow: 0 30px 90px rgba(255, 107, 0, 0.3);
  display: grid;
  grid-template-columns: 1.2fr 1fr;
  gap: 40px;
  align-items: center;
}}

.profile-links-flex {{
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
  margin-top: 28px;
}}

.link-btn-social {{
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  border-radius: 12px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  font-weight: 700;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--border-light);
  color: var(--text-main);
  transition: all 0.25s ease;
}}

.link-btn-social:hover {{
  background: var(--orange-launch);
  color: #FFF;
  border-color: var(--orange-launch);
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(255, 107, 0, 0.4);
}}

/* MODAL LAUNCH DIALOG - ROBUST Z-INDEX & LAYERING */
.modal-launch-overlay {{
  display: none;
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(2, 6, 23, 0.88);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  z-index: 9999;
  align-items: center;
  justify-content: center;
  padding: 20px;
}}

.modal-launch-overlay.active {{
  display: flex !important;
}}

.modal-launch-box {{
  position: relative;
  z-index: 10000;
  max-width: 520px;
  width: 100%;
  background: linear-gradient(145deg, #0F172A, #030712);
  border: 2px solid var(--orange-launch);
  border-radius: 28px;
  padding: 36px;
  box-shadow: 0 30px 90px rgba(255, 107, 0, 0.5), 0 0 50px rgba(0,0,0,0.9);
  color: var(--text-main);
}}

/* FOOTER */
footer {{
  border-top: 1px solid var(--border-light);
  padding: 50px 36px;
  text-align: center;
  font-family: 'JetBrains Mono', monospace;
  font-size: 12px;
  color: var(--text-dim);
  background: #020617;
  line-height: 1.8;
}}

footer a {{
  color: var(--orange-launch);
  transition: color 0.2s ease;
}}

footer a:hover {{
  color: var(--cyan-beam);
  text-decoration: underline;
}}

/* RESPONSIVE LAYOUT */
@media (max-width: 1280px) {{
  .tools-purpose-grid {{ grid-template-columns: repeat(3, 1fr); }}
}}

@media (max-width: 1024px) {{
  .journey-16-grid {{ grid-template-columns: repeat(2, 1fr); }}
  .evolution-cards-grid {{ grid-template-columns: repeat(2, 1fr); }}
  .layers-pipeline-grid {{ grid-template-columns: 1fr; }}
  .docker-assembly-chamber {{ grid-template-columns: 1fr; }}
  .cloud-expanse-grid {{ grid-template-columns: 1fr; }}
  .monitors-grid-3d {{ grid-template-columns: 1fr; }}
  .results-check-grid {{ grid-template-columns: repeat(2, 1fr); }}
  .profile-card-3d {{ grid-template-columns: 1fr; }}
}}

@media (max-width: 768px) {{
  .tools-purpose-grid {{ grid-template-columns: repeat(2, 1fr); }}
}}

@media (max-width: 640px) {{
  .nav-links-space {{ display: none; }}
  .hero-headline {{ font-size: 38px; }}
  .journey-16-grid {{ grid-template-columns: 1fr; }}
  .evolution-cards-grid {{ grid-template-columns: 1fr; }}
  .results-check-grid {{ grid-template-columns: 1fr; }}
  .tools-purpose-grid {{ grid-template-columns: 1fr; }}
}}

@media (prefers-reduced-motion: reduce) {{
  * {{ animation: none !important; transition: none !important; transform: none !important; }}
}}
</style>
</head>
<body>

<!-- NAVIGATION -->
<nav class="nav-space">
  <div class="nav-inner">
    <a href="#top" class="brand-space">
      <div class="brand-space-icon">
        <i class="fa-solid fa-rocket"></i>
      </div>
      <div class="brand-space-text">
        <h1>MULTI-CLOUD</h1>
        <span>CI/CD DEPLOYMENT SYSTEM</span>
      </div>
    </a>
    
    <ul class="nav-links-space">
      <li><a href="#overview" class="nav-link-item">Overview</a></li>
      <li><a href="#evolution" class="nav-link-item">Evolution</a></li>
      <li><a href="#journey" class="nav-link-item">Journey</a></li>
      <li><a href="#pipeline" class="nav-link-item">Pipeline</a></li>
      <li><a href="#k8s" class="nav-link-item">Kubernetes</a></li>
      <li><a href="#cloud" class="nav-link-item">Cloud</a></li>
      <li><a href="#observability" class="nav-link-item">Observability</a></li>
      <li><a href="#builder" class="nav-link-item">About Me</a></li>
    </ul>
    
    <div class="live-indicator-pill">
      <span class="pulse-dot-green"></span> SYSTEM ONLINE
    </div>
  </div>
</nav>

<!-- MAIN WRAPPER -->
<main class="section-wrapper" id="top">

  <!-- 1. HERO SECTION -->
  <section class="hero-space-container">
    <div class="hero-status-pill">
      <i class="fa-solid fa-satellite"></i> AUTOMATED DEPLOYMENT FACILITY • V3 RELEASE ENGINEERING
    </div>

    <h1 class="hero-headline">
      MULTI-CLOUD<br>
      <span class="text-glow-orange">DEPLOYMENT SYSTEM</span>
    </h1>

    <p class="hero-subheadline">
      From code commit to validated release — follow software changes physically moving through GitHub Actions, Docker, Trivy Security, Kind Kubernetes, AWS EC2, and Render.
    </p>

    <div class="hero-cta-flex">
      <button class="btn-launch" onclick="executeInteractiveLaunchSequence(event)">
        <i class="fa-solid fa-rocket"></i> LAUNCH DEPLOYMENT
      </button>
      <button class="btn-explore" onclick="document.getElementById('journey').scrollIntoView({{behavior:'smooth'}})">
        <i class="fa-solid fa-compass"></i> EXPLORE JOURNEY
      </button>
    </div>

    <!-- 3D ROCKET LAUNCH CANVAS -->
    <div class="rocket-launch-facility">
      <div class="orbit-station-node st-1" id="st-code"><i class="fa-solid fa-code"></i> Code Commit</div>
      <div class="orbit-station-node st-2" id="st-github"><i class="fa-brands fa-github"></i> GitHub Actions</div>
      <div class="orbit-station-node st-3" id="st-docker"><i class="fa-brands fa-docker"></i> Docker Build</div>
      <div class="orbit-station-node st-4" id="st-trivy"><i class="fa-solid fa-shield-halved"></i> Trivy Scan</div>
      <div class="orbit-station-node st-5" id="st-k8s"><i class="fa-solid fa-dharmachakra"></i> Kind K8s</div>
      <div class="orbit-station-node st-6" id="st-cloud"><i class="fa-solid fa-cloud"></i> AWS + Render</div>

      <div class="rocket-launch-pad">
        <div class="rocket-object" id="mainRocket">
          <svg viewBox="0 0 100 200" width="100%" height="100%">
            <defs>
              <linearGradient id="rocketBodyGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#FFFFFF" />
                <stop offset="100%" stop-color="#CBD5E1" />
              </linearGradient>
              <linearGradient id="rocketNoseGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#FF6B00" />
                <stop offset="100%" stop-color="#FF9900" />
              </linearGradient>
            </defs>
            <path d="M50 10 Q65 50 65 70 L35 70 Q35 50 50 10 Z" fill="url(#rocketNoseGrad)" />
            <rect x="35" y="70" width="30" height="80" rx="4" fill="url(#rocketBodyGrad)" />
            <circle cx="50" cy="100" r="8" fill="#099CEC" stroke="#1E293B" stroke-width="2" />
            <path d="M35 120 L15 160 L35 150 Z" fill="#FF6B00" />
            <path d="M65 120 L85 160 L65 150 Z" fill="#FF6B00" />
            <rect x="42" y="150" width="16" height="10" fill="#475569" />
          </svg>
          <div class="rocket-flame"></div>
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--orange-launch); font-weight: 800; margin-top: 14px;">
          DEPLOYMENT ROCKET V3
        </div>
      </div>
    </div>
  </section>

  <!-- 2. PROJECT OVERVIEW & INTRODUCTION -->
  <section class="story-section" id="overview">
    <div class="story-header">
      <div class="story-num">PROJECT OVERVIEW</div>
      <h2 class="story-title">What Is This System?</h2>
      <p class="story-desc">A production-style DevOps architecture demonstrating automated software release delivery.</p>
    </div>

    <div class="project-intro-card">
      <div>
        <h3 style="font-size: 26px; font-weight: 900; margin-bottom: 14px;">Automated Release Engineering</h3>
        <p style="font-size: 15px; color: var(--text-dim); line-height: 1.7; margin-bottom: 20px;">
          This project demonstrates a production-style CI/CD pipeline built with <strong>Python Flask</strong>, <strong>Docker</strong>, <strong>Kubernetes (Kind)</strong>, <strong>GitHub Actions</strong>, <strong>Trivy Security</strong>, <strong>Terraform IaC</strong>, <strong>AWS EC2</strong>, and <strong>Render</strong>. Every code modification passes thorough automated quality gates before release image publication.
        </p>
        <div style="display: flex; gap: 12px; flex-wrap: wrap;">
          <a class="btn-launch" href="https://github.com/JOSESAMUEL14/multicloud-cicd" target="_blank" rel="noopener noreferrer">
            <i class="fa-brands fa-github"></i> VIEW SOURCE CODE
          </a>
          <a class="btn-explore" href="https://multicloud-cicd.onrender.com/" target="_blank" rel="noopener noreferrer">
            <i class="fa-solid fa-globe"></i> OPEN LIVE DEMO
          </a>
        </div>
      </div>

      <div style="background: rgba(0,0,0,0.4); border-radius: 20px; padding: 24px; border: 1px solid var(--border-light);">
        <h4 style="font-size: 14px; font-family: 'JetBrains Mono', monospace; color: var(--orange-launch); margin-bottom: 12px;">PROJECT CORE HIGHLIGHTS</h4>
        <ul style="font-size: 13px; color: var(--text-dim); line-height: 2; list-style: none;">
          <li>✓ Automated Pytest Suite Execution</li>
          <li>✓ Container Build & Smoke Validation</li>
          <li>✓ Trivy Security Vulnerability Scan</li>
          <li>✓ Kind Kubernetes CI Cluster Verification</li>
          <li>✓ 2 Pod Replicas Availability Check</li>
          <li>✓ Traceable Release Images on Docker Hub</li>
        </ul>
      </div>
    </div>
  </section>

  <!-- 3. NEW SECTION: FROM FOUNDATION TO RELEASE ENGINEERING -->
  <section class="story-section" id="evolution">
    <div class="story-header">
      <div class="story-num">PROJECT EVOLUTION</div>
      <h2 class="story-title">From Foundation to Release Engineering</h2>
      <p class="story-desc">
        This system evolved from an initial Flask-based CI/CD implementation into a broader release-engineering project. The current version preserves the core application and deployment capabilities while adding stronger automated validation, containerization, security scanning, Kubernetes validation, infrastructure-as-code, cloud environments, and observability.
      </p>
    </div>

    <!-- VISUAL PROGRESSION DIAGRAM -->
    <div class="arch-flow-box">
      <div style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--orange-launch); font-weight: 800; letter-spacing: 2px; text-transform: uppercase; text-align: center;">
        ENGINEERING PROGRESSION
      </div>
      <div class="arch-flow-grid">
        <div class="arch-node">PROJECT FOUNDATION</div>
        <div class="arch-arrow">→</div>
        <div class="arch-node">Python Flask Application</div>
        <div class="arch-arrow">→</div>
        <div class="arch-node">CI/CD Automation</div>
        <div class="arch-arrow">→</div>
        <div class="arch-node">Containerization</div>
        <div class="arch-arrow">→</div>
        <div class="arch-node arch-k8s">Kubernetes Validation</div>
        <div class="arch-arrow">→</div>
        <div class="arch-node">Security Scanning</div>
        <div class="arch-arrow">→</div>
        <div class="arch-node arch-aws">Infrastructure as Code</div>
        <div class="arch-arrow">→</div>
        <div class="arch-node arch-render">Cloud Environments</div>
        <div class="arch-arrow">→</div>
        <div class="arch-node">Observability</div>
        <div class="arch-arrow">→</div>
        <div class="arch-node" style="border-color: var(--orange-launch); color: var(--orange-launch);">RELEASE ENGINEERING</div>
      </div>
    </div>

    <!-- WHAT THE EVOLUTION ADDS (8 CARDS) -->
    <div class="evolution-cards-grid">
      <div class="evolution-card">
        <div class="evolution-icon"><i class="fa-solid fa-code"></i></div>
        <h4 style="font-size: 15px; font-weight: 800; margin-bottom: 6px; color: var(--text-main);">FOUNDATION</h4>
        <p style="font-size: 12px; color: var(--text-dim); line-height: 1.6;">Python Flask application and existing service functionality.</p>
      </div>

      <div class="evolution-card">
        <div class="evolution-icon"><i class="fa-brands fa-github"></i></div>
        <h4 style="font-size: 15px; font-weight: 800; margin-bottom: 6px; color: var(--cyan-beam);">AUTOMATION</h4>
        <p style="font-size: 12px; color: var(--text-dim); line-height: 1.6;">GitHub Actions CI workflow and automated testing.</p>
      </div>

      <div class="evolution-card">
        <div class="evolution-icon"><i class="fa-brands fa-docker"></i></div>
        <h4 style="font-size: 15px; font-weight: 800; margin-bottom: 6px; color: var(--docker-blue);">CONTAINERIZATION</h4>
        <p style="font-size: 12px; color: var(--text-dim); line-height: 1.6;">Docker image build and container smoke validation.</p>
      </div>

      <div class="evolution-card">
        <div class="evolution-icon"><i class="fa-solid fa-shield-halved"></i></div>
        <h4 style="font-size: 15px; font-weight: 800; margin-bottom: 6px; color: var(--sec-red);">SECURITY</h4>
        <p style="font-size: 12px; color: var(--text-dim); line-height: 1.6;">Trivy vulnerability scanning during CI.</p>
      </div>

      <div class="evolution-card">
        <div class="evolution-icon"><i class="fa-solid fa-dharmachakra"></i></div>
        <h4 style="font-size: 15px; font-weight: 800; margin-bottom: 6px; color: var(--k8s-blue);">KUBERNETES</h4>
        <p style="font-size: 12px; color: var(--text-dim); line-height: 1.6;">Kind-based CI validation, rollout checks, and replica verification.</p>
      </div>

      <div class="evolution-card">
        <div class="evolution-icon"><i class="fa-solid fa-cubes-stacked"></i></div>
        <h4 style="font-size: 15px; font-weight: 800; margin-bottom: 6px; color: #844FBA;">INFRASTRUCTURE</h4>
        <p style="font-size: 12px; color: var(--text-dim); line-height: 1.6;">Terraform-managed cloud infrastructure.</p>
      </div>

      <div class="evolution-card">
        <div class="evolution-icon"><i class="fa-solid fa-cloud"></i></div>
        <h4 style="font-size: 15px; font-weight: 800; margin-bottom: 6px; color: var(--aws-orange);">CLOUD</h4>
        <p style="font-size: 12px; color: var(--text-dim); line-height: 1.6;">AWS EC2 as a cloud deployment target and Render as the public live demo environment.</p>
      </div>

      <div class="evolution-card">
        <div class="evolution-icon"><i class="fa-solid fa-chart-line"></i></div>
        <h4 style="font-size: 15px; font-weight: 800; margin-bottom: 6px; color: var(--purple-space);">OBSERVABILITY</h4>
        <p style="font-size: 12px; color: var(--text-dim); line-height: 1.6;">Prometheus / Grafana monitoring and metrics.</p>
      </div>
    </div>
  </section>

  <!-- 4. 16-STAGE HOW THE DEPLOYMENT WORKS (INTERACTIVE HOVER/TAP POPOVER CARDS) -->
  <section class="story-section" id="journey">
    <div class="story-header">
      <div class="story-num">THE 16-STAGE JOURNEY</div>
      <h2 class="story-title">How The Deployment Works</h2>
      <p class="story-desc">From code commit to validated release — hover or tap any stage to inspect its physical workflow, rationale, and output.</p>
    </div>

    <div class="journey-16-grid">
      <!-- 01 -->
      <div class="journey-step-card" data-stage="01" tabindex="0"
           onmouseenter="showStagePopover(this, '01')" onmouseleave="hideStagePopover()"
           onfocus="showStagePopover(this, '01')" onblur="hideStagePopover()"
           onclick="toggleStagePopover(this, '01', event)">
        <span class="step-num-badge">01 — COMMIT</span>
        <h4 style="font-size: 15px; font-weight: 800; margin-top: 10px;">Code Commit</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 4px;">Developer changes application code.</p>
        <div class="step-hover-hint"><i class="fa-solid fa-circle-info"></i> Hover/Tap for Details</div>
      </div>

      <!-- 02 -->
      <div class="journey-step-card" data-stage="02" tabindex="0"
           onmouseenter="showStagePopover(this, '02')" onmouseleave="hideStagePopover()"
           onfocus="showStagePopover(this, '02')" onblur="hideStagePopover()"
           onclick="toggleStagePopover(this, '02', event)">
        <span class="step-num-badge">02 — GITHUB</span>
        <h4 style="font-size: 15px; font-weight: 800; margin-top: 10px;">GitHub Repository</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 4px;">Code is pushed to the repository.</p>
        <div class="step-hover-hint"><i class="fa-solid fa-circle-info"></i> Hover/Tap for Details</div>
      </div>

      <!-- 03 -->
      <div class="journey-step-card" data-stage="03" tabindex="0"
           onmouseenter="showStagePopover(this, '03')" onmouseleave="hideStagePopover()"
           onfocus="showStagePopover(this, '03')" onblur="hideStagePopover()"
           onclick="toggleStagePopover(this, '03', event)">
        <span class="step-num-badge">03 — GITHUB ACTIONS</span>
        <h4 style="font-size: 15px; font-weight: 800; margin-top: 10px;">GitHub Actions</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 4px;">CI workflow starts.</p>
        <div class="step-hover-hint"><i class="fa-solid fa-circle-info"></i> Hover/Tap for Details</div>
      </div>

      <!-- 04 -->
      <div class="journey-step-card" data-stage="04" tabindex="0"
           onmouseenter="showStagePopover(this, '04')" onmouseleave="hideStagePopover()"
           onfocus="showStagePopover(this, '04')" onblur="hideStagePopover()"
           onclick="toggleStagePopover(this, '04', event)">
        <span class="step-num-badge">04 — PYTEST</span>
        <h4 style="font-size: 15px; font-weight: 800; margin-top: 10px;">Pytest Execution</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 4px;">Automated tests run.</p>
        <div class="step-hover-hint"><i class="fa-solid fa-circle-info"></i> Hover/Tap for Details</div>
      </div>

      <!-- 05 -->
      <div class="journey-step-card" data-stage="05" tabindex="0"
           onmouseenter="showStagePopover(this, '05')" onmouseleave="hideStagePopover()"
           onfocus="showStagePopover(this, '05')" onblur="hideStagePopover()"
           onclick="toggleStagePopover(this, '05', event)">
        <span class="step-num-badge">05 — DOCKER BUILD</span>
        <h4 style="font-size: 15px; font-weight: 800; margin-top: 10px;">Docker Build</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 4px;">Application container image is built.</p>
        <div class="step-hover-hint"><i class="fa-solid fa-circle-info"></i> Hover/Tap for Details</div>
      </div>

      <!-- 06 -->
      <div class="journey-step-card" data-stage="06" tabindex="0"
           onmouseenter="showStagePopover(this, '06')" onmouseleave="hideStagePopover()"
           onfocus="showStagePopover(this, '06')" onblur="hideStagePopover()"
           onclick="toggleStagePopover(this, '06', event)">
        <span class="step-num-badge">06 — DOCKER SMOKE TEST</span>
        <h4 style="font-size: 15px; font-weight: 800; margin-top: 10px;">Docker Smoke Test</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 4px;">Container health endpoint is checked.</p>
        <div class="step-hover-hint"><i class="fa-solid fa-circle-info"></i> Hover/Tap for Details</div>
      </div>

      <!-- 07 -->
      <div class="journey-step-card" data-stage="07" tabindex="0"
           onmouseenter="showStagePopover(this, '07')" onmouseleave="hideStagePopover()"
           onfocus="showStagePopover(this, '07')" onblur="hideStagePopover()"
           onclick="toggleStagePopover(this, '07', event)">
        <span class="step-num-badge">07 — TRIVY SCAN</span>
        <h4 style="font-size: 15px; font-weight: 800; margin-top: 10px;">Trivy Security Scan</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 4px;">Container is scanned for vulnerabilities.</p>
        <div class="step-hover-hint"><i class="fa-solid fa-circle-info"></i> Hover/Tap for Details</div>
      </div>

      <!-- 08 -->
      <div class="journey-step-card" data-stage="08" tabindex="0"
           onmouseenter="showStagePopover(this, '08')" onmouseleave="hideStagePopover()"
           onfocus="showStagePopover(this, '08')" onblur="hideStagePopover()"
           onclick="toggleStagePopover(this, '08', event)">
        <span class="step-num-badge">08 — KIND K8S CHECK</span>
        <h4 style="font-size: 15px; font-weight: 800; margin-top: 10px;">Kind K8s CI Check</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 4px;">Image is validated in a Kind Kubernetes cluster.</p>
        <div class="step-hover-hint"><i class="fa-solid fa-circle-info"></i> Hover/Tap for Details</div>
      </div>

      <!-- 09 -->
      <div class="journey-step-card" data-stage="09" tabindex="0"
           onmouseenter="showStagePopover(this, '09')" onmouseleave="hideStagePopover()"
           onfocus="showStagePopover(this, '09')" onblur="hideStagePopover()"
           onclick="toggleStagePopover(this, '09', event)">
        <span class="step-num-badge">09 — ROLLOUT</span>
        <h4 style="font-size: 15px; font-weight: 800; margin-top: 10px;">Rollout Check</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 4px;">Kubernetes deployment rollout is checked.</p>
        <div class="step-hover-hint"><i class="fa-solid fa-circle-info"></i> Hover/Tap for Details</div>
      </div>

      <!-- 10 -->
      <div class="journey-step-card" data-stage="10" tabindex="0"
           onmouseenter="showStagePopover(this, '10')" onmouseleave="hideStagePopover()"
           onfocus="showStagePopover(this, '10')" onblur="hideStagePopover()"
           onclick="toggleStagePopover(this, '10', event)">
        <span class="step-num-badge">10 — 2 REPLICAS READY</span>
        <h4 style="font-size: 15px; font-weight: 800; margin-top: 10px;">2 Replicas Ready</h4>
        <p style="font-size: 12px; color: var(--sec-green); margin-top: 4px; font-weight: 700;">Expected replicas are verified.</p>
        <div class="step-hover-hint"><i class="fa-solid fa-circle-info"></i> Hover/Tap for Details</div>
      </div>

      <!-- 11 -->
      <div class="journey-step-card" data-stage="11" tabindex="0"
           onmouseenter="showStagePopover(this, '11')" onmouseleave="hideStagePopover()"
           onfocus="showStagePopover(this, '11')" onblur="hideStagePopover()"
           onclick="toggleStagePopover(this, '11', event)">
        <span class="step-num-badge">11 — HEALTH CHECK</span>
        <h4 style="font-size: 15px; font-weight: 800; margin-top: 10px;">Health Check</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 4px;">Service health endpoint is verified.</p>
        <div class="step-hover-hint"><i class="fa-solid fa-circle-info"></i> Hover/Tap for Details</div>
      </div>

      <!-- 12 -->
      <div class="journey-step-card" data-stage="12" tabindex="0"
           onmouseenter="showStagePopover(this, '12')" onmouseleave="hideStagePopover()"
           onfocus="showStagePopover(this, '12')" onblur="hideStagePopover()"
           onclick="toggleStagePopover(this, '12', event)">
        <span class="step-num-badge">12 — RELEASE IMAGE / SHA</span>
        <h4 style="font-size: 15px; font-weight: 800; margin-top: 10px;">Release Image / SHA</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 4px;">Validated image is tagged/published according to CI.</p>
        <div class="step-hover-hint"><i class="fa-solid fa-circle-info"></i> Hover/Tap for Details</div>
      </div>

      <!-- SECTION LABEL FOR STAGES 13-16 -->
      <div style="grid-column: 1 / -1; margin-top: 14px; margin-bottom: 2px;">
        <span style="font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 800; color: var(--purple-space); text-transform: uppercase; letter-spacing: 2px; background: rgba(139, 92, 246, 0.12); border: 1px solid rgba(139, 92, 246, 0.3); padding: 6px 14px; border-radius: 8px; display: inline-block;">
          Post-validation environments & observability
        </span>
      </div>

      <!-- 13 -->
      <div class="journey-step-card" data-stage="13" tabindex="0"
           onmouseenter="showStagePopover(this, '13')" onmouseleave="hideStagePopover()"
           onfocus="showStagePopover(this, '13')" onblur="hideStagePopover()"
           onclick="toggleStagePopover(this, '13', event)">
        <span class="step-num-badge">13 — AWS EC2</span>
        <h4 style="font-size: 15px; font-weight: 800; margin-top: 10px;">AWS EC2</h4>
        <p style="font-size: 12px; color: var(--aws-orange); margin-top: 4px;">Terraform-managed cloud deployment target.</p>
        <div class="step-hover-hint"><i class="fa-solid fa-circle-info"></i> Hover/Tap for Details</div>
      </div>

      <!-- 14 -->
      <div class="journey-step-card" data-stage="14" tabindex="0"
           onmouseenter="showStagePopover(this, '14')" onmouseleave="hideStagePopover()"
           onfocus="showStagePopover(this, '14')" onblur="hideStagePopover()"
           onclick="toggleStagePopover(this, '14', event)">
        <span class="step-num-badge">14 — RENDER</span>
        <h4 style="font-size: 15px; font-weight: 800; margin-top: 10px;">Render</h4>
        <p style="font-size: 12px; color: var(--purple-space); margin-top: 4px;">Public live demonstration environment.</p>
        <div class="step-hover-hint"><i class="fa-solid fa-circle-info"></i> Hover/Tap for Details</div>
      </div>

      <!-- 15 -->
      <div class="journey-step-card" data-stage="15" tabindex="0"
           onmouseenter="showStagePopover(this, '15')" onmouseleave="hideStagePopover()"
           onfocus="showStagePopover(this, '15')" onblur="hideStagePopover()"
           onclick="toggleStagePopover(this, '15', event)">
        <span class="step-num-badge">15 — OBSERVABILITY</span>
        <h4 style="font-size: 15px; font-weight: 800; margin-top: 10px;">Observability</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 4px;">Prometheus / Grafana provide monitoring and metrics.</p>
        <div class="step-hover-hint"><i class="fa-solid fa-circle-info"></i> Hover/Tap for Details</div>
      </div>

      <!-- 16 -->
      <div class="journey-step-card" data-stage="16" tabindex="0"
           onmouseenter="showStagePopover(this, '16')" onmouseleave="hideStagePopover()"
           onfocus="showStagePopover(this, '16')" onblur="hideStagePopover()"
           onclick="toggleStagePopover(this, '16', event)">
        <span class="step-num-badge">16 — LIVE SYSTEM</span>
        <h4 style="font-size: 15px; font-weight: 800; margin-top: 10px;">Live System</h4>
        <p style="font-size: 12px; color: var(--sec-green); margin-top: 4px; font-weight: 700;">Validated system available through project environment.</p>
        <div class="step-hover-hint"><i class="fa-solid fa-circle-info"></i> Hover/Tap for Details</div>
      </div>
    </div>

    <!-- 5. START -> FINISH SUMMARY BANNER -->
    <div class="start-finish-banner">
      <h3 style="font-size: 26px; font-weight: 900; margin-bottom: 8px; color: var(--text-main);">FROM CODE TO VALIDATED RELEASE</h3>
      <p style="font-size: 14px; color: var(--text-dim);">Every CI validation stage is automated and traceable across GitHub Actions runners, Kind CI clusters, and release registries.</p>
    </div>
  </section>

  <!-- 6. INSIDE THE PIPELINE — 3 LAYERS -->
  <section class="story-section" id="pipeline">
    <div class="story-header">
      <div class="story-num">PIPELINE ARCHITECTURE</div>
      <h2 class="story-title">Inside The Pipeline</h2>
      <p class="story-desc">The three distinct layers of automation handling software delivery.</p>
    </div>

    <div class="layers-pipeline-grid">
      <!-- Layer 1 -->
      <div class="layer-card-3d">
        <h3>LAYER 1 — BUILD</h3>
        <ul style="font-size: 13px; color: var(--text-dim); line-height: 2.2; list-style: none;">
          <li>• Python Flask Application</li>
          <li>• Pytest Unit Testing</li>
          <li>• Docker Image Containerization</li>
        </ul>
      </div>

      <!-- Layer 2 -->
      <div class="layer-card-3d">
        <h3 style="color: var(--cyan-beam);">LAYER 2 — VALIDATE</h3>
        <ul style="font-size: 13px; color: var(--text-dim); line-height: 2.2; list-style: none;">
          <li>• Docker Smoke Test</li>
          <li>• Trivy Security Scan</li>
          <li>• Kind Kubernetes CI Cluster</li>
          <li>• Rollout Check</li>
          <li>• 2 Replicas Ready</li>
          <li>• Health Endpoint Check</li>
        </ul>
      </div>

      <!-- Layer 3 -->
      <div class="layer-card-3d">
        <h3 style="color: var(--purple-space);">LAYER 3 — RELEASE</h3>
        <ul style="font-size: 13px; color: var(--text-dim); line-height: 2.2; list-style: none;">
          <li>• Docker Image / SHA Tagging</li>
          <li>• AWS EC2 / Render Environments</li>
          <li>• Prometheus Telemetry</li>
        </ul>
      </div>
    </div>
  </section>

  <!-- 7. CONTAINERIZATION (DOCKER) -->
  <section class="story-section">
    <div class="docker-assembly-chamber">
      <div class="container-physical-stack">
        <div class="stack-block-3d">
          <div style="display: flex; align-items: center; gap: 12px;">
            <i class="fa-solid fa-layer-group" style="color: var(--orange-launch); font-size: 22px;"></i>
            <div>
              <strong style="font-size: 14px;">Application Code Layer</strong>
              <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--text-dim);">app/app.py & HTML assets</div>
            </div>
          </div>
          <span class="station-badge">Top Layer</span>
        </div>

        <div class="stack-block-3d">
          <div style="display: flex; align-items: center; gap: 12px;">
            <i class="fa-brands fa-python" style="color: var(--cyan-beam); font-size: 22px;"></i>
            <div>
              <strong style="font-size: 14px;">Python & Dependencies</strong>
              <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--text-dim);">Flask & Prometheus Exporter</div>
            </div>
          </div>
          <span class="station-badge">Mid Layer</span>
        </div>

        <div class="stack-block-3d">
          <div style="display: flex; align-items: center; gap: 12px;">
            <i class="fa-brands fa-linux" style="color: var(--docker-blue); font-size: 22px;"></i>
            <div>
              <strong style="font-size: 14px;">Base Linux OS Image</strong>
              <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--text-dim);">python:3.11-slim runtime</div>
            </div>
          </div>
          <span class="station-badge">Base Layer</span>
        </div>
      </div>

      <div>
        <i class="fa-brands fa-docker" style="font-size: 54px; color: var(--docker-blue); margin-bottom: 16px;"></i>
        <h3 style="font-size: 24px; font-weight: 900; margin-bottom: 12px;">Docker Container Packaging</h3>
        <p style="color: var(--text-dim); font-size: 14px; line-height: 1.7;">
          Source code is packaged into a minimal container image, smoke-tested, and published to Docker Hub registry with SHA tagging.
        </p>
      </div>
    </div>
  </section>

  <!-- 8. SECURITY SCANNING (TRIVY) -->
  <section class="story-section">
    <div class="security-laser-vault">
      <div class="laser-scan-line"></div>

      <div style="display: flex; align-items: center; justify-content: space-between;">
        <div>
          <h3 style="font-size: 24px; font-weight: 900; color: var(--sec-red);">TRIVY SECURITY SCANNER</h3>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--text-dim); margin-top: 4px;">AUTOMATED CONTAINER VULNERABILITY CHECK</div>
        </div>
        <span class="station-badge" style="font-size: 12px; padding: 6px 14px;">✓ TRIVY SECURITY GATE</span>
      </div>

      <div class="sec-checks-grid">
        <div class="sec-check-card">
          <i class="fa-solid fa-shield-cat" style="font-size: 26px; color: var(--sec-red); margin-bottom: 10px;"></i>
          <h4 style="font-size: 14px; font-weight: 800;">Trivy Scan</h4>
          <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;">HIGH/CRITICAL Check</div>
        </div>

        <div class="sec-check-card">
          <i class="fa-solid fa-robot" style="font-size: 26px; color: var(--cyan-beam); margin-bottom: 10px;"></i>
          <h4 style="font-size: 14px; font-weight: 800;">GitHub Actions</h4>
          <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;">Automated CI</div>
        </div>

        <div class="sec-check-card">
          <i class="fa-solid fa-vial-circle-check" style="font-size: 26px; color: var(--sec-green); margin-bottom: 10px;"></i>
          <h4 style="font-size: 14px; font-weight: 800;">Pytest</h4>
          <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;">Unit Testing</div>
        </div>

        <div class="sec-check-card">
          <i class="fa-solid fa-user-shield" style="font-size: 26px; color: var(--orange-launch); margin-bottom: 10px;"></i>
          <h4 style="font-size: 14px; font-weight: 800;">Non-Root User</h4>
          <div style="font-size: 11px; color: var(--text-dim); margin-top: 4px;">Hardened Container</div>
        </div>
      </div>
    </div>
  </section>

  <!-- 9. KUBERNETES CITY (KIND CI VALIDATION) -->
  <section class="story-section" id="k8s">
    <div class="k8s-city-vault">
      <div style="display: flex; align-items: center; justify-content: space-between;">
        <div>
          <span class="station-badge" style="color: var(--k8s-blue); background: rgba(50, 108, 229, 0.15); border-color: rgba(50, 108, 229, 0.4);">
            CI VALIDATION CLUSTER
          </span>
          <h3 style="font-size: 26px; font-weight: 900; margin-top: 10px;">2 Pod Replicas Verified</h3>
        </div>
        <i class="fa-solid fa-dharmachakra" style="font-size: 42px; color: var(--k8s-blue);"></i>
      </div>

      <div class="k8s-pods-flex">
        <div class="pod-active-card">
          <i class="fa-solid fa-cubes" style="font-size: 32px; color: var(--k8s-blue); margin-bottom: 8px;"></i>
          <h4 style="font-size: 16px; font-weight: 800;">POD 01</h4>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--sec-green); margin-top: 6px;">● RUNNING (1/1)</div>
        </div>

        <div style="font-family: 'JetBrains Mono', monospace; font-size: 18px; color: var(--cyan-beam); font-weight: 800;">
          ⚡ ROLLOUT VERIFIED ⚡
        </div>

        <div class="pod-active-card">
          <i class="fa-solid fa-cubes" style="font-size: 32px; color: var(--k8s-blue); margin-bottom: 8px;"></i>
          <h4 style="font-size: 16px; font-weight: 800;">POD 02</h4>
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--sec-green); margin-top: 6px;">● RUNNING (1/1)</div>
        </div>
      </div>
    </div>
  </section>

  <!-- 10. CLOUD INFRASTRUCTURE (AWS & RENDER) -->
  <section class="story-section" id="cloud">
    <div class="story-header">
      <div class="story-num">INFRASTRUCTURE TARGETS</div>
      <h2 class="story-title">Cloud Environments</h2>
      <p class="story-desc">Distinguishing between Terraform-managed cloud targets and public live demo environments.</p>
    </div>

    <div class="cloud-expanse-grid">
      <!-- AWS Card -->
      <div class="cloud-zone-card aws-zone">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
          <i class="fa-brands fa-aws" style="font-size: 36px; color: var(--aws-orange);"></i>
          <span class="station-badge" style="color: var(--aws-orange); background: rgba(255, 153, 0, 0.12); border-color: rgba(255, 153, 0, 0.3);">Terraform-managed target</span>
        </div>
        <h3 style="font-size: 22px; font-weight: 900;">AWS EC2 Target</h3>
        <p style="font-size: 13px; color: var(--text-dim); margin-top: 8px; line-height: 1.6;">
          AWS EC2 cloud compute deployment target with Terraform IaC configuration stored under version control in <code>/terraform</code>.
        </p>
        <div style="margin-top: 20px; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--text-dim);">
          Region: ap-south-1 (Mumbai) • Terraform Managed
        </div>
      </div>

      <!-- Render Card -->
      <div class="cloud-zone-card render-zone">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
          <i class="fa-solid fa-globe" style="font-size: 32px; color: var(--purple-space);"></i>
          <span class="station-badge">Public live demo</span>
        </div>
        <h3 style="font-size: 22px; font-weight: 900;">Render Cloud</h3>
        <p style="font-size: 13px; color: var(--text-dim); margin-top: 8px; line-height: 1.6;">
          Hosts the active public demonstration web app, serving continuous delivery updates directly from the main branch.
        </p>
        <div style="margin-top: 20px; font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--cyan-beam);">
          URL: multicloud-cicd.onrender.com
        </div>
      </div>
    </div>
  </section>

  <!-- 11. OBSERVABILITY CONTROL ROOM -->
  <section class="story-section" id="observability">
    <div class="story-header">
      <div class="story-num">OBSERVABILITY CONTROL ROOM</div>
      <h2 class="story-title">Metrics & Telemetry</h2>
      <p class="story-desc">Real-time application telemetry reading from Flask <code>/stats</code> and Prometheus endpoints.</p>
    </div>

    <div class="observability-control-room">
      <div class="monitors-grid-3d">
        <div class="monitor-hud-card">
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--text-dim);">SYSTEM STATUS</div>
          <div class="monitor-val-big" id="mon-status" style="color: var(--sec-green);">HEALTHY</div>
          <div style="font-size: 11px; color: var(--text-dim);">/health endpoint response</div>
        </div>

        <div class="monitor-hud-card">
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--text-dim);">PROCESS UPTIME</div>
          <div class="monitor-val-big" id="mon-uptime">--:--:--</div>
          <div style="font-size: 11px; color: var(--text-dim);">Flask runtime duration</div>
        </div>

        <div class="monitor-hud-card">
          <div style="font-family: 'JetBrains Mono', monospace; font-size: 10px; color: var(--text-dim);">REQUESTS SERVED</div>
          <div class="monitor-val-big" id="mon-requests" style="color: var(--orange-launch);">0</div>
          <div style="font-size: 11px; color: var(--text-dim);">HTTP requests count</div>
        </div>
      </div>

      <div class="terminal-dev-hud">
        <div class="terminal-hud-header">
          <div><i class="fa-solid fa-terminal"></i> devops-terminal · release-log</div>
          <div>RELEASE VERIFIED</div>
        </div>
        <div class="terminal-hud-body">
          <div><span style="color: var(--orange-launch); font-weight: 700;">$</span> pipeline launch sequence initialized</div>
          <div><span style="color: var(--cyan-beam);">→</span> git push origin main verified</div>
          <div><span style="color: var(--sec-green);">✓</span> pytest suite passed (automated unit tests verified)</div>
          <div><span style="color: var(--sec-green);">✓</span> docker build completed with SHA tag</div>
          <div><span style="color: var(--sec-green);">✓</span> trivy scan passed (vulnerability gate verified)</div>
          <div><span style="color: var(--sec-green);">✓</span> kind CI cluster deployment & 2 replicas verified</div>
          <div><span style="color: var(--sec-green);">✓</span> release image published to docker hub</div>
          <div><span style="color: var(--orange-launch); font-weight: 700;">STATUS</span> <span style="background: rgba(16, 185, 129, 0.2); color: var(--sec-green); padding: 2px 8px; border-radius: 4px;">CI/CD RELEASE VERIFIED</span></div>
        </div>
      </div>
    </div>
  </section>

  <!-- 12. WHY THESE TOOLS? (TECHNOLOGY ECOSYSTEM — EXACTLY 15 CARDS, 5+5+5 NO GAP) -->
  <section class="story-section" id="stack">
    <div class="story-header">
      <div class="story-num">TECHNOLOGY ECOSYSTEM</div>
      <h2 class="story-title">Why These Tools?</h2>
      <p class="story-desc">The specific role of each technology integrated across the architecture.</p>
    </div>

    <div class="tools-purpose-grid">
      <div class="tool-purpose-card">
        <h4 style="font-size: 15px; font-weight: 800; color: #3776AB;"><i class="fa-brands fa-python"></i> Python + Flask</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">Application web backend engine.</p>
      </div>

      <div class="tool-purpose-card">
        <h4 style="font-size: 15px; font-weight: 800; color: var(--purple-space);"><i class="fa-solid fa-vial"></i> Pytest</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">Automated application testing.</p>
      </div>

      <div class="tool-purpose-card">
        <h4 style="font-size: 15px; font-weight: 800; color: var(--docker-blue);"><i class="fa-brands fa-docker"></i> Docker</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">Application containerization.</p>
      </div>

      <div class="tool-purpose-card">
        <h4 style="font-size: 15px; font-weight: 800; color: var(--cyan-beam);"><i class="fa-brands fa-github"></i> GitHub Actions</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">CI/CD automation runner.</p>
      </div>

      <div class="tool-purpose-card">
        <h4 style="font-size: 15px; font-weight: 800; color: var(--sec-red);"><i class="fa-solid fa-shield-halved"></i> Trivy</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">Container security scanning.</p>
      </div>

      <div class="tool-purpose-card">
        <h4 style="font-size: 15px; font-weight: 800; color: var(--k8s-blue);"><i class="fa-solid fa-dharmachakra"></i> Kubernetes</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">Container orchestration validation.</p>
      </div>

      <div class="tool-purpose-card">
        <h4 style="font-size: 15px; font-weight: 800; color: var(--orange-launch);"><i class="fa-solid fa-cube"></i> Kind</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">CI validation cluster.</p>
      </div>

      <div class="tool-purpose-card">
        <h4 style="font-size: 15px; font-weight: 800; color: #844FBA;"><i class="fa-solid fa-cubes-stacked"></i> Terraform</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">Infrastructure as Code.</p>
      </div>

      <div class="tool-purpose-card">
        <h4 style="font-size: 15px; font-weight: 800; color: var(--aws-orange);"><i class="fa-brands fa-aws"></i> AWS EC2</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">Terraform-managed cloud target.</p>
      </div>

      <div class="tool-purpose-card">
        <h4 style="font-size: 15px; font-weight: 800; color: #099CEC;"><i class="fa-solid fa-box"></i> Docker Hub</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">Container image registry.</p>
      </div>

      <div class="tool-purpose-card">
        <h4 style="font-size: 15px; font-weight: 800; color: #E6522C;"><i class="fa-solid fa-chart-line"></i> Prometheus</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">Metrics collection engine.</p>
      </div>

      <div class="tool-purpose-card">
        <h4 style="font-size: 15px; font-weight: 800; color: #F46800;"><i class="fa-solid fa-chart-area"></i> Grafana</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">Metrics visualization UI.</p>
      </div>

      <div class="tool-purpose-card">
        <h4 style="font-size: 15px; font-weight: 800; color: var(--sec-green);"><i class="fa-solid fa-microchip"></i> Node Exporter</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">Host-level metrics collector.</p>
      </div>

      <div class="tool-purpose-card">
        <h4 style="font-size: 15px; font-weight: 800; color: var(--purple-space);"><i class="fa-solid fa-globe"></i> Render</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">Public live demo.</p>
      </div>

      <!-- 15TH CARD: LINUX -->
      <div class="tool-purpose-card">
        <h4 style="font-size: 15px; font-weight: 800; color: #FCC624;"><i class="fa-brands fa-linux"></i> Linux</h4>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 6px;">Operating system and command-line environment used for DevOps workflows and deployment operations.</p>
      </div>
    </div>
  </section>

  <!-- 13. PROJECT RESULTS / CAPABILITIES (EXACTLY 15 ITEMS, 3+3+3+3+3 NO GAP) -->
  <section class="story-section">
    <div class="story-header">
      <div class="story-num">PROJECT CAPABILITIES</div>
      <h2 class="story-title">What This Project Demonstrates</h2>
      <p class="story-desc">Key engineering practices validated in this implementation.</p>
    </div>

    <div class="results-check-grid">
      <div class="check-item-card"><i class="fa-solid fa-circle-check"></i> CI/CD automation</div>
      <div class="check-item-card"><i class="fa-solid fa-circle-check"></i> Automated testing</div>
      <div class="check-item-card"><i class="fa-solid fa-circle-check"></i> Docker containerization</div>
      <div class="check-item-card"><i class="fa-solid fa-circle-check"></i> Container smoke testing</div>
      <div class="check-item-card"><i class="fa-solid fa-circle-check"></i> Security scanning</div>
      <div class="check-item-card"><i class="fa-solid fa-circle-check"></i> Kubernetes validation</div>
      <div class="check-item-card"><i class="fa-solid fa-circle-check"></i> Rolling deployment verification</div>
      <div class="check-item-card"><i class="fa-solid fa-circle-check"></i> Replica verification</div>
      <div class="check-item-card"><i class="fa-solid fa-circle-check"></i> Health checks</div>
      <div class="check-item-card"><i class="fa-solid fa-circle-check"></i> Infrastructure as Code</div>
      <div class="check-item-card"><i class="fa-solid fa-circle-check"></i> Cloud infrastructure</div>
      <div class="check-item-card"><i class="fa-solid fa-circle-check"></i> Monitoring and observability</div>
      <div class="check-item-card"><i class="fa-solid fa-circle-check"></i> Git/GitHub workflow</div>
      <div class="check-item-card"><i class="fa-solid fa-circle-check"></i> Release validation</div>
      <!-- 15TH CAPABILITY: RELEASE IMAGE PUBLICATION -->
      <div class="check-item-card"><i class="fa-solid fa-circle-check"></i> Release Image Publication</div>
    </div>
  </section>

  <!-- 14. ABOUT THE BUILDER (PERSONAL PORTFOLIO CARD) -->
  <section class="about-builder-section" id="builder">
    <div class="profile-card-3d">
      <div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--orange-launch); font-weight: 800; letter-spacing: 2px; margin-bottom: 8px;">
          ABOUT THE BUILDER
        </div>
        <h2 style="font-size: 38px; font-weight: 900; margin-bottom: 8px;">SAMUEL D</h2>
        <div style="font-size: 15px; color: var(--cyan-beam); font-weight: 700; margin-bottom: 16px;">
          Final-Year B.E. Computer Science and Engineering Student • Prathyusha Engineering College
        </div>
        
        <p style="font-size: 14px; color: var(--text-dim); line-height: 1.7; margin-bottom: 20px;">
          Aspiring DevOps & Cloud Engineer. "I build practical cloud and DevOps systems focused on automation, containerization, CI/CD, Kubernetes, and cloud infrastructure."
        </p>

        <div style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--text-main);">
          <strong>Focus Areas:</strong> Cloud Engineering • DevOps • CI/CD • Docker • Kubernetes • AWS • Terraform • Observability
        </div>

        <div class="profile-links-flex">
          <a class="link-btn-social" href="https://www.linkedin.com/in/samueld14/" target="_blank" rel="noopener noreferrer">
            <i class="fa-brands fa-linkedin"></i> LINKEDIN
          </a>
          <a class="link-btn-social" href="https://github.com/JOSESAMUEL14" target="_blank" rel="noopener noreferrer">
            <i class="fa-brands fa-github"></i> GITHUB
          </a>
          <a class="link-btn-social" href="https://leetcode.com/u/josesamuel14/" target="_blank" rel="noopener noreferrer">
            <i class="fa-solid fa-code"></i> LEETCODE
          </a>
          <a class="link-btn-social" href="https://mail.google.com/mail/?view=cm&fs=1&to=Josesamueld2005@gmail.com" target="_blank" rel="noopener noreferrer">
            <i class="fa-solid fa-envelope"></i> EMAIL
          </a>
        </div>
      </div>

      <div style="background: rgba(0,0,0,0.5); border-radius: 24px; padding: 32px; border: 1px solid var(--border-light); text-align: center;">
        <i class="fa-solid fa-paper-plane" style="font-size: 48px; color: var(--orange-launch); margin-bottom: 16px;"></i>
        <h3 style="font-size: 24px; font-weight: 900; margin-bottom: 10px;">LET'S BUILD SOMETHING</h3>
        <p style="font-size: 13px; color: var(--text-dim); line-height: 1.6; margin-bottom: 20px;">
          Open to Cloud & DevOps engineering opportunities, infrastructure automation, and technical collaboration.
        </p>
        <a class="btn-launch" href="https://www.linkedin.com/in/samueld14/" target="_blank" rel="noopener noreferrer" style="width: 100%;">
          <i class="fa-brands fa-linkedin"></i> GET IN TOUCH
        </a>
      </div>
    </div>
  </section>

</main>

<!-- GLOBAL INTERACTIVE STAGE POPOVER -->
<div id="stagePopover" class="stage-popover" aria-hidden="true">
  <div class="popover-header-flex">
    <span class="popover-badge" id="pop-num">STAGE 01</span>
    <span class="popover-title-main" id="pop-title-main">Code Commit</span>
  </div>
  <div class="popover-section">
    <div class="popover-sec-title"><i class="fa-solid fa-circle-info"></i> WHAT HAPPENS?</div>
    <div class="popover-text" id="pop-happens"></div>
  </div>
  <div class="popover-section">
    <div class="popover-sec-title"><i class="fa-solid fa-bullseye"></i> WHY?</div>
    <div class="popover-text" id="pop-why"></div>
  </div>
  <div class="popover-section">
    <div class="popover-sec-title"><i class="fa-solid fa-diagram-project"></i> SIMPLE FLOW</div>
    <div class="popover-flow-box" id="pop-flow"></div>
  </div>
  <div class="popover-section">
    <div class="popover-sec-title"><i class="fa-solid fa-square-check"></i> RESULT</div>
    <div class="popover-result-text" id="pop-result"></div>
  </div>
</div>

<!-- LAUNCH MODAL DIALOG (VISITOR DEMO + OWNER MODES) -->
<div id="launchModal" class="modal-launch-overlay" role="dialog" aria-modal="true" aria-labelledby="modalTitle">
  <div class="modal-launch-box">
    <!-- MODAL MODE TABS -->
    <div class="modal-mode-tabs" style="display: flex; background: rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 4px; margin-bottom: 20px; gap: 4px; border: 1px solid var(--border-light);">
      <button id="tabDemoBtn" class="modal-tab-btn active" type="button" onclick="switchLaunchModalMode('demo')" style="flex: 1; padding: 10px; border-radius: 9px; border: none; background: var(--orange-launch); color: #000; font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 800; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px;">
        <i class="fa-solid fa-play"></i> VISITOR DEMO MODE
      </button>
      <button id="tabOwnerBtn" class="modal-tab-btn" type="button" onclick="switchLaunchModalMode('owner')" style="flex: 1; padding: 10px; border-radius: 9px; border: none; background: transparent; color: var(--text-dim); font-family: 'JetBrains Mono', monospace; font-size: 12px; font-weight: 800; cursor: pointer; display: flex; align-items: center; justify-content: center; gap: 8px;">
        <i class="fa-solid fa-lock"></i> OWNER MODE
      </button>
    </div>

    <!-- 1. VISITOR DEMO MODE PANEL -->
    <div id="modal-panel-demo" class="modal-mode-panel" style="display: block;">
      <h3 id="modalTitle" style="font-size: 21px; font-weight: 900; margin-bottom: 10px; color: var(--orange-launch); display: flex; align-items: center; gap: 10px;">
        <i class="fa-solid fa-satellite-dish"></i> INTERACTIVE PIPELINE DEMO
      </h3>
      <p style="color: var(--text-dim); font-size: 13.5px; line-height: 1.6; margin-bottom: 18px;">
        Simulate software changes progressing physically through all 16 CI/CD stages right in your browser. No secrets or tokens needed.
      </p>

      <div id="demoProgressBox" class="demo-progress-container" style="display: none; background: rgba(0, 0, 0, 0.4); border: 1px solid var(--border-light); border-radius: 12px; padding: 14px; margin: 18px 0;">
        <div style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 700; margin-bottom: 4px;">
          <span id="demoStageName" style="color: var(--orange-launch); font-weight: 700;">INITIALIZING...</span>
          <span id="demoStagePercent" style="color: var(--cyan-beam);">0%</span>
        </div>
        <div style="width: 100%; height: 8px; background: rgba(255, 255, 255, 0.1); border-radius: 999px; overflow: hidden; margin: 10px 0;">
          <div id="demoProgressBar" style="height: 100%; width: 0%; background: linear-gradient(90deg, var(--orange-launch), var(--cyan-beam)); border-radius: 999px; transition: width 0.3s ease;"></div>
        </div>
        <div id="demoStageLog" style="font-family: 'JetBrains Mono', monospace; font-size: 12px; color: var(--cyan-beam); line-height: 1.5; min-height: 36px;">
          Preparing simulation runner...
        </div>
      </div>

      <div style="background: rgba(255, 107, 0, 0.08); border: 1px dashed rgba(255, 107, 0, 0.3); border-radius: 10px; padding: 12px; margin-bottom: 20px;">
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--orange-launch); font-weight: 700; display: flex; align-items: center; gap: 6px;">
          <i class="fa-solid fa-triangle-exclamation"></i> SIMULATION — NO REAL DEPLOYMENT TRIGGERED
        </div>
        <p style="font-size: 12px; color: var(--text-dim); margin-top: 4px;">
          This demo runs purely in your browser for educational demonstration and does not dispatch GitHub Actions workflows.
        </p>
      </div>

      <div style="display: flex; gap: 12px; justify-content: flex-end;">
        <button class="btn-explore" type="button" onclick="closeLaunchModal()">CLOSE</button>
        <button id="btn-start-demo" class="btn-launch" type="button" onclick="startVisitorDemoSimulation()">
          <i class="fa-solid fa-play"></i> START SIMULATION
        </button>
      </div>
    </div>

    <!-- 2. OWNER MODE PANEL -->
    <div id="modal-panel-owner" class="modal-mode-panel" style="display: none;">
      <h3 style="font-size: 21px; font-weight: 900; margin-bottom: 10px; color: var(--orange-launch); display: flex; align-items: center; gap: 10px;">
        <i class="fa-solid fa-lock"></i> OWNER DEPLOYMENT DISPATCH
      </h3>
      <p style="color: var(--text-dim); font-size: 13.5px; line-height: 1.6; margin-bottom: 18px;">
        Trigger the real GitHub Actions CI/CD workflow via server-side repository dispatch on <code>JOSESAMUEL14/multicloud-cicd</code>.
      </p>

      <div style="margin-bottom: 18px; text-align: left;">
        <label for="triggerKeyInput" style="display: block; font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 700; color: var(--cyan-beam); margin-bottom: 8px; letter-spacing: 1px; text-transform: uppercase;">
          <i class="fa-solid fa-key" style="margin-right: 4px;"></i> Security Trigger Key (Required If Configured)
        </label>
        <input type="password" id="triggerKeyInput" placeholder="Enter server trigger key if enabled" autocomplete="off"
               style="width: 100%; padding: 12px 16px; border-radius: 10px; background: rgba(0, 0, 0, 0.4); border: 1px solid var(--border-light); color: #FFF; font-family: 'JetBrains Mono', monospace; font-size: 13px; outline: none; transition: border-color 0.2s;"
               onfocus="this.style.borderColor='var(--orange-launch)'" onblur="this.style.borderColor='var(--border-light)'">
      </div>

      <div id="owner-resp-box" style="display: none; background: rgba(0, 0, 0, 0.4); border-radius: 12px; padding: 14px; margin-bottom: 18px; text-align: left; border: 1px solid var(--border-light);">
        <div id="owner-resp-header" style="font-family: 'JetBrains Mono', monospace; font-size: 11.5px; font-weight: 800; margin-bottom: 6px;"></div>
        <div id="owner-resp-body"></div>
      </div>

      <div style="display: flex; gap: 12px; justify-content: flex-end;">
        <button class="btn-explore" type="button" onclick="closeLaunchModal()">CANCEL</button>
        <button id="btn-confirm-owner" class="btn-launch" type="button" onclick="confirmOwnerDeploymentLaunch()">
          <i class="fa-solid fa-rocket"></i> CONFIRM LAUNCH
        </button>
      </div>
    </div>
  </div>
</div>

<!-- FOOTER -->
<footer>
  <p style="font-weight: 700; color: #FFF; font-size: 13px; margin-bottom: 8px;">
    Multi-Cloud CI/CD Deployment System • Developed by Samuel D
  </p>
  <p style="display: flex; gap: 20px; justify-content: center; flex-wrap: wrap;">
    <a href="https://multicloud-cicd.onrender.com/" target="_blank" rel="noopener noreferrer"><i class="fa-solid fa-globe"></i> Live Demo (Render)</a>
    <a href="https://github.com/JOSESAMUEL14/multicloud-cicd" target="_blank" rel="noopener noreferrer"><i class="fa-brands fa-github"></i> GitHub Repository</a>
    <a href="https://leetcode.com/u/josesamuel14/" target="_blank" rel="noopener noreferrer"><i class="fa-solid fa-code"></i> LeetCode</a>
    <a href="https://www.linkedin.com/in/samueld14/" target="_blank" rel="noopener noreferrer"><i class="fa-brands fa-linkedin"></i> LinkedIn</a>
    <a href="https://mail.google.com/mail/?view=cm&fs=1&to=Josesamueld2005@gmail.com" target="_blank" rel="noopener noreferrer"><i class="fa-solid fa-envelope"></i> Josesamueld2005@gmail.com</a>
  </p>
</footer>

<script>
/* 1. 16 STAGE EXPLANATIONS DATA DICTIONARY */
const STAGE_DETAILS = {{
  "01": {{
    title: "Code Commit",
    happens: "The developer changes the Flask application or project files and creates a Git commit.",
    why: "Git records the change so the exact version of the code can be tracked.",
    flow: "Code Change → Git Commit",
    result: "A traceable version of the project is ready to be pushed."
  }},
  "02": {{
    title: "GitHub Repository",
    happens: "The committed code is pushed to the GitHub repository.",
    why: "GitHub becomes the central source repository and provides the trigger for the CI workflow.",
    flow: "Local Repository → GitHub",
    result: "The new code is available to the CI system."
  }},
  "03": {{
    title: "GitHub Actions",
    happens: "GitHub Actions detects the push or dispatch event and starts the automated workflow.",
    why: "Every change must be automatically validated without manual intervention.",
    flow: "GitHub Event → Actions Runner",
    result: "The CI pipeline begins execution in an isolated Ubuntu runner."
  }},
  "04": {{
    title: "Pytest Suite",
    happens: "The test suite runs unit tests for endpoints, metrics, and health checks.",
    why: "Tests confirm the application works correctly before any container image is built.",
    flow: "Flask Code → Pytest Execution",
    result: "Zero regression errors verified across the codebase."
  }},
  "05": {{
    title: "Docker Build",
    happens: "Docker builds the container image containing Python, Flask, dependencies, and app code.",
    why: "Containers make the runtime environment identical everywhere.",
    flow: "Dockerfile → Docker Image",
    result: "An immutable application container image is created."
  }},
  "06": {{
    title: "Docker Smoke Test",
    happens: "The newly built container is started and its health endpoint is checked.",
    why: "A smoke test quickly verifies that the container can start and respond correctly.",
    flow: "Docker Image → Container → /health",
    result: "Basic container functionality is verified."
  }},
  "07": {{
    title: "Trivy Vulnerability Scan",
    happens: "Trivy scans the container image for security vulnerabilities and CVEs.",
    why: "Security vulnerabilities must be caught before deployment.",
    flow: "Container Image → Trivy Audit",
    result: "A secure container image with no blocking CVEs."
  }},
  "08": {{
    title: "Kind K8s Cluster",
    happens: "An ephemeral Kubernetes cluster is created using Kind directly on the CI runner.",
    why: "Testing inside real Kubernetes validates Kubernetes manifests before cloud release.",
    flow: "CI Runner → Kind Cluster Started",
    result: "A temporary Kubernetes testing environment is ready."
  }},
  "09": {{
    title: "K8s Deployment Rollout",
    happens: "Kubernetes manifests (Deployment and Service) are applied to the Kind cluster.",
    why: "This verifies that manifests are syntactically valid and apply cleanly.",
    flow: "k8s/deployment.yaml → kubectl apply",
    result: "Kubernetes begins creating pods and services."
  }},
  "10": {{
    title: "2 Pod Replicas Ready",
    happens: "Kubernetes schedules and runs two replica pods of the application.",
    why: "Running multiple replicas provides high availability and fault tolerance.",
    flow: "Deployment → 2 Pods Running",
    result: "Two healthy pods are verified running in the cluster."
  }},
  "11": {{
    title: "K8s In-Cluster Health",
    happens: "The CI runner connects through the Kubernetes Service to verify the application inside the cluster.",
    why: "This proves that routing, ports, and service load balancing work.",
    flow: "K8s Service → Pod Endpoint → 200 OK",
    result: "Cluster networking and application health verified."
  }},
  "12": {{
    title: "Docker Hub SHA Tag",
    happens: "The verified Docker image is pushed to Docker Hub with an immutable Git commit SHA tag.",
    why: "SHA tags ensure exact traceability and make rollback fast and reliable.",
    flow: "Verified Image → Docker Hub (SHA Tag)",
    result: "The release image is securely stored in the container registry."
  }},
  "13": {{
    title: "AWS EC2 Target",
    happens: "The deployment pipeline targets the AWS EC2 virtual machine provisioned by Terraform.",
    why: "AWS provides enterprise cloud compute capacity.",
    flow: "Image Registry → AWS EC2 Container",
    result: "The application runs in the AWS cloud environment."
  }},
  "14": {{
    title: "Render Cloud Target",
    happens: "The application is deployed to the Render managed cloud platform.",
    why: "Render provides a public live demo environment with zero server maintenance.",
    flow: "Docker Hub → Render Web Service",
    result: "The public live demo is updated and accessible."
  }},
  "15": {{
    title: "Prometheus Observability",
    happens: "Prometheus monitors the application using the /metrics endpoint.",
    why: "Observability provides visibility into throughput, latencies, and uptime.",
    flow: "App /metrics → Prometheus Scraper",
    result: "Live metrics and telemetry are collected for monitoring."
  }},
  "16": {{
    title: "Live System Online",
    happens: "The entire deployment is complete and serving live traffic across targets.",
    why: "Users can now interact with the verified release of the project.",
    flow: "End-to-End Pipeline → Production Release",
    result: "A resilient, secure, multi-cloud system is live."
  }}
}};

/* 2. POPOVER INTERACTION ENGINE (VIEWPORT POSITIONING & PINNING) */
const popover = document.getElementById('stagePopover');
const stageCards = document.querySelectorAll('.journey-step-card');
let currentPinnedStage = null;
let currentHoveredCard = null;

function renderPopoverData(stageId) {{
  const data = STAGE_DETAILS[stageId];
  if (!data) return;
  const numEl = document.getElementById('pop-num') || document.getElementById('pop-stage-num');
  if (numEl) numEl.textContent = 'STAGE ' + stageId;
  const titleEl = document.getElementById('pop-title-main');
  if (titleEl) titleEl.textContent = data.title;
  const happensEl = document.getElementById('pop-happens');
  if (happensEl) happensEl.textContent = data.happens;
  const whyEl = document.getElementById('pop-why');
  if (whyEl) whyEl.textContent = data.why;
  const flowEl = document.getElementById('pop-flow');
  if (flowEl) flowEl.textContent = data.flow;
  const resultEl = document.getElementById('pop-result');
  if (resultEl) resultEl.textContent = data.result;
}}

function positionPopover(card) {{
  if (!card) return;
  const rect = card.getBoundingClientRect();
  const popWidth = 360;
  const popHeight = popover.offsetHeight || 260;
  const margin = 14;

  let top = rect.bottom + margin;
  let left = rect.left + (rect.width / 2) - (popWidth / 2);

  if (top + popHeight > window.innerHeight - margin) {{
    top = rect.top - popHeight - margin;
  }}

  if (top < margin) {{
    top = margin;
  }}

  if (left + popWidth > window.innerWidth - margin) {{
    left = window.innerWidth - popWidth - margin;
  }}
  if (left < margin) {{
    left = margin;
  }}

  popover.style.top = `${{top}}px`;
  popover.style.left = `${{left}}px`;
}}

function showPopoverForCard(card) {{
  const stageId = card.getAttribute('data-stage');
  renderPopoverData(stageId);
  popover.classList.add('visible');
  popover.setAttribute('aria-hidden', 'false');
  positionPopover(card);
}}

function hidePopover() {{
  if (currentPinnedStage) return;
  popover.classList.remove('visible');
  popover.setAttribute('aria-hidden', 'true');
  currentHoveredCard = null;
}}



window.addEventListener('scroll', () => {{
  const target = currentPinnedStage 
    ? document.querySelector(`.journey-step-card[data-stage="${{currentPinnedStage}}"]`)
    : currentHoveredCard;
  if (target && popover.classList.contains('visible')) {{
    positionPopover(target);
  }}
}}, {{ passive: true }});

window.addEventListener('resize', () => {{
  const target = currentPinnedStage 
    ? document.querySelector(`.journey-step-card[data-stage="${{currentPinnedStage}}"]`)
    : currentHoveredCard;
  if (target && popover.classList.contains('visible')) {{
    positionPopover(target);
  }}
}});

document.addEventListener('keydown', (e) => {{
  if (e.key === 'Escape') {{
    currentPinnedStage = null;
    stageCards.forEach(c => c.classList.remove('active'));
    hidePopover();
    const modal = document.getElementById('launchModal');
    if (modal && modal.classList.contains('active')) {{
      closeLaunchModal();
    }}
  }}
}});

document.addEventListener('click', (e) => {{
  if (currentPinnedStage && !e.target.closest('.journey-step-card') && !e.target.closest('#stagePopover')) {{
    currentPinnedStage = null;
    stageCards.forEach(c => c.classList.remove('active'));
    hidePopover();
  }}
}});

/* 3. REAL MONOTONIC PROCESS UPTIME TIMER */
let serverBaseSeconds = 0;
let clientEpochAtFetch = Date.now();

function formatSecondsToHMS(totalSecs) {{
  const hours = Math.floor(totalSecs / 3600);
  const minutes = Math.floor((totalSecs % 3600) / 60);
  const seconds = Math.floor(totalSecs % 60);
  return `${{String(hours).padStart(2, '0')}}:${{String(minutes).padStart(2, '0')}}:${{String(seconds).padStart(2, '0')}}`;
}}

function updateUptimeDisplay() {{
  const uptEl = document.getElementById('mon-uptime');
  if (!uptEl) return;
  const elapsedSinceFetch = Math.floor((Date.now() - clientEpochAtFetch) / 1000);
  const currentTotal = serverBaseSeconds + Math.max(0, elapsedSinceFetch);
  uptEl.textContent = formatSecondsToHMS(currentTotal);
}}

setInterval(updateUptimeDisplay, 1000);

function pollServerStats() {{
  fetch('/stats')
    .then(r => r.json())
    .then(d => {{
      if (d.total_requests !== undefined) {{
        const reqEl = document.getElementById('mon-requests');
        if (reqEl) reqEl.textContent = d.total_requests;
      }}
      if (d.start_time) {{
        const nowSec = Date.now() / 1000;
        serverBaseSeconds = Math.max(0, Math.floor(nowSec - d.start_time));
        clientEpochAtFetch = Date.now();
      }} else if (d.uptime_seconds !== undefined) {{
        serverBaseSeconds = d.uptime_seconds;
        clientEpochAtFetch = Date.now();
      }}
      updateUptimeDisplay();
    }})
    .catch(() => {{}});
}}

pollServerStats();
setInterval(pollServerStats, 15000);

/* 4. LAUNCH MODAL ENGINE (DEMO MODE & OWNER MODE) */
let demoSimulationTimer = null;
let isDemoRunning = false;

function executeInteractiveLaunchSequence(e) {{
  if (e) e.preventDefault();
  openLaunchModal();
}}

function openLaunchModal() {{
  const modal = document.getElementById('launchModal');
  modal.classList.add('active');
  switchLaunchModalMode('demo');
}}

function closeLaunchModal() {{
  const modal = document.getElementById('launchModal');
  modal.classList.remove('active');
  if (demoSimulationTimer) {{
    clearInterval(demoSimulationTimer);
    isDemoRunning = false;
  }}
}}

let hoverTimer = null;

function showStagePopover(cardEl, stageId) {{
  if (currentPinnedStage) return;
  currentHoveredCard = cardEl;
  if (hoverTimer) clearTimeout(hoverTimer);
  hoverTimer = setTimeout(() => {{
    if (currentHoveredCard === cardEl && !currentPinnedStage) {{
      showPopoverForCard(cardEl);
    }}
  }}, 2000);
}}

function hideStagePopover() {{
  if (hoverTimer) {{ clearTimeout(hoverTimer); hoverTimer = null; }}
  hidePopover();
}}

function toggleStagePopover(cardEl, stageId, evt) {{
  if (evt) evt.stopPropagation();
  if (hoverTimer) {{ clearTimeout(hoverTimer); hoverTimer = null; }}
  if (currentPinnedStage === stageId) {{
    currentPinnedStage = null;
    stageCards.forEach(c => c.classList.remove('active'));
    popover.classList.remove('visible');
    popover.setAttribute('aria-hidden', 'true');
    currentHoveredCard = null;
  }} else {{
    currentPinnedStage = stageId;
    stageCards.forEach(c => c.classList.remove('active'));
    cardEl.classList.add('active');
    showPopoverForCard(cardEl);
  }}
}}

function switchLaunchModalMode(mode) {{
  const tabDemo = document.getElementById('tabDemoBtn');
  const tabOwner = document.getElementById('tabOwnerBtn');
  const panelDemo = document.getElementById('modal-panel-demo');
  const panelOwner = document.getElementById('modal-panel-owner');

  if (mode === 'demo') {{
    tabDemo.classList.add('active');
    tabDemo.style.background = 'var(--orange-launch)';
    tabDemo.style.color = '#000';
    tabOwner.classList.remove('active');
    tabOwner.style.background = 'transparent';
    tabOwner.style.color = 'var(--text-dim)';
    panelDemo.classList.add('active');
    panelDemo.style.display = 'block';
    panelOwner.classList.remove('active');
    panelOwner.style.display = 'none';
  }} else {{
    tabOwner.classList.add('active');
    tabOwner.style.background = 'var(--orange-launch)';
    tabOwner.style.color = '#000';
    tabDemo.classList.remove('active');
    tabDemo.style.background = 'transparent';
    tabDemo.style.color = 'var(--text-dim)';
    panelOwner.classList.add('active');
    panelOwner.style.display = 'block';
    panelDemo.classList.remove('active');
    panelDemo.style.display = 'none';
  }}
}}

/* VISITOR DEMO MODE SIMULATION (NO /deploy CALL) */
const DEMO_STAGES = [
  {{ num: "01", name: "Code Commit", log: "Local git commit recorded on development branch." }},
  {{ num: "02", name: "GitHub Repository", log: "Code pushed to branch; GitHub webhook verifies trigger events." }},
  {{ num: "03", name: "GitHub Actions", log: "Ubuntu runner initialized; Python 3.12 environment established." }},
  {{ num: "04", name: "Pytest Suite", log: "Running pytest unit & integration tests... 100% PASSED." }},
  {{ num: "05", name: "Docker Build", log: "Container image built with commit SHA tag from Dockerfile." }},
  {{ num: "06", name: "Docker Smoke Test", log: "Local container started; /health endpoint returned 200 OK." }},
  {{ num: "07", name: "Trivy Vulnerability Scan", log: "Security scan completed with 0 critical CVE vulnerabilities." }},
  {{ num: "08", name: "Kind K8s Cluster", log: "Spinning up ephemeral Kind Kubernetes test cluster in runner..." }},
  {{ num: "09", name: "K8s Deployment Rollout", log: "Applying k8s/deployment.yaml manifests to cluster..." }},
  {{ num: "10", name: "2 Pod Replicas Ready", log: "2/2 pod replicas transitioned to healthy and ready status." }},
  {{ num: "11", name: "K8s In-Cluster Health", log: "In-cluster port forward test against service endpoint verified." }},
  {{ num: "12", name: "Docker Hub SHA Tag", log: "Image pushed to Docker Hub registry with immutable SHA tag." }},
  {{ num: "13", name: "AWS EC2 Target", log: "Terraform-provisioned AWS EC2 host notified of updated image." }},
  {{ num: "14", name: "Render Cloud Target", log: "Render deployment webhook executed; rolling update completed." }},
  {{ num: "15", name: "Prometheus Observability", log: "Prometheus metric scraper confirmed active on /metrics." }},
  {{ num: "16", name: "Live System Online", log: "All 16 stages complete! Release online and healthy across targets." }}
];

function startVisitorDemoSimulation() {{
  if (isDemoRunning) return;
  isDemoRunning = true;

  const progressBox = document.getElementById('demoProgressBox');
  const startBtn = document.getElementById('btn-start-demo');
  const stageName = document.getElementById('demoStageName');
  const stagePercent = document.getElementById('demoStagePercent');
  const progressBar = document.getElementById('demoProgressBar');
  const stageLog = document.getElementById('demoStageLog');

  progressBox.style.display = 'block';
  startBtn.disabled = true;
  startBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> RUNNING SIMULATION...';

  triggerRocketAnimation();

  let index = 0;
  progressBar.style.width = '0%';

  demoSimulationTimer = setInterval(() => {{
    if (index >= DEMO_STAGES.length) {{
      clearInterval(demoSimulationTimer);
      isDemoRunning = false;
      startBtn.disabled = false;
      startBtn.innerHTML = '<i class="fa-solid fa-rotate-right"></i> RE-RUN SIMULATION';
      stageName.textContent = 'DEMO COMPLETE — 100%';
      stagePercent.textContent = '100%';
      progressBar.style.width = '100%';
      stageLog.innerHTML = '<span style="color: var(--sec-green); font-weight: 700;">✓ SIMULATION COMPLETED: All 16 CI/CD stages verified in-browser.</span>';
      return;
    }}

    const s = DEMO_STAGES[index];
    const pct = Math.round(((index + 1) / DEMO_STAGES.length) * 100);
    stageName.textContent = `STAGE ${{s.num}} — ${{s.name.toUpperCase()}}`;
    stagePercent.textContent = `${{pct}}%`;
    progressBar.style.width = `${{pct}}%`;
    stageLog.innerHTML = `<span style="color: #FFF;">${{s.log}}</span>`;

    index++;
  }}, 500);
}}

/* OWNER MODE REAL DISPATCH */
function confirmOwnerDeploymentLaunch() {{
  const confirmBtn = document.getElementById('btn-confirm-owner');
  const keyInput = document.getElementById('triggerKeyInput');
  const triggerKey = keyInput ? keyInput.value.trim() : '';
  const respBox = document.getElementById('owner-resp-box');
  const respHeader = document.getElementById('owner-resp-header');
  const respBody = document.getElementById('owner-resp-body');

  if (confirmBtn) confirmBtn.disabled = true;
  confirmBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> TRIGGERING CI/CD...';

  respBox.style.display = 'block';
  respHeader.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> DISPATCHING REPOSITORY EVENT...';
  respHeader.style.color = 'var(--cyan-beam)';
  respBody.innerHTML = '<p style="color: var(--text-dim);">Sending repository dispatch to GitHub Actions API...</p>';

  fetch('/deploy', {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json' }},
    body: JSON.stringify({{ trigger_key: triggerKey, event_type: 'manual-deploy' }})
  }})
  .then(r => r.json())
  .then(d => {{
    if (confirmBtn) {{
      confirmBtn.disabled = false;
      confirmBtn.innerHTML = '<i class="fa-solid fa-rocket"></i> CONFIRM LAUNCH';
    }}

    if (d.success) {{
      respHeader.innerHTML = '<i class="fa-solid fa-circle-check" style="color: var(--sec-green);"></i> DEPLOYMENT TRIGGERED';
      respHeader.style.color = 'var(--sec-green)';
      respBody.innerHTML = '<p style="margin-bottom: 10px; font-weight: 700; color: var(--text-main);">' + (d.message || 'GitHub Actions workflow triggered successfully.') + '</p>' +
        '<p style="font-size: 13px; color: var(--text-dim); margin-bottom: 16px; line-height: 1.6;">GitHub Actions has received the deployment event and started CI validation stages.</p>' +
        '<a href="https://github.com/JOSESAMUEL14/multicloud-cicd/actions" target="_blank" rel="noopener noreferrer" class="btn-launch" style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.9), rgba(5, 150, 105, 0.9)); box-shadow: 0 10px 25px rgba(16, 185, 129, 0.4); text-decoration: none; font-size: 11.5px; padding: 10px 20px; border-radius: 10px; display: inline-flex; align-items: center; gap: 8px;">' +
        '<i class="fa-brands fa-github"></i> VIEW GITHUB ACTIONS</a>';
      triggerRocketAnimation();
    }} else {{
      respHeader.innerHTML = '<i class="fa-solid fa-triangle-exclamation" style="color: var(--aws-orange);"></i> DEPLOYMENT TRIGGER FAILED';
      respHeader.style.color = 'var(--aws-orange)';
      respBody.innerHTML = '<p style="font-weight: 700; margin-bottom: 6px; color: var(--text-main);">' + (d.message || 'GitHub rejected the workflow trigger.') + '</p><p style="color: var(--text-dim); font-size: 12px;">No workflow was dispatched.</p>';
    }}
  }})
  .catch(e => {{
    if (confirmBtn) {{
      confirmBtn.disabled = false;
      confirmBtn.innerHTML = '<i class="fa-solid fa-rocket"></i> CONFIRM LAUNCH';
    }}
    respHeader.innerHTML = '<i class="fa-solid fa-circle-xmark" style="color: var(--sec-red);"></i> NETWORK / SERVER ERROR';
    respHeader.style.color = 'var(--sec-red)';
    respBody.innerHTML = '<p style="color: var(--text-dim); font-size: 13px;">Unable to contact the server /deploy route.</p>';
  }});
}}

function triggerRocketAnimation() {{
  const rocket = document.getElementById('mainRocket');
  if (rocket) {{
    rocket.classList.add('launching');
    setTimeout(() => {{
      rocket.classList.remove('launching');
    }}, 3000);
  }}
}}

document.getElementById('launchModal').addEventListener('click', e => {{
  if (e.target === e.currentTarget) closeLaunchModal();
}});
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
        "total_requests": total_requests,
        "uptime": get_uptime(),
        "uptime_seconds": int(time.time() - START_TIME),
        "start_time": START_TIME,
        "cloud": os.getenv("CLOUD_PROVIDER", "local"),
        "hostname": socket.gethostname()
    }
    return jsonify(data), 200


@app.route("/deploy", methods=["POST"])
def deploy():
    req_data = request.get_json(silent=True) or {}
    
    expected_trigger_key = os.getenv("DEPLOY_TRIGGER_KEY", "").strip()
    if expected_trigger_key:
        provided_key = str(req_data.get("trigger_key", "")).strip()
        if not hmac.compare_digest(provided_key, expected_trigger_key):
            return jsonify({
                "success": False,
                "message": "Deployment trigger key is invalid or required for this environment."
            }), 200

    token = os.getenv("GITHUB_TOKEN", "").strip()
    if not token:
        return jsonify({
            "success": False,
            "message": "GitHub token is not configured on this server."
        }), 200

    try:
        r = requests.post(
            "https://api.github.com/repos/JOSESAMUEL14/multicloud-cicd/dispatches",
            headers={
                "Authorization": f"Bearer {token}",
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
                "Content-Type": "application/json",
                "User-Agent": "MultiCloud-CICD-App"
            },
            json={"event_type": "manual-deploy"},
            timeout=10
        )
        if r.status_code == 204:
            return jsonify({
                "success": True,
                "message": "GitHub Actions workflow triggered successfully.",
                "workflow": "manual-deploy",
                "actions_url": "https://github.com/JOSESAMUEL14/multicloud-cicd/actions"
            }), 200
        elif r.status_code in (401, 403):
            return jsonify({
                "success": False,
                "message": "GitHub rejected the workflow trigger. Check server token permissions."
            }), 200
        elif r.status_code == 404:
            return jsonify({
                "success": False,
                "message": "GitHub repository not found or token lacks repository access."
            }), 200
        else:
            return jsonify({
                "success": False,
                "message": f"GitHub API returned status {r.status_code}."
            }), 200
    except Exception:
        return jsonify({
            "success": False,
            "message": "Unable to communicate with GitHub API server-side."
        }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
