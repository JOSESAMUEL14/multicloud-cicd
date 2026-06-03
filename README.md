# Multi-Cloud CI/CD Pipeline

A production-grade CI/CD pipeline that automatically builds, tests, and deploys a containerised application to AWS, monitored with Prometheus and Grafana.

## Tech Stack

- Docker 29.1.3 — Containerisation
- Kubernetes v1.34.1 — Container Orchestration
- GitHub Actions — CI/CD Pipeline
- Terraform v1.15.5 — Infrastructure as Code
- AWS EC2 — Cloud Deployment
- Prometheus — Metrics Collection
- Grafana — Monitoring Dashboard
- Python Flask — Web Application

## Features

- Automated CI/CD — Push code, auto build and deploy in 30 seconds
- Kubernetes — 2 replicas with self-healing and zero downtime updates
- Live Monitoring — Prometheus and Grafana real time dashboard
- Infrastructure as Code — Terraform provisions all cloud resources
- Multi-cloud Ready — Architecture supports AWS and GCP

## Quick Start

git clone https://github.com/JOSESAMUEL14/multicloud-cicd.git
cd multicloud-cicd
docker compose -f monitoring/docker-compose.yml up -d

## Access

- App: http://localhost:5000
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Author

Jose Samuel D
GitHub: JOSESAMUEL14
LinkedIn: samueld14
Email: Josesamueld2005@gmail.com
