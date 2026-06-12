# Multi-Cloud CI/CD Pipeline

[![CI/CD Pipeline](https://github.com/JOSESAMUEL14/multicloud-cicd/actions/workflows/deploy.yml/badge.svg)](https://github.com/JOSESAMUEL14/multicloud-cicd/actions/workflows/deploy.yml)
![Docker](https://img.shields.io/badge/Docker-29.1.3-blue)
![Kubernetes](https://img.shields.io/badge/Kubernetes-v1.34.1-blue)
![Terraform](https://img.shields.io/badge/Terraform-v1.15.5-purple)
![AWS](https://img.shields.io/badge/AWS-EC2-orange)
![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus-red)
![Grafana](https://img.shields.io/badge/Dashboard-Grafana-orange)

A production-grade Multi-Cloud CI/CD pipeline that automatically builds, tests, and deploys a containerised Flask application to AWS EC2 and Render, monitored with Prometheus and Grafana.

---

## 🌐 Live Demo

| Platform | URL | Status |
|----------|-----|--------|
| Render (24/7) | https://multicloud-cicd.onrender.com | ✅ Always Live |
| AWS EC2 Mumbai | http://15.206.189.12:5000 | ⚡ When Running |

---

## 🛠️ Tech Stack

| Tool | Purpose | Version |
|------|---------|---------|
| Docker | Containerisation | 29.1.3 |
| Kubernetes | Container Orchestration | v1.34.1 |
| GitHub Actions | CI/CD Pipeline | - |
| Terraform | Infrastructure as Code | v1.15.5 |
| AWS EC2 | Cloud Deployment Mumbai | Free Tier |
| Prometheus | Metrics Collection | Latest |
| Grafana | Monitoring Dashboard | Latest |
| Python Flask | Web Application | 3.11.15 |

---

## ✨ Features

- ⚡ **Automated CI/CD** — Push code, Docker image built and deployed in under 60 seconds
- ☸️ **Kubernetes** — 2 replicas with self-healing and zero downtime rolling updates
- 📊 **Live Monitoring** — Prometheus scrapes metrics every 15 seconds, Grafana live dashboards
- 🏗️ **Infrastructure as Code** — Terraform provisions all AWS resources automatically
- 🌐 **Multi-Cloud** — Deployed on AWS EC2 Mumbai and Render simultaneously
- 🚀 **Interactive Dashboard** — Deploy button, health check API, live metrics
- 🔗 **Public URL** — Always accessible at multicloud-cicd.onrender.com

---

## 🔄 How It Works
git push origin main

↓

GitHub Actions triggers automatically

↓

Docker image built and pushed to Docker Hub

↓

Kubernetes rolling update (zero downtime)

↓

Live on AWS EC2 + Render in under 60 seconds

↓

Prometheus + Grafana monitoring everything

---

## 🚀 Quick Start

```bash
git clone https://github.com/JOSESAMUEL14/multicloud-cicd.git
cd multicloud-cicd
docker compose -f monitoring/docker-compose.yml up -d
```

Then open:
- App: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000 (admin/multicloud123)

---

## 📁 Project Structure
multicloud-cicd/

├── app/

│   ├── app.py              # Flask app + full website + REST API

│   ├── Dockerfile          # Container definition

│   └── requirements.txt    # Python dependencies

├── terraform/

│   └── aws-ec2.tf          # AWS infrastructure as code

├── scripts/

│   ├── deploy-aws.sh       # AWS deployment script

│   └── protect-aws.sh      # Billing protection script

├── monitoring/

│   ├── docker-compose.yml  # Prometheus + Grafana stack

│   └── prometheus.yml      # Prometheus scrape config

├── deployment.yaml         # Kubernetes deployment

├── service.yaml            # Kubernetes service

└── .github/workflows/

└── deploy.yml          # GitHub Actions CI/CD pipeline

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Interactive dashboard website |
| `/health` | GET | Real-time health check JSON |
| `/stats` | GET | Live request count and uptime |
| `/metrics` | GET | Prometheus metrics endpoint |
| `/deploy` | POST | Trigger GitHub Actions pipeline |

---

## 👨‍💻 Author

**Samuel D**
- 🐙 GitHub: https://github.com/JOSESAMUEL14
- 💼 LinkedIn: https://linkedin.com/in/samueld14
- 📧 Email: Josesamueld2005@gmail.com
- 🌐 Live Demo: https://multicloud-cicd.onrender.com

---

## 📝 License

MIT License — feel free to use this project as a reference!
