# Kubernetes Deployment Setup Log

This document tracks all commands needed to set up the MBASIC web application for deployment on DigitalOcean Kubernetes.

## Prerequisites
- `doctl` CLI installed and authenticated
- `kubectl` configured to connect to your Kubernetes cluster
- Docker installed locally

### Install Docker (if needed)
```bash
# Install Docker from Ubuntu repository
sudo apt-get update
sudo apt-get install -y docker.io

# Add user to docker group (requires logout/login or newgrp to take effect)
sudo usermod -aG docker $USER

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# After running above, logout/login OR run: newgrp docker
```

### Configure doctl for Docker registry
```bash
# Give doctl snap permission to access Docker
sudo snap connect doctl:dot-docker
```

## Container Registry Setup

### 1. Create DigitalOcean Container Registry
```bash
# Create the registry with starter tier (free)
doctl registry create <YOUR_REGISTRY_NAME> --subscription-tier starter --region nyc3
```

### 2. Configure Docker Authentication
```bash
# Login to the registry
doctl registry login
```

## Kubernetes Configuration

### 3. Create Kubernetes Secrets
```bash
# First create the namespace
kubectl apply -f deployment/k8s_templates/namespace.yaml

# Create the secrets with MySQL and hCaptcha credentials
kubectl create secret generic mbasic-secrets \
  --namespace=mbasic \
  --from-literal=MYSQL_HOST=<YOUR_MYSQL_PRIVATE_IP> \
  --from-literal=MYSQL_USER=mbasic \
  --from-literal=MYSQL_PASSWORD='<YOUR_PASSWORD>' \
  --from-literal=HCAPTCHA_SITE_KEY=<YOUR_SITE_KEY> \
  --from-literal=HCAPTCHA_SECRET_KEY=<YOUR_SECRET_KEY>

# Note: Use private network IP for MySQL connection if in same VPC
# No SSL needed for MySQL connection (firewall-based security on private network)
```

## Docker Image Build and Push

### 4. Build Docker Image
```bash
# Build the Docker image
docker build -t registry.digitalocean.com/<YOUR_REGISTRY>/mbasic-web:latest .
```

### 5. Push to Registry
```bash
# Push the image to DigitalOcean registry
docker push registry.digitalocean.com/<YOUR_REGISTRY>/mbasic-web:latest
```

## Deployment

### 6. Apply Kubernetes Manifests
```bash
# Deploy Redis (session storage)
kubectl apply -f deployment/k8s_templates/redis-deployment.yaml

# Deploy ConfigMap (multiuser.json config)
kubectl apply -f deployment/k8s_templates/mbasic-configmap.yaml

# Deploy landing page
kubectl apply -f deployment/k8s_templates/landing-page-deployment.yaml

# Deploy MBASIC web application
kubectl apply -f deployment/k8s_templates/mbasic-deployment.yaml

# Deploy ingress (routes traffic, TLS/SSL)
kubectl apply -f deployment/k8s_templates/ingress.yaml
```

### 7. Verify Deployment
```bash
# Check pod status
kubectl get pods -n mbasic

# Check services
kubectl get svc -n mbasic

# Check ingress
kubectl get ingress -n mbasic

# View logs from a pod
kubectl logs -n mbasic -l app=mbasic-web --tail=50
```

## Configuration Summary

- **Registry:** `registry.digitalocean.com/<YOUR_REGISTRY>`
- **Image:** `registry.digitalocean.com/<YOUR_REGISTRY>/mbasic-web:latest`
- **Domain:** Your domain
- **MySQL Host:** Private network IP (if using VPC)
- **MySQL User:** `mbasic`
- **MySQL Database:** `mbasic_logs`
- **Let's Encrypt Email:** Your email for certificate notifications
- **hCaptcha:** Get keys from https://www.hcaptcha.com/

---
**Last Updated:** 2025-11-12
