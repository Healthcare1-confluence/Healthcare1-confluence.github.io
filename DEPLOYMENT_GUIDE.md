# MkDocs Deployment Guide

Your Healthcare AI Contact Center documentation is now ready to be published!

## 🎯 Quick Reference: Publishing Methods

| Method | Effort | Cost | Setup Time |
|--------|--------|------|-----------|
| **GitHub Pages** | ⭐ Minimal | Free | 2 minutes |
| **Azure Static Web Apps** | ⭐ Minimal | Minimal | 5 minutes |
| **AWS S3 + CloudFront** | ⭐⭐ Medium | ~$0.50/month | 15 minutes |
| **Confluence (Manual)** | ⭐⭐⭐ High | Included | 30+ minutes |
| **Docker + AKS** | ⭐⭐⭐ High | Depends | 30+ minutes |

---

## 🚀 Option 1: GitHub Pages (Recommended for Teams)

### Step 1: Push to GitHub

```bash
# Initialize git (if not done)
git init
git add .
git commit -m "Initial MkDocs setup"
git remote add origin https://github.com/YOUR_ORG/healthcare-contact-center-doc.git
git branch -M main
git push -u origin main
```

### Step 2: Deploy with One Command

```bash
source venv/Scripts/activate
mkdocs gh-deploy
```

### Step 3: Configure GitHub Pages

1. Go to repository **Settings → Pages**
2. Select `gh-pages` branch as source
3. Click Save
4. Documentation is live at: `https://YOUR_ORG.github.io/healthcare-contact-center-doc/`

**Pro Tips:**
- ✓ Free hosting
- ✓ Automatic updates on each push
- ✓ HTTPS by default
- ✓ Custom domain support

---

## 🚀 Option 2: Azure Static Web Apps (Integrated with Azure)

### Step 1: Create Static Web App

```bash
az staticwebapp create \
  --name healthcare-ai-docs \
  --resource-group healthcare-rg \
  --source https://github.com/YOUR_ORG/healthcare-contact-center-doc \
  --branch main \
  --app-location "site" \
  --output-location "site" \
  --sku free
```

### Step 2: Configure Build Settings

Create `.github/workflows/azure-static-web-apps-deploy.yml`:

```yaml
name: Deploy to Azure Static Web App

on:
  push:
    branches:
      - main

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.11'
      - name: Install MkDocs
        run: |
          pip install mkdocs mkdocs-material
      - name: Build docs
        run: mkdocs build
      - name: Deploy to Azure
        uses: azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "site"
```

### Step 3: Access Documentation

Once deployed, access at:
```
https://healthcare-ai-docs.azurestaticapps.net
```

---

## 🚀 Option 3: AWS S3 + CloudFront (High Performance)

### Step 1: Create S3 Bucket

```bash
# Create bucket
aws s3api create-bucket \
  --bucket healthcare-ai-docs \
  --region us-east-1

# Enable static website hosting
aws s3api put-bucket-website \
  --bucket healthcare-ai-docs \
  --website-configuration '{
    "IndexDocument": {"Suffix": "index.html"},
    "ErrorDocument": {"Key": "404.html"}
  }'

# Block public access (use CloudFront instead)
aws s3api put-public-access-block \
  --bucket healthcare-ai-docs \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

### Step 2: Upload Documentation

```bash
# Build MkDocs
mkdocs build

# Sync to S3
aws s3 sync site/ s3://healthcare-ai-docs/
```

### Step 3: Create CloudFront Distribution

```bash
# Create CloudFront distribution
aws cloudfront create-distribution \
  --origin-domain-name healthcare-ai-docs.s3.amazonaws.com \
  --origin-id s3-healthcare-docs \
  --default-root-object index.html \
  --default-cache-behavior ... # (See template)
```

Access at: `https://d123abc.cloudfront.net`

---

## 📋 Option 4: Deploy to Confluence (Manual Sync)

### Step 1: Create Confluence Space

1. Go to Confluence
2. Create new Space: "Healthcare AI Platform Docs"
3. Note Space Key: `HCA`

### Step 2: Convert MkDocs to Confluence Format

Install Confluence sync tool:

```bash
pip install confluence-py
```

### Step 3: Sync Documentation

Create sync script (`sync_to_confluence.py`):

```python
#!/usr/bin/env python
import os
from pathlib import Path
from atlassian import Confluence

# Initialize Confluence client
confluence = Confluence(
    url='https://your-domain.atlassian.net',
    username='email@example.com',
    password='YOUR_API_TOKEN'  # Use API token, not password
)

# Sync docs
docs_path = Path('docs')
for md_file in docs_path.glob('**/*.md'):
    with open(md_file, 'r') as f:
        content = f.read()
    
    # Upload page
    page_title = md_file.stem.replace('-', ' ').title()
    confluence.create_page(
        space='HCA',
        title=page_title,
        body=content,
        parent_title='Healthcare AI Platform'
    )

print("✓ Documentation synced to Confluence!")
```

Run it:
```bash
python sync_to_confluence.py
```

---

## 🐳 Option 5: Docker + AKS Deployment

### Step 1: Create Dockerfile

```dockerfile
FROM node:18-alpine as build
WORKDIR /app
RUN npm install -g http-server

FROM python:3.11-slim
WORKDIR /app
COPY --from=build /usr/local/bin/http-server /usr/local/bin/

RUN pip install mkdocs mkdocs-material
COPY . /app/
RUN mkdocs build

EXPOSE 8000
CMD ["http-server", "site", "-p", "8000"]
```

### Step 2: Build and Push Image

```bash
docker build -t your-registry/healthcare-docs:1.0 .
docker push your-registry/healthcare-docs:1.0
```

### Step 3: Deploy to AKS

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: healthcare-docs
spec:
  replicas: 2
  selector:
    matchLabels:
      app: healthcare-docs
  template:
    metadata:
      labels:
        app: healthcare-docs
    spec:
      containers:
      - name: docs
        image: your-registry/healthcare-docs:1.0
        ports:
        - containerPort: 8000
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: healthcare-docs
spec:
  type: LoadBalancer
  selector:
    app: healthcare-docs
  ports:
  - port: 80
    targetPort: 8000
```

Deploy:
```bash
kubectl apply -f deployment.yaml
```

---

## 📝 CI/CD Pipeline (GitHub Actions)

Create `.github/workflows/deploy-docs.yml`:

```yaml
name: Deploy Documentation

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install mkdocs mkdocs-material
      
      - name: Build documentation
        run: mkdocs build
      
      - name: Deploy to GitHub Pages
        if: github.ref == 'refs/heads/main'
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./site
          cname: docs.healthcare-ai.com  # Optional: custom domain
```

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] Documentation is accessible via chosen URL
- [ ] Navigation works (sidebar links)
- [ ] Images load correctly
- [ ] Code blocks render properly
- [ ] Search functionality works (if enabled)
- [ ] Mobile responsive design looks good
- [ ] All links are working

---

## 🔧 Maintenance & Updates

### Update Documentation

```bash
# Make changes to docs/
vi docs/business-context/overview.md

# Test locally
mkdocs serve

# Commit and push
git add docs/
git commit -m "Update business context"
git push origin main
```

Deployment auto-triggers with each push (if using CI/CD).

### Rebuild Static Site

```bash
mkdocs build
```

---

## 📊 Recommended Setup

For **Production Healthcare Documentation**, we recommend:

```
Primary: GitHub Pages (free, automatic updates)
Backup: Azure Static Web Apps (HIPAA-compliant)
Search: Algolia (premium feature)
Analytics: Google Analytics via MkDocs plugin
```

---

## 🆘 Troubleshooting

### MkDocs won't build?
```bash
pip install --upgrade mkdocs mkdocs-material
mkdocs build --verbose
```

### GitHub Pages not updating?
- Wait 2-3 minutes
- Check "Settings → Pages" shows `gh-pages` branch
- Verify `mkdocs gh-deploy` output

### CloudFront not showing latest?
```bash
aws cloudfront create-invalidation \
  --distribution-id <ID> \
  --paths "/*"
```

---

**Ready to deploy? Choose your method above and follow the steps!**

