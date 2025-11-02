#!/bin/bash
# Biryani Club Installation Script for Ubuntu VPS

echo "🚀 Installing Biryani Club on Ubuntu VPS..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and required packages
sudo apt install -y python3 python3-pip python3-venv nginx

# Create application directory
sudo mkdir -p /var/www/biryaniclub
sudo chown $USER:$USER /var/www/biryaniclub

# Copy application files
cp -r * /var/www/biryaniclub/
cd /var/www/biryaniclub

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Run database migration
python migrate_timezone_data.py

# Create environment file
cp .env.example .env
echo "Please edit /var/www/biryaniclub/.env with your configuration"

# Set up systemd service
sudo cp biryaniclub.service /etc/systemd/system/
sudo systemctl daemon-reload

# Set up nginx
sudo cp nginx.conf.example /etc/nginx/sites-available/biryaniclub
sudo ln -sf /etc/nginx/sites-available/biryaniclub /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test nginx configuration
sudo nginx -t

echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit /var/www/biryaniclub/.env with your settings"
echo "2. Update paths in /etc/systemd/system/biryaniclub.service"
echo "3. Update domain in /etc/nginx/sites-available/biryaniclub"
echo "4. Start services:"
echo "   sudo systemctl enable biryaniclub"
echo "   sudo systemctl start biryaniclub"
echo "   sudo systemctl reload nginx"
echo ""
echo "Default admin credentials: admin/admin123"
echo "Default delivery credentials: delivery/delivery123"
echo "⚠️  CHANGE THESE CREDENTIALS AFTER FIRST LOGIN!"
