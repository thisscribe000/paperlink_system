import { Hono } from 'hono'
import { PrismaClient } from '@prisma/client'
import { deleteFile } from '../storage'

const db = new PrismaClient()

export const filesRoute = new Hono()

filesRoute.get('/', async (c) => {
  const files = await db.file.findMany({
    orderBy: { created_at: 'desc' },
    take: 100,
  })

  return c.json({ files })
})

filesRoute.get('/:id', async (c) => {
  const id = c.req.param('id')
  const file = await db.file.findUnique({ where: { id } })

  if (!file) {
    return c.json({ error: 'File not found' }, 404)
  }

  return c.json({ file })
})

filesRoute.delete('/:id', async (c) => {
  const id = c.req.param('id')
  const file = await db.file.findUnique({ where: { id } })

  if (!file) {
    return c.json({ error: 'File not found' }, 404)
  }

  await deleteFile(file.storage_key)
  await db.link.deleteMany({ where: { file_id: id } })
  await db.file.delete({ where: { id } })

  return c.json({ success: true })
})