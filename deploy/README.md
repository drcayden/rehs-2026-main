# Deploy — build, run, and ship the chatbot

Two stages: run it in **Docker** locally (Week 5), then ship it to **Kubernetes**
on NRP (Week 7).

---

## Local Docker (Week 5)

Build from the **repo root** (the Dockerfile lives in `deploy/` but copies from `.`):

```bash
docker build -t rehs-chatbot:v0.1 -f deploy/Dockerfile .
docker run --env-file .env -p 8501:8501 rehs-chatbot:v0.1
```

Open http://localhost:8501 — it should look identical to running outside Docker.

---

## Kubernetes on NRP (Week 7)

The manifests live in `deploy/k8s/`. They use **placeholder tokens** (`<<NAMESPACE>>`,
`<<IMAGE>>`, etc.) so they don't ship wrong cluster values. **Before you apply, fill
them in** with the real, mentor-confirmed values for your cluster. See
`resources/` in the curriculum for the confirmed values table.

| Placeholder | What it is | Example |
|---|---|---|
| `<<NAMESPACE>>` | your team's namespace | `rehs-2026` |
| `<<GH_ORG>>` | GitHub org/user owning the repo + image | `sdsc-rehs` |
| `<<IMAGE>>` | full image ref incl. tag | `ghcr.io/sdsc-rehs/rehs-chatbot:v0.7` |
| `<<INGRESS_HOST>>` | public hostname | `rehs-chatbot.nrp-nautilus.io` |
| `<<INGRESS_CLASS>>` | ingress class | `haproxy` |
| `<<CERT_ISSUER>>` | cert-manager cluster issuer | `letsencrypt-prod` |
| `<<STORAGE_CLASS>>` | PVC storage class | `rook-ceph-block` |
| `<<TLS_SECRET>>` | secret cert-manager writes the TLS cert into | `rehs-chatbot-tls` |

### Push the image (GHCR option)

```bash
docker tag rehs-chatbot:v0.7 <<IMAGE>>
docker login ghcr.io -u <gh-username>   # use a GitHub PAT with package:write
docker push <<IMAGE>>
```

### Create the secret (NEVER commit it)

`secret.example.yaml` is a TEMPLATE. Do not put your real token in a file you commit.
Prefer creating it imperatively:

```bash
kubectl create secret generic chatbot-llm-token \
  --from-literal=NRP_LLM_TOKEN=sk-yourtoken \
  -n <<NAMESPACE>>
```

### Apply, in order

```bash
kubectl apply -f deploy/k8s/configmap.yaml
kubectl apply -f deploy/k8s/pvc.yaml
kubectl apply -f deploy/k8s/deployment.yaml
kubectl apply -f deploy/k8s/service.yaml
kubectl apply -f deploy/k8s/ingress.yaml
kubectl get pods -n <<NAMESPACE>> -w
```

The PVC starts **empty** — seed it (one-shot Job, initContainer, or baked into the
image). See the TODO in `deploy/Dockerfile`.

---

## Common errors

| Symptom | Likely cause | Fix |
|---|---|---|
| Docker image is 5 GB | copied `.venv/` or no `--no-cache-dir` | check `.dockerignore`; it excludes `.venv/`, `__pycache__/`, `*.pyc` |
| Streamlit "running" but never opens in a container | missing `--server.address=0.0.0.0` | already set in the CMD — don't remove it |
| Pod `ImagePullBackOff` | private image, no pull secret | make the GHCR image public or add an `imagePullSecret` |
| Pod `CrashLoopBackOff` | app crashes on start | `kubectl logs <pod> --previous` |
| PVC stuck `Pending` | wrong storage class | `kubectl get storageclass`; fix `<<STORAGE_CLASS>>` |
| Public URL 502/504 | Service can't reach pod | confirm pod `Ready` and Service `selector` matches pod labels |
| TLS warning in browser | wrong cert issuer / class | `kubectl describe ingress`; confirm `<<CERT_ISSUER>>` and `<<INGRESS_CLASS>>` |
| Vector DB empty after restart | writing outside the PVC mount | data must be under `/app/chroma_db` (the mount path) |
