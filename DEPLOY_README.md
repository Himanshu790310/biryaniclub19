# Biryani Club VPS Deployment Package

## Quick Start

1. **Upload this package to your VPS**
2. **Run the automated deployment script:**
   ```bash
   chmod +x vps_deploy.sh
   sudo ./vps_deploy.sh
   ```

## What's Included

- Complete application code
- Deployment scripts (automated & manual)
- Nginx configuration
- Systemd service file
- Database migration scripts
- Coupon creation script
- Comprehensive deployment documentation

## Files Overview

- `vps_deploy.sh` - Automated deployment script (recommended)
- `VPS_DEPLOYMENT_INSTRUCTIONS.MD` - Step-by-step manual instructions
- `DEPLOYMENT.md` - Detailed deployment guide with troubleshooting
- `.env.example` - Environment variables template
- `biryaniclub.service` - Systemd service configuration
- `nginx.conf.example` - Nginx reverse proxy configuration

## After Deployment

1. Your app will be available at: https://thebiryaniclub.shop
2. Admin login: admin / admin123
3. Delivery login: delivery / delivery123
4. **Change these passwords immediately!**

## Support

Review VPS_DEPLOYMENT_INSTRUCTIONS.MD for detailed setup instructions.
