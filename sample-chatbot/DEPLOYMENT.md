# 🚀 Deployment Guide

This guide covers deploying the Sample Chatbot to various platforms.

## 📋 Prerequisites

- GitHub account
- OpenAI API key
- Platform account (Railway, Heroku, etc.)

## 🛤️ Deployment Options

### Option 1: Railway (Recommended)

**Why Railway?**
- Free tier available
- Easy GitHub integration
- Persistent storage
- Custom domains
- Automatic deployments

**Steps:**

1. **Prepare Repository**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin main
   ```

2. **Deploy on Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Add environment variable:
     ```
     OPENAI_API_KEY=your_actual_openai_api_key
     ```
   - Click "Deploy"

3. **Access Your App**:
   - Railway provides a URL like: `https://your-app.up.railway.app`
   - Your chatbot is now live! 🎉

**Railway Tips:**
- Enable automatic deployments for GitHub push
- Use custom domains in settings
- Monitor usage in dashboard

---

### Option 2: Heroku

**Steps:**

1. **Install Heroku CLI**:
   ```bash
   # macOS
   brew install heroku/brew/heroku
   
   # Ubuntu/Debian
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Create and Deploy**:
   ```bash
   # Login to Heroku
   heroku login
   
   # Create app
   heroku create your-chatbot-name
   
   # Set environment variable
   heroku config:set OPENAI_API_KEY=your_api_key
   
   # Deploy
   git push heroku main
   ```

3. **Open Your App**:
   ```bash
   heroku open
   ```

**Heroku Tips:**
- Use `heroku logs --tail` to monitor
- Scale with `heroku ps:scale web=1`
- Custom domains available

---

### Option 3: Vercel

**Steps:**

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Deploy**:
   ```bash
   # Login
   vercel login
   
   # Deploy
   vercel
   
   # Set environment variable
   vercel env add OPENAI_API_KEY
   ```

3. **Configure for Vercel**:
   Create `vercel.json`:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "backend/main.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "backend/main.py"
       }
     ]
   }
   ```

---

### Option 4: Google Cloud Run

**Steps:**

1. **Install Google Cloud CLI**:
   ```bash
   # macOS
   brew install google-cloud-sdk
   
   # Ubuntu
   curl https://sdk.cloud.google.com | bash
   ```

2. **Deploy**:
   ```bash
   # Authenticate
   gcloud auth login
   
   # Deploy
   gcloud run deploy sample-chatbot \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars OPENAI_API_KEY=your_key
   ```

3. **Access**:
   ```bash
   gcloud run services describe sample-chatbot --region us-central1
   ```

---

### Option 5: DigitalOcean App Platform

**Steps:**

1. **Create App Spec**:
   Create `.do/app.yaml`:
   ```yaml
   name: sample-chatbot
   services:
   - name: web
     source_dir: /
     github:
       repo: yourusername/your-repo
       branch: main
     run_command: uvicorn backend.main:app --host 0.0.0.0 --port 8080
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: OPENAI_API_KEY
       value: your_api_key
       type: SECRET
   ```

2. **Deploy**:
   - Go to DigitalOcean Apps
   - Connect GitHub repository
   - Select the app spec file
   - Deploy

---

### Option 6: AWS App Runner

**Steps:**

1. **Create buildspec**:
   Create `buildspec.yml`:
   ```yaml
   version: 0.2
   phases:
     install:
       runtime-versions:
         python: 3.9
     pre_build:
       commands:
         - pip install -r requirements.txt
     build:
       commands:
         - echo "Build completed"
   artifacts:
     files:
       - '**/*'
   ```

2. **Deploy via Console**:
   - Go to AWS App Runner
   - Connect repository
   - Configure environment variables
   - Deploy

---

## 🔧 Environment Configuration

### Required Variables

| Platform | Variable Name | How to Set |
|----------|---------------|------------|
| Railway | `OPENAI_API_KEY` | Dashboard → Variables |
| Heroku | `OPENAI_API_KEY` | `heroku config:set` |
| Vercel | `OPENAI_API_KEY` | Dashboard or CLI |
| Cloud Run | `OPENAI_API_KEY` | Deployment command |
| DigitalOcean | `OPENAI_API_KEY` | App spec file |
| AWS | `OPENAI_API_KEY` | Console configuration |

### Optional Variables

```bash
# Environment mode
ENVIRONMENT=production

# Port (auto-detected on most platforms)
PORT=8000

# OpenAI model
OPENAI_MODEL=gpt-3.5-turbo
```

## 🧪 Testing Deployment

### Health Check

1. **Basic Health**:
   Visit: `https://your-app-url/health`
   
   Expected response:
   ```json
   {
     "status": "healthy",
     "message": "Chatbot is running"
   }
   ```

2. **Chat Test**:
   - Open your app URL
   - Send a test message: "Hello, test message"
   - Verify you get a response

### Load Testing

```bash
# Install artillery for load testing
npm install -g artillery

# Create test config
cat > load-test.yml << EOF
config:
  target: 'https://your-app-url'
  phases:
    - duration: 60
      arrivalRate: 5
scenarios:
  - name: "Chat load test"
    weight: 100
    flow:
      - post:
          url: "/api/chat"
          json:
            message: "Test message"
            history: []
EOF

# Run test
artillery run load-test.yml
```

## 🔍 Monitoring & Debugging

### Platform-Specific Logs

**Railway**:
```bash
railway logs
```

**Heroku**:
```bash
heroku logs --tail
```

**Vercel**:
```bash
vercel logs
```

**Google Cloud**:
```bash
gcloud run services logs read sample-chatbot --region us-central1
```

### Common Issues

**1. "Module not found"**:
- Ensure `requirements.txt` is in root directory
- Check platform build logs

**2. "OPENAI_API_KEY not set"**:
- Verify environment variable is set correctly
- Restart application after setting variables

**3. "Port not available"**:
- Use `PORT` environment variable
- Most platforms auto-detect the correct port

**4. "Frontend 404"**:
- Check file paths are correct
- Verify static file mounting in FastAPI

## 📊 Performance Optimization

### Platform Recommendations

| Platform | Best For | Cost | Scalability |
|----------|----------|------|-------------|
| Railway | Beginners | $5-20/mo | Good |
| Heroku | Production | $7-25/mo | Excellent |
| Vercel | Frontend-focused | Free-$$ | Good |
| Cloud Run | Serverless | Pay-per-use | Auto-scaling |
| DigitalOcean | Developers | $5-12/mo | Good |

### Optimization Tips

1. **Use environment-specific models**:
   - Development: `gpt-3.5-turbo`
   - Production: Consider `gpt-4` for better responses

2. **Implement caching**:
   - Cache frequent responses
   - Reduce OpenAI API calls

3. **Rate limiting**:
   - Implement user rate limits
   - Prevent API abuse

## 🔒 Security Best Practices

1. **API Key Security**:
   - Never commit API keys to git
   - Use platform environment variables
   - Rotate keys regularly

2. **HTTPS**:
   - All platforms provide SSL by default
   - Use HTTPS URLs in production

3. **Input Validation**:
   - Implement message length limits
   - Sanitize user input
   - Add rate limiting

## 📈 Scaling Considerations

### Horizontal Scaling
- Stateless design allows easy scaling
- Most platforms auto-scale
- Monitor OpenAI API rate limits

### Cost Management
- Set usage alerts
- Monitor OpenAI API costs
- Implement caching strategies

---

## 🎉 Success Checklist

- [ ] Code pushed to GitHub
- [ ] Platform account created
- [ ] Environment variables configured
- [ ] Application deployed successfully
- [ ] Health endpoint responding
- [ ] Chat interface working
- [ ] OpenAI API key configured
- [ ] Custom domain (optional)
- [ ] Monitoring set up

**Your chatbot is now live! 🚀**