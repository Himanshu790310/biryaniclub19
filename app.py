
import os
import logging
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key-change-in-production")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_for=1)

# Configure the database with UTF-8 encoding
database_url = os.environ.get("DATABASE_URL", "sqlite:///biryani_club.db")
if database_url.startswith("sqlite") and "?" not in database_url:
    database_url += "?charset=utf8mb4"

app.config["SQLALCHEMY_DATABASE_URI"] = database_url
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
    "connect_args": {"check_same_thread": False} if database_url.startswith("sqlite") else {}
}

# File upload configuration
app.config["UPLOAD_FOLDER"] = "static/uploads/menu_items"
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB max file size
app.config["ALLOWED_EXTENSIONS"] = {"jpg", "jpeg", "png", "webp"}

# Initialize SQLAlchemy
from models import db
db.init_app(app)

# Create tables and initialize data within app context
with app.app_context():
    # Import models to ensure tables are created
    from models import User, MenuItem, CartItem, Order, OrderItem, StoreSettings, Promotion
    
    # Create all tables
    db.create_all()
    
    # Initialize default data if not exists
    if StoreSettings.query.count() == 0:
        # Add default store settings
        StoreSettings.set_setting('store_open', 'true')
        StoreSettings.set_setting('delivery_radius', '10')
        StoreSettings.set_setting('base_delivery_charge', '30')
        print("Default store settings added")
        
    # Create admin user if not exists
    if User.query.filter_by(role='admin').count() == 0:
        admin_user = User(
            username='admin',
            email='admin@biryaniclub.com',
            full_name='Admin User',
            role='admin',
            phone='9999999999'
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        try:
            db.session.commit()
            print("Admin user created: username=admin, password=admin123")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating admin user: {e}")
            
    # Create delivery person if not exists
    if User.query.filter_by(role='delivery').count() == 0:
        delivery_user = User(
            username='delivery',
            email='delivery@biryaniclub.com',
            full_name='Delivery Person',
            role='delivery',
            phone='8888888888'
        )
        delivery_user.set_password('delivery123')
        db.session.add(delivery_user)
        try:
            db.session.commit()
            print("Delivery user created: username=delivery, password=delivery123")
        except Exception as e:
            db.session.rollback()
            print(f"Error creating delivery user: {e}")
    
    # Add complete menu items if none exist
    if MenuItem.query.count() == 0:
        menu_items = [
            # BIRYANI - Expanded varieties
            MenuItem(name='Veg Biryani', description='Fragrant basmati rice with mixed vegetables', price=114, category='Biryani', emoji='🍛', popularity=8),
            MenuItem(name='Veg Biryani (Large)', description='Fragrant basmati rice with mixed vegetables', price=218, category='Biryani', emoji='🍛', popularity=8),
            MenuItem(name='Egg Biryani', description='Aromatic rice with boiled eggs', price=126, category='Biryani', emoji='🍛', popularity=7),
            MenuItem(name='Egg Biryani (Large)', description='Aromatic rice with boiled eggs', price=229, category='Biryani', emoji='🍛', popularity=7),
            MenuItem(name='Paneer Biryani', description='Premium paneer pieces with fragrant rice', price=149, category='Biryani', emoji='🍛', popularity=9),
            MenuItem(name='Paneer Biryani (Large)', description='Premium paneer pieces with fragrant rice', price=275, category='Biryani', emoji='🍛', popularity=9),
            MenuItem(name='Mushroom Biryani', description='Fresh mushrooms with spiced rice', price=126, category='Biryani', emoji='🍛', popularity=6),
            MenuItem(name='Mushroom Biryani (Large)', description='Fresh mushrooms with spiced rice', price=229, category='Biryani', emoji='🍛', popularity=6),
            MenuItem(name='Chicken Biryani', description='Tender chicken pieces with aromatic rice', price=137, category='Biryani', emoji='🍛', popularity=10),
            MenuItem(name='Chicken Biryani (Large)', description='Tender chicken pieces with aromatic rice', price=252, category='Biryani', emoji='🍛', popularity=10),
            MenuItem(name='Chicken Biryani (Premium)', description='Premium chicken biryani with extra spices', price=160, category='Biryani', emoji='🍛', popularity=10),
            MenuItem(name='Chicken Biryani (Premium Large)', description='Premium chicken biryani with extra spices', price=287, category='Biryani', emoji='🍛', popularity=10),
            MenuItem(name='Mutton Biryani', description='Tender mutton pieces with aromatic basmati rice', price=206, category='Biryani', emoji='🍛', popularity=9),
            MenuItem(name='Mutton Biryani (Large)', description='Tender mutton pieces with aromatic basmati rice', price=379, category='Biryani', emoji='🍛', popularity=9),
            MenuItem(name='Keema Biryani', description='Spiced minced meat with fragrant rice', price=172, category='Biryani', emoji='🍛', popularity=8),
            MenuItem(name='Keema Biryani (Large)', description='Spiced minced meat with fragrant rice', price=321, category='Biryani', emoji='🍛', popularity=8),
            MenuItem(name='Fish Biryani', description='Fresh fish pieces with aromatic rice', price=183, category='Biryani', emoji='🍛', popularity=7),
            MenuItem(name='Fish Biryani (Large)', description='Fresh fish pieces with aromatic rice', price=344, category='Biryani', emoji='🍛', popularity=7),
            MenuItem(name='Prawn Biryani', description='Succulent prawns with spiced basmati rice', price=218, category='Biryani', emoji='🍛', popularity=8),
            MenuItem(name='Prawn Biryani (Large)', description='Succulent prawns with spiced basmati rice', price=402, category='Biryani', emoji='🍛', popularity=8),
            MenuItem(name='Hyderabadi Biryani', description='Traditional Hyderabadi style chicken biryani', price=195, category='Biryani', emoji='🍛', popularity=9),
            MenuItem(name='Hyderabadi Biryani (Large)', description='Traditional Hyderabadi style chicken biryani', price=367, category='Biryani', emoji='🍛', popularity=9),
            MenuItem(name='Awadhi Biryani', description='Lucknowi style aromatic biryani with chicken', price=183, category='Biryani', emoji='🍛', popularity=8),
            MenuItem(name='Awadhi Biryani (Large)', description='Lucknowi style aromatic biryani with chicken', price=344, category='Biryani', emoji='🍛', popularity=8),
            MenuItem(name='Dum Biryani', description='Slow cooked dum style chicken biryani', price=172, category='Biryani', emoji='🍛', popularity=9),
            MenuItem(name='Dum Biryani (Large)', description='Slow cooked dum style chicken biryani', price=333, category='Biryani', emoji='🍛', popularity=9),
            MenuItem(name='Kolkata Biryani', description='Bengali style biryani with potato and chicken', price=160, category='Biryani', emoji='🍛', popularity=7),
            MenuItem(name='Kolkata Biryani (Large)', description='Bengali style biryani with potato and chicken', price=310, category='Biryani', emoji='🍛', popularity=7),

            # ROLLS - Separated and expanded
            MenuItem(name='Veg Roll', description='Fresh vegetables wrapped in soft paratha', price=34, category='Rolls', emoji='🌯', popularity=7),
            MenuItem(name='Egg Roll', description='Scrambled eggs with onions in paratha wrap', price=45, category='Rolls', emoji='🌯', popularity=8),
            MenuItem(name='Paneer Roll', description='Spiced paneer cubes in soft roll', price=91, category='Rolls', emoji='🌯', popularity=6),
            MenuItem(name='Chicken Roll', description='Tender chicken pieces in paratha wrap', price=103, category='Rolls', emoji='🌯', popularity=9),
            MenuItem(name='Mutton Roll', description='Spiced mutton pieces wrapped in paratha', price=137, category='Rolls', emoji='🌯', popularity=8),
            MenuItem(name='Seekh Kebab Roll', description='Grilled seekh kebab wrapped in rumali roti', price=114, category='Rolls', emoji='🌯', popularity=9),
            MenuItem(name='Chicken Tikka Roll', description='Tandoor chicken tikka in naan wrap', price=126, category='Rolls', emoji='🌯', popularity=10),
            MenuItem(name='Aloo Roll', description='Spiced potato filling in soft paratha', price=29, category='Rolls', emoji='🌯', popularity=6),
            MenuItem(name='Masala Roll', description='Mixed vegetables with Indian spices', price=41, category='Rolls', emoji='🌯', popularity=7),
            MenuItem(name='Fish Roll', description='Fried fish pieces in paratha wrap', price=103, category='Rolls', emoji='🌯', popularity=6),
            MenuItem(name='Reshmi Kebab Roll', description='Soft chicken reshmi kebab in roomali roti', price=137, category='Rolls', emoji='🌯', popularity=8),
            MenuItem(name='Kathi Roll', description='Kolkata style chicken kathi roll', price=110, category='Rolls', emoji='🌯', popularity=9),
            MenuItem(name='Cheese Roll', description='Melted cheese with vegetables in roll', price=80, category='Rolls', emoji='🌯', popularity=7),
            MenuItem(name='Chicken Schezwan Roll', description='Spicy schezwan chicken roll', price=114, category='Rolls', emoji='🌯', popularity=8),
            MenuItem(name='Paneer Tikka Roll', description='Grilled paneer tikka in naan wrap', price=103, category='Rolls', emoji='🌯', popularity=7),
            MenuItem(name='Mushroom Roll', description='Sautéed mushrooms in soft paratha', price=68, category='Rolls', emoji='🌯', popularity=5),
            MenuItem(name='Double Egg Roll', description='Double portion of scrambled eggs in roll', price=68, category='Rolls', emoji='🌯', popularity=8),
            MenuItem(name='Chicken Keema Roll', description='Spiced chicken mince in paratha wrap', price=114, category='Rolls', emoji='🌯', popularity=8),
            MenuItem(name='Mutton Keema Roll', description='Spiced mutton mince in paratha wrap', price=137, category='Rolls', emoji='🌯', popularity=7),
            MenuItem(name='Chicken Malai Roll', description='Creamy chicken malai tikka roll', price=126, category='Rolls', emoji='🌯', popularity=8),
            MenuItem(name='Chicken 65 Roll', description='Spicy chicken 65 wrapped in paratha', price=121, category='Rolls', emoji='🌯', popularity=9),
            MenuItem(name='Prawn Roll', description='Fried prawns in soft paratha wrap', price=149, category='Rolls', emoji='🌯', popularity=6),

            # CHOWMEIN - Separated and expanded
            MenuItem(name='Veg Chowmein', description='Stir-fried noodles with mixed vegetables', price=57, category='Chowmein', emoji='🍜', popularity=6),
            MenuItem(name='Veg Chowmein (Large)', description='Stir-fried noodles with mixed vegetables', price=114, category='Chowmein', emoji='🍜', popularity=6),
            MenuItem(name='Paneer Chowmein', description='Noodles with paneer cubes and vegetables', price=68, category='Chowmein', emoji='🍜', popularity=5),
            MenuItem(name='Paneer Chowmein (Large)', description='Noodles with paneer cubes and vegetables', price=126, category='Chowmein', emoji='🍜', popularity=5),
            MenuItem(name='Egg Chowmein', description='Egg noodles with scrambled eggs', price=57, category='Chowmein', emoji='🍜', popularity=7),
            MenuItem(name='Egg Chowmein (Large)', description='Egg noodles with scrambled eggs', price=114, category='Chowmein', emoji='🍜', popularity=7),
            MenuItem(name='Chicken Chowmein', description='Noodles with tender chicken pieces', price=91, category='Chowmein', emoji='🍜', popularity=8),
            MenuItem(name='Chicken Chowmein (Large)', description='Noodles with tender chicken pieces', price=172, category='Chowmein', emoji='🍜', popularity=8),
            MenuItem(name='Hakka Noodles', description='Chinese style hakka noodles with vegetables', price=68, category='Chowmein', emoji='🍜', popularity=7),
            MenuItem(name='Hakka Noodles (Large)', description='Chinese style hakka noodles with vegetables', price=126, category='Chowmein', emoji='🍜', popularity=7),
            MenuItem(name='Schezwan Noodles', description='Spicy schezwan sauce noodles with vegetables', price=80, category='Chowmein', emoji='🍜', popularity=8),
            MenuItem(name='Schezwan Noodles (Large)', description='Spicy schezwan sauce noodles with vegetables', price=149, category='Chowmein', emoji='🍜', popularity=8),
            MenuItem(name='Singapore Noodles', description='Singapore style curry flavored noodles', price=103, category='Chowmein', emoji='🍜', popularity=6),
            MenuItem(name='Singapore Noodles (Large)', description='Singapore style curry flavored noodles', price=183, category='Chowmein', emoji='🍜', popularity=6),
            MenuItem(name='American Chop Suey', description='Crispy noodles with sweet and sour sauce', price=114, category='Chowmein', emoji='🍜', popularity=7),
            MenuItem(name='Chicken Hakka Noodles', description='Hakka noodles with chicken pieces', price=103, category='Chowmein', emoji='🍜', popularity=8),
            MenuItem(name='Chicken Hakka Noodles (Large)', description='Hakka noodles with chicken pieces', price=183, category='Chowmein', emoji='🍜', popularity=8),
            MenuItem(name='Chicken Schezwan Noodles', description='Spicy schezwan noodles with chicken', price=114, category='Chowmein', emoji='🍜', popularity=9),
            MenuItem(name='Chicken Schezwan Noodles (Large)', description='Spicy schezwan noodles with chicken', price=206, category='Chowmein', emoji='🍜', popularity=9),
            MenuItem(name='Mixed Noodles', description='Noodles with chicken, egg and vegetables', price=126, category='Chowmein', emoji='🍜', popularity=8),
            MenuItem(name='Mixed Noodles (Large)', description='Noodles with chicken, egg and vegetables', price=218, category='Chowmein', emoji='🍜', popularity=8),
            MenuItem(name='Mushroom Noodles', description='Noodles with fresh mushrooms', price=80, category='Chowmein', emoji='🍜', popularity=6),
            MenuItem(name='Triple Schezwan Rice', description='Schezwan rice with noodles and manchurian', price=172, category='Chowmein', emoji='🍜', popularity=7),
            MenuItem(name='Garlic Noodles', description='Stir-fried noodles with garlic flavor', price=91, category='Chowmein', emoji='🍜', popularity=6),
            MenuItem(name='Hong Kong Noodles', description='Crispy noodles with gravy topping', price=137, category='Chowmein', emoji='🍜', popularity=6),

            # BREAD - Expanded varieties
            MenuItem(name='Plain Roti', description='Fresh wheat bread', price=14, category='Bread', emoji='🍞', popularity=8),
            MenuItem(name='Butter Roti', description='Roti with butter', price=18, category='Bread', emoji='🍞', popularity=7),
            MenuItem(name='Plain Naan', description='Traditional Indian bread', price=29, category='Bread', emoji='🫓', popularity=9),
            MenuItem(name='Butter Naan', description='Naan with butter', price=41, category='Bread', emoji='🫓', popularity=9),
            MenuItem(name='Garlic Naan', description='Naan with garlic and herbs', price=57, category='Bread', emoji='🫓', popularity=8),
            MenuItem(name='Cheese Naan', description='Naan stuffed with cheese', price=80, category='Bread', emoji='🫓', popularity=8),
            MenuItem(name='Keema Naan', description='Naan stuffed with spiced minced meat', price=103, category='Bread', emoji='🫓', popularity=7),
            MenuItem(name='Peshawari Naan', description='Sweet naan with nuts and coconut', price=91, category='Bread', emoji='🫓', popularity=6),
            MenuItem(name='Lachha Paratha', description='Layered wheat bread', price=34, category='Bread', emoji='🫓', popularity=7),
            MenuItem(name='Aloo Paratha', description='Paratha stuffed with spiced potatoes', price=45, category='Bread', emoji='🫓', popularity=8),
            MenuItem(name='Gobi Paratha', description='Paratha stuffed with cauliflower', price=52, category='Bread', emoji='🫓', popularity=7),
            MenuItem(name='Paneer Paratha', description='Paratha stuffed with cottage cheese', price=68, category='Bread', emoji='🫓', popularity=8),
            MenuItem(name='Mix Veg Paratha', description='Paratha with mixed vegetable stuffing', price=57, category='Bread', emoji='🫓', popularity=7),
            MenuItem(name='Kulcha', description='Punjabi style leavened bread', price=41, category='Bread', emoji='🫓', popularity=6),
            MenuItem(name='Bhatura', description='Deep fried puffed bread', price=52, category='Bread', emoji='🫓', popularity=7),
            MenuItem(name='Roomali Roti', description='Thin handkerchief bread', price=29, category='Bread', emoji='🫓', popularity=6),
            MenuItem(name='Tandoori Roti', description='Clay oven baked wheat bread', price=21, category='Bread', emoji='🫓', popularity=7),

            # RICE - Expanded varieties  
            MenuItem(name='Plain Rice', description='Steamed basmati rice', price=80, category='Rice', emoji='🍚', popularity=6),
            MenuItem(name='Jeera Rice', description='Cumin flavored rice', price=91, category='Rice', emoji='🍚', popularity=6),
            MenuItem(name='Veg Fried Rice', description='Rice with mixed vegetables', price=91, category='Rice', emoji='🍚', popularity=7),
            MenuItem(name='Egg Fried Rice', description='Rice with scrambled eggs', price=103, category='Rice', emoji='🍚', popularity=7),
            MenuItem(name='Chicken Fried Rice', description='Rice with chicken pieces', price=114, category='Rice', emoji='🍚', popularity=8),
            MenuItem(name='Schezwan Rice', description='Spicy rice with schezwan sauce', price=114, category='Rice', emoji='🍚', popularity=5),
            MenuItem(name='Mix Fried Rice', description='Rice with chicken, egg and vegetables', price=137, category='Rice', emoji='🍚', popularity=6),
            MenuItem(name='Mushroom Rice', description='Rice with fresh mushrooms', price=103, category='Rice', emoji='🍚', popularity=5),
            MenuItem(name='Paneer Fried Rice', description='Rice with paneer cubes', price=126, category='Rice', emoji='🍚', popularity=6),
            MenuItem(name='Prawn Fried Rice', description='Rice with prawns and vegetables', price=160, category='Rice', emoji='🍚', popularity=7),
            MenuItem(name='Singapore Rice', description='Singapore style curry rice', price=126, category='Rice', emoji='🍚', popularity=5),
            MenuItem(name='Kashmiri Pulao', description='Aromatic rice with nuts and fruits', price=149, category='Rice', emoji='🍚', popularity=6),
            MenuItem(name='Coconut Rice', description='Rice cooked with coconut and spices', price=114, category='Rice', emoji='🍚', popularity=5),
            MenuItem(name='Lemon Rice', description='Tangy rice with curry leaves', price=91, category='Rice', emoji='🍚', popularity=6),
            MenuItem(name='Curd Rice', description='Rice mixed with fresh yogurt', price=80, category='Rice', emoji='🍚', popularity=5),
            MenuItem(name='Mutton Fried Rice', description='Rice with tender mutton pieces', price=172, category='Rice', emoji='🍚', popularity=7),

            # STARTERS - Expanded varieties
            MenuItem(name='Chilli Potato', description='Crispy potato with spicy sauce', price=80, category='Starters', emoji='🥔', popularity=8),
            MenuItem(name='Chilli Potato (Large)', description='Crispy potato with spicy sauce', price=149, category='Starters', emoji='🥔', popularity=8),
            MenuItem(name='Honey Chilli Potato', description='Sweet and spicy potato', price=103, category='Starters', emoji='🥔', popularity=7),
            MenuItem(name='Honey Chilli Potato (Large)', description='Sweet and spicy potato', price=195, category='Starters', emoji='🥔', popularity=7),
            MenuItem(name='Veg Manchurian', description='Deep fried vegetable balls', price=57, category='Starters', emoji='🥗', popularity=6),
            MenuItem(name='Veg Manchurian (Large)', description='Deep fried vegetable balls', price=114, category='Starters', emoji='🥗', popularity=6),
            MenuItem(name='Paneer Manchurian', description='Paneer cubes in manchurian sauce', price=103, category='Starters', emoji='🧀', popularity=7),
            MenuItem(name='Paneer Manchurian (Large)', description='Paneer cubes in manchurian sauce', price=195, category='Starters', emoji='🧀', popularity=7),
            MenuItem(name='Chicken Manchurian', description='Chicken pieces in spicy sauce', price=137, category='Starters', emoji='🍗', popularity=9),
            MenuItem(name='Chicken Manchurian (Large)', description='Chicken pieces in spicy sauce', price=241, category='Starters', emoji='🍗', popularity=9),
            MenuItem(name='Paneer Chilli', description='Spicy paneer cubes', price=229, category='Starters', emoji='🧀', popularity=7),
            MenuItem(name='Chicken Chilli', description='Spicy chicken preparation', price=264, category='Starters', emoji='🍗', popularity=9),
            MenuItem(name='Boneless Chilli', description='Boneless chicken in spicy sauce', price=287, category='Starters', emoji='🍗', popularity=8),
            MenuItem(name='Paneer Tikka', description='Grilled paneer cubes', price=229, category='Starters', emoji='🧀', popularity=8),
            MenuItem(name='Malai Paneer Tikka', description='Creamy paneer tikka', price=264, category='Starters', emoji='🧀', popularity=7),
            MenuItem(name='Chicken Tikka', description='Tandoor grilled chicken pieces', price=252, category='Starters', emoji='🍗', popularity=9),
            MenuItem(name='Chicken Malai Tikka', description='Creamy chicken tikka', price=275, category='Starters', emoji='🍗', popularity=8),
            MenuItem(name='Chicken Lollipop', description='Chicken drumettes in spicy coating', price=229, category='Starters', emoji='🍗', popularity=8),
            MenuItem(name='Chicken 65', description='South Indian spicy chicken starter', price=252, category='Starters', emoji='🍗', popularity=9),
            MenuItem(name='Fish Tikka', description='Grilled fish with Indian spices', price=287, category='Starters', emoji='🐟', popularity=7),
            MenuItem(name='Fish Finger', description='Crispy fried fish fingers', price=264, category='Starters', emoji='🐟', popularity=6),
            MenuItem(name='Prawn Koliwada', description='Bombay style fried prawns', price=321, category='Starters', emoji='🦐', popularity=7),
            MenuItem(name='Crispy Baby Corn', description='Crispy baby corn with sauce', price=172, category='Starters', emoji='🌽', popularity=5),
            MenuItem(name='Baby Corn Chilli', description='Spicy baby corn preparation', price=218, category='Starters', emoji='🌽', popularity=5),
            MenuItem(name='Mushroom Pepper Dry', description='Stir-fried mushrooms with black pepper', price=206, category='Starters', emoji='🍄', popularity=6),
            MenuItem(name='Chicken Pepper Dry', description='Dry chicken with black pepper', price=275, category='Starters', emoji='🍗', popularity=8),
            MenuItem(name='Mutton Pepper Dry', description='Dry mutton with black pepper', price=321, category='Starters', emoji='🥩', popularity=7),
            MenuItem(name='Chicken Wings', description='Spicy chicken wings', price=229, category='Starters', emoji='🍗', popularity=8),

            # MAIN COURSE - Expanded varieties
            MenuItem(name='Dal Tadka', description='Yellow lentils with tempering', price=137, category='Main Course', emoji='🍛', popularity=7),
            MenuItem(name='Dal Makhni', description='Creamy black lentils', price=160, category='Main Course', emoji='🍛', popularity=8),
            MenuItem(name='Dal Fry', description='Simple fried lentils', price=114, category='Main Course', emoji='🍛', popularity=6),
            MenuItem(name='Chana Masala', description='Spiced chickpeas curry', price=137, category='Main Course', emoji='🍛', popularity=6),
            MenuItem(name='Rajma Masala', description='Red kidney beans curry', price=149, category='Main Course', emoji='🍛', popularity=7),
            MenuItem(name='Shahi Paneer', description='Paneer in rich tomato gravy', price=229, category='Main Course', emoji='🧀', popularity=9),
            MenuItem(name='Kadhai Paneer', description='Paneer cooked in kadhai style', price=229, category='Main Course', emoji='🧀', popularity=8),
            MenuItem(name='Paneer Butter Masala', description='Paneer in buttery tomato sauce', price=229, category='Main Course', emoji='🧀', popularity=9),
            MenuItem(name='Handi Paneer', description='Paneer cooked in clay pot style', price=241, category='Main Course', emoji='🧀', popularity=7),
            MenuItem(name='Palak Paneer', description='Paneer with spinach gravy', price=218, category='Main Course', emoji='🧀', popularity=8),
            MenuItem(name='Matar Paneer', description='Paneer with green peas curry', price=206, category='Main Course', emoji='🧀', popularity=7),
            MenuItem(name='Paneer Do Pyaza', description='Paneer with onions curry', price=218, category='Main Course', emoji='🧀', popularity=6),
            MenuItem(name='Kadhai Chicken', description='Chicken cooked kadhai style', price=287, category='Main Course', emoji='🍗', popularity=9),
            MenuItem(name='Butter Chicken', description='Chicken in creamy tomato sauce', price=310, category='Main Course', emoji='🍗', popularity=10),
            MenuItem(name='Chicken Curry', description='Traditional chicken curry', price=275, category='Main Course', emoji='🍗', popularity=8),
            MenuItem(name='Chicken Masala', description='Spiced chicken gravy', price=287, category='Main Course', emoji='🍗', popularity=8),
            MenuItem(name='Palak Chicken', description='Chicken with spinach gravy', price=298, category='Main Course', emoji='🍗', popularity=7),
            MenuItem(name='Chicken Do Pyaza', description='Chicken with onions curry', price=287, category='Main Course', emoji='🍗', popularity=7),
            MenuItem(name='Mutton Curry', description='Traditional mutton curry', price=344, category='Main Course', emoji='🥩', popularity=8),
            MenuItem(name='Mutton Masala', description='Spiced mutton gravy', price=367, category='Main Course', emoji='🥩', popularity=8),
            MenuItem(name='Keema Curry', description='Spiced minced meat curry', price=298, category='Main Course', emoji='🥩', popularity=7),
            MenuItem(name='Fish Curry', description='Traditional fish curry', price=275, category='Main Course', emoji='🐟', popularity=7),
            MenuItem(name='Prawn Curry', description='Spiced prawn curry', price=321, category='Main Course', emoji='🦐', popularity=7),
            MenuItem(name='Mushroom Masala', description='Mushrooms in spiced gravy', price=218, category='Main Course', emoji='🍄', popularity=5),
            MenuItem(name='Mushroom Curry', description='Mushroom curry with spices', price=218, category='Main Course', emoji='🍄', popularity=5),
            MenuItem(name='Mixed Veg Curry', description='Mixed vegetables in curry', price=172, category='Main Course', emoji='🥗', popularity=6),
            MenuItem(name='Aloo Gobi', description='Potato and cauliflower curry', price=149, category='Main Course', emoji='🥔', popularity=6),
            MenuItem(name='Bhindi Masala', description='Spiced okra curry', price=160, category='Main Course', emoji='🌶️', popularity=5),
            MenuItem(name='Baingan Bharta', description='Roasted eggplant curry', price=172, category='Main Course', emoji='🍆', popularity=5),

            # BEVERAGES - New category
            MenuItem(name='Masala Chai', description='Traditional Indian spiced tea', price=18, category='Beverages', emoji='☕', popularity=9),
            MenuItem(name='Coffee', description='Hot brewed coffee', price=23, category='Beverages', emoji='☕', popularity=8),
            MenuItem(name='Green Tea', description='Healthy green tea', price=29, category='Beverages', emoji='🍵', popularity=6),
            MenuItem(name='Cold Coffee', description='Iced coffee with milk', price=52, category='Beverages', emoji='🥤', popularity=7),
            MenuItem(name='Lassi (Sweet)', description='Sweet yogurt drink', price=41, category='Beverages', emoji='🥤', popularity=8),
            MenuItem(name='Lassi (Salt)', description='Salted yogurt drink', price=41, category='Beverages', emoji='🥤', popularity=7),
            MenuItem(name='Mango Lassi', description='Mango flavored yogurt drink', price=57, category='Beverages', emoji='🥤', popularity=9),
            MenuItem(name='Fresh Lime Soda', description='Fresh lime with soda', price=34, category='Beverages', emoji='🥤', popularity=7),
            MenuItem(name='Fresh Lime Water', description='Fresh lime with water', price=29, category='Beverages', emoji='🥤', popularity=6),
            MenuItem(name='Buttermilk', description='Spiced buttermilk', price=29, category='Beverages', emoji='🥤', popularity=6),
            MenuItem(name='Mango Shake', description='Fresh mango milkshake', price=68, category='Beverages', emoji='🥤', popularity=8),
            MenuItem(name='Banana Shake', description='Fresh banana milkshake', price=57, category='Beverages', emoji='🥤', popularity=7),
            MenuItem(name='Chocolate Shake', description='Rich chocolate milkshake', price=68, category='Beverages', emoji='🥤', popularity=8),
            MenuItem(name='Vanilla Shake', description='Creamy vanilla milkshake', price=64, category='Beverages', emoji='🥤', popularity=7),
            MenuItem(name='Strawberry Shake', description='Fresh strawberry milkshake', price=68, category='Beverages', emoji='🥤', popularity=7),
            MenuItem(name='Soft Drinks', description='Assorted cold drinks', price=29, category='Beverages', emoji='🥤', popularity=8),
            MenuItem(name='Mineral Water', description='Packaged drinking water', price=18, category='Beverages', emoji='💧', popularity=5),
            MenuItem(name='Lemon Iced Tea', description='Refreshing lemon iced tea', price=45, category='Beverages', emoji='🧊', popularity=6),
            MenuItem(name='Fresh Orange Juice', description='Freshly squeezed orange juice', price=57, category='Beverages', emoji='🍊', popularity=7),

            # DESSERTS - New category
            MenuItem(name='Gulab Jamun', description='Sweet milk balls in sugar syrup (2 pcs)', price=57, category='Desserts', emoji='🍯', popularity=9),
            MenuItem(name='Rasmalai', description='Cottage cheese dumplings in milk (2 pcs)', price=80, category='Desserts', emoji='🍯', popularity=8),
            MenuItem(name='Ras Gulla', description='Spongy cottage cheese balls (2 pcs)', price=45, category='Desserts', emoji='🍯', popularity=7),
            MenuItem(name='Kheer', description='Traditional rice pudding', price=68, category='Desserts', emoji='🍯', popularity=8),
            MenuItem(name='Gajar Halwa', description='Carrot pudding with nuts', price=91, category='Desserts', emoji='🍯', popularity=7),
            MenuItem(name='Ice Cream', description='Assorted flavors ice cream', price=57, category='Desserts', emoji='🍦', popularity=8),
            MenuItem(name='Kulfi', description='Traditional Indian ice cream', price=45, category='Desserts', emoji='🍦', popularity=7),
            MenuItem(name='Falooda', description='Rose flavored dessert drink', price=91, category='Desserts', emoji='🍨', popularity=6),
            MenuItem(name='Jalebi', description='Crispy sweet spirals (100g)', price=68, category='Desserts', emoji='🍯', popularity=8),
            MenuItem(name='Rabri', description='Thickened sweet milk', price=80, category='Desserts', emoji='🍯', popularity=6),
            MenuItem(name='Chocolate Brownie', description='Rich chocolate brownie with ice cream', price=103, category='Desserts', emoji='🍫', popularity=7),
            MenuItem(name='Moong Dal Halwa', description='Sweet lentil pudding', price=91, category='Desserts', emoji='🍯', popularity=6),

            # SOUPS - New category
            MenuItem(name='Tomato Soup', description='Fresh tomato soup with herbs', price=57, category='Soups', emoji='🍅', popularity=7),
            MenuItem(name='Sweet Corn Soup', description='Creamy sweet corn soup', price=68, category='Soups', emoji='🌽', popularity=8),
            MenuItem(name='Hot & Sour Soup', description='Spicy and tangy soup', price=80, category='Soups', emoji='🍲', popularity=7),
            MenuItem(name='Manchow Soup', description='Chinese style vegetable soup', price=91, category='Soups', emoji='🍲', popularity=6),
            MenuItem(name='Chicken Soup', description='Clear chicken soup with herbs', price=103, category='Soups', emoji='🍲', popularity=8),
            MenuItem(name='Chicken Sweet Corn Soup', description='Chicken and sweet corn soup', price=114, category='Soups', emoji='🍲', popularity=8),
            MenuItem(name='Chicken Hot & Sour Soup', description='Spicy chicken soup', price=126, category='Soups', emoji='🍲', popularity=7),
            MenuItem(name='Chicken Manchow Soup', description='Chinese style chicken soup', price=137, category='Soups', emoji='🍲', popularity=7),
            MenuItem(name='Mushroom Soup', description='Creamy mushroom soup', price=91, category='Soups', emoji='🍄', popularity=6),
            MenuItem(name='Veg Clear Soup', description='Light vegetable clear soup', price=57, category='Soups', emoji='🥗', popularity=5),
        ]
        
        for item in menu_items:
            db.session.add(item)
        
        try:
            db.session.commit()
            print("Complete menu items added")
            
            # Add sample promotions if none exist
            if Promotion.query.count() == 0:
                sample_promotions = [
                    Promotion(
                        code='WELCOME20',
                        description='Welcome Special - 20% off on first order',
                        discount_type='percentage',
                        discount_value=20,
                        min_order_amount=200,
                        max_discount=200,
                        usage_limit=None,
                        expires_at=None,
                        is_active=True
                    ),
                    Promotion(
                        code='SAVE50',
                        description='Get flat ₹50 off on orders above ₹300',
                        discount_type='fixed',
                        discount_value=50,
                        min_order_amount=300,
                        max_discount=None,
                        usage_limit=None,
                        expires_at=None,
                        is_active=True
                    ),
                    Promotion(
                        code='BIRYANI20',
                        description='Special biryani discount - 20% off',
                        discount_type='percentage',
                        discount_value=20,
                        min_order_amount=200,
                        max_discount=150,
                        usage_limit=100,
                        expires_at=None,
                        is_active=True
                    )
                ]
                
                for promo in sample_promotions:
                    db.session.add(promo)
                
                db.session.commit()
                print('Sample promotions added')
        except Exception as e:
            db.session.rollback()
            print(f"Error adding menu items: {e}")
    
    # Import routes after everything is initialized
    import routes
