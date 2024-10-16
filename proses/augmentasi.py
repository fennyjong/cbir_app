from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
import os
import numpy as np

# Setup for ImageDataGenerator with augmentation
datagen = ImageDataGenerator(
    rotation_range=40,
    width_shift_range=0.2,
    height_shift_range=0.2,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True,
    fill_mode='nearest'
)

def augment_image(file_path, output_folder, num_augments=5):
    img = load_img(file_path)  # Load original image
    x = img_to_array(img)  # Convert to array
    x = np.expand_dims(x, axis=0)  # Add batch dimension
    
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)
    
    i = 0
    for batch in datagen.flow(x, batch_size=1, save_to_dir=output_folder, save_prefix='aug', save_format='jpeg'):
        i += 1
        if i >= num_augments:  # Generate the specified number of augmentations
            break
