# Deployment Guide - CSV Processor

This guide explains how to deploy the CSV Processor application on different systems and environments.

## 🚀 Quick Deployment Options

### Option 1: One-Click Installation (Easiest)

1. **Download the project** to your computer
2. **Open terminal/command prompt** in the `backend` folder
3. **Run the installer**:
   ```bash
   python install.py
   ```
4. **Start the application**:
   - **Windows**: Double-click `run.bat`
   - **Linux/macOS**: Run `./run.sh`

### Option 2: Manual Setup

1. **Install Python 3.8+** on your system
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Start the server**:
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Option 3: Docker Deployment (Recommended for Production)

1. **Install Docker** on your system
2. **Build and run**:
   ```bash
   docker build -t csv-processor .
   docker run -p 8000:8000 csv-processor
   ```

### Option 4: Docker Compose (Best for Development)

1. **Install Docker Compose**
2. **Run**:
   ```bash
   docker-compose up
   ```

## 🌐 Network Deployment

### Making it Accessible on Your Network

To allow other computers on your network to access the application:

1. **Start the server with network access**:
   ```bash
   python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Find your computer's IP address**:
   - **Windows**: Run `ipconfig` and look for "IPv4 Address"
   - **macOS/Linux**: Run `ifconfig` or `ip addr show`

3. **Access from other computers**:
   - Use `http://YOUR_IP_ADDRESS:8000` (e.g., `http://192.168.1.100:8000`)

### Firewall Configuration

You may need to configure your firewall to allow connections on port 8000:

#### Windows:
1. Open Windows Defender Firewall
2. Click "Allow an app or feature through Windows Defender Firewall"
3. Add Python or allow port 8000

#### macOS:
```bash
sudo pfctl -f /etc/pf.conf
```

#### Linux (Ubuntu):
```bash
sudo ufw allow 8000
```

## 🏢 Production Deployment

### Using a Reverse Proxy (Nginx)

1. **Install Nginx**
2. **Create configuration file** `/etc/nginx/sites-available/csv-processor`:
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```
3. **Enable the site**:
   ```bash
   sudo ln -s /etc/nginx/sites-available/csv-processor /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl reload nginx
   ```

### Using PM2 (Process Manager)

1. **Install PM2**:
   ```bash
   npm install -g pm2
   ```

2. **Create ecosystem file** `ecosystem.config.js`:
   ```javascript
   module.exports = {
     apps: [{
       name: 'csv-processor',
       script: 'python',
       args: '-m uvicorn main:app --host 0.0.0.0 --port 8000',
       cwd: '/path/to/your/app',
       instances: 1,
       autorestart: true,
       watch: false,
       max_memory_restart: '1G',
       env: {
         NODE_ENV: 'production'
       }
     }]
   }
   ```

3. **Start with PM2**:
   ```bash
   pm2 start ecosystem.config.js
   pm2 save
   pm2 startup
   ```

## ☁️ Cloud Deployment

### Heroku

1. **Create `Procfile`**:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. **Deploy**:
   ```bash
   git add .
   git commit -m "Deploy CSV Processor"
   git push heroku main
   ```

### AWS EC2

1. **Launch EC2 instance** (Ubuntu recommended)
2. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip nginx
   ```
3. **Deploy application** and configure Nginx as above

### DigitalOcean App Platform

1. **Create `app.yaml`**:
   ```yaml
   name: csv-processor
   services:
   - name: web
     source_dir: /backend
     github:
       repo: your-username/your-repo
       branch: main
     run_command: uvicorn main:app --host 0.0.0.0 --port 8080
     http_port: 8080
     instance_count: 1
     instance_size_slug: basic-xxs
   ```

## 🔧 Configuration Options

### Environment Variables

Create a `.env` file for configuration:

```env
# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=True

# File Upload Limits
MAX_FILE_SIZE=10485760  # 10MB
ALLOWED_EXTENSIONS=.csv
```

### Custom Port

To run on a different port:

```bash
python -m uvicorn main:app --reload --host 0.0.0.0 --port 3000
```

### SSL/HTTPS Setup

For production, use a reverse proxy like Nginx with SSL certificates from Let's Encrypt.

## 📱 Mobile Access

The web interface is fully responsive and works on mobile devices. Users can:

- Upload CSV files from their mobile device
- Process data on the go
- Download filtered results

## 🔒 Security Considerations

### For Production Use:

1. **Use HTTPS** in production
2. **Implement authentication** if needed
3. **Set file upload limits**
4. **Use environment variables** for sensitive data
5. **Regular security updates**

### Basic Security Setup:

```python
# Add to main.py
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware, 
    allowed_hosts=["yourdomain.com", "*.yourdomain.com"]
)
```

## 🐛 Troubleshooting

### Common Issues:

1. **Port already in use**:
   ```bash
   # Find process using port 8000
   lsof -i :8000
   # Kill the process
   kill -9 PID
   ```

2. **Permission denied**:
   ```bash
   # Make scripts executable
   chmod +x start.sh run.sh
   ```

3. **Dependencies not found**:
   ```bash
   # Use virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # or
   venv\Scripts\activate  # Windows
   pip install -r requirements.txt
   ```

## 📊 Monitoring

### Health Checks

The application includes health check endpoints:

- `GET /` - Main interface
- `GET /docs` - API documentation (FastAPI auto-generated)

### Logging

For production, configure proper logging:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
```

## 🚀 Performance Optimization

1. **Use production server**:
   ```bash
   # Instead of --reload for development
   python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

2. **Enable gzip compression**
3. **Use CDN for static files**
4. **Implement caching** for repeated requests

## 📞 Support

If you encounter issues:

1. Check the logs for error messages
2. Verify all dependencies are installed
3. Ensure Python 3.8+ is being used
4. Check firewall and network settings
5. Review the troubleshooting section above
