import os
import shutil

SOURCE = "data/GTSRB/Final_Training/Images"
DEST = "assets/class_images"

folders = sorted(os.listdir(SOURCE))

for idx, folder in enumerate(folders):
    folder_path = os.path.join(SOURCE, folder)

    images = [f for f in os.listdir(folder_path) if f.endswith(".ppm")]

    if images:
        src_img = os.path.join(folder_path, images[0])
        dst_img = os.path.join(DEST, f"{idx}.ppm")

        shutil.copy(src_img, dst_img)

print("Done.")