
from app import app, db
from models import MenuItem

def categorize_veg_nonveg():
    """Categorize existing menu items as veg or non-veg based on their names"""
    
    # Definitive non-veg keywords (these override everything)
    non_veg_keywords = [
        'chicken', 'mutton', 'keema', 'fish', 'prawn', 'egg', 
        'seekh', 'tandoor', 'malai', 'reshmi', 'lollipop'
    ]
    
    # Definitive veg keywords
    veg_keywords = ['paneer', 'mushroom', 'aloo', 'gobi', 'dal', 'palak', 'matar', 'veg']
    
    with app.app_context():
        menu_items = MenuItem.query.all()
        
        for item in menu_items:
            name_lower = item.name.lower()
            
            # Default to non-veg (safer assumption for restaurant)
            is_veg = False
            
            # Check for non-veg keywords first (highest priority)
            has_nonveg = any(keyword in name_lower for keyword in non_veg_keywords)
            
            # Check for veg keywords
            has_veg_keyword = any(keyword in name_lower for keyword in veg_keywords)
            
            # Logic:
            # 1. If it has non-veg keywords, it's non-veg (even if it says "veg biryani")
            # 2. If it has "veg" explicitly in name, it's veg
            # 3. If it has veg ingredients (paneer, mushroom, etc.), it's veg
            # 4. Special cases for bread, rice, desserts, beverages
            
            if has_nonveg:
                is_veg = False
            elif 'veg' in name_lower and 'non' not in name_lower:
                is_veg = True
            elif has_veg_keyword:
                is_veg = True
            elif item.category in ['Bread', 'Desserts', 'Beverages', 'Soups']:
                # Most breads, desserts, beverages, and soups are veg unless they have non-veg keywords
                is_veg = True
            elif 'rice' in name_lower and not has_nonveg:
                # Plain rice items are veg
                is_veg = True
            
            item.is_vegetarian = is_veg
            
            print(f"{item.name}: {'Veg' if item.is_vegetarian else 'Non-Veg'}")
        
        db.session.commit()
        print(f"\n✓ Successfully categorized {len(menu_items)} menu items")

def increase_prices():
    """Increase all menu item prices by 15%"""
    with app.app_context():
        menu_items = MenuItem.query.all()
        
        for item in menu_items:
            old_price = item.price
            item.price = round(old_price * 1.15, 2)
            print(f"{item.name}: ₹{old_price} → ₹{item.price}")
        
        db.session.commit()
        print(f"\n✓ Successfully increased prices for {len(updated_items)} items by 15%")

if __name__ == "__main__":
    print("Starting migration...")
    print("\n1. Categorizing items as veg/non-veg:")
    categorize_veg_nonveg()
    
    # Uncomment below if you want to increase prices
    print("\n2. Increasing prices by 15%:")
    increase_prices()
    
    print("\n✓ Migration completed successfully!")
