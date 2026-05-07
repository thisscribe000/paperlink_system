import { Bot } from 'grammy'
import { generateSlug } from '../utils/id'
import { saveFile } from '../storage'
import { db } from '../db'

const bot = new Bot(process.env.TELEGRAM_BOT_TOKEN || '')

const BASE_URL = process.env.BASE_URL || 'http://localhost:3000'

bot.command('start', async (ctx) => {
  await ctx.reply(
    `📦 *PaperLink Storage*\n\n`
    + `Your Telegram-native file storage.\n\n`
    + `*Commands:*\n`
    + `/files — List your files\n`
    + `/upload — Learn how to upload\n`
    + `/share <id> — Get share link\n`
    + `/delete <id> — Delete a file`,
    { parse_mode: 'Markdown' }
  )
})

bot.command('files', async (ctx) => {
  const telegram_id = ctx.from?.id.toString()
  if (!telegram_id) return

  let user = await db.user.findUnique({ where: { telegram_id: BigInt(telegram_id) } })

  if (!user) {
    await ctx.reply('📭 You have no files yet. Just send me any file to upload!')
    return
  }

  const files = await db.file.findMany({
    where: { owner_id: user.id },
    orderBy: { created_at: 'desc' },
    take: 20,
  })

  if (!files.length) {
    await ctx.reply('📭 No files yet. Send me a file to upload!')
    return
  }

  let text = `📁 *Your Files:*\n\n`
  for (const f of files) {
    const link = await db.link.findFirst({ where: { file_id: f.id } })
    text += `• ${f.filename} (${formatSize(f.size)})\n`
    text += `  ID: \`${f.id}\`\n`
    if (link) text += `  Link: ${BASE_URL}/f/${link.url_slug}\n`
    text += '\n'
  }

  await ctx.reply(text, { parse_mode: 'Markdown' })
})

bot.command('share', async (ctx) => {
  const args = ctx.message.text.split(' ').slice(1)
  if (!args[0]) {
    await ctx.reply('Usage: `/share <file_id>`')
    return
  }

  const file = await db.file.findUnique({ where: { id: args[0] } })
  if (!file) {
    await ctx.reply('❌ File not found.')
    return
  }

  let link = await db.link.findFirst({ where: { file_id: file.id } })
  if (!link) {
    const url_slug = generateSlug(8)
    link = await db.link.create({
      data: { file_id: file.id, url_slug },
    })
  }

  await ctx.reply(
    `🔗 *Share Link*\n\n`
    + `${BASE_URL}/f/${link.url_slug}\n\n`
    + `File: ${file.filename}\n`
    + `Size: ${formatSize(file.size)}`,
    { parse_mode: 'Markdown' }
  )
})

bot.command('delete', async (ctx) => {
  const args = ctx.message.text.split(' ').slice(1)
  if (!args[0]) {
    await ctx.reply('Usage: `/delete <file_id>`')
    return
  }

  const file = await db.file.findUnique({ where: { id: args[0] } })
  if (!file) {
    await ctx.reply('❌ File not found.')
    return
  }

  const telegram_id = ctx.from?.id.toString()
  const user = await db.user.findUnique({ where: { telegram_id: BigInt(telegram_id || '0') } })

  if (user && file.owner_id !== user.id) {
    await ctx.reply('❌ Not your file.')
    return
  }

  await db.link.deleteMany({ where: { file_id: file.id } })
  await db.file.delete({ where: { id: file.id } })

  await ctx.reply('🗑️ File deleted.')
})

bot.on('message', async (ctx) => {
  const msg = ctx.message

  if (msg.photo) {
    await ctx.reply('📸 Processing photo...')
    const file = await ctx.getFile()
    const buffer = await downloadFile(file.file_path)
    if (!buffer) {
      await ctx.reply('❌ Failed to download file.')
      return
    }

    const storage_key = generateSlug(16)
    await saveFile(storage_key, buffer)

    let user = await getOrCreateUser(ctx.from?.id.toString(), ctx.from?.username)

    const dbFile = await db.file.create({
      data: {
        storage_key,
        filename: `photo_${Date.now()}.jpg`,
        mime_type: 'image/jpeg',
        size: buffer.byteLength,
        owner_id: user.id,
        is_public: true,
      },
    })

    const url_slug = generateSlug(8)
    await db.link.create({
      data: { file_id: dbFile.id, url_slug },
    })

    await ctx.reply(
      `✅ *Uploaded!*\n\n`
      + `Link: ${BASE_URL}/f/${url_slug}\n`
      + `ID: \`${dbFile.id}\``,
      { parse_mode: 'Markdown' }
    )
  }
  else if (msg.document) {
    await ctx.reply('📄 Processing document...')
    const doc = msg.document
    const file = await ctx.getFile()
    const buffer = await downloadFile(file.file_path)

    if (!buffer) {
      await ctx.reply('❌ Failed to download file.')
      return
    }

    let user = await getOrCreateUser(ctx.from?.id.toString(), ctx.from?.username)

    const dbFile = await db.file.create({
      data: {
        storage_key: generateSlug(16),
        filename: doc.file_name || 'document',
        mime_type: doc.mime_type || 'application/octet-stream',
        size: doc.size || buffer.byteLength,
        owner_id: user.id,
        is_public: true,
      },
    })

    await saveFile(dbFile.storage_key, buffer)

    const url_slug = generateSlug(8)
    await db.link.create({
      data: { file_id: dbFile.id, url_slug },
    })

    await ctx.reply(
      `✅ *Uploaded!*\n\n`
      + `File: ${doc.file_name}\n`
      + `Link: ${BASE_URL}/f/${url_slug}\n`
      + `ID: \`${dbFile.id}\``,
      { parse_mode: 'Markdown' }
    )
  }
})

async function getOrCreateUser(telegram_id: string | undefined, username: string | undefined) {
  if (!telegram_id) throw new Error('No telegram_id')

  let user = await db.user.findUnique({ where: { telegram_id: BigInt(telegram_id) } })
  if (!user) {
    user = await db.user.create({
      data: {
        telegram_id: BigInt(telegram_id),
        username: username || null,
      },
    })
  }
  return user
}

async function downloadFile(file_path: string): Promise<ArrayBuffer | null> {
  try {
    const response = await fetch(`https://api.telegram.org/file/bot${process.env.TELEGRAM_BOT_TOKEN}/${file_path}`)
    return await response.arrayBuffer()
  } catch {
    return null
  }
}

function formatSize(bytes: number): string {
  if (bytes < 1024) return `${bytes}B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)}MB`
}

export async function startBot() {
  const token = process.env.TELEGRAM_BOT_TOKEN
  if (!token || token === 'your_bot_token_here') {
    console.log('⚠️  No Telegram bot token (TELEGRAM_BOT_TOKEN). Bot disabled.')
    return
  }
  console.log('🤖 Starting Telegram bot...')
  try {
    await bot.start()
    console.log('✅ Bot is running!')
  } catch (e: any) {
    console.error('❌ Bot failed to start:', e.message)
  }
}

export { bot }