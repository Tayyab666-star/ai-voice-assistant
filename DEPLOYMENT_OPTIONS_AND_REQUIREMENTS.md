# AI Voice Assistant - Deployment Options & System Requirements

## Overview

The AI Voice Assistant can be deployed in multiple environments, from local development to production cloud infrastructure. This guide covers all deployment options, system requirements, and step-by-step instructions.

## 🖥️ Deployment Options

### 1. Local Development (Your PC/Laptop)
**Best for**: Development, testing, learning the system

### 2. Single Server Deployment
**Best for**: Small businesses, proof of concept, low-traffic scenarios

### 3. Cloud Deployment (Recommended for Production)
**Best for**: Production use, high availability, scalability

### 4. Kubernetes Cluster
**Best for**: Enterprise deployment, high scalability, microservices management

---

## 💻 PC/Server Requirements

### Minimum Requirements (Local Development)

**Hardware:**
- **CPU**: 4 cores (Intel i5 or AMD Ryzen 5 equivalent)
- **RAM**: 8 GB
- **Storage**: 20 GB free space (SSD recommended)
- **Network**: Stable internet connection (for API calls)

**Software:**
- **OS**: Windows 10/11, macOS 10.15+, or Linux (Ubuntu 20.04+ recommended)
- **Docker**: Version 20.10+
- **Docker Compose**: Version 2.0+
- **Python**: 3.9+ (if running without Docker)
- **Git**: For code management

### Recommended Requirements (Local Development)

**Hardware:**
- **CPU**: 8 cores (Intel i7 or AMD Ryzen 7)
- **RAM**: 16 GB
- **Storage**: 50 GB free space (NVMe SSD)
- **Network**: High-speed internet (for faster API responses)

### Production Server Requirements

**Single Server Deployment:**
- **CPU**: 8-16 cores
- **RAM**: 32-64 GB
- **Storage**: 100+ GB SSD
- **Network**: High-speed internet with low latency
- **OS**: Ubuntu 22.04 LTS or CentOS 8+

**Cloud Instance Recommendations:**
- **AWS**: t3.xlarge or larger (4 vCPU, 16 GB RAM)
- **Google Cloud**: n2-standard-4 or larger
- **Azure**: Standard_D4s_v3 or larger
- **DigitalOcean**: 8 GB Memory droplet or larger

### Kubernetes Cluster Requirements

**Minimum Cluster:**
- **Nodes**: 3 nodes (1 master, 2 workers)
- **Per Node**: 4 vCPU, 8 GB RAM, 50 GB storage
- **Total**: 12 vCPU, 24 GB RAM, 150 GB storage

**Production Cluster:**
- **Nodes**: 5+ nodes (3 masters, 3+ workers)
- **Per Node**: 8 vCPU, 16 GB RAM, 100 GB storage
- **Load Balancer**: For external traffic
- **Persistent Storage**: For database and logs

---

## 🚀 Deployment Instructions

### Option 1: Local Development Setup

**Step 1: Install Prerequisites**

```bash
# Install Docker Desktop (Windows/Mac)
# Download from: https://www.docker.com/products/docker-desktop

# Or install Docker on Linux
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

**Step 2: Clone and Setup**

```bash
# Clone the repository
git clone <your-repo-url>
cd ai-voice-assistant

# Copy environment template
cp .env.example .env

# Edit .env file with your API keys
nano .env  # or use your preferred editor
```

**Step 3: Configure Environment Variables**

Edit `.env` file with your credentials:

```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/voice_assistant

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# Twilio
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

# Google (optional)
GOOGLE_CREDENTIALS_PATH=/app/credentials/google-credentials.json
GOOGLE_CALENDAR_ID=your_calendar_id

# ElevenLabs (optional)
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

**Step 4: Start the System**

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

**Step 5: Verify Installation**

```bash
# Run system validation
python scripts/validate_system.py

# Test individual services
curl http://localhost:8001/health  # Call Handler
curl http://localhost:8002/health  # STT Service
curl http://localhost:8003/health  # TTS Service
curl http://localhost:8004/health  # NLU Service
curl http://localhost:8005/health  # Appointment Service
curl http://localhost:8006/health  # SMS Service
```

### Option 2: Single Server Deployment

**Step 1: Prepare Server**

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install additional tools
sudo apt install -y git nginx certbot python3-certbot-nginx
```

**Step 2: Setup SSL Certificate (Production)**

```bash
# Install SSL certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

**Step 3: Deploy Application**

```bash
# Clone repository
git clone <your-repo-url>
cd ai-voice-assistant

# Setup production environment
cp .env.production .env
# Edit .env with production values

# Start services
docker-compose -f docker-compose.prod.yml up -d

# Setup reverse proxy (nginx)
sudo cp nginx/production.conf /etc/nginx/sites-available/voice-assistant
sudo ln -s /etc/nginx/sites-available/voice-assistant /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

### Option 3: Cloud Deployment (AWS Example)

**Step 1: Setup AWS Infrastructure**

```bash
# Install AWS CLI
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install

# Configure AWS
aws configure

# Create EC2 instance
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --instance-type t3.xlarge \
  --key-name your-key-pair \
  --security-group-ids sg-xxxxxxxxx \
  --subnet-id subnet-xxxxxxxxx
```

**Step 2: Setup RDS Database**

```bash
# Create RDS PostgreSQL instance
aws rds create-db-instance \
  --db-instance-identifier voice-assistant-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username postgres \
  --master-user-password your-secure-password \
  --allocated-storage 20
```

**Step 3: Deploy to EC2**

```bash
# SSH to instance
ssh -i your-key.pem ubuntu@your-instance-ip

# Follow single server deployment steps
# Update DATABASE_URL to point to RDS instance
```

### Option 4: Kubernetes Deployment

**Step 1: Setup Kubernetes Cluster**

```bash
# Using managed Kubernetes (recommended)
# AWS EKS
eksctl create cluster --name voice-assistant --region us-west-2 --nodes 3

# Google GKE
gcloud container clusters create voice-assistant --num-nodes=3

# Azure AKS
az aks create --resource-group myResourceGroup --name voice-assistant --node-count 3
```

**Step 2: Deploy to Kubernetes**

```bash
# Configure kubectl
kubectl config current-context

# Create namespace
kubectl create namespace ai-voice-assistant

# Deploy secrets
kubectl apply -f k8s/secrets.yaml

# Deploy services
kubectl apply -f k8s/

# Check deployment
kubectl get pods -n ai-voice-assistant
```

---

## 🔧 Required API Keys and Services

### Essential Services (Required)

1. **OpenAI API Key**
   - **Purpose**: Natural Language Understanding and Speech-to-Text
   - **Cost**: Pay-per-use (approximately $0.002 per 1K tokens)
   - **Get it**: https://platform.openai.com/api-keys
   - **Free tier**: $5 credit for new accounts

2. **Twilio Account**
   - **Purpose**: Voice calls and SMS messaging
   - **Cost**: Pay-per-use (calls ~$0.0085/min, SMS ~$0.0075/message)
   - **Get it**: https://www.twilio.com/console
   - **Free tier**: $15 credit for new accounts

### Optional Services (Enhanced Features)

3. **Google Cloud Platform**
   - **Purpose**: Alternative STT/TTS, Google Calendar integration
   - **Cost**: Pay-per-use
   - **Get it**: https://console.cloud.google.com/
   - **Free tier**: $300 credit for new accounts

4. **ElevenLabs API**
   - **Purpose**: High-quality Text-to-Speech
   - **Cost**: Subscription-based (~$5/month for starter)
   - **Get it**: https://elevenlabs.io/
   - **Free tier**: 10,000 characters/month

5. **AWS Account** (if using AWS Polly)
   - **Purpose**: Alternative Text-to-Speech
   - **Cost**: Pay-per-use
   - **Get it**: https://aws.amazon.com/
   - **Free tier**: 5 million characters/month for 12 months

---

## 💰 Cost Estimates

### Development/Testing (Monthly)
- **Local development**: Free (using your PC)
- **API costs**: $10-50/month (depending on usage)
- **Total**: $10-50/month

### Small Business Deployment
- **Cloud server**: $50-100/month (AWS t3.large)
- **Database**: $15-30/month (managed database)
- **API costs**: $50-200/month
- **Total**: $115-330/month

### Enterprise Deployment
- **Kubernetes cluster**: $300-1000/month
- **Load balancers**: $20-50/month
- **Database**: $100-500/month
- **API costs**: $200-1000/month
- **Total**: $620-2550/month

---

## 🔍 Performance Expectations

### Local Development
- **Concurrent calls**: 1-5
- **Response time**: 2-5 seconds
- **Suitable for**: Testing, development

### Single Server
- **Concurrent calls**: 10-25
- **Response time**: 1-3 seconds
- **Suitable for**: Small businesses, low traffic

### Cloud/Kubernetes
- **Concurrent calls**: 100+
- **Response time**: 0.5-2 seconds
- **Suitable for**: Production, high traffic

---

## 🛠️ Quick Start Commands

### For Developers (Local Setup)
```bash
# Quick start
git clone <repo-url>
cd ai-voice-assistant
cp .env.example .env
# Edit .env with your API keys
docker-compose up -d
python scripts/validate_system.py
```

### For Production (Cloud)
```bash
# Production deployment
git clone <repo-url>
cd ai-voice-assistant
cp .env.production .env
# Edit .env with production values
docker-compose -f docker-compose.prod.yml up -d
python scripts/validate_system.py --output production_validation.json
```

---

## 📞 Support and Next Steps

### Getting Help
1. **Documentation**: Check `SYSTEM_DOCUMENTATION.md`
2. **Troubleshooting**: See `PRODUCTION_READINESS_CHECKLIST.md`
3. **Issues**: Create GitHub issues for bugs
4. **Community**: Join our Discord/Slack for support

### Recommended Learning Path
1. **Start Local**: Deploy on your PC first
2. **Test Features**: Make test calls, book appointments
3. **Scale Up**: Move to cloud when ready for production
4. **Monitor**: Set up monitoring and alerting
5. **Optimize**: Use performance tools to optimize

### Production Readiness
Before going live:
- [ ] Complete the Production Readiness Checklist
- [ ] Run load tests with expected traffic
- [ ] Set up monitoring and alerting
- [ ] Configure backup and disaster recovery
- [ ] Train your team on operations

---

**Need help?** The system includes comprehensive validation and monitoring tools to help you succeed. Start with local development and gradually scale up as your needs grow!