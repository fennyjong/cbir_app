# In proses/augmentasi.py

import os
from PIL import Image, ImageOps

# Define the folder where augmented images will be saved
AUGMENTED_FOLDER = 'augmented_images'

def augment_image(file_path, output_folder, num_augments=7):
    img = Image.open(file_path)

    # Resize to 255x255
    img_resized = img.resize((255, 255), Image.LANCZOS)
    resized_filename = os.path.join(output_folder, f'{os.path.splitext(os.path.basename(file_path))[0]}_resized.jpg')
    img_resized.save(resized_filename, 'JPEG')

    augmented_filenames = [resized_filename]  # Start with resized image

    # Augmentation: vertical flip
    img_flip = ImageOps.flip(img_resized)
    flip_filename = os.path.join(output_folder, f'{os.path.splitext(os.path.basename(file_path))[0]}_flip.jpg')
    img_flip.save(flip_filename, 'JPEG')
    augmented_filenames.append(flip_filename)

    # Augmentation: rotate -90 degrees
    img_rotate_minus = img_resized.rotate(-90, resample=Image.BICUBIC, expand=True)
    rotate_minus_filename = os.path.join(output_folder, f'{os.path.splitext(os.path.basename(file_path))[0]}_rotate_minus_90.jpg')
    img_rotate_minus.save(rotate_minus_filename, 'JPEG')
    augmented_filenames.append(rotate_minus_filename)

    # Augmentation: rotate +90 degrees
    img_rotate_plus = img_resized.rotate(90, resample=Image.BICUBIC, expand=True)
    rotate_plus_filename = os.path.join(output_folder, f'{os.path.splitext(os.path.basename(file_path))[0]}_rotate_plus_90.jpg')
    img_rotate_plus.save(rotate_plus_filename, 'JPEG')
    augmented_filenames.append(rotate_plus_filename)

    # Augmentation: zoom (crop from the center)
    zoom_factor = 0.5
    width, height = img_resized.size
    new_width = int(width * zoom_factor)
    new_height = int(height * zoom_factor)
    img_zoom = img_resized.crop((
        (width - new_width) // 2,
        (height - new_height) // 2,
        (width + new_width) // 2,
        (height + new_height) // 2
    )).resize((255, 255), Image.LANCZOS)
    
    zoom_filename = os.path.join(output_folder, f'{os.path.splitext(os.path.basename(file_path))[0]}_zoom.jpg')
    img_zoom.save(zoom_filename, 'JPEG')
    augmented_filenames.append(zoom_filename)

    return augmented_filenames
