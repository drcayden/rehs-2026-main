kubectl apply -f deploy/k8s/pvc.yaml                                   
kubectl apply -f deploy/k8s/secret.yaml
kubectl apply -f deploy/k8s/deployment.yaml
kubectl apply -f deploy/k8s/service.yaml
kubectl apply -f deploy/k8s/ingress.yaml
kubectl get pods -n rehs-2026-chatbot