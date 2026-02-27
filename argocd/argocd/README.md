# ArgoCD manifests

This folder was added by the Backstage **ArgoCD (existing repo)** template.

- **apps/app-qa.yaml** – Argo CD Application for QA (`np-argocd`).
- **apps/app-prod.yaml** – Argo CD Application for prod (`prod-argocd`).
- **appsets/appset-pr.yaml** – ApplicationSet for PR preview environments.

## Backstage catalog-info.yaml

When you run the Backstage template, it will **patch your existing `catalog-info.yaml`** and add these Argo CD annotations to the first Component. If you have no `catalog-info.yaml` yet, add a Component and include:

```yaml
  annotations:
    # ArgoCD integration
    argocd/app-name: fastapi-test
    argocd/app-namespace: np-argocd
    argocd/instance-name: main
```

Use the same app name and QA namespace you used when running the template.
