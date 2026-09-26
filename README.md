# 🚀 Multi-Cloud CI/CD Pipeline

<p align="center">

  <b>A production-style DevOps project for automated testing, containerization, security scanning, Kubernetes validation, cloud deployment, and monitoring.</b>

</p>

<p align="center">

  <a href="https://github.com/JOSESAMUEL14/multicloud-cicd/actions">

    <img src="https://github.com/JOSESAMUEL14/multicloud-cicd/actions/workflows/deploy.yml/badge.svg" alt="CI/CD Pipeline">

  </a>

  <img src="https://img.shields.io/badge/Python-3.11-blue?logo=python" alt="Python">

  <img src="https://img.shields.io/badge/Docker-Containerized-blue?logo=docker" alt="Docker">

  <img src="https://img.shields.io/badge/Kubernetes-Kind-blue?logo=kubernetes" alt="Kubernetes">

  <img src="https://img.shields.io/badge/AWS-EC2-orange?logo=amazonaws" alt="AWS">

  <img src="https://img.shields.io/badge/Terraform-IaC-purple?logo=terraform" alt="Terraform">

  <img src="https://img.shields.io/badge/Trivy-Security-red" alt="Trivy">

  <img src="https://img.shields.io/badge/Prometheus-Monitoring-orange?logo=prometheus" alt="Prometheus">

  <img src="https://img.shields.io/badge/Grafana-Observability-orange?logo=grafana" alt="Grafana">

</p>

---

## 🌐 Project Links

<table>

<tr>

<td width="50%">

### 🌍 Live Application

**Render Demo**

[🚀 Open Live Application](https://multicloud-cicd.onrender.com)

</td>

<td width="50%">

### ⚙️ CI/CD Pipeline

**GitHub Actions**

[🔄 View Pipeline Runs](https://github.com/JOSESAMUEL14/multicloud-cicd/actions)

</td>

</tr>

<tr>

<td>

### 💻 Source Code

**GitHub Repository**

[📂 View Repository](https://github.com/JOSESAMUEL14/multicloud-cicd)

</td>

<td>

### 🐳 Container Registry

**Docker Hub**

[📦 View Docker Image](https://hub.docker.com/r/josesamuel14/multicloud-app)

</td>

</tr>

</table>

---

## ☁️ AWS EC2 Deployment

The application has also been successfully deployed to **AWS EC2 through the automated CI/CD pipeline**.

The AWS EC2 instance is not kept running continuously to avoid unnecessary cloud usage.

> 💡 **Want to see the real AWS deployment?**

>

> The AWS EC2 deployment and complete CI/CD workflow can be demonstrated on request.

>

> If you would like to see the **real AWS EC2 deployment, GitHub Actions pipeline, Docker image deployment, and health verification**, feel free to contact me:

>

> 💼 **LinkedIn:**  

> https://linkedin.com/in/samueld14

>

> 💻 **GitHub:**  

> https://github.com/JOSESAMUEL14

>

> 📧 **Email:**  

> Josesamueld2005@gmail.com

>

> I can provide a live demonstration of the AWS deployment and CI/CD workflow when required.

---

# 🎯 Project Overview

**Multi-Cloud CI/CD Pipeline** is a Flask-based DevOps project designed to demonstrate how a software application can move through a practical CI/CD lifecycle.

The project combines:

- 🧪 Automated testing

- 🐳 Docker containerization

- 🔒 Trivy vulnerability scanning

- ☸️ Kubernetes validation

- 📦 Docker Hub image publishing

- ☁️ AWS EC2 deployment

- 🔐 Immutable Git SHA image deployment

- ❤️ Automated health verification

- 🔄 Deployment rollback logic

- 📊 Prometheus monitoring

- 📈 Grafana dashboards

- 🏗️ Terraform infrastructure as code

- 🔀 Git/GitHub version control

The goal is not to collect tools, but to demonstrate how the tools work together in an actual DevOps workflow.

---

# 🧭 DevOps Workflow

```text

                         👨‍💻 Developer

                              │

                              ▼

                       💻 GitHub Repository

                              │

                              ▼

                       ⚙️ GitHub Actions

                              │

             ┌────────────────┼─────────────────┐

             │                │                 │

             ▼                ▼                 ▼

          🧪 Tests       🐳 Docker Build    🔒 Trivy Scan

             │                │                 │

             └────────────────┼─────────────────┘

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

                              ┌──────────────────┐

                              │     Developer    │

                              └────────┬─────────┘

                                       │

                                       ▼

                              ┌──────────────────┐

                              │      GitHub      │

                              └────────┬─────────┘

                                       │

                                       ▼

                           ┌───────────────────────┐

                           │    GitHub Actions     │

                           └───────────┬───────────┘

                                       │

              ┌────────────────────────┼────────────────────────┐

              │                        │                        │

              ▼                        ▼                        ▼

       ┌─────────────┐        ┌─────────────┐        ┌─────────────┐

       │    Pytest   │        │    Docker   │        │    Trivy    │

       │    Tests    │        │    Build    │        │    Scan     │

       └──────┬──────┘        └──────┬──────┘        └──────┬──────┘

              │                      │                      │

              └──────────────────────┼──────────────────────┘

                                     │

                                     ▼

                           ┌────────────────────┐

                           │  Kind Kubernetes    │

                           │     Validation      │

                           └─────────┬──────────┘

                                     │

                                     ▼

                              ┌───────────────┐

                              │   Docker Hub  │

                              └───────┬───────┘

                                      │

                                      ▼

                              ┌───────────────┐

                              │    AWS EC2    │

                              │    Docker     │

                              └───────┬───────┘

                                      │

                                      ▼

                              ┌───────────────┐

                              │ Flask App     │

                              │ Port 5000     │

                              └───────┬───────┘

                                      │

                                      ▼

                                  /health

🔄 Complete CI/CD Pipeline

The GitHub Actions workflow performs multiple validation stages before deploying to AWS.

1. Push to GitHub

       ↓

2. Checkout source code

       ↓

3. Setup Python 3.11

       ↓

4. Install dependencies

       ↓

5. Run pytest

       ↓

6. Build Docker image

       ↓

7. Docker smoke test

       ↓

8. Trivy vulnerability scan

       ↓

9. Create Kind Kubernetes cluster

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

15. Publish Docker image on main

       ↓

16. SSH into AWS EC2

       ↓

17. Pull exact Git SHA image

       ↓

18. Replace old container

       ↓

19. Start new container

       ↓

20. Verify /health

       ↓

21. Deployment successful

Workflow file:

.github/workflows/deploy.yml

☁️ AWS EC2 Deployment — V4

V4 extends the CI/CD pipeline by adding automated deployment to AWS EC2.

The deployment runs when changes reach the main branch.

V4 Flow

                 GitHub Push

                      │

                      ▼

               GitHub Actions

                      │

                      ▼

                 Run Tests

                      │

                      ▼

                Build Docker

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

             Stop Previous App

                      │

                      ▼

             Start New Container

                      │

                      ▼

                /health Check

                      │

                      ▼

                  SUCCESS

🔐 Immutable Deployment

Instead of relying only on:

latest

the AWS deployment uses the exact Git commit SHA.

Example:

josesamuel14/multicloud-app:fedae7b99f755f833196e396a214e32248a8dd91

This provides:

🔎 Traceability

🔐 Immutable deployment references

🔄 Easier rollback

🧪 Better debugging

📌 Direct connection between source code and deployed container

The deployed EC2 container was successfully verified using the exact Git commit image.

🚀 AWS EC2 Runtime

The application runs inside Docker on AWS EC2.

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

Environment configuration:

CLOUD_PROVIDER=aws

CLOUD_REGION=ap-south-1

Application port:

5000

❤️ Deployment Verification

A deployment is considered successful only after the EC2 application responds successfully to:

GET /health

Example:

{

  "cloud": "aws",

  "region": "ap-south-1",

  "status": "healthy"

}

The V4 deployment was successfully verified on the AWS EC2 instance after GitHub Actions completed.

🔄 Deployment Rollback

The deployment script stores the previously running Docker image.

Normal deployment:

New Image

    │

    ▼

Container Starts

    │

    ▼

/health

    │

    ▼

Healthy

    │

    ▼

✅ Deployment Successful

Failure path:

New Image

    │

    ▼

Container Starts

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

This provides a basic recovery mechanism for failed deployments.

Note: The rollback logic is implemented in the deployment workflow. A deliberate failure-path test is planned as a future validation step.

🐳 Docker

The Flask application is packaged using:

app/Dockerfile

The container runs as a non-root user:

UID 10001

The image uses Python 3.11 slim.

Build locally:

docker build -t multicloud-app:v4 ./app

Run:

docker run -d \

  --name multicloud-app \

  -p 5000:5000 \

  multicloud-app:v4

Test:

curl http://localhost:5000/health

🔒 Trivy Security Scanning

The CI pipeline uses Trivy to scan the Docker image.

The pipeline checks:

HIGH

CRITICAL

severity vulnerabilities.

Unfixed vulnerabilities are ignored so that vulnerabilities without an available fix do not unnecessarily block the pipeline.

The embedded pip SBOM file is excluded to avoid duplicate/stale dependency metadata findings.

The installed Python packages remain subject to scanning.

☸️ Kubernetes

The project uses Kubernetes for deployment validation.

Configuration files:

deployment.yaml

service.yaml

kind-config.yaml

Current deployment includes:

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

Apply:

kubectl apply -f deployment.yaml

kubectl apply -f service.yaml

Check:

kubectl get pods

kubectl get deployment

kubectl get service

Rollout:

kubectl rollout status deployment/multicloud-app

❤️ Kubernetes Health Probes

The application provides:

/health

Readiness probe:

readinessProbe:

  httpGet:

    path: /health

    port: 5000

Liveness probe:

livenessProbe:

  httpGet:

    path: /health

    port: 5000

Readiness

Determines whether the application is ready to receive traffic.

Liveness

Determines whether the application is still running correctly.

🔄 Kubernetes Self-Healing

The deployment was tested for pod failure and recovery.

Validation:

2 replicas running

      ↓

Delete one application pod

      ↓

Kubernetes detects missing replica

      ↓

Replacement pod created

      ↓

Deployment returns to 2/2

Expected state:

Deployment: 2/2 available

Pods:       2/2 Running

📊 Monitoring & Observability

The local monitoring stack contains:

                    Flask App

                        │

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

Services

Service Port

Flask App 5000

Prometheus  9090

Grafana 3000

Node Exporter 9100

Prometheus scrapes metrics every 15 seconds.

📡 Prometheus

Targets:

multicloud-app

prometheus

node-exporter

Open:

http://localhost:9090/targets

Expected state:

UP

Prometheus health:

http://localhost:9090/-/healthy

📈 Grafana

Grafana credentials are provided through .env.

Create:

.env

Example:

GRAFANA_ADMIN_PASSWORD=your-secure-password

⚠️ Never commit .env or real credentials to GitHub.

Start monitoring:

docker compose --env-file .env -f monitoring/docker-compose.yml up -d

Check:

docker compose --env-file .env -f monitoring/docker-compose.yml ps

🏗️ Terraform / AWS Infrastructure

Terraform configuration:

terraform/aws-ec2.tf

The configuration demonstrates:

AWS Provider

EC2

Security Group

Elastic IP configuration

Docker installation

EC2 user data

Application startup

Terraform variables

Terraform outputs

Default AWS region:

ap-south-1

SSH CIDR is provided as a variable:

variable "ssh_cidr" {

  description = "CIDR block allowed to access SSH"

  type        = string

}

⚠️ Infrastructure Safety

Do not run:

terraform apply

unless the AWS resources, Terraform state, and potential cloud usage are understood.

AWS free-tier and credit eligibility depends on the account, region, resource usage, and current AWS pricing rules.

🧪 Automated Testing

Test file:

tests/test_app.py

The test verifies:

GET /health

      ↓

HTTP 200

Run:

pip install -r requirements-dev.txt

python -m pytest tests/test_app.py

Expected:

1 passed

🐳 Docker Image Publishing

Docker images are published to Docker Hub when changes reach main.

Two tags are generated:

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

Endpoint  Method  Description

/ GET Application dashboard

/health GET Application health

/stats  GET Application statistics

/metrics  GET Prometheus metrics

/deploy POST  Deployment-related API

📁 Project Structure

multicloud-cicd/

│

├── .github/

│   └── workflows/

│       └── deploy.yml

│

├── app/

│   ├── app.py

│   ├── Dockerfile

│   └── requirements.txt

│

├── tests/

│   └── test_app.py

│

├── monitoring/

│   ├── docker-compose.yml

│   └── prometheus.yml

│

├── terraform/

│   └── aws-ec2.tf

│

├── scripts/

│   ├── deploy-aws.sh

│   └── protect-aws.sh

│

├── deployment.yaml

├── service.yaml

├── kind-config.yaml

├── requirements-dev.txt

├── .gitignore

├── LICENSE

└── README.md

🚀 Quick Start

1️⃣ Clone

git clone https://github.com/JOSESAMUEL14/multicloud-cicd.git

cd multicloud-cicd

2️⃣ Create Environment File

Create:

.env

Add:

GRAFANA_ADMIN_PASSWORD=your-secure-password

3️⃣ Start Monitoring

docker compose --env-file .env -f monitoring/docker-compose.yml up -d

4️⃣ Start Application

docker compose --env-file .env -f monitoring/docker-compose.yml up -d

5️⃣ Verify

curl http://localhost:5000/health

🔧 Troubleshooting

Check Application

curl http://localhost:5000/health

Check Docker

docker ps

Check Monitoring

docker compose --env-file .env -f monitoring/docker-compose.yml ps

Check Prometheus

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

 └── Stable merged version

       │

       ├── V1 preserved in v1-stable

       │

       ├── V3 development preserved in devops-v3

       │

       └── V4 AWS deployment developed in

           v4-aws-ec2-deployment

Version History

V1

 │

 └── Original working implementation

      ↓

v1-stable



V3

 │

 └── Advanced portfolio UI + CI/CD improvements

      ↓

devops-v3



V4

 │

 └── AWS EC2 automated deployment

      ↓

v4-aws-ec2-deployment

      ↓

main

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

        2/2 Replicas

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

             │     CODE      │

             └───────┬───────┘

                     ↓

             ┌───────────────┐

             │     TEST      │

             └───────┬───────┘

                     ↓

             ┌───────────────┐

             │     BUILD     │

             └───────┬───────┘

                     ↓

             ┌───────────────┐

             │  CONTAINERIZE │

             └───────┬───────┘

                     ↓

             ┌───────────────┐

             │     SCAN      │

             └───────┬───────┘

                     ↓

             ┌───────────────┐

             │    VALIDATE   │

             └───────┬───────┘

                     ↓

             ┌───────────────┐

             │    PUBLISH    │

             └───────┬───────┘

                     ↓

             ┌───────────────┐

             │    DEPLOY     │

             └───────┬───────┘

                     ↓

             ┌───────────────┐

             │    VERIFY     │

             └───────┬───────┘

                     ↓

             ┌───────────────┐

             │    MONITOR    │

             └───────┬───────┘

                     ↓

             ┌───────────────┐

             │    RECOVER    │

             └───────────────┘

The project emphasizes practical DevOps engineering rather than simply collecting a large number of technologies.

🏆 Key Project Highlights

🔹 Automated CI/CD

GitHub Actions automatically validates and deploys the application.

🔹 Containerized Application

Flask application packaged and executed using Docker.

🔹 Kubernetes Validation

Deployment validated using Kind with two replicas and health probes.

🔹 Security Scanning

Docker images scanned using Trivy for HIGH and CRITICAL vulnerabilities.

🔹 Immutable Deployment

AWS deployment uses the exact Git commit SHA rather than relying only on latest.

🔹 AWS EC2 Deployment

The application has been successfully deployed to AWS EC2 through the CI/CD pipeline.

🔹 Health Verification

Deployment completion is verified using the application's /health endpoint.

🔹 Monitoring

Prometheus, Grafana, and Node Exporter provide local observability.

👨‍💻 Author

Samuel D

B.E. Computer Science and Engineering

🔗 Connect

💻 GitHub

https://github.com/JOSESAMUEL14

💼 LinkedIn

https://linkedin.com/in/samueld14

📧 Email

Josesamueld2005@gmail.com

📜 License

MIT License
