let analytics: KVNamespace | null = null

if (typeof caches !== 'undefined' && typeof ANALYTICS !== 'undefined') {
  analytics = (globalThis as any).ANALYTICS
}

export async function trackDownload(fileId: string, userId?: string): Promise<void> {
  if (!analytics) return

  const today = new Date().toISOString().split('T')[0]
  const key = `downloads:${today}`
  const existing = await analytics.get(key)
  const count = existing ? parseInt(existing) + 1 : 1
  await analytics.put(key, count.toString())

  if (userId) {
    const userKey = `user:${userId}:downloads`
    const userExisting = await analytics.get(userKey)
    const userCount = userExisting ? parseInt(userExisting) + 1 : 1
    await analytics.put(userKey, userCount.toString())
  }
}

export async function trackUpload(userId: string, size: number): Promise<void> {
  if (!analytics) return

  const today = new Date().toISOString().split('T')[0]
  const key = `uploads:${today}`
  const existing = await analytics.get(key)
  const count = existing ? parseInt(existing) + 1 : 1
  await analytics.put(key, count.toString())

  const sizeKey = `uploads:size:${today}`
  const sizeExisting = await analytics.get(sizeKey)
  const totalSize = sizeExisting ? parseInt(sizeExisting) + size : size
  await analytics.put(sizeKey, totalSize.toString())
}

export async function getAnalytics(days: number = 7): Promise<{
  downloads: Record<string, number>
  uploads: Record<string, number>
  uploadSize: Record<string, number>
}> {
  const downloads: Record<string, number> = {}
  const uploads: Record<string, number> = {}
  const uploadSize: Record<string, number> = {}

  if (!analytics) {
    return { downloads, uploads, uploadSize }
  }

  for (let i = 0; i < days; i++) {
    const date = new Date()
    date.setDate(date.getDate() - i)
    const today = date.toISOString().split('T')[0]

    const dl = await analytics.get(`downloads:${today}`)
    downloads[today] = dl ? parseInt(dl) : 0

    const up = await analytics.get(`uploads:${today}`)
    uploads[today] = up ? parseInt(up) : 0

    const sz = await analytics.get(`uploads:size:${today}`)
    uploadSize[today] = sz ? parseInt(sz) : 0
  }

  return { downloads, uploads, uploadSize }
}