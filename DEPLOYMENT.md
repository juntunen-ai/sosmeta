# Setup and Deployment Guide

## OpenAI Action for Finnish Social Services Schemas

This guide will help you deploy and configure the Finnish Social Services Schema API as an OpenAI action.

## Prerequisites

1. **Server Infrastructure**: Cloud hosting (AWS, Google Cloud, Azure, or similar)
2. **Domain**: Public domain with SSL certificate
3. **OpenAI Account**: With custom actions capability
4. **Python Environment**: Python 3.8+ with Flask

## Deployment Steps

### 1. Server Setup

```bash
# Clone your repository
git clone https://github.com/juntunen-ai/sosmeta.git
cd sosmeta

# Install dependencies
pip install flask jsonschema python-dotenv gunicorn

# Set up environment variables
echo "API_KEY=your-secret-api-key" > .env
echo "FLASK_ENV=production" >> .env
```

### 2. Deploy to Production

#### Option A: Using Heroku
```bash
# Install Heroku CLI and login
heroku login

# Create app
heroku create sosmeta-api

# Set environment variables
heroku config:set API_KEY=your-secret-api-key

# Deploy
git push heroku main
```

#### Option B: Using Google Cloud Run
```bash
# Build container
docker build -t gcr.io/your-project/sosmeta-api .

# Deploy
gcloud run deploy sosmeta-api \
  --image gcr.io/your-project/sosmeta-api \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Option C: Using AWS EC2
```bash
# Copy files to server
scp -r * ubuntu@your-server:/home/ubuntu/sosmeta/

# SSH to server
ssh ubuntu@your-server

# Install and run
cd sosmeta
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:8000 server_example:app
```

### 3. Configure OpenAI Action

1. **Go to OpenAI Platform**: https://platform.openai.com/
2. **Navigate to Actions**: Find the Actions section in your account
3. **Create New Action**: Click "Create Action"
4. **Import Schema**: Upload `openai-action-config.json`
5. **Set Server URL**: Update to your deployed server URL
6. **Configure Authentication**: Set up API key authentication
7. **Test Action**: Use the testing interface to verify functionality

### 4. Authentication Setup

Update your server to require API key authentication:

```python
from functools import wraps
from flask import request, jsonify
import os

def require_api_key(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('Authorization')
        if not api_key or api_key != f"Bearer {os.getenv('API_KEY')}":
            return jsonify({'error': 'Invalid API key'}), 401
        return f(*args, **kwargs)
    return decorated_function

# Add to all routes
@app.route('/api/v1/schemas', methods=['GET'])
@require_api_key
def list_schemas():
    # ... existing code
```

### 5. Update OpenAI Action Configuration

```json
{
  "auth": {
    "type": "service_http",
    "authorization_type": "bearer",
    "verification_tokens": {
      "openai": "your-verification-token"
    }
  }
}
```

## Configuration Files

### requirements.txt
```
Flask==2.3.3
jsonschema==4.19.0
python-dotenv==1.0.0
gunicorn==21.2.0
```

### Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "server_example:app"]
```

### docker-compose.yml
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_KEY=${API_KEY}
      - FLASK_ENV=production
    volumes:
      - ./Valmis:/app/Valmis:ro
```

## Environment Variables

Required environment variables:

```bash
API_KEY=your-secret-api-key-here
FLASK_ENV=production
CORS_ORIGINS=https://chat.openai.com
LOG_LEVEL=INFO
```

## Security Considerations

1. **API Key Security**: Use strong, randomly generated API keys
2. **CORS Configuration**: Restrict origins to OpenAI domains
3. **Rate Limiting**: Implement rate limiting per IP/key
4. **Input Validation**: Validate all input parameters
5. **Error Handling**: Don't expose internal errors to users

### Rate Limiting Example
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per hour"]
)

@app.route('/api/v1/schemas')
@limiter.limit("10 per minute")
def list_schemas():
    # ... existing code
```

## Monitoring and Logging

### Add logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

@app.before_request
def log_request():
    app.logger.info(f"{request.method} {request.path} from {request.remote_addr}")
```

### Health check endpoint
```python
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'schemas_loaded': len(schemas_cache),
        'timestamp': datetime.utcnow().isoformat()
    })
```

## Testing

### Test the API locally
```bash
# Start local server
python server_example.py

# Test endpoints
curl http://localhost:5000/api/v1/schemas
curl http://localhost:5000/health
```

### Test with OpenAI
1. Configure the action with your local server (use ngrok for testing)
2. Test each endpoint through the OpenAI interface
3. Verify responses match expected format

## Troubleshooting

### Common Issues

1. **Schema Loading Errors**
   - Ensure Valmis folder is accessible
   - Check file permissions
   - Verify JSON format

2. **Authentication Failures**
   - Verify API key configuration
   - Check OpenAI action auth settings
   - Confirm header format

3. **CORS Errors**
   - Add proper CORS headers
   - Configure allowed origins
   - Check preflight requests

### Debug Mode
```python
# Enable debug mode for development
app.run(debug=True, port=5000)

# Add debug logging
app.logger.setLevel(logging.DEBUG)
```

## Maintenance

### Schema Updates
```bash
# Update schemas
git pull origin main

# Restart service
sudo systemctl restart sosmeta-api
```

### Backup
```bash
# Backup schema files
tar -czf schemas-backup-$(date +%Y%m%d).tar.gz Valmis/
```

## Support

For issues or questions:
- Check logs: `tail -f /var/log/sosmeta-api.log`
- Monitor health: `curl https://your-domain.com/health`
- Contact: your-support-email@domain.com

---

*This setup provides a production-ready API for the Finnish Social Services Schema OpenAI action with proper security, monitoring, and deployment procedures.*
