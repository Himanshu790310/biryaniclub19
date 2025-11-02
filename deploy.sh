#!/bin/bash
# Biryani Club Deployment Script

echo "🚀 Starting Biryani Club deployment..."

# Create virtual environment (optional but recommended)
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run database migration
echo "Running database migration..."
python migrate_timezone_data.py

# Create systemd service file template
cat > biryaniclub.service << 'EOF'
[Unit]
Description=Biryani Club Flask Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/your/app
Environment=PATH=/path/to/your/app/venv/bin
EnvironmentFile=/path/to/your/app/.env
ExecStart=/path/to/your/app/venv/bin/gunicorn --workers 3 --bind unix:/run/biryaniclub/biryaniclub.sock app:app
Restart=always
RestartSec=3
RuntimeDirectory=biryaniclub
RuntimeDirectoryMode=755

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Deployment setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your configuration"
echo "2. Update paths in biryaniclub.service"
echo "3. Install service: sudo cp biryaniclub.service /etc/systemd/system/"
echo "4. Enable service: sudo systemctl enable biryaniclub"
echo "5. Start service: sudo systemctl start biryaniclub"
echo ""
echo "For development, run: python main.py"
echo "For production, run: gunicorn --bind 0.0.0.0:5000 --workers 3 app:app"
