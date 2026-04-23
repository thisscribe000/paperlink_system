import os
import logging
import re
from pathlib import Path
from dotenv import load_dotenv

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters
)

from database import (
    get_or_create_tenant, create_site, get_site, 
    get_user_sites, update_site_content, publish_site
)
from builder import generate_site

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BASE_URL = os.getenv("BASE_URL", "http://localhost:8080")

def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏗️ New Site", callback_data="new")],
        [InlineKeyboardButton("📁 My Sites", callback_data="sites")],
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    tenant = get_or_create_tenant(user.id, user.username)
    
    await update.message.reply_text(
        f"🏗️ *Telegram Land*\n\n"
        f"Host sites. Edit code. Go live.\n\n"
        f"Commands:\n"
        f"`/new <slug>` — Create site\n"
        f"`/edit <slug>` — Open code editor\n"
        f"`/sites` — List sites\n"
        f"`/delete <slug>` — Delete site\n\n"
        f"Sites: {tenant[5]}",
        parse_mode='Markdown',
        reply_markup=get_main_menu()
    )

async def new_site(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    
    if not context.args:
        await update.message.reply_text(
            "Usage: `/new <slug>`\n\nExample: `/new myshop`",
            parse_mode='Markdown'
        )
        return
    
    slug = context.args[0].lower().strip()
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    
    if len(slug) < 2 or len(slug) > 50:
        await update.message.reply_text("❌ Slug must be 2-50 chars")
        return
    
    if get_site(slug):
        await update.message.reply_text(f"❌ `{slug}` already taken.")
        return
    
    tenant = get_or_create_tenant(user.id, user.username)
    
    content = {
        'name': slug.replace('-', ' ').title(),
        'hero_text': 'Welcome',
        'title': 'Welcome',
        'hero_subtext': 'Edit this site',
        'description': 'Edit this site',
        'brand_color': '#0088cc',
    }
    
    try:
        create_site(tenant[0], slug, content['name'], 'landing', content)
        generate_site(slug, 'landing', content)
        publish_site(slug)
        
        site_url = f"{BASE_URL}/sites/{slug}"
        edit_url = f"{BASE_URL}/editor.html?slug={slug}"
        
        keyboard = [
            [InlineKeyboardButton("✏️ Open Code Editor", web_app=WebAppInfo(url=edit_url))],
            [InlineKeyboardButton("🌐 View Site", url=site_url)],
        ]
        
        await update.message.reply_text(
            f"🚀 *Site Created!*\n\n🔗 {site_url}\nSlug: `{slug}`\n\nTap 'Open Code Editor' to edit HTML.",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
    except Exception as e:
        logger.error(f"new_site error: {e}")
        await update.message.reply_text(f"❌ Error: {str(e)}")

async def edit_site(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: `/edit <slug>`")
        return
    
    slug = context.args[0]
    site = get_site(slug)
    
    if not site:
        await update.message.reply_text(f"❌ Site `{slug}` not found.")
        return
    
    tenant = get_or_create_tenant(update.effective_user.id, update.effective_user.username)
    if site[1] != tenant[0]:
        await update.message.reply_text("❌ Not your site.")
        return
    
    edit_url = f"{BASE_URL}/editor.html?slug={slug}"
    site_url = f"{BASE_URL}/sites/{slug}"
    
    keyboard = [
        [InlineKeyboardButton("✏️ Open Code Editor", web_app=WebAppInfo(url=edit_url))],
        [InlineKeyboardButton("🌐 View Site", url=site_url)],
    ]
    
    await update.message.reply_text(
        f"✏️ *Editing: {site[4]}*\n\nSlug: `{slug}`\n\nTap below to open editor.",
        parse_mode='Markdown',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def list_sites(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    tenant = get_or_create_tenant(user.id, user.username)
    sites = get_user_sites(tenant[0])
    
    if not sites:
        await update.message.reply_text("📭 No sites yet.\n\nCreate: `/new mysite`", parse_mode='Markdown')
        return
    
    text = "📁 *Your Sites:*\n\n"
    
    for site in sites:
        url = f"{BASE_URL}/sites/{site[3]}"
        edit = f"{BASE_URL}/editor.html?slug={site[3]}"
        text += f"• *{site[4]}* (`{site[3]}`)\n  [View]({url}) | [Edit]({edit})\n\n"
    
    await update.message.reply_text(text, parse_mode='Markdown', disable_web_page_preview=True)

async def delete_site(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Usage: `/delete <slug>`")
        return
    
    slug = context.args[0]
    site = get_site(slug)
    
    if not site:
        await update.message.reply_text(f"❌ Site `{slug}` not found.")
        return
    
    tenant = get_or_create_tenant(update.effective_user.id, update.effective_user.username)
    if site[1] != tenant[0]:
        await update.message.reply_text("❌ Not your site.")
        return
    
    import shutil
    site_dir = Path("sites") / slug
    if site_dir.exists():
        shutil.rmtree(site_dir)
    
    import sqlite3
    conn = sqlite3.connect("telegram_land.db")
    c = conn.cursor()
    c.execute("DELETE FROM sites WHERE slug = ?", (slug,))
    conn.commit()
    conn.close()
    
    await update.message.reply_text(f"🗑️ Site `{slug}` deleted.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "new":
        await query.edit_message_text("Send: `/new <slug>`\n\nExample: `/new myshop`", parse_mode='Markdown')
    elif query.data == "sites":
        await list_sites(update, context)

def main():
    token = os.getenv("BOT_TOKEN")
    if not token:
        print("❌ No BOT_TOKEN in .env")
        return
    
    app = Application.builder().token(token).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("new", new_site))
    app.add_handler(CommandHandler("edit", edit_site))
    app.add_handler(CommandHandler("sites", list_sites))
    app.add_handler(CommandHandler("delete", delete_site))
    app.add_handler(CallbackQueryHandler(button_handler))
    
    print("🏗️ Bot running — Hosting Mode")
    app.run_polling()

if __name__ == "__main__":
    main()