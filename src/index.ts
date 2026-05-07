import { Hono } from 'hono'
import { cors } from 'hono/cors'
import { serve } from '@hono/node-server'
import { uploadRoute } from './api/upload'
import { filesRoute } from './api/files'
import { linksRoute } from './api/links'
import { serveFileRoute } from './api/serve'
import { startBot } from './bot'

const app = new Hono()

app.use('*', cors())

app.get('/', (c) => c.json({ status: 'ok', service: 'PaperLink Storage' }))

app.route('/upload', uploadRoute)
app.route('/api/files', filesRoute)
app.route('/api/links', linksRoute)
app.route('/f', serveFileRoute)

async function main() {
  const port = parseInt(process.env.PORT || '3000')

  startBot().catch(console.error)

  console.log(`🚀 PaperLink Storage running on port ${port}`)
  serve({ fetch: app.fetch, port })
}

main()