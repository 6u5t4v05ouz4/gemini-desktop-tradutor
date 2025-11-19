from PIL import Image, ImageDraw, ImageFont
import os

def create_icons():
    size = (64, 64)
    # Create a blue background
    image = Image.new('RGB', size, color=(33, 150, 243)) # Material Blue
    draw = ImageDraw.Draw(image)
    
    # Draw a white "T" or similar symbol
    # Since we might not have a specific font, we'll draw lines or simple shapes
    # Let's draw a stylized "T"
    
    # Horizontal bar
    draw.rectangle([10, 10, 54, 20], fill="white")
    # Vertical bar
    draw.rectangle([27, 20, 37, 54], fill="white")
    
    # Save as PNG for pystray
    image.save("app_icon.png")
    
    # Save as ICO for Windows window
    image.save("app_icon.ico", format='ICO', sizes=[(64, 64)])
    
    print("Icons created: app_icon.png, app_icon.ico")

if __name__ == "__main__":
    create_icons()
