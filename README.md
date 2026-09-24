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
    └── Build Docker image
            │
            └── main → Push image to Docker Hub

The application can also be run locally using Docker Compose and deployed to a local Kubernetes cluster using Kind.
AWS infrastructure is defined separately using Terraform.
🏗️ Architecture
                         GitHub
                           │
                           ▼
                    GitHub Actions
                           │
                    ┌──────┴──────┐
                    │             │
                 Tests        Docker Build
                    │             │
                    └──────┬──────┘
                           │
                    devops-v2 → Build only
                           │
                    main → Push Image
                           │
                           ▼
                     Docker Hub
                           │
                           ▼
                  Containerized Flask App
                           │
              ┌────────────┴────────────┐
              │                         │
              ▼                         ▼
        Local Docker               Kubernetes
              │                         │
              │                    2 replicas
              │                    Health probes
              │                    Security context
              │
              ▼
        Prometheus
              │
              ▼
           Grafana

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


🔄 CI/CD Pipeline
The GitHub Actions workflow runs for both main and devops-v2.
devops-v2
Push to devops-v2
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
Done

The V2 branch does not push experimental images to Docker Hub.
main
Push to main
       ↓
Checkout
       ↓
Python 3.11 setup
       ↓
Install dependencies
       ↓
Run pytest
       ↓
Docker login
       ↓
Build Docker image
       ↓
Push to Docker Hub
       ├── latest
       └── Git commit SHA

Using the Git SHA provides an immutable image reference in addition to the latest tag.
🧪 Automated Testing
The project includes a Flask health test:
tests/test_app.py

The test verifies:
GET /health
      ↓
HTTP 200

Run locally:
pip install -r app/requirements.txt
pytest tests/test_app.py

Expected result:
1 passed

🐳 Docker
The Flask application is packaged using:
app/Dockerfile

The container runs as a non-root user:
UID 10001

This reduces unnecessary container privileges.
Build locally:
docker build -t multicloud-app:v2 ./app

Run:
docker run -d \
  --name multicloud-app \
  -p 5000:5000 \
  multicloud-app:v2

Test:
curl http://localhost:5000/health

☸️ Kubernetes
The Kubernetes deployment is defined in:
deployment.yaml
service.yaml
kind-config.yaml

Current deployment configuration includes:
- 2 replicas
- Readiness probe
- Liveness probe
- CPU and memory requests/limits
- Non-root execution
- runAsUser: 10001
- Dropped Linux capabilities
- Disabled privilege escalation
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

☁️ Terraform / AWS
AWS infrastructure is defined in:
terraform/aws-ec2.tf

The configuration defines:
- AWS provider
- EC2 instance
- Security group
- Elastic IP
- Docker installation through EC2 user data
- Application container startup
- Terraform outputs
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
Check application
curl http://localhost:5000/health

Check monitoring containers
docker compose --env-file .env -f monitoring/docker-compose.yml ps

Check Prometheus targets
Open:
http://localhost:9090

Prometheus should report the application, Prometheus, and Node Exporter targets as healthy.
Check Kubernetes
kubectl get pods
kubectl get deployment
kubectl describe pod <pod-name>

Check Git state
git status
git branch

The stable main branch should not be used for experimental V2 changes.
🔒 V2 Development Safety
The project uses:
main
   │
   └── Stable recruiter-facing version

devops-v2
   │
   └── Development and improvements

V2 changes are developed and tested separately before any future merge into main.
No secrets should be committed to the repository.
👨‍💻 Author
Samuel D
GitHub:
https://github.com/JOSESAMUEL14
LinkedIn:
https://linkedin.com/in/samueld14
📜 License
MIT License

### After saving

Run these **only**:

```cmd
git diff --check