# 🚀 Deployment Guide

This guide shows you how to deploy the Symptom Recommendation System to various cloud platforms using GitHub Actions and Docker.

## 📋 Prerequisites

1. **GitHub Repository**: Your code should be in a GitHub repository
2. **Docker Hub Account**: For Docker image deployment
3. **Cloud Platform Account**: Choose one of the supported platforms
4. **Docker Desktop**: For local Docker operations

## 🌐 Supported Platforms

### 1. **Railway** (Recommended - Free Tier)
- Free tier available
- Easy deployment
- Automatic HTTPS
- Supports Docker Hub images

### 2. **Render** (Recommended - Free Tier)
- Free tier available
- Easy deployment
- Automatic HTTPS

### 3. **Heroku** (Paid)
- No free tier anymore
- Very reliable
- Good for production

### 4. **Vercel** (Free Tier)
- Free tier available
- Good for static sites
- Limited for FastAPI

## 🐳 Docker Hub Deployment

### Step 1: Prepare Docker Image

#### 1.1 Build Docker Image Locally
```bash
# Build the image
docker build -t symptom-recommendation-api .

# Test locally
docker run -p 8000:8000 symptom-recommendation-api
```

#### 1.2 Tag for Docker Hub
```bash
# Tag with your Docker Hub username
docker tag symptom-recommendation-api yourusername/symptom-recommendation-api:latest
docker tag symptom-recommendation-api yourusername/symptom-recommendation-api:v1.0.0
```

#### 1.3 Push to Docker Hub
```bash
# Login to Docker Hub
docker login

# Push images
docker push yourusername/symptom-recommendation-api:latest
docker push yourusername/symptom-recommendation-api:v1.0.0
```

### Step 2: Deploy from Docker Hub

#### 2.1 Railway Docker Hub Deployment

1. **Go to [railway.app](https://railway.app)**
2. **Create new project**
3. **Choose "Deploy from Docker Hub"**
4. **Enter your image name**: `yourusername/symptom-recommendation-api:latest`
5. **Configure environment variables**:
   ```
   PORT=8000
   HOST=0.0.0.0
   ```
6. **Deploy**

#### 2.2 Railway CLI Docker Hub Deployment
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Create new project
railway init

# Deploy from Docker Hub
railway up --image yourusername/symptom-recommendation-api:latest
```

### Step 3: Automated Docker Hub Deployment

#### 3.1 GitHub Actions for Docker Hub
Create `.github/workflows/docker-deploy.yml`:

```yaml
name: Build and Deploy Docker Image

on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Docker Buildx
      uses: docker/setup-buildx-action@v2
    
    - name: Login to Docker Hub
      uses: docker/login-action@v2
      with:
        username: ${{ secrets.DOCKER_HUB_USERNAME }}
        password: ${{ secrets.DOCKER_HUB_TOKEN }}
    
    - name: Build and push Docker image
      uses: docker/build-push-action@v4
      with:
        context: .
        push: true
        tags: |
          yourusername/symptom-recommendation-api:latest
          yourusername/symptom-recommendation-api:${{ github.sha }}
        cache-from: type=gha
        cache-to: type=gha,mode=max
```

#### 3.2 Set up GitHub Secrets
Go to your GitHub repository → Settings → Secrets and variables → Actions

Add these secrets:
- `DOCKER_HUB_USERNAME`: Your Docker Hub username
- `DOCKER_HUB_TOKEN`: Your Docker Hub access token

### Step 4: Railway Auto-Deploy from Docker Hub

#### 4.1 Connect Railway to Docker Hub
1. **In Railway dashboard**, go to your project
2. **Add new service** → **"Deploy from Docker Hub"**
3. **Enter image name**: `yourusername/symptom-recommendation-api:latest`
4. **Configure auto-deploy**:
   - Enable "Auto-deploy on push"
   - Set deployment strategy

#### 4.2 Railway Configuration
Create `railway.json` for Docker Hub deployment:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "DOCKERFILE",
    "dockerfilePath": "Dockerfile"
  },
  "deploy": {
    "startCommand": "uvicorn app:app --host 0.0.0.0 --port $PORT",
    "healthcheckPath": "/status",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

## 🔧 Setup Instructions

### Step 1: Prepare Your Repository

Make sure your repository has these files:
- `app.py` - Main FastAPI application
- `requirements.txt` - Python dependencies
- `Dockerfile` - For containerized deployment
- `.dockerignore` - Docker build optimization
- `railway.json` - Railway configuration

### Step 2: Docker Hub Setup

#### 2.1 Create Docker Hub Account
1. Go to [hub.docker.com](https://hub.docker.com)
2. Sign up for free account
3. Create access token:
   - Go to Account Settings → Security
   - Create New Access Token
   - Save the token securely

#### 2.2 Docker Hub Repository
1. Create new repository on Docker Hub
2. Name it: `symptom-recommendation-api`
3. Set visibility (public/private)

### Step 3: Deploy to Railway from Docker Hub

#### 3.1 Manual Deployment
```bash
# Build and push to Docker Hub
docker build -t yourusername/symptom-recommendation-api .
docker push yourusername/symptom-recommendation-api

# Deploy to Railway
railway up --image yourusername/symptom-recommendation-api:latest
```

#### 3.2 Automated Deployment
1. **Set up GitHub Actions** (see above)
2. **Connect Railway to Docker Hub**
3. **Push to GitHub** → Auto-deploy to Railway

## 🔄 GitHub Actions Workflow

The `.github/workflows/docker-deploy.yml` file will:

1. **Build** Docker image on every push
2. **Push** to Docker Hub
3. **Deploy** to Railway automatically
4. **Run tests** before deployment

## 📊 Monitoring

### Health Check
Your deployed app will have a health check endpoint:
```
https://your-app.railway.app/status
https://your-app.onrender.com/status
https://your-app.herokuapp.com/status
```

### API Documentation
Access your API docs at:
```
https://your-app.railway.app/docs
https://your-app.onrender.com/docs
https://your-app.herokuapp.com/docs
```

### Web Interface
Access your web interface at:
```
https://your-app.railway.app/web
https://your-app.onrender.com/web
https://your-app.herokuapp.com/web
```

## 🐳 Docker Commands Reference

### Build and Push
```bash
# Build image
docker build -t symptom-recommendation-api .

# Tag for Docker Hub
docker tag symptom-recommendation-api yourusername/symptom-recommendation-api:latest

# Push to Docker Hub
docker push yourusername/symptom-recommendation-api:latest
```

### Local Testing
```bash
# Run locally
docker run -p 8000:8000 symptom-recommendation-api

# Run with environment variables
docker run -p 8000:8000 -e PORT=8000 symptom-recommendation-api

# Run in background
docker run -d -p 8000:8000 symptom-recommendation-api
```

### Docker Hub Management
```bash
# List local images
docker images

# Remove local image
docker rmi symptom-recommendation-api

# Pull from Docker Hub
docker pull yourusername/symptom-recommendation-api:latest
```

## 🔍 Troubleshooting

### Common Issues:

1. **Docker Build Fails**: Check Dockerfile and requirements.txt
2. **Docker Hub Push Fails**: Verify login and permissions
3. **Railway Deployment Fails**: Check image name and configuration
4. **Port Issues**: Ensure PORT environment variable is set

### Debug Commands:

```bash
# Check Docker Hub login
docker login

# Check Railway status
railway status

# View Railway logs
railway logs

# Check Docker image
docker inspect yourusername/symptom-recommendation-api:latest
```

## 📈 Performance Optimization

1. **Multi-stage builds** for smaller images
2. **Layer caching** for faster builds
3. **Image optimization** for faster deployment
4. **Health checks** for better monitoring

## 🔒 Security Considerations

1. **Docker Hub access tokens** for secure authentication
2. **Image scanning** for vulnerabilities
3. **Non-root user** in Docker containers
4. **Environment variables** for sensitive data

## 📝 Environment Variables

Set these in Railway:

```bash
PORT=8000
HOST=0.0.0.0
ENVIRONMENT=production
```

## 🎯 Quick Deploy Commands

### Docker Hub + Railway:
```bash
# Build and push
docker build -t yourusername/symptom-recommendation-api .
docker push yourusername/symptom-recommendation-api

# Deploy to Railway
railway up --image yourusername/symptom-recommendation-api:latest
```

### Automated Pipeline:
```bash
# Just push to GitHub
git push origin main
# GitHub Actions builds and pushes to Docker Hub
# Railway auto-deploys from Docker Hub
```

## 📞 Support

If you encounter issues:

1. Check Docker Hub repository
2. Review Railway logs
3. Test Docker image locally first
4. Check GitHub Actions workflow status

## 🎉 Success!

Once deployed, your API will be available at:
- **Railway**: `https://your-app.railway.app`
- **Docker Hub**: `docker pull yourusername/symptom-recommendation-api`
- **Web Interface**: `https://your-app.railway.app/web`

Your symptom recommendation system is now live and accessible worldwide! 🌍 