"""Testing grounds"""
from PIL import Image, ImageDraw, ImageFont

# Load an image
image = Image.new('RGB', (400,400), (255,255,255))

# Initialize ImageDraw
draw = ImageDraw.Draw(image)

# Define the text and position
TEXT = "Hello, World!"
POSITION = (50, 50)  # x, y coordinates

# Optional: Load a font (you can specify font size)
# You can use ImageFont.load_default() for a basic font
font = ImageFont.truetype("arial.ttf", 40)

# Draw the text on the image
draw.text(POSITION, TEXT, font=font, fill="black")

# Save the modified image
image.save("output_image.jpg")

# Display the image (optional)
image.show()
