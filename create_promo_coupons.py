#!/usr/bin/env python3
"""
Create promotional coupons for Biryani Club
"""

from app import app, db
from models import Promotion
from datetime import datetime, timedelta
import pytz

def create_promotional_coupons():
    """Create promotional coupons"""
    with app.app_context():
        ist = pytz.timezone('Asia/Kolkata')
        
        # Delete existing promotional coupons if they exist
        existing_codes = ['WELCOME20', 'FIRST10', 'ORDER2', 'ORDER3', 'ORDER4', 'ORDER5']
        for code in existing_codes:
            existing = Promotion.query.filter_by(code=code).first()
            if existing:
                db.session.delete(existing)
                print(f"Deleted existing coupon: {code}")
        
        db.session.commit()
        
        # 1. WELCOME20 - 20% off first order
        welcome20 = Promotion(
            code='WELCOME20',
            description='Welcome Offer - 20% off on your first order! Minimum order ₹200',
            discount_type='percentage',
            discount_value=20,
            min_order_amount=200,
            max_discount=200,  # Maximum discount is ₹200
            is_active=True,
            expires_at=None  # No expiry
        )
        db.session.add(welcome20)
        print("✓ Created WELCOME20 coupon: 20% off (max ₹200), min order ₹200")
        
        # 2. FIRST10 - 10% off for orders (can be used up to 5 times total across all users)
        first10 = Promotion(
            code='FIRST10',
            description='10% off on your orders - Valid for first 5 orders only',
            discount_type='percentage',
            discount_value=10,
            min_order_amount=150,
            max_discount=100,  # Maximum discount is ₹100
            is_active=True,
            expires_at=None  # No expiry
        )
        db.session.add(first10)
        print("✓ Created FIRST10 coupon: 10% off (max ₹100), min order ₹150")
        
        # Additional coupons for subsequent orders
        order_coupons = [
            ('ORDER2', 'Second order special - 10% off', 10, 100, 150),
            ('ORDER3', 'Third time lucky - 10% off', 10, 100, 150),
            ('ORDER4', 'Fourth order bonus - 10% off', 10, 100, 150),
            ('ORDER5', 'Fifth order celebration - 10% off', 10, 100, 150),
        ]
        
        for code, desc, value, max_disc, min_amt in order_coupons:
            promo = Promotion(
                code=code,
                description=desc,
                discount_type='percentage',
                discount_value=value,
                min_order_amount=min_amt,
                max_discount=max_disc,
                is_active=True,
                expires_at=None
            )
            db.session.add(promo)
            print(f"✓ Created {code} coupon: {value}% off (max ₹{max_disc}), min order ₹{min_amt}")
        
        # 3. Limited time festive offers
        festive_offer = Promotion(
            code='FEAST50',
            description='Festive Special - ₹50 off on orders above ₹300',
            discount_type='fixed',
            discount_value=50,
            min_order_amount=300,
            is_active=True,
            expires_at=datetime.now(ist) + timedelta(days=30)
        )
        db.session.add(festive_offer)
        print("✓ Created FEAST50 coupon: ₹50 off, min order ₹300 (expires in 30 days)")
        
        # 4. Free dessert on biryani orders
        free_dessert = Promotion(
            code='SWEETTOOTH',
            description='Free dessert with Biryani orders above ₹250',
            discount_type='free_item_category',
            discount_value=0,
            min_order_amount=250,
            free_item_category='Desserts',
            free_item_qty=1,
            is_active=True
        )
        db.session.add(free_dessert)
        print("✓ Created SWEETTOOTH coupon: Free dessert with orders above ₹250")
        
        db.session.commit()
        print("\n✅ All promotional coupons created successfully!")
        print("\n📋 Coupon Summary:")
        print("   • WELCOME20: Perfect for new customers - 20% off first order")
        print("   • FIRST10, ORDER2-5: 10% off for first 5 orders (one-time use each)")
        print("   • FEAST50: ₹50 off festive special")
        print("   • SWEETTOOTH: Free dessert on biryani orders")

if __name__ == '__main__':
    print("🎁 Creating promotional coupons...\n")
    create_promotional_coupons()
