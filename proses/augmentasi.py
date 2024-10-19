import os
from PIL import Image, ImageOps, ImageEnhance

def augment_image(file_path, output_folder, num_augments=7):
    img = Image.open(file_path)
    
    # Resize to 255x255
    img_resized = img.resize((255, 255), Image.LANCZOS)
    base_filename = os.path.splitext(os.path.basename(file_path))[0]
    
    augmented_filenames = []

    # 1. Original resized image
    resized_filename = os.path.join(output_folder, f'{base_filename}_resized.jpg')
    img_resized.save(resized_filename, 'JPEG')
    augmented_filenames.append(resized_filename)

    # 2. Vertical flip
    img_flip = ImageOps.flip(img_resized)
    flip_filename = os.path.join(output_folder, f'{base_filename}_flip.jpg')
    img_flip.save(flip_filename, 'JPEG')
    augmented_filenames.append(flip_filename)

    # 3. Rotate -90 degrees
    img_rotate_minus = img_resized.rotate(-90, resample=Image.BICUBIC, expand=True)
    rotate_minus_filename = os.path.join(output_folder, f'{base_filename}_rotate_minus_90.jpg')
    img_rotate_minus.save(rotate_minus_filename, 'JPEG')
    augmented_filenames.append(rotate_minus_filename)

    # 4. Rotate +90 degrees
    img_rotate_plus = img_resized.rotate(90, resample=Image.BICUBIC, expand=True)
    rotate_plus_filename = os.path.join(output_folder, f'{base_filename}_rotate_plus_90.jpg')
    img_rotate_plus.save(rotate_plus_filename, 'JPEG')
    augmented_filenames.append(rotate_plus_filename)

    # 5. Zoom (crop from the center)
    zoom_factor = 0.75
    width, height = img_resized.size
    new_width = int(width * zoom_factor)
    new_height = int(height * zoom_factor)
    img_zoom = img_resized.crop((
        (width - new_width) // 2,
        (height - new_height) // 2,
        (width + new_width) // 2,
        (height + new_height) // 2
    )).resize((255, 255), Image.LANCZOS)
    zoom_filename = os.path.join(output_folder, f'{base_filename}_zoom.jpg')
    img_zoom.save(zoom_filename, 'JPEG')
    augmented_filenames.append(zoom_filename)

    # 6. Brightness adjustment
    enhancer = ImageEnhance.Brightness(img_resized)
    img_bright = enhancer.enhance(1.5)
    bright_filename = os.path.join(output_folder, f'{base_filename}_bright.jpg')
    img_bright.save(bright_filename, 'JPEG')
    augmented_filenames.append(bright_filename)

    # 7. Contrast adjustment
    enhancer = ImageEnhance.Contrast(img_resized)
    img_contrast = enhancer.enhance(1.5)
    contrast_filename = os.path.join(output_folder, f'{base_filename}_contrast.jpg')
    img_contrast.save(contrast_filename, 'JPEG')
    augmented_filenames.append(contrast_filename)

    return augmented_filenames