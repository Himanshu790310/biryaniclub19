
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
            MenuItem(name='Veg Biryani', description='Fragrant basmati rice with mixed vegetables', price=99, category='Biryani', emoji='🍛', popularity=8),
            MenuItem(name='Veg Biryani (Large)', description='Fragrant basmati rice with mixed vegetables', price=189, category='Biryani', emoji='🍛', popularity=8),
            MenuItem(name='Egg Biryani', description='Aromatic rice with boiled eggs', price=109, category='Biryani', emoji='🍛', popularity=7),
            MenuItem(name='Egg Biryani (Large)', description='Aromatic rice with boiled eggs', price=199, category='Biryani', emoji='🍛', popularity=7),
            MenuItem(name='Paneer Biryani', description='Premium paneer pieces with fragrant rice', price=129, category='Biryani', emoji='🍛', popularity=9),
            MenuItem(name='Paneer Biryani (Large)', description='Premium paneer pieces with fragrant rice', price=239, category='Biryani', emoji='🍛', popularity=9),
            MenuItem(name='Mushroom Biryani', description='Fresh mushrooms with spiced rice', price=109, category='Biryani', emoji='🍛', popularity=6),
            MenuItem(name='Mushroom Biryani (Large)', description='Fresh mushrooms with spiced rice', price=199, category='Biryani', emoji='🍛', popularity=6),
            MenuItem(name='Chicken Biryani', description='Tender chicken pieces with aromatic rice', price=119, category='Biryani', emoji='🍛', popularity=10),
            MenuItem(name='Chicken Biryani (Large)', description='Tender chicken pieces with aromatic rice', price=219, category='Biryani', emoji='🍛', popularity=10),
            MenuItem(name='Chicken Biryani (Premium)', description='Premium chicken biryani with extra spices', price=139, category='Biryani', emoji='🍛', popularity=10),
            MenuItem(name='Chicken Biryani (Premium Large)', description='Premium chicken biryani with extra spices', price=249, category='Biryani', emoji='🍛', popularity=10),
            MenuItem(name='Mutton Biryani', description='Tender mutton pieces with aromatic basmati rice', price=179, category='Biryani', emoji='🍛', popularity=9),
            MenuItem(name='Mutton Biryani (Large)', description='Tender mutton pieces with aromatic basmati rice', price=329, category='Biryani', emoji='🍛', popularity=9),
            MenuItem(name='Keema Biryani', description='Spiced minced meat with fragrant rice', price=149, category='Biryani', emoji='🍛', popularity=8),
            MenuItem(name='Keema Biryani (Large)', description='Spiced minced meat with fragrant rice', price=279, category='Biryani', emoji='🍛', popularity=8),
            MenuItem(name='Fish Biryani', description='Fresh fish pieces with aromatic rice', price=159, category='Biryani', emoji='🍛', popularity=7),
            MenuItem(name='Fish Biryani (Large)', description='Fresh fish pieces with aromatic rice', price=299, category='Biryani', emoji='🍛', popularity=7),
            MenuItem(name='Prawn Biryani', description='Succulent prawns with spiced basmati rice', price=189, category='Biryani', emoji='🍛', popularity=8),
            MenuItem(name='Prawn Biryani (Large)', description='Succulent prawns with spiced basmati rice', price=349, category='Biryani', emoji='🍛', popularity=8),
            MenuItem(name='Hyderabadi Biryani', description='Traditional Hyderabadi style chicken biryani', price=169, category='Biryani', emoji='🍛', popularity=9),
            MenuItem(name='Hyderabadi Biryani (Large)', description='Traditional Hyderabadi style chicken biryani', price=319, category='Biryani', emoji='🍛', popularity=9),
            MenuItem(name='Awadhi Biryani', description='Lucknowi style aromatic biryani with chicken', price=159, category='Biryani', emoji='🍛', popularity=8),
            MenuItem(name='Awadhi Biryani (Large)', description='Lucknowi style aromatic biryani with chicken', price=299, category='Biryani', emoji='🍛', popularity=8),
            MenuItem(name='Dum Biryani', description='Slow cooked dum style chicken biryani', price=149, category='Biryani', emoji='🍛', popularity=9),
            MenuItem(name='Dum Biryani (Large)', description='Slow cooked dum style chicken biryani', price=289, category='Biryani', emoji='🍛', popularity=9),
            MenuItem(name='Kolkata Biryani', description='Bengali style biryani with potato and chicken', price=139, category='Biryani', emoji='🍛', popularity=7),
            MenuItem(name='Kolkata Biryani (Large)', description='Bengali style biryani with potato and chicken', price=269, category='Biryani', emoji='🍛', popularity=7),

            # ROLLS - Separated and expanded
            MenuItem(name='Veg Roll', description='Fresh vegetables wrapped in soft paratha', price=29, category='Rolls', emoji='🌯', popularity=7),
            MenuItem(name='Egg Roll', description='Scrambled eggs with onions in paratha wrap', price=39, category='Rolls', emoji='🌯', popularity=8),
            MenuItem(name='Paneer Roll', description='Spiced paneer cubes in soft roll', price=79, category='Rolls', emoji='🌯', popularity=6),
            MenuItem(name='Chicken Roll', description='Tender chicken pieces in paratha wrap', price=89, category='Rolls', emoji='🌯', popularity=9),
            MenuItem(name='Mutton Roll', description='Spiced mutton pieces wrapped in paratha', price=119, category='Rolls', emoji='🌯', popularity=8),
            MenuItem(name='Seekh Kebab Roll', description='Grilled seekh kebab wrapped in rumali roti', price=99, category='Rolls', emoji='🌯', popularity=9),
            MenuItem(name='Chicken Tikka Roll', description='Tandoor chicken tikka in naan wrap', price=109, category='Rolls', emoji='🌯', popularity=10),
            MenuItem(name='Aloo Roll', description='Spiced potato filling in soft paratha', price=25, category='Rolls', emoji='🌯', popularity=6),
            MenuItem(name='Masala Roll', description='Mixed vegetables with Indian spices', price=35, category='Rolls', emoji='🌯', popularity=7),
            MenuItem(name='Fish Roll', description='Fried fish pieces in paratha wrap', price=89, category='Rolls', emoji='🌯', popularity=6),
            MenuItem(name='Reshmi Kebab Roll', description='Soft chicken reshmi kebab in roomali roti', price=119, category='Rolls', emoji='🌯', popularity=8),
            MenuItem(name='Kathi Roll', description='Kolkata style chicken kathi roll', price=95, category='Rolls', emoji='🌯', popularity=9),
            MenuItem(name='Cheese Roll', description='Melted cheese with vegetables in roll', price=69, category='Rolls', emoji='🌯', popularity=7),
            MenuItem(name='Chicken Schezwan Roll', description='Spicy schezwan chicken roll', price=99, category='Rolls', emoji='🌯', popularity=8),
            MenuItem(name='Paneer Tikka Roll', description='Grilled paneer tikka in naan wrap', price=89, category='Rolls', emoji='🌯', popularity=7),
            MenuItem(name='Mushroom Roll', description='Sautéed mushrooms in soft paratha', price=59, category='Rolls', emoji='🌯', popularity=5),
            MenuItem(name='Double Egg Roll', description='Double portion of scrambled eggs in roll', price=59, category='Rolls', emoji='🌯', popularity=8),
            MenuItem(name='Chicken Keema Roll', description='Spiced chicken mince in paratha wrap', price=99, category='Rolls', emoji='🌯', popularity=8),
            MenuItem(name='Mutton Keema Roll', description='Spiced mutton mince in paratha wrap', price=119, category='Rolls', emoji='🌯', popularity=7),
            MenuItem(name='Chicken Malai Roll', description='Creamy chicken malai tikka roll', price=109, category='Rolls', emoji='🌯', popularity=8),
            MenuItem(name='Chicken 65 Roll', description='Spicy chicken 65 wrapped in paratha', price=105, category='Rolls', emoji='🌯', popularity=9),
            MenuItem(name='Prawn Roll', description='Fried prawns in soft paratha wrap', price=129, category='Rolls', emoji='🌯', popularity=6),

            # CHOWMEIN - Separated and expanded
            MenuItem(name='Veg Chowmein', description='Stir-fried noodles with mixed vegetables', price=49, category='Chowmein', emoji='🍜', popularity=6),
            MenuItem(name='Veg Chowmein (Large)', description='Stir-fried noodles with mixed vegetables', price=99, category='Chowmein', emoji='🍜', popularity=6),
            MenuItem(name='Paneer Chowmein', description='Noodles with paneer cubes and vegetables', price=59, category='Chowmein', emoji='🍜', popularity=5),
            MenuItem(name='Paneer Chowmein (Large)', description='Noodles with paneer cubes and vegetables', price=109, category='Chowmein', emoji='🍜', popularity=5),
            MenuItem(name='Egg Chowmein', description='Egg noodles with scrambled eggs', price=49, category='Chowmein', emoji='🍜', popularity=7),
            MenuItem(name='Egg Chowmein (Large)', description='Egg noodles with scrambled eggs', price=99, category='Chowmein', emoji='🍜', popularity=7),
            MenuItem(name='Chicken Chowmein', description='Noodles with tender chicken pieces', price=79, category='Chowmein', emoji='🍜', popularity=8),
            MenuItem(name='Chicken Chowmein (Large)', description='Noodles with tender chicken pieces', price=149, category='Chowmein', emoji='🍜', popularity=8),
            MenuItem(name='Hakka Noodles', description='Chinese style hakka noodles with vegetables', price=59, category='Chowmein', emoji='🍜', popularity=7),
            MenuItem(name='Hakka Noodles (Large)', description='Chinese style hakka noodles with vegetables', price=109, category='Chowmein', emoji='🍜', popularity=7),
            MenuItem(name='Schezwan Noodles', description='Spicy schezwan sauce noodles with vegetables', price=69, category='Chowmein', emoji='🍜', popularity=8),
            MenuItem(name='Schezwan Noodles (Large)', description='Spicy schezwan sauce noodles with vegetables', price=129, category='Chowmein', emoji='🍜', popularity=8),
            MenuItem(name='Singapore Noodles', description='Singapore style curry flavored noodles', price=89, category='Chowmein', emoji='🍜', popularity=6),
            MenuItem(name='Singapore Noodles (Large)', description='Singapore style curry flavored noodles', price=159, category='Chowmein', emoji='🍜', popularity=6),
            MenuItem(name='American Chop Suey', description='Crispy noodles with sweet and sour sauce', price=99, category='Chowmein', emoji='🍜', popularity=7),
            MenuItem(name='Chicken Hakka Noodles', description='Hakka noodles with chicken pieces', price=89, category='Chowmein', emoji='🍜', popularity=8),
            MenuItem(name='Chicken Hakka Noodles (Large)', description='Hakka noodles with chicken pieces', price=159, category='Chowmein', emoji='🍜', popularity=8),
            MenuItem(name='Chicken Schezwan Noodles', description='Spicy schezwan noodles with chicken', price=99, category='Chowmein', emoji='🍜', popularity=9),
            MenuItem(name='Chicken Schezwan Noodles (Large)', description='Spicy schezwan noodles with chicken', price=179, category='Chowmein', emoji='🍜', popularity=9),
            MenuItem(name='Mixed Noodles', description='Noodles with chicken, egg and vegetables', price=109, category='Chowmein', emoji='🍜', popularity=8),
            MenuItem(name='Mixed Noodles (Large)', description='Noodles with chicken, egg and vegetables', price=189, category='Chowmein', emoji='🍜', popularity=8),
            MenuItem(name='Mushroom Noodles', description='Noodles with fresh mushrooms', price=69, category='Chowmein', emoji='🍜', popularity=6),
            MenuItem(name='Triple Schezwan Rice', description='Schezwan rice with noodles and manchurian', price=149, category='Chowmein', emoji='🍜', popularity=7),
            MenuItem(name='Garlic Noodles', description='Stir-fried noodles with garlic flavor', price=79, category='Chowmein', emoji='🍜', popularity=6),
            MenuItem(name='Hong Kong Noodles', description='Crispy noodles with gravy topping', price=119, category='Chowmein', emoji='🍜', popularity=6),

            # BREAD - Expanded varieties
            MenuItem(name='Plain Roti', description='Fresh wheat bread', price=12, category='Bread', emoji='🍞', popularity=8),
            MenuItem(name='Butter Roti', description='Roti with butter', price=15, category='Bread', emoji='🍞', popularity=7),
            MenuItem(name='Plain Naan', description='Traditional Indian bread', price=25, category='Bread', emoji='🫓', popularity=9),
            MenuItem(name='Butter Naan', description='Naan with butter', price=35, category='Bread', emoji='🫓', popularity=9),
            MenuItem(name='Garlic Naan', description='Naan with garlic and herbs', price=49, category='Bread', emoji='🫓', popularity=8),
            MenuItem(name='Cheese Naan', description='Naan stuffed with cheese', price=69, category='Bread', emoji='🫓', popularity=8),
            MenuItem(name='Keema Naan', description='Naan stuffed with spiced minced meat', price=89, category='Bread', emoji='🫓', popularity=7),
            MenuItem(name='Peshawari Naan', description='Sweet naan with nuts and coconut', price=79, category='Bread', emoji='🫓', popularity=6),
            MenuItem(name='Lachha Paratha', description='Layered wheat bread', price=29, category='Bread', emoji='🫓', popularity=7),
            MenuItem(name='Aloo Paratha', description='Paratha stuffed with spiced potatoes', price=39, category='Bread', emoji='🫓', popularity=8),
            MenuItem(name='Gobi Paratha', description='Paratha stuffed with cauliflower', price=45, category='Bread', emoji='🫓', popularity=7),
            MenuItem(name='Paneer Paratha', description='Paratha stuffed with cottage cheese', price=59, category='Bread', emoji='🫓', popularity=8),
            MenuItem(name='Mix Veg Paratha', description='Paratha with mixed vegetable stuffing', price=49, category='Bread', emoji='🫓', popularity=7),
            MenuItem(name='Kulcha', description='Punjabi style leavened bread', price=35, category='Bread', emoji='🫓', popularity=6),
            MenuItem(name='Bhatura', description='Deep fried puffed bread', price=45, category='Bread', emoji='🫓', popularity=7),
            MenuItem(name='Roomali Roti', description='Thin handkerchief bread', price=25, category='Bread', emoji='🫓', popularity=6),
            MenuItem(name='Tandoori Roti', description='Clay oven baked wheat bread', price=18, category='Bread', emoji='🫓', popularity=7),

            # RICE - Expanded varieties  
            MenuItem(name='Plain Rice', description='Steamed basmati rice', price=69, category='Rice', emoji='🍚', popularity=6),
            MenuItem(name='Jeera Rice', description='Cumin flavored rice', price=79, category='Rice', emoji='🍚', popularity=6),
            MenuItem(name='Veg Fried Rice', description='Rice with mixed vegetables', price=79, category='Rice', emoji='🍚', popularity=7),
            MenuItem(name='Egg Fried Rice', description='Rice with scrambled eggs', price=89, category='Rice', emoji='🍚', popularity=7),
            MenuItem(name='Chicken Fried Rice', description='Rice with chicken pieces', price=99, category='Rice', emoji='🍚', popularity=8),
            MenuItem(name='Schezwan Rice', description='Spicy rice with schezwan sauce', price=99, category='Rice', emoji='🍚', popularity=5),
            MenuItem(name='Mix Fried Rice', description='Rice with chicken, egg and vegetables', price=119, category='Rice', emoji='🍚', popularity=6),
            MenuItem(name='Mushroom Rice', description='Rice with fresh mushrooms', price=89, category='Rice', emoji='🍚', popularity=5),
            MenuItem(name='Paneer Fried Rice', description='Rice with paneer cubes', price=109, category='Rice', emoji='🍚', popularity=6),
            MenuItem(name='Prawn Fried Rice', description='Rice with prawns and vegetables', price=139, category='Rice', emoji='🍚', popularity=7),
            MenuItem(name='Singapore Rice', description='Singapore style curry rice', price=109, category='Rice', emoji='🍚', popularity=5),
            MenuItem(name='Kashmiri Pulao', description='Aromatic rice with nuts and fruits', price=129, category='Rice', emoji='🍚', popularity=6),
            MenuItem(name='Coconut Rice', description='Rice cooked with coconut and spices', price=99, category='Rice', emoji='🍚', popularity=5),
            MenuItem(name='Lemon Rice', description='Tangy rice with curry leaves', price=79, category='Rice', emoji='🍚', popularity=6),
            MenuItem(name='Curd Rice', description='Rice mixed with fresh yogurt', price=69, category='Rice', emoji='🍚', popularity=5),
            MenuItem(name='Mutton Fried Rice', description='Rice with tender mutton pieces', price=149, category='Rice', emoji='🍚', popularity=7),

            # STARTERS - Expanded varieties
            MenuItem(name='Chilli Potato', description='Crispy potato with spicy sauce', price=69, category='Starters', emoji='🥔', popularity=8),
            MenuItem(name='Chilli Potato (Large)', description='Crispy potato with spicy sauce', price=129, category='Starters', emoji='🥔', popularity=8),
            MenuItem(name='Honey Chilli Potato', description='Sweet and spicy potato', price=89, category='Starters', emoji='🥔', popularity=7),
            MenuItem(name='Honey Chilli Potato (Large)', description='Sweet and spicy potato', price=169, category='Starters', emoji='🥔', popularity=7),
            MenuItem(name='Veg Manchurian', description='Deep fried vegetable balls', price=49, category='Starters', emoji='🥗', popularity=6),
            MenuItem(name='Veg Manchurian (Large)', description='Deep fried vegetable balls', price=99, category='Starters', emoji='🥗', popularity=6),
            MenuItem(name='Paneer Manchurian', description='Paneer cubes in manchurian sauce', price=89, category='Starters', emoji='🧀', popularity=7),
            MenuItem(name='Paneer Manchurian (Large)', description='Paneer cubes in manchurian sauce', price=169, category='Starters', emoji='🧀', popularity=7),
            MenuItem(name='Chicken Manchurian', description='Chicken pieces in spicy sauce', price=119, category='Starters', emoji='🍗', popularity=9),
            MenuItem(name='Chicken Manchurian (Large)', description='Chicken pieces in spicy sauce', price=209, category='Starters', emoji='🍗', popularity=9),
            MenuItem(name='Paneer Chilli', description='Spicy paneer cubes', price=199, category='Starters', emoji='🧀', popularity=7),
            MenuItem(name='Chicken Chilli', description='Spicy chicken preparation', price=229, category='Starters', emoji='🍗', popularity=9),
            MenuItem(name='Boneless Chilli', description='Boneless chicken in spicy sauce', price=249, category='Starters', emoji='🍗', popularity=8),
            MenuItem(name='Paneer Tikka', description='Grilled paneer cubes', price=199, category='Starters', emoji='🧀', popularity=8),
            MenuItem(name='Malai Paneer Tikka', description='Creamy paneer tikka', price=229, category='Starters', emoji='🧀', popularity=7),
            MenuItem(name='Chicken Tikka', description='Tandoor grilled chicken pieces', price=219, category='Starters', emoji='🍗', popularity=9),
            MenuItem(name='Chicken Malai Tikka', description='Creamy chicken tikka', price=239, category='Starters', emoji='🍗', popularity=8),
            MenuItem(name='Chicken Lollipop', description='Chicken drumettes in spicy coating', price=199, category='Starters', emoji='🍗', popularity=8),
            MenuItem(name='Chicken 65', description='South Indian spicy chicken starter', price=219, category='Starters', emoji='🍗', popularity=9),
            MenuItem(name='Fish Tikka', description='Grilled fish with Indian spices', price=249, category='Starters', emoji='🐟', popularity=7),
            MenuItem(name='Fish Finger', description='Crispy fried fish fingers', price=229, category='Starters', emoji='🐟', popularity=6),
            MenuItem(name='Prawn Koliwada', description='Bombay style fried prawns', price=279, category='Starters', emoji='🦐', popularity=7),
            MenuItem(name='Crispy Baby Corn', description='Crispy baby corn with sauce', price=149, category='Starters', emoji='🌽', popularity=5),
            MenuItem(name='Baby Corn Chilli', description='Spicy baby corn preparation', price=189, category='Starters', emoji='🌽', popularity=5),
            MenuItem(name='Mushroom Pepper Dry', description='Stir-fried mushrooms with black pepper', price=179, category='Starters', emoji='🍄', popularity=6),
            MenuItem(name='Chicken Pepper Dry', description='Dry chicken with black pepper', price=239, category='Starters', emoji='🍗', popularity=8),
            MenuItem(name='Mutton Pepper Dry', description='Dry mutton with black pepper', price=279, category='Starters', emoji='🥩', popularity=7),
            MenuItem(name='Chicken Wings', description='Spicy chicken wings', price=199, category='Starters', emoji='🍗', popularity=8),

            # MAIN COURSE - Expanded varieties
            MenuItem(name='Dal Tadka', description='Yellow lentils with tempering', price=119, category='Main Course', emoji='🍛', popularity=7),
            MenuItem(name='Dal Makhni', description='Creamy black lentils', price=139, category='Main Course', emoji='🍛', popularity=8),
            MenuItem(name='Dal Fry', description='Simple fried lentils', price=99, category='Main Course', emoji='🍛', popularity=6),
            MenuItem(name='Chana Masala', description='Spiced chickpeas curry', price=119, category='Main Course', emoji='🍛', popularity=6),
            MenuItem(name='Rajma Masala', description='Red kidney beans curry', price=129, category='Main Course', emoji='🍛', popularity=7),
            MenuItem(name='Shahi Paneer', description='Paneer in rich tomato gravy', price=199, category='Main Course', emoji='🧀', popularity=9),
            MenuItem(name='Kadhai Paneer', description='Paneer cooked in kadhai style', price=199, category='Main Course', emoji='🧀', popularity=8),
            MenuItem(name='Paneer Butter Masala', description='Paneer in buttery tomato sauce', price=199, category='Main Course', emoji='🧀', popularity=9),
            MenuItem(name='Handi Paneer', description='Paneer cooked in clay pot style', price=209, category='Main Course', emoji='🧀', popularity=7),
            MenuItem(name='Palak Paneer', description='Paneer with spinach gravy', price=189, category='Main Course', emoji='🧀', popularity=8),
            MenuItem(name='Matar Paneer', description='Paneer with green peas curry', price=179, category='Main Course', emoji='🧀', popularity=7),
            MenuItem(name='Paneer Do Pyaza', description='Paneer with onions curry', price=189, category='Main Course', emoji='🧀', popularity=6),
            MenuItem(name='Kadhai Chicken', description='Chicken cooked kadhai style', price=249, category='Main Course', emoji='🍗', popularity=9),
            MenuItem(name='Butter Chicken', description='Chicken in creamy tomato sauce', price=269, category='Main Course', emoji='🍗', popularity=10),
            MenuItem(name='Chicken Curry', description='Traditional chicken curry', price=239, category='Main Course', emoji='🍗', popularity=8),
            MenuItem(name='Chicken Masala', description='Spiced chicken gravy', price=249, category='Main Course', emoji='🍗', popularity=8),
            MenuItem(name='Palak Chicken', description='Chicken with spinach gravy', price=259, category='Main Course', emoji='🍗', popularity=7),
            MenuItem(name='Chicken Do Pyaza', description='Chicken with onions curry', price=249, category='Main Course', emoji='🍗', popularity=7),
            MenuItem(name='Mutton Curry', description='Traditional mutton curry', price=299, category='Main Course', emoji='🥩', popularity=8),
            MenuItem(name='Mutton Masala', description='Spiced mutton gravy', price=319, category='Main Course', emoji='🥩', popularity=8),
            MenuItem(name='Keema Curry', description='Spiced minced meat curry', price=259, category='Main Course', emoji='🥩', popularity=7),
            MenuItem(name='Fish Curry', description='Traditional fish curry', price=239, category='Main Course', emoji='🐟', popularity=7),
            MenuItem(name='Prawn Curry', description='Spiced prawn curry', price=279, category='Main Course', emoji='🦐', popularity=7),
            MenuItem(name='Mushroom Masala', description='Mushrooms in spiced gravy', price=189, category='Main Course', emoji='🍄', popularity=5),
            MenuItem(name='Mushroom Curry', description='Mushroom curry with spices', price=189, category='Main Course', emoji='🍄', popularity=5),
            MenuItem(name='Mixed Veg Curry', description='Mixed vegetables in curry', price=149, category='Main Course', emoji='🥗', popularity=6),
            MenuItem(name='Aloo Gobi', description='Potato and cauliflower curry', price=129, category='Main Course', emoji='🥔', popularity=6),
            MenuItem(name='Bhindi Masala', description='Spiced okra curry', price=139, category='Main Course', emoji='🌶️', popularity=5),
            MenuItem(name='Baingan Bharta', description='Roasted eggplant curry', price=149, category='Main Course', emoji='🍆', popularity=5),

            # BEVERAGES - New category
            MenuItem(name='Masala Chai', description='Traditional Indian spiced tea', price=15, category='Beverages', emoji='☕', popularity=9),
            MenuItem(name='Coffee', description='Hot brewed coffee', price=20, category='Beverages', emoji='☕', popularity=8),
            MenuItem(name='Green Tea', description='Healthy green tea', price=25, category='Beverages', emoji='🍵', popularity=6),
            MenuItem(name='Cold Coffee', description='Iced coffee with milk', price=45, category='Beverages', emoji='🥤', popularity=7),
            MenuItem(name='Lassi (Sweet)', description='Sweet yogurt drink', price=35, category='Beverages', emoji='🥤', popularity=8),
            MenuItem(name='Lassi (Salt)', description='Salted yogurt drink', price=35, category='Beverages', emoji='🥤', popularity=7),
            MenuItem(name='Mango Lassi', description='Mango flavored yogurt drink', price=49, category='Beverages', emoji='🥤', popularity=9),
            MenuItem(name='Fresh Lime Soda', description='Fresh lime with soda', price=29, category='Beverages', emoji='🥤', popularity=7),
            MenuItem(name='Fresh Lime Water', description='Fresh lime with water', price=25, category='Beverages', emoji='🥤', popularity=6),
            MenuItem(name='Buttermilk', description='Spiced buttermilk', price=25, category='Beverages', emoji='🥤', popularity=6),
            MenuItem(name='Mango Shake', description='Fresh mango milkshake', price=59, category='Beverages', emoji='🥤', popularity=8),
            MenuItem(name='Banana Shake', description='Fresh banana milkshake', price=49, category='Beverages', emoji='🥤', popularity=7),
            MenuItem(name='Chocolate Shake', description='Rich chocolate milkshake', price=59, category='Beverages', emoji='🥤', popularity=8),
            MenuItem(name='Vanilla Shake', description='Creamy vanilla milkshake', price=55, category='Beverages', emoji='🥤', popularity=7),
            MenuItem(name='Strawberry Shake', description='Fresh strawberry milkshake', price=59, category='Beverages', emoji='🥤', popularity=7),
            MenuItem(name='Soft Drinks', description='Assorted cold drinks', price=25, category='Beverages', emoji='🥤', popularity=8),
            MenuItem(name='Mineral Water', description='Packaged drinking water', price=15, category='Beverages', emoji='💧', popularity=5),
            MenuItem(name='Lemon Iced Tea', description='Refreshing lemon iced tea', price=39, category='Beverages', emoji='🧊', popularity=6),
            MenuItem(name='Fresh Orange Juice', description='Freshly squeezed orange juice', price=49, category='Beverages', emoji='🍊', popularity=7),

            # DESSERTS - New category
            MenuItem(name='Gulab Jamun', description='Sweet milk balls in sugar syrup (2 pcs)', price=49, category='Desserts', emoji='🍯', popularity=9),
            MenuItem(name='Rasmalai', description='Cottage cheese dumplings in milk (2 pcs)', price=69, category='Desserts', emoji='🍯', popularity=8),
            MenuItem(name='Ras Gulla', description='Spongy cottage cheese balls (2 pcs)', price=39, category='Desserts', emoji='🍯', popularity=7),
            MenuItem(name='Kheer', description='Traditional rice pudding', price=59, category='Desserts', emoji='🍯', popularity=8),
            MenuItem(name='Gajar Halwa', description='Carrot pudding with nuts', price=79, category='Desserts', emoji='🍯', popularity=7),
            MenuItem(name='Ice Cream', description='Assorted flavors ice cream', price=49, category='Desserts', emoji='🍦', popularity=8),
            MenuItem(name='Kulfi', description='Traditional Indian ice cream', price=39, category='Desserts', emoji='🍦', popularity=7),
            MenuItem(name='Falooda', description='Rose flavored dessert drink', price=79, category='Desserts', emoji='🍨', popularity=6),
            MenuItem(name='Jalebi', description='Crispy sweet spirals (100g)', price=59, category='Desserts', emoji='🍯', popularity=8),
            MenuItem(name='Rabri', description='Thickened sweet milk', price=69, category='Desserts', emoji='🍯', popularity=6),
            MenuItem(name='Chocolate Brownie', description='Rich chocolate brownie with ice cream', price=89, category='Desserts', emoji='🍫', popularity=7),
            MenuItem(name='Moong Dal Halwa', description='Sweet lentil pudding', price=79, category='Desserts', emoji='🍯', popularity=6),

            # SOUPS - New category
            MenuItem(name='Tomato Soup', description='Fresh tomato soup with herbs', price=49, category='Soups', emoji='🍅', popularity=7),
            MenuItem(name='Sweet Corn Soup', description='Creamy sweet corn soup', price=59, category='Soups', emoji='🌽', popularity=8),
            MenuItem(name='Hot & Sour Soup', description='Spicy and tangy soup', price=69, category='Soups', emoji='🍲', popularity=7),
            MenuItem(name='Manchow Soup', description='Chinese style vegetable soup', price=79, category='Soups', emoji='🍲', popularity=6),
            MenuItem(name='Chicken Soup', description='Clear chicken soup with herbs', price=89, category='Soups', emoji='🍲', popularity=8),
            MenuItem(name='Chicken Sweet Corn Soup', description='Chicken and sweet corn soup', price=99, category='Soups', emoji='🍲', popularity=8),
            MenuItem(name='Chicken Hot & Sour Soup', description='Spicy chicken soup', price=109, category='Soups', emoji='🍲', popularity=7),
            MenuItem(name='Chicken Manchow Soup', description='Chinese style chicken soup', price=119, category='Soups', emoji='🍲', popularity=7),
            MenuItem(name='Mushroom Soup', description='Creamy mushroom soup', price=79, category='Soups', emoji='🍄', popularity=6),
            MenuItem(name='Veg Clear Soup', description='Light vegetable clear soup', price=49, category='Soups', emoji='🥗', popularity=5),
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
                        code='WELCOME10',
                        description='Welcome offer - 10% off on first order',
                        discount_type='percentage',
                        discount_value=10,
                        min_order_amount=100,
                        max_discount=100,
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
