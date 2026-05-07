import { PrismaClient } from '@prisma/client'
import { deleteFile } from '../storage'

const db = new PrismaClient()

async function cleanup() {
  console.log('Starting cleanup worker...')

  const now = new Date()

  const expiredLinks = await db.link.findMany({
    where: { expires_at: { lt: now } },
  })
  console.log(`Found ${expiredLinks.length} expired links`)

  await db.link.deleteMany({
    where: { expires_at: { lt: now } },
  })

  const expiredFiles = await db.file.findMany({
    where: { expires_at: { lt: now } },
  })
  console.log(`Found ${expiredFiles.length} expired files`)

  for (const file of expiredFiles) {
    try {
      await deleteFile(file.storage_key)
    } catch (err) {
      console.error(`Failed to delete file ${file.storage_key}:`, err)
    }
  }

  await db.file.deleteMany({
    where: { expires_at: { lt: now } },
  })

  const users = await db.user.findMany()
  for (const user of users) {
    const totalSize = await db.file.aggregate({
      where: { owner_id: user.id },
      _sum: { size: true },
    })
    await db.user.update({
      where: { id: user.id },
      data: { storage_used: totalSize._sum.size || 0 },
    })
  }
  console.log('Updated storage usage for users')

  console.log('Cleanup complete')
}

cleanup()
  .then(() => process.exit(0))
  .catch((err) => {
    console.error('Cleanup failed:', err)
    process.exit(1)
  })