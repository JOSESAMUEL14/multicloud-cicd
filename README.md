# Multi-Cloud CI/CD Pipeline

[![CI/CD Pipeline](https://github.com/JOSESAMUEL14/multicloud-cicd/actions/workflows/deploy.yml/badge.svg)](https://github.com/JOSESAMUEL14/multicloud-cicd/actions/workflows/deploy.yml)

A Flask-based DevOps project demonstrating containerization, CI/CD, Kubernetes deployment, Terraform-based AWS infrastructure, and Prometheus/Grafana monitoring.


---

## 🚀 Project Overview

This project demonstrates a complete DevOps workflow around a Flask application:

```text
Developer
    │
    ▼
GitHub Repository
    │
    ▼
GitHub Actions
    │
    ├── Run Python tests
    │
    ├── Build Docker image
    │
    ├── Docker smoke test
    │
    ├── Trivy vulnerability scan
    │
    ├── Create local Kubernetes cluster
    │
    ├── Deploy application to Kubernetes
    │
    ├── Verify Kubernetes rollout
    │
    └── Verify application health
             │
             └── main → Push image to Docker Hub

The application can also be run locally using Docker Compose and deployed to a local Kubernetes cluster.

AWS infrastructure is defined separately using Terraform.

🏗️ Architecture
                         GitHub
                           │
                           ▼
                    GitHub Actions
                           │
             ┌─────────────┴─────────────┐
             │                           │
          Tests                     Docker Build
             │                           │
             └─────────────┬─────────────┘
                           │
                    Docker Smoke Test
                           │
                           ▼
                  Trivy Security Scan
                           │
                           ▼
                 Local Kubernetes
                    (Kind in CI)
                           │
                           ▼
                 Containerized Flask App
                           │
                 ┌─────────┴─────────┐
                 │                   │
                 ▼                   ▼
             2 replicas        Health Probes
                 │                   │
                 └─────────┬─────────┘
                           │
                           ▼
                       /metrics
                           │
                           ▼
                      Prometheus
                           │
                           ▼
                        Grafana

                    Node Exporter
                           │
                           ▼
                      Prometheus
🛠️ Tech Stack
Technology	Purpose
Python / Flask	Web application and REST API
Docker	Application containerization
GitHub Actions	CI/CD automation
Docker Hub	Container image registry
Kubernetes	Container orchestration
Kind	Local Kubernetes cluster
Terraform	AWS infrastructure as code
AWS EC2	Cloud deployment target
Prometheus	Metrics collection
Grafana	Monitoring dashboard
Node Exporter	System metrics
Trivy	Container vulnerability scanning
Git/GitHub	Version control
🔄 CI/CD Pipeline

The GitHub Actions workflow validates the application through automated testing, Docker build validation, security scanning, and Kubernetes deployment validation.

The workflow runs for:

main
devops-v2
devops-v3
Pipeline Flow
Push
  ↓
Checkout
  ↓
Python 3.11 setup
  ↓
Install dependencies
  ↓
Run pytest
  ↓
Build Docker image
  ↓
Docker smoke test
  ↓
Trivy vulnerability scan
  ↓
Create Kind Kubernetes cluster
  ↓
Load Docker image
  ↓
Deploy Kubernetes manifests
  ↓
Wait for rollout
  ↓
Verify 2/2 replicas
  ↓
Verify application health
  ↓
Show Kubernetes diagnostics
  ↓
Push Docker image on main

The workflow is defined in:

.github/workflows/deploy.yml
Docker Image Publishing

Docker images are pushed to Docker Hub only when changes reach main.

Two image tags are published:

latest
Git commit SHA

The Git commit SHA provides an immutable image reference in addition to the latest tag.

Development branches build and validate the image without publishing it to Docker Hub.

🧪 Automated Testing

The project includes a Flask health test:

tests/test_app.py

The test verifies:

GET /health
     ↓
HTTP 200

Run locally:

pip install -r requirements-dev.txt
python -m pytest tests/test_app.py

Expected result:

1 passed
🐳 Docker

The Flask application is packaged using:

app/Dockerfile

The container runs as a non-root user:

UID 10001

This reduces unnecessary container privileges.

The Docker image uses Python 3.11 slim and installs only the application dependencies.

Build locally:

docker build -t multicloud-app:v3 ./app

Run:

docker run -d \
  --name multicloud-app \
  -p 5000:5000 \
  multicloud-app:v3

Test:

curl http://localhost:5000/health
🔒 Docker Vulnerability Scanning

The CI pipeline uses Trivy to scan the Docker image.

The scan checks for:

HIGH
CRITICAL

severity vulnerabilities.

Unfixed vulnerabilities are ignored so that vulnerabilities without an available fix do not unnecessarily block the pipeline.

The pipeline also excludes the embedded pip SBOM file that can contain stale dependency metadata and cause duplicate vulnerability findings.

The installed Python packages are still scanned.

☸️ Kubernetes

The Kubernetes deployment is defined in:

deployment.yaml
service.yaml
kind-config.yaml

Current deployment configuration includes:

2 replicas
Readiness probe
Liveness probe
CPU and memory requests/limits
Non-root execution
runAsUser: 10001
Dropped Linux capabilities
Disabled privilege escalation

The application is exposed locally through a NodePort.

Apply:

kubectl apply -f deployment.yaml
kubectl apply -f service.yaml

Check:

kubectl get pods
kubectl get deployment
kubectl get service

Check rollout:

kubectl rollout status deployment/multicloud-app
Kubernetes Health Probes

The application provides:

/health

Kubernetes uses this endpoint for:

Readiness Probe

Determines whether the application is ready to receive traffic.

readinessProbe:
  httpGet:
    path: /health
    port: 5000
Liveness Probe

Determines whether the application is still running correctly.

livenessProbe:
  httpGet:
    path: /health
    port: 5000
Kubernetes Resource Management

Each application pod has resource requests and limits.

Example:

resources:
  requests:
    cpu: "100m"
    memory: "128Mi"

  limits:
    cpu: "500m"
    memory: "256Mi"
Kubernetes Reliability Validation

The Kubernetes deployment was tested for pod failure and recovery.

Validation performed:

Deployment configured with 2 replicas
A running application pod was manually deleted
Kubernetes automatically created a replacement pod
Deployment returned to 2/2 ready replicas
Readiness and liveness probes continued to use /health

This validates Kubernetes self-healing behavior for the application deployment.

Example recovery check:

kubectl get pods
kubectl get deployment multicloud-app

Expected state after recovery:

Deployment: 2/2 available
Pods:       2/2 Running
☁️ Terraform / AWS

AWS infrastructure is defined in:

terraform/aws-ec2.tf

The configuration defines:

AWS provider
EC2 instance
Security group
Elastic IP
Docker installation through EC2 user data
Application container startup
Terraform outputs

The default AWS region is:

ap-south-1

The SSH CIDR is provided as an input variable:

variable "ssh_cidr" {
  description = "CIDR block allowed to access SSH"
  type        = string
}

This avoids permanently hardcoding an SSH source range in the Terraform configuration.

Important

The Terraform configuration is provided for infrastructure-as-code demonstration.

Do not run:

terraform apply

unless you understand the AWS resources and possible charges.

AWS free-tier eligibility depends on the AWS account, region, resource usage, and current AWS pricing rules.

📊 Monitoring

The local monitoring stack contains:

Flask App
    │
    │ /metrics
    ▼
Prometheus
    │
    ▼
Grafana

Node Exporter
    │
    ▼
Prometheus

Services:

Service	Port
Flask App	5000
Prometheus	9090
Grafana	3000
Node Exporter	9100

Prometheus scrapes metrics every 15 seconds.

The monitoring images are pinned to specific versions for reproducibility.

Prometheus Target Validation

Prometheus targets can be checked at:

http://localhost:9090/targets

Expected targets:

multicloud-app
prometheus
node-exporter

A healthy monitoring stack should report these targets as:

UP

Prometheus health can also be checked at:

http://localhost:9090/-/healthy
🔐 Grafana Credentials

Grafana credentials are provided through .env.

Create:

.env

Example:

GRAFANA_ADMIN_PASSWORD=your-secure-password

The .env file is ignored by Git and must not be committed.

Start monitoring:

docker compose --env-file .env -f monitoring/docker-compose.yml up -d

Check:

docker compose --env-file .env -f monitoring/docker-compose.yml ps

All services should eventually show:

healthy
🚀 Quick Start

Clone the repository:

git clone https://github.com/JOSESAMUEL14/multicloud-cicd.git
cd multicloud-cicd

Create the local environment file:

.env

Add:

GRAFANA_ADMIN_PASSWORD=your-secure-password

Start the application and monitoring stack:

docker compose --env-file .env -f monitoring/docker-compose.yml up -d

Open:

Application:

http://localhost:5000

Prometheus:

http://localhost:9090

Grafana:

http://localhost:3000
❤️ Health Check

The application provides:

GET /health

Example:

{
  "cloud": "local",
  "status": "healthy"
}

The /health endpoint is used by:

Docker smoke testing
Kubernetes readiness probes
Kubernetes liveness probes
Manual application validation
📡 API Endpoints
Endpoint	Method	Description
/	GET	Application dashboard
/health	GET	Application health status
/stats	GET	Application statistics
/metrics	GET	Prometheus metrics
/deploy	POST	Deployment-related API endpoint
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
├── requirements-dev.txt
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
├── .gitignore
├── LICENSE
└── README.md
🔧 Troubleshooting
Check Application
curl http://localhost:5000/health
Check Monitoring Containers
docker compose --env-file .env -f monitoring/docker-compose.yml ps
Check Prometheus Targets

Open:

http://localhost:9090/targets

Prometheus should report:

multicloud-app
prometheus
node-exporter

as healthy and UP.

Check Kubernetes
kubectl get pods
kubectl get deployment
kubectl get service

Describe a pod:

kubectl describe pod <pod-name>

View logs:

kubectl logs -l app=multicloud-app
Check Kubernetes Rollout
kubectl rollout status deployment/multicloud-app
Check Git State
git status
git branch

The stable main branch should not be used for experimental development.

🔒 Development Branch Safety

The project uses separate branches for stability and development:

main
  │
  └── Stable merged version

v1-stable
  │
  └── Original V1 preserved

devops-v3
  │
  └── Current V3 development

The original V1 implementation is preserved in:

v1-stable

The current V3 work is developed on:

devops-v3

Experimental changes are not made directly on main.

No secrets should be committed to the repository.

🧪 CI Reliability Validation

The CI pipeline validates more than simply whether the application can build.

It verifies:

Application Tests
       ↓
Docker Build
       ↓
Docker Runtime
       ↓
Health Endpoint
       ↓
Security Scan
       ↓
Kubernetes Cluster
       ↓
Kubernetes Deployment
       ↓
2/2 Ready Replicas
       ↓
Application Health

This provides multiple validation layers before the Docker image is published.

📚 Engineering Concepts Demonstrated
CI/CD
Automated testing
Build automation
Pipeline dependencies
Docker image publishing
CI failure handling
Docker
Containerization
Immutable image tagging
Non-root containers
Runtime health validation
Vulnerability scanning
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
Terraform
Infrastructure as Code
AWS provider
EC2
Security groups
Elastic IP
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
Documentation
🎯 Project Objective

The objective of this project is to demonstrate how a software application can move through a DevOps workflow:

Code
 ↓
Test
 ↓
Build
 ↓
Containerize
 ↓
Scan
 ↓
Deploy
 ↓
Validate
 ↓
Monitor
 ↓
Recover

The project emphasizes practical engineering concepts rather than simply collecting a large number of tools.

👨‍💻 Author

Samuel D

B.E. Computer Science and Engineering

GitHub:

https://github.com/JOSESAMUEL14

LinkedIn:

https://linkedin.com/in/samueld14

## 📜 License

MIT License
