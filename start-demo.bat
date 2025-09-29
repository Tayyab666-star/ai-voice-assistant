@echo off
REM AI Voice Assistant - Demo Mode Startup Script for Windows
REM Starts the system in complete demo mode (no external APIs required)

echo 🎙️  AI Voice Assistant - Demo Mode
echo ==================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not running. Please start Docker Desktop first.
    pause
    exit /b 1
)

echo ✅ Docker is running

REM Create demo environment file
if not exist .env (
    echo 📝 Creating demo environment configuration...
    copy .env.demo .env >nul
    echo ✅ Demo configuration created
) else (
    echo ✅ Environment configuration exists
)

REM Create models directory
if not exist models mkdir models
echo ✅ Models directory ready

echo.
echo 🚀 Starting AI Voice Assistant in Demo Mode...
echo This may take a few minutes on first run...
echo.

REM Start services
docker-compose -f docker-compose.demo.yml up -d

echo.
echo ⏳ Waiting for services to start...
timeout /t 30 /nobreak >nul

echo 🔍 Checking service health...

REM Check web interface
curl -f -s "http://localhost:3000" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Web interface is healthy
) else (
    echo ⚠️  Web interface is starting...
)

REM Check appointment service
curl -f -s "http://localhost:8005/health" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Appointment service is healthy
) else (
    echo ⚠️  Appointment service is starting...
)

echo.
echo 🎉 Demo setup complete!
echo.
echo 🌐 Access the Demo Interface:
echo    Open your browser and go to: http://localhost:3000
echo.
echo 📚 What you can do:
echo    • Click 'Start Call' to simulate a phone call
echo    • Type messages instead of speaking
echo    • Try: 'I want to book an appointment for tomorrow at 2 PM'
echo    • Try: 'I need to reschedule my appointment'
echo    • Try: 'Cancel my appointment'
echo.
echo 🛠️  Useful commands:
echo    • View logs: docker-compose -f docker-compose.demo.yml logs -f
echo    • Stop demo: docker-compose -f docker-compose.demo.yml down
echo    • Restart: docker-compose -f docker-compose.demo.yml restart
echo.
echo 🎯 This demo runs completely offline with no API costs!
echo    Perfect for learning how the system works.
echo.
pause