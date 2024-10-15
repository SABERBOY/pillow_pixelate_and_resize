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
        pixelated = pixelated.resize((new_width, new_height), Image.NEAREST)

        # Save the pixelated image
        output_image_path = (
            input_file_path.rsplit(".", 1)[0] + f"_pixelated_{scale_factor}.png"
        )
        pixelated.save(output_image_path)
        print(f"Pixelated and resized image saved as {output_image_path}")

    return pixelated, output_image_path


def get_pixel_colors(image):
    width, height = image.size
    color_data = []
    for y in range(height):
        for x in range(width):
            r, g, b, a = image.getpixel((x, y))
            # Ignore fully transparent pixels
            # if a > 0:
            if r != 1 and g != 1 and b != 1:
                color_data.append({"x": x, "y": y, "color": [r, g, b, a]})

    return color_data


def save_colors_as_json(color_data, output_path):
    with open(output_path, "w") as f:
        json.dump(color_data, f)
    print(f"Color data saved as {output_path}")


# if __name__ == "__main__":
#     if len(sys.argv) != 4:
#         print("Usage: python script.py <input_image_path> <pixel_size> <scale_factor>")
#         sys.exit(1)

#     input_file_path = sys.argv[1]
#     pixel_size = int(sys.argv[2])
#     scale_factor = float(sys.argv[3])

#     pixelated_image, output_image_path = pixelate_and_resize(
#         input_file_path, pixel_size, scale_factor
#     )
#     color_data = get_pixel_colors(pixelated_image)

#     output_json_path = output_image_path.rsplit(".", 1)[0] + "_colors.json"
#     save_colors_as_json(color_data, output_json_path)

if __name__ == "__main__":
    # if len(sys.argv) != 4:
    #     print("Usage: python script.py <input_image_path> <pixel_size> <scale_factor>")
    #     sys.exit(1)

    input_file_path = "./girl.jpg"
    pixel_size = 10
    scale_factor = 0.3

    pixelated_image, output_image_path = pixelate_and_resize(
        input_file_path, pixel_size, scale_factor
    )
    color_data = get_pixel_colors(pixelated_image)

    output_json_path = output_image_path.rsplit(".", 1)[0] + "_colors.json"
    save_colors_as_json(color_data, output_json_path)
