🚀 Multi-Cloud CI/CD Pipeline

<p align="center">
  <strong>A production-style DevOps project for automated testing, containerization, security scanning, Kubernetes validation, cloud deployment, and monitoring.</strong>
</p>

<p align="center">
  <a href="https://github.com/JOSESAMUEL14/multicloud-cicd/actions">
    <img src="https://github.com/JOSESAMUEL14/multicloud-cicd/actions/workflows/deploy.yml/badge.svg" alt="CI/CD Pipeline">
  </a>
  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python" alt="Python 3.11">
  <img src="https://img.shields.io/badge/Docker-Containerized-blue?logo=docker" alt="Docker">
  <img src="https://img.shields.io/badge/Kubernetes-Kind-blue?logo=kubernetes" alt="Kubernetes">
  <img src="https://img.shields.io/badge/AWS-EC2-orange?logo=amazonaws" alt="AWS EC2">
  <img src="https://img.shields.io/badge/Terraform-IaC-purple?logo=terraform" alt="Terraform">
  <img src="https://img.shields.io/badge/Trivy-Security-red" alt="Trivy">
  <img src="https://img.shields.io/badge/Prometheus-Monitoring-orange?logo=prometheus" alt="Prometheus">
  <img src="https://img.shields.io/badge/Grafana-Observability-orange?logo=grafana" alt="Grafana">
</p>

🌐 Project Links

Resource

Service

Access

🌍 Live Application

Render Demo

🚀 Open Live Application

⚙️ CI/CD Pipeline

GitHub Actions

🔄 View Pipeline Runs

💻 Source Code

GitHub Repository

📂 View Repository

🐳 Container Registry

Docker Hub

📦 View Docker Image

☁️ AWS EC2 Demo

Current EC2 Deployment

🚀 Open AWS EC2 Application

📖 Documentation

GitHub README

📘 View Documentation

⚠️ AWS demo note: The EC2 instance is not kept running continuously. The current public IP is 13.201.186.250, but AWS public IP addresses can change after a stop/start cycle. The AWS link should therefore be treated as a live-demo link rather than a permanent URL.

☁️ AWS EC2 Deployment

The application has been successfully deployed to AWS EC2 through the automated CI/CD pipeline.

The EC2 instance is started only when a live demonstration is required, helping avoid unnecessary cloud usage.

Live Demonstration Flow

Git Push
   │
   ▼
GitHub Actions
   │
   ▼
Automated Tests
   │
   ▼
Docker Build
   │
   ▼
Trivy Security Scan
   │
   ▼
Kind Kubernetes Validation
   │
   ▼
Docker Hub
   │
   ▼
AWS EC2
   │
   ▼
Pull Exact Git SHA Image
   │
   ▼
Replace Existing Container
   │
   ▼
/health Verification
   │
   ▼
Deployment Verified

Demonstration & Contact

For a live demonstration of the AWS deployment and complete CI/CD workflow:

💼 LinkedIn: linkedin.com/in/samueld14

💻 GitHub: github.com/JOSESAMUEL14

📧 Email: Josesamueld2005@gmail.com

🎯 Project Overview

Multi-Cloud CI/CD Pipeline is a Flask-based DevOps project designed to demonstrate how an application can move through a practical CI/CD lifecycle.

The project combines:

🧪 Automated testing with Pytest

🐳 Docker containerization

🔒 Trivy vulnerability scanning

☸️ Kubernetes validation using Kind

📦 Docker Hub image publishing

☁️ AWS EC2 deployment

🔐 Immutable Git SHA image deployment

❤️ Automated health verification

🔄 Deployment rollback logic

📊 Prometheus monitoring

📈 Grafana dashboards

🖥️ Node Exporter system metrics

🏗️ Terraform infrastructure as code

🔀 Git/GitHub version control

The objective is not simply to collect DevOps tools, but to demonstrate how the tools work together as an automated engineering workflow.

🧭 DevOps Workflow

flowchart TD
    A["👨‍💻 Developer"] --> B["💻 GitHub Repository"]
    B --> C["⚙️ GitHub Actions"]

    C --> D["🧪 Pytest"]
    C --> E["🐳 Docker Build"]
    C --> F["🔒 Trivy Scan"]

    D --> G["☸️ Kind Kubernetes Validation"]
    E --> G
    F --> G

    G --> H["📦 Docker Hub"]
    H --> I["☁️ AWS EC2"]
    I --> J["🐳 Docker Container"]
    J --> K["❤️ /health"]
    K --> L["✅ Deployment Verified"]

🏗️ Architecture

flowchart TD
    A["Developer"] --> B["GitHub"]
    B --> C["GitHub Actions"]

    C --> D["Pytest Tests"]
    C --> E["Docker Build"]
    C --> F["Trivy Security Scan"]

    D --> G["Kind Kubernetes Validation"]
    E --> G
    F --> G

    G --> H["Docker Hub"]
    H --> I["AWS EC2"]
    I --> J["Flask Application"]
    J --> K["Port 5000"]
    K --> L["/health"]

🛠️ Technology Stack

Technology

Category

Purpose

Python / Flask

Application

Web application and REST API

Docker

Containerization

Application packaging and runtime

GitHub Actions

CI/CD

Continuous integration and deployment automation

Docker Hub

Registry

Container image storage and publishing

Kubernetes / Kind

Orchestration

CI/CD deployment validation

Terraform

Infrastructure as Code

AWS infrastructure configuration

AWS EC2

Cloud

Cloud deployment target

Prometheus

Monitoring

Time-series metric collection

Grafana

Visualization

Monitoring dashboards

Node Exporter

System Metrics

Host and OS metrics

Trivy

Security

Container vulnerability scanning

Git / GitHub

Version Control

Source control and collaboration

🔄 Complete CI/CD Pipeline

The GitHub Actions workflow performs multiple validation and deployment stages before the deployment is considered successful.

Pipeline Stages

01. Push to GitHub
        ↓
02. Checkout source code
        ↓
03. Setup Python 3.11
        ↓
04. Install dependencies
        ↓
05. Run Pytest
        ↓
06. Build Docker image
        ↓
07. Docker smoke test
        ↓
08. Trivy vulnerability scan
        ↓
09. Create Kind Kubernetes cluster
        ↓
10. Load Docker image into Kind
        ↓
11. Deploy Kubernetes manifests
        ↓
12. Wait for rollout
        ↓
13. Verify 2/2 replicas
        ↓
14. Verify application health
        ↓
15. Show Kubernetes diagnostics
        ↓
16. Publish Docker image on main
        ↓
17. SSH into AWS EC2
        ↓
18. Pull exact Git SHA image
        ↓
19. Replace existing container
        ↓
20. Start new container
        ↓
21. Verify /health endpoint
        ↓
22. Deployment successful

Workflow File

.github/workflows/deploy.yml

☁️ AWS EC2 Deployment — V4

V4 extends the CI/CD pipeline with automated deployment directly to AWS EC2.

The AWS deployment runs after changes reach the main branch and the earlier CI validation stages succeed.

V4 Deployment Flow

GitHub Push
     │
     ▼
GitHub Actions
     │
     ▼
Run Tests
     │
     ▼
Build Docker Image
     │
     ▼
Docker Smoke Test
     │
     ▼
Trivy Security Scan
     │
     ▼
Kubernetes Validation
     │
     ▼
Docker Hub
     │
     ▼
AWS EC2
     │
     ▼
Pull Git SHA Image
     │
     ▼
Stop Previous Application
     │
     ▼
Start New Container
     │
     ▼
/health Check
     │
     ▼
SUCCESS

AWS Runtime

AWS EC2
   │
   ▼
Docker
   │
   ▼
multicloud-app
   │
   ▼
Flask Application
   │
   ▼
/health

Runtime Configuration

CLOUD_PROVIDER=aws
CLOUD_REGION=ap-south-1
Application Port=5000

🔐 Immutable Git SHA Deployment

The AWS deployment does not rely only on the mutable latest tag.

Instead, the deployment uses the exact Git commit SHA.

Example:

josesamuel14/multicloud-app:fedae7b99f755f833196e396a214e32248a8dd91

Benefits

🔎 Traceability — connects the running container to a specific source commit.

🔐 Immutable Reference — identifies an exact image rather than a moving tag.

🔄 Easier Rollback — the previous image reference can be reused.

🧪 Better Debugging — deployment issues can be traced to a specific revision.

📌 Reproducibility — the same image reference can be deployed again.

The EC2 runtime was successfully verified using an image tagged with the exact Git commit SHA.

❤️ Deployment Verification

A deployment is considered successful only after the EC2 application responds successfully to:

GET /health

Example response:

{
  "cloud": "aws",
  "region": "ap-south-1",
  "status": "healthy"
}

The /health endpoint is used as the final runtime verification step.

🔄 Deployment Rollback

The EC2 deployment script records the previously running Docker image before replacing the application container.

Normal Deployment

New Image
    │
    ▼
Pull Image
    │
    ▼
Stop Previous Container
    │
    ▼
Start New Container
    │
    ▼
/health
    │
    ▼
Healthy
    │
    ▼
✅ Deployment Successful

Failure Path

New Image
    │
    ▼
Start New Container
    │
    ▼
/health
    │
    ▼
❌ Failure
    │
    ▼
Remove Failed Container
    │
    ▼
Start Previous Image
    │
    ▼
Rollback Health Check
    │
    ▼
Previous Version Restored

The rollback mechanism is implemented in the deployment workflow.

Validation note: A deliberate failure-path test is planned as a future validation step.

🐳 Docker Configuration

The Flask application is packaged using:

app/Dockerfile

Container Security

Base image: python:3.11-slim

Non-root runtime user: UID 10001

Build Locally

docker build -t multicloud-app:v4 ./app

Run Locally

docker run -d \
  --name multicloud-app \
  -p 5000:5000 \
  multicloud-app:v4

Verify Runtime

curl http://localhost:5000/health

🔒 Trivy Security Scanning

The CI pipeline uses Trivy to scan the Docker image.

The pipeline checks:

HIGH severity vulnerabilities

CRITICAL severity vulnerabilities

Unfixed vulnerabilities are ignored so that vulnerabilities without an available fix do not unnecessarily block the pipeline.

The embedded pip SBOM file is excluded to avoid duplicate or stale dependency metadata findings.

The installed Python packages remain subject to vulnerability scanning.

☸️ Kubernetes Validation

The project uses Kubernetes for deployment validation through Kind (Kubernetes in Docker).

Configuration Files

deployment.yaml
service.yaml
kind-config.yaml

Current Deployment

The Kubernetes deployment includes:

2 replicas

Readiness probe

Liveness probe

CPU requests

CPU limits

Memory requests

Memory limits

Non-root execution

runAsUser: 10001

Dropped Linux capabilities

Disabled privilege escalation

Apply Manifests

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

Check Resources

kubectl get pods
kubectl get deployment
kubectl get service

Check Rollout

kubectl rollout status deployment/multicloud-app

❤️ Kubernetes Health Probes

The application provides:

/health

Kubernetes uses this endpoint for both readiness and liveness checks.

Readiness Probe

readinessProbe:
  httpGet:
    path: /health
    port: 5000

The readiness probe determines whether the application is ready to receive traffic.

Liveness Probe

livenessProbe:
  httpGet:
    path: /health
    port: 5000

The liveness probe determines whether the application is still running correctly.

🔄 Kubernetes Self-Healing

The deployment was tested for pod failure and recovery.

2 replicas running
       │
       ▼
Delete one application pod
       │
       ▼
Kubernetes detects missing replica
       │
       ▼
Replacement pod created
       │
       ▼
Deployment returns to 2/2

Expected State

Deployment: 2/2 available
Pods:       2/2 Running

This demonstrates Kubernetes controller-based self-healing.

📊 Monitoring & Observability

The local monitoring stack contains:

                    ┌───────────────┐
                    │   Flask App   │
                    │   /metrics    │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Prometheus   │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │    Grafana    │
                    └───────────────┘


                    ┌───────────────┐
                    │ Node Exporter │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Prometheus   │
                    └───────────────┘

Services

Service

Port

Purpose

Flask App

5000

Application and health endpoints

Prometheus

9090

Metrics collection and queries

Grafana

3000

Monitoring dashboards

Node Exporter

9100

Host/system metrics

Prometheus scrapes metrics every 15 seconds.

📡 Prometheus

Prometheus monitors application and infrastructure metrics.

Expected Targets

multicloud-app
prometheus
node-exporter

Prometheus Targets

Open:

http://localhost:9090/targets

Expected state:

UP

Prometheus Health

Open:

http://localhost:9090/-/healthy

📈 Grafana

Grafana is used for observability and visualization.

Grafana credentials are provided through .env.

Create .env

GRAFANA_ADMIN_PASSWORD=your-secure-password

⚠️ Security: Never commit .env or real credentials to GitHub.

Start Monitoring

docker compose --env-file .env -f monitoring/docker-compose.yml up -d

Check Monitoring Containers

docker compose --env-file .env -f monitoring/docker-compose.yml ps

🏗️ Terraform / AWS Infrastructure

Terraform configuration:

terraform/aws-ec2.tf

The configuration demonstrates:

AWS provider

EC2

Security Group

Elastic IP resource configuration

Docker installation

EC2 user data

Application startup

Terraform variables

Terraform outputs

Important: The Terraform configuration demonstrates Elastic IP resource configuration, but the currently used EC2 instance does not have a permanent Elastic IP. Its public IP can therefore change after stop/start.

Default AWS Region

ap-south-1

SSH CIDR Variable

variable "ssh_cidr" {
  description = "CIDR block allowed to access SSH"
  type        = string
}

Infrastructure Safety

Do not run:

terraform apply

unless the AWS resources, Terraform state, instance configuration, and potential cloud usage are understood.

AWS free-tier and credit eligibility depends on the account, region, resource usage, and current AWS pricing rules.

🧪 Automated Testing

Test file:

tests/test_app.py

The test verifies:

GET /health
      │
      ▼
HTTP 200

Install Development Dependencies

pip install -r requirements-dev.txt

Run Tests

python -m pytest tests/test_app.py

Expected:

1 passed

🐳 Docker Image Publishing

Docker images are published to Docker Hub when changes reach main.

Docker Hub Repository

📦 josesamuel14/multicloud-app

Generated Tags

latest

and:

<Git commit SHA>

Example:

josesamuel14/multicloud-app:fedae7b99f755f833196e396a214e32248a8dd91

Development branches validate the image without publishing it.

❤️ Health Endpoint

The application provides:

GET /health

Example local response:

{
  "cloud": "local",
  "status": "healthy"
}

The endpoint is used for:

Docker smoke testing

Kubernetes readiness

Kubernetes liveness

Manual validation

AWS EC2 deployment verification

📡 API Endpoints

Endpoint

Method

Description

/

GET

Application dashboard

/health

GET

Application health

/stats

GET

Application statistics

/metrics

GET

Prometheus metrics

/deploy

POST

Deployment-related API

📁 Project Structure

multicloud-cicd/
│
├── .github/
│   └── workflows/
│       └── deploy.yml
│
├── app/
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
│
├── tests/
│   └── test_app.py
│
├── monitoring/
│   ├── docker-compose.yml
│   └── prometheus.yml
│
├── terraform/
│   └── aws-ec2.tf
│
├── scripts/
│   ├── deploy-aws.sh
│   └── protect-aws.sh
│
├── deployment.yaml
├── service.yaml
├── kind-config.yaml
├── requirements-dev.txt
├── .gitignore
├── LICENSE
└── README.md

🚀 Quick Start Guide

1️⃣ Clone Repository

git clone https://github.com/JOSESAMUEL14/multicloud-cicd.git
cd multicloud-cicd

2️⃣ Create Environment File

Create:

.env

Add:

GRAFANA_ADMIN_PASSWORD=your-secure-password

3️⃣ Start Application + Monitoring

docker compose --env-file .env -f monitoring/docker-compose.yml up -d

4️⃣ Verify Containers

docker compose --env-file .env -f monitoring/docker-compose.yml ps

5️⃣ Verify Application

curl http://localhost:5000/health

6️⃣ Open Services

Service

URL

🌍 Application

http://localhost:5000

📡 Prometheus

http://localhost:9090

📈 Grafana

http://localhost:3000

🔧 Troubleshooting

Check Application

curl http://localhost:5000/health

Check Docker

docker ps

Check Monitoring

docker compose --env-file .env -f monitoring/docker-compose.yml ps

Check Prometheus

Open:

http://localhost:9090/targets

Check Kubernetes

kubectl get pods
kubectl get deployment
kubectl get service

Check Kubernetes Logs

kubectl logs -l app=multicloud-app

Check Rollout

kubectl rollout status deployment/multicloud-app

Check Git

git status
git branch

🔒 Branch & Version Safety

The project uses separate branches to protect stable versions.

main
 │
 ├── v1-stable
 │     └── Original V1 preserved
 │
 ├── devops-v3
 │     └── V3 development preserved
 │
 └── v4-aws-ec2-deployment
       └── V4 AWS deployment development

Version History

Version

Branch

Purpose

V1

v1-stable

Original working implementation

V3

devops-v3

Advanced portfolio UI and CI/CD improvements

V4

main

AWS EC2 automated deployment after merge

Experimental changes should not be made directly on main.

No secrets should ever be committed to the repository.

🧪 CI Reliability Validation

The pipeline validates multiple layers:

Application Tests
       │
       ▼
Docker Build
       │
       ▼
Docker Runtime
       │
       ▼
Health Endpoint
       │
       ▼
Trivy Security Scan
       │
       ▼
Kubernetes Cluster
       │
       ▼
Kubernetes Deployment
       │
       ▼
2/2 Ready Replicas
       │
       ▼
Application Health
       │
       ▼
Docker Hub Image
       │
       ▼
AWS EC2 Deployment
       │
       ▼
EC2 Health Check

This creates multiple validation layers before the application is considered successfully deployed.

🧠 Engineering Concepts Demonstrated

CI/CD

Automated testing

Build automation

Pipeline dependencies

Docker image publishing

CI failure handling

AWS deployment automation

Deployment verification

Docker

Containerization

Immutable image tagging

Non-root containers

Runtime health validation

Vulnerability scanning

Docker Hub publishing

Kubernetes

Deployments

ReplicaSets

Pods

Services

NodePort

Readiness probes

Liveness probes

Resource requests and limits

Security contexts

Self-healing

AWS

EC2 deployment

Docker runtime

SSH-based deployment

Git SHA image deployment

Health verification

Deployment rollback

Terraform

Infrastructure as Code

AWS provider

EC2

Security groups

Variables

Outputs

User data

Observability

Prometheus

Grafana

Node Exporter

Application metrics

Health endpoints

Prometheus target monitoring

DevOps Engineering

Git branching

Failure testing

Troubleshooting

Security hardening

Automated validation

Infrastructure automation

Immutable deployments

Deployment verification

Documentation

🎯 Project Objective

The objective of this project is to demonstrate how a software application can move through a practical DevOps lifecycle:

┌───────────────┐
│     CODE      │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│     TEST      │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│     BUILD     │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│  CONTAINERIZE │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│     SCAN      │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   VALIDATE    │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│    PUBLISH    │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│    DEPLOY     │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│    VERIFY     │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│   MONITOR     │
└───────┬───────┘
        │
        ▼
┌───────────────┐
│    RECOVER    │
└───────────────┘

The project emphasizes practical DevOps engineering rather than simply collecting a large number of technologies.

🏆 Key Project Highlights

🔹 Automated CI/CD

GitHub Actions automatically validates the application and, on main, publishes the container image and deploys the application to AWS EC2.

🔹 Containerized Application

The Flask application is packaged and executed using Docker.

🔹 Kubernetes Validation

The deployment is validated using Kind with two replicas and health probes.

🔹 Security Scanning

Docker images are scanned using Trivy for HIGH and CRITICAL vulnerabilities.

🔹 Immutable Deployment

AWS deployment uses the exact Git commit SHA rather than relying only on latest.

🔹 AWS EC2 Deployment

The application has been successfully deployed to AWS EC2 through the CI/CD pipeline.

🔹 Health Verification

Deployment completion is verified using the application's /health endpoint.

🔹 Monitoring

Prometheus, Grafana, and Node Exporter provide local observability.

🔗 Direct Repository Links

Resource

Direct Link

🌍 Live Render Application

Open Application

⚙️ GitHub Actions

View Actions

💻 GitHub Repository

Open Repository

🐳 Docker Hub

Open Docker Image

📄 CI/CD Workflow

deploy.yml

☸️ Kubernetes Deployment

deployment.yaml

☸️ Kubernetes Service

service.yaml

🏗️ Terraform AWS Config

aws-ec2.tf

🧪 Automated Tests

test_app.py

📊 Monitoring Configuration

monitoring/

📁 Repository Files

Browse Repository

📘 Documentation

README

👨‍💻 Author

Samuel D

B.E. Computer Science and Engineering

Connect

💻 GitHub: @JOSESAMUEL14

💼 LinkedIn: linkedin.com/in/samueld14

📧 Email: Josesamueld2005@gmail.com

📜 License

Distributed under the MIT License.
