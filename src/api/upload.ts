import { Hono } from 'hono'
import { PrismaClient } from '@prisma/client'
import { generateSlug } from '../utils/id'
import { saveFile } from '../storage'
import { trackUpload } from '../utils/analytics'

const db = new PrismaClient()

export const uploadRoute = new Hono()

uploadRoute.post('/', async (c) => {
  try {
    const body = await c.req.parseBody()
    const file = body['file'] as File | undefined

    if (!file) {
      return c.json({ error: 'No file provided' }, 400)
    }

    const storage_key = generateSlug(16)
    const filename = (file as any).name || 'upload'
    const mime_type = (file as any).type || 'application/octet-stream'
    const size = (file as any).size || 0

    const buffer = await file.arrayBuffer()
    await saveFile(storage_key, buffer)

    const url_slug = generateSlug(8)

    const fileRecord = await db.file.create({
      data: {
        storage_key,
        filename,
        mime_type,
        size,
        owner_id: null,
        is_public: true,
      },
    })

    await db.link.create({
      data: {
        file_id: fileRecord.id,
        url_slug,
      },
    })

    await trackUpload(fileRecord.owner_id || 'anonymous', size)

    const base_url = process.env.BASE_URL || 'http://localhost:3000'

    return c.json({
      id: fileRecord.id,
      url_slug,
      url: `${base_url}/f/${url_slug}`,
      filename,
      size,
      mime_type,
    })
  } catch (error) {
    console.error('Upload error:', error)
    return c.json({ error: 'Upload failed' }, 500)
  }
})