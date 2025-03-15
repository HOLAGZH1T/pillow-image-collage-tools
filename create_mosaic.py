import os
from PIL import Image

# --- Configuration ---

# Folder with your images
image_folder = "/Users/acc1/Pictures/PepeCollection"

# Target size for each tile in the mosaic (adjusted to avoid exceeding 65,500 pixels)
tile_size = (600, 600)

# Grid dimensions: choose the number of columns (adjust as needed)
columns = 100  # For example, 100 columns

# Gather the list of image files (check for common extensions)
image_files = [os.path.join(image_folder, f) for f in os.listdir(image_folder)
               if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

# Debug: Print how many images were found
print(f"Found {len(image_files)} image files.")

if not image_files:
    print("No image files found. Check the directory path and file extensions.")
    exit(1)

# Calculate the number of rows (ceiling division)
rows = -(-len(image_files) // columns)

# Calculate mosaic dimensions
mosaic_width = columns * tile_size[0]
mosaic_height = rows * tile_size[1]

# Debug: Print mosaic dimensions
print(f"Mosaic dimensions: {mosaic_width} x {mosaic_height}")

# Check if dimensions exceed Pillow's limit
max_dimension = 65500
if mosaic_width > max_dimension or mosaic_height > max_dimension:
    print("Error: Mosaic dimensions exceed the maximum allowed (65,500 pixels).")
    print(f"Mosaic dimensions: {mosaic_width}x{mosaic_height}")
    exit(1)

# Create a new blank image for the mosaic (white background)
mosaic = Image.new("RGB", (mosaic_width, mosaic_height), "white")

# --- Create the Mosaic ---
for idx, image_path in enumerate(image_files):
    try:
        # Debug: Print the current image being processed
        print(f"Processing image {idx + 1}/{len(image_files)}: {image_path}")
        img = Image.open(image_path)
        # Use the new resampling filter instead of ANTIALIAS
        img = img.resize(tile_size, Image.Resampling.LANCZOS)

        # Calculate x and y coordinates for placement
        x = (idx % columns) * tile_size[0]
        y = (idx // columns) * tile_size[1]

        # Paste the image into the mosaic
        mosaic.paste(img, (x, y))
    except Exception as e:
        print(f"Error processing {image_path}: {e}")

# Save the mosaic
output_path = "mosaic_collage.jpg"
mosaic.save(output_path)
print(f"Mosaic created successfully and saved as '{output_path}'")
