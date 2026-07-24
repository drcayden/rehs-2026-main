kubectl delete -f deploy/k8s/ingress.yaml 
kubectl delete -f deploy/k8s/service.yaml                              
kubectl delete -f deploy/k8s/deployment.yaml
kubectl delete -f deploy/k8s/secret.yaml
kubectl delete -f deploy/k8s/pvc.yaml 
kubectl get pods -n rehs-2026-chatbot