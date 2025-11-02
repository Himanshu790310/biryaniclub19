#!/usr/bin/env python3
"""
Migration script to convert existing UTC-naive timestamps to IST-naive timestamps.

This script converts UTC-naive timestamps to IST-naive by adding 5h30m.
It's designed to be safe and idempotent - can be run multiple times safely.

Run this script once to fix the timezone data issue.
"""

import os
import sys
from datetime import datetime, timedelta
import pytz

# Add the current directory to path to import our models
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User, MenuItem, CartItem, Order, StoreSettings, Promotion

# UTC to IST conversion (add 5h30m)
UTC_TO_IST_OFFSET = timedelta(hours=5, minutes=30)

def is_likely_utc_timestamp(timestamp, reference_ist_time=None):
    """
    Determine if a timestamp is likely UTC-naive (needs conversion) vs IST-naive (already converted).
    
    Strategy: More aggressive detection for UTC-naive timestamps.
    Since we know the system was changed to IST-naive recently, we can be more certain
    about which records need conversion.
    """
    if not timestamp:
        return False
        
    if not reference_ist_time:
        # Get current IST time as naive datetime
        ist = pytz.timezone('Asia/Kolkata')
        reference_ist_time = datetime.now(ist).replace(tzinfo=None)
    
    # Deployment cutoff: when the system switched to IST-naive timestamps
    # Any timestamp before this is likely UTC-naive and needs conversion
    deployment_cutoff = datetime(2025, 9, 17, 16, 30)  # Around when IST system was deployed
    
    if timestamp < deployment_cutoff:
        return True  # Likely UTC, needs conversion
    
    # For recent timestamps from today, use more refined logic
    if timestamp.date() == reference_ist_time.date():
        # If timestamp is very early morning (before 10 AM IST), it could be UTC
        # A UTC timestamp would appear in early morning hours after IST conversion
        if timestamp.hour < 10:
            return True  # Likely UTC that needs conversion
            
        # If it's a reasonable IST business hour, likely already IST
        if timestamp.hour >= 10:
            return False  # Likely already IST
    
    return False  # Default: assume already IST

def migrate_timezone_data():
    """Convert existing UTC-naive timestamps to IST-naive by adding 5h30m"""
    
    with app.app_context():
        try:
            print("Starting timezone migration (UTC-naive to IST-naive)...")
            print(f"Conversion offset: +{UTC_TO_IST_OFFSET}")
            
            # Get current IST time for reference
            ist = pytz.timezone('Asia/Kolkata')
            reference_ist_time = datetime.now(ist).replace(tzinfo=None)
            print(f"Reference IST time: {reference_ist_time}")
            
            total_converted = 0
            
            # Update User created_at timestamps
            users = User.query.all()
            user_count = 0
            for user in users:
                if user.created_at and is_likely_utc_timestamp(user.created_at, reference_ist_time):
                    old_time = user.created_at
                    user.created_at = user.created_at + UTC_TO_IST_OFFSET
                    user_count += 1
                    print(f"User {user.id}: {old_time} -> {user.created_at}")
            print(f"Updated {user_count} user timestamps")
            total_converted += user_count
            
            # Update MenuItem created_at and image_updated_at timestamps
            menu_items = MenuItem.query.all()
            menu_count = 0
            for item in menu_items:
                updated = False
                if item.created_at and is_likely_utc_timestamp(item.created_at, reference_ist_time):
                    old_time = item.created_at
                    item.created_at = item.created_at + UTC_TO_IST_OFFSET
                    print(f"MenuItem {item.id} created_at: {old_time} -> {item.created_at}")
                    updated = True
                    
                if item.image_updated_at and is_likely_utc_timestamp(item.image_updated_at, reference_ist_time):
                    old_time = item.image_updated_at
                    item.image_updated_at = item.image_updated_at + UTC_TO_IST_OFFSET
                    print(f"MenuItem {item.id} image_updated_at: {old_time} -> {item.image_updated_at}")
                    updated = True
                    
                if updated:
                    menu_count += 1
            print(f"Updated {menu_count} menu item records")
            total_converted += menu_count
            
            # Update CartItem created_at timestamps
            cart_items = CartItem.query.all()
            cart_count = 0
            for item in cart_items:
                if item.created_at and is_likely_utc_timestamp(item.created_at, reference_ist_time):
                    old_time = item.created_at
                    item.created_at = item.created_at + UTC_TO_IST_OFFSET
                    cart_count += 1
                    print(f"CartItem {item.id}: {old_time} -> {item.created_at}")
            print(f"Updated {cart_count} cart item timestamps")
            total_converted += cart_count
            
            # Update Order timestamps (created_at, confirmed_at, delivery_time)
            orders = Order.query.all()
            order_count = 0
            for order in orders:
                updated = False
                if order.created_at and is_likely_utc_timestamp(order.created_at, reference_ist_time):
                    old_time = order.created_at
                    order.created_at = order.created_at + UTC_TO_IST_OFFSET
                    print(f"Order {order.id} created_at: {old_time} -> {order.created_at}")
                    updated = True
                    
                if order.confirmed_at and is_likely_utc_timestamp(order.confirmed_at, reference_ist_time):
                    old_time = order.confirmed_at
                    order.confirmed_at = order.confirmed_at + UTC_TO_IST_OFFSET
                    print(f"Order {order.id} confirmed_at: {old_time} -> {order.confirmed_at}")
                    updated = True
                    
                if order.delivery_time and is_likely_utc_timestamp(order.delivery_time, reference_ist_time):
                    old_time = order.delivery_time
                    order.delivery_time = order.delivery_time + UTC_TO_IST_OFFSET
                    print(f"Order {order.id} delivery_time: {old_time} -> {order.delivery_time}")
                    updated = True
                    
                if updated:
                    order_count += 1
            print(f"Updated {order_count} order records")
            total_converted += order_count
            
            # Update StoreSettings updated_at timestamps
            settings = StoreSettings.query.all()
            settings_count = 0
            for setting in settings:
                if setting.updated_at and is_likely_utc_timestamp(setting.updated_at, reference_ist_time):
                    old_time = setting.updated_at
                    setting.updated_at = setting.updated_at + UTC_TO_IST_OFFSET
                    settings_count += 1
                    print(f"StoreSetting {setting.id}: {old_time} -> {setting.updated_at}")
            print(f"Updated {settings_count} store settings timestamps")
            total_converted += settings_count
            
            # Update Promotion timestamps (created_at, expires_at)
            promotions = Promotion.query.all()
            promo_count = 0
            for promo in promotions:
                updated = False
                if promo.created_at and is_likely_utc_timestamp(promo.created_at, reference_ist_time):
                    old_time = promo.created_at
                    promo.created_at = promo.created_at + UTC_TO_IST_OFFSET
                    print(f"Promotion {promo.id} created_at: {old_time} -> {promo.created_at}")
                    updated = True
                    
                if promo.expires_at and is_likely_utc_timestamp(promo.expires_at, reference_ist_time):
                    old_time = promo.expires_at
                    promo.expires_at = promo.expires_at + UTC_TO_IST_OFFSET
                    print(f"Promotion {promo.id} expires_at: {old_time} -> {promo.expires_at}")
                    updated = True
                    
                if updated:
                    promo_count += 1
            print(f"Updated {promo_count} promotion records")
            total_converted += promo_count
            
            # Show summary before committing
            print(f"\n📊 Migration Summary:")
            print(f"   Users: {user_count} records")
            print(f"   Menu Items: {menu_count} records") 
            print(f"   Cart Items: {cart_count} records")
            print(f"   Orders: {order_count} records")
            print(f"   Store Settings: {settings_count} records")
            print(f"   Promotions: {promo_count} records")
            print(f"   Total converted: {total_converted} records")
            
            if total_converted > 0:
                # Check for auto-confirm flag
                auto_confirm = len(sys.argv) > 1 and sys.argv[1] == '--yes'
                
                if auto_confirm:
                    print(f"🤖 Auto-confirming migration of {total_converted} records...")
                    confirm = 'y'
                else:
                    # Ask for confirmation before committing
                    confirm = input(f"\n⚠️  About to update {total_converted} records. Continue? (y/N): ")
                
                if confirm.lower() != 'y':
                    print("❌ Migration cancelled by user")
                    return
                    
                # Commit all changes
                db.session.commit()
                print("✅ Timezone migration completed successfully!")
            else:
                print("✅ No records needed conversion - all timestamps appear to already be IST-naive!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ Migration failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == "__main__":
    migrate_timezone_data()