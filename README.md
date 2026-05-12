# TechTrends

TechTrends is a Flask web app where users can read and post tech articles. This project covers the full cloud-native lifecycle — packaging with Docker, deploying to Kubernetes with raw manifests and Helm, and setting up GitOps with ArgoCD.

## Running the app locally

```bash
cd techtrends
pip install -r requirements.txt
python init_db.py
python app.py
```

Runs on `http://localhost:3111`.

## Docker

```bash
docker build -t techtrends ./techtrends
docker run -d -p 7111:3111 techtrends
```

The image is also published to Docker Hub automatically via GitHub Actions on every push to `main`. The workflow lives in [.github/workflows/techtrends-dockerhub.yml](.github/workflows/techtrends-dockerhub.yml) and needs two repo secrets set:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN` — needs Read & Write scope

## Kubernetes

Raw manifests are in `kubernetes/`. To deploy:

```bash
kubectl apply -f kubernetes/
```

For Helm:

```bash
# staging
helm upgrade --install techtrends ./helm -f helm/values-staging.yaml

# production
helm upgrade --install techtrends ./helm -f helm/values-prod.yaml
```

Prod runs 5 replicas on port 7111. Staging runs 1 replica on port 5111.

## ArgoCD

The `argocd/` directory has Application manifests pointing at this repo. Apply them once ArgoCD is installed on the cluster:

```bash
kubectl apply -f argocd/
```

ArgoCD will then keep staging and prod in sync with the Helm chart in this repo.

## Local Kubernetes with Vagrant

To spin up a local k3s cluster:

```bash
vagrant up
```

VM IP is `192.168.50.4`, 2GB RAM, 2 CPUs.

## App endpoints

- `GET /` — article list
- `GET /<id>` — single article
- `GET /create` — new article form
- `GET /about` — about page
- `GET /healthz` — health check (used for liveness/readiness probes)
- `GET /metrics` — returns post count and total DB connections
