# AI Voice Assistant System Documentation

## Table of Contents

1. [System Overview](#system-overview)
2. [Architecture](#architecture)
3. [Services](#services)
4. [Deployment](#deployment)
5. [Configuration](#configuration)
6. [Monitoring](#monitoring)
7. [Troubleshooting](#troubleshooting)
8. [API Reference](#api-reference)
9. [Performance Optimization](#performance-optimization)
10. [Security](#security)

## System Overview

The AI Voice Assistant is a cloud-based microservices system that enables users to manage appointments through natural voice interactions. The system handles incoming calls via Twilio, processes speech using AI services, manages appointments through Google Calendar, and provides confirmations via SMS.

### Key Features

- **Voice-Based Appointment Management**: Book, reschedule, and cancel appointments using natural speech
- **Bilingual Support**: Full support for English and French languages
- **AI-Powered Processing**: Uses OpenAI GPT-4/5 for natural language understanding
- **Multiple TTS Providers**: ElevenLabs, Amazon Polly, and Google TTS support
- **Real-time Processing**: Streaming speech-to-text and text-to-speech
- **Scalable Architecture**: Microservices-based design for horizontal scaling
- **Comprehensive Monitoring**: Performance monitoring and error tracking

### System Requirements

**Performance Requirements:**
- STT processing: < 2 seconds
- TTS generation: < 3 seconds  
- Calendar availability check: < 5 seconds
- Complete appointment booking: < 30 seconds
- System uptime: 99.9%

**Scalability Requirements:**
- Support for 100+ concurrent calls
- Horizontal scaling of individual services
- Database connection pooling
- Caching for frequently accessed data

## Architecture

### High-Level Architecture

```
┌─────────────┐    ┌──────────────┐    ┌─────────────────┐
│   Caller    │───▶│ Twilio Voice │───▶│ Call Handler    │
└─────────────┘    └──────────────┘    │ Service         │
                                       └─────────┬───────┘
                                                 │
                   ┌─────────────────────────────┼─────────────────────────────┐
                   │                             │                             │
                   ▼                             ▼                             ▼
         ┌─────────────────┐           ┌─────────────────┐           ┌─────────────────┐
         │ Speech-to-Text  │           │ Text-to-Speech  │           │      NLU        │
         │    Service      │           │    Service      │           │    Service      │
         └─────────────────┘           └─────────────────┘           └─────────┬───────┘
                                                                               │
                                                                               ▼
                                                                     ┌─────────────────┐
                                                                     │  Appointment    │
                                                                     │    Service      │
                                                                     └─────────┬───────┘
                                                                               │
                                       ┌───────────────────────────────────────┼───────────────┐
                                       │                                       │               │
                                       ▼                                       ▼               ▼
                             ┌─────────────────┐                    ┌─────────────────┐ ┌─────────────┐
                             │ Google Calendar │                    │  SMS Service    │ │ Database    │
                             │      API        │                    │                 │ │             │
                             └─────────────────┘                    └─────────────────┘ └─────────────┘
```

### Microservices Architecture

The system consists of 6 main microservices:

1. **Call Handler Service** (Port 8001)
   - Orchestrates call flow and manages conversation state
   - Handles Twilio webhooks
   - Manages language detection and switching

2. **Speech-to-Text Service** (Port 8002)
   - Converts voice input to text using OpenAI Whisper or Google STT
   - Supports streaming transcription
   - Handles multiple languages

3. **Text-to-Speech Service** (Port 8003)
   - Converts text responses to speech
   - Multiple provider support (ElevenLabs, Polly, Google)
   - Optimized for telephony quality

4. **Natural Language Understanding Service** (Port 8004)
   - Processes text to extract intents and entities using GPT-4/5
   - Bilingual processing capabilities
   - Context-aware response generation

5. **Appointment Service** (Port 8005)
   - Manages calendar operations and business logic
   - Google Calendar API integration
   - Appointment conflict detection

6. **SMS Service** (Port 8006)
   - Handles notification delivery via Twilio SMS
   - Bilingual message templates
   - Delivery status tracking

### Data Flow

1. **Incoming Call**: Twilio receives call and sends webhook to Call Handler
2. **Speech Processing**: Audio is sent to STT service for transcription
3. **Intent Recognition**: Transcribed text is processed by NLU service
4. **Business Logic**: Appointment service handles calendar operations
5. **Response Generation**: TTS service generates audio response
6. **Confirmation**: SMS service sends confirmation message

## Services

### Call Handler Service

**Responsibilities:**
- Receive and manage Twilio webhook calls
- Orchestrate conversation flow
- Maintain call state and context
- Handle language detection and switching

**Key Endpoints:**
- `POST /webhook/voice` - Twilio voice webhook
- `POST /webhook/speech` - Speech recognition results
- `GET /health` - Health check

**Configuration:**
```yaml
CALL_HANDLER_PORT: 8001
TWILIO_ACCOUNT_SID: your_account_sid
TWILIO_AUTH_TOKEN: your_auth_token
TWILIO_PHONE_NUMBER: your_phone_number
```

### Speech-to-Text Service

**Responsibilities:**
- Convert audio streams to text
- Handle multiple languages (English/French)
- Provide confidence scores
- Stream processing for real-time conversion

**Key Endpoints:**
- `POST /stt/transcribe` - Single audio file transcription
- `POST /stt/stream` - Real-time streaming transcription
- `GET /health` - Health check

**Configuration:**
```yaml
STT_SERVICE_PORT: 8002
OPENAI_API_KEY: your_openai_key
GOOGLE_CREDENTIALS_PATH: path/to/credentials.json
```

### Text-to-Speech Service

**Responsibilities:**
- Convert text responses to natural speech
- Support multiple languages and voices
- Optimize for telephony audio quality
- Cache frequently used phrases

**Key Endpoints:**
- `POST /tts/synthesize` - Convert text to speech
- `GET /tts/voices` - List available voices
- `GET /health` - Health check

**Configuration:**
```yaml
TTS_SERVICE_PORT: 8003
ELEVENLABS_API_KEY: your_elevenlabs_key
AWS_ACCESS_KEY_ID: your_aws_key
AWS_SECRET_ACCESS_KEY: your_aws_secret
```

### Natural Language Understanding Service

**Responsibilities:**
- Extract intents from transcribed text
- Identify entities (dates, times, appointment details)
- Handle context and conversation history
- Support bilingual processing

**Key Endpoints:**
- `POST /nlu/analyze` - Analyze text for intent and entities
- `POST /nlu/generate-response` - Generate contextual responses
- `GET /health` - Health check

**Configuration:**
```yaml
NLU_SERVICE_PORT: 8004
OPENAI_API_KEY: your_openai_key
OPENAI_MODEL: gpt-4
```

### Appointment Service

**Responsibilities:**
- Interface with Google Calendar API
- Validate appointment requests
- Handle scheduling conflicts
- Manage appointment CRUD operations

**Key Endpoints:**
- `GET /appointments/availability` - Check time slot availability
- `POST /appointments` - Create new appointment
- `PUT /appointments/{id}` - Update existing appointment
- `DELETE /appointments/{id}` - Cancel appointment
- `GET /appointments/search` - Find appointments
- `GET /health` - Health check

**Configuration:**
```yaml
APPOINTMENT_SERVICE_PORT: 8005
GOOGLE_CREDENTIALS_PATH: path/to/credentials.json
GOOGLE_CALENDAR_ID: your_calendar_id
```

### SMS Service

**Responsibilities:**
- Send appointment confirmations and reminders
- Handle delivery status tracking
- Support bilingual messaging
- Manage message templates

**Key Endpoints:**
- `POST /sms/send` - Send SMS message
- `GET /sms/status/{message_id}` - Check delivery status
- `GET /health` - Health check

**Configuration:**
```yaml
SMS_SERVICE_PORT: 8006
TWILIO_ACCOUNT_SID: your_account_sid
TWILIO_AUTH_TOKEN: your_auth_token
```

## Deployment

### Docker Deployment

Each service is containerized and can be deployed using Docker:

```bash
# Build all services
make build

# Run with Docker Compose
docker-compose up -d

# Check service status
docker-compose ps
```

### Kubernetes Deployment

For production deployment, use Kubernetes:

```bash
# Deploy to Kubernetes
kubectl apply -f k8s/

# Check deployment status
kubectl get pods -n voice-assistant

# View logs
kubectl logs -f deployment/call-handler -n voice-assistant
```

### Environment Setup

1. **Development Environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   make dev-setup
   ```

2. **Production Environment:**
   ```bash
   # Set environment variables
   export ENVIRONMENT=production
   export DATABASE_URL=postgresql://user:pass@host:5432/db
   # ... other variables
   
   # Deploy
   make deploy-prod
   ```

## Configuration

### Environment Variables

**Database Configuration:**
```bash
DB_HOST=localhost
DB_PORT=5432
DB_NAME=voice_assistant
DB_USER=postgres
DB_PASSWORD=your_password
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

**Service Configuration:**
```bash
CALL_HANDLER_HOST=localhost
CALL_HANDLER_PORT=8001
STT_SERVICE_HOST=localhost
STT_SERVICE_PORT=8002
# ... other services
```

**External Services:**
```bash
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
OPENAI_API_KEY=your_openai_key
GOOGLE_CREDENTIALS_PATH=/path/to/credentials.json
```

**Performance Settings:**
```bash
REDIS_URL=redis://localhost:6379
CACHE_DEFAULT_TTL=3600
HTTP_MAX_CONNECTIONS=100
HTTP_TIMEOUT=30
```

### Configuration Management

The system uses a hierarchical configuration system:

1. **Default Values**: Built-in defaults in code
2. **Configuration Files**: JSON configuration files
3. **Environment Variables**: Override file settings
4. **Runtime Configuration**: Hot-reloadable settings

Example configuration file:
```json
{
  "environment": "production",
  "database": {
    "host": "db.example.com",
    "port": 5432,
    "pool_size": 20
  },
  "services": {
    "call_handler": {
      "port": 8001,
      "workers": 4
    }
  }
}
```

## Monitoring

### Health Checks

All services provide health check endpoints:

```bash
# Check individual service health
curl http://localhost:8001/health

# Check all services
make health-check
```

### Performance Monitoring

The system includes comprehensive performance monitoring:

**Metrics Collected:**
- Response times for all operations
- Request rates and error rates
- Database query performance
- Cache hit rates
- Resource usage (CPU, memory)

**Monitoring Tools:**
- Built-in performance monitor
- Prometheus metrics (optional)
- Grafana dashboards (optional)
- Custom monitoring dashboard

### Logging

Structured JSON logging with correlation IDs:

```json
{
  "timestamp": "2024-12-01T10:00:00Z",
  "level": "INFO",
  "service": "appointment_service",
  "correlation_id": "req_12345",
  "message": "Appointment booked successfully",
  "appointment_id": "apt_67890",
  "duration_ms": 150
}
```

**Log Levels:**
- `DEBUG`: Detailed debugging information
- `INFO`: General information messages
- `WARNING`: Warning messages
- `ERROR`: Error messages
- `CRITICAL`: Critical system errors

### Alerting

Configure alerts for:
- Service health check failures
- High error rates (>5%)
- Slow response times (>SLA thresholds)
- Database connection issues
- External service failures

## Troubleshooting

### Common Issues

**1. Service Not Responding**
```bash
# Check service status
kubectl get pods -n voice-assistant

# Check logs
kubectl logs -f deployment/service-name -n voice-assistant

# Check health endpoint
curl http://service-url/health
```

**2. Database Connection Issues**
```bash
# Check database connectivity
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME

# Check connection pool status
curl http://localhost:8001/admin/db-stats
```

**3. High Response Times**
```bash
# Check performance metrics
curl http://localhost:8001/admin/performance

# Check cache hit rates
curl http://localhost:8001/admin/cache-stats

# Run database optimization
python scripts/optimize_database.py
```

**4. External Service Failures**
```bash
# Check Twilio service status
curl https://status.twilio.com/

# Check OpenAI service status
curl https://status.openai.com/

# Check Google Calendar API
curl "https://www.googleapis.com/calendar/v3/calendars/primary" \
  -H "Authorization: Bearer $ACCESS_TOKEN"
```

### Performance Troubleshooting

**Slow STT Processing:**
- Check OpenAI API rate limits
- Verify audio quality and format
- Monitor network latency

**Slow Database Queries:**
- Run `EXPLAIN ANALYZE` on slow queries
- Check index usage
- Monitor connection pool utilization

**High Memory Usage:**
- Check for memory leaks in services
- Monitor cache size and eviction
- Review connection pool settings

### Error Codes

**System Error Codes:**
- `SYS_001`: Database connection failure
- `SYS_002`: External service timeout
- `SYS_003`: Configuration error
- `SYS_004`: Authentication failure

**Business Logic Error Codes:**
- `BIZ_001`: Appointment conflict
- `BIZ_002`: Invalid time slot
- `BIZ_003`: Calendar unavailable
- `BIZ_004`: SMS delivery failure

## API Reference

### Call Handler Service API

**POST /webhook/voice**
Handle incoming Twilio voice webhook.

Request:
```json
{
  "CallSid": "CA1234567890",
  "From": "+1234567890",
  "To": "+0987654321"
}
```

Response:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Say>Hello, how can I help you today?</Say>
  <Record action="/webhook/speech" />
</Response>
```

### Appointment Service API

**GET /appointments/availability**
Check time slot availability.

Parameters:
- `start_time`: ISO 8601 datetime
- `duration`: Duration in minutes

Response:
```json
{
  "available": true,
  "requested_time": "2024-12-01T14:00:00Z",
  "duration_minutes": 60,
  "alternative_times": [
    "2024-12-01T15:00:00Z",
    "2024-12-01T16:00:00Z"
  ]
}
```

**POST /appointments**
Create new appointment.

Request:
```json
{
  "title": "Doctor Appointment",
  "start_time": "2024-12-01T14:00:00Z",
  "end_time": "2024-12-01T15:00:00Z",
  "attendee_phone": "+1234567890",
  "attendee_name": "John Doe",
  "description": "Regular checkup",
  "language": "en"
}
```

Response:
```json
{
  "success": true,
  "appointment": {
    "id": "apt_12345",
    "title": "Doctor Appointment",
    "start_time": "2024-12-01T14:00:00Z",
    "end_time": "2024-12-01T15:00:00Z",
    "status": "confirmed",
    "google_calendar_event_id": "event_67890"
  }
}
```

## Performance Optimization

### Caching Strategy

**Cache Layers:**
1. **Application Cache**: In-memory caching for frequently accessed data
2. **Redis Cache**: Distributed caching for session data and API responses
3. **Database Query Cache**: Query result caching
4. **TTS Audio Cache**: Cached audio for common phrases

**Cache Configuration:**
```python
# Cache TTL settings
CACHE_TTL_SESSION = 1800  # 30 minutes
CACHE_TTL_APPOINTMENT = 300  # 5 minutes
CACHE_TTL_TTS_AUDIO = 86400  # 24 hours
CACHE_TTL_AVAILABILITY = 60  # 1 minute
```

### Database Optimization

**Indexes Created:**
- `idx_appointments_phone_start_time`: Optimize appointment search
- `idx_call_sessions_phone_activity`: Optimize session lookup
- `idx_call_logs_timestamp_event`: Optimize log queries

**Query Optimization:**
- Use prepared statements
- Implement query result caching
- Optimize JOIN operations
- Regular VACUUM and ANALYZE

### Connection Pooling

**Database Pool Settings:**
```python
DB_POOL_SIZE = 10
DB_MAX_OVERFLOW = 20
DB_POOL_TIMEOUT = 30
DB_POOL_RECYCLE = 3600
```

**HTTP Pool Settings:**
```python
HTTP_MAX_CONNECTIONS = 100
HTTP_MAX_KEEPALIVE = 20
HTTP_KEEPALIVE_EXPIRY = 30
```

### Load Testing

Run comprehensive load tests:

```bash
# Run load tests
python scripts/load_test.py --concurrent 10 --requests 100

# Run quick tests
python scripts/load_test.py --quick

# Test specific service
python scripts/load_test.py --service appointment
```

## Security

### Authentication & Authorization

**Service-to-Service Authentication:**
- API key-based authentication
- JWT tokens for session management
- Rate limiting per service

**External Service Security:**
- Secure credential storage
- API key rotation
- OAuth 2.0 for Google services

### Data Protection

**Encryption:**
- TLS 1.3 for all HTTP communications
- Database encryption at rest
- Encrypted configuration secrets

**PII Handling:**
- Phone numbers hashed in logs
- Personal data encrypted in database
- GDPR compliance measures

### Security Headers

```http
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'
X-Frame-Options: DENY
X-Content-Type-Options: nosniff
X-XSS-Protection: 1; mode=block
```

### Rate Limiting

```python
# Rate limits per service
RATE_LIMIT_CALLS_PER_MINUTE = 60
RATE_LIMIT_SMS_PER_HOUR = 100
RATE_LIMIT_API_PER_MINUTE = 1000
```

---

**Document Version**: 1.0  
**Last Updated**: December 2024  
**Next Review**: March 2025