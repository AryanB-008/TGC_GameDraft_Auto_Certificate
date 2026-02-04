import os
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# ====== CONFIG ======
BASE_DIR = Path(__file__).parent.absolute()
TEMPLATE_PATH = BASE_DIR / "certificate.jpg"
OUTPUT_PATH = BASE_DIR / "test_alignment.jpg"

# Fonts
NAME_FONT_PATH = str(BASE_DIR / "fonts" / "Roboto-Bold.ttf")
TEAM_FONT_PATH = str(BASE_DIR / "fonts" / "Roboto-Regular.ttf")

# Coordinates calculated for your specific image
NAME_POSITION = (1058, 890) 
TEAM_POSITION = (1783, 885) 
NAME_FONT_SIZE = 40
TEAM_FONT_SIZE = 40

def generate_test():
    if not TEMPLATE_PATH.exists():
        print(f"❌ Error: {TEMPLATE_PATH} not found!")
        return

    img = Image.open(TEMPLATE_PATH).convert("RGB")
    draw = ImageDraw.Draw(img)

    try:
        name_font = ImageFont.truetype(NAME_FONT_PATH, NAME_FONT_SIZE)
        team_font = ImageFont.truetype(TEAM_FONT_PATH, TEAM_FONT_SIZE)
    except:
        print("❌ Font error! Using default font.")
        name_font = team_font = ImageFont.load_default()

    def draw_centered(text, center, font):
        # Using textbbox for Pillow 10+ compatibility
        bbox = draw.textbbox((0, 0), text, font=font)
        w = bbox[2] - bbox[0]
        h = bbox[3] - bbox[1]
        
        # Position logic: center horizontally, sit 'on' the line vertically
        x = center[0] - w // 2
        y = center[1] - h - 5 # Subtracting 5 pixels to hover slightly above the line
        draw.text((x, y), text, font=font, fill=(0, 0, 0))

    # Test Data
    draw_centered("Vansh Agarwal", NAME_POSITION, name_font)
    draw_centered("The Game Crafters", TEAM_POSITION, team_font)

    img.save(OUTPUT_PATH)
    print(f"✅ Test certificate saved as: {OUTPUT_PATH}")

if __name__ == "__main__":
    generate_test()