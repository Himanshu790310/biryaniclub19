import os
import uuid
from datetime import datetime
from werkzeug.utils import secure_filename
from PIL import Image

def allowed_file(filename, allowed_extensions):
    """Check if file has an allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def generate_unique_filename(original_filename):
    """Generate a unique filename while preserving the extension"""
    if not original_filename:
        return None
    
    # Get file extension
    ext = original_filename.rsplit('.', 1)[1].lower()
    # Generate unique filename with timestamp and UUID
    unique_id = str(uuid.uuid4())[:8]  # First 8 chars of UUID
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{timestamp}_{unique_id}.{ext}"

def save_menu_item_image(file, upload_folder, menu_item_id):
    """
    Save uploaded image for a menu item
    Returns: (success, filename_or_error_message)
    """
    try:
        if not file or file.filename == '':
            return False, "No file selected"
        
        # Check if file type is allowed
        allowed_extensions = {'jpg', 'jpeg', 'png', 'webp'}
        if not allowed_file(file.filename, allowed_extensions):
            return False, "Invalid file type. Please upload JPG, PNG, or WEBP images."
        
        # Generate unique filename
        filename = generate_unique_filename(file.filename)
        if not filename:
            return False, "Invalid filename"
        
        # Ensure upload directory exists
        os.makedirs(upload_folder, exist_ok=True)
        
        # Full file path
        file_path = os.path.join(upload_folder, filename)
        
        # Save the file
        file.save(file_path)
        
        # Optimize and resize image using PIL
        try:
            with Image.open(file_path) as img:
                # Convert to RGB if necessary (for JPEG compatibility)
                if img.mode in ('RGBA', 'LA', 'P'):
                    # Create white background
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode in ('RGBA', 'LA') else None)
                    img = background
                
                # Resize image to max 800x600 while maintaining aspect ratio
                max_size = (800, 600)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Save optimized image
                quality = 85 if filename.lower().endswith(('.jpg', '.jpeg')) else None
                save_kwargs = {'optimize': True}
                if quality:
                    save_kwargs['quality'] = quality
                
                img.save(file_path, **save_kwargs)
                
        except Exception as e:
            # If image processing fails, delete the file and return error
            if os.path.exists(file_path):
                os.remove(file_path)
            return False, f"Error processing image: {str(e)}"
        
        return True, filename
        
    except Exception as e:
        return False, f"Error saving file: {str(e)}"

def delete_menu_item_image(filename, upload_folder):
    """Delete an existing menu item image"""
    if not filename:
        return True
    
    try:
        file_path = os.path.join(upload_folder, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
        return True
    except Exception as e:
        print(f"Error deleting image {filename}: {str(e)}")
        return False

def get_image_info(file_path):
    """Get information about an image file"""
    try:
        with Image.open(file_path) as img:
            return {
                'width': img.width,
                'height': img.height,
                'format': img.format,
                'mode': img.mode,
                'size_kb': round(os.path.getsize(file_path) / 1024, 2)
            }
    except Exception as e:
        return None