import os
import numpy as np
from PIL import Image
import argparse
Image.MAX_IMAGE_PIXELS = None
# Define color mapping for each class
colors = {
    0: (0, 255, 0),       # Green
    1: (255, 105, 180),   # Pink
    2: (255, 165, 0),     # Orange
    3: (255, 0, 0),       # Red
    4: (255, 255, 0),     # Yellow
    5: (0, 0, 255),       # Blue
    6: (128, 128, 128),   # Gray
}

def process_images(original_image_path, mask_path, pred_mask_path, output_gt_image_path, output_pred_image_path):
    # Load the original image, ground truth mask, and predicted mask
    original_image = Image.open(original_image_path).convert('RGB')
    gt_mask = Image.open(mask_path).convert('L')
    pred_mask = Image.open(pred_mask_path).convert('L')

    # Convert to numpy arrays
    original_image_array = np.array(original_image)
    gt_mask_array = np.array(gt_mask)
    pred_mask_array = np.array(pred_mask)

    # Ignore white area (255) in ground truth mask
    valid_mask = gt_mask_array != 255

    # Create a copy of the original image for both the ground truth and prediction overlays
    gt_overlay_image = original_image_array.copy()
    pred_overlay_image = original_image_array.copy()

    # Apply colors to ground truth mask
    for value, color in colors.items():
        mask_area = (gt_mask_array == value) & valid_mask
        gt_overlay_image[mask_area] = (0.5 * gt_overlay_image[mask_area] + 0.5 * np.array(color)).astype(np.uint8)

    # Apply colors to prediction mask
    for value, color in colors.items():
        mask_area = (pred_mask_array == value) & valid_mask
        pred_overlay_image[mask_area] = (0.5 * pred_overlay_image[mask_area] + 0.5 * np.array(color)).astype(np.uint8)

    # Convert back to images
    gt_overlay_image = Image.fromarray(gt_overlay_image)
    pred_overlay_image = Image.fromarray(pred_overlay_image)

    # Save the generated images
    gt_overlay_image.save(output_gt_image_path)
    pred_overlay_image.save(output_pred_image_path)

def process_folder(input_folder):
    # Loop through all .png masks in the folder
    for mask_file in os.listdir(input_folder):
        if mask_file.endswith(".png"):
            mask_name = os.path.splitext(mask_file)[0]
            mask_path = os.path.join(input_folder, mask_file)

            # Corresponding original image (.jpg)
            original_image_path = os.path.join(input_folder, f"{mask_name}.jpg")

            # Corresponding folder for prediction and output
            pred_folder = os.path.join(input_folder, mask_name)
            pred_mask_path = os.path.join(pred_folder, "adjust_SAM.png")

            # Output file paths for generated images
            output_gt_image_path = os.path.join(pred_folder, f"{mask_name}_gt_overlay.jpg")
            output_pred_image_path = os.path.join(pred_folder, f"{mask_name}_pred_overlay_semantic_org_adjust_sam_step4.jpg")

            # Process images and generate overlays
            if os.path.exists(original_image_path) and os.path.exists(pred_mask_path):
                process_images(original_image_path, mask_path, pred_mask_path, output_gt_image_path, output_pred_image_path)
            else:
                print(f"Original image or prediction mask missing for {mask_name}")

# if __name__ == "__main__":
#     # Set up argument parser
#     parser = argparse.ArgumentParser(description="Generate overlay images from ground truth and predictions.")
#     parser.add_argument('--input_folder', type=str, required=True, help="Path to the input folder containing mask, original images, and prediction subfolders.")
    
#     # Parse arguments
#     args = parser.parse_args()

#     # Process the folder
#     process_folder(args.input_folder)
process_images(
    "/media/zzd/hrhsr/backup/Documents/img_seg/River/data/data_2023_mavic_p4/p4/test_data_1/mavic3_pro_10_2_2023_transparent_mosaic_group1_stitched_full.jpg", 
    "/media/zzd/hrhsr/backup/Documents/img_seg/River/data/data_2023_mavic_p4/p4/test_data_1/mavic3_pro_10_2_2023_transparent_mosaic_group1_stitched_full.png", 
    "/media/zzd/hrhsr/backup/Documents/img_seg/River/data/data_2023_mavic_p4/p4/test_data_1/mavic3_pro_10_2_2023_transparent_mosaic_group1_stitched_full.png", 
    "/media/zzd/hrhsr/backup/Documents/img_seg/River/data/data_2023_mavic_p4/p4/test_data_1/mavic3_pro_10_2_2023_transparent_mosaic_group1_stitched_full_gt.jpg", 
    "/media/zzd/hrhsr/backup/Documents/img_seg/River/data/data_2023_mavic_p4/p4/test_data_1/mavic3_pro_10_2_2023_transparent_mosaic_group1_stitched_full_gt1.jpg")