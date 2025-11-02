#!/usr/bin/env python3
"""
Update menu pricing with psychological pricing and better portion naming
- Rename (Small) -> (Half) and (Large) -> (Full)
- Increase all prices by 15%
- Apply psychological pricing (end with 9 for better conversion)
"""

from app import app, db
from models import MenuItem
import math

def apply_psychological_price(price):
    """Apply psychological pricing - end with 9"""
    # Increase by 15%
    new_price = price * 1.15
    
    # Round to nearest 10 then subtract 1 for prices above 50
    if new_price >= 50:
        rounded = math.ceil(new_price / 10) * 10 - 1
    else:
        # For lower prices, round to nearest 5 then subtract 1
        rounded = math.ceil(new_price / 5) * 5 - 1
    
    return max(rounded, 29)  # Minimum price is 29

def rename_portion_sizes(name):
    """Rename portion sizes for better psychology"""
    replacements = [
        (' (Small)', ' (Half)'),
        (' (small)', ' (Half)'),
        (' (Large)', ' (Full)'),
        (' (large)', ' (Full)'),
        # Also handle the plain versions without parentheses
        (' Small', ' (Half)'),
        (' Large', ' (Full)'),
    ]
    
    new_name = name
    for old, new in replacements:
        new_name = new_name.replace(old, new)
    
    return new_name

def update_all_prices():
    """Update all menu items with new pricing strategy"""
    with app.app_context():
        items = MenuItem.query.all()
        updated_count = 0
        
        for item in items:
            old_name = item.name
            old_price = item.price
            
            # Update name (Half/Full nomenclature)
            item.name = rename_portion_sizes(item.name)
            
            # Update price with 15% increase and psychological pricing
            item.price = apply_psychological_price(item.price)
            
            # Show what changed
            if old_name != item.name or old_price != item.price:
                print(f"✓ {old_name} (₹{old_price}) → {item.name} (₹{item.price})")
                updated_count += 1
        
        # Commit all changes
        try:
            db.session.commit()
            print(f"\n✅ Successfully updated {updated_count} menu items!")
            print("   - All prices increased by ~15% with psychological pricing")
            print("   - Renamed Small→Half, Large→Full for better perception")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error updating prices: {e}")

if __name__ == '__main__':
    print("🔄 Updating menu prices and portion names...\n")
    update_all_prices()
