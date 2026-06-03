#!/bin/bash
# ── MultiCloud CI/CD — AWS EC2 Deploy Script ──
# Run this on your EC2 instance after first login

set -e

echo "================================================"
echo "  MultiCloud CI/CD — AWS Deployment Script"
echo "================================================"

IMAGE="josesamuel14/multicloud-app:latest"
REGION=$(curl -s http://169.254.169.254/latest/meta-data/placement/region 2>/dev/null || echo "ap-south-1")

echo "[1/5] Updating system..."
sudo apt-get update -y -q

echo "[2/5] Installing Docker..."
sudo apt-get install -y -q docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker ubuntu

echo "[3/5] Pulling latest image from Docker Hub..."
sudo docker pull $IMAGE

echo "[4/5] Stopping old container if running..."
sudo docker stop multicloud-app 2>/dev/null || true
sudo docker rm multicloud-app 2>/dev/null || true

echo "[5/5] Starting new container..."
sudo docker run -d \
  -p 5000:5000 \
  --name multicloud-app \
  --restart unless-stopped \
  -e CLOUD_PROVIDER=aws \
  -e CLOUD_REGION=$REGION \
  $IMAGE

echo "================================================"
echo "  ✅ Deployment Complete!"
echo "  🌐 App running at: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):5000"
echo "================================================"

# ── AUTO STOP PROTECTION ──
echo "[PROTECTION] Setting up auto-stop at 11PM daily..."
(crontab -l 2>/dev/null; echo "0 23 * * * sudo shutdown -h now # multicloud-auto-stop") | crontab -
echo "[PROTECTION] ✅ Auto-stop scheduled at 11PM every night"
echo "[PROTECTION] ✅ Your EC2 will never run overnight accidentally"
