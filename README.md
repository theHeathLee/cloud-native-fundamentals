# TechTrends

A cloud-native news sharing web application built with Flask, containerized with Docker, and deployed to Kubernetes using Helm and ArgoCD.

## Overview

TechTrends allows users to browse, create, and share technology articles. It exposes health and metrics endpoints for observability, and is designed for GitOps-style continuous deployment across staging and production environments.

## Tech Stack

| Layer | Technology |
|---|---|
| Application | Python 3.8 / Flask |
| Database | SQLite |
| Container | Docker |
| Orchestration | Kubernetes (k3s) |
| Package Manager | Helm |
| GitOps | ArgoCD |
| CI/CD | GitHub Actions |
| Local Dev | Vagrant + VirtualBox |

## Project Structure

```
.
├── techtrends/           # Flask application
│   ├── app.py            # Main application & routes
│   ├── init_db.py        # Database initializer
│   ├── schema.sql        # SQLite schema
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── static/
│   └── templates/
├── kubernetes/           # Raw Kubernetes manifests
│   ├── namespace.yaml
│   ├── deploy.yaml
│   └── service.yaml
├── helm/                 # Helm chart
│   ├── Chart.yaml
│   ├── values.yaml           # Defaults (sandbox)
│   ├── values-staging.yaml
│   ├── values-prod.yaml
│   └── templates/
├── argocd/               # ArgoCD Application manifests
│   ├── argocd-server-nodeport.yaml
│   ├── helm-techtrends-staging.yaml
│   └── helm-techtrends-prod.yaml
├── Vagrantfile           # Local k3s VM
└── .github/workflows/
    └── techtrends-dockerhub.yml  # Docker build & push CI
```

## Application Endpoints

| Endpoint | Description |
|---|---|
| `GET /` | Home — list all articles |
| `GET /<id>` | View a single article |
| `GET /create` | Create a new article |
| `GET /about` | About page |
| `GET /healthz` | Liveness/readiness probe |
| `GET /metrics` | DB connection count and post count |

## Running Locally

**Prerequisites:** Python 3.8+

```bash
cd techtrends
pip install -r requirements.txt
python init_db.py
python app.py
```

App runs at `http://localhost:3111`.

## Docker

```bash
# Build
docker build -t techtrends ./techtrends

# Run
docker run -p 3111:3111 techtrends
```

## CI/CD — GitHub Actions

On every push to `main`, the workflow in [.github/workflows/techtrends-dockerhub.yml](.github/workflows/techtrends-dockerhub.yml) builds and pushes the image to Docker Hub.

**Required GitHub secrets:**

| Secret | Value |
|---|---|
| `DOCKERHUB_USERNAME` | Your Docker Hub username |
| `DOCKERHUB_TOKEN` | Docker Hub access token (Read & Write) |

```bash
gh secret set DOCKERHUB_USERNAME
gh secret set DOCKERHUB_TOKEN
```

## Kubernetes Deployment

### Raw manifests

```bash
kubectl apply -f kubernetes/
```

### Helm

```bash
# Staging
helm upgrade --install techtrends ./helm -f helm/values-staging.yaml

# Production
helm upgrade --install techtrends ./helm -f helm/values-prod.yaml
```

### Environment comparison

| Setting | Staging | Production |
|---|---|---|
| Replicas | 1 | 5 |
| Service port | 5111 | 7111 |
| Image pull policy | IfNotPresent | Always |
| Memory limit | 128Mi | 256Mi |

## GitOps with ArgoCD

ArgoCD watches this repo and syncs the Helm chart to the cluster automatically.

1. Update the `repoURL` in [argocd/helm-techtrends-staging.yaml](argocd/helm-techtrends-staging.yaml) and [argocd/helm-techtrends-prod.yaml](argocd/helm-techtrends-prod.yaml) with your GitHub repo URL.
2. Apply the ArgoCD Application manifests:

```bash
kubectl apply -f argocd/
```

## Local Kubernetes with Vagrant

Spins up a k3s single-node cluster in a VirtualBox VM:

```bash
vagrant up
```

The VM is reachable at `192.168.50.4`. Export the kubeconfig:

```bash
export KUBECONFIG=/etc/rancher/k3s/k3s.yaml
```
