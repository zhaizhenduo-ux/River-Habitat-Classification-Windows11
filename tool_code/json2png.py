import json
from PIL import Image, ImageDraw

# Adjust the maximum number of pixels allowed for an image to avoid DecompressionBombWarning.
Image.MAX_IMAGE_PIXELS = None

def create_mask_from_json(json_path, image_path, output_path):
    # Mapping from class to pixel value
    class_to_value = {
        "Tall_canopy": 0,
        "Grassland": 1,
        "Road": 2,
        "Low_canopy": 3,
        "Water": 4,
        "Agriculture": 5,
        "Bar": 6
    }

    # Load JSON file
    with open(json_path) as f:
        data = json.load(f)

    # Load image to get dimensions
    image = Image.open(image_path)
    width, height = image.size

    # Create a blank mask
    mask = Image.new('L', (width, height), 255)
    draw = ImageDraw.Draw(mask)

    # Draw each polygon with the corresponding pixel value
    for shape in data['shapes']:
        # Flatten the list of points
        polygon = [coord for point in shape['points'] for coord in point]
        label = shape['label']
        pixel_value = class_to_value.get(label, 255)  # Default to 0 if class is not found
        draw.polygon(polygon, fill=pixel_value)

    # Save the mask as a PNG file
    mask.save(output_path)

# Example usage - Replace these paths with your actual file paths
# json_path = '../data/third_test/mavic3/10_16_2023/mavic3_pro_10_16_2023_transparent_mosaic_group1_0_1.json'
# image_path = '../data/third_test/mavic3/10_16_2023/mavic3_pro_10_16_2023_transparent_mosaic_group1_0_1.jpg'
# output_path = '../data/third_test/mavic3/10_16_2023/mavic3_pro_10_16_2023_transparent_mosaic_group1_0_1.png'

# create_mask_from_json(json_path, image_path, output_path)
# #/media/zzd/hrhsr/backup/Documents/img_seg/River/data/third_test/mavic3/10_16_2023/mavic3_pro_10_16_2023_transparent_mosaic_group1_0_1.jpg

import glob
json_dirs = glob.glob("/media/zzd/hrhsr/backup/Documents/img_seg/River/data/data_2023_mavic_p4/p4/test_data_1/*.json")
for json_dir in json_dirs:
    create_mask_from_json(json_dir,json_dir.replace(".json", ".jpg", 1), json_dir.replace(".json", ".png", 1))