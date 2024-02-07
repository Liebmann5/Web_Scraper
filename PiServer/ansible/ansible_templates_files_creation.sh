#!/bin/bash

# Create the templates directory
mkdir -p templates

cd templates

cat <<'EOL' > argocd_root_app.yml.j2
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: root
  namespace: argocd
spec:
  destination:
    namespace: argocd
    server: https://kubernetes.default.svc
  project: default
  source:
    path: argocd/bootstrap/root
    repoURL: https://github.com/liebmann5/pi-cluster
    targetRevision: master
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    retry:
      limit: 10
      backoff:
        duration: 1m
        maxDuration: 16m
        factor: 2
    syncOptions:
    - CreateNamespace=true
EOL

cat <<'EOL' > ionos-credentials.ini.j2
dns_ionos_prefix = {{ ionos_public_prefix }}
dns_ionos_secret = {{ ionos_secret }}
dns_ionos_endpoint = {{ ionos_api_endpoint }}
EOL

#cd ..

chmod +x argocd_root_app.yml.j2
chmod +x ionos-credentials.ini.j2