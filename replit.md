# Biryani Club - Food Ordering Platform

## Overview
Biryani Club is a comprehensive food ordering web application built with Flask. This is a fully functional restaurant management system featuring online ordering, delivery tracking, admin management, and customer loyalty programs.

**Live Application**: The app is now running and ready to use!

## Key Features

### Customer Features
- **Browse Menu**: 200+ menu items across 9 categories (Biryani, Rolls, Chowmein, Bread, Rice, Starters, Main Course, Soups, Beverages, Desserts)
- **Smart Search & Filters**: Search by name, filter by category, toggle vegetarian mode
- **Shopping Cart**: Add items, modify quantities, apply coupon codes
- **User Authentication**: Register, login, manage profile
- **Order Tracking**: Real-time order status updates (Pending → Confirmed → Preparing → Out for Delivery → Delivered)
- **Loyalty Program**: Earn points on orders, tier-based rewards (Bronze, Silver, Gold, Platinum)
- **Promotions & Offers**: Seasonal promotions, welcome coupons, discount codes
- **UPI Payment**: QR code generation for UPI payments

### Admin Features
- **Menu Management**: Add, edit, delete menu items with image uploads
- **Order Management**: View all orders, update order status, assign delivery personnel
- **User Management**: View and manage customer accounts
- **Promotions**: Create and manage promotional offers
- **Store Settings**: Control store open/close status, delivery settings
- **Analytics**: View coupon usage and order statistics

### Delivery Personnel Features
- **Delivery Dashboard**: View assigned orders
- **Route Planning**: Interactive map for delivery locations
- **Status Updates**: Update order status in real-time

## Technology Stack

### Backend
- **Framework**: Flask 3.1.2
- **Database**: PostgreSQL (with SQLAlchemy ORM)
- **Authentication**: Werkzeug password hashing
- **Image Processing**: Pillow for menu item images
- **QR Codes**: qrcode library for UPI payments

### Frontend
- **Templates**: Jinja2 templating
- **Styling**: Custom CSS with gradient backgrounds
- **JavaScript**: Vanilla JS for dynamic interactions
- **PWA**: Service Worker for offline support and installability

## Project Structure

```
.
├── app.py                      # Flask app initialization & database setup
├── main.py                     # Application entry point
├── routes.py                   # All application routes
├── models.py                   # Database models (User, MenuItem, Order, etc.)
├── utils.py                    # Helper functions
├── image_utils.py              # Image upload and processing
├── templates/                  # HTML templates
│   ├── base.html              # Base template with navigation
│   ├── home.html              # Landing page
│   ├── menu.html              # Menu browsing
│   ├── cart.html              # Shopping cart
│   ├── checkout.html          # Checkout process
│   ├── my_orders.html         # Order history
│   ├── admin*.html            # Admin panel templates
│   └── delivery*.html         # Delivery dashboard
└── static/                     # Static assets
    ├── style.css              # Main stylesheet
    ├── delivery.js            # Delivery dashboard logic
    ├── sw.js                  # Service Worker for PWA
    ├── manifest.json          # PWA manifest
    └── uploads/               # User-uploaded images
```

## Database Schema

### Models
- **User**: Customer accounts, admin, delivery personnel
- **MenuItem**: Menu items with categories, pricing, images
- **CartItem**: Shopping cart entries
- **Order**: Customer orders with status tracking
- **OrderItem**: Individual items in an order
- **Promotion**: Marketing promotions and offers
- **CouponUsage**: Track coupon redemptions
- **StoreSettings**: Application-wide settings

## Default Credentials

### Admin Access
- **Username**: admin
- **Password**: admin123
- **Role**: Full admin access to all features

### Delivery Personnel
- **Username**: delivery
- **Password**: delivery123
- **Role**: Delivery dashboard access

## Environment Variables

The application uses the following environment variables:
- `DATABASE_URL`: PostgreSQL connection string (automatically configured)
- `SESSION_SECRET`: Flask session secret (auto-generated for dev)
- `CONTACT_PHONE`: Business contact number (default: 9241169665)
- `UPI_VPA`: UPI payment address (auto-generated from contact phone)

## Running the Application

The app is configured to run automatically via Replit workflow:
- **Development**: `python main.py` (runs on port 5000)
- **Production**: Gunicorn with 4 workers configured for autoscale deployment

## Recent Changes

### November 2, 2025
- Initial project setup in Replit environment
- Installed all Python dependencies
- Connected PostgreSQL database
- Created uploads directory for menu images
- Configured Flask workflow on port 5000
- Set up deployment configuration with Gunicorn
- Verified all features working (menu, cart, login, admin)

## Features Implementation Status

✅ **Complete and Working**:
- User registration and authentication
- Menu browsing with 200+ items
- Category filtering and search
- Shopping cart functionality
- Order placement and tracking
- Admin panel (menu, orders, users, promotions)
- Delivery dashboard
- Loyalty points system
- Coupon management
- UPI payment integration
- Store open/close control
- Progressive Web App (PWA) support

## Development Notes

### Image Uploads
Menu item images are stored in `static/uploads/menu_items/`. The system supports JPG, PNG, and WebP formats up to 5MB.

### Timezone
All timestamps use India Standard Time (IST/Asia/Kolkata) via pytz.

### Database Migrations
The app uses `db.create_all()` for initial setup. For production migrations, consider using Flask-Migrate.

## User Preferences

None specified yet. This section will be updated as user preferences are communicated.

## Next Steps (Optional Enhancements)

- Add payment gateway integration (Razorpay, Stripe)
- Implement SMS notifications for order updates
- Add review and rating system
- Create mobile app using the existing API
- Add analytics dashboard for sales insights
- Implement advanced inventory management
