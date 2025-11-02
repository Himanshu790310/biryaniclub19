# Biryani Club - Ubuntu 24.04 VPS Deployment Guide

This guide provides step-by-step instructions for deploying the Biryani Club application on an Ubuntu 24.04 VPS.

## Table of Contents
- [Prerequisites](#prerequisites)
- [System Setup](#system-setup)
- [Database Setup](#database-setup)
- [Application Setup](#application-setup)
- [Nginx Configuration](#nginx-configuration)
- [SSL/HTTPS Setup](#sslhttps-setup)
- [Systemd Service](#systemd-service)
- [Environment Variables](#environment-variables)
- [Firewall Configuration](#firewall-configuration)
- [Maintenance](#maintenance)

## Prerequisites

- Ubuntu 24.04 LTS VPS with at least 1GB RAM
- Root or sudo access
- Domain name pointed to your server's IP address
- SSH access to the server

## System Setup

### 1. Update System Packages

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Required System Packages

```bash
sudo apt install -y python3.11 python3.11-venv python3-pip \
    postgresql postgresql-contrib \
    nginx \
    git \
    build-essential \
    libpq-dev \
    python3-dev \
    ufw \
    certbot \
    python3-certbot-nginx
```

### 3. Create Application User

```bash
sudo adduser --system --group --home /opt/biryaniclub biryaniclub
```

## Database Setup

### 1. Configure PostgreSQL

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL prompt, create database and user:
CREATE DATABASE biryaniclub;
CREATE USER biryaniclub WITH PASSWORD 'your_secure_password_here';
ALTER ROLE biryaniclub SET client_encoding TO 'utf8';
ALTER ROLE biryaniclub SET default_transaction_isolation TO 'read committed';
ALTER ROLE biryaniclub SET timezone TO 'Asia/Kolkata';
GRANT ALL PRIVILEGES ON DATABASE biryaniclub TO biryaniclub;
\q
```

### 2. Configure PostgreSQL for Remote Connections (if needed)

Edit `/etc/postgresql/16/main/postgresql.conf`:
```bash
sudo nano /etc/postgresql/16/main/postgresql.conf
```

Find and modify:
```
listen_addresses = 'localhost'
```

Edit `/etc/postgresql/16/main/pg_hba.conf`:
```bash
sudo nano /etc/postgresql/16/main/pg_hba.conf
```

Add:
```
local   biryaniclub     biryaniclub                     md5
```

Restart PostgreSQL:
```bash
sudo systemctl restart postgresql
```

## Application Setup

### 1. Clone Repository

```bash
cd /opt/biryaniclub
sudo -u biryaniclub git clone https://github.com/yourusername/biryani-club.git .
```

Or upload your files:
```bash
# Using SCP from your local machine
scp -r /path/to/biryani-club/* user@yourserver:/opt/biryaniclub/
sudo chown -R biryaniclub:biryaniclub /opt/biryaniclub
```

### 2. Create Virtual Environment

```bash
cd /opt/biryaniclub
sudo -u biryaniclub python3.11 -m venv venv
```

### 3. Install Python Dependencies

```bash
sudo -u biryaniclub /opt/biryaniclub/venv/bin/pip install --upgrade pip
sudo -u biryaniclub /opt/biryaniclub/venv/bin/pip install -r requirements.txt
```

### 4. Create Production Environment File

```bash
sudo -u biryaniclub nano /opt/biryaniclub/.env
```

Add the following content:
```env
# Flask Configuration
SESSION_SECRET=your_very_secure_random_secret_key_here
FLASK_ENV=production

# Database Configuration
DATABASE_URL=postgresql://biryaniclub:your_secure_password_here@localhost/biryaniclub

# Server Configuration
PORT=5000
HOST=0.0.0.0

# Contact Information
CONTACT_PHONE=9876543210
UPI_VPA=biryaniclub@upi

# Optional: Email Configuration (for future features)
# MAIL_SERVER=smtp.gmail.com
# MAIL_PORT=587
# MAIL_USERNAME=your-email@gmail.com
# MAIL_PASSWORD=your-app-password
```

**Important:** Replace all placeholder values with your actual credentials.

### 5. Set Correct Permissions

```bash
sudo chown -R biryaniclub:biryaniclub /opt/biryaniclub
sudo chmod 640 /opt/biryaniclub/.env
```

### 6. Initialize Database

```bash
sudo -u biryaniclub /opt/biryaniclub/venv/bin/python /opt/biryaniclub/main.py
```

Press Ctrl+C after the database is initialized.

## Nginx Configuration

### 1. Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/biryaniclub
```

Add the following configuration:
```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    client_max_body_size 5M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeouts
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    location /static {
        alias /opt/biryaniclub/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location ~* \.(jpg|jpeg|png|gif|ico|css|js|webp)$ {
        root /opt/biryaniclub;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
```

### 2. Enable the Site

```bash
sudo ln -s /etc/nginx/sites-available/biryaniclub /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## SSL/HTTPS Setup

### 1. Obtain SSL Certificate with Let's Encrypt

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Follow the prompts to:
- Enter your email address
- Agree to terms of service
- Choose to redirect HTTP to HTTPS (recommended)

### 2. Auto-Renewal Setup

Certbot automatically sets up a cron job for renewal. Test it:
```bash
sudo certbot renew --dry-run
```

## Systemd Service

### 1. Create Systemd Service File

```bash
sudo nano /etc/systemd/system/biryaniclub.service
```

Add the following content:
```ini
[Unit]
Description=Biryani Club Gunicorn Application
After=network.target postgresql.service

[Service]
Type=notify
User=biryaniclub
Group=biryaniclub
WorkingDirectory=/opt/biryaniclub
Environment="PATH=/opt/biryaniclub/venv/bin"
EnvironmentFile=/opt/biryaniclub/.env
ExecStart=/opt/biryaniclub/venv/bin/gunicorn \
    --bind 127.0.0.1:5000 \
    --workers 3 \
    --worker-class sync \
    --max-requests 1000 \
    --max-requests-jitter 50 \
    --timeout 60 \
    --access-logfile /var/log/biryaniclub/access.log \
    --error-logfile /var/log/biryaniclub/error.log \
    --log-level info \
    app:app

# Restart policy
Restart=always
RestartSec=10

# Security settings
NoNewPrivileges=true
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

### 2. Create Log Directory

```bash
sudo mkdir -p /var/log/biryaniclub
sudo chown -R biryaniclub:biryaniclub /var/log/biryaniclub
```

### 3. Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable biryaniclub
sudo systemctl start biryaniclub
sudo systemctl status biryaniclub
```

### 4. Check Application Logs

```bash
# View real-time logs
sudo journalctl -u biryaniclub -f

# View error logs
sudo tail -f /var/log/biryaniclub/error.log

# View access logs
sudo tail -f /var/log/biryaniclub/access.log
```

## Environment Variables

The `.env` file should contain:

```env
# Required Variables
SESSION_SECRET=<generate-random-secret>
DATABASE_URL=postgresql://user:password@localhost/dbname
CONTACT_PHONE=<your-phone>
UPI_VPA=<your-upi-id>

# Optional Variables
FLASK_ENV=production
PORT=5000
HOST=0.0.0.0
```

### Generate Secure Secret Key

```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

## Firewall Configuration

### 1. Configure UFW Firewall

```bash
# Allow SSH (important - don't lock yourself out!)
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

### 2. Configure Fail2ban (Optional but Recommended)

```bash
sudo apt install fail2ban -y
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

## Maintenance

### Update Application

```bash
# Stop the service
sudo systemctl stop biryaniclub

# Backup database
sudo -u postgres pg_dump biryaniclub > backup_$(date +%Y%m%d_%H%M%S).sql

# Pull latest code
cd /opt/biryaniclub
sudo -u biryaniclub git pull

# Install new dependencies if any
sudo -u biryaniclub /opt/biryaniclub/venv/bin/pip install -r requirements.txt

# Start the service
sudo systemctl start biryaniclub
```

### Backup Database

```bash
# Manual backup
sudo -u postgres pg_dump biryaniclub > /backup/biryaniclub_$(date +%Y%m%d).sql

# Automated daily backup (add to cron)
sudo crontab -e
```

Add this line:
```
0 2 * * * /usr/bin/pg_dump -U postgres biryaniclub > /backup/biryaniclub_$(date +\%Y\%m\%d).sql
```

### Restore Database

```bash
sudo -u postgres psql biryaniclub < /path/to/backup.sql
```

### Monitor Service

```bash
# Check service status
sudo systemctl status biryaniclub

# View logs
sudo journalctl -u biryaniclub --since "1 hour ago"

# Monitor resource usage
htop
```

### Restart Services

```bash
# Restart application
sudo systemctl restart biryaniclub

# Restart Nginx
sudo systemctl restart nginx

# Restart PostgreSQL
sudo systemctl restart postgresql
```

## Troubleshooting

### Application Won't Start

1. Check logs:
```bash
sudo journalctl -u biryaniclub -n 100
```

2. Verify environment file:
```bash
sudo -u biryaniclub cat /opt/biryaniclub/.env
```

3. Test Gunicorn manually:
```bash
sudo -u biryaniclub /opt/biryaniclub/venv/bin/gunicorn --bind 0.0.0.0:5000 app:app
```

### Database Connection Issues

1. Verify PostgreSQL is running:
```bash
sudo systemctl status postgresql
```

2. Test database connection:
```bash
sudo -u biryaniclub psql -h localhost -U biryaniclub -d biryaniclub
```

### Nginx Issues

1. Test Nginx configuration:
```bash
sudo nginx -t
```

2. Check Nginx logs:
```bash
sudo tail -f /var/log/nginx/error.log
```

### SSL Certificate Issues

```bash
# Renew certificate
sudo certbot renew

# Check certificate status
sudo certbot certificates
```

## Security Recommendations

1. **Regular Updates**: Keep system and packages updated
```bash
sudo apt update && sudo apt upgrade -y
```

2. **Change Default Credentials**: Update admin/delivery passwords immediately after deployment

3. **Use Strong Passwords**: For database and application secrets

4. **Enable Firewall**: Use UFW to restrict access

5. **Monitor Logs**: Regularly check application and system logs

6. **Backup Regularly**: Set up automated database backups

7. **Use HTTPS Only**: Force all traffic through HTTPS

## Performance Optimization

### 1. Optimize Gunicorn Workers

Rule of thumb: `(2 x CPU cores) + 1`

For a 2-core server:
```bash
--workers 5
```

### 2. Enable Nginx Caching

Add to Nginx config:
```nginx
proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;

location / {
    proxy_cache my_cache;
    proxy_cache_valid 200 1m;
    # ... rest of config
}
```

### 3. Database Connection Pooling

The application uses SQLAlchemy connection pooling by default. No additional configuration needed.

## Support

For issues or questions:
- Check application logs: `/var/log/biryaniclub/`
- Check system logs: `journalctl -u biryaniclub`
- Review this deployment guide
- Contact your system administrator

---

**Last Updated**: October 2025
**Compatible with**: Ubuntu 24.04 LTS
