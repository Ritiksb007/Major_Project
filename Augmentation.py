import os
import cv2
import numpy as np
from keras.preprocessing.image import ImageDataGenerator  # Ensure keras is installed
from tqdm import tqdm  # Standard tqdm for progress bars

# Define paths
dataset_folder = ''  # Change this to your local dataset folder
output_folder = 'path/to/output_dataset'  # Change this to your local output folder
categories = ['Mild', 'Moderate', 'No_DR', 'Proliferate_DR', 'Severe']

# Create ImageDataGenerator for augmentation
datagen = ImageDataGenerator(
    rotation_range=20,
    width_shift_range=0.1,
    height_shift_range=0.1,
    shear_range=0.1,
    zoom_range=0.1,
    horizontal_flip=True,
    fill_mode='nearest'
)

# Function to save augmented images
def save_augmented_images(category, img_array, image_name, augmentations_needed):
    img_array = np.expand_dims(img_array, axis=0)
    aug_iter = datagen.flow(img_array, batch_size=1)
    for i in range(augmentations_needed):
        aug_image = next(aug_iter)[0].astype('uint8')
        save_path = os.path.join(output_folder, category, f"aug_{i}_{image_name}")
        cv2.imwrite(save_path, aug_image)

# Ensure output folder structure
for category in categories:
    os.makedirs(os.path.join(output_folder, category), exist_ok=True)

# Count images per class
image_counts = {category: len(os.listdir(os.path.join(dataset_folder, category))) for category in categories}

# Target count is the maximum number of images from any class
max_count = max(image_counts.values())

# Perform augmentation
for category in categories:
    category_folder = os.path.join(dataset_folder, category)
    images = os.listdir(category_folder)
    
    for image_name in tqdm(images, desc=f"Augmenting {category}"):
        img_path = os.path.join(category_folder, image_name)
        img = cv2.imread(img_path)
        if img is None:
            continue  # Skip if image can't be read

        # Check how many augmentations we need to perform
        augmentations_needed = max_count - image_counts[category]
        
        if augmentations_needed > 0:
            save_augmented_images(category, img, image_name, augmentations_needed)
