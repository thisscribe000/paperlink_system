import { Hono } from 'hono'
import { PrismaClient } from '@prisma/client'
import { getFileBuffer } from '../storage'
import { trackDownload } from '../utils/analytics'
import { verifySignedUrl } from '../utils/signed-url'

const db = new PrismaClient()

export const serveFileRoute = new Hono()

serveFileRoute.get('/:slug', async (c) => {
  const slug = c.req.param('slug')

  const link = await db.link.findUnique({ where: { url_slug: slug } })

  if (!link) {
    return c.json({ error: 'File not found' }, 404)
  }

  if (link.expires_at && new Date(link.expires_at) < new Date()) {
    return c.json({ error: 'Link expired' }, 410)
  }

  if (link.password) {
    const provided = c.req.query('password')
    if (!provided || provided !== link.password) {
      return c.json({ error: 'Password required' }, 401)
    }
  }

  const signedExpires = c.req.query('expires')
  const signedSignature = c.req.query('signature')
  if (signedExpires && signedSignature) {
    if (!verifySignedUrl(slug, signedExpires, signedSignature)) {
      return c.json({ error: 'Invalid or expired signed URL' }, 403)
    }
  }

  await db.link.update({
    where: { id: link.id },
    data: { click_count: { increment: 1 } },
  })

  await trackDownload(link.file_id)

  const file = await db.file.findUnique({ where: { id: link.file_id } })

  if (!file) {
    return c.json({ error: 'File not found' }, 404)
  }

  const buffer = await getFileBuffer(file.storage_key)

  if (!buffer) {
    return c.json({ error: 'File not found' }, 404)
  }

  return new Response(buffer, {
    headers: {
      'Content-Type': file.mime_type,
      'Content-Disposition': `inline; filename="${file.filename}"`,
      'Cache-Control': 'public, max-age=31536000',
    },
  })
})