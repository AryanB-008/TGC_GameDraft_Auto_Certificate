import os
import time
import getpass
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import smtplib
from email.message import EmailMessage
from pathlib import Path

# ====== CONFIG ======
BASE_DIR = Path(__file__).parent.absolute()
CSV_PATH = BASE_DIR / "participants.csv"
TEMPLATE_PATH = BASE_DIR / "certificate.jpg"

NAME_COL = "Candidate's Name"
TEAM_COL = "Team Name"
EMAIL_COL = "Candidate's Email"

# Final Coordinates based on your template
NAME_POSITION = (1170, 890) 
TEAM_POSITION = (1900, 885) 
NAME_FONT_SIZE = 35
TEAM_FONT_SIZE = 35

NAME_FONT_PATH = str(BASE_DIR / "fonts" / "Roboto-Bold.ttf")
TEAM_FONT_PATH = str(BASE_DIR / "fonts" / "Roboto-Bold.ttf")

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_SUBJECT = "GameDraft'25 Participation Certificate"
EMAIL_BODY_TEMPLATE = "Dear {name},\n\nPlease find attached your certificate for GameDraft 25.\n\nBest regards,\nThe Gaming Club,IIITH"

def generate_certificate(name, team, out_path):
    img = Image.open(TEMPLATE_PATH).convert("RGB")
    draw = ImageDraw.Draw(img)
    name_font = ImageFont.truetype(NAME_FONT_PATH, NAME_FONT_SIZE)
    team_font = ImageFont.truetype(TEAM_FONT_PATH, TEAM_FONT_SIZE)

    def draw_centered(text, center, font):
        bbox = draw.textbbox((0, 0), text, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text((center[0] - w // 2, center[1] - h - 5), text, font=font, fill=(0,0,0))

    draw_centered(name, NAME_POSITION, name_font)
    draw_centered(team, TEAM_POSITION, team_font)
    img.save(out_path, "JPEG")

def main():
    if not CSV_PATH.exists():
        print(f"❌ Missing CSV: {CSV_PATH}")
        return

    # Load and clean CSV immediately
    df = pd.read_csv(CSV_PATH).dropna(how='all')
    
    dry_run = input("Dry run? (y/n): ").lower() == 'y'
    sender_email = ""
    sender_password = ""
    
    if not dry_run:
        sender_email = input("Email: ").strip()
        sender_password = input("Enter App Password: ").strip()

    output_dir = BASE_DIR / "certificates"
    if not output_dir.exists(): output_dir.mkdir()

    for _, row in df.iterrows():
        name = str(row.get(NAME_COL, "")).strip()
        team = str(row.get(TEAM_COL, "")).strip()
        email = str(row.get(EMAIL_COL, "")).strip()

        # THE NAN FIX: Skip if essential data is missing
        if not name or name.lower() == "nan" or not email or email.lower() == "nan":
            continue

        filename = f"{name.replace(' ', '_')}.jpg"
        cert_path = output_dir / filename
        
        generate_certificate(name, team, str(cert_path))
        print(f"✅ Created: {filename}")

        if not dry_run:
            try:
                # 1. Create the Email Message
                msg = EmailMessage()
                msg["Subject"] = EMAIL_SUBJECT
                msg["From"] = sender_email
                msg["To"] = email
                msg.set_content(EMAIL_BODY_TEMPLATE.format(name=name))

                # 2. Attach the Certificate
                with open(cert_path, "rb") as f:
                    file_data = f.read()
                msg.add_attachment(
                    file_data, 
                    maintype="image", 
                    subtype="jpeg", 
                    filename=filename
                )

                # 3. Connect to Gmail and Send
                with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                    server.starttls()  # Secure the connection
                    server.login(sender_email, sender_password)
                    server.send_message(msg)

                print(f"📧 Sent to {email}")
                
                # 4. ADD DELAY: Wait 2 seconds before the next loop
                print("Waiting 2 seconds...")
                time.sleep(2) 
                
            except Exception as e:
                print(f"❌ Failed to email {email}: {e}")

if __name__ == "__main__":
    main()