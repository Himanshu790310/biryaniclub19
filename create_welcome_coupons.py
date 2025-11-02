#!/usr/bin/env python
"""Create welcome and order-based coupon promotions"""

from app import app, db
from models import Promotion
from datetime import datetime, timedelta
import pytz

def ist_now():
    """Get current IST time"""
    ist = pytz.timezone('Asia/Kolkata')
    return datetime.now(ist).replace(tzinfo=None)

with app.app_context():
    # Create WELCOME20 promotion (20% off, first-time users)
    welcome20 = Promotion.query.filter_by(code='WELCOME20').first()
    if not welcome20:
        welcome20 = Promotion(
            code='WELCOME20',
            description='Welcome offer - 20% discount on your first order',
            discount_type='percentage',
            discount_value=20.0,
            min_order_amount=200.0,  # Minimum order of ₹200
            max_discount=100.0,      # Maximum discount of ₹100
            is_active=True,
            usage_limit=None,        # Unlimited usage (but tracked per user)
            expires_at=None          # Never expires
        )
        db.session.add(welcome20)
        print("✅ Created WELCOME20: 20% off (max ₹100), min order ₹200")
    else:
        print("ℹ️  WELCOME20 already exists")
    
    # Create order-based coupons (10% off for orders 2-5)
    order_coupons = [
        {
            'code': '2ND10',
            'description': 'Second order discount - 10% off',
            'order_number': 2
        },
        {
            'code': '3RD10',
            'description': 'Third order discount - 10% off',
            'order_number': 3
        },
        {
            'code': '4TH10',
            'description': 'Fourth order discount - 10% off',
            'order_number': 4
        },
        {
            'code': '5TH10',
            'description': 'Fifth order discount - 10% off',
            'order_number': 5
        }
    ]
    
    for coupon_data in order_coupons:
        existing = Promotion.query.filter_by(code=coupon_data['code']).first()
        if not existing:
            coupon = Promotion(
                code=coupon_data['code'],
                description=coupon_data['description'],
                discount_type='percentage',
                discount_value=10.0,
                min_order_amount=150.0,  # Minimum order of ₹150
                max_discount=75.0,       # Maximum discount of ₹75
                is_active=True,
                usage_limit=None,        # Unlimited usage (but tracked per user)
                expires_at=None          # Never expires
            )
            db.session.add(coupon)
            print(f"✅ Created {coupon_data['code']}: 10% off (max ₹75), min order ₹150")
        else:
            print(f"ℹ️  {coupon_data['code']} already exists")
    
    # Commit all changes
    db.session.commit()
    
    print("\n🎉 All welcome and order-based coupons are ready!")
    print("\nActive Promotions:")
    promotions = Promotion.query.filter_by(is_active=True).all()
    for promo in promotions:
        print(f"  • {promo.code}: {promo.description}")
