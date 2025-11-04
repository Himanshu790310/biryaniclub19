# Biryani Club - VPS Deployment Guide

## Quick Setup

### 1. Install Dependencies
```bash
sudo apt update
sudo apt install python3.11 python3.11-venv postgresql nginx -y
```

### 2. Extract Files
```bash
tar -xzf biryani_club_deployment.tar.gz
cd biryani_club_deployment
```

### 3. Create Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 4. Setup Database
```bash
sudo -u postgres psql
# CREATE DATABASE biryani_club;
# CREATE USER biryani_user WITH PASSWORD 'your_password';
# GRANT ALL PRIVILEGES ON DATABASE biryani_club TO biryani_user;
# \q
```

### 5. Configure Environment
Create `.env` file:
```
DATABASE_URL=postgresql://biryani_user:password@localhost/biryani_club
SESSION_SECRET=your-random-secret-key
CONTACT_PHONE=9241169665
```

### 6. Run Application
```bash
# Development
python main.py

# Production with Gunicorn
gunicorn --bind=0.0.0.0:5000 --workers=4 app:app
```

### 7. Setup Nginx (Optional)
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
    
    location /static {
        alias /path/to/biryani_club_deployment/static;
    }
}
```

## Default Credentials
- Admin: admin / admin123
- Delivery: delivery / delivery123

**IMPORTANT: Change these after first login!**

## Features
- 200+ menu items
- Shopping cart & checkout
- UPI payment integration
- Admin panel
- Delivery tracking
- Loyalty points system
- PWA support

## Support
Check logs: `tail -f /var/log/biryani_club.log`
