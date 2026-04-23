#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
exec python -c "
import asyncio
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from database import get_or_create_tenant, create_site, get_site, get_user_sites
from builder import generate_site
from dotenv import load_dotenv

load_dotenv()
BASE_URL = os.getenv('BASE_URL', 'http://localhost:8080')

def get_main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton('🏗️ New Site', callback_data='new')],
        [InlineKeyboardButton('📁 My Sites', callback_data='sites')],
    ])

async def start(update, context):
    user = update.effective_user
    tenant = get_or_create_tenant(user.id, user.username)
    await update.message.reply_text(
        f'🏗️ Telegram Land\n\nHost sites. Edit code.\n\n/new <slug> — Create\n/sites — List\n/edit <slug> — Editor\n\nSites: {tenant[5]}',
        reply_markup=get_main_menu()
    )

async def new_site(update, context):
    user = update.effective_user
    if not context.args:
        await update.message.reply_text('Usage: /new <slug>')
        return
    slug = context.args[0].lower().strip()
    import re
    slug = re.sub(r'[^a-z0-9-]', '', slug)
    if get_site(slug):
        await update.message.reply_text(f'❌ {slug} taken')
        return
    tenant = get_or_create_tenant(user.id, user.username)
    content = {'name': slug.replace('-', ' ').title(), 'hero_text': 'Welcome', 'title': 'Welcome'}
    create_site(tenant[0], slug, content['name'], 'landing', content)
    generate_site(slug, 'landing', content)
    site_url = f'{BASE_URL}/sites/{slug}'
    edit_url = f'{BASE_URL}/editor.html?slug={slug}'
    await update.message.reply_text(
        f'🚀 Site Created!\n\n🔗 {site_url}\n\nTap Open Editor to edit HTML.',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('✏️ Open Editor', web_app=WebAppInfo(url=edit_url))],
            [InlineKeyboardButton('🌐 View', url=site_url)]
        ])
    )

async def edit_site(update, context):
    if not context.args:
        await update.message.reply_text('Usage: /edit <slug>')
        return
    slug = context.args[0]
    site = get_site(slug)
    if not site:
        await update.message.reply_text('❌ Site not found')
        return
    edit_url = f'{BASE_URL}/editor.html?slug={slug}'
    site_url = f'{BASE_URL}/sites/{slug}'
    await update.message.reply_text(
        f'✏️ Editing: {site[4]}\n\nTap below:',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('✏️ Open Editor', web_app=WebAppInfo(url=edit_url))],
            [InlineKeyboardButton('🌐 View', url=site_url)]
        ])
    )

async def list_sites(update, context):
    user = update.effective_user
    tenant = get_or_create_tenant(user.id, user.username)
    sites = get_user_sites(tenant[0])
    if not sites:
        await update.message.reply_text('📭 No sites yet')
        return
    text = '📁 Your Sites:\n\n'
    for site in sites:
        text += f'• {site[4]} ({site[3]})\n'
    await update.message.reply_text(text)

async def button_handler(update, context):
    query = update.callback_query
    await query.answer()
    if query.data == 'new':
        await query.edit_message_text('Send: /new <slug>')
    elif query.data == 'sites':
        await list_sites(update, context)

async def main():
    app = Application.builder().token(os.getenv('BOT_TOKEN')).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('new', new_site))
    app.add_handler(CommandHandler('edit', edit_site))
    app.add_handler(CommandHandler('sites', list_sites))
    app.add_handler(CallbackQueryHandler(button_handler))
    print('🏗️ Bot running...')
    await app.run_polling()

asyncio.run(main())
"