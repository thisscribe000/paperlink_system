import { Hono } from 'hono'
import { cors } from 'hono/cors'
import { uploadRoute } from './api/upload'
import { filesRoute } from './api/files'
import { linksRoute } from './api/links'
import { serveFileRoute } from './api/serve'
import { startBot } from './bot'

const app = new Hono()

app.use('*', cors())

app.get('/', (c) => c.json({ 
  status: 'ok', 
  service: 'PaperLink Storage',
  environment: 'node'
}))

app.route('/upload', uploadRoute)
app.route('/api/files', filesRoute)
app.route('/api/links', linksRoute)
app.route('/f', serveFileRoute)

const port = parseInt(process.env.PORT || '3000')
console.log(`🚀 PaperLink Storage running on port ${port}`)

const server = Bun.serve({
  port,
  fetch: app.fetch,
})
console.log(`Server started on ${server.hostname}:${server.port}`)

startBot()