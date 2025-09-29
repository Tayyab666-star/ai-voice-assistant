@echo off
REM AI Voice Assistant - Local Free Setup for Windows
REM Runs completely free with local AI models

echo.
echo 🎙️  AI Voice Assistant - Local Free Setup
echo ==========================================
echo 💰 Cost: $0 - Runs completely free on your PC
echo 🤖 Uses: Local AI models (no external APIs)
echo 🌐 Interface: Web browser (no phone needed)
echo.

REM Check if Docker is running
echo 🔍 Checking Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed or not running
    echo.
    echo Please install Docker Desktop from:
    echo https://www.docker.com/products/docker-desktop
    echo.
    echo After installation:
    echo 1. Restart your computer
    echo 2. Start Docker Desktop
    echo 3. Run this script again
    echo.
    pause
    exit /b 1
)

echo ✅ Docker is ready

REM Create free local configuration
echo.
echo 📝 Setting up free local configuration...
if not exist .env (
    copy .env.local-free .env >nul
    echo ✅ Created local configuration
) else (
    echo ✅ Configuration already exists
)

REM Create necessary directories
if not exist models mkdir models
if not exist data mkdir data
if not exist logs mkdir logs
echo ✅ Created directories

REM Check available RAM
echo.
echo 🔍 Checking your PC specifications...
for /f "tokens=2 delims==" %%i in ('wmic computersystem get TotalPhysicalMemory /value ^| find "="') do set ram=%%i
set /a ram_gb=%ram:~0,-9%
echo 💾 Available RAM: %ram_gb% GB

if %ram_gb% LSS 8 (
    echo ⚠️  Warning: You have less than 8GB RAM
    echo    The system will work but may be slower
    echo    Consider closing other applications
) else (
    echo ✅ RAM is sufficient for good performance
)

REM Check available disk space
for /f "tokens=3" %%i in ('dir /-c ^| find "bytes free"') do set free_space=%%i
set /a free_gb=%free_space:~0,-10%
echo 💽 Free disk space: %free_gb% GB

if %free_gb% LSS 15 (
    echo ❌ Error: Need at least 15GB free space
    echo    Please free up some disk space and try again
    pause
    exit /b 1
) else (
    echo ✅ Disk space is sufficient
)

echo.
echo 🚀 Starting AI Voice Assistant (Local Free Version)...
echo ⏳ This may take 5-10 minutes on first run (downloading models)
echo.

REM Start the local free version
docker-compose -f docker-compose.local-free.yml up -d

echo.
echo ⏳ Waiting for services to initialize...
echo    (AI models are loading in the background)
timeout /t 60 /nobreak >nul

REM Check if services are running
echo.
echo 🔍 Checking services...

curl -f -s "http://localhost:3000" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Web interface is ready
) else (
    echo ⏳ Web interface is still starting...
)

curl -f -s "http://localhost:8005/health" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Appointment service is ready
) else (
    echo ⏳ Appointment service is still starting...
)

echo.
echo 🎉 Setup Complete! Your AI Voice Assistant is running locally!
echo.
echo 🌐 Access Your AI Assistant:
echo    👉 Open your browser and go to: http://localhost:3000
echo.
echo 📱 How to Use:
echo    1. Click "Start Call" to begin
echo    2. Type what you would say (instead of speaking)
echo    3. Try: "I want to book an appointment for tomorrow at 2 PM"
echo    4. Try: "Reschedule my appointment to next Monday"
echo    5. Try: "Cancel my appointment"
echo.
echo 🤖 What's Running (All Free):
echo    • Local Whisper AI for speech recognition
echo    • Local Coqui TTS for voice generation  
echo    • Local spaCy for language understanding
echo    • PostgreSQL database for appointments
echo    • Web interface for easy testing
echo.
echo 🛠️  Useful Commands:
echo    • View logs: docker-compose -f docker-compose.local-free.yml logs -f
echo    • Stop system: docker-compose -f docker-compose.local-free.yml down
echo    • Restart: docker-compose -f docker-compose.local-free.yml restart
echo.
echo 💡 Tips:
echo    • Keep Docker Desktop running
echo    • First AI responses may be slower (models loading)
echo    • Close other heavy applications for better performance
echo    • System runs completely offline after initial setup
echo.
echo 🎯 This version costs $0 and runs entirely on your PC!
echo.
start http://localhost:3000
pause