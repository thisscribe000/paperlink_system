import { Hono } from 'hono'
import { cors } from 'hono/cors'
import { uploadRoute } from './api/upload'
import { filesRoute } from './api/files'
import { linksRoute } from './api/links'
import { serveFileRoute } from './api/serve'

const app = new Hono()

app.use('*', cors())

app.get('/', (c) => c.json({ 
  status: 'ok', 
  service: 'PaperLink Storage',
  environment: 'cloudflare'
}))

app.route('/upload', uploadRoute)
app.route('/api/files', filesRoute)
app.route('/api/links', linksRoute)
app.route('/f', serveFileRoute)

export default app