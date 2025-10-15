
from app import app, db
from models import Promotion
from datetime import datetime, timedelta
import pytz

def create_welcome_coupons():
    """Create welcome and loyalty coupons"""
    
    with app.app_context():
        ist = pytz.timezone('Asia/Kolkata')
        
        # Check if WELCOME20 exists
        welcome20 = Promotion.query.filter_by(code='WELCOME20').first()
        if not welcome20:
            welcome20 = Promotion(
                code='WELCOME20',
                description='Welcome offer - 20% off on first order',
                discount_type='percentage',
                discount_value=20,
                min_order_amount=200,
                max_discount=200,
                usage_limit=None,  # Unlimited
                expires_at=None,  # Never expires
                is_active=True
            )
            db.session.add(welcome20)
            print("✓ Created WELCOME20 coupon")
        else:
            print("✓ WELCOME20 already exists")
        
        # Generate ORDER10_X coupons for orders 2-5
        for order_num in range(2, 6):
            code = f'ORDER10_{order_num}'
            existing = Promotion.query.filter_by(code=code).first()
            
            if not existing:
                promo = Promotion(
                    code=code,
                    description=f'10% off on order #{order_num}',
                    discount_type='percentage',
                    discount_value=10,
                    min_order_amount=200,
                    max_discount=150,
                    usage_limit=None,  # Unlimited
                    expires_at=None,  # Never expires
                    is_active=True
                )
                db.session.add(promo)
                print(f"✓ Created {code} coupon")
            else:
                print(f"✓ {code} already exists")
        
        db.session.commit()
        print("\n✅ All coupons created successfully!")
        
        # Display all active coupons
        print("\n📋 Active Coupons:")
        print("-" * 60)
        all_promos = Promotion.query.filter_by(is_active=True).all()
        for p in all_promos:
            print(f"Code: {p.code:15} | {p.discount_value}% off | Min: ₹{p.min_order_amount}")
        print("-" * 60)

if __name__ == '__main__':
    create_welcome_coupons()
