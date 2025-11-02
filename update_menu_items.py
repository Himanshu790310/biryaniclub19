#!/usr/bin/env python
"""Update menu items with correct veg/non-veg classification"""

from app import app, db
from models import MenuItem

# Items that should be marked as non-vegetarian
NON_VEG_KEYWORDS = [
    'chicken', 'mutton', 'fish', 'prawn', 'egg', 'keema', 
    'meat', 'seekh', 'reshmi', 'tandoori chicken', 'malai chicken'
]

with app.app_context():
    # Get all menu items
    items = MenuItem.query.all()
    updated_count = 0
    
    for item in items:
        name_lower = item.name.lower()
        desc_lower = (item.description or '').lower()
        
        # Check if item should be non-veg
        is_non_veg = any(keyword in name_lower or keyword in desc_lower 
                        for keyword in NON_VEG_KEYWORDS)
        
        # Update if classification is wrong
        if is_non_veg and item.is_vegetarian:
            item.is_vegetarian = False
            updated_count += 1
            print(f"Updated to NON-VEG: {item.name}")
        elif not is_non_veg and not item.is_vegetarian:
            # Make sure veg items are marked as veg
            item.is_vegetarian = True
            updated_count += 1
            print(f"Updated to VEG: {item.name}")
    
    # Commit changes
    if updated_count > 0:
        db.session.commit()
        print(f"\n✅ Successfully updated {updated_count} menu items!")
    else:
        print("\n✅ All menu items are already correctly classified!")
    
    # Show summary
    veg_count = MenuItem.query.filter_by(is_vegetarian=True).count()
    non_veg_count = MenuItem.query.filter_by(is_vegetarian=False).count()
    print(f"\nSummary:")
    print(f"  Vegetarian items: {veg_count}")
    print(f"  Non-Vegetarian items: {non_veg_count}")
    print(f"  Total items: {veg_count + non_veg_count}")
