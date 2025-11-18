#!/bin/bash
# Script to diagnose and fix 503 errors after database migration

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${YELLOW}=== MBASIC 503 Diagnostic and Fix Script ===${NC}"
echo

# Check if we have kubectl access
if ! kubectl get pods -n mbasic &>/dev/null; then
    echo -e "${RED}Error: Cannot access Kubernetes cluster${NC}"
    echo "Please ensure kubeconfig is set up:"
    echo "  doctl kubernetes cluster kubeconfig save mbasic-cluster"
    exit 1
fi

# Step 1: Check pod status
echo -e "${YELLOW}1. Checking pod status...${NC}"
kubectl get pods -n mbasic
echo

# Step 2: Check pod logs for errors
echo -e "${YELLOW}2. Checking recent logs for errors...${NC}"
echo "--- Latest logs from mbasic-web pods ---"
kubectl logs -n mbasic -l app=mbasic-web --tail=50 --prefix=true | grep -i "error\|exception\|fail\|mysql\|database" || echo "No obvious errors in logs"
echo

# Step 3: Check current secrets
echo -e "${YELLOW}3. Checking current MySQL configuration...${NC}"
MYSQL_HOST=$(kubectl get secret mbasic-secrets -n mbasic -o jsonpath='{.data.MYSQL_HOST}' | base64 -d)
MYSQL_USER=$(kubectl get secret mbasic-secrets -n mbasic -o jsonpath='{.data.MYSQL_USER}' | base64 -d)
echo "Current MYSQL_HOST: $MYSQL_HOST"
echo "Current MYSQL_USER: $MYSQL_USER"
echo

# Step 4: Test database connectivity from a pod
echo -e "${YELLOW}4. Testing database connectivity from pod...${NC}"
POD=$(kubectl get pod -n mbasic -l app=mbasic-web -o jsonpath='{.items[0].metadata.name}')
if [ -n "$POD" ]; then
    echo "Testing from pod: $POD"
    kubectl exec -n mbasic $POD -- bash -c 'echo "Testing MySQL connection to $MYSQL_HOST..."; timeout 5 bash -c "cat < /dev/null > /dev/tcp/$MYSQL_HOST/3306" && echo "SUCCESS: Port 3306 is reachable" || echo "FAILED: Cannot reach $MYSQL_HOST:3306"' || echo "Pod not ready for exec"
else
    echo "No running pods found to test from"
fi
echo

# Step 5: Check service endpoints
echo -e "${YELLOW}5. Checking service endpoints...${NC}"
kubectl get endpoints -n mbasic
echo

# Step 6: Provide fix instructions
echo -e "${YELLOW}=== Diagnosis Complete ===${NC}"
echo
echo -e "${YELLOW}To fix the issue:${NC}"
echo
echo "1. If database host changed, update the secret:"
echo "   kubectl create secret generic mbasic-secrets -n mbasic \\"
echo "     --from-literal=MYSQL_HOST='awohl.com' \\"
echo "     --from-literal=MYSQL_USER='your-mysql-user' \\"
echo "     --from-literal=MYSQL_PASSWORD='your-mysql-password' \\"
echo "     --from-literal=HCAPTCHA_SITE_KEY='your-hcaptcha-site-key' \\"
echo "     --from-literal=HCAPTCHA_SECRET_KEY='your-hcaptcha-secret-key' \\"
echo "     --dry-run=client -o yaml | kubectl apply -f -"
echo
echo "2. Restart the deployment to pick up new secrets:"
echo "   kubectl rollout restart deployment/mbasic-web -n mbasic"
echo
echo "3. Watch the rollout:"
echo "   kubectl rollout status deployment/mbasic-web -n mbasic"
echo
echo "4. Check pod logs:"
echo "   kubectl logs -f -n mbasic -l app=mbasic-web"
echo
