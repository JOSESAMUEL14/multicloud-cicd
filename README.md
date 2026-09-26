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

<table>
  <tr>
    <td width="50%">
      <h3>🌍 Live Application</h3>
      <strong>Render Demo</strong><br><br>
      <a href="https://multicloud-cicd.onrender.com">🚀 Open Live Application</a>
    </td>
    <td width="50%">
      <h3>⚙️ CI/CD Pipeline</h3>
      <strong>GitHub Actions</strong><br><br>
      <a href="https://github.com/JOSESAMUEL14/multicloud-cicd/actions">🔄 View Pipeline Runs</a>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>💻 Source Code</h3>
      <strong>GitHub Repository</strong><br><br>
      <a href="https://github.com/JOSESAMUEL14/multicloud-cicd">📂 View Repository</a>
    </td>
    <td width="50%">
      <h3>🐳 Container Registry</h3>
      <strong>Docker Hub</strong><br><br>
      <a href="https://hub.docker.com/r/josesamuel14/multicloud-app">📦 View Docker Image</a>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>☁️ AWS EC2 Demo</h3>
      <strong>Current EC2 Deployment</strong><br><br>
      <a href="http://13.201.186.250:5000">🚀 Open AWS EC2 Application</a>
      <br><br>
      <sub>Live-demo instance. Public IP may change after stop/start.</sub>
    </td>
    <td width="50%">
      <h3>📖 Project Documentation</h3>
      <strong>GitHub README</strong><br><br>
      <a href="https://github.com/JOSESAMUEL14/multicloud-cicd#readme">📘 View Documentation</a>
    </td>
  </tr>
</table>

⚠️ AWS demo note: The current EC2 public IP is 13.201.186.250. The instance is not kept running continuously, and AWS can assign a different public IP after a stop/start cycle. Therefore, the AWS URL is intended for live demonstrations rather than as a permanent endpoint.

🎯 Project Overview

Multi-Cloud CI/CD Pipeline is a Flask-based DevOps project that demonstrates a practical software delivery lifecycle from source code to containerized deployment and runtime verification.

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

The goal is to demonstrate how these technologies work together as one automated DevOps workflow rather than simply listing tools.

☁️ AWS EC2 Deployment

The application has been successfully deployed to AWS EC2 through the automated CI/CD pipeline.

The EC2 instance is started only when a live demonstration is required to avoid unnecessary continuous cloud usage.

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
Port 5000
   │
   ▼
/health

Runtime Configuration

CLOUD_PROVIDER=aws
CLOUD_REGION=ap-south-1
Application Port=5000

Live Demonstration Contact

💼 LinkedIn: linkedin.com/in/samueld14

💻 GitHub: github.com/JOSESAMUEL14

📧 Email: Josesamueld2005@gmail.com

🧭 DevOps Workflow

                         👨‍💻 Developer
                              │
                              ▼
                    💻 GitHub Repository
                              │
                              ▼
                     ⚙️ GitHub Actions
                              │
               ┌──────────────┼──────────────┐
               │              │              │
               ▼              ▼              ▼
          🧪 Pytest      🐳 Docker Build  🔒 Trivy
               │              │              │
               └──────────────┼──────────────┘
                              │
                              ▼
                    ☸️ Kind Kubernetes
                       Validation
                              │
                              ▼
                         📦 Docker Hub
                              │
                              ▼
                           ☁️ AWS EC2
                              │
                              ▼
                       🐳 Docker Container
                              │
                              ▼
                           ❤️ /health
                              │
                              ▼
                     ✅ Deployment Verified

🏗️ Architecture

┌──────────────────────┐
│      Developer       │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│       GitHub         │
└──────────┬───────────┘
           │
           ▼
┌────────────────────────────┐
│      GitHub Actions        │
└─────────────┬──────────────┘
              │
      ┌───────┼────────┐
      │       │        │
      ▼       ▼        ▼
┌─────────┐ ┌────────┐ ┌─────────┐
│ Pytest  │ │ Docker │ │  Trivy  │
│  Tests  │ │ Build  │ │  Scan   │
└────┬────┘ └───┬────┘ └────┬────┘
     │          │           │
     └──────────┼───────────┘
                │
                ▼
      ┌────────────────────┐
      │  Kind Kubernetes   │
      │     Validation     │
      └─────────┬──────────┘
                │
                ▼
        ┌──────────────┐
        │  Docker Hub  │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │   AWS EC2    │
        │    Docker    │
        └──────┬───────┘
               │
               ▼
        ┌──────────────┐
        │  Flask App   │
        │   Port 5000  │
        └──────┬───────┘
               │
               ▼
            /health

🛠️ Technology Stack

<table>
  <thead>
    <tr>
      <th>Technology</th>
      <th>Category</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Python / Flask</td>
      <td>Application</td>
      <td>Web application and REST API</td>
    </tr>
    <tr>
      <td>Docker</td>
      <td>Containerization</td>
      <td>Application packaging and runtime</td>
    </tr>
    <tr>
      <td>GitHub Actions</td>
      <td>CI/CD</td>
      <td>Continuous integration and deployment automation</td>
    </tr>
    <tr>
      <td>Docker Hub</td>
      <td>Registry</td>
      <td>Container image storage and publishing</td>
    </tr>
    <tr>
      <td>Kubernetes / Kind</td>
      <td>Orchestration</td>
      <td>CI/CD deployment validation</td>
    </tr>
    <tr>
      <td>Terraform</td>
      <td>Infrastructure as Code</td>
      <td>AWS infrastructure configuration</td>
    </tr>
    <tr>
      <td>AWS EC2</td>
      <td>Cloud</td>
      <td>Cloud deployment target</td>
    </tr>
    <tr>
      <td>Prometheus</td>
      <td>Monitoring</td>
      <td>Time-series metric collection</td>
    </tr>
    <tr>
      <td>Grafana</td>
      <td>Observability</td>
      <td>Monitoring dashboards</td>
    </tr>
    <tr>
      <td>Node Exporter</td>
      <td>System Metrics</td>
      <td>Host and OS metrics</td>
    </tr>
    <tr>
      <td>Trivy</td>
      <td>Security</td>
      <td>Container vulnerability scanning</td>
    </tr>
    <tr>
      <td>Git / GitHub</td>
      <td>Version Control</td>
      <td>Source control and collaboration</td>
    </tr>
  </tbody>
</table>

🔄 Complete CI/CD Pipeline

The GitHub Actions workflow performs multiple validation and deployment stages before considering the deployment successful.

Pipeline Stages

01. Push to GitHub
        │
        ▼
02. Checkout source code
        │
        ▼
03. Setup Python 3.11
        │
        ▼
04. Install dependencies
        │
        ▼
05. Run Pytest
        │
        ▼
06. Build Docker image
        │
        ▼
07. Docker smoke test
        │
        ▼
08. Trivy vulnerability scan
        │
        ▼
09. Create Kind Kubernetes cluster
        │
        ▼
10. Load Docker image into Kind
        │
        ▼
11. Deploy Kubernetes manifests
        │
        ▼
12. Wait for rollout
        │
        ▼
13. Verify 2/2 replicas
        │
        ▼
14. Verify application health
        │
        ▼
15. Show Kubernetes diagnostics
        │
        ▼
16. Publish Docker image on main
        │
        ▼
17. SSH into AWS EC2
        │
        ▼
18. Pull exact Git SHA image
        │
        ▼
19. Replace existing container
        │
        ▼
20. Start new container
        │
        ▼
21. Verify /health endpoint
        │
        ▼
22. Deployment successful

Workflow File

.github/workflows/deploy.yml

☁️ AWS EC2 Deployment — V4

V4 extends the existing CI/CD pipeline with automated deployment directly to AWS EC2.

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

🔐 Immutable Git SHA Deployment

The AWS deployment does not rely only on the mutable latest tag.

Instead, it uses the exact Git commit SHA.

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

🐳 Docker

The Flask application is packaged using:

app/Dockerfile

Container Configuration

Base Image: Python 3.11 slim
Runtime User: UID 10001
Application Port: 5000

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

                    ┌─────────────────┐
                    │    Flask App    │
                    │    /metrics     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Prometheus    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Grafana     │
                    └─────────────────┘


                    ┌─────────────────┐
                    │  Node Exporter  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │   Prometheus    │
                    └─────────────────┘

Services

<table>
  <thead>
    <tr>
      <th>Service</th>
      <th>Port</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Flask App</td>
      <td>5000</td>
      <td>Application and health endpoints</td>
    </tr>
    <tr>
      <td>Prometheus</td>
      <td>9090</td>
      <td>Metrics collection and queries</td>
    </tr>
    <tr>
      <td>Grafana</td>
      <td>3000</td>
      <td>Monitoring dashboards</td>
    </tr>
    <tr>
      <td>Node Exporter</td>
      <td>9100</td>
      <td>Host and system metrics</td>
    </tr>
  </tbody>
</table>

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

Important: The Terraform configuration demonstrates Elastic IP resource configuration, but the currently used EC2 instance does not have a permanent Elastic IP. Its public IP can therefore change after a stop/start cycle.

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

<a href="https://hub.docker.com/r/josesamuel14/multicloud-app">📦 josesamuel14/multicloud-app</a>

Generated Tags

latest
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

<table>
  <thead>
    <tr>
      <th>Endpoint</th>
      <th>Method</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>/</code></td>
      <td><code>GET</code></td>
      <td>Application dashboard</td>
    </tr>
    <tr>
      <td><code>/health</code></td>
      <td><code>GET</code></td>
      <td>Application health</td>
    </tr>
    <tr>
      <td><code>/stats</code></td>
      <td><code>GET</code></td>
      <td>Application statistics</td>
    </tr>
    <tr>
      <td><code>/metrics</code></td>
      <td><code>GET</code></td>
      <td>Prometheus metrics</td>
    </tr>
    <tr>
      <td><code>/deploy</code></td>
      <td><code>POST</code></td>
      <td>Deployment-related API</td>
    </tr>
  </tbody>
</table>

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

<table>
  <tr>
    <td><strong>🌍 Application</strong></td>
    <td><a href="http://localhost:5000">http://localhost:5000</a></td>
  </tr>
  <tr>
    <td><strong>📡 Prometheus</strong></td>
    <td><a href="http://localhost:9090">http://localhost:9090</a></td>
  </tr>
  <tr>
    <td><strong>📈 Grafana</strong></td>
    <td><a href="http://localhost:3000">http://localhost:3000</a></td>
  </tr>
</table>

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

The project uses separate branches to protect stable versions and keep development work isolated.

Branch Structure

<table>
  <thead>
    <tr>
      <th>Branch</th>
      <th>Purpose</th>
      <th>Status</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>main</code></td>
      <td>Stable recruiter-facing project</td>
      <td>🟢 Stable</td>
    </tr>
    <tr>
      <td><code>v1-stable</code></td>
      <td>Original V1 implementation</td>
      <td>🔒 Preserved</td>
    </tr>
    <tr>
      <td><code>devops-v3</code></td>
      <td>V3 development and portfolio UI</td>
      <td>📦 Preserved</td>
    </tr>
    <tr>
      <td><code>v4-aws-ec2-deployment</code></td>
      <td>V4 AWS EC2 deployment development</td>
      <td>🛠️ Development</td>
    </tr>
  </tbody>
</table>

Version Flow

v1-stable
    │
    ▼
devops-v3
    │
    ▼
v4-aws-ec2-deployment
    │
    ▼
main

Version History

<table>
  <thead>
    <tr>
      <th>Version</th>
      <th>Branch</th>
      <th>Purpose</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>V1</strong></td>
      <td><code>v1-stable</code></td>
      <td>Original working implementation</td>
    </tr>
    <tr>
      <td><strong>V3</strong></td>
      <td><code>devops-v3</code></td>
      <td>Advanced portfolio UI and CI/CD improvements</td>
    </tr>
    <tr>
      <td><strong>V4</strong></td>
      <td><code>v4-aws-ec2-deployment</code> → <code>main</code></td>
      <td>AWS EC2 automated deployment after merge</td>
    </tr>
  </tbody>
</table>

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

The objective of this project is to demonstrate how a software application can move through a practical DevOps lifecycle.

DevOps Lifecycle

<table>
  <tr>
    <td align="center"><strong>01</strong><br>💻<br><strong>CODE</strong></td>
    <td align="center">→</td>
    <td align="center"><strong>02</strong><br>🧪<br><strong>TEST</strong></td>
    <td align="center">→</td>
    <td align="center"><strong>03</strong><br>🐳<br><strong>BUILD</strong></td>
    <td align="center">→</td>
    <td align="center"><strong>04</strong><br>📦<br><strong>CONTAINERIZE</strong></td>
  </tr>
  <tr>
    <td colspan="7" align="center">↓</td>
  </tr>
  <tr>
    <td align="center"><strong>08</strong><br>🔄<br><strong>RECOVER</strong></td>
    <td align="center">←</td>
    <td align="center"><strong>07</strong><br>📊<br><strong>MONITOR</strong></td>
    <td align="center">←</td>
    <td align="center"><strong>06</strong><br>🚀<br><strong>DEPLOY</strong></td>
    <td align="center">←</td>
    <td align="center"><strong>05</strong><br>🔒<br><strong>SCAN &amp; VALIDATE</strong></td>
  </tr>
</table>

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

<table>
  <thead>
    <tr>
      <th>Resource</th>
      <th>Link</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>🌍 Live Render Application</td>
      <td><a href="https://multicloud-cicd.onrender.com">Open Application</a></td>
    </tr>
    <tr>
      <td>⚙️ GitHub Actions</td>
      <td><a href="https://github.com/JOSESAMUEL14/multicloud-cicd/actions">View Actions</a></td>
    </tr>
    <tr>
      <td>💻 GitHub Repository</td>
      <td><a href="https://github.com/JOSESAMUEL14/multicloud-cicd">Open Repository</a></td>
    </tr>
    <tr>
      <td>🐳 Docker Hub</td>
      <td><a href="https://hub.docker.com/r/josesamuel14/multicloud-app">Open Docker Image</a></td>
    </tr>
    <tr>
      <td>📄 CI/CD Workflow</td>
      <td><a href="https://github.com/JOSESAMUEL14/multicloud-cicd/blob/main/.github/workflows/deploy.yml">deploy.yml</a></td>
    </tr>
    <tr>
      <td>☸️ Kubernetes Deployment</td>
      <td><a href="https://github.com/JOSESAMUEL14/multicloud-cicd/blob/main/deployment.yaml">deployment.yaml</a></td>
    </tr>
    <tr>
      <td>☸️ Kubernetes Service</td>
      <td><a href="https://github.com/JOSESAMUEL14/multicloud-cicd/blob/main/service.yaml">service.yaml</a></td>
    </tr>
    <tr>
      <td>🏗️ Terraform AWS Config</td>
      <td><a href="https://github.com/JOSESAMUEL14/multicloud-cicd/blob/main/terraform/aws-ec2.tf">aws-ec2.tf</a></td>
    </tr>
    <tr>
      <td>🧪 Automated Tests</td>
      <td><a href="https://github.com/JOSESAMUEL14/multicloud-cicd/blob/main/tests/test_app.py">test_app.py</a></td>
    </tr>
    <tr>
      <td>📊 Monitoring Configuration</td>
      <td><a href="https://github.com/JOSESAMUEL14/multicloud-cicd/tree/main/monitoring">monitoring/</a></td>
    </tr>
    <tr>
      <td>📁 Repository Files</td>
      <td><a href="https://github.com/JOSESAMUEL14/multicloud-cicd/tree/main">Browse Repository</a></td>
    </tr>
    <tr>
      <td>📘 Documentation</td>
      <td><a href="https://github.com/JOSESAMUEL14/multicloud-cicd#readme">README</a></td>
    </tr>
  </tbody>
</table>

👨‍💻 Author

<p>
  <strong>Samuel D</strong><br>
  B.E. Computer Science and Engineering
</p>

Connect

<table>
  <tr>
    <td>💻 <strong>GitHub</strong></td>
    <td><a href="https://github.com/JOSESAMUEL14">@JOSESAMUEL14</a></td>
  </tr>
  <tr>
    <td>💼 <strong>LinkedIn</strong></td>
    <td><a href="https://linkedin.com/in/samueld14">linkedin.com/in/samueld14</a></td>
  </tr>
  <tr>
    <td>📧 <strong>Email</strong></td>
    <td><a href="mailto:Josesamueld2005@gmail.com">Josesamueld2005@gmail.com</a></td>
  </tr>
</table>

📜 License

This project is distributed under the MIT License.

See the LICENSE file for details.
