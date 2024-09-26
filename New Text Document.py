import os
import shutil
import random
from collections import Counter

def undersample_dataset(source_dir, target_dir, class_counts):
    # Create the target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Find the minimum class count
    min_count = min(class_counts.values())
    
    for class_name, count in class_counts.items():
        source_class_dir = os.path.join(source_dir, class_name)
        target_class_dir = os.path.join(target_dir, class_name)
        os.makedirs(target_class_dir, exist_ok=True)
        
        # Get all image files in the source class directory
        image_files = [f for f in os.listdir(source_class_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        # Randomly select 'min_count' images
        selected_images = random.sample(image_files, min_count)
        
        # Copy selected images to the target class directory
        for image in selected_images:
            shutil.copy(os.path.join(source_class_dir, image), target_class_dir)
    
    print(f"Balanced dataset created in {target_dir}")

# Define the class counts
class_counts = {
    "No_dr": 21988,
    "Mild": 2412,
    "Moderate": 5142,
    "Severe": 870,
    "Proliferate_dr": 705
}

# Set the source and target directories
source_dir = "D:\Major Project\Datasets\Datasets"
target_dir = "D:\Major Project\Datasets\balanced_data"
# Perform undersampling
undersample_dataset(source_dir, target_dir, class_counts)

# Verify the balanced dataset
balanced_counts = {}
for class_name in class_counts.keys():
    class_dir = os.path.join(target_dir, class_name)
    balanced_counts[class_name] = len([f for f in os.listdir(class_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

print("Balanced class counts:")
print(Counter(balanced_counts))