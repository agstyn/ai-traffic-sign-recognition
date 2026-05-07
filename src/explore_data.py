import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Path to training images
TRAIN_PATH = "data/GTSRB/Final_Training/Images"

# Count classes and images
class_folders = sorted(os.listdir(TRAIN_PATH))
num_classes = len(class_folders)
print(f"Total classes (traffic sign types): {num_classes}")

# Count images per class
class_counts = []
for folder in class_folders:
    folder_path = os.path.join(TRAIN_PATH, folder)
    images = [f for f in os.listdir(folder_path) if f.endswith('.ppm')]
    class_counts.append(len(images))

total_images = sum(class_counts)
print(f"Total training images: {total_images}")
print(f"Min images in a class: {min(class_counts)}")
print(f"Max images in a class: {max(class_counts)}")

# Plot class distribution
plt.figure(figsize=(18, 5))
plt.bar(range(num_classes), class_counts, color='steelblue')
plt.xlabel("Class ID")
plt.ylabel("Number of Images")
plt.title("Training Images per Class")
plt.xticks(range(num_classes), rotation=90, fontsize=7)
plt.tight_layout()
plt.savefig("data/class_distribution.png")
plt.show()
print("Class distribution chart saved!")

# Show sample images from 9 random classes
fig, axes = plt.subplots(3, 3, figsize=(10, 10))
sample_classes = np.random.choice(range(num_classes), 9, replace=False)

for ax, class_id in zip(axes.flatten(), sample_classes):
    folder = os.path.join(TRAIN_PATH, class_folders[class_id])
    sample_img = os.path.join(folder, os.listdir(folder)[0])
    img = mpimg.imread(sample_img)
    ax.imshow(img)
    ax.set_title(f"Class {class_id:05d}", fontsize=9)
    ax.axis('off')

plt.suptitle("Sample Traffic Signs", fontsize=14)
plt.tight_layout()
plt.savefig("data/sample_images.png")
plt.show()
print("Sample images chart saved!")