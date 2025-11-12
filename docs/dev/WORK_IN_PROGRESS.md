# Work In Progress: Kubernetes Deployment Configuration

## Task
Configure and deploy MBASIC web application to DigitalOcean Kubernetes cluster.

## Status
**Phase 1: Configuration** ✅ COMPLETED
**Phase 2: Docker Build** ✅ COMPLETED
**Phase 3: Deployment** ✅ COMPLETED
**Phase 4: DNS Configuration** ✅ COMPLETED
**Phase 5: SSL Certificate** ⏳ IN PROGRESS (waiting for DNS propagation)

## Completed Steps

### 1. ✅ Container Registry
- Created DigitalOcean registry: `awohl-mbasic` (starter tier, free)
- Registry URL: `registry.digitalocean.com/awohl-mbasic`
- Updated `deployment/k8s_templates/mbasic-deployment.yaml` with registry URL

### 2. ✅ Ingress Configuration
- Updated `deployment/k8s_templates/ingress.yaml` with Let's Encrypt email: `xlets@awohl.com`
- Domain: `mbasic.awohl.com`

### 3. ✅ Network Configuration
- Identified shared VPC: `b3756118-dc84-11e8-8650-3cfdfea9f8c8`
- awohl4 droplet (MariaDB): `10.136.0.2` (private IP)
- Kubernetes nodes: `10.136.0.3`, `10.136.0.4`, `10.136.0.5`
- Using private network for MySQL connection (no SSL)

### 4. ✅ Kubernetes Secrets
- Created namespace: `mbasic`
- Created secret: `mbasic-secrets` with:
  - MySQL credentials (host: 10.136.0.2, user: mbasic, password: [stored])
  - hCaptcha keys (site key: 849ee574-ddc4-468c-b8be-bdb2936cd808, secret: [stored])

### 5. ✅ Deployment Configuration Updates
- Removed MySQL CA certificate volume mount (not needed for non-SSL connection)
- Updated deployment to use environment variables from secrets

### 6. ✅ Docker Installation
- Installed Docker: `docker.io` version 28.2.2
- Added user to docker group
- Configured doctl snap for Docker registry access: `sudo snap connect doctl:dot-docker`
- Logged into DigitalOcean registry: `doctl registry login`

### 7. ✅ Documentation
- Created comprehensive setup guide: `docs/dev/KUBERNETES_DEPLOYMENT_SETUP.md`
- Documented all commands for future reference

### 8. ✅ Docker Build and Push
- Built Docker image successfully
- Pushed to registry: `registry.digitalocean.com/awohl-mbasic/mbasic-web:latest`

### 9. ✅ Kubernetes Deployment
- Deployed Redis (1 pod running)
- Deployed ConfigMap
- Deployed landing page (2 pods running)
- Deployed MBASIC application (3 pods running)
- Created image pull secret: `registry-awohl-mbasic`
- Updated deployment to use image pull secret

### 10. ✅ SSL and Ingress Setup
- Installed cert-manager v1.14.2
- Created Let's Encrypt ClusterIssuer (production)
- Installed nginx-ingress controller v1.9.5
- Deployed ingress configuration
- Load balancer IP assigned: **129.212.196.85**

### 11. ✅ DNS Configuration
- Created A record via doctl: `mbasic.awohl.com` → `129.212.196.85`
- TTL: 300 seconds
- DNS propagating (resolves on Google DNS 8.8.8.8)

### 12. ✅ Redis Configuration
- Enabled Redis session storage: `NICEGUI_REDIS_URL=redis://redis-service:6379`
- Updated MBASIC deployment with Redis connection
- Verified pods showing "Redis storage enabled"
- Session state now shared across all load-balanced instances

## Next Steps (Automated)

1. **SSL Certificate Provisioning** (in progress):
   - DNS propagating to global DNS servers
   - Let's Encrypt HTTP-01 challenge pending
   - Certificate will auto-issue once DNS propagates to cluster DNS
   - Expected completion: 10-20 minutes from DNS record creation

2. **Monitor SSL Certificate**:
   Once DNS propagates, the Let's Encrypt certificate will be automatically issued:
   ```bash
   kubectl get certificate -n mbasic
   kubectl describe certificate mbasic-tls -n mbasic
   ```

3. **Access Your Application**:
   - Landing page: https://mbasic.awohl.com/
   - MBASIC IDE: https://mbasic.awohl.com/ide

## Files Modified
- `deployment/k8s_templates/mbasic-deployment.yaml` - Added imagePullSecrets for registry authentication
- `deployment/k8s_templates/ingress.yaml` - Added ingressClassName, removed configuration-snippet (disabled by admin)
- `docs/dev/KUBERNETES_DEPLOYMENT_SETUP.md` - Created comprehensive setup guide
- `docs/dev/WORK_IN_PROGRESS.md` - This file

## Additional Notes

### Architecture
- **Redis**: In-cluster deployment (1 pod in mbasic namespace) for session storage
- **MySQL**: External on awohl4 droplet at 10.136.0.2 (private network) for user accounts
- **MBASIC Web**: 3-10 pods (HPA enabled) with shared Redis sessions
- **Landing Page**: 2 pods (nginx static content)

### Security & Configuration
- All credentials stored in Kubernetes secrets, not in config files
- Private networking between k8s cluster and MySQL server (10.136.0.2, more secure/faster)
- Image pull secret: `registry-awohl-mbasic` for accessing private registry
- Nginx-ingress controller configuration snippets disabled by default for security
- SSL certificate auto-renews via Let's Encrypt (90-day cycle)

### Networking
- Load balancer IP: **129.212.196.85** (assigned by DigitalOcean)
- Domain: **mbasic.awohl.com**
- Routes: `/` → landing page, `/ide` → MBASIC IDE
- VPC: b3756118-dc84-11e8-8650-3cfdfea9f8c8 (shared with awohl4)

---
**Created:** 2025-11-12
**Last Updated:** 2025-11-12
