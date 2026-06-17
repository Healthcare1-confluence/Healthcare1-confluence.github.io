# Deployment Design

## Container Architecture

The FastAPI application is containerized and deployed to Azure Kubernetes Service (AKS).

### Build & Package

1. **Dockerfile** includes:
   - Python 3.11+ base image
   - LangGraph and all dependencies installed
   - FastAPI application code
   - Health check endpoint

2. **Docker Image**
   - Build: `docker build -t healthcare-ai-contact-center:v1.0 .`
   - Push to Azure Container Registry (ACR)
   - Deploy to AKS via Helm or kubectl

### Graph Compilation Strategy

- **Lazy Compilation**: Graph is compiled on first request, not at pod startup
- **No Cold-Start Cost**: Subsequent requests retrieve cached CompiledGraph
- **Singleton Cache**: One compiled instance per pod instance

## Deployment Configuration

### Kubernetes Resources

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: healthcare-ai-contact-center
spec:
  replicas: 2  # Minimum for HA
  template:
    spec:
      containers:
      - name: app
        image: acr.azurecr.io/healthcare-ai-contact-center:v1.0
        ports:
        - containerPort: 8000
        resources:
          requests:
            cpu: 500m
            memory: 1Gi
          limits:
            cpu: 2000m
            memory: 4Gi
        env:
        - name: MONGODB_URL
          valueFrom:
            secretKeyRef:
              name: mongodb-credentials
              key: connection-string
        - name: AZURE_OPENAI_ENDPOINT
          valueFrom:
            secretKeyRef:
              name: azure-openai
              key: endpoint
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: azure-openai
              key: api-key
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

### Autoscaling

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: healthcare-ai-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: healthcare-ai-contact-center
  minReplicas: 2
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

### Resource Limits

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Minimum Replicas | 2 | High availability across AZs |
| Maximum Replicas | 20 | Configurable per environment |
| CPU Request | 500m | Per-pod baseline |
| CPU Limit | 2000m | 4x request for burst capacity |
| Memory Request | 1Gi | Graph compilation + state |
| Memory Limit | 4Gi | Safe margin for ReAct loops |
| Liveness Probe | /health (30s delay, 10s period) | Detects hung processes |
| Readiness Probe | /health (10s delay, 5s period) | Detects initialization issues |

## Environment Configuration

### Azure Secrets Management

Store all credentials in Azure Key Vault:

```bash
# Create secrets
az keyvault secret set --vault-name <vault-name> \
  --name MONGODB-URL --value <connection-string>
  
az keyvault secret set --vault-name <vault-name> \
  --name AZURE-OPENAI-ENDPOINT --value <endpoint>
  
az keyvault secret set --vault-name <vault-name> \
  --name OPENAI-API-KEY --value <key>
```

### Pod Environment Injection

Use Azure Managed Identity + Pod Identity binding:

```yaml
env:
- name: MONGODB_URL
  valueFrom:
    secretKeyRef:
      name: app-secrets
      key: mongodb-url
```

## Deployment Environments

### Development
- Single pod (no HA)
- MemorySaver for checkpointing (no MongoDB)
- Local testing via `mkdocs serve`

### Staging
- 2 pods (HA)
- MongoDB development instance
- Full observability enabled
- A/B testing prompts

### Production
- 2-20 pods (HPA enabled)
- MongoDB production instance (backup enabled)
- Full observability, alerting, PagerDuty
- Immutable container images with semantic versioning

## CI/CD Pipeline

### GitHub Actions Workflow

1. **Push to main** → Trigger build
2. **Build** → Docker image, push to ACR
3. **Test** → Unit tests, integration tests
4. **Deploy Staging** → kubectl apply
5. **Smoke tests** → Health checks
6. **Deploy Production** → Blue-green deployment
7. **Monitor** → Alert on error rate spike

### Rollback Strategy

- Blue-green deployment: keep previous version running
- If error rate >5%, automatically roll back to previous version
- Manual confirmation required for production rollouts

