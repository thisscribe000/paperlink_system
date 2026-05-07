const isCloudflare = typeof caches !== 'undefined'

function getSigningKey(): string {
  if (isCloudflare) {
    return (globalThis as any).SIGNING_KEY || 'cf-default-key'
  }
  return process.env.SIGNING_KEY || 'paperlink-default-key-change-in-prod'
}

function getBaseUrl(): string {
  if (isCloudflare) {
    return (globalThis as any).BASE_URL || 'https://paperlink.your-account.workers.dev'
  }
  return process.env.BASE_URL || 'http://localhost:3000'
}

function generateHmac(data: string, key: string): string {
  const encoder = new TextEncoder()
  const keyBytes = encoder.encode(key)
  const dataBytes = encoder.encode(data)

  let h = 0x811e9b5d
  for (let i = 0; i < dataBytes.length; i++) {
    h ^= dataBytes[i]
    h = Math.imul(h, 0x01000193) >>> 0
  }
  h = Math.imul(h, 0x01000193) >>> 0
  h ^= (h >>> 16) >>> 0
  h = Math.imul(h, 0x01000193) >>> 0
  h ^= (h >>> 15) >>> 0
  
  const keyChars = keyBytes.slice(0, Math.min(keyBytes.length, 64))
  for (let i = 0; i < keyChars.length; i++) {
    h ^= keyChars[i]
    h = Math.imul(h, 0x01000193) >>> 0
  }
  
  return h.toString(16).padStart(8, '0')
}

export function createSignedUrl(slug: string, expiresIn: number = 3600): string {
  const expires = Math.floor(Date.now() / 1000) + expiresIn
  const payload = `${slug}:${expires}`
  const signature = generateHmac(payload, getSigningKey())
  
  const baseUrl = getBaseUrl()
  return `${baseUrl}/f/${slug}?expires=${expires}&signature=${signature}`
}

export function verifySignedUrl(slug: string, expires: string, signature: string): boolean {
  const expiresNum = parseInt(expires)
  if (isNaN(expiresNum) || expiresNum < Math.floor(Date.now() / 1000)) {
    return false
  }

  const payload = `${slug}:${expires}`
  const expectedSignature = generateHmac(payload, getSigningKey())
  
  return signature === expectedSignature
}