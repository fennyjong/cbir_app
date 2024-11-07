import os
import cv2
import imgaug.augmenters as iaa

seq = iaa.Sequential([
    iaa.Rotate(rotate=(-90, 90)),  # Rotasi acak dari -90 hingga 90 derajat
    iaa.ShearX(shear=(-0.2, 0.2)),   # Transformasi shear acak dari antara -20% hingga +20%
    iaa.Affine(scale=(0.7, 1.5)),    # Zoom acak dari 70% hingga 150%
    iaa.TranslateX(percent=(-0.2, 0.2)),  # Pergeseran horizontal acak hingga 20%
    iaa.TranslateY(percent=(-0.2, 0.2)),  # Pergeseran vertikal acak hingga 20%
])

def augment_image(file_path, output_folder, num_augmentations=5):
    img = cv2.imread(file_path)

    if img is None:
        raise ValueError(f"Image not found or could not be loaded: {file_path}")

    # Resize to 255x255
    img_resized = cv2.resize(img, (255, 255))
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Save the resized image
    resized_filename = os.path.join(output_folder, f'{os.path.splitext(os.path.basename(file_path))[0]}_resized.jpg')
    cv2.imwrite(resized_filename, img_resized)

    augmented_filenames = [resized_filename]  # Start with resized image

    # Generate multiple augmented images
    for i in range(num_augmentations):
        # Apply augmentations
        img_augmented = seq(image=img_resized)

        # Save the augmented image with a unique filename
        augmented_filename = os.path.join(output_folder, f'{os.path.splitext(os.path.basename(file_path))[0]}_augmented_{i + 1}.jpg')
        cv2.imwrite(augmented_filename, img_augmented)
        augmented_filenames.append(augmented_filename)

    return augmented_filenames