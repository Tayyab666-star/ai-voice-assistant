#!/bin/bash

# AI Voice Assistant - Demo Mode Startup Script
# Starts the system in complete demo mode (no external APIs required)

set -e

echo "🎙️  AI Voice Assistant - Demo Mode"
echo "=================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Create demo environment file
if [ ! -f .env ]; then
    echo "📝 Creating demo environment configuration..."
    cp .env.demo .env
    echo "✅ Demo configuration created"
else
    echo "✅ Environment configuration exists"
fi

# Create models directory
mkdir -p models
echo "✅ Models directory ready"

echo ""
echo "🚀 Starting AI Voice Assistant in Demo Mode..."
echo "This may take a few minutes on first run..."
echo ""

# Start services
docker-compose -f docker-compose.demo.yml up -d

echo ""
echo "⏳ Waiting for services to start..."
sleep 30

# Check service health
echo "🔍 Checking service health..."

services=("web-interface:3000" "call-handler:8001" "appointment-service:8005")
all_healthy=true

for service in "${services[@]}"; do
    name=$(echo $service | cut -d: -f1)
    port=$(echo $service | cut -d: -f2)
    
    if curl -f -s "http://localhost:$port/health" > /dev/null 2>&1 || curl -f -s "http://localhost:$port" > /dev/null 2>&1; then
        echo "✅ $name is healthy"
    else
        echo "⚠️  $name is not responding"
        all_healthy=false
    fi
done

echo ""
if [ "$all_healthy" = true ]; then
    echo "🎉 Demo setup complete!"
else
    echo "⚠️  Some services may still be starting. Please wait a moment and try accessing the web interface."
fi

echo ""
echo "🌐 Access the Demo Interface:"
echo "   Open your browser and go to: http://localhost:3000"
echo ""
echo "📚 What you can do:"
echo "   • Click 'Start Call' to simulate a phone call"
echo "   • Type messages instead of speaking"
echo "   • Try: 'I want to book an appointment for tomorrow at 2 PM'"
echo "   • Try: 'I need to reschedule my appointment'"
echo "   • Try: 'Cancel my appointment'"
echo ""
echo "🛠️  Useful commands:"
echo "   • View logs: docker-compose -f docker-compose.demo.yml logs -f"
echo "   • Stop demo: docker-compose -f docker-compose.demo.yml down"
echo "   • Restart: docker-compose -f docker-compose.demo.yml restart"
echo ""
echo "🎯 This demo runs completely offline with no API costs!"
echo "   Perfect for learning how the system works."