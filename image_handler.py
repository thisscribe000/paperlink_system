import os
import aiohttp
from pathlib import Path
from telegram import Update
from telegram.ext import ContextTypes

SITES_DIR = Path("sites")

async def download_telegram_file(file_id: str, bot_token: str, destination: Path):
    """Download file from Telegram servers"""
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}"
        ) as resp:
            data = await resp.json()
            if not data.get("ok"):
                return None
            file_path = data["result"]["file_path"]
        
        file_url = f"https://api.telegram.org/file/bot{bot_token}/{file_path}"
        async with session.get(file_url) as resp:
            if resp.status == 200:
                destination.write_bytes(await resp.read())
                return destination.name
            return None

async def handle_photo_upload(update: Update, context: ContextTypes.DEFAULT_TYPE, user_sessions: dict):
    """Handle when user sends a photo to add to their site"""
    user_id = update.effective_user.id
    
    if user_id not in user_sessions:
        await update.message.reply_text(
            "📸 Send me a photo while creating or editing a site to use it.\n\n"
            "Start with /new to create a site."
        )
        return
    
    session = user_sessions[user_id]
    slug = session.get("slug")
    
    if not slug:
        await update.message.reply_text("❌ No active site session. Start over with /new")
        return
    
    photo = update.message.photo[-1]
    file_id = photo.file_id
    
    site_images_dir = SITES_DIR / slug / "images"
    site_images_dir.mkdir(parents=True, exist_ok=True)
    
    existing_images = list(site_images_dir.glob("*.jpg")) + list(site_images_dir.glob("*.png"))
    img_number = len(existing_images) + 1
    filename = f"image_{img_number}.jpg"
    dest_path = site_images_dir / filename
    
    bot_token = context.bot.token
    downloaded = await download_telegram_file(file_id, bot_token, dest_path)
    
    if not downloaded:
        await update.message.reply_text("❌ Failed to download image. Try again.")
        return
    
    relative_path = f"images/{filename}"
    
    if "images" not in session["content"]:
        session["content"]["images"] = []
    
    session["content"]["images"].append(relative_path)
    
    if len(session["content"]["images"]) == 1 and not session["content"].get("logo_url"):
        session["content"]["logo_url"] = relative_path
        await update.message.reply_text(
            f"✅ Image saved and set as logo!\n\n"
            f"Send more photos or continue with the setup."
        )
    else:
        await update.message.reply_text(
            f"✅ Image #{len(session['content']['images'])} saved!\n\n"
            f"Send more or continue."
        )