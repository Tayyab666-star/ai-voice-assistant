#!/bin/bash

# AI Voice Assistant - Quick Start Script
# This script helps you get the system running quickly on your local machine

set -e

echo "🎙️  AI Voice Assistant - Quick Start Setup"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker Desktop first:"
    echo "   https://www.docker.com/products/docker-desktop"
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not available. Please install Docker Compose."
    exit 1
fi

echo "✅ Docker is installed and running"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating environment configuration..."
    cp .env.example .env
    echo "⚠️  IMPORTANT: Please edit .env file with your API keys before continuing"
    echo "   Required: OPENAI_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN"
    echo ""
    read -p "Press Enter after you've updated the .env file..."
fi

echo "🚀 Starting AI Voice Assistant services..."
docker-compose up -d

echo "⏳ Waiting for services to start..."
sleep 30

echo "🔍 Validating system..."
if command -v python3 &> /dev/null; then
    python3 scripts/validate_system.py
else
    echo "⚠️  Python3 not found. Skipping validation."
fi

echo ""
echo "🎉 Setup complete! Your AI Voice Assistant is running:"
echo "   Call Handler:      http://localhost:8001/health"
echo "   STT Service:       http://localhost:8002/health"
echo "   TTS Service:       http://localhost:8003/health"
echo "   NLU Service:       http://localhost:8004/health"
echo "   Appointment Service: http://localhost:8005/health"
echo "   SMS Service:       http://localhost:8006/health"
echo ""
echo "📚 Next steps:"
echo "   1. Configure your Twilio webhook URL"
echo "   2. Test the system with a phone call"
echo "   3. Check logs: docker-compose logs -f"
echo "   4. Stop services: docker-compose down"