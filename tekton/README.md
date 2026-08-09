# Tekton CD Pipeline

The pipeline clones the repository, runs linting/tests, and only deploys the Kubernetes manifests after the test task succeeds.

```bash
kubectl apply -f tekton/pipeline.yaml
kubectl create -f tekton/pipelinerun.yaml
```

For a real cluster, replace the sample `accounts:latest` image with an image available to the cluster and configure registry credentials when using a private registry.
