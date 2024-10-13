import os
import numpy as np
from PIL import Image
import tensorflow as tf
from models import db, SongketDataset  # Ganti 'models' dengan nama file model Anda

def augment_and_save_images(image_path, region, fabric_name):
    # Buat direktori untuk menyimpan gambar hasil augmentasi
    augmented_dir = 'augmented_images'
    os.makedirs(augmented_dir, exist_ok=True)

    # Muat gambar asli
    img = Image.open(image_path)
    img = img.convert('RGB')
    img_array = np.array(img)

    # Buat nama file untuk 5 varian gambar
    augmented_filenames = []

    # Buat 5 varian gambar
    for i in range(5):
        # Augmentasi gambar menggunakan TensorFlow
        if i == 0:  # Original image
            augmented_image = img_array
        elif i == 1:  # Rotate
            augmented_image = tf.image.rot90(img_array, k=1).numpy()
        elif i == 2:  # Flip horizontal
            augmented_image = tf.image.flip_left_right(img_array).numpy()
        elif i == 3:  # Brightness adjustment
            augmented_image = tf.image.adjust_brightness(img_array, delta=0.1).numpy()
        elif i == 4:  # Contrast adjustment
            augmented_image = tf.image.adjust_contrast(img_array, contrast_factor=1.5).numpy()

        # Simpan gambar hasil augmentasi
        augmented_filename = f'aug_{i + 1}.jpg'
        augmented_filenames.append(augmented_filename)
        augmented_image_pil = Image.fromarray(augmented_image)
        augmented_image_pil.save(os.path.join(augmented_dir, augmented_filename))

    # Simpan informasi ke database
    augmented_entry = SongketDataset(
        region=region,
        fabric_name=fabric_name,
        image_filename_1=augmented_filenames[0],
        image_filename_2=augmented_filenames[1],
        image_filename_3=augmented_filenames[2],
        image_filename_4=augmented_filenames[3],
        image_filename_5=augmented_filenames[4]
    )

    db.session.add(augmented_entry)
    db.session.commit()
