# Multi-Cloud CI/CD Pipeline

[![CI/CD Pipeline](https://github.com/JOSESAMUEL14/multicloud-cicd/actions/workflows/deploy.yml/badge.svg)](https://github.com/JOSESAMUEL14/multicloud-cicd/actions/workflows/deploy.yml)

A production-grade CI/CD pipeline that automatically builds, tests, and deploys a containerised application to AWS and Render, monitored with Prometheus and Grafana.

## Live Demo

Visit the live application:
https://multicloud-cicd.onrender.com

## Tech Stack

- Docker 29.1.3 — Containerisation
- Kubernetes v1.34.1 — Container Orchestration
- GitHub Actions — CI/CD Pipeline
- Terraform v1.15.5 — Infrastructure as Code
- AWS EC2 ap-south-1 — Cloud Deployment
- Render — Public Hosting
- Prometheus — Metrics Collection
- Grafana — Monitoring Dashboard
- Python Flask — Web Application

## Features

- Automated CI/CD — Push code, auto build and deploy in 30 seconds
- Kubernetes — 2 replicas with self-healing and zero downtime updates
- Live Monitoring — Prometheus and Grafana real time dashboard
- Infrastructure as Code — Terraform provisions all cloud resources
- Multi-cloud Ready — Deployed on AWS EC2 and Render simultaneously
- Public URL — Always accessible at multicloud-cicd.onrender.com

## Quick Start

git clone https://github.com/JOSESAMUEL14/multicloud-cicd.git
cd multicloud-cicd
docker compose -f monitoring/docker-compose.yml up -d

## Access

- Live App: https://multicloud-cicd.onrender.com
- Local App: http://localhost:5000
- AWS App: http://3.110.56.122:5000 (when EC2 running)
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000

## Project Structure

multicloud-cicd/
├── app/
│   ├── app.py              # Flask application with Prometheus metrics
│   ├── Dockerfile          # Container definition
│   └── requirements.txt    # Python dependencies
├── terraform/
│   └── aws-ec2.tf          # AWS infrastructure as code
├── scripts/
│   ├── deploy-aws.sh       # AWS deployment script
│   └── protect-aws.sh      # Billing protection script
├── monitoring/
│   ├── docker-compose.yml  # Monitoring stack
│   └── prometheus.yml      # Prometheus config
├── deployment.yaml         # Kubernetes deployment
├── service.yaml            # Kubernetes service
└── .github/workflows/
    └── deploy.yml          # GitHub Actions pipeline

## Author

Jose Samuel D
GitHub: https://github.com/JOSESAMUEL14
LinkedIn: https://linkedin.com/in/samueld14
Email: Josesamueld2005@gmail.com
Live Demo: https://multicloud-cicd.onrender.com
