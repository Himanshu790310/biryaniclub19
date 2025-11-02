#!/usr/bin/env python
"""Increase all menu item prices by 15%"""

from app import app, db
from models import MenuItem
import math

with app.app_context():
    menu_items = MenuItem.query.all()
    
    print(f"Updating {len(menu_items)} menu items...")
    print(f"{'Item Name':<40} {'Old Price':>10} {'New Price':>10}")
    print("-" * 65)
    
    for item in menu_items:
        old_price = item.price
        new_price = math.ceil(old_price * 1.15)  # 15% increase, rounded up
        item.price = new_price
        print(f"{item.name:<40} ₹{old_price:>9.2f} ₹{new_price:>9.2f}")
    
    db.session.commit()
    print("\n✅ All prices updated successfully! (+15%)")
