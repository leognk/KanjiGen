import os
import csv


img_dir = os.path.join('data', 'images')
metadata_path = os.path.join(img_dir, 'metadata.csv')

# Read metadata file.
with open(metadata_path, 'r') as f:
    csv_reader = csv.reader(f)
    header = next(csv_reader)
    valid_img_files = {entry[0] for entry in csv_reader}

# Remove PNG files which are not in metadata.
for entry in os.listdir(img_dir):
    if entry.endswith('.png') and entry not in valid_img_files:
        os.remove(os.path.join(img_dir, entry))
        print(f"Removed {entry}")