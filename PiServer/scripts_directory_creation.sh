#!/bin/bash

# Create the scripts directory
mkdir -p scripts

cd scripts

cat <<'EOL' > get_argocd_admin_pass.sh
#!/usr/bin/env bash

echo "Getting ArgoCD admin password:" >&2
export KUBECONFIG=./ansible-runner/runner/.kube/config
kubectl get secret argocd-initial-admin-secret -o jsonpath='{.data.password}' -n argocd | base64 -d;echo
EOL

cat <<'EOL' > get_elastic_pass.sh
#!/usr/bin/env bash

echo "Getting Elastic admin password:" >&2
export KUBECONFIG=./ansible-runner/runner/.kube/config
kubectl get secret efk-es-elastic-user -o jsonpath='{.data.elastic}' -n logging | base64 -d;echo
EOL

cd ..

chmod +x scripts/get_argocd_admin_pass.sh
chmod +x scripts/get_elastic_pass.sh