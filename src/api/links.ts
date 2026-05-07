import { Hono } from 'hono'
import { PrismaClient } from '@prisma/client'
import { generateSlug } from '../utils/id'
import { createSignedUrl } from '../utils/signed-url'

const db = new PrismaClient()

export const linksRoute = new Hono()

linksRoute.post('/', async (c) => {
  try {
    const { file_id, expires_in, password } = await c.req.json()

    const file = await db.file.findUnique({ where: { id: file_id } })
    if (!file) {
      return c.json({ error: 'File not found' }, 404)
    }

    const url_slug = generateSlug(8)
    let expires_at = null

    if (expires_in) {
      const hours = parseInt(expires_in)
      expires_at = new Date(Date.now() + hours * 60 * 60 * 1000)
    }

    const link = await db.link.create({
      data: {
        file_id,
        url_slug,
        expires_at,
        password: password || null,
      },
    })

    const base_url = process.env.BASE_URL || 'http://localhost:3000'

    return c.json({
      id: link.id,
      url_slug,
      url: `${base_url}/f/${url_slug}`,
      expires_at,
    })
  } catch (error) {
    console.error('Create link error:', error)
    return c.json({ error: 'Failed to create link' }, 500)
  }
})

linksRoute.delete('/:id', async (c) => {
  const id = c.req.param('id')
  await db.link.delete({ where: { id } })
  return c.json({ success: true })
})

linksRoute.post('/signed', async (c) => {
  try {
    const { url_slug, expires_in } = await c.req.json()

    const link = await db.link.findUnique({ where: { url_slug } })
    if (!link) {
      return c.json({ error: 'Link not found' }, 404)
    }

    const expiresSeconds = parseInt(expires_in) || 3600
    const signedUrl = createSignedUrl(url_slug, expiresSeconds)

    return c.json({ signed_url: signedUrl, expires_in: expiresSeconds })
  } catch (error) {
    console.error('Signed URL error:', error)
    return c.json({ error: 'Failed to create signed URL' }, 500)
  }
})