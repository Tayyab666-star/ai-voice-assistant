# 🎙️ AI Voice Assistant

> **Complete microservices system for appointment booking via voice calls**  
> Supports both **local free deployment** ($0 cost) and **cloud production** deployment

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-Ready-blue.svg)](https://kubernetes.io/)
[![Python](https://img.shields.io/badge/Python-3.9+-green.svg)](https://www.python.org/)

---

## 🌟 **Features**

- 🎯 **Voice-Based Appointment Management** - Book, reschedule, cancel appointments using natural speech
- 🌍 **Bilingual Support** - Full English and French language support
- 🤖 **AI-Powered** - Uses OpenAI GPT-4/Whisper or local AI models
- 🏗️ **Microservices Architecture** - 6 independent, scalable services
- 💰 **$0 Local Version** - Run completely free with local AI models
- ☁️ **Cloud Ready** - Production deployment with APIs
- 📱 **Multi-Channel** - Phone calls, web interface, SMS confirmations
- 🔒 **Privacy First** - Local deployment keeps all data on your machine

---

## 🚀 **Quick Start**

### **Option 1: Local Free Version ($0 cost)**
```bash
# Windows
start-local-free.bat

# Mac/Linux  
./start-local-free.sh

# Then open: http://localhost:3000
```

### **Option 2: Cloud Version (with APIs)**
```bash
# Windows
quick-start.bat

# Mac/Linux
./quick-start.sh
```

---

## 🏗️ **System Architecture**

```mermaid
graph TB
    A[Caller] --> B[Twilio Voice]
    B --> C[Call Handler Service]
    C --> D[Speech-to-Text Service]
    C --> E[Text-to-Speech Service]
    D --> F[NLU Service]
    F --> G[Appointment Service]
    G --> H[Google Calendar API]
    G --> I[SMS Service]
    I --> J[Twilio SMS API]
```

### **Microservices:**
- **Call Handler** (Port 8001) - Orchestrates conversation flow
- **Speech-to-Text** (Port 8002) - Converts voice to text
- **Text-to-Speech** (Port 8003) - Converts text to voice
- **NLU Service** (Port 8004) - Understands user intent
- **Appointment Service** (Port 8005) - Manages calendar operations
- **SMS Service** (Port 8006) - Sends confirmations

---

## 💻 **Deployment Options**

| Option | Cost | Setup Time | Use Case |
|--------|------|------------|----------|
| **Local Free** | $0/month | 5 minutes | Learning, Development |
| **Cloud APIs** | $10-50/month | 5 minutes | Small Business |
| **Enterprise** | $500+/month | 1 hour | Large Scale |

### **Local Free Version:**
- ✅ OpenAI Whisper (local STT)
- ✅ Coqui TTS (local voice generation)
- ✅ spaCy NLU (local language understanding)
- ✅ Web interface for testing
- ✅ Complete privacy

### **Cloud Version:**
- ✅ OpenAI GPT-4 + Whisper APIs
- ✅ Twilio Voice + SMS
- ✅ ElevenLabs/Polly TTS
- ✅ Real phone call handling
- ✅ Production scalability

---

## 📋 **Requirements**

### **Local Free Version:**
- **OS**: Windows 10+, macOS 10.15+, or Linux
- **CPU**: 4+ cores
- **RAM**: 8 GB minimum (16 GB recommended)
- **Storage**: 15 GB free space
- **Software**: Docker Desktop

### **Cloud Version:**
- **APIs**: OpenAI API key, Twilio account
- **Optional**: Google Calendar, ElevenLabs
- **Infrastructure**: Any cloud provider or VPS

---

## 🛠️ **Installation**

### **Prerequisites:**
1. **Install Docker Desktop**
   - Windows/Mac: https://www.docker.com/products/docker-desktop
   - Linux: `curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh`

2. **Clone Repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/ai-voice-assistant.git
   cd ai-voice-assistant
   ```

### **Local Free Setup:**
```bash
# Windows
start-local-free.bat

# Mac/Linux
chmod +x start-local-free.sh
./start-local-free.sh
```

### **Cloud Setup:**
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your API keys
# OPENAI_API_KEY=your_key_here
# TWILIO_ACCOUNT_SID=your_sid_here
# TWILIO_AUTH_TOKEN=your_token_here

# Start services
docker-compose up -d
```

---

## 🎯 **Usage Examples**

### **Web Interface (Local Free):**
1. Open http://localhost:3000
2. Click "Start Call"
3. Type: "I want to book an appointment for tomorrow at 2 PM"
4. Follow the conversation flow

### **Phone Calls (Cloud Version):**
1. Configure Twilio webhook: `https://your-domain.com/webhook/voice`
2. Call your Twilio number
3. Speak naturally: "Book me an appointment for next Monday at 10 AM"

### **Supported Commands:**
- "Book an appointment for [date] at [time]"
- "Reschedule my appointment to [new date/time]"
- "Cancel my appointment"
- "What appointments do I have?"

---

## 🔧 **Configuration**

### **Environment Variables:**
```bash
# AI Services
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-4

# Communication
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=your_phone_number

# Calendar Integration
GOOGLE_CREDENTIALS_PATH=path/to/credentials.json
GOOGLE_CALENDAR_ID=your_calendar_id

# Database
DATABASE_URL=postgresql://user:pass@host:5432/db
```

### **Service Configuration:**
Each service can be configured independently through environment variables or configuration files.

---

## 📊 **Performance**

### **Response Times:**
- **STT Processing**: < 2 seconds
- **NLU Analysis**: < 1 second  
- **TTS Generation**: < 3 seconds
- **Calendar Operations**: < 5 seconds
- **End-to-End Booking**: < 30 seconds

### **Scalability:**
- **Local**: 1-5 concurrent calls
- **Cloud**: 100+ concurrent calls
- **Enterprise**: Unlimited with proper infrastructure

---

## 🧪 **Testing**

### **Run Tests:**
```bash
# Unit tests
python -m pytest tests/unit/

# Integration tests
python -m pytest tests/integration/

# Load testing
python scripts/load_test.py --concurrent 10 --requests 100

# System validation
python scripts/validate_system.py
```

### **Manual Testing:**
```bash
# Health checks
curl http://localhost:8001/health  # Call Handler
curl http://localhost:8005/health  # Appointment Service

# Test appointment booking
curl -X POST http://localhost:8005/appointments \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","start_time":"2024-12-01T14:00:00Z",...}'
```

---

## 🚀 **Deployment**

### **Local Development:**
```bash
docker-compose up -d
```

### **Production (Docker):**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### **Kubernetes:**
```bash
kubectl apply -f k8s/
```

### **Cloud Providers:**
- **AWS**: Use ECS or EKS
- **Google Cloud**: Use Cloud Run or GKE  
- **Azure**: Use Container Instances or AKS
- **DigitalOcean**: Use App Platform or Kubernetes

---

## 📚 **Documentation**

- 📖 [System Documentation](SYSTEM_DOCUMENTATION.md) - Complete technical docs
- 🚀 [Deployment Guide](DEPLOYMENT_OPTIONS_AND_REQUIREMENTS.md) - All deployment options
- ✅ [Production Checklist](PRODUCTION_READINESS_CHECKLIST.md) - Go-live checklist
- 🆓 [Local Free Setup](README_LOCAL_FREE.md) - $0 cost version guide
- 🔧 [GitHub Setup](GITHUB_SETUP_GUIDE.md) - How to fork and customize

---

## 🤝 **Contributing**

We welcome contributions! Here's how to get started:

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Make changes and test**
4. **Commit**: `git commit -m 'Add amazing feature'`
5. **Push**: `git push origin feature/amazing-feature`
6. **Create Pull Request**

### **Development Setup:**
```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/ai-voice-assistant.git

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements-dev.txt

# Run in development mode
docker-compose -f docker-compose.dev.yml up -d
```

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 **Support**

- 📖 **Documentation**: Check the docs folder
- 🐛 **Issues**: Create a GitHub issue
- 💬 **Discussions**: Use GitHub Discussions
- 📧 **Email**: [your-email@example.com]

---

## 🙏 **Acknowledgments**

- **OpenAI** for GPT-4 and Whisper APIs
- **Twilio** for voice and SMS services
- **Coqui** for open-source TTS
- **spaCy** for NLP capabilities
- **Docker** and **Kubernetes** communities

---

## 🎯 **Roadmap**

- [ ] **Multi-language support** (Spanish, German, etc.)
- [ ] **Video call integration**
- [ ] **Advanced analytics dashboard**
- [ ] **Mobile app companion**
- [ ] **Integration with more calendar providers**
- [ ] **Voice biometric authentication**

---

**⭐ If this project helps you, please give it a star on GitHub!**

**🚀 Ready to build amazing voice-powered applications? Get started now!**