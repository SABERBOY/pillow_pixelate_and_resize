import sys
import json
from PIL import Image


def pixelate_and_resize(input_file_path, pixel_size, scale_factor):
    with Image.open(input_file_path) as image:
        # Convert image to RGBA mode to handle transparency
        image = image.convert("RGBA")

        # Calculate new dimensions
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)

        # Resize the image to a smaller size
        image = image.resize((new_width, new_height), Image.LANCZOS)

        # Pixelate the image
        pixelated = image.resize(
            (new_width // pixel_size, new_height // pixel_size), Image.NEAREST
        )

        # Save the pixelated image
        output_image_path = (
            input_file_path.rsplit(".", 1)[0] + f"_pixelated_{scale_factor}.png"
        )
        pixelated.save(output_image_path)
        print(f"Pixelated and resized image saved as {output_image_path}")

    return pixelated, output_image_path


def merge_pixel_blocks(image, block_size):
    width, height = image.size
    color_data = []

    for y in range(0, height, block_size):
        for x in range(0, width, block_size):
            # Get the color of the top-left pixel in the block
            r, g, b, a = image.getpixel((x, y))

            # Check if the entire block has the same color
            is_uniform = True
            for by in range(block_size):
                for bx in range(block_size):
                    if x + bx < width and y + by < height:
                        if image.getpixel((x + bx, y + by)) != (r, g, b, a):
                            is_uniform = False
                            break
                if not is_uniform:
                    break

            # If the block is uniform and not fully transparent, add it to color_data
            if is_uniform and r:
                color_data.append(
                    {"x": x // block_size, "y": y // block_size, "color": [r, g, b, a]}
                )

    return color_data


def get_pixel_colors(image):
    width, height = image.size
    color_data = []
    for y in range(height):
        for x in range(width):
            r, g, b, a = image.getpixel((x, y))
            # Ignore fully transparent pixels
            if a > 0 and r != 1 and g != 1 and b != 1:
                color_data.append(
                    {
                        "x": x,
                        "y": y,
                        "c": [
                            float("{:.2f}".format(r / 255)),
                            float("{:.2f}".format(g / 255)),
                            float("{:.2f}".format(b / 255)),
                            float("{:.2f}".format(a / 255)),
                        ],
                    }
                )

    return color_data


def save_colors_as_json(color_data, output_path):
    with open(output_path, "w") as f:
        json.dump(color_data, f)
    print(f"Color data saved as {output_path}")


if __name__ == "__main__":
    # if len(sys.argv) != 4:
    #     print("Usage: python script.py <input_image_path> <pixel_size> <scale_factor>")
    #     sys.exit(1)

    input_file_path = "./1.png"
    pixel_size = 10
    scale_factor = 0.3

    pixelated_image, output_image_path = pixelate_and_resize(
        input_file_path, pixel_size, scale_factor
    )
    color_data = get_pixel_colors(pixelated_image)

    output_json_path = output_image_path.rsplit(".", 1)[0] + "_colors.json"
    save_colors_as_json(color_data, output_json_path)
