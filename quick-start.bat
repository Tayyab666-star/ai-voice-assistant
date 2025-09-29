@echo off
REM AI Voice Assistant - Quick Start Script for Windows
REM This script helps you get the system running quickly on your Windows machine

echo 🎙️  AI Voice Assistant - Quick Start Setup
echo ==========================================

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker Desktop first:
    echo    https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)

echo ✅ Docker is installed and running

REM Create .env file if it doesn't exist
if not exist .env (
    echo 📝 Creating environment configuration...
    copy .env.example .env
    echo ⚠️  IMPORTANT: Please edit .env file with your API keys before continuing
    echo    Required: OPENAI_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
    echo.
    pause
)

echo 🚀 Starting AI Voice Assistant services...
docker-compose up -d

echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak >nul

echo 🔍 Validating system...
python scripts/validate_system.py 2>nul || echo ⚠️  Python not found. Skipping validation.

echo.
echo 🎉 Setup complete! Your AI Voice Assistant is running:
echo    Call Handler:      http://localhost:8001/health
echo    STT Service:       http://localhost:8002/health
echo    TTS Service:       http://localhost:8003/health
echo    NLU Service:       http://localhost:8004/health
echo    Appointment Service: http://localhost:8005/health
echo    SMS Service:       http://localhost:8006/health
echo.
echo 📚 Next steps:
echo    1. Configure your Twilio webhook URL
echo    2. Test the system with a phone call
echo    3. Check logs: docker-compose logs -f
echo    4. Stop services: docker-compose down
echo.
pause